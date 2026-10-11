---
name: blackboard
description: "Parallel work coordinator. Decomposes a task into independent streams, spawns one subagent per stream in dependency-ordered waves, records each result as a durable YAML board signal on disk, merges worktree branches, and synthesizes results in a caller-defined shape. Use whenever a task has 2+ independent work streams (parallel issue builds, multi-artifact renders, research fan-out, validator + red-team pairs), when a multi-phase workflow needs context preserved across handoffs or session restarts, or when a parent coordinator needs fan-out/fan-in. Also use when the user says 'in parallel', 'fan out', 'spawn agents for each', or '--resume' a board."
metadata:
  version: "2.2"
---

# Blackboard — Parallel Coordination

Coordinate subagents on a shared task. **Files are truth**: every result is written as YAML to a board directory on disk, so the run survives context compaction, session kills, and agent crashes, and can be resumed. Agent messages are never the source of state.

## Fast path (the 80% case)

1. Decompose the task into streams (schema below). If only one stream and no handoff complexity, stop — do the work directly.
2. Create `.pipeline/blackboard-{slug}/` with `context.yaml`.
3. **For every write stream, write its acceptance tests yourself first and commit them red** (hostile rows: gap, duplicate, reorder, excluded-kind row, real row shapes). Give the agent the test paths and forbid edits to them; a round whose diff touches them fails. Evidence (2026-10-11, lakebase-agentic-search): when agents wrote both code and tests, 4 of 4 streams shipped tests that could not fail.
4. Topologically sort streams into waves. Touch the wave's start marker, then spawn every agent in the wave in a single message.
5. As each agent returns, verify it (Step 4), then write its result YAML to `board/{agent}-complete.yaml`. Inject verified deliverables into the next wave's prompts.
6. Merge worktree branches (write streams only), run tests, write `artifacts/SYNTHESIS.{md|yaml}`.
7. Report to caller. Archive the board.

Details for each step follow. Read `references/` files only when the pointer says to.

## When not to use

- Single linear task with no handoffs — the coordination overhead costs more than it saves.
- Streams that all touch the same files — they will conflict at merge; do them sequentially.
- Already at max nesting depth (default 2, hard ceiling 3).

## Prerequisites

- The `Agent` tool with `isolation: "worktree"` support (for write streams).
- Optional: agent-teams tools (`TeamCreate`, `SendMessage`, `TeamDelete`). If absent, skip the team steps — everything else works without them.
- Add `.pipeline/` to `.gitignore` if it isn't already.

## Step 1: Decompose

You are the coordinator and you are an LLM — reason about the task directly rather than pattern-matching phrases. Produce this YAML and save it into `context.yaml`:

```yaml
streams:
  - name: "issue-2-api-endpoints"         # short slug; the coordinator's label for this stream (board filename, merge msg) — NOT the agent's assigned name, which the Agent tool returns
    description: "Implement REST endpoints for X per issue #2. TDD."
    critical: true                          # if this fails, is the whole task useless?
    depends_on: []                          # stream names that must finish first
    agent_type: "general-purpose"           # general-purpose | Explore | Plan | custom
    writes_files: true                      # true → worktree isolation + merge
    timeout_min: 30                         # per-stream; research 10, builds 30+
    scope: ["src/api/**", "tests/api/**"]   # files this stream may touch
```

Rules of thumb:
- `Explore` for read-only research (it has no Write tool, so it can never produce files); `Plan` for design alternatives; `general-purpose` for anything that edits files. There is no `Bash` agent type.
- Set `scope` so streams are disjoint: every path belongs to at most one stream. Overlap causes merge conflicts in worktrees and silent overwrites in a shared tree.
- If two streams would each take under ~5 tool calls, they aren't worth parallelizing — fold them into one.

**Parallelize when**: 2+ streams with no mutual dependency, each needing meaningful work (multiple files, or 5+ tool calls). Otherwise do the task inline and say why.

**Cycle check**: topologically sort `depends_on`. If a cycle exists, stop and report it (`A → B → A`) — don't guess a linearization.

