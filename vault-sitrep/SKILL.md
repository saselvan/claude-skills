# /vault-sitrep

"What happened while you were away" summary from brain.db. Surfaces compiler activity, pending research, overdue commitments, recent corrections, and account health in a single terminal-markdown report.

## Invocation

```bash
/vault-sitrep
/vault-sitrep --since 2026-04-15
/vault-sitrep --account nwm
```

## CLI Args

- `--since DATE` — only show activity since this date (default: 24h ago)
- `--account SLUG` — filter to specific account

## Data Sources

All from `brain.db` via sqlite3. Each section handles missing tables gracefully (table may not exist if migration not yet applied).

| Section | Table(s) | Migration |
|---------|----------|-----------|
| Compiler Activity | `compiler_wiki_runs` | 0013 |
| Pending Interrogations | `interrogation_queue` | 0002 |
| Overdue Commitments | `commitments_expanded` | 0004 |
| Recent Corrections | `corrections`, `corrections_w6` | 0002, 0009 |
| Account Health | `account_state` | 0004 |
| Artifact Outcomes | `artifact_outcomes_expanded` | 0004 |

## Implementation

Run `check_schema_integrity.py` first, then query each section. Use the Python script below.

### Step 1: Run schema check

```bash
python3 /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/check_schema_integrity.py
```

Report any drift warnings before the sitrep.

### Step 2: Run sitrep query script

```bash
python3 /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/vault_sitrep.py [--since DATE] [--account SLUG]
```

The script outputs terminal markdown directly.

### Step 3: Display output

Print the script output as-is. No further formatting needed.

## Output Format

```markdown
# Vault Sitrep — {date}

## Schema Integrity
{clean | N drift warnings — run migrations to fix}

## Compiler Activity
Last run: {date/time} — {status}
Pages updated: {N} | Contradictions: {found}/{resolved}
{If digest exists, show first 5 lines}

## Pending Interrogations ({count})
| Priority | Question | Account | Age |
|----------|----------|---------|-----|
| P{N} | {truncated question} | {account} | {days}d |

## Overdue Commitments ({count})
| Commitment | Account | Due | Days Overdue |
|------------|---------|-----|--------------|
| {desc} | {account} | {date} | {N}d |

## Recent Corrections ({count in period})
{count} corrections applied. Categories: {top 3 learning_category values}

## Artifact Outcomes ({count in period})
| Artifact | Type | Account | Outcome | Status |
|----------|------|---------|---------|--------|
| {id} | {type} | {account} | {outcome} | {status} |

## Account Health
| Account | Status | Engagements | Active Commitments |
|---------|--------|-------------|-------------------|
| {slug} | {health} | {N} | {N} |
```

## Error Handling

- If brain.db is inaccessible: print "brain.db not accessible at {path}" and exit
- If a table does not exist: skip that section with "(table not yet created — run migration 00XX)"
- If no data in a section: print "None in period"

## Related Skills

- `/vault-health` — system telemetry and invocation metrics
- `/forecast` — weekly forecast snapshots
- `/today` — daily priorities dashboard
