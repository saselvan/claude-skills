# vault-speaker

**Opus orchestrator** that routes vault retrieval requests to specialized retrievers, synthesizes responses, handles contradictions, caches results, and emits telemetry. This is the **central retrieval interface** — ALL skills that need vault context call vault_speaker instead of individual retrievers.

---

## Overview

Answers any vault retrieval need by:
1. Parsing intent + scope
2. Routing to the right combination of retrievers (in parallel)
3. Synthesizing retriever outputs into a unified markdown package
4. Reconciling contradictions across retrievers
5. Caching results (5-minute TTL)
6. Emitting telemetry to brain.db

**Model:** claude-opus-4-6 (orchestrator — NOT Haiku)
**Context budget:** full (needs to synthesize multiple retriever outputs)
**Input:** intent enum + scope dict + optional filters
**Output:** Structured markdown package with frontmatter

---

## Input Contract

```yaml
intent: enum[prep, status, email, deck, signal_extraction, regeneration, synthesis, retrieval]
scope:
  account_id: string (optional)    # e.g., "nwm", "chn"
  project_id: string (optional)    # e.g., "career-growth-2026"
  filters: dict (optional)         # Intent-specific filters (topic, artifact_type, time_window, etc.)
  depth: enum[shallow, standard, deep] (optional, default: standard)
```

**Context resolution:**
- If `account_id` provided → routes to account-scoped retrievers
- If `project_id` provided → routes to project-retriever + account-retriever for the project's account
- If both provided → `account_id` takes precedence

---

## Intent Routing Table

| Intent | Required Retrievers | Optional Retrievers |
|--------|-------------------|-------------------|
| `prep` | account, stakeholder, temporal, consumption, sfdc | artifact, pattern |
| `status` | account, stakeholder, consumption, sfdc | temporal |
| `email` | account, stakeholder, artifact | pattern |
| `deck` | account, artifact, pattern | stakeholder |
| `signal_extraction` | long-tail, account, glean | stakeholder |
| `regeneration` | artifact, account | pattern |
| `synthesis` | account, stakeholder, temporal | artifact, pattern |
| `retrieval` | *(dynamic based on scope)* | all (incl. consumption, glean, sfdc) |

