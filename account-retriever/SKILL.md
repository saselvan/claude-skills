# account-retriever

**Haiku agent** that queries account state, use cases, recent momentum, and stakeholder alignment. Returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What are NWM's current use cases and which are slipping?"
- "Is NWM still focused on Epic integration?"
- "What is NWM's health and recent momentum?"

**Model:** claude-haiku-4-5-20251001  
**Context budget:** fork (isolated, ~20k tokens)  
**Input:** Vault summary + use case list for account  
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: account
query_intent: string
scope:
  account_id: string (e.g., "nwm", "chn")
  time_window: string (optional, e.g., "30days", "90days")
```

---

## Retrieval Process (4 steps)

### Step 1: Load Account Summary
- Query: `vault_summary(account_id)`
- Extract: account health, tech stack, stakeholders, MRR potential
- Confidence seed: If account file has > 5 stakeholders + tech stack documented → boost to high

### Step 2: Load Use Cases
- Query: `vault_signals(account, signal_type="use_case")`
- For each use case: extract stage, status, close_date, slippage signals
- Count: How many are on-track vs slipping
- Confidence rule: If 3+ use cases documented + status is current → high

### Step 3: Load Recent Sessions
- Query: `vault_search(query="recent sessions", account=account_id, limit=3)`
- Extract: last 3 sessions, any new signals or momentum shifts
- Recency: Use most recent session timestamp

### Step 4: Compute Confidence & Fallback Interrogation
- If steps 1-3 yield source_count ≥ 3 → high
- If source_count 1-2 → medium
- If source_count 0 → low with fallback_interrogation

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: account-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [list of tiers found]
recency: {ISO8601 of most recent session or file update}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# {Account Name}

## Account Health

| Field | Value |
|-------|-------|
| Health Status | {green|yellow|red} |
| MRR Potential | ${amount} |
| MRR Live | ${amount} |
| Tech Stack | {comma-separated} |
| Key Stakeholders | {count} |

## Use Cases ({on_track}/{total})

| Use Case | Stage | Status | Close Date | Slippage | Owner |
|----------|-------|--------|------------|----------|-------|
| {name} | {stage} | {status} | {date} | {flag or none} | {stakeholder} |
...

## Recent Momentum

{Summary of last 2-3 sessions and any new signals}

## Stakeholder Alignment

{Who are the champions, blockers, economic buyers?}

---

## Confidence Assessment

**Confidence:** {high|medium|low}  
**Source Count:** {n}  
**Source Tiers:** {list}  
**Recency:** {date of most recent source}

{Explanation of why this confidence level, based on sources}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope — or null if high confidence}
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Calls vault_summary(account_id)
- [ ] Calls vault_signals(account, signal_type="use_case")
- [ ] Calls vault_search for recent sessions (limit=3)
- [ ] Computes source_count from results
- [ ] Applies confidence logic:
  - 3+ sources → high
  - 1-2 → medium
  - 0 → low
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (escalate|research|queue)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id for telemetry

---

## Test Case 1: High Confidence (NWM)

**Input:**
```yaml
entity_type: account
query_intent: "What are NWM's current use cases and momentum?"
scope:
  account_id: nwm
  time_window: 90days
```

**Expected Output:**
- confidence: high
- source_count: ≥ 3
- degradation_flags: []
- fallback_interrogation: null

**Validation:**
- Account file has tech stack, stakeholders, MRR
- Use cases table has 2+ cases documented
- Recent session within 14 days
- All frontmatter fields populated

---

## Test Case 2: Medium Confidence (New Account)

**Input:**
```yaml
entity_type: account
query_intent: "What is CHLA's current use case priority?"
scope:
  account_id: chla
  time_window: 30days
```

**Expected Output:**
- confidence: medium (source_count 1-2)
- degradation_flags: [outdated] or [incomplete]
- fallback_interrogation: present

**Validation:**
- Use case documented but not validated in recent session
- Account file exists but may be stale
- Suggests escalation or research to confirm current priorities

---

## Test Case 3: Low Confidence (No Data)

**Input:**
```yaml
entity_type: account
query_intent: "What's the status of account X?"
scope:
  account_id: account_x
  time_window: 30days
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation: question about whether account exists or needs research

**Validation:**
- Query surfaces that no data is available
- Suggests next step (create account file, schedule discovery)

---

## Deployment

Skills directory: `~/.claude/skills/account-retriever/`

Run:
```
/account-retriever --input '{
  "entity_type": "account",
  "query_intent": "What is NWM's current use case momentum?",
  "scope": {
    "account_id": "nwm",
    "time_window": "90days"
  }
}'
```

---

## Notes

- Always use vault MCP tools (vault_summary, vault_signals, vault_search) — never raw file reads
- Confidence is deterministic; source_count is the main driver
- If time_window filter finds nothing, set degradation_flag=missing_context and suggest expanding window
- Fallback interrogation is the escape hatch for unanswerable questions

---

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Contract Reference:** `_System/retriever-contract.md` (immutable)
