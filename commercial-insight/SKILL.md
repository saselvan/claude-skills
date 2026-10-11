---
name: commercial-insight
description: "Produce a 1-page Challenger reframe for the specified account, synthesized from extracted commercial insights across all sessions. USE WHEN: user says '/commercial-insight {account}', 'build commercial insight for {account}', or 'what's our challenger reframe for {account}'."
allowed-tools: Read, Write, Glob, Grep, mcp__sa-vault__vault_search, mcp__sa-vault__vault_summary, mcp__sa-vault__vault_reindex
---

# /commercial-insight {account}

Produce a 1-page Challenger reframe for the specified account.

## Arguments

- `{account}` — account slug (e.g., `nwm`, `chn`, `chla`, `providence`)

## Inputs

Load in order:
1. All commercial insight files: `_System/coaching/commercial-insights-{account}-*.md`
2. Account file: `Accounts/{account-name}.md` (use vault_search if slug → name mapping needed)
3. Recent sessions: last 3 session files from `Sessions/{account-name}/`

If no commercial insight files exist yet, note this in the output and synthesize from session files directly.

## Output

Write to `Accounts/{account-slug}/commercial-insight.md`:

```yaml
---
artifact_id: "{account}-commercial-insight-{date}"
account: "{account}"
artifact_type: commercial_insight
title: "Commercial Insight — {Account Name}"
created: "{date}"
supersedes: "{previous version id or null}"
provenance:
  extracted: N
  inferred: N
  ambiguous: 0
---
```

Then produce a structured 1-pager:

---

# Commercial Insight: {Account Name}

## The Status Quo They're Defending
{What the customer currently believes is fine — specific, customer's own words when possible}

## What the Data Shows
{Specific benchmarks, industry data, or comparable customer outcomes that challenge the status quo}

## The Real Cost of Inaction
{Translate the gap into dollars, time, or risk — their frame, not yours. Be specific: "$X/year", "N FTEs", "Q{N} slip"}

## The Reframe (Teaching Moment)
{The Challenger-style insight that changes how they see the problem. One clear paragraph. No Databricks product names — their problem, not our features.}

## Evidence in Our Conversations
{Specific quotes or moments where this insight was delivered or where it clearly applies. Format:
> "Exact quote" — Stakeholder Name, Session Date}

---
*Regenerate with: `/commercial-insight {account}`*
*Sources: {N} commercial insights extracted from {N} sessions*

---

## After Writing

Call `vault_reindex(full=false, embed=false)`.

## vault_speaker Integration (Production — W5 Cutover)

**Status:** PRIMARY (graduated from shadow mode)

vault_speaker is the primary context source for commercial insight generation. Existing retrieval logic (commercial insight files, account file, session reads) serves as fallback.

### At generation start:

1. Call vault_speaker: `/vault-speaker --intent retrieval --account {account_id}`
2. If vault_speaker succeeds (returns confidence != low): use its package as primary context
   - Account signals, stakeholder sentiments, and competitive context come from vault_speaker
   - Still read commercial insight files from `_System/coaching/` for extracted insights
3. If vault_speaker fails or returns confidence=low: fall back to existing retrieval logic (commercial insight files + account file + session reads)
4. Log outcome_tag to vault_speaker_invocations after generation completes

### Fallback behavior:

- vault_speaker timeout (>15s): use existing retrieval logic, log outcome_tag='timeout'
- vault_speaker error: use existing retrieval logic, log outcome_tag='error'
- vault_speaker confidence=low for all retrievers: use existing retrieval logic, log outcome_tag='low_confidence_fallback'

### What vault_speaker provides (when successful):

- **Account signals**: recent momentum, risks, commitments
- **Stakeholder sentiments**: how key contacts feel about status quo vs change
- **Competitive context**: incumbent positioning and vulnerability points

### What existing logic still owns (always):

- Commercial insight file extraction from `_System/coaching/commercial-insights-{account}-*.md`
- Direct session quote extraction for the "Evidence in Our Conversations" section
- Provenance tracking (extracted vs inferred counts)

### Logging:

After commercial insight generation completes, log the invocation to brain.db:
```python
import sqlite3, json, secrets
db = sqlite3.connect("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")
db.execute("""
    INSERT INTO vault_speaker_invocations
    (invocation_id, run_id, intent, scope, outcome_tag, latency_ms)
    VALUES (?, ?, 'retrieval', ?, ?, ?)
""", (
    secrets.token_hex(16), secrets.token_hex(16),
    json.dumps({"account_id": account_id, "skill": "commercial-insight"}),
    outcome_tag,  # 'success' | 'timeout' | 'error' | 'low_confidence_fallback'
    latency_ms,
))
db.commit()
db.close()
```

---

## Quality Rules

- Never invent data points — cite source or mark as inferred
- Reframe must be in customer's language, not Databricks feature language
- Cost of inaction must be specific — "significant" is not acceptable
- If provenance is zero (no extracted insights, no session data), output a warning and stop
