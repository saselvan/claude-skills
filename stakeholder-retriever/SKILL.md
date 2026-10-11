# stakeholder-retriever

**Haiku agent** that queries stakeholder profile, influence, recent stance shifts, and commitment status. Returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What is Bob Slavieck's current stance on Fabric vs Databricks?"
- "Is Camila still the decision-maker on Epic architecture?"
- "How is Paul Lendman aligned with our Epic proposal?"

**Model:** claude-haiku-4-5-20251001  
**Context budget:** fork (isolated, ~20k tokens)  
**Input:** Stakeholder name + account context  
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: stakeholder
query_intent: string
scope:
  account_id: string (e.g., "nwm", "chn")
  filters:
    stakeholder_name: string (required, e.g., "Bob Slavieck")
    role_type: string (optional, e.g., "champion", "blocker", "economic-buyer")
```

---

## Retrieval Process (4 steps)

### Step 1: Load Stakeholder File
- Query: `vault_entity_lookup(name=stakeholder_name, entity_type="stakeholder")`
- Extract: title, influence score, stance, relationship strength, tags
- Confidence seed: If file exists and is detailed → boost

### Step 2: Load Recent Sessions
- Query: `vault_search(query=stakeholder_name, account=account_id, limit=3)`
- Extract: last 3 sessions involving stakeholder, sentiment, statements, commitments
- Recency: Use most recent session timestamp
- Confidence impact: Sessions within 14 days boost confidence; > 30 days degrade

### Step 3: Load Signals
- Query: `vault_signals(account=account_id, stakeholder=stakeholder_name)`
- Extract: action items assigned to/owned by stakeholder, commitments, risks involving them
- Source tier: signal_database

### Step 4: Load Artifacts
- Query: `vault_search(query="artifacts", account=account_id)`
- Filter for artifacts presented to this stakeholder
- Extract: artifact type, date, outcome notes if available

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: stakeholder-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [list of tiers found]
recency: {ISO8601 of most recent session}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# {Stakeholder Name}

## Profile

| Field | Value |
|-------|-------|
| Title | {title} |
| Role Type | {champion|blocker|economic-buyer|technical-buyer|coach} |
| Influence Score | {0-10} |
| Relationship Strength | {weak|moderate|strong} |
| Account | {account name} |
| Direct Manager | {name or unknown} |

## Current Stance & Trajectory

{Summary of current position on key decisions (e.g., Fabric vs Databricks, Epic priority, etc.)}

**Last Updated:** {date of most recent session}

### Recent Sessions ({count})

| Date | Type | Key Sentiment | Commitments | Owner Follow-up |
|------|------|---------------|-------------|-----------------|
| {date} | {session type} | {positive|neutral|concerned} | {commitments if any} | {owner or none} |
...

## Commitments & Action Items

| Commitment | Due Date | Status | Owner |
|------------|----------|--------|-------|
| {commitment} | {date} | {open|in_progress|completed} | {owner} |
...

## Topics of Interest

{High-level interests: Epic, Fabric, OMOP, etc. based on sessions and artifacts}

## Artifacts Presented to {Stakeholder}

| Artifact | Type | Date | Topic | Outcome |
|----------|------|------|-------|---------|
| {artifact} | {type} | {date} | {topic} | {outcome if known} |
...

---

## Confidence Assessment

**Confidence:** {high|medium|low}  
**Source Count:** {n}  
**Source Tiers:** {list}  
**Recency:** {date of most recent source}

{Explanation of confidence}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope — or null if high confidence}
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope, filters)
- [ ] Calls vault_entity_lookup for stakeholder file
- [ ] Calls vault_search for recent sessions (limit=3)
- [ ] Calls vault_signals for stakeholder-related signals
- [ ] Calls vault_search for artifacts presented to stakeholder
- [ ] Computes source_count:
  - File + 2+ sessions → 3+
  - File + 1 session → 2
  - File only → 1
  - No file → 0
- [ ] Applies confidence logic:
  - 3+ sources + session ≤ 14 days → high
  - 1-2 sources OR session > 30 days → medium
  - 0 sources OR file doesn't exist → low
- [ ] Adds degradation_flags if confidence < high:
  - outdated: session > 30 days
  - single_thread: only one session mentions this stakeholder
  - missing_context: no file found
- [ ] Generates fallback_interrogation with intent
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id for telemetry

---

## Test Case 1: High Confidence (Bob Slavieck, NWM)

**Input:**
```yaml
entity_type: stakeholder
query_intent: "What is Bob Slavieck's current stance on Fabric vs Databricks?"
scope:
  account_id: nwm
  filters:
    stakeholder_name: "Bob Slavieck"
```

**Expected Output:**
- confidence: high
- source_count: ≥ 3 (file + 2 sessions + signals)
- degradation_flags: []
- fallback_interrogation: null

**Validation:**
- Stakeholder file exists (NWM directory)
- Recent session within 14 days mentions Bob
- Signals/commitments involving Bob are current
- Stance on Fabric vs Databricks is documented

---

## Test Case 2: Medium Confidence (Stale Stakeholder)

**Input:**
```yaml
entity_type: stakeholder
query_intent: "What is Camila Altman's current priority?"
scope:
  account_id: nwm
  filters:
    stakeholder_name: "Camila Altman"
```

**Expected Output:**
- confidence: medium
- source_count: 1-2
- degradation_flags: [outdated]
- fallback_interrogation: "Last session was {days} ago. Suggest checking in to confirm current priorities."

**Validation:**
- Stakeholder file exists
- Most recent session > 30 days old
- Stance may have shifted
- Recommends validation from customer

---

## Test Case 3: Low Confidence (Unknown Stakeholder)

**Input:**
```yaml
entity_type: stakeholder
query_intent: "What is unknown_person's role in the CHLA account?"
scope:
  account_id: chla
  filters:
    stakeholder_name: "unknown_person"
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation: "No file found for unknown_person. Should we create a stakeholder profile?"

**Validation:**
- Vault returns no results
- Raises question for downstream processing

---

## Single-Threading Detection

**Special case:** If stakeholder appears in only 1 session and no other signal sources:

```yaml
degradation_flags: [single_thread]
fallback_interrogation:
  question: "Only Bob mentioned Fabric priority in one session. Is this the authoritative voice, or should we validate with Camila?"
  intent: validate
  scope:
    suggested_approach: "Ask Camila to confirm if Bob's stance aligns with hers"
```

---

## Deployment

Skills directory: `~/.claude/skills/stakeholder-retriever/`

Run:
```
/stakeholder-retriever --input '{
  "entity_type": "stakeholder",
  "query_intent": "What is Bob Slavieck'\''s current stance on Fabric?",
  "scope": {
    "account_id": "nwm",
    "filters": {
      "stakeholder_name": "Bob Slavieck"
    }
  }
}'
```

---

## Notes

- Recency matters heavily for stakeholders; sentiment shifts fast
- If only one session mentions a stakeholder, flag single_thread degradation
- Stakeholder files may be stale; sessions are the ground truth
- Influence and decision power are often implicit; infer from outcomes (whose commitment matters?)
- Manager relationships (who reports to whom) signal influence chains

---

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Contract Reference:** `_System/retriever-contract.md` (immutable)
