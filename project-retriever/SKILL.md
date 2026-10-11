# project-retriever

**Haiku agent** that queries project status, progress, engagement history, and collaborators from brain.db. Returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What's the status of the clinical-agent project?"
- "Which projects have stalled recently?"
- "Show me all active projects for NWM"
- "Who's collaborating on revenue-radar?"

**Model:** claude-haiku-4-5-20251001  
**Context budget:** fork (isolated, ~20k tokens)  
**Input:** Project queries against brain.db (repos, apps, entities, relationships)  
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: project
query_intent: string
scope:
  project_id: string (optional, e.g., "clinical-agent", "revenue-radar")
  account_id: string (optional, e.g., "nwm", "chn", "_cross", "_internal")
  status_filter: string (optional, e.g., "active", "demo", "archived")
```

---

## Retrieval Process (4 steps)

### Step 1: Check Available Tables

```python
import sqlite3

DB_PATH = "/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Check which project-related tables exist
available_tables = {}
for tbl in ['projects', 'project_state', 'engagements', 'repos', 'apps', 'deployments']:
    cur.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name=?", (tbl,))
    available_tables[tbl] = cur.fetchone() is not None
```

Core tables that always exist: `repos`, `apps`, `deployments`.
Tables that may not exist yet: `projects`, `project_state`, `engagements`.

### Step 2: Query Project Data

```python
sources = []

# Always: query repos table (known to exist)
repo_query = "SELECT id, name, account_id, language, status, file_path, updated_at FROM repos WHERE 1=1"
repo_params = []
if project_id:
    repo_query += " AND (id = ? OR name LIKE ?)"
    repo_params.extend([project_id, f"%{project_id}%"])
if account_id:
    repo_query += " AND account_id = ?"
    repo_params.append(account_id)
if status_filter:
    repo_query += " AND status = ?"
    repo_params.append(status_filter)
cur.execute(repo_query, repo_params)
repos = cur.fetchall()
sources.extend(repos)

# Always: query apps table
app_query = "SELECT id, name, account_id, status, updated_at FROM apps WHERE 1=1"
app_params = []
if project_id:
    app_query += " AND (id = ? OR name LIKE ?)"
    app_params.extend([project_id, f"%{project_id}%"])
if account_id:
    app_query += " AND account_id = ?"
    app_params.append(account_id)
cur.execute(app_query, app_params)
apps = cur.fetchall()
sources.extend(apps)

# If projects table exists, query it
if available_tables.get('projects'):
    proj_query = "SELECT * FROM projects WHERE 1=1"
    proj_params = []
    if project_id:
        proj_query += " AND (id = ? OR name LIKE ?)"
        proj_params.extend([project_id, f"%{project_id}%"])
    if account_id:
        proj_query += " AND account_id = ?"
        proj_params.append(account_id)
    cur.execute(proj_query, proj_params)
    projects = cur.fetchall()
    sources.extend(projects)

# If project_state exists, get latest state
if available_tables.get('project_state') and project_id:
    cur.execute("SELECT * FROM project_state WHERE project_id = ? ORDER BY updated_at DESC LIMIT 1", (project_id,))
    state = cur.fetchone()
    if state:
        sources.append(state)

# If engagements exist, get engagement count
if available_tables.get('engagements') and project_id:
    cur.execute("SELECT COUNT(*) as cnt FROM engagements WHERE project_id = ?", (project_id,))
    eng_count = cur.fetchone()

# Also check deployments
deploy_query = "SELECT id, app_id, environment, status, deployed_at FROM deployments WHERE 1=1"
deploy_params = []
if project_id:
    deploy_query += " AND app_id = ?"
    deploy_params.append(project_id)
cur.execute(deploy_query, deploy_params)
deployments = cur.fetchall()
sources.extend(deployments)
```

### Step 3: Enrich with Relationship Graph

```python
# Check entities table for project-related entities
if project_id:
    cur.execute("""
        SELECT e.id, e.entity_type, e.name, e.account_id
        FROM entities e
        WHERE e.name LIKE ? OR e.id LIKE ?
    """, (f"%{project_id}%", f"%{project_id}%"))
    related_entities = cur.fetchall()

    # Get relationships (collaborators, dependencies)
    for entity in related_entities:
        cur.execute("""
            SELECT r.rel_type, r.confidence, e2.name, e2.entity_type
            FROM relationships r
            JOIN entities e2 ON r.target_id = e2.id
            WHERE r.source_id = ?
        """, (entity['id'],))
        relationships = cur.fetchall()
        sources.extend(relationships)
