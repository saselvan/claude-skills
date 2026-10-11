---
name: verification-ladder
description: Run a build-and-verify loop where an independent grader — not the maker — decides PASS, every claim is checked against a hand-computed oracle, and all loop state lives on disk. Use this whenever a project must PROVE something works (benchmarks, acceptance evidence, adversarial cases) rather than just build it — demos with a failure mode to prevent, governance/HIPAA-adjacent features, "grader-verified" or "acceptance" asks, autonomous /goal loops, or any request mentioning maker≠grader, oracles, circuit breakers, or evidence-before-code. Also use it when a past failure (a wrong number, a hallucinated answer, a silent rollback) must provably never recur.
---

# Verification Ladder

A loop discipline for building something AND proving it works, developed on
the NWM Metrics CMS Tier-3 loop (embedded Genie panel: spec → recon → build →
adversarial review → benchmarks → independent grading, goal met in one
iteration with zero benchmark failures).

The ladder's rungs, in order. Skipping a rung is how loops produce
plausible-but-unproven work.

## 0 — Isolation: worktree per loop (required setup)

Every loop gets its own git worktree and branch before anything else:

```bash
git worktree add ../<repo>-<loop-name> <loop-branch>
```

Why: loops share machines with other loops and with humans. A dedicated
worktree means your git operations can never race another session's checkout,
your uncommitted state is yours alone, and "main untouched" is structurally
true instead of carefully hoped. Never run git in a checkout another session
owns — if you find yourself needing to, the setup is wrong; fix the setup.
Local servers, venvs, and databases for the loop live in the worktree or the
scratchpad, never in the shared checkout.

## 1 — The spec (state on disk, before any code)

Write `{LOOP}_SPEC.md` from `assets/SPEC_TEMPLATE.md`. The template's
sections are invariant — architecture (maker≠grader, state-on-disk, oracle
rule), measured goal conditions, stop rules (circuit breaker + budget),
constraints, deliverable. Fill them; don't drop them. Two tests of a good
spec:

- Every goal condition has a COUNT and an ORACLE SOURCE ("10/10 runs never
  return the pooled 4.02 blend, oracle = hand-computed warehouse UNION
  average"). Adjectives are not conditions.
- The adversarial benchmark reproduces a REAL prior failure verbatim (the
  exact input that broke it), not a hypothetical.

State lives on disk, not in context: the spec, `{LOOP}_ACCEPTANCE.md`
(verdicts + evidence, updated as you go), and a benchmark protocol file.
Context gets compacted; disk survives. Write verdicts the moment they're
made.

## 2 — The goal string

Set the session goal as a SHORT measurable condition that points at the spec
file rather than restating it:

```
/goal {LOOP}_ACCEPTANCE.md on branch <loop-branch> shows E1–E5 all PASS,
grader-verified per {LOOP}_SPEC.md, with the recon verdict recorded with
evidence, <protected surface> untouched
```

Why this shape: the goal is checkable by reading one file; the spec stays the
single source of truth for WHAT passing means; and "grader-verified" in the
goal string makes maker-graded green insufficient by construction.

## 3 — Subagent routing (model pins are part of the method)

Copy `agents/*.md` into the loop repo's `.claude/agents/` (they register for
future sessions; mid-session, spawn general-purpose agents with the same
model pins and paste the hard rules into the prompt). The routing:

| Role | Model | Why |
|---|---|---|
| `vl-grader` | highest tier available (pinned `fable`; edit to your top tier) | Sole PASS authority, fresh context, read-only, recomputes every oracle itself. Verdict quality is the product — spend here. |
| `vl-maker` | `opus` | Implementation and test-writing from precise briefs. Never grades, never commits. |
| `vl-explorer` | `haiku` | File finding, fact extraction, evidence collection. Read-only, cheap. |

The orchestrator (you) keeps: recon VERDICTS, root-cause diagnosis when a
benchmark fails, the adversarial grading pass on the highest-stakes
benchmark, circuit-breaker decisions, and all commits. Delegation is for
mechanical execution, not judgment.

## 4 — Recon before code

Inspect the real artifacts (registry tarballs, API responses, schemas,
licenses) and record a verdict WITH the evidence in the acceptance file
before building. A recon verdict that kills your preferred option is a
verdict, not a failure — the spec must say so, or the loop will rationalize
past it.

## 5 — Build, then adversarial review, then bench

Build phases go to makers with briefs that quote the spec's measurable
clauses. Between build-green and benchmarks, run a Devil's-Advocate review
(fresh context, high tier) explicitly briefed to BREAK it: governance
bypasses, spec-vs-code diffs, benchmark-protocol loopholes ("does any pass
criterion coincide with a blind spot in the code?"). Triage its findings
yourself; fix before benching. On the Tier-3 loop this caught a cross-user
IDOR and an audit row that the benchmark boundary would have hidden —
benchmarks only prove what they measure, the DA attacks what they don't.

## 6 — Benchmarks with the oracle rule

Before the run: hand-compute every oracle from the primary source and file it
(maker's copy). The bench harness captures WIRE evidence (every request +
response line, timestamped, to files) — verdicts cite captured lines, not
summaries. Read `references/standing-rules.md` and walk its checklist before
declaring the bench ready; it exists because each rule is a bug class that
shipped once.

Make the grader RUNNABLE, not just described. `scripts/oracle_harness.py` is
a black-box skeleton: it drives the running system, compares against
hand-authored expected values, AND independently recomputes the invariants
from the fixtures — two derivations of "correct", so a mis-authored
expectation can't hide a real defect. Adapt the checks; keep the shape.
Hand-author expectations; if you regenerate them from the code you have a
change-detector, not an oracle.

Then prove the harness discriminates BEFORE you trust it: re-introduce the
bug the loop exists to prevent, run the harness, and confirm it goes RED. A
harness that has never failed is not evidence — it's decoration.

## 7 — Independent grading

Spawn `vl-grader` fresh: it recomputes oracles from scratch (bit-for-bit
match with the maker's copy is itself evidence), grades each benchmark
against the protocol citing file+line, writes the grader report, and lists
what it could NOT verify. The orchestrator grades the highest-stakes
adversarial benchmark personally from primary evidence. Only after both:
update the acceptance file's verdict table and close the loop.

Circuit breaker: any benchmark failing K grades (default 3) → STOP,
escalate with transcripts. Budget M loops (default 4). These numbers go in
the spec, and tripping them is a successful outcome of the process.

## 8 — Deliverable

The acceptance file carries: recon verdict + evidence, the verdict table with
per-benchmark evidence citations, post-bench fixes discovered BY the
benchmarks (with their re-verification), a mutation log proving the
constraints held, and environment/teardown notes. Branch pushed. Merge policy
per the spec.

## References

- `assets/SPEC_TEMPLATE.md` — the spec template (copy, fill, keep sections)
- `scripts/oracle_harness.py` — runnable black-box grader skeleton (drive the
  system, compare to hand-authored expectations, recompute invariants); prove
  it goes RED on the known bug before trusting it
- `references/standing-rules.md` — the pre-bench checklist; read before T-bench
- `references/worked-example.md` — the Tier-3 loop end-to-end, with what each
  rung caught; read when unsure how a rung looks in practice
- `agents/vl-grader.md`, `agents/vl-maker.md`, `agents/vl-explorer.md`
