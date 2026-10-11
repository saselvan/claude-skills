---
name: glean-retriever
description: Wrapper retriever for Glean enterprise search. Queries internal Databricks docs, SFDC notes, Slack threads via Glean MCP tools. Conforms to retriever-contract.md.
model: claude-haiku-4-5-20251001
context: fork
user-invocable: true
---

# glean-retriever

**Haiku agent** that retrieves internal Databricks knowledge via Glean enterprise search. Returns structured markdown conforming to retriever-contract.md.

---

## Overview

Answers questions like:
- "What do internal docs say about NWM's architecture decisions?"
- "Are there any Slack threads about CHN's Epic integration?"
- "What SFDC notes exist for NWM's renewal?"

**Model:** claude-haiku-4-5-20251001
**Context budget:** fork (isolated, ~20k tokens)
**Input:** Query text + optional account context
**Output:** Markdown file with frontmatter + body

---

## Input Contract

```yaml
entity_type: glean
query_intent: string
scope:
  account_id: string (optional, e.g., "nwm", "chn")
  time_window: string (optional, e.g., "30days", "90days")
  filters:
    query: string (required -- the search query for Glean)
    source_type: string (optional -- e.g., "salesforce", "slack", "confluence", "google_drive")
```

---

## Retrieval Process (4 steps)

### Step 1: Build Search Query

Construct the Glean search query from inputs:
- Base query: `scope.filters.query` or `query_intent`
- Account context: if `account_id` provided, prepend account name (e.g., "Northwestern Medicine {query}")
- Source filter: if `source_type` specified, include in search params

### Step 2: Execute Glean Search

Call `mcp__glean__search` with the constructed query:

```
mcp__glean__search(query="{constructed_query}", page_size=10)
```

Parse results:
- Count total results
- Extract document titles, snippets, authors, dates, source types
- Identify most relevant results (top 5 by relevance score)

### Step 3: Fetch Document Content (Top Results)

For the top 3 most relevant results, call `mcp__glean__get_document_content`:

```
mcp__glean__get_document_content(document_id="{doc_id}")
```

Extract key information from each document.

### Step 4: Compute Confidence & Fallback Interrogation

Confidence based on result count and relevance:
- **3+ relevant results** with matching account context -> high
- **1-2 results** or results without strong account match -> medium
- **0 results** or Glean auth failure -> low

If Glean MCP tools fail (auth error, timeout):
- Return confidence=low
- Set degradation_flags: [missing_context]
- Set fallback_interrogation suggesting manual Glean search

---

## Output Format

Markdown file with this structure:

```markdown
---
retriever_name: glean-retriever
query_intent: {echo input}
confidence: {high|medium|low}
source_count: {int}
source_tiers: [databricks_internal]
recency: {ISO8601 of most recent result}
degradation_flags: {empty array or flags if confidence < high}
fallback_interrogation: {dict or null}
invocation_id: {UUID}
---

# Glean Results: {query summary}

## Top Results

### 1. {Document Title}
- **Source:** {Salesforce|Slack|Confluence|Google Drive}
- **Author:** {name}
- **Date:** {date}
- **Relevance:** {high|medium}

{Key excerpt or summary}

### 2. {Document Title}
...

### 3. {Document Title}
...

## Source Breakdown

| Source Type | Count | Most Recent |
|------------|-------|-------------|
| Salesforce | {n} | {date} |
| Slack | {n} | {date} |
| Confluence | {n} | {date} |
| Google Drive | {n} | {date} |

## Key Themes

{Synthesized themes across all results}

---

## Confidence Assessment

**Confidence:** {high|medium|low}
**Source Count:** {n}
**Source Tiers:** [databricks_internal]
**Recency:** {date of most recent result}

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
    json.dumps(["glean-retriever"]),
    latency_ms,
    None  # populated in W3-W4
))
db.commit()
db.close()
```

---

## Implementation Checklist

- [ ] Accepts input package (entity_type, query_intent, scope)
- [ ] Builds search query with account context
- [ ] Calls mcp__glean__search with constructed query
- [ ] Calls mcp__glean__get_document_content for top 3 results
- [ ] Computes source_count from results
- [ ] Applies confidence logic:
  - 3+ results -> high
  - 1-2 results -> medium
  - 0 results or auth failure -> low
