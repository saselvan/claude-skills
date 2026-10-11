# verification-ladder — iteration 1 eval results

Tested per skill-creator's eval guidance: 2 realistic prompts × (with-skill,
no-skill control), all arms on the same model tier (opus), objective
assertions drafted before grading, scripted checks where possible.

## Benchmark

| configuration | pass rate | assertions | tokens (mean) | wall-clock (mean) |
|---|---|---|---|---|
| with_skill | **100%** | 9/9 + 7/7 | 96,281 | 439.9s |
| with_skill_organic_trigger | **100%** | 9/9 | 97,312 | 506.9s |
| without_skill (control) | **51%** | 4/9 + 4/7 | 78,850 | 427.4s |

The skill roughly doubles assertion pass rate at comparable cost.

## What the controls missed (i.e. the skill's measured value)

Both controls produced strong first-principles work — and both missed the
same governance layer:
- no independent fresh-context grader with SOLE PASS authority (control 1
  used a role matrix; control 2 enforced separation by artifact ownership but
  never named a sole authority or required the grader to recompute oracles)
- no ledger state machine (TODO · FAIL · FIXED-PENDING-GRADE · WONTFIX ·
  PASS) with maker-cannot-write-PASS
- no per-item circuit breaker or loop budget (control 2 had a global
  max_iterations only; control 1 had none — the loop could thrash forever)
- no worktree-per-loop isolation
- no model-pinned agent routing (grader tier > maker tier > explorer tier)
- no goal string pointing at the acceptance file

What the controls got right unprompted: the adversarial replay of the stated
prior failure, and measurable conditions. Those are the parts a capable model
does anyway; the loop governance is what the skill actually adds.

## What the evals changed in the skill

The eval-0 control shipped an EXECUTABLE grader (a black-box harness with
byte-exact goldens) and proved it discriminating by simulating the original
bug and watching it go red — better than the skill's prose description of a
grader. Folded back in as `scripts/oracle_harness.py`, plus the standing
instruction: *prove the harness goes RED on the known bug before trusting it;
a harness that has never failed is not evidence.*

The harness was then held to its own rule — run against a correct CSV
exporter (PASS, exit 0) and against the shipped null-owner-dropping bug
(FAIL, exit 1, caught on all three independent checks: byte mismatch, 2≠4 row
conservation, 0-of-2 null-owner rows preserved).

## Trigger test

The eval-0 run launched as a control invoked the skill organically from its
description alone (task never named it) and scored 9/9 — evidence the
description triggers on matching work. It also improved on the reference E2
design (metric-id-presence grep instead of count-only, so a drop-plus-
duplicate can't fool the benchmark).

## Process notes (disclosed, not buried)

Two early baseline runs were contaminated by a harness design error of mine:
the control agents shared a sandbox with the with-skill arms, so one read the
assertion rubric (`eval_metadata.json`) and the other consumed the with-skill
arm's fixtures. Both were discarded (kept on disk with contamination notes)
and rerun with isolated sandboxes and neutral output staging. The benchmark
above uses only clean runs.

Workspace (uncommitted, local): `~/.claude/skills/verification-ladder-workspace/`
— per-run outputs, grading.json, timing.json, benchmark.json, review.html.
