# long-tail-retriever

**Haiku agent** that performs FTS5 full-text search on brain.db chunks and falls back to scanning vault files via glob. Returns relevant chunks with source attribution, conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What do we know about Epic Caboodle ETL patterns?"
- "Find anything about HEDIS quality measures in the vault"
- "What notes mention PostGIS or geospatial?"
- "Search for anything related to renewal risk"

**Model:** claude-haiku-4-5-20251001  
**Context budget:** fork (isolated, ~20k tokens)  
**Input:** Free-text query for FTS5 search across vault chunks  
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: long-tail
query_intent: string
scope:
  query: string (required, the search terms)
  account_id: string (optional, filter to account)
  entity_type_filter: string (optional, e.g., "session", "account", "use_case")
  max_results: int (optional, default 10)
```

---

## Retrieval Process (4 steps)

### Step 1: FTS5 Search on fts_chunks

```python
import sqlite3
import os
import glob as glob_mod

DB_PATH = "/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db"
VAULT_PATH = "/Users/samuel.selvan/obsidian/sa-intel"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Check if fts_chunks exists (created by sa-vault db.py, NOT by migration 0003)
# Note: sa-vault creates "fts_chunks", migration 0003 creates "derived_chunks_fts"
# Try both, prefer fts_chunks (live sa-vault table)
fts_table = None
for candidate in ("fts_chunks", "chunks_fts", "derived_chunks_fts"):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (candidate,))
    if cur.fetchone():
        fts_table = candidate
        break
has_fts = fts_table is not None

results = []
if has_fts:
    # FTS5 MATCH query -- tokenize search terms for FTS5 syntax
    # Use simple terms joined by spaces (implicit AND)
    search_query = query  # e.g., "Epic Caboodle ETL"

    fts_sql = f"""
        SELECT c.chunk_id, c.file_path, c.chunk_text, c.heading_path,
               c.chunk_type, c.account_id, c.entity_type,
               rank
        FROM {fts_table}
        JOIN chunks c ON {fts_table}.rowid = c.rowid
        WHERE {fts_table} MATCH ?
    """
    fts_params = [search_query]

    if account_id:
        fts_sql += " AND c.account_id = ?"
        fts_params.append(account_id)

    if entity_type_filter:
        fts_sql += " AND c.entity_type = ?"
        fts_params.append(entity_type_filter)

    fts_sql += " ORDER BY rank LIMIT ?"
    fts_params.append(max_results)

    try:
        cur.execute(fts_sql, fts_params)
        results = cur.fetchall()
    except Exception:
        # FTS5 query syntax error -- try simpler tokenization
        simple_terms = " ".join(f'"{t}"' for t in query.split())
        try:
            fts_params[0] = simple_terms
            cur.execute(fts_sql, fts_params)
            results = cur.fetchall()
        except Exception:
            results = []
```

Also check `repo_docs_fts` for code documentation:

```python
# Secondary: search repo_docs_fts
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='repo_docs_fts'")
if cur.fetchone():
    repo_fts_sql = """
        SELECT rd.file_path, rd.chunk_text, rank
        FROM repo_docs_fts
        JOIN repo_docs rd ON repo_docs_fts.rowid = rd.rowid
        WHERE repo_docs_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """
    try:
        cur.execute(repo_fts_sql, [search_query, max_results])
        repo_results = cur.fetchall()
        results.extend(repo_results)
    except Exception:
        pass
```

### Step 2: Fallback -- Scan Reference/Knowledge Files

If FTS5 yields < 3 results, scan `Reference/Knowledge/` directory files:

```python
if len(results) < 3:
    knowledge_dir = os.path.join(VAULT_PATH, "Reference", "Knowledge")
    if os.path.isdir(knowledge_dir):
        for fpath in glob_mod.glob(os.path.join(knowledge_dir, "*.md")):
            try:
                with open(fpath, "r") as f:
                    content = f.read()
                # Simple keyword match
                query_terms = query.lower().split()
                content_lower = content.lower()
                if any(term in content_lower for term in query_terms):
                    results.append({
                        "file_path": fpath,
                        "chunk_text": content[:500],  # First 500 chars as preview
                        "heading_path": os.path.basename(fpath),
                        "source": "file_scan"
                    })
            except Exception:
                continue
