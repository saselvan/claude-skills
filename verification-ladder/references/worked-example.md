# Worked example — the Tier-3 embedded-Genie loop (NWM Metrics CMS)

One full ladder, run 2026-07-11 on branch `genie-embed`, goal met in a single
iteration with zero benchmark failures. Read this to see what each rung looks
like in practice and — more useful — what each rung CAUGHT that the previous
rungs missed. Source artifacts: `TIER3_SPEC.md`, `TIER3_ACCEPTANCE.md`,
`bench/` on that branch. Sibling specs of the same pattern: FUNCTIONAL_SPEC
(matrix-of-cells goals), CALM_SPEC (baseline→target design metrics),
GENIE_SPEC (KEEP/CUT decision benchmarks, on branch genie-setup).

## The spec (rung 1)

TIER3_SPEC.md in one architecture line:

> maker≠grader; state on disk (TIER3_ACCEPTANCE.md, LOOP_STATE); oracle rule
> (benchmarks assert against hand-computed warehouse answers and captured
> wire responses, never "looks right"). Estate untouched. Deployed app
> untouched. Local/preview deployment only.

Goal conditions were counts with oracle sources: E1 "matches hand-computed
oracle, 5/5"; E2 ADVERSARIAL replayed the exact prior failure — the raw
question "what's our average length of stay", which had once produced a
cross-grain pooled blend of 4.02 — "10/10 runs … never a pooled number"; E3
honest not-available for a metric with no view; E4 rate-limit exhaustion with
wire-captured backoff; E5 an audit row for every question. Stop rules: 3
failed grades → escalate; budget 4 loops.

## Isolation (rung 0)

`git worktree add ../nwm-genie-embed genie-embed` — mandatory because a
second session owned the main checkout (with uncommitted changes) the whole
time. Every server, venv, and a throwaway local Postgres (:55432, schema
deployed from the repo DDL, three metrics seeded from the real seed script)
lived in the worktree/scratchpad. The shared Lakebase was never a write
target; `DATABRICKS_APP_NAME` was never set (that env flips the pool to the
shared DB — a run-discipline item on the checklist).

## Goal string (rung 2)

> /goal TIER3_ACCEPTANCE.md on branch genie-embed shows E1–E5 all PASS,
> grader-verified per TIER3_SPEC.md, with the T1 recon verdict recorded with
> evidence, main untouched, and the demo estate unchanged

Short, checkable by reading one file, "grader-verified" baked in.

## Recon verdict (rung 4)

Question: reuse `@databricks/appkit-ui`'s GenieChat against a FastAPI proxy
speaking its contract (a), or borrow the design and build on our tokens (b)?
Evidence gathered from the actual npm tarballs: prop surface `{alias,
basePath, placeholder, className}` — no per-message hook, so the governance
prefix couldn't be injected client-side; Tailwind/shadcn styling vs. our
CSS-variable token system; 25+ radix deps + echarts + arrow; Express server
plugin vs. our FastAPI. Verdict (b), recorded with the evidence table in the
acceptance file. What we kept from appkit: the SSE event vocabulary, two-
phase result fetch, 3s poll default, error classification map.

## Build (rung 5, makers on opus)

Backend proxy (scoped ask over SSE, per-user 5/min honest 429, poll 2s→5s,
10-min cap, audit every ask), frontend panel (scope-transparency line,
Generated-SQL collapsible, honest busy/timeout/access/failed states, calm
tokens only), contract gates green (routes + response models in OpenAPI,
schema types regenerated, RAW_FETCHES entry for the SSE POST).

## The DA review (rung 5.5) — what it caught that tests didn't

Fresh-context adversarial reviewer, briefed to BREAK it. Found, pre-bench:
- **F1 (HIGH)**: client-supplied conversation_id was unbound — cross-user /
  cross-metric conversation hijack, invisible to every planned benchmark
  (E2 uses fresh conversations). Fixed by binding conversations to
  (metric, principal) via the audit trail itself.
- **F3/F8**: 429-rejected asks weren't audited — and the benchmark protocol's
  E5 boundary happened to exclude exactly that gap. The protocol was widened
  AND the code fixed. Lesson: run the DA against the benchmark protocol too;
  ask "does any pass criterion coincide with a code blind spot?"
- **F2**: "structurally cannot ask the unqualified form" was overstated — the
  guarantee is transmit-level (prefix always sent), model obedience is
  behavior. The claim was corrected and two injection probes (E2i) added so
  obedience is measured, not assumed.

## Bench + what the benchmarks themselves caught (rung 6)

Oracles hand-computed first: inpatient 4.891666666666663 (n=1200), the
poisoned pooled blend 4.024809523809521 (n=2100). Harness captured every
request and SSE line to JSONL. Two audit-persistence bugs were found only by
LIVE probes, after all 79 unit tests were green:
1. The RATE_LIMITED audit row silently vanished — written on the request's
   dependency connection, rolled back when the 429 HTTPException propagated
   through the pool context. The unit test asserted the CALL, not the
   persistence (see standing-rules #3).
2. A client disconnecting mid-stream left the worker thread blocked on a dead
   consumer — the completion audit row never landed (this empirically
   REFUTED the DA's own "mid-stream disconnect does audit" claim). Fixed
   additively with an `ask_submitted` row at transmit time, so the evidence
   already captured stayed valid; a live disconnect probe verified it.

## Grading (rung 7)

Fresh-context grader recomputed all three oracles from the warehouse —
bit-for-bit match with the maker's file — then graded E1/E3/E4/E5 citing
wire lines and live DB rows, and listed what it could not verify. The
orchestrator personally graded E2/E2i from primary evidence (grep of the
raw wire for every poisoned value: zero occurrences in 10/10 runs; both
injection probes refused). Verdict table + evidence went into
TIER3_ACCEPTANCE.md; branch pushed, unmerged per the freeze.

## The doctrine, earned empirically

From FUNCTIONAL_LOOP_SUMMARY.md (the loop that preceded this one):

> A UI assertion is only trustworthy when checked against a database/API
> oracle by a session that did not build it. Every bug in class A/B above
> passed unit tests, returned HTTP 200, and "looked right" — they were only
> exposed by operating the deployed app against ground truth.

Its grader's iteration-1 alone found 15 FAILs the maker believed were fixed.
The dominant bug class (frontend↔API contract drift) became a permanent CI
gate (the SCHEMA CONTRACT rule) — the loop's output is governance, not just
a fixed app.
