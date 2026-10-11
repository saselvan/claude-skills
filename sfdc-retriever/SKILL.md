---
name: sfdc-retriever
description: Wrapper retriever for Salesforce data via Glean. Queries SFDC deal stage, pipeline, AE notes, activity history using Glean's SFDC-indexed content. Conforms to retriever-contract.md.
model: claude-haiku-4-5-20251001
context: fork
user-invocable: true
---

# sfdc-retriever

**Haiku agent** that retrieves Salesforce data (deal stage, pipeline, AE notes, activity history) via Glean's SFDC-indexed content. Returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What is the current SFDC pipeline for NWM?"
- "What stage is the NWM GenAI opportunity at?"
- "What AE notes exist for CHN's renewal?"
- "What is the SFDC activity history for NWM in the last 90 days?"

**Model:** claude-haiku-4-5-20251001
**Context budget:** fork (isolated, ~20k tokens)
**Input:** Account name + query intent + optional opportunity/UCO filter
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: sfdc
query_intent: string
scope:
  account_id: string (e.g., "nwm", "chn")
  time_window: string (optional, e.g., "30days", "90days")
  filters:
    opportunity_name: string (optional -- specific opportunity to look up)
    uco_name: string (optional -- specific UCO to look up)
    record_type: string (optional -- e.g., "opportunity", "account", "contact", "activity")
```

---

## Retrieval Process (4 steps)

### Step 1: Map Account Slug to SFDC Name

Resolve account_id to full SFDC account name:

| Slug | SFDC Account Name |
|---|---|
| nwm | Northwestern Medicine |
| chn | Community Health Network |

Use `vault_summary(account_id)` to get the canonical account name if not in the mapping.

### Step 2: Execute SFDC-Filtered Glean Search

Call `mcp__glean__search` with SFDC-specific query construction:

**For opportunity lookups:**
```
mcp__glean__search(query="Salesforce {account_name} opportunity {opportunity_name}", page_size=10)
```

**For pipeline overview:**
```
mcp__glean__search(query="Salesforce {account_name} pipeline opportunity stage", page_size=10)
```

**For AE notes / activity:**
```
mcp__glean__search(query="Salesforce {account_name} activity notes {time_context}", page_size=10)
```

**For UCO lookups:**
```
mcp__glean__search(query="Salesforce {account_name} UCO {uco_name}", page_size=10)
```

Filter results to prioritize Salesforce-sourced documents over other sources.

### Step 3: Fetch Document Content (Top SFDC Results)

For the top 3 SFDC-sourced results, call `mcp__glean__get_document_content`:

```
mcp__glean__get_document_content(document_id="{doc_id}")
```

Extract:
- Deal stage (if opportunity)
- Close date
- Amount / ARR
- AE notes
- Activity history entries
- Last modified date

### Step 4: Compute Confidence & Fallback Interrogation

Confidence based on SFDC result quality:
- **3+ SFDC results** with deal stage, amount, and recent activity -> high
- **1-2 SFDC results** or results missing key fields (stage, amount) -> medium
- **0 SFDC results** or only non-SFDC results -> low

Freshness check:
- Most recent SFDC activity < 14 days -> confidence boost
- Most recent SFDC activity 14-30 days -> no change
- Most recent SFDC activity > 30 days -> downgrade by one level (high->medium, medium->low)

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: sfdc-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [databricks_internal]
recency: {ISO8601 of most recent SFDC record}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# {Account Name} -- SFDC Intelligence

## Pipeline Summary

| Opportunity | Stage | Amount | Close Date | Last Activity |
|------------|-------|--------|------------|---------------|
| {name} | {stage} | ${amount} | {date} | {date} |
...

## AE Notes (Recent)

### {Date} -- {AE Name}
{Note content summary}

### {Date} -- {AE Name}
{Note content summary}

## Activity History

| Date | Type | Subject | Owner |
|------|------|---------|-------|
| {date} | {call|email|meeting|task} | {subject} | {name} |
...

## UCO Status (if queried)

| UCO | Stage | Status | Notes |
|-----|-------|--------|-------|
| {name} | {stage} | {status} | {notes} |

---

## Confidence Assessment

**Confidence:** {high|medium|low}
**Source Count:** {n}
**Source Tiers:** [databricks_internal]
**Recency:** {date of most recent SFDC record}
**SFDC Freshness:** {days since last SFDC activity}

{Explanation of confidence level}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope -- or null if high confidence}
```

---

## Telemetry

After every invocation, log to `vault_speaker_invocations` in brain.db:

