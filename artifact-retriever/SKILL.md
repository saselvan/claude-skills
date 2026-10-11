# artifact-retriever

**Haiku agent** that queries artifacts presented to an account, their outcomes, and usage patterns. Returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What artifacts have we presented to NWM around Epic integration?"
- "Did the deck on Fabric vs Databricks result in follow-up?"
- "What's our track record of presentations to Camila?"

**Model:** claude-haiku-4-5-20251001  
**Context budget:** fork (isolated, ~20k tokens)  
**Input:** Account + optional topic/artifact type filters  
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: artifact
query_intent: string
scope:
  account_id: string (e.g., "nwm", "chn")
  time_window: string (optional, e.g., "90days", "ytd")
  filters:
    topic: string (optional, e.g., "Epic", "Fabric", "OMOP")
    artifact_type: [string] (optional, e.g., ["deck", "one_pager"])
    presented_to: string (optional, stakeholder name)
```

---

## Retrieval Process (4 steps)

### Step 1: Query Artifacts Table
- Query: `vault_search(query="artifacts", account=account_id, limit=50)`
- Filter by topic, artifact_type if specified
- Filter by time_window if specified
- Extract: artifact ID, type, date created, title

### Step 2: Load Artifact Metadata
- For each artifact found, load the .artifact.md sidecar file
- Extract: title, artifact_type, created_date, source_skill
- Extract: related_session if present (links to outcomes)

### Step 3: Link to Sessions & Outcomes
- Query: `vault_search(query=artifact_title, entity_type="session")`
- Find sessions where artifact was presented
- Extract: session date, attendees, outcome notes
- Confidence boost: If session mentions specific outcome (e.g., "resulted in commitment") → high

### Step 4: Compute Confidence & Fallback Interrogation
- If artifacts found + outcomes documented → high
- If artifacts found, no outcomes → medium
- If no artifacts found → low with fallback_interrogation

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: artifact-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [list of tiers found]
recency: {ISO8601 of most recent artifact}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# Artifacts Presented to {Account Name}

## Summary

{Total count}: {n} artifacts found  
**Topic Filter:** {topic or "all"}  
**Artifact Types:** {types}  
**Time Window:** {window}  
**Confidence:** {high|medium|low}

## Artifacts by Type

### Decks ({count})

| Date | Title | Topic | Presented To | Outcome | Status |
|------|-------|-------|--------------|---------|--------|
| {date} | {title} | {topic} | {stakeholder(s)} | {outcome if known} | {outcome_status} |
...

### One-Pagers ({count})

| Date | Title | Topic | Presented To | Outcome |
|------|-------|-------|--------------|---------|
...

### Cheatsheets ({count})

| Date | Title | Topic | Outcome |
|------|-------|-------|---------|
...

### Other ({count})

| Date | Type | Title | Outcome |
|------|------|-------|---------|
...

## Outcomes & Impact

{Summary of known outcomes:}
- {Artifact} led to {outcome} (confirmed in session {date})
- {Artifact} resulted in {specific commitment} (owner: {name})
- {Artifact} generated {follow-up action item}

{If outcomes unknown:} No documented outcomes for presented artifacts. See fallback_interrogation.

## Patterns & Insights

{Any observations about what topics/formats work well with this account}

### High-Impact Topics
- {Topic}: {# successful presentations, pattern}

### Low-Engagement Topics
- {Topic}: {# presentations with no documented follow-up}

---

## Confidence Assessment

**Confidence:** {high|medium|low}  
**Source Count:** {n}  
**Source Tiers:** {list}  
**Recency:** {date of most recent artifact}

{Explanation of confidence}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope — or null if high confidence}
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope, filters)
- [ ] Calls vault_search for artifacts (limit=50, account=account_id)
- [ ] Filters by topic, artifact_type, time_window if specified
- [ ] For each artifact found: loads .artifact.md sidecar
- [ ] Links artifacts to sessions via vault_search
- [ ] Extracts outcome information from session notes
- [ ] Computes source_count:
  - Artifacts found + outcomes documented → 3+
  - Artifacts found, outcomes unknown → 1-2
  - No artifacts found → 0
- [ ] Applies confidence logic:
  - source_count ≥ 3 → high
  - source_count 1-2 → medium
  - source_count 0 → low
- [ ] Adds degradation_flags if confidence < high:
  - missing_context: no artifacts found for this query
  - incomplete: artifacts found but no outcomes documented
  - sparse_data: only 1-2 artifacts found (may need broader search)
- [ ] Generates fallback_interrogation with intent (research|escalate|queue)
- [ ] Organizes artifacts by type in output
- [ ] Includes pattern insights if 3+ artifacts of same type exist
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id for telemetry

---

## Test Case 1: High Confidence (NWM, Multiple Artifacts with Outcomes)

**Input:**
```yaml
entity_type: artifact
query_intent: "What artifacts have we presented to NWM around Epic integration?"
scope:
  account_id: nwm
  filters:
    topic: "Epic"
    artifact_type: ["deck", "one_pager"]