```

### Step 4: Compute Confidence & Fallback Interrogation

- **high**: project_state exists + recent activity (updated_at within 30 days) + repo/app found
- **medium**: repo or app found but no project_state or stale (updated_at > 30 days ago)
- **low**: project not found in any table

If confidence < high, populate fallback_interrogation.

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: project-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [list of tiers found]
recency: {ISO8601 of most recent project activity or null}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# Project: {project_name or query}

## Project Overview

| Field | Value |
|-------|-------|
| Name | {name} |
| Account | {account_id} |
| Language | {language} |
| Status | {active|demo|archived} |
| Last Updated | {date} |
| Deployments | {count} |
| Engagements | {count or "not tracked"} |

## Repository Details

| Repo | Account | Language | Status | Last Updated |
|------|---------|----------|--------|--------------|
| {name} | {account} | {lang} | {status} | {date} |
...

## App & Deployment History

| App | Environment | Status | Deployed At |
|-----|-------------|--------|-------------|
| {name} | {env} | {status} | {date} |
...

## Collaborators & Relationships

| Entity | Type | Relationship | Confidence |
|--------|------|-------------|------------|
| {name} | {type} | {rel_type} | {confidence} |
...

## Project State (if available)

{Latest project state snapshot or "project_state table not yet created"}

---

## Confidence Assessment

**Confidence:** {high|medium|low}  
**Source Count:** {n}  
**Source Tiers:** {list}  
**Recency:** {date of most recent activity}

{Explanation of why this confidence level}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope -- or null if high confidence}
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Checks which tables exist (projects, project_state, engagements vs repos, apps, deployments)
- [ ] Queries repos and apps tables (always available)
- [ ] Queries projects/project_state/engagements if they exist
- [ ] Uses sqlite3 with `?` params (NOT psycopg / %s)
- [ ] Enriches with entity graph relationships
- [ ] Checks deployments for deployment history
- [ ] Computes source_count from total results found
- [ ] Applies confidence logic:
  - project_state + recent activity + repo/app -> high
  - repo/app found but stale or no state -> medium
  - not found -> low
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (research|queue|escalate)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id for telemetry

---

## Test Case 1: High Confidence (known repo)

**Input:**
```yaml
entity_type: project
query_intent: "What's the status of the clinical-agent project?"
scope:
  project_id: clinical_agent
  account_id: chn
```

**Expected Output:**
- confidence: high (if project_state exists + recent activity)
- confidence: medium (if only repo found, no project_state)
- source_count: >= 3
- degradation_flags: [] or [outdated] if stale

**Validation:**
- Repo record found in repos table
- Deployment history populated if available
- All frontmatter fields populated

---

## Test Case 2: Medium Confidence (stale project)

**Input:**
```yaml
entity_type: project
query_intent: "What happened with the hedis-helper project?"
scope:
  project_id: hedis-helper
```

**Expected Output:**
- confidence: medium (source_count 1-2, likely stale)
- degradation_flags: [outdated]
- fallback_interrogation: present

**Validation:**
- Repo exists but last activity was months ago
- Suggests checking if project is still active

---

## Test Case 3: Low Confidence (unknown project)

**Input:**
```yaml
entity_type: project
query_intent: "Show me project alpha-prototype"
scope:
  project_id: alpha-prototype
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation: question about registering the project

**Validation:**
- No matching records in any table
- Suggests using /register to add the project

---

## Deployment

Skills directory: `~/.claude/skills/project-retriever/`

Run:
```
/project-retriever --input '{
  "entity_type": "project",
  "query_intent": "What is the status of clinical-agent?",
  "scope": {
    "project_id": "clinical_agent",
    "account_id": "chn"
  }
}'
```

---

## Notes

- Uses sqlite3 stdlib to query brain.db directly -- NOT vault MCP tools
- DB path: `/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db`
- Core tables always available: repos, apps, deployments
- Tables that may not exist: projects, project_state, engagements -- check before querying
- Known repos are backfilled (sa-vault, clinical_agent, revenue-radar, etc.)
- Confidence factors in both data presence AND recency (stale = medium)
- Enriches with entity graph for collaborator/dependency relationships
- Fallback interrogation is the escape hatch for unanswerable questions

---

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Contract Reference:** `_System/retriever-contract.md` (immutable)
