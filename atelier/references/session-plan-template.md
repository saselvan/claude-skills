# SESSION_PLAN.md — template

**Goal (ONE):** {the single thing this session proves or produces}
**Tier:** {1/2/3} · **Attended or unattended:** {which, and why}
**Stop condition:** {executable — what green looks like}

## Items
Each item: a checkbox, a one-line acceptance criterion, and (for checks) its red proof.

- [ ] {item} — *accept when:* {criterion} — *red proof:* {how it was shown to fail first}
- [ ] …

## Rules in force this session
- Re-read this file before each item; it is the source of truth over memory.
- Commit per item, message referencing the item.
- Every claim of "passes" is backed by output the human could re-run.
- Every new check ships with its own red proof, run and shown.
- Findings out of scope → REGISTER.md, continue. Decisions not pre-answered → DECISIONS_PENDING.md with reasoning + reversal cost, continue. Hard stops only: irreversible actions, security invariants, real money.

## Close-out (fill before ending)
- STATE.md updated: {yes/no}
- Pushed: {commits}
- Invariant clean: {yes/no}
- First prompt of next session: {written below / N/A}
