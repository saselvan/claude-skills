# Status — SA Intelligence Vault

Manager-consumable account or project status summary. Concise, 1-page, actionable. Output rendered as terminal markdown (not saved to file).

## Usage

```
/status [account]                    # Account status summary
/status --project [project-id]       # Project-scoped status
/status nwm                          # NWM account status
/status chn                          # CHN account status
/status all                          # All active accounts (nwm, chn)
```

## Vault Speaker Integration

**Step 1: Invoke vault_speaker as the primary context source.**

```
/vault-speaker --intent status --account {account_id}
```

Or for project-scoped status:

```
/vault-speaker --intent status --project {project_id}
```

This replaces manual vault queries. The vault_speaker package for intent=status includes:
- Account Context (use cases, stages, MRR, health, risks)
- Stakeholder Context (key contacts, engagement level)
- Contradictions (flagged for review)

**Step 2: Parse the vault_speaker package.**

Extract frontmatter fields:
- `invocation_id` — needed for outcome feedback (Step 4)
- `min_confidence` — determines data trustworthiness
- `cache_hit` — informational

**Step 3: Generate status output.**

Map vault_speaker sections to status output:

| Vault Speaker Section | Status Section |
|---|---|
| Account Context | Account Health, Pipeline Summary, Use Case Status |
| Stakeholder Context | Key Contacts, Engagement |
| Contradictions | Flags / Warnings |

**Confidence handling:**
- `high` — proceed normally
- `medium` — add note: "Some data may be stale"
- `low` — add warning: "Data quality is low — manual vault review recommended"

**Step 4: Log outcome feedback.**

After generating status output, log the invocation using the shared helper:

```python
python3 -c "
import sys; sys.path.insert(0, '/Users/samuel.selvan/obsidian/sa-intel/_System/scripts')
from shared.invocation_logger import log_invocation
log_invocation(intent='status', caller_skill='status', scope={'account': '{account_id}'}, outcome_tag='usable')
"
```

Valid outcome_tag values: `usable`, `incomplete`, `abandoned`, `error`.

**Outcome feedback mechanism:**
- If user gives thumbs-down or says "this is wrong" -> update to 'incomplete'
- If user abandons and re-runs -> update prior invocation to 'abandoned'
- Default assumption: if user proceeds without complaint -> 'usable'

---

## Fallback: Direct Vault Queries

If vault_speaker is unavailable, fall back to:

1. `vault_summary(account="[name]")` — account overview
2. `vault_signals(account="[name]", status="open")` — open signals

Log degradation warning: "vault_speaker unavailable — using direct vault queries"

---

## Output Format (Terminal Markdown)

Status output is displayed directly in the terminal. Never write to file.

```markdown
# Status: [Account]
**As of:** [Today]
**Data source:** vault_speaker (invocation: {invocation_id})

---

## Account Health: [GREEN | YELLOW | RED]

| Metric | Value |
|--------|-------|
| Total Pipeline MRR | $X |
| Active Use Cases | N |
| On Track | N |
| Slipping | N |
| At Risk | N |
| Primary Competitor | [Name] |

---

## Pipeline Summary

| Use Case | Stage | MRR | Close Date | Status | Delta |
|----------|-------|-----|------------|--------|-------|
| [UC 1] | Evaluation | $25K | May 15 | On Track | -- |
| [UC 2] | Scoping | $15K | Jun 01 | Slipping | +14d |
| [UC 3] | Validating | $10K | TBD | At Risk | new |

---

## Key Risks

| Risk | Use Case | Severity | Action Needed |
|------|----------|----------|---------------|
| [Risk 1] | [UC] | Critical | [What to do] |
| [Risk 2] | [UC] | High | [What to do] |

---

## Open Action Items

| Item | Owner | Due | Status |
|------|-------|-----|--------|
| [Action 1] | [Name] | [Date] | Overdue |
| [Action 2] | [Name] | [Date] | Pending |

---

## Engagement Summary

- Last customer meeting: [Date] ([N] days ago)
- Next scheduled: [Date] or "None scheduled"
- Key contacts: [N] active stakeholders
- Champion status: [Name] — [Active | Quiet | At Risk]

---

## Manager Talking Points

1. **[UC 1]:** [One-sentence status + next step]
2. **[UC 2]:** [One-sentence status + concern]
3. **Overall:** [One-sentence account trajectory]

---

## Flags

{Contradictions or data quality warnings from vault_speaker}
{Empty if none}
```

---

## Multi-Account Status (`/status all`)

When `all` is specified, invoke vault_speaker once per active account (nwm, chn) and produce a consolidated view:

```markdown
# Territory Status
**As of:** [Today]

## Account Summary

| Account | Health | Pipeline MRR | Active UCs | On Track | Slipping | At Risk |
|---------|--------|-------------|------------|----------|----------|---------|
| NWM | YELLOW | $X | N | N | N | N |
| CHN | GREEN | $Y | N | N | N | N |
| **Total** | -- | **$Z** | **N** | **N** | **N** | **N** |

## Top Risks (Cross-Account)

| Account | Risk | Use Case | Severity |
|---------|------|----------|----------|
| NWM | [Risk] | [UC] | Critical |
| CHN | [Risk] | [UC] | High |

## This Week's Priorities

1. [Account] — [Action needed]
2. [Account] — [Action needed]
3. [Account] — [Action needed]
```

---

## Project-Scoped Status (`/status --project`)

For non-account projects (career, internal tools, etc.):

```markdown
# Status: [Project Name]
**As of:** [Today]

## Progress

| Phase | Status | Notes |
|-------|--------|-------|
| [Phase 1] | Complete | [Summary] |
| [Phase 2] | In Progress | [Summary] |
| [Phase 3] | Not Started | [Dependencies] |

## Open Items

| Item | Priority | Due |
|------|----------|-----|
| [Item 1] | High | [Date] |

## Next Steps

1. [Action 1]
2. [Action 2]
```

---

## Notes

- Output is always terminal markdown — never written to a file
- Designed for quick consumption by managers (Catherine Fan) or in 1:1s
- For detailed meeting prep, use `/prep` instead
- For forecast-specific views, use `/forecast`
- vault_speaker intent=status routes to account + stakeholder retrievers (no temporal by default)

$ARGUMENTS
