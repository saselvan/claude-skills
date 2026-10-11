---
name: compiler-runs
description: "Show compiler wiki run history — status, pages scanned/updated, contradictions, corrections, errors, digest previews. USE WHEN compiler-runs, compiler history, wiki runs, compilation status."
---

# /compiler-runs

Observability skill for the wiki compiler pipeline. Queries `compiler_wiki_runs` table in brain.db to show run history, contradiction tracking, and error diagnostics.

## Invocation

```bash
/compiler-runs [--last N]       # default: last 10 runs
```

## Implementation

Run the report script, then format output as terminal markdown tables.

```bash
python3 /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/compiler_runs_report.py [--last N]
```

If the script is unavailable, query brain.db directly.

## Queries

### 1. Recent Runs Summary

```sql
SELECT
    run_id,
    run_date,
    status,
    pages_scanned,
    pages_updated,
    contradictions_found,
    contradictions_resolved,
    contradictions_queued,
    interrogations_created,
    interrogations_deferred,
    pause_encountered,
    duration_seconds
FROM compiler_wiki_runs
ORDER BY started_at DESC
LIMIT ?
```

### 2. Corrections Applied Per Run

Cross-reference `corrections_v2` with `compiler_wiki_runs` using `last_fired_at` within the run window:

```sql
SELECT
    r.run_id,
    r.run_date,
    COUNT(c.correction_id) as corrections_applied
FROM compiler_wiki_runs r
LEFT JOIN corrections_v2 c
    ON c.last_fired_at BETWEEN r.started_at AND COALESCE(r.completed_at, datetime('now'))
GROUP BY r.run_id
ORDER BY r.started_at DESC
LIMIT ?
```

### 3. Error Log Excerpts

For runs with status = 'failed', show first 500 chars of error_log:

```sql
SELECT run_id, run_date, SUBSTR(error_log, 1, 500) as error_excerpt
FROM compiler_wiki_runs
WHERE status = 'failed' AND error_log IS NOT NULL
ORDER BY started_at DESC
LIMIT 5
```

### 4. Digest Previews

Show first 200 chars of digest for completed runs:

```sql
SELECT run_id, run_date, SUBSTR(digest, 1, 200) as digest_preview
FROM compiler_wiki_runs
WHERE status = 'complete' AND digest IS NOT NULL
ORDER BY started_at DESC
LIMIT 5
```

## Output Format

```
compiler-runs report (last 10 runs)

RECENT RUNS
--------------------------------------------------------------------------------------------
Run Date     Status     Scanned  Updated  Found  Resolved  Queued  Interrog.  Duration
--------------------------------------------------------------------------------------------
2026-04-19   complete      45       12       3        2        1        1       42s
2026-04-18   complete      45       8        1        1        0        0       38s
2026-04-17   failed        23       0        0        0        0        0       12s
2026-04-16   paused        30       5        2        0        2        1       25s
--------------------------------------------------------------------------------------------

CORRECTIONS APPLIED PER RUN
--------------------------------------------------------------------------------------------
Run Date     Corrections Applied
--------------------------------------------------------------------------------------------
2026-04-19           4
2026-04-18           2
--------------------------------------------------------------------------------------------

ERROR LOG EXCERPTS
--------------------------------------------------------------------------------------------
2026-04-17 (failed):
  FileNotFoundError: _wiki/accounts/mayo.md not found after archival...
--------------------------------------------------------------------------------------------

DIGEST PREVIEWS
--------------------------------------------------------------------------------------------
2026-04-19:
  Updated NWM account page with new stakeholder role. Resolved DICOM
  modality conflict between session 2026-04-15 and prior state...
--------------------------------------------------------------------------------------------
```

## Error Handling

- If brain.db unavailable: "brain.db not accessible"
- If compiler_wiki_runs table missing: "compiler_wiki_runs table not found (migration 0013 pending)"
- If no runs found: "No compiler runs recorded yet"

## Related Skills

- `/vault-health` -- overall vault health dashboard (includes compiler summary)
- `/correct` -- creates corrections that the compiler applies
- `/vault-sitrep` -- situational awareness report
