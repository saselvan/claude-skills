# temporal-retriever

**Haiku agent** that queries sessions, action items, signals, and commitments by date range from brain.db. Returns chronological timelines, upcoming deadlines, and overdue commitments conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What happened with NWM in the last 30 days?"
- "What commitments are overdue across all accounts?"
- "Show me the timeline of CHN engagement this quarter"
- "What's coming up in the next two weeks?"

**Model:** claude-haiku-4-5-20251001  
**Context budget:** fork (isolated, ~20k tokens)  
**Input:** Time-scoped queries against sessions, action_items, signals  
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: temporal
query_intent: string
scope:
  account_id: string (optional, e.g., "nwm", "chn")
  time_window: string (required, e.g., "30days", "90days", "ytd", "since:2026-01-15")
  event_types: list (optional, e.g., ["sessions", "action_items", "signals"])
```

---

## Retrieval Process (4 steps)

### Step 1: Parse Time Window

```python
import sqlite3
from datetime import datetime, timedelta

DB_PATH = "/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db"

def parse_time_window(window: str) -> str:
    """Returns ISO8601 date string for the start of the window."""
    today = datetime.now()
    if window == "30days":
        return (today - timedelta(days=30)).strftime("%Y-%m-%d")
    elif window == "90days":
        return (today - timedelta(days=90)).strftime("%Y-%m-%d")
    elif window == "ytd":
        return f"{today.year}-01-01"
    elif window.startswith("since:"):
        return window.replace("since:", "")
    else:
        return (today - timedelta(days=30)).strftime("%Y-%m-%d")

start_date = parse_time_window(time_window)
```

### Step 2: Query Events by Date Range

```python
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

sources = []

# Sessions in window
session_query = "SELECT id, account_id, date, session_type, title FROM sessions WHERE date >= ?"
session_params = [start_date]
if account_id:
    session_query += " AND account_id = ?"
    session_params.append(account_id)
session_query += " ORDER BY date DESC"
cur.execute(session_query, session_params)
sessions = cur.fetchall()
sources.extend(sessions)

# Action items (open + due in window, or created in window)
ai_query = """
    SELECT id, account_id, text, kind, owed_by, due_date, status, created_at
    FROM action_items
    WHERE (due_date >= ? OR created_at >= ?)
"""
ai_params = [start_date, start_date]
if account_id:
    ai_query += " AND account_id = ?"
    ai_params.append(account_id)
ai_query += " ORDER BY CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, due_date ASC"
cur.execute(ai_query, ai_params)
action_items = cur.fetchall()
sources.extend(action_items)

# Signals in window
sig_query = "SELECT id, account_id, signal_type, text, severity, status, created_at FROM signals WHERE created_at >= ?"
sig_params = [start_date]
if account_id:
    sig_query += " AND account_id = ?"
    sig_params.append(account_id)
sig_query += " ORDER BY created_at DESC"
cur.execute(sig_query, sig_params)
signals = cur.fetchall()
sources.extend(signals)

# Check for commitments_expanded view/table (may not exist yet)
cur.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name='commitments_expanded'")
if cur.fetchone():
    commit_query = "SELECT * FROM commitments_expanded WHERE created_at >= ?"
    commit_params = [start_date]
    if account_id:
        commit_query += " AND account_id = ?"
        commit_params.append(account_id)
    cur.execute(commit_query, commit_params)
    commitments = cur.fetchall()
    sources.extend(commitments)

# Check for engagements table (may not exist yet)
cur.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name='engagements'")
if cur.fetchone():
    eng_query = "SELECT * FROM engagements WHERE engagement_date >= ?"
    eng_params = [start_date]
    if account_id:
        eng_query += " AND account_id = ?"
        eng_params.append(account_id)
    cur.execute(eng_query, eng_params)
    engagements = cur.fetchall()
    sources.extend(engagements)