## Step 2: Board setup

```
MODE      = resume | nested | standalone   (from args: --resume {dir}, --nested {parent_dir} {depth})
DEPTH     = parent_depth + 1 (nested) | 1
BOARD_DIR = standalone: .pipeline/blackboard-{slug}/
            nested:     {parent_board}/board/blackboard-{epoch}/
mkdir -p {BOARD_DIR}/board {BOARD_DIR}/artifacts
```

Refuse if `DEPTH > max_nesting_depth` (default 2) or `DEPTH > 3` regardless of config. Deep nesting multiplies overhead and makes failures hard to trace; flatten instead.

`context.yaml`:

```yaml
_meta: {board_dir, coordinator: blackboard, parent_board, run_id, nesting_depth, mode, max_nesting_depth: 2}
task_description: "..."
target_branch: "{current branch}"        # where worktree branches merge
phase: decompose                          # decompose → spawn → collect → merge → synthesize → complete
streams: [...]
waves: [[...], [...]]                     # names, in execution order
agents: []                                # {name, wave, spawned_at, returned_at, status}
synthesis_format: markdown-report         # preset name, or:
synthesis_schema: null                    # caller-defined (see references/synthesis.md)
failures: []
```

For `--resume`, read `context.yaml` and `board/*-complete.yaml`, compute `missing = streams − completed`, and continue from Step 3 spawning only the missing streams. Existing signals count toward completion. Nothing else is needed because all state is already on disk.

## Step 3: Spawn in waves

Group streams by dependency level. Before each wave, `touch {BOARD_DIR}/board/wave-{n}.start`; Step 4's scope check lists changed files against this marker. Spawn all agents in a wave **in one message** so they run concurrently. Do not spawn wave N+1 until wave N has returned — this replaces polling and cross-agent messaging entirely; agents never wait on each other.

Every agent prompt must be self-contained. Subagents do not see this SKILL.md, CLAUDE.md context you have loaded, or the other agents' work. Use `references/agent-prompt.md` as the template; the essentials:

- What to build, the acceptance criteria, and the `scope` boundary.
- Deliverables from upstream streams (paths + one-line summaries), pasted in from their board signals.
- Repo conventions and code-quality rules the agent must follow (see `references/code-quality.md` — paste, don't reference).
- The exact result YAML to return as its **final message**. The coordinator writes it to the board; agents don't write board files themselves (Explore agents can't, and others forget).

Spawn with:

```
Agent(
  subagent_type: stream.agent_type,
  isolation: "worktree" if stream.writes_files else omitted,
  description: stream.name,
  prompt: <rendered template>
)
```

`isolation: "worktree"` bases the worktree on `main`, not on `target_branch`. When the work lives on another branch, either create the worktrees by hand (`git worktree add --detach .claude/worktrees/{name} {target_branch}`; symlink `node_modules`) and give each prompt its absolute path, or run the wave in the shared tree, where disjoint `scope` is the only thing keeping agents off each other's files.

Record `{name, wave, spawned_at}` in `context.yaml.agents` and set `phase: spawn`.

## Step 4: Collect and verify results

When an agent returns, parse the result YAML from its final message (shape: the `## Result` block in `references/agent-prompt.md`). The report is a **lead**, not evidence: agents report "tests green", "reverted", "captured", "fixed" and "mutation red" when none of it happened. Accept a stream only after all four checks below pass, run by you, in the stream's worktree or the shared tree:

