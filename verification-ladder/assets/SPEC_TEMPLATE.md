# {LOOP_NAME}_SPEC.md — {one-line what this loop builds and proves}

Purpose: build and grader-verify {the thing} WITHOUT touching {protected
surfaces}. Deliverable is a verified branch + evidence{, demo'd/merged when
sanctioned}.

ARCHITECTURE (invariant — copy verbatim, then fill):
maker≠grader; state on disk ({LOOP}_ACCEPTANCE.md, LOOP_STATE); oracle rule
(benchmarks assert against hand-computed answers from the primary source and
captured wire responses, never "looks right"). {Protected surface 1}
untouched. {Protected surface 2} untouched. {Isolation mode — e.g.
local/preview deployment only}.

T1 — RECON (evidence before code):
{What must be inspected before any code is written: the API surface, the
library source, the license, the data shape. Name the artifacts.} Record
verdict in {LOOP}_ACCEPTANCE.md: {option (a)} or {option (b)}. Choose by
evidence; {hard requirement that binds either choice}. A verdict that kills
an option is a verdict, not a failure.

T2..Tn — BUILD PHASES:
{One block per phase. Each block names: the exact routes/components/artifacts
to produce, the non-negotiable behaviors (rate limits, caps, audit writes,
scoping rules), and the gate that must be green on the branch (contract
tests, schema gates). Write behaviors as measurable clauses — "poll 1–5s;
10-min cap" — never adjectives.}

T{n+1} — BENCHMARKS (grader, fresh context, via the running system):
  E1: {happy path} → {exact expected artifact/number}, matches hand-computed
      oracle, {N}/{N}.
  E2 ADVERSARIAL: {the known failure mode, reproduced verbatim — the exact
      input that broke it before} → {the poisoned outcome that must NOT
      appear}, {N}/{N} runs: {acceptable outcomes}, never {the poison}.
  E3: {absence case — something that does not exist} → honest "not
      available", no fabricated answer.
  E4: {resource-exhaustion case} → graceful degraded state, no crash, no
      retry storm (assert via wire capture).
  E5: {meta-oracle — every action in E1–E{n} left its required trace (audit
      row, ledger entry, log record)}.
Grader recomputes oracles itself; writes PASS/FAIL with wire evidence.

MEASURED GOAL CONDITIONS: every condition takes one of three shapes —
(a) a graded MATRIX of cells, each with its own oracle query ("150–300
cells. Do not sample."); (b) numbered metrics with explicit baseline→target
numbers ("was 84% → target <15%" — even 'calm' becomes chip counts and a
squint test on an 8x-downscaled screenshot); or (c) run-count benchmarks
("5/5", "10/10", "≥9/10 → KEEP else CUT"). If a condition cannot be counted
or measured, it is not a goal condition — rewrite it until it can.

LEDGER: goal conditions live as rows in {LOOP}_ACCEPTANCE.md (or a
*_MATRIX/*_AUDIT file): `# | Condition | Baseline | Target | After | State`.
States: TODO · FAIL(ref) · FIXED-PENDING-GRADE · WONTFIX(reason) · PASS.
PASS may be written ONLY by the independent grader; the maker's ceiling is
FIXED-PENDING-GRADE. LOOP_STATE.md is the mutation log: every test-time
mutation of protected state, with its revert, so "estate untouched" is
auditable rather than asserted.

STOP RULES: any benchmark failing {K} grades → escalate with transcripts;
budget {M} loops. {Any recon outcome that redirects rather than fails.}

CONSTRAINTS: {protected surfaces, named expendable test rows, spend/rate
budgets, freeze windows, who owns which checkout}. List KNOWN TOOLING
ARTIFACTS (harness quirks) up front so they aren't misfiled as new bugs
mid-loop. Constraints are graded — the grader re-verifies the estate oracle
at final grade, and the mutation log proves the rest.

DELIVERABLE: {LOOP}_ACCEPTANCE.md (recon verdict + evidence, benchmark
results, wire captures, screenshots where UI is involved), branch pushed,
{merged/unmerged per policy}.