```

### Step 3: Build Chronological Timeline

- Merge all events into a single timeline sorted by date
- Identify overdue action items (status=open, due_date < today)
- Identify upcoming deadlines (due_date within next 14 days)
- Group by week for readability

### Step 4: Compute Confidence & Fallback Interrogation

- **high**: Events found in window (sessions + action_items + signals >= 3 total)
- **medium**: Sparse data (1-2 events in window)
- **low**: Empty window (0 events found)

If confidence < high, populate fallback_interrogation suggesting expanding time window or checking specific accounts.

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: temporal-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [list of tiers found]
recency: {ISO8601 of most recent event in window}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# Timeline: {account_id or "All Accounts"} ({time_window})

## Summary

| Metric | Value |
|--------|-------|
| Time Window | {start_date} to {today} |
| Sessions | {count} |
| Action Items | {count} (open: {n}, overdue: {n}) |
| Signals | {count} |
| Commitments | {count or "table not available"} |

## Overdue Items

| Item | Account | Owed By | Due Date | Days Overdue |
|------|---------|---------|----------|--------------|
| {text} | {account} | {owed_by} | {due_date} | {n} |
...

## Upcoming Deadlines (next 14 days)

| Item | Account | Owed By | Due Date | Days Remaining |
|------|---------|---------|----------|----------------|
| {text} | {account} | {owed_by} | {due_date} | {n} |
...

## Chronological Timeline

### Week of {YYYY-MM-DD}

- **{date}** [{event_type}] {description}
  - Account: {account_id}
  - {additional context}

### Week of {YYYY-MM-DD}

- **{date}** [{event_type}] {description}
  ...

---

## Confidence Assessment

**Confidence:** {high|medium|low}  
**Source Count:** {n}  
**Source Tiers:** {list}  
**Recency:** {date of most recent event}

{Explanation of why this confidence level}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope -- or null if high confidence}
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Parses time_window into start date (30days, 90days, ytd, since:YYYY-MM-DD)
- [ ] Queries sessions table filtered by date >= start_date
- [ ] Queries action_items filtered by due_date or created_at >= start_date
- [ ] Queries signals filtered by created_at >= start_date
- [ ] Checks if commitments_expanded table/view exists before querying
- [ ] Checks if engagements table exists before querying
- [ ] Uses sqlite3 with `?` params (NOT psycopg / %s)
- [ ] Merges all events into chronological timeline
- [ ] Identifies overdue items (open + due_date < today)
- [ ] Identifies upcoming deadlines (due_date within 14 days)
- [ ] Computes source_count from total events found
- [ ] Applies confidence logic:
  - 3+ events -> high
  - 1-2 -> medium
  - 0 -> low
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (research|queue|escalate)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id for telemetry

---

## Test Case 1: High Confidence (NWM 90 days)

**Input:**
```yaml
entity_type: temporal
query_intent: "What happened with NWM in the last 90 days?"
scope:
  account_id: nwm
  time_window: 90days
```

**Expected Output:**
- confidence: high
- source_count: >= 3
- degradation_flags: []
- fallback_interrogation: null

**Validation:**
- Sessions, action items, and signals found in window
- Chronological timeline grouped by week
- Overdue items flagged with days overdue
- All frontmatter fields populated

---

## Test Case 2: Medium Confidence (sparse window)

**Input:**
```yaml
entity_type: temporal
query_intent: "What happened at CHN this week?"
scope:
  account_id: chn
  time_window: since:2026-04-14
```

**Expected Output:**
- confidence: medium (source_count 1-2)
- degradation_flags: [sparse_data]
- fallback_interrogation: present

**Validation:**
- Few events in narrow window
- Suggests expanding to 30days or 90days

---

## Test Case 3: Low Confidence (empty window)

**Input:**
```yaml
entity_type: temporal
query_intent: "What happened at account_x last month?"
scope:
  account_id: account_x
  time_window: 30days
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation: question about whether account exists or needs onboarding

**Validation:**
- No events found in window
- Suggests checking account existence or expanding scope

---

## Deployment

Skills directory: `~/.claude/skills/temporal-retriever/`

Run:
```
/temporal-retriever --input '{
  "entity_type": "temporal",
  "query_intent": "What happened with NWM in the last 30 days?",
  "scope": {
    "account_id": "nwm",
    "time_window": "30days"
  }
}'
```

---

## Notes

- Uses sqlite3 stdlib to query brain.db directly -- NOT vault MCP tools for temporal queries
- DB path: `/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db`
- Tables that may not exist: commitments_expanded, engagements -- check before querying
- Core tables always available: sessions, action_items, signals
- Confidence is deterministic: based on total event count in the time window
- Overdue detection uses today's date vs action_item.due_date where status='open'
- If time_window filter finds nothing, set degradation_flag=sparse_data and suggest expanding window
- Fallback interrogation is the escape hatch for unanswerable questions

---

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Contract Reference:** `_System/retriever-contract.md` (immutable)
