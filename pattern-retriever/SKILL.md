# pattern-retriever

**Haiku agent** that queries pattern usage and effectiveness data from brain.db. Returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What patterns have worked best with clinical executives?"
- "Which discovery patterns landed well at NWM?"
- "What's our most effective Challenger reframe pattern?"

**Model:** claude-haiku-4-5-20251001  
**Context budget:** fork (isolated, ~20k tokens)  
**Input:** Pattern usage records from brain.db  
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: pattern
query_intent: string
scope:
  audience_role: string (optional, e.g., "clinical_executive", "technical_gatekeeper")
  pattern_family: string (optional, e.g., "challenger_reframe", "discovery", "demo_narrative")
  account_id: string (optional, e.g., "nwm", "chn")
```

---

## Retrieval Process (4 steps)

### Step 1: Check Table Existence

```python
import sqlite3

DB_PATH = "/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if pattern_usage table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pattern_usage'")
has_pattern_usage = cur.fetchone() is not None

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pattern_usage_expanded'")
has_expanded = cur.fetchone() is not None
```

If neither table exists, set confidence=low, degradation_flags=[missing_context], and return early with fallback_interrogation suggesting table creation.

### Step 2: Query Pattern Usage

```python
# If pattern_usage_expanded exists, prefer it (richer view)
if has_expanded:
    query = "SELECT * FROM pattern_usage_expanded WHERE 1=1"
    params = []
    if audience_role:
        query += " AND audience_role = ?"
        params.append(audience_role)
    if pattern_family:
        query += " AND pattern_family = ?"
        params.append(pattern_family)
    if account_id:
        query += " AND account_id = ?"
        params.append(account_id)
    query += " ORDER BY effectiveness_score DESC"
    cur.execute(query, params)
elif has_pattern_usage:
    query = "SELECT * FROM pattern_usage WHERE 1=1"
    params = []
    if audience_role:
        query += " AND audience_role = ?"
        params.append(audience_role)
    if pattern_family:
        query += " AND pattern_family = ?"
        params.append(pattern_family)
    if account_id:
        query += " AND account_id = ?"
        params.append(account_id)
    query += " ORDER BY effectiveness_score DESC"
    cur.execute(query, params)
```

### Step 3: Rank by Effectiveness

- Sort results by `effectiveness_score` descending (landed rate)
- Count total records with evaluated outcomes
- Extract top patterns with highest effectiveness

### Step 4: Compute Confidence & Fallback Interrogation

- **high**: 3+ usage records with evaluated outcomes (effectiveness_score != NULL)
- **medium**: 1-2 usage records with evaluated outcomes
- **low**: 0 records or tables don't exist

If confidence < high, populate fallback_interrogation.

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: pattern-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [list of tiers found]
recency: {ISO8601 of most recent pattern usage or null}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# Pattern Analysis

## Query Context

| Filter | Value |
|--------|-------|
| Audience Role | {role or "any"} |
| Pattern Family | {family or "any"} |
| Account | {account or "all"} |

## Top Patterns by Effectiveness

| Pattern | Family | Audience | Effectiveness | Uses | Last Used |
|---------|--------|----------|---------------|------|-----------|
| {name} | {family} | {audience} | {score} | {count} | {date} |
...

## Pattern Details

### {Pattern Name} (effectiveness: {score})

**Family:** {family}  
**Audience:** {role}  
**Account(s):** {accounts}  
**Usage count:** {n}  
**Landed rate:** {percentage}

{Description or notes if available}

---

## Confidence Assessment

**Confidence:** {high|medium|low}  
**Source Count:** {n}  
**Source Tiers:** {list}  
**Recency:** {date of most recent pattern usage}

{Explanation of why this confidence level}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope -- or null if high confidence}
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Checks if pattern_usage / pattern_usage_expanded tables exist in brain.db
- [ ] Uses sqlite3 with `?` params (NOT psycopg / %s)
- [ ] Filters by audience_role, pattern_family, account_id
- [ ] Ranks by effectiveness_score descending
- [ ] Counts records with evaluated outcomes for confidence
- [ ] Applies confidence logic:
  - 3+ evaluated records -> high
  - 1-2 -> medium
  - 0 or tables missing -> low
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (research|queue|escalate)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id for telemetry

---

## Test Case 1: High Confidence (NWM patterns)

**Input:**
```yaml
entity_type: pattern
query_intent: "What discovery patterns work best at NWM?"
scope:
  account_id: nwm
  pattern_family: discovery
```

**Expected Output:**
- confidence: high
- source_count: >= 3
- degradation_flags: []
- fallback_interrogation: null

**Validation:**
- 3+ pattern_usage records exist for nwm + discovery
- Ranked by effectiveness_score
- All frontmatter fields populated

---

## Test Case 2: Medium Confidence (sparse data)

**Input:**
```yaml
entity_type: pattern
query_intent: "What challenger reframes landed with payer executives?"
scope:
  audience_role: clinical_executive
  pattern_family: challenger_reframe
```

**Expected Output:**
- confidence: medium (source_count 1-2)
- degradation_flags: [sparse_data]
- fallback_interrogation: present

**Validation:**
- 1-2 records found matching filters
- Fallback suggests researching more pattern usage data

---

## Test Case 3: Low Confidence (no data)

**Input:**
```yaml
entity_type: pattern
query_intent: "What patterns work for radiology departments?"
scope:
  audience_role: department_head
  pattern_family: radiology_specific
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation: question about creating pattern tracking for this audience

**Validation:**
- No matching records or tables don't exist
- Clear guidance on what to capture next

---

## Deployment

Skills directory: `~/.claude/skills/pattern-retriever/`

Run:
```
/pattern-retriever --input '{
  "entity_type": "pattern",
  "query_intent": "What patterns work best with clinical executives?",
  "scope": {
    "audience_role": "clinical_executive",
    "pattern_family": "challenger_reframe",
    "account_id": "nwm"
  }
}'
```

---

## Notes

- Uses sqlite3 stdlib to query brain.db directly -- NOT vault MCP tools
- DB path: `/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db`
- Tables may not exist yet (pattern_usage, pattern_usage_expanded) -- degrade gracefully
- Confidence is deterministic: based on count of records with non-null effectiveness_score
- If tables don't exist, set degradation_flag=missing_context and suggest bootstrapping pattern tracking
- Fallback interrogation is the escape hatch for unanswerable questions

---

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Contract Reference:** `_System/retriever-contract.md` (immutable)