```

**Expected Output:**
- confidence: high
- source_count: ≥ 3 (multiple artifacts + documented outcomes)
- degradation_flags: []
- fallback_interrogation: null

**Validation:**
- 2+ artifacts found with Epic in title
- Outcomes documented in session notes
- Artifacts are recent (within artifact_type filter if specified)

---

## Test Case 2: Medium Confidence (Artifacts, Unknown Outcomes)

**Input:**
```yaml
entity_type: artifact
query_intent: "What's our artifact history with CHN?"
scope:
  account_id: chn
  time_window: 90days
```

**Expected Output:**
- confidence: medium
- source_count: 1-2
- degradation_flags: [incomplete]
- fallback_interrogation: "Artifacts found but outcomes not documented. Should we check session notes for follow-up?"

**Validation:**
- Artifacts exist for account
- But session linkage or outcome data is missing
- Suggests checking sessions manually for implicit outcomes

---

## Test Case 3: Low Confidence (No Artifacts Found)

**Input:**
```yaml
entity_type: artifact
query_intent: "What Epic artifacts have we presented in the last 30 days?"
scope:
  account_id: nwm
  time_window: 30days
  filters:
    topic: "Epic"
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation: "No Epic artifacts found in last 30 days. Should we schedule a presentation or expand time window?"

**Validation:**
- Query returns no results
- Suggests next steps (create, present, or expand search)

---

## Outcome Types

Recognize and extract these outcome patterns from sessions:

- **Commitment:** "Customer committed to X"
- **Follow-up Action:** "Customer agreed to Y"
- **Feedback:** "Customer wants Z"
- **Objection:** "Customer concerned about W"
- **Next Step:** "Customer scheduled follow-up for {date}"
- **None Documented:** "Artifact presented, but outcome not recorded"

---

## Presentation to Specific Stakeholder

**Special case:** If `presented_to` filter is specified:

```yaml
filters:
  presented_to: "Camila Altman"
```

- Query sessions where Camila was an attendee + artifact was discussed
- Track: How many times have we presented to Camila? What topics? What outcomes?
- Highlight: Camila's individual response pattern (does she ask follow-up questions? commit to actions?)

---

## Deployment

Skills directory: `~/.claude/skills/artifact-retriever/`

Run:
```
/artifact-retriever --input '{
  "entity_type": "artifact",
  "query_intent": "What Epic artifacts have we presented to NWM?",
  "scope": {
    "account_id": "nwm",
    "filters": {
      "topic": "Epic",
      "artifact_type": ["deck"]
    }
  }
}'
```

---

## Notes

- Outcomes are often implicit in session notes; retrieve the actual session to extract them
- If artifact has a related_session field in metadata, use that as primary linkage
- Pattern insights require 3+ artifacts; don't force patterns with fewer samples
- Time window filters matter: recent artifacts may not yet have sessions with documented outcomes
- Presentation frequency (how many times have we pitched X topic?) is a confidence signal

---

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Contract Reference:** `_System/retriever-contract.md` (immutable)
