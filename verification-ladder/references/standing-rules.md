# Standing rules — the pre-bench checklist

Walk this before declaring a bench ready, and again before the final grade.
Each rule exists because its violation shipped a real bug that "passed unit
tests, returned HTTP 200, and looked right" (FUNCTIONAL_LOOP_SUMMARY.md, NWM
Metrics CMS). Check the box only with evidence, not intent.

## 1. Oracle rule
Every truth claim resolves to an external ground truth: a direct DB query, a
raw API/wire response, a hand-computed answer from the primary source, or a
DOM/pixel measurement. Never code inspection, never the maker's summary,
never "looks right." Even qualitative goals get operationalized (the CALM
loop turned "calm" into chip-count percentages, font-size enumeration, a
squint test on an 8x-downscaled screenshot).
- [ ] Every benchmark row names its oracle source.
- [ ] The grader recomputes oracles independently; maker's copy is only a
      cross-check (bit-for-bit agreement is itself evidence).

## 2. Deployed-truth verification
Grade what actually runs, not what the repo contains. A command exiting 0 is
not confirmation; `apps deploy` alone does not prove the live app serves new
code. Verify a live version marker (bundle hash, asset timestamp) against the
build output; after any seed/insert, SELECT the rows back and spot-check
values (no NULLs where the UI needs data, filters match, counts equal
oracle).
- [ ] The bench runs against a RUNNING system, not test doubles.
- [ ] Post-seed spot-check output is captured in the evidence.
- [ ] If a deploy is involved: live version marker checked, not assumed.

## 3. Mutation-test the load-bearing assertions
For every assertion that a verdict depends on, ask: if the implementation
were structurally present but broken, would this catch it? Status-code-only
tests, render-without-fetch tests, and mocked-DB green are how the Revenue
Radar failure happened. Where cheap, actually break the code (or the
transaction semantics) and watch the assertion fail. The Tier-3 loop's
RATE_LIMITED audit bug is the canonical case: the unit test asserted the
audit CALL happened; only a live probe caught that the row was rolled back —
the assertion wasn't load-bearing until it checked persistence.
- [ ] Each load-bearing assertion has been argued (or demonstrated) to fail
      under a broken implementation.
- [ ] Mock boundaries: external services only. Never the DB, never the
      agent's tool invocation.

## 4. Contract gates per bug class
When grading exposes a recurring bug CLASS, the loop's deliverable includes a
permanent, mechanical gate for that class — not just the fixes. The NWM
functional loop's dominant class (frontend↔API field/vocabulary drift) became
the SCHEMA CONTRACT standing rule: UI reads only schema-derived types;
`check:schema` regenerates OpenAPI + TS types and diffs in CI; new response
interfaces require key-subset assertions; endpoints returning bare dicts must
gain a response_model first (else the schema is empty and the contract is
toothless).
- [ ] Recurring bug classes from this loop are named in the acceptance file.
- [ ] Each has a CI-enforceable gate (schema diff, contract test, lint), not
      a "remember to" note.

## 5. Estate preservation is graded, not asserted
Constraints name the protected surfaces (frozen branches, shared databases,
governed catalogs, planted demo state) and the specific rows that are
expendable. Every test-time mutation goes in the LOOP_STATE mutation log with
its revert. The GRADER re-verifies the estate oracle at the end (the GENIE
loop's grader re-checked 400/269/3/5/2 and zero new drift events) — side-
effect damage is a grading criterion.
- [ ] Mutation log current, with revert status per entry.
- [ ] Final grade includes the estate-unchanged check.

## 6. Ledger discipline
The ledger (matrix/audit/acceptance file) is the loop's single source of
truth. States: TODO · FAIL(ref) · FIXED-PENDING-GRADE · WONTFIX(reason) ·
PASS. **PASS may be written only by the independent grader.** The maker's
strongest claim is FIXED-PENDING-GRADE. A row without a numeric Target and an
oracle source is not a goal condition yet.
- [ ] No PASS in the ledger that lacks a grader citation.
- [ ] Known tooling artifacts (harness quirks) are pre-listed so they aren't
      filed as new bugs mid-loop.

## 7. Honest failure handling
A failed assertion is a FAIL with evidence, never silently retried into a
PASS. Diagnose root cause only after capturing the evidence. Tradeoffs left
deliberately incomplete are written down (documented tradeoffs, not silent
ones). Stop rules are part of the method: per-item circuit breaker (default
3 failed grades → escalate with transcripts) and a total loop budget
(default 4) — tripping them cleanly is a successful outcome of the process.