For `retrieval` intent, determine retrievers dynamically:
- If scope has `project_id` → project + account (for the project's account)
- If scope has `account_id` → account + stakeholder
- If scope has filters with `artifact_type` → add artifact
- If scope has filters with `stakeholder_name` → add stakeholder
- If scope has filters with `time_window` → add temporal
- If scope has filters with `topic` → add pattern + long-tail
- Default fallback: account + stakeholder + artifact

---

## Orchestration Process (6 steps)

### Step 1: Parse & Validate Input

```python
import secrets

# Validate intent is in enum
VALID_INTENTS = {"prep", "status", "email", "deck", "signal_extraction", "regeneration", "synthesis", "retrieval"}
assert intent in VALID_INTENTS, f"Invalid intent: {intent}"

# Validate scope has at least one context anchor
assert scope.get("account_id") or scope.get("project_id"), "Scope must include account_id or project_id"

# Generate invocation_id (hex string, no uuid4 dependency) and start timer
invocation_id = secrets.token_hex(16)
start_time = time.monotonic()
```

### Step 2: Check Cache

```python
import hashlib, json

cache_key = hashlib.sha256(json.dumps({
    "intent": intent,
    "scope": scope,
    "depth": depth
}, sort_keys=True).encode()).hexdigest()

# In-memory cache dict (module-level)
_cache = {}  # key → (result, timestamp)
CACHE_TTL = 300  # 5 minutes

if cache_key in _cache:
    result, cached_at = _cache[cache_key]
    if time.monotonic() - cached_at < CACHE_TTL:
        # Cache hit — return cached result with cache_hit=true in frontmatter
        return result
    else:
        del _cache[cache_key]  # Expired
```

### Step 3: Resolve Retriever Set

Look up the routing table for the given intent. For each required retriever, construct an input package following the retriever contract:

```yaml
entity_type: {retriever's entity type}
query_intent: {derived from vault_speaker's intent + scope}
scope:
  account_id: {from scope}
  time_window: {from filters or default "90days"}
  filters: {retriever-specific subset of scope.filters}
```

### Step 4: Invoke Retrievers in Parallel

**Parallel invocation pattern:** Use the Skill tool to invoke each retriever as an independent subagent call. Since retrievers are Haiku agents with isolated context, they can run concurrently without interference.

```
# Conceptual parallel invocation (actual implementation uses Skill tool calls)
results = parallel_invoke([
    invoke_skill("account-retriever", input_package_account),
    invoke_skill("stakeholder-retriever", input_package_stakeholder),
    invoke_skill("temporal-retriever", input_package_temporal),
    # ... etc based on routing table
])
```

Each retriever returns markdown with frontmatter per the retriever contract. Parse the frontmatter from each response to extract:
- `confidence` (high | medium | low)
- `source_count`
- `source_tiers`
- `recency`
- `degradation_flags`
- `fallback_interrogation`

### Step 5: Synthesize & Reconcile

**Synthesis:** Merge all retriever outputs into sections of the output package. Each retriever's body maps to a named section (Account Context, Stakeholder Context, etc.).

**Contradiction reconciliation** — when multiple retrievers return conflicting data on the same entity or fact:

1. **Recency wins:** Compare `recency` timestamps. Most recent source wins.
2. **Outcome confidence:** If same recency, prefer the source with higher `confidence` (high > medium > low).
3. **Source tier weight:** If tied on confidence, prefer higher-weight source tier:
   - `customer_domain` (3) > `session_synthesis` (3) > `sa_observation` (2) = `vault_file` (2) = `signal_database` (2) > `inferred` (1)
4. **Explicit flag:** If still tied, surface BOTH values with `CONFLICTING DATA` flag in the Contradictions section.

```markdown
## Contradictions

### {Entity/Fact Name}
- **Source A** ({retriever}, {recency}, {tier}): {value A}
- **Source B** ({retriever}, {recency}, {tier}): {value B}
- **Resolution:** {which wins and why, OR "CONFLICTING DATA — requires manual validation"}
```

### Step 6: Emit Telemetry

Write telemetry row to brain.db after each invocation:

```python
import sqlite3
from pathlib import Path

BRAIN_DB = Path("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")

def emit_telemetry(invocation_id, intent, scope, retriever_set, latency_ms):
    """Write telemetry row to vault_speaker_invocations table."""
    conn = None
    try:
        conn = sqlite3.connect(str(BRAIN_DB))
        cur = conn.cursor()

        # Ensure table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vault_speaker_invocations (
                invocation_id TEXT PRIMARY KEY,
                timestamp TEXT DEFAULT (datetime('now')),
                intent TEXT,
                scope TEXT,
                retriever_set TEXT,
                latency_ms INTEGER,
                outcome_tag TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        cur.execute("""
            INSERT INTO vault_speaker_invocations
                (invocation_id, intent, scope, retriever_set, latency_ms, outcome_tag)
            VALUES (?, ?, ?, ?, ?, NULL)
        """, (
            invocation_id,
            intent,
            json.dumps(scope),
            json.dumps(retriever_set),
            latency_ms
        ))

        conn.commit()
    except Exception as e:
        # Telemetry failure is non-fatal — log and continue
        print(f"WARNING: telemetry write failed: {e}")
    finally:
        if conn:
            conn.close()
```

**CRITICAL:** Use `?` params for SQLite, NOT `%s`. brain.db is SQLite, not PostgreSQL.

---

## Output Format

The skill returns a structured markdown package:

```markdown
---
vault_speaker_version: "1.0"
intent: {intent}
scope: {scope as YAML}
retriever_count: {N}
total_source_count: {sum of all retriever source_counts}
min_confidence: {lowest confidence across retrievers}
cache_hit: true|false
invocation_id: {UUID}
latency_ms: {total ms}
---

# Vault Speaker Package: {intent} for {context}

## Summary
{1-3 sentence synthesis of all retriever outputs — what does the SA need to know RIGHT NOW}

## Account Context
{from account-retriever, if called — verbatim body from retriever output}

## Stakeholder Context
{from stakeholder-retriever, if called — verbatim body from retriever output}

## Temporal Context
{from temporal-retriever, if called — verbatim body from retriever output}

## Artifact Context
{from artifact-retriever, if called — verbatim body from retriever output}

## Pattern Context
{from pattern-retriever, if called — verbatim body from retriever output}

## Unextracted Signals (Inbox)
{from inbox query, if N > 0 — see "Inbox-Aware Retrieval (W6)" section}
{omit entirely if 0 matching items}

## Contradictions
{any conflicting data between retrievers, with resolution or explicit CONFLICTING DATA flag}
{empty section note if no contradictions found}

## Fallback Interrogations
{aggregated from all retrievers with confidence < high}
{each interrogation includes: question, intent, scope, suggested_approach}

## Degradation Notes
{any retriever degradation flags, cache staleness warnings}
{list which retrievers returned low confidence and why}
```

---

## Invocation Examples

```bash
# Meeting prep for NWM
/vault-speaker --intent prep --account nwm

# Account status for CHN
/vault-speaker --intent status --account chn

# Deck context for NWM governance topic
/vault-speaker --intent deck --account nwm --filters '{"topic": "governance"}'

# Signal extraction (long-tail search)
/vault-speaker --intent signal_extraction --account nwm

# Project-scoped retrieval
/vault-speaker --intent retrieval --project career-growth-2026

# Deep retrieval with all retrievers
/vault-speaker --intent retrieval --account nwm --depth deep
```

---

## Caching Behavior

- **Cache key:** SHA-256 hash of `(intent, scope, depth)` serialized as sorted JSON
- **TTL:** 5 minutes (300 seconds)
- **Storage:** In-memory dict, cleared on skill restart
- **Cache hit:** Return cached result immediately, set `cache_hit: true` in frontmatter, skip retriever calls and telemetry
- **Cache miss:** Invoke retrievers, cache result, set `cache_hit: false`
- **Cache invalidation:** Automatic via TTL expiry. No manual invalidation mechanism (W3 scope).

---

## Contradiction Reconciliation Rules

When multiple retrievers return data about the same entity or fact that conflicts:

| Priority | Rule | Example |
|----------|------|---------|
| 1 | **Recency** — most recent source wins | Session from Apr 18 beats session from Mar 15 |
| 2 | **Outcome confidence** — higher confidence wins | high > medium > low |
| 3 | **Source tier weight** — higher tier wins | customer_domain (3) beats inferred (1) |
| 4 | **Explicit surfacing** — flag CONFLICTING DATA | Both sources shown, SA decides |

**Detection heuristic:** Contradictions are detected when:
- Two retrievers mention the same stakeholder with different stance/sentiment
- Two retrievers report different stage/status for the same use case
- Two retrievers disagree on timeline/close_date for the same deal
- Any factual assertion from one retriever is negated by another

---

## Confidence Cascade

The package's `min_confidence` is the LOWEST confidence across all invoked retrievers. Consuming skills should act on this:

| min_confidence | Consuming Skill Action |
|----------------|----------------------|
| `high` | Proceed with full confidence. Use data as-is. |
| `medium` | Surface fallback interrogations to user. Data usable but flag gaps. |
| `low` | Do NOT use data for customer-facing artifacts without manual validation. Escalate interrogations. |

---

## Telemetry Schema

```sql
CREATE TABLE IF NOT EXISTS vault_speaker_invocations (
    invocation_id TEXT PRIMARY KEY,
    timestamp TEXT DEFAULT (datetime('now')),
    intent TEXT,
    scope TEXT,           -- JSON string of scope dict
    retriever_set TEXT,   -- JSON array of retriever names called
    latency_ms INTEGER,
    outcome_tag TEXT,     -- NULL at invocation time; W4+ producers write it back
    created_at TEXT DEFAULT (datetime('now'))
);
```

**Database:** `brain.db` (SQLite) at `/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db`
**Params:** Use `?` positional params (SQLite), NOT `%s` (PostgreSQL)

---

## Error Handling

| Error | Behavior |
|-------|----------|
| Invalid intent | Return error message, do not invoke retrievers |
| Missing scope (no account_id or project_id) | Return error message |
| Retriever skill not found | Skip that retriever, add `missing_retriever: {name}` to degradation notes |
| Retriever returns error | Log error, continue with remaining retrievers, add to degradation notes |
| All retrievers fail | Return package with `min_confidence: low` and all degradation flags |
| brain.db unavailable for telemetry | Log warning, return package anyway (telemetry is non-fatal) |
| Cache corruption | Clear cache entry, proceed with fresh retrieval |

---

## Implementation Checklist

- [ ] Accepts input package (intent, scope, filters, depth)
- [ ] Validates intent against enum
- [ ] Validates scope has at least one context anchor
- [ ] Generates invocation_id (UUID) and starts timer
- [ ] Checks in-memory cache (5-min TTL)
- [ ] Resolves retriever set from routing table
- [ ] For `retrieval` intent, dynamically selects retrievers based on scope
- [ ] Constructs input packages for each retriever per retriever contract
- [ ] Invokes retrievers via Skill tool (parallel when possible)
- [ ] Parses frontmatter from each retriever response
- [ ] Synthesizes body sections from retriever outputs
- [ ] Queries inbox for unextracted items matching account scope (W6)
- [ ] Appends Unextracted Signals section if N > 0, adds inbox_unprocessed to degradation_flags
- [ ] Detects contradictions across retriever outputs
- [ ] Applies 4-step reconciliation (recency → confidence → tier → flag)
- [ ] Aggregates fallback interrogations from low/medium confidence retrievers
- [ ] Aggregates degradation flags
- [ ] Computes min_confidence across all retrievers
- [ ] Builds output markdown package with all frontmatter fields
- [ ] Caches result (on cache miss)
- [ ] Emits telemetry row to brain.db vault_speaker_invocations table
- [ ] Returns markdown package

---

## Consumer Skills

These skills call vault_speaker instead of individual retrievers:

| Skill | Intent Used |
|-------|-------------|
| `/prep` | `prep` |
| `/forecast` | `status` |
| `/email`, `/draft-followup` | `email` |
| `/deck-render`, `/strategy` | `deck` |
| `/process-transcript` | `signal_extraction` |
| `/content-factory` | varies by artifact |
| `/commercial-insight` | `synthesis` |
| `/account-plan` | `retrieval` (deep) |

---

## Contract Reference

- Retriever contract: `/Users/samuel.selvan/obsidian/sa-intel/_System/retriever-contract.md`
- Brain DB: `/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db`
- Account slugs: `/Users/samuel.selvan/obsidian/sa-intel/_System/account-slugs.yaml`

---

## Notes

- Always use vault MCP tools via retrievers — vault_speaker never queries brain.db directly for vault data (only for telemetry writes)
- Retrievers are Haiku agents; vault_speaker is Opus (orchestration requires synthesis quality)
- Cache is in-memory only — no persistence across skill restarts
- Telemetry writes are fire-and-forget; failure does not block response
- The `outcome_tag` column is NULL at write time; downstream W4+ feedback loops populate it
- `project_id` support requires project-retriever (stub in W3); if unavailable, fall back to account-retriever with project name as query

---

## Inbox-Aware Retrieval (W6)

After all retrievers return their packages (Step 4), vault_speaker queries the inbox table for unprocessed items matching the current scope. This surfaces unextracted signals that may be relevant but have not yet been through the extraction pipeline.

### When to Query

- Only when `scope.account_id` is provided
- Only after retriever results are collected (between Step 4 and Step 5)
- Query is non-fatal: if inbox table doesn't exist or query fails, skip silently

### Query

```python
import sqlite3
from pathlib import Path

BRAIN_DB = Path("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")

def query_inbox_unextracted(account_id: str, limit: int = 10) -> list[dict]:
    """Query inbox for unreviewed items matching account scope."""
    conn = None
    try:
        conn = sqlite3.connect(str(BRAIN_DB))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Check table exists
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='inbox'"
        )
        if not cur.fetchone():
            return []

        cur.execute("""
            SELECT inbox_id, SUBSTR(raw_content, 1, 60) AS preview,
                   source_type, source_tier, created_at, action_label
            FROM inbox
            WHERE triage_status = 'unreviewed'
              AND account_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (account_id, limit))

        rows = cur.fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []
    finally:
        if conn:
            conn.close()
```

### Output Section

If unextracted items are found (N > 0), append this section to the package **after** the retriever context sections and **before** the Contradictions section:

```markdown
## Unextracted Signals (Inbox)
⚠️ {N} unprocessed items in inbox matching this scope — confidence unknown

| Item | Source | Age | Status |
|------|--------|-----|--------|
| {preview (first 60 chars of raw_content)} | {source_type} | {days}d | unreviewed |

These items have NOT been extracted. Treat as potential signals but do not cite as confirmed facts.
```

Age calculation: `(now - created_at).days`

If 0 unextracted items match: **omit the section entirely** (do not show an empty table).

### Degradation Impact

If unextracted items exist, add `inbox_unprocessed` to the package's `degradation_flags` list. This signals to consuming skills that the vault may have incomplete coverage for this account.

In the Degradation Notes section, include:

```markdown
- **inbox_unprocessed**: {N} unreviewed inbox items match this account scope. Run `/extract-inbox --account {account_id}` to process them.
```

### Cache Interaction

Inbox query results are included in the cached package. When the cache TTL expires and a fresh retrieval runs, inbox state is re-queried. No separate cache invalidation is needed for inbox changes.

---

**Version:** 1.1
**Last Updated:** 2026-04-19
**Contract Reference:** `_System/retriever-contract.md` (immutable)
