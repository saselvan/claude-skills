---
name: vault-health
description: "Full observability dashboard for vault telemetry and system health. Confidence distribution, stale entries, contradictions, interrogation queue, latency analysis. USE WHEN vault-health, system health, telemetry, observability."
---

# /vault-health

Full observability skill for vault telemetry and system health. Queries brain.db for confidence distribution, stale entries, unresolved contradictions, interrogation queue status, and latency analysis.

## Invocation

```bash
/vault-health [--account ACCOUNT] [--since DATE] [--intent INTENT]
```

## Implementation

Run the report script, then format the output as terminal markdown tables.

```bash
python3 /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/vault_health_report.py [--account ACCOUNT] [--since DATE] [--intent INTENT]
```

If the script is unavailable, query brain.db directly using the sections below.

## Report Sections

### 1. Telemetry by Intent

Query `vault_speaker_invocations` (if table exists). Group by `intent`, show:
- Count of invocations
- Success count and rate (outcome_tag = 'usable')
- Average latency_ms

If table does not exist, print: "vault_speaker_invocations table not found (migration 0010 pending)"

### 2. Confidence Distribution

Query `vault_speaker_invocations` WHERE outcome_tag IS NOT NULL. Group by intent, then bucket confidence:
- **high**: outcome_tag = 'usable'
- **medium**: outcome_tag = 'incomplete'
- **low**: outcome_tag IN ('abandoned', 'error')

Show % distribution per intent. If table missing, skip with note.

### 3. Stale Entries

Query `artifacts` WHERE `created_at < date('now', '-30 days')` and no `updated_at` within 30 days. Also check `chunks` WHERE `created_at < date('now', '-30 days')`. Report count per entity_type.

Additionally, check `corrections_v2` WHERE `last_fired_at IS NULL AND created_at < date('now', '-30 days')` -- corrections that have never fired.

### 4. Unresolved Contradictions

Scan `corrections_v2` for active corrections (is_active = 1). Group by:
- `source_type` (wiki_page, derived_chunk, account_state, stakeholder_view)
- `correction_type` (override, demote)

Also count `compiler_wiki_runs` WHERE `contradictions_found > contradictions_resolved` for runs with unresolved contradictions.

### 5. Interrogation Queue by Priority

Query `interrogation_queue` grouped by priority and status:

```sql
SELECT priority, status, COUNT(*) as count
FROM interrogation_queue
GROUP BY priority, status
ORDER BY priority, status
```

Flag overdue entries: status = 'pending' AND created_at < date('now', '-7 days').

### 6. Latency Analysis (if vault_speaker_invocations exists)

Per-intent latency percentiles. Use ORDER BY + LIMIT for approximate percentiles:

```sql
-- p50 approximation
SELECT intent,
       COUNT(*) as n,
       AVG(latency_ms) as avg_ms,
       MIN(latency_ms) as min_ms,
       MAX(latency_ms) as max_ms
FROM vault_speaker_invocations
WHERE latency_ms IS NOT NULL
GROUP BY intent
```

Flag slow invocations: latency_ms > 5000.

## Output Format

Terminal markdown tables. Example:

```
vault-health report (2026-04-19)

TELEMETRY BY INTENT
------------------------------------------------------------
Intent               Count    Success    Avg Latency
------------------------------------------------------------
signal_extraction      342    294 (86%)  287ms
regeneration           156    148 (95%)  412ms
synthesis               92     81 (88%)  1,247ms
retrieval              201    187 (93%)  156ms
------------------------------------------------------------

CONFIDENCE DISTRIBUTION
------------------------------------------------------------
Intent               High %   Medium %   Low %
------------------------------------------------------------
signal_extraction     86%      8%         6%
regeneration          95%      3%         2%
synthesis             88%      7%         5%
------------------------------------------------------------

STALE ENTRIES (>30 days without update)
------------------------------------------------------------
Entity Type          Count    Oldest
------------------------------------------------------------
artifacts              12     2026-02-15
chunks                 34     2026-01-28
never-fired corr.       2     2026-03-01
------------------------------------------------------------

UNRESOLVED CONTRADICTIONS
------------------------------------------------------------
Source Type           Active Corrections    Unresolved Runs
------------------------------------------------------------
wiki_page                    3                   2
account_state                1                   0
------------------------------------------------------------

INTERROGATION QUEUE
------------------------------------------------------------
Priority   Pending   Processing   Complete   Failed   Overdue
------------------------------------------------------------
P1             2          1           45        3        0
P3             5          0           32        2        1
P5             5          2           50        3        4
------------------------------------------------------------

LATENCY ANALYSIS
------------------------------------------------------------
Intent               Avg      Min      Max      Slow (>5s)
------------------------------------------------------------
signal_extraction    287ms    45ms     3,200ms   0
synthesis          1,247ms   340ms    8,100ms    3
------------------------------------------------------------
```

## Error Handling

- If brain.db unavailable: return "brain.db not accessible at /Users/samuel.selvan/obsidian/sa-intel/_System/brain.db"
- If vault_speaker_invocations missing: skip telemetry/confidence/latency sections with migration-pending note
- If no data in date range: return "No records in date range"
- If account not found: show all-account summary (remove filter)

## Related Skills

- `/compiler-runs` -- detailed compiler wiki run history
- `/speaker-invocations` -- detailed vault_speaker telemetry
- `/evolve` -- uses outcome_tag data for skill improvement
- `/interrogate` -- submits queries to interrogation_queue
- `/signal` -- emits telemetry via PostToolUse hook

## Implementation Notes

- Uses sqlite3 with ? params throughout
- All data from brain.db -- no external API calls
- Read-only; safe for repeated invocations
- Script at `_System/scripts/vault_health_report.py` for CLI usage