- [ ] Populates degradation_flags if confidence < high
- [ ] Generates fallback_interrogation with intent (escalate|research|queue)
- [ ] Returns markdown with ALL frontmatter fields
- [ ] Logs invocation_id to vault_speaker_invocations (sqlite3, ? params)
- [ ] Handles Glean auth failures gracefully (confidence=low, fallback)
- [ ] Source tier: databricks_internal

---

## Test Case 1: High Confidence (NWM, multiple results)

**Input:**
```yaml
entity_type: glean
query_intent: "What internal docs exist about NWM's Epic integration plans?"
scope:
  account_id: nwm
  filters:
    query: "Northwestern Medicine Epic integration"
```

**Expected Output:**
- confidence: high
- source_count: >= 3
- degradation_flags: []
- fallback_interrogation: null
- Results from multiple source types (SFDC, Slack, Confluence)
- Key themes synthesized

**Validation:**
- Glean search returns 3+ relevant results
- At least one result mentions Epic or integration
- Source breakdown populated
- Most recent result date present

---

## Test Case 2: Medium Confidence (sparse results)

**Input:**
```yaml
entity_type: glean
query_intent: "Any internal discussion about CHN's OMOP implementation?"
scope:
  account_id: chn
  filters:
    query: "Community Health Network OMOP"
```

**Expected Output:**
- confidence: medium
- source_count: 1-2
- degradation_flags: [sparse_data]
- fallback_interrogation:
  - question: "Only 1-2 results found for CHN OMOP. Are there other search terms to try?"
  - intent: research
  - scope: { suggested_approach: "Try alternative queries: 'CHN data model', 'Community Health CDM'" }

**Validation:**
- Few results but still provides what was found
- Suggests alternative search queries
- Does not claim comprehensive coverage

---

## Test Case 3: Low Confidence (Glean auth failure)

**Input:**
```yaml
entity_type: glean
query_intent: "What does Glean know about account X?"
scope:
  account_id: account_x
  filters:
    query: "account X Databricks"
```

**Expected Output:**
- confidence: low
- source_count: 0
- degradation_flags: [missing_context]
- fallback_interrogation:
  - question: "Glean search returned 0 results or failed to authenticate. Manual search needed."
  - intent: escalate
  - scope: { needed_tier: databricks_internal, suggested_approach: "Open Glean in browser and search manually at go/glean" }

**Validation:**
- Graceful failure with clear next steps
- Does not fabricate results
- Suggests manual fallback

---

## Error Handling

### Glean Auth Failure
If `mcp__glean__search` returns an auth error:
```yaml
confidence: low
source_count: 0
degradation_flags: [missing_context]
fallback_interrogation:
  question: "Glean MCP authentication failed. Cannot retrieve internal docs."
  intent: escalate
  scope:
    suggested_approach: "Check Glean MCP auth token. Search manually at go/glean."
```

### Glean Timeout
If search takes > 30 seconds:
```yaml
confidence: low
degradation_flags: [missing_context]
fallback_interrogation:
  question: "Glean search timed out. Try a more specific query or search manually."
  intent: research
```

### Empty Results
If search returns 0 results:
```yaml
confidence: low
source_count: 0
degradation_flags: [missing_context]
fallback_interrogation:
  question: "No Glean results for '{query}'. Try broader terms or check if content exists."
  intent: research
  scope:
    suggested_queries: ["broader term 1", "broader term 2"]
```

---

## Deployment

Skills directory: `~/.claude/skills/glean-retriever/`

Run:
```
/glean-retriever --input '{
  "entity_type": "glean",
  "query_intent": "What internal docs exist about NWM Epic integration?",
  "scope": {
    "account_id": "nwm",
    "filters": {
      "query": "Northwestern Medicine Epic integration"
    }
  }
}'
```

---

## Notes

- Always use mcp__glean__search and mcp__glean__get_document_content -- never raw HTTP calls
- Glean indexes SFDC, Slack, Confluence, Google Drive, and internal docs
- For SFDC-specific queries, prefer the sfdc-retriever which adds SFDC-specific filters
- Confidence is deterministic: result count is the main driver
- Source tier is always `databricks_internal` (Glean indexes internal Databricks content)
- If Glean is down, degrade gracefully -- never block the caller

---

**Version:** 1.0
**Last Updated:** 2026-04-19
**Contract Reference:** `_System/retriever-contract.md` (immutable)