```python
import sqlite3, secrets, json, time

db = sqlite3.connect("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")
db.execute("""
    INSERT INTO vault_speaker_invocations
    (invocation_id, run_id, intent, scope, retriever_set, latency_ms, outcome_tag)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    secrets.token_hex(16),
    secrets.token_hex(16),
    intent,
    json.dumps({"account_id": account_id}),
    json.dumps(["sfdc-retriever"]),
    latency_ms,
    None  # populated in W3-W4
))
db.commit()
db.close()
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Maps account_id slug to SFDC account name
- [ ] Calls mcp__glean__search with SFDC-specific query construction
- [ ] Filters results to prioritize Salesforce-sourced documents
- [ ] Calls mcp__glean__get_document_content for top 3 SFDC results
- [ ] Extracts deal stage, amount, close date, AE notes, activity history
- [ ] Computes source_count from SFDC-specific results only
- [ ] Applies confidence logic:
  - 3+ SFDC results with key fields -> high
  - 1-2 SFDC results or missing fields -> medium
  - 0 SFDC results -> low
- [ ] Applies freshness downgrade (> 30 days since last activity)
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (escalate|research|queue)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id to vault_speaker_invocations (sqlite3, ? params)
- [ ] Source tier: databricks_internal

---

## Test Case 1: High Confidence (NWM, active pipeline)

**Input:**
```yaml
entity_type: sfdc
query_intent: "What is NWM's current SFDC pipeline and deal stages?"
scope:
  account_id: nwm
  time_window: 90days
```

**Expected Output:**
- confidence: high
- source_count: >= 3
- degradation_flags: []
- fallback_interrogation: null
- Pipeline table with opportunities, stages, amounts
- AE notes from last 14 days
- Activity history present

**Validation:**
- Glean returns 3+ SFDC-sourced documents for NWM
- Deal stage and amount are populated
- Recent SFDC activity exists (< 14 days)

---

## Test Case 2: Medium Confidence (CHN, sparse SFDC data)

**Input:**
```yaml
entity_type: sfdc
query_intent: "What AE notes exist for CHN's renewal?"
scope:
  account_id: chn
  filters:
    record_type: activity
```

**Expected Output:**
- confidence: medium
- source_count: 1-2
- degradation_flags: [sparse_data]
- fallback_interrogation:
  - question: "Only 1-2 SFDC records found for CHN. Is SFDC data up to date?"
  - intent: validate
  - scope: { suggested_approach: "Check SFDC directly for CHN activity. AE may not be logging notes." }

**Validation:**
- Limited SFDC records found via Glean
- Suggests verifying SFDC data directly
- Does not fabricate AE notes

---

## Test Case 3: Low Confidence (No SFDC results)

**Input:**
```yaml
entity_type: sfdc
query_intent: "What is account X's SFDC pipeline?"
scope:
  account_id: account_x
  time_window: 30days
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation:
  - question: "No SFDC data found for account_x via Glean. Is this account in Salesforce?"
  - intent: escalate
  - scope: { needed_tier: databricks_internal, suggested_approach: "Verify account exists in SFDC. Search SFDC directly if Glean indexing is delayed." }

**Validation:**
- No SFDC records found
- Clear escalation path
- Suggests direct SFDC lookup as fallback

---

## Error Handling

### Glean Auth Failure
If `mcp__glean__search` returns an auth error:
```yaml
confidence: low
source_count: 0
degradation_flags: [missing_context]
fallback_interrogation:
  question: "Glean MCP authentication failed. Cannot retrieve SFDC data."
  intent: escalate
  scope:
    suggested_approach: "Check Glean MCP auth token. Access SFDC directly at login.salesforce.com."
```

### No SFDC-Sourced Results
If Glean returns results but none are from Salesforce:
```yaml
confidence: low
degradation_flags: [incomplete]
fallback_interrogation:
  question: "Glean returned results but none from Salesforce. SFDC may not be indexed for this account."
  intent: research
  scope:
    suggested_approach: "Check if SFDC data is indexed in Glean. Try direct SFDC search."
    non_sfdc_results_found: true
```

### Stale SFDC Data
If most recent SFDC record is > 30 days old:
```yaml
degradation_flags: [outdated]
fallback_interrogation:
  question: "Most recent SFDC activity is {n} days old. Pipeline data may be stale."
  intent: validate
  scope:
    suggested_approach: "Check if AE has logged recent activity. SFDC may be out of date."
```

---

## Deployment

Skills directory: `~/.claude/skills/sfdc-retriever/`

Run:
```
/sfdc-retriever --input '{
  "entity_type": "sfdc",
  "query_intent": "What is NWM's current SFDC pipeline?",
  "scope": {
    "account_id": "nwm",
    "time_window": "90days"
  }
}'
```

---

## Notes

- SFDC data is accessed via Glean (Glean indexes Salesforce) -- there is no direct SFDC API call
- For general Glean queries (not SFDC-specific), use the glean-retriever instead
- This retriever adds SFDC-specific query construction and result filtering on top of Glean
- Confidence is deterministic: SFDC result count + freshness are the main drivers
- Source tier is always `databricks_internal` (SFDC data accessed through internal Glean)
- Never fabricate deal stages, amounts, or AE notes -- only report what Glean returns
- UCO (Use Case Opportunity) is Databricks-specific SFDC object -- query with "UCO" prefix

---

**Version:** 1.0
**Last Updated:** 2026-04-19
**Contract Reference:** `_System/retriever-contract.md` (immutable)