1. **Scope.** List the changed files yourself: `find {repo} -newer {BOARD_DIR}/board/wave-{n}.start -type f -not -path '*/.git/*' -not -path '*/node_modules/*'` in a shared tree, `git diff --stat {target_branch}...{branch_name}` in a worktree. Compare against the stream's `scope` and its reported `changed_files`. Read the diff of every touched file, including files the report left out. In a shared tree the wave's changed files must partition across the wave's scopes; a file inside no stream's scope, or inside another stream's scope, fails the round for the stream that touched it.
2. **Evidence.** Re-run every command in the result's `evidence` list and compare the output with the claim. A claim that doesn't reproduce fails.
3. **Coordinator mutation.** For EVERY acceptance criterion (not one), break the shipped code for it on committed state, run the test the agent names for it, and watch it go red; restore with `git checkout -- {file}` (clean tree only). A mutation that survives fails the stream. Read-only streams: re-open the cited source for one finding instead.
4. **Falsifiable tests.** Each test calls the shipped code. A test that re-implements the logic inline, or asserts a value it computed itself, is *vacuous*: reject it whatever colour it shows.

A failed check sends the stream back: resume the same agent (`SendMessage`) with the failing command and its output. This counts as the stream's one retry; a second failure escalates to the user. On pass, write the signal verbatim to `{BOARD_DIR}/board/{name}-complete.yaml` with `verified: {scope, evidence, mutation, tests}` recording what you ran.

If the final message has no parsable YAML, write a signal with `status: failed` and `errors: ["no result YAML"]`, and record the agent's last output in `failures`.

**Failure rules** (apply after each wave, not just at the end):
- A `critical` stream failed or timed out → stop. Write what you have to the board, report to the user which stream failed and why, and offer `--resume` after they fix it. Don't spawn later waves that depend on it.
- Non-critical failures → log to `failures`, continue. Mention them in synthesis.
- One retry per agent, for a transient failure (tool error, timeout with clear progress: re-spawn with the same prompt plus the last error) or a failed verification (resume the agent, above). A second failure escalates.

## Step 5: Merge and synthesize

**Merge** (skip if no stream wrote files). For each completed write stream, in wave order:

```
git merge {branch_name} --no-ff -m "blackboard: merge {stream.name}"
```

On conflict: `git merge --abort`, log the conflicting files to `failures`, and continue with remaining branches. Never auto-resolve — the user or parent coordinator decides. After merging, run the project's test suite (look for `package.json` scripts, `pytest`, `Makefile`, etc.) and record results. Delete merged branches with `git branch -d`.

**Synthesize**. If `synthesis_schema` is set, produce exactly those fields from the board signals. Otherwise use the named preset (default `markdown-report`). Presets and schema format: `references/synthesis.md`. Write to `{BOARD_DIR}/artifacts/SYNTHESIS.{md|yaml}`.

## Step 6: Report and archive

```
BLACKBOARD COMPLETE
Task:      {description}
Streams:   {N} ({completed} complete, {failed} failed)
Merge:     clean | {N} conflicts in {files}
Tests:     {passed}/{total}
Synthesis: {path}
```

If agent-teams tools are present, send `shutdown_request` to each agent and `TeamDelete`. Then:
- standalone → `mv {BOARD_DIR} .pipeline/completed/blackboard-{slug}-{epoch}/`
- nested → leave in place; the parent reads `artifacts/SYNTHESIS.*`

Set `phase: complete`.

## Anti-patterns

- Agents polling for each other's files or messaging each other for state. Waves make this unnecessary.
- Spawning agents one per message. They run sequentially and you lose the parallelism.
- Writing anything in the agent prompt as "see SKILL.md" or "follow repo conventions" — the agent has neither.
- Estimating minutes saved. You can't; decide on stream count and independence instead.
- Two streams with overlapping `scope`.
- Retrying more than once, or retrying a failure that isn't transient.
- Nesting past depth 2 to avoid thinking about decomposition.

## References

- `references/agent-prompt.md` — the spawn prompt template. Read before Step 3.
- `references/parallel-dev-lessons.md` — 17 rules from a 25-ticket parallel build (design batching, contract-file pins, standing test authority, never trust a report). Read before Step 1 on multi-ticket runs.
- `references/synthesis.md` — presets and caller-defined schema. Read at Step 5.
- `references/code-quality.md` — rules to paste into prompts for write streams.
- `references/integrations.md` — how design-ops, content-factory, and demo-factory invoke blackboard. Read only when called by one of them.
