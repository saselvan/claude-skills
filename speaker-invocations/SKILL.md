---
name: speaker-invocations
description: "Detailed vault_speaker invocation telemetry — retriever combinations, per-intent latency, outcome distribution, hierarchicalization candidates. USE WHEN speaker-invocations, retriever telemetry, speaker stats, invocation analysis."
---

# /speaker-invocations

Observability skill for vault_speaker retrieval telemetry. Queries `vault_speaker_invocations` table in brain.db to analyze retriever combinations, latency, outcomes, and identify hierarchicalization candidates.

## Invocation

```bash
/speaker-invocations [--intent INTENT] [--days N]    # default: all intents, last 30 days
```

## Implementation

Run the report script, then format output as terminal markdown tables.

```bash
python3 /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/speaker_invocations_report.py [--intent INTENT] [--days N]
```

If the script is unavailable, query brain.db directly.

## Prerequisite

The `vault_speaker_invocations` table must exist (migration 0010). If missing, print:
"vault_speaker_invocations table not found (migration 0010 pending)"

## Queries

### 1. Retriever Combination Frequency

```sql
SELECT
    retriever_set,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vault_speaker_invocations WHERE created_at >= date('now', ? || ' days')), 1) as pct
FROM vault_speaker_invocations
WHERE created_at >= date('now', ? || ' days')
GROUP BY retriever_set
ORDER BY count DESC
```

### 2. Per-Intent Latency

```sql
SELECT
    intent,
    COUNT(*) as n,
    ROUND(AVG(latency_ms), 0) as avg_ms,
    MIN(latency_ms) as min_ms,
    MAX(latency_ms) as max_ms,
    SUM(CASE WHEN latency_ms > 5000 THEN 1 ELSE 0 END) as slow_count
FROM vault_speaker_invocations
WHERE latency_ms IS NOT NULL
  AND created_at >= date('now', ? || ' days')
GROUP BY intent
ORDER BY avg_ms DESC
```

### 3. Outcome-Tag Distribution

```sql
SELECT
    intent,
    COUNT(*) as total,
    SUM(CASE WHEN outcome_tag = 'usable' THEN 1 ELSE 0 END) as usable,
    SUM(CASE WHEN outcome_tag = 'incomplete' THEN 1 ELSE 0 END) as incomplete,
    SUM(CASE WHEN outcome_tag = 'abandoned' THEN 1 ELSE 0 END) as abandoned,
    SUM(CASE WHEN outcome_tag = 'error' THEN 1 ELSE 0 END) as error_ct,
    SUM(CASE WHEN outcome_tag IS NULL THEN 1 ELSE 0 END) as untagged,
    ROUND(SUM(CASE WHEN outcome_tag = 'usable' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as usable_pct
FROM vault_speaker_invocations
WHERE created_at >= date('now', ? || ' days')
GROUP BY intent
ORDER BY usable_pct ASC
```

### 4. Hierarchicalization Candidates

Intent+retriever pairs appearing in >80% of calls for that intent -- these are so dominant they should be hardwired into the planner rather than dynamically selected:

```sql
SELECT
    i.intent,
    i.retriever_set,
    i.combo_count,
    t.intent_total,
    ROUND(i.combo_count * 100.0 / t.intent_total, 1) as dominance_pct
FROM (
    SELECT intent, retriever_set, COUNT(*) as combo_count
    FROM vault_speaker_invocations
    WHERE created_at >= date('now', ? || ' days')
    GROUP BY intent, retriever_set
) i
JOIN (
    SELECT intent, COUNT(*) as intent_total
    FROM vault_speaker_invocations
    WHERE created_at >= date('now', ? || ' days')
    GROUP BY intent
) t ON i.intent = t.intent
WHERE ROUND(i.combo_count * 100.0 / t.intent_total, 1) > 80.0
ORDER BY dominance_pct DESC
```

## Output Format

```
speaker-invocations report (last 30 days)

RETRIEVER COMBINATION FREQUENCY
------------------------------------------------------------
Retriever Set                          Count    %
------------------------------------------------------------
account+temporal+pattern                 142   35.2%
account+stakeholder+temporal              98   24.3%
account+long-tail                         67   16.6%
pattern+glean                             45   11.2%
account+sfdc                              32    7.9%
other combinations                        19    4.7%
------------------------------------------------------------

PER-INTENT LATENCY
------------------------------------------------------------
Intent               N     Avg      Min     Max      Slow
------------------------------------------------------------
synthesis            92   1,247ms   340ms   8,100ms    3
regeneration        156     412ms   120ms   2,800ms    0
signal_extraction   342     287ms    45ms   3,200ms    0
retrieval           201     156ms    28ms   1,900ms    0
------------------------------------------------------------

OUTCOME DISTRIBUTION
------------------------------------------------------------
Intent               Total  Usable  Incomplete  Abandoned  Error  Untagged  Usable%
------------------------------------------------------------
retrieval              201     187          8          3       1         2    93.0%
signal_extraction      342     294         24         12       8         4    85.9%
synthesis               92      81          5          3       2         1    88.0%
regeneration           156     148          4          2       1         1    94.9%
------------------------------------------------------------

HIERARCHICALIZATION CANDIDATES (>80% dominance)
------------------------------------------------------------
Intent               Retriever Set                   Dominance
------------------------------------------------------------
retrieval            account+temporal+pattern          87.3%
signal_extraction    account+temporal+pattern          82.1%
------------------------------------------------------------
  These combos are used so consistently they should be
  hardwired into the planner rather than dynamically selected.
```

## Error Handling

- If brain.db unavailable: "brain.db not accessible"
- If vault_speaker_invocations missing: "vault_speaker_invocations table not found (migration 0010 pending)"
- If no data in range: "No invocations recorded in last N days"
- If --intent specified but not found: "No invocations for intent '{intent}'"

## Related Skills

- `/vault-health` -- high-level health dashboard (includes invocation summary)
- `/evolve` -- uses outcome_tag data for skill evolution decisions
- `/vault-speaker` -- the retriever itself (produces the telemetry this skill reads)
