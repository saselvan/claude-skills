# DECISIONS.md — the unattended-run decision policy (template)

Paste into every long-run prompt. This is what makes unattended hours worth anything: an agent that stops to ask at 1 AM converts eight hours into zero.

## Pre-answered categories (never ask)
- Contract vs prototype/spec conflict → **the contract wins**; log to DESIGN_DIVERGENCE.md.
- Anything risky → **throwaway copy first**, then the real target.
- Real finding, out of scope → **REGISTER.md**, continue.
- Item green → **commit**, continue.
- Two implementation options, both reversible → **pick one, note why**, continue.
- {project-specific pre-answers — add the 3–5 questions this project will predictably raise}

## Standing instruction (everything else)
If blocked on a decision not covered above, make the call a competent senior engineer would make, record it in **DECISIONS_PENDING.md** with (a) the decision, (b) your reasoning, (c) what reversing it would take — and continue.

## Hard stops (the only reasons to wait for a human)
1. Anything **irreversible**: schema changes, deletions, production deploys, credential/identity changes.
2. Anything that **weakens a security invariant**.
3. Anything that **spends real money** beyond the session budget.

Reversibility is the sort key: two-way doors are yours, always; one-way doors queue. If a one-way door blocks all remaining work, stop *safely* and say so — a safe stop overnight is a fine outcome; continuing wrongly is the only disaster.

## Morning protocol (for the human)
1. Workbench / gates output — 5 minutes.
2. DECISIONS_PENDING.md — reverse the one or two you'd have called differently.
3. REGISTER.md — triage at phase boundaries only.
