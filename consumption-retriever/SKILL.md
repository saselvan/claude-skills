---
name: consumption-retriever
description: Wrapper retriever for Databricks consumption data. Invokes consumption-vault-sync, returns DBU trends, WoW/MoM growth, and anomalies conforming to retriever-contract.md.
model: claude-haiku-4-5-20251001
context: fork
user-invocable: true
---

# consumption-retriever

**Haiku agent** that retrieves Databricks consumption intelligence for an account. Wraps the `consumption-vault-sync` skill and returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What is NWM's current DBU consumption trend?"
- "Is NWM's consumption growing or declining WoW?"
- "Are there any consumption anomalies or churn risks for CHN?"

**Model:** claude-haiku-4-5-20251001
**Context budget:** fork (isolated, ~20k tokens)
**Input:** Account ID + query intent
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: consumption
query_intent: string
scope:
  account_id: string (e.g., "nwm", "chn")
  time_window: string (optional, e.g., "30days", "90days")
  filters: dict (optional)
```

---

## Retrieval Process (4 steps)

### Step 1: Invoke consumption-vault-sync

Invoke the `/consumption-vault-sync` skill to ensure latest consumption data is synced to the vault. Use the account mapping:

| Account Slug | SFDC Account ID | Account Name |
|---|---|---|
| nwm | 0016100000cF3SpAAK | Northwestern Medicine |
| chn | (lookup from vault) | Community Health Network |

If the skill has already been run within the last 7 days (check vault signals for recent `metrics` signal_type), skip re-invocation and use cached data.

### Step 2: Query Vault for Consumption Signals

- Query: `vault_signals(account=account_id, signal_type="metrics")`
- Query: `vault_signals(account=account_id, signal_type="risk")`
- Query: `vault_signals(account=account_id, signal_type="opportunity")`
- Extract: weekly spend, WoW growth, SWLY growth, health score, churn risk, expansion signal, product mix

### Step 3: Analyze Freshness

Determine data freshness from the most recent signal timestamp:
- **< 7 days old**: confidence boost (data is current)
- **7-30 days old**: confidence = medium (data may be stale)
- **> 30 days old**: confidence = low (data is outdated, needs refresh)

### Step 4: Compute Confidence & Fallback Interrogation

- If consumption data found AND < 7 days old AND source_count >= 3 -> high
- If consumption data found AND 7-30 days old OR source_count 1-2 -> medium
- If no consumption data OR > 30 days old -> low with fallback_interrogation

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: consumption-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [databricks_internal]
recency: {ISO8601 of most recent consumption data}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# {Account Name} — Consumption Intelligence

## Current Week Summary

| Metric | Value |
|--------|-------|
| Weekly Spend | ${amount} |
| WoW Growth | {percent}% |
| SWLY Growth | {percent}% |
| Health Score | {Healthy|At Risk|Critical} |
| Churn Risk | {0-1 score} |
| Expansion Signal | {0-1 score} |

## Product Mix

| Product Line | Spend | % of Total |
|--------------|-------|-----------|
| Model Serving | ${amount} | {pct}% |
| AI Gateway | ${amount} | {pct}% |
| Interactive | ${amount} | {pct}% |
| Lakeflow Pipelines | ${amount} | {pct}% |
| Others | ${amount} | {pct}% |

## Trend (Last 4 Weeks)

| Week | Spend | WoW Growth |
|------|-------|-----------|
| {date} | ${amount} | {pct}% |
...

## Anomalies & Risks

{Any churn risk alerts, sudden drops, or expansion signals}

---

## Confidence Assessment

**Confidence:** {high|medium|low}
**Source Count:** {n}
**Source Tiers:** [databricks_internal]
**Data Freshness:** {days since last sync}
**Recency:** {date of most recent data}

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
    json.dumps(["consumption-retriever"]),
    latency_ms,
    None  # populated in W3-W4
))
db.commit()
db.close()
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Invokes `/consumption-vault-sync` if data > 7 days stale
- [ ] Queries vault_signals for metrics, risk, opportunity signals
- [ ] Computes data freshness from signal timestamps
- [ ] Applies confidence logic (freshness + source_count)
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (escalate|research|queue)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id to vault_speaker_invocations (sqlite3, ? params)
- [ ] Source tier: databricks_internal

---

## Test Case 1: High Confidence (NWM, fresh data)

**Input:**
```yaml
entity_type: consumption
query_intent: "What is NWM's current consumption trend and health?"
scope:
  account_id: nwm
  time_window: 30days
```

**Expected Output:**
- confidence: high
- source_count: >= 3 (metrics + risk + opportunity signals)
- degradation_flags: []
- fallback_interrogation: null
- Data freshness < 7 days
- Product mix breakdown present
- WoW/SWLY growth populated

**Validation:**
- consumption-vault-sync ran within last 7 days
- vault has metrics signal with weekly spend, growth
- At least 3 source signals found

---

## Test Case 2: Medium Confidence (CHN, data 2 weeks old)

**Input:**
```yaml
entity_type: consumption
query_intent: "Is CHN consumption growing or declining?"
scope:
  account_id: chn
  time_window: 30days
```

**Expected Output:**
- confidence: medium
- source_count: 1-2
- degradation_flags: [outdated]
- fallback_interrogation:
  - question: "Consumption data is 14 days old. Run /consumption-vault-sync to refresh?"
  - intent: research
  - scope: { suggested_approach: "Re-run consumption-vault-sync for CHN" }

**Validation:**
- Data exists but is 7-30 days old
- Suggests re-running the sync
- Still provides available data with staleness warning

---

## Test Case 3: Low Confidence (No data available)

**Input:**
```yaml
entity_type: consumption
query_intent: "What is account X's DBU consumption?"
scope:
  account_id: account_x
  time_window: 30days
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation:
  - question: "No consumption data found for account_x. Is this account tracked in Logfood?"
  - intent: escalate
  - scope: { needed_tier: databricks_internal, suggested_approach: "Verify SFDC account ID and run /consumption-vault-sync" }

**Validation:**
- No metrics/risk/opportunity signals found
- Clear escalation path provided
- Suggests verifying account exists in Logfood

---

## Deployment

Skills directory: `~/.claude/skills/consumption-retriever/`

Run:
```
/consumption-retriever --input '{
  "entity_type": "consumption",
  "query_intent": "What is NWM's current consumption health?",
  "scope": {
    "account_id": "nwm",
    "time_window": "30days"
  }
}'
```

---

## Notes

- Always use vault MCP tools (vault_signals, vault_search) for data retrieval
- Confidence is deterministic: freshness + source_count are the main drivers
- Source tier is always `databricks_internal` (consumption data comes from Logfood/Delta)
- If consumption-vault-sync fails, return confidence=low with fallback suggesting manual check
- Product mix is critical for identifying GenAI adoption signals (Model Serving, AI Gateway growth)

---

**Version:** 1.0
**Last Updated:** 2026-04-19
**Contract Reference:** `_System/retriever-contract.md` (immutable)
