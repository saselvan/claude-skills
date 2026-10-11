# Parallel agentic dev: lessons from a 25-ticket build

Evidence base: lakebase-agent-memory Phase 6 (2026-10-08). There, one coordinator ran up to 5 agents at
once: builders, an independent mutation prover, read-only question sweeps, and live research spikes.
Each rule below fixed a real failure. Read this before Step 3. Paste the relevant rules into the
prompts, because agents do not see this file.

## Before any build: remove the pauses
1. **Answer all design questions in one batch.** Run read-only sweep agents, one per ticket group. Give
   each one the files that hold earlier owner answers, and say "skip decided items". Otherwise most of
   the output repeats decisions, and false clashes slip in. Every question needs a source path:line,
   at most 2 options, the production consequence of each, and a recommendation.
2. **Judge every decision at the largest size the system supports**, not at today's size. Every
   per-request path must stay bounded as history grows. Two of seven answers flipped under that lens.
3. **Write rules that remove whole classes of questions.** Examples: every writing privileged
   function is listed in an allow-list; every new table gets the same security settings; cross-tenant
   reads go through a small content-free table.

## Prevent clashes with merged tests
4. **Keep exact-set pins in ONE contract file.** Grant sets, allow-list keys, role lists, table lists
   and migration counts all belong there. Tests compare against the file, and a guard test fails on
   drift in either direction. A new ticket then adds one line and never edits a merged test. Without
   this, every expand-only ticket clashed and stopped.
5. **Give builders standing authority.** When a decided ticket changes a fact that a merged test relied
   on, the builder updates the test and keeps its assertions. It shows one mutation red per changed
   file, and it reports the change. It stops only when the ticket's own design must change.
6. **Run a pre-flight probe in the first 10 minutes.** Apply the planned schema change as a throwaway
   change on clean HEAD, and run the suites that pin grants, roles and security. Find clashes before
   writing tests.

## Run many tickets at once
7. **Use one git worktree per ticket**, each from the integration branch, and write the run-order
   rules for shared files ("A then B", "X and Y never at once").
8. **Merge build stages where you can, but keep the prover independent.** One agent writes the red
   tests (committed red first) and then builds. After green, the critic and a FRESH mutation prover
   run in parallel. An author's own mutations miss what the author did not think of, which is
   measured. Every fix round gets a fresh prover.
9. **Treat live resources as a queue.** Respect the platform cap (for example, 3 test branches).
   Keep one parameterised verify script. Never copy a script with sed: renames broke result paths twice.
10. **Use an allow-list settings file** (`.claude/settings.local.json` `permissions.allow`) for the
    live CLI command families. Prompts then stop blocking unattended runs. Scope limits (throwaway
    resources only) stay in the prompts.

## Never trust a report
11. **A report is a lead, not evidence.** Open the agent's raw results file. One research agent
    claimed LIVE answers while its own results file said the feature was never enabled. Every LIVE
    claim needs an evidence file holding the command and its verbatim output. Anything else is
    UNTESTED, and an honest UNTESTED is fine.
12. **Handle an agent that ends with no report.** Check git log and git status in its worktree, then
    message it for the result. Put the result contract at the top AND the bottom of every prompt.
13. **Run one coordinator mutation per accepted stream.** Break one criterion on committed state, run
    the named test, and watch it go red.
14. **Name the auth profile in every live prompt**, and preflight `whoami -p <profile>`. A logged-out
    default profile stalled research for an hour.
15. **Pin the toolchain.** Every `uv run` uses `--frozen`, and the coordinator checks the lock file
    for the wrong registry before accepting. Set `PYTHONDONTWRITEBYTECODE=1` for every mutation run,
    because stale bytecode gives false reds and false greens.

## Safety
16. **Put destructive platform facts in every prompt that touches them.** For example, `bundle destroy`
    deletes a declared database project with all its data. Spikes use throwaway names only, and they
    end with teardown proof.
17. **No permission laundering.** A subagent cannot grant approvals, and an approval in one context
    does not carry over to the next.

## Added 2026-10-10 (lakebase-agentic-search, Plan B 01)
18. **"Would fail" is not a red run.** Two builders in one wave wrote mutation result lines as "Would fail if…"
    and one ran zero live tests (all skipped, profile not named). Require a `proof_file` (raw pytest output) per
    mutation and per test run, and gate every report with a script before reading it: reject "would" in a result
    line, missing proof files, skipped tests in a live stream, and any required symbol a grep cannot find.
    Paste lessons 6, 8 and 14 into every write-stream prompt.
