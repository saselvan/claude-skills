---
name: map
description: "Produce a Mutual Action Plan (MAP) for the specified use case. USE WHEN: user says '/map {use-case-slug}', 'build a MAP for {use case}', 'create mutual action plan', or 'draft MAP for {account} {deal}'."
allowed-tools: Read, Write, Glob, Grep, mcp__sa-vault__vault_search, mcp__sa-vault__vault_summary, mcp__sa-vault__vault_reindex
---

# /map {use-case-slug}

Produce a Mutual Action Plan (MAP) for the specified use case.

## Arguments

- `{use-case-slug}` — e.g., `nwm-demand-planning` or just `demand-planning` (then infer account from vault context or ask)

## Inputs

Load in order:
1. Use case file: `UseCases/{account}/{case}/` directory (or `UseCases/{account}/{case}.md`)
2. Account file: `Accounts/{account}.md`
3. Recent sessions related to this use case (use vault_search with account + use case filters)

Extract from these files:
- Current stage and status
- Close date / target decision date
- Key stakeholders and their roles
- Open action items and commitments
- Known success criteria

## Output

Write to `UseCases/{account}/{case}/MAP.md` (or `UseCases/{account}/{case}-MAP.md` if single-file use case):

```yaml
---
artifact_id: "{account}-{case}-map-{date}"
account: "{account}"
artifact_type: mutual_action_plan
title: "Mutual Action Plan — {Use Case Title}"
created: "{date}"
customer_facing: true
provenance:
  extracted: 0
  inferred: 0
  ambiguous: 0
---
```

Content format (buyer language — no internal jargon, no Databricks-internal stage names):

---

# Mutual Action Plan: {Use Case Title}

**{Account Name} + Databricks**
**Target: {goal in customer terms — e.g., "Production deployment of demand planning model"}**
**Decision by: {close date or "TBD"}**

## Our Shared Goal
{1-2 sentences in customer language about what success looks like. Focus on the outcome they care about, not the technology.}

## Milestones

| Date | Action | Owner | Done? |
|------|--------|-------|-------|
| {date} | {milestone} | {Customer Name / Samuel} | ☐ |

*(List milestones in chronological order. Include both parties' actions. Dates should be real or clearly marked TBD.)*

## Open Questions
- {Question that must be answered before proceeding — be specific}

*(Remove this section if no open questions.)*

## Success Looks Like
{What the customer will be able to do when this is done — their words, not product features. Measurable if possible.}

---
*Customer-facing document. Render to PDF: `pandoc MAP.md -o MAP.pdf --pdf-engine=wkhtmltopdf`*
*Internal notes: [Use Case File](./)*

---

## After Writing

Call `vault_reindex(full=false, embed=false)`.

## vault_speaker Integration (Production — W5 Cutover)

**Status:** PRIMARY (graduated from shadow mode)

vault_speaker is the primary context source for MAP generation. Existing retrieval logic (use case files, account files, vault_search) serves as fallback.

### At generation start:

1. Call vault_speaker: `/vault-speaker --intent prep --account {account_id}`
2. If vault_speaker succeeds (returns confidence != low): use its package as primary context
   - Commitments, stakeholders, timeline, and use case status come from vault_speaker
   - Still read use case file directly for stage, close date, and success criteria details
3. If vault_speaker fails or returns confidence=low: fall back to existing retrieval logic (use case files + account file + vault_search)
4. Log outcome_tag to vault_speaker_invocations after generation completes

### Fallback behavior:

- vault_speaker timeout (>15s): use existing retrieval logic, log outcome_tag='timeout'
- vault_speaker error: use existing retrieval logic, log outcome_tag='error'
- vault_speaker confidence=low for all retrievers: use existing retrieval logic, log outcome_tag='low_confidence_fallback'

### What vault_speaker provides (when successful):

- **Commitments**: ours-to-them and theirs-to-us with dates and owners
- **Stakeholders**: key contacts with roles for milestone ownership
- **Timeline**: decision dates, milestone dates, dependencies
- **Use case status**: current stage, blockers, open questions

### What existing logic still owns (always):

- Use case file parsing for stage, close date, MEDPICC details
- Account file reading for account-level context
- Quality rules enforcement (buyer language, owner specificity)

### Logging:

After MAP generation completes, log the invocation:
```yaml
# Append to _System/vault-speaker-invocations.yaml
- skill: map
  account: {account_id}
  timestamp: {ISO 8601}
  intent: prep
  outcome_tag: success | timeout | error | low_confidence_fallback
  context_used: vault_speaker | existing_retrieval
```

---

## Quality Rules

- Buyer language only — no "POC", "Scoping", "MEDPICC", Databricks internal stage names
- Milestones must have owners — never "TBD" as owner
- Success criteria must be measurable or specific — "happy with the result" is not acceptable
- Open Questions section: only include if there are real blockers. Remove if empty.
- Never fabricate stakeholder names, dates, or commitments not found in vault files