```

### Step 3: Deduplicate and Rank

- Deduplicate by file_path (keep highest-ranked per file)
- Compute source diversity: count unique file_paths and entity_types
- Extract source tiers: vault_file for chunk results, sa_observation for knowledge files

### Step 4: Compute Confidence & Fallback Interrogation

Confidence based on FTS match count AND source diversity:

- **high**: 3+ results from 2+ distinct sources (files)
- **medium**: 1-2 results or single source
- **low**: 0 results from both FTS5 and file scan

If confidence < high, populate fallback_interrogation suggesting refining search terms or ingesting new content.

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: long-tail-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [list of tiers found]
recency: {ISO8601 of most recent chunk creation or null}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# Search Results: "{query}"

## Summary

| Metric | Value |
|--------|-------|
| Query | {query} |
| FTS5 Results | {count} |
| File Scan Results | {count} |
| Unique Sources | {count distinct file_paths} |
| Account Filter | {account_id or "all"} |

## Results

### Result 1: {heading_path or filename}

**Source:** `{file_path}`  
**Entity Type:** {entity_type or "unknown"}  
**Account:** {account_id or "unscoped"}  
**Relevance:** FTS5 rank {rank}

> {chunk_text excerpt, truncated to ~200 chars}

---

### Result 2: {heading_path or filename}

**Source:** `{file_path}`  
...

---

## Source Attribution

| Source File | Entity Type | Tier | Match Method |
|-------------|-------------|------|-------------|
| {file_path} | {entity_type} | {vault_file|sa_observation} | {fts5|keyword_scan} |
...

---

## Confidence Assessment

**Confidence:** {high|medium|low}  
**Source Count:** {n}  
**Source Tiers:** {list}  
**Recency:** {date of most recent source}

{Explanation of confidence based on match count and source diversity}

---

## Fallback Interrogation (if confidence < high)

{question, intent, scope -- or null if high confidence}
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Queries fts_chunks (or chunks_fts / derived_chunks_fts fallback) using FTS5 MATCH syntax
- [ ] Falls back to simpler tokenization if FTS5 MATCH fails
- [ ] Also queries repo_docs_fts if table exists
- [ ] Falls back to file scan of Reference/Knowledge/ if < 3 FTS results
- [ ] Uses sqlite3 with `?` params (NOT psycopg / %s)
- [ ] Deduplicates by file_path
- [ ] Computes source diversity (unique file_paths, entity_types)
- [ ] Applies confidence logic:
  - 3+ results from 2+ sources -> high
  - 1-2 results or single source -> medium
  - 0 results -> low
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (research|queue|escalate)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Includes source attribution for every result
- [ ] Logs invocation_id for telemetry

---

## Test Case 1: High Confidence (broad topic)

**Input:**
```yaml
entity_type: long-tail
query_intent: "What do we know about Epic Caboodle?"
scope:
  query: "Epic Caboodle"
  max_results: 10
```

**Expected Output:**
- confidence: high
- source_count: >= 3
- degradation_flags: []
- fallback_interrogation: null

**Validation:**
- FTS5 returns chunks from session notes, knowledge files, etc.
- Multiple distinct source files
- Source attribution table populated
- All frontmatter fields populated

---

## Test Case 2: Medium Confidence (narrow topic)

**Input:**
```yaml
entity_type: long-tail
query_intent: "Any notes on PostGIS geospatial queries?"
scope:
  query: "PostGIS geospatial"
  account_id: chn
  max_results: 5
```

**Expected Output:**
- confidence: medium (source_count 1-2)
- degradation_flags: [sparse_data]
- fallback_interrogation: present

**Validation:**
- Few matches, possibly from a single file
- Suggests ingesting more PostGIS-related content

---

## Test Case 3: Low Confidence (no matches)

**Input:**
```yaml
entity_type: long-tail
query_intent: "Find anything about quantum computing"
scope:
  query: "quantum computing"
  max_results: 10
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation: question about whether this topic exists in the vault

**Validation:**
- No FTS5 matches
- No file scan matches
- Clear guidance to ingest relevant content first

---

## Deployment

Skills directory: `~/.claude/skills/long-tail-retriever/`

Run:
```
/long-tail-retriever --input '{
  "entity_type": "long-tail",
  "query_intent": "What do we know about HEDIS measures?",
  "scope": {
    "query": "HEDIS quality measures",
    "max_results": 10
  }
}'
```

---

## Notes

- Uses sqlite3 stdlib to query brain.db directly -- NOT vault MCP tools
- DB path: `/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db`
- Primary search: FTS5 on `fts_chunks` table (created by sa-vault; fallback to `chunks_fts` or `derived_chunks_fts`)
- Secondary search: FTS5 on `repo_docs_fts` table (code documentation)
- Fallback: keyword scan of `Reference/Knowledge/*.md` files
- FTS5 MATCH syntax: simple terms joined by spaces = implicit AND
- If FTS5 MATCH throws syntax error (special characters), falls back to quoted terms
- Source tiers: vault_file for FTS5 results, sa_observation for file scan results
- Confidence factors in BOTH match count AND source diversity (unique files)
- Chunk text excerpts are truncated to ~200 chars for readability
- Fallback interrogation is the escape hatch for unanswerable questions

---

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Contract Reference:** `_System/retriever-contract.md` (immutable)
