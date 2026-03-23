---
name: blackboard
description: "Recursive parallel work coordinator — spawns agents with board-based coordination, worktree isolation, and caller-defined synthesis. USE WHEN 2+ independent work streams, parallel issue build, multi-phase handoffs, structured synthesis needed."
version: "2.0"
changelog: |
  v2.0: Grill-me redesign — LLM decomposition replaces regex parser, stream criticality, per-stream agent type selection, worktree isolation via Claude Code native support, caller-defined synthesis schema, --resume mode, execution history for cost/benefit, dual-channel coordination (YAML state + optional message nudge), .pipeline/ board convention, default max depth 2.
  v1.0: Initial skill with regex stream parsing, hardcoded synthesis formats, scratch/ board directory, hard depth-3 limit.
---

# Blackboard v2.0 — Recursive Parallel Coordination

Coordinate multiple agents on a shared task using file-based board signals. Supports recursive invocation (coordinators calling blackboard, blackboard calling blackboard).

**Core architecture:** Files are truth. Board signals are durable YAML on disk — they survive session kills, context compaction, and agent crashes. Messages are optional nudges for latency, never the source of truth.

## Trigger

Invoke when:
- Task has 2+ truly independent work streams (parallel work)
- Sequential pipeline with complex handoffs requiring context preservation
- Multi-phase workflow where board signals prevent context loss
- `/design build` detects parallel-eligible issues in the dependency graph
- A coordinator (content-factory, demo-factory, enablement-kit) needs fan-out/fan-in

**The board serves two purposes:**
1. **Parallelization** — coordinate independent work streams
2. **External memory** — preserve context across complex handoffs and session restarts

Do NOT invoke when:
- Simple linear task with no handoff complexity
- Trivial work (cost/benefit analysis will reject it)
- Already at max nesting depth

## Entry Point

Parse args to detect mode:

- `--resume {board_dir}` → resume from existing board state
- `--nested` → extract parent board dir, increment depth
- Otherwise → standalone mode, depth = 1

## Phase 0: Board Setup

### 0a. Detect Mode

```
if args contain --resume {path}:
  MODE = "resume"
  BOARD_DIR = {path}
  Read context.yaml → restore state
  Skip to Phase 4 (monitor) with partial agent re-spawn

elif args contain --nested:
  PARENT_BOARD = extract from args
  PARENT_DEPTH = extract from args (default 0)
  NESTING_DEPTH = PARENT_DEPTH + 1
  MODE = "nested"

else:
  PARENT_BOARD = null
  NESTING_DEPTH = 1
  MODE = "standalone"
```

### 0b. Depth Check

Default max depth: 2. Configurable up to hard ceiling of 3.

```
max_depth = context.yaml.max_nesting_depth or 2
if NESTING_DEPTH > max_depth:
  ERROR: "Max nesting depth ({max_depth}) exceeded. Flatten your task decomposition."
  exit
if NESTING_DEPTH > 3:
  ERROR: "Hard ceiling of 3 exceeded regardless of config."
  exit
```

### 0c. Create Board Directory

All boards use `.pipeline/` convention for unified archival:

```
TASK_SLUG = slugify(TASK_DESCRIPTION, max=40)
TIMESTAMP = unix_epoch

if MODE == "nested":
  BOARD_DIR = "{PARENT_BOARD}/board/blackboard-{TIMESTAMP}"
else:
  BOARD_DIR = ".pipeline/blackboard-{TASK_SLUG}/"

mkdir -p "{BOARD_DIR}/board"
mkdir -p "{BOARD_DIR}/artifacts"
```

### 0d. Write context.yaml

```yaml
_meta:
  board_dir: "{BOARD_DIR}"
  coordinator: "blackboard"
  parent_coordinator: "{parent if nested, else null}"
  run_id: "{ISO timestamp}"
  nesting_depth: N
  mode: "{standalone|nested|resume}"
  max_nesting_depth: 2  # configurable up to 3

task_description: "{user's task}"
phase_completed: null  # null → analysis → spawn → monitor → synthesis → cleanup → complete
streams: null
agents_spawned: []

# Caller-defined synthesis
synthesis_format: "markdown-report"  # named preset (backward compat)
synthesis_schema: null               # or inline schema from caller

# Cost/benefit tracking
estimated_parallel_time_min: null
estimated_sequential_time_min: null
parallelization_decision: null
parallelization_reason: ""

# Monitoring
agent_timeout_min: 10
max_retries_per_agent: 1

# Failures
failures: []
```

### 0e. Write failures.yaml

```yaml
failures: []
warnings: []
```

## Phase 1: Analyze Complexity

### 1a. LLM Decomposition (replaces regex parsing)

The coordinator IS an LLM. Let it reason about task decomposition natively instead of pattern-matching English phrases.

**Prompt the LLM to output a structured YAML block:**

```
Analyze this task and decompose it into parallel work streams.
Output ONLY a YAML block with this exact schema:

streams:
  - name: "{short descriptive name}"
    description: "{what this stream must accomplish}"
    critical: true|false    # must complete for synthesis to proceed?
    depends_on: []          # list of stream names this depends on
    agent_type: "general-purpose|Explore|Bash|Plan"  # right-sized agent

Rules:
- Streams with no mutual dependencies can run in parallel
- Mark streams "critical: true" if their failure makes the whole task useless
- Use "Explore" for read-only research, "Bash" for command execution only,
  "Plan" for architecture/design, "general-purpose" for anything needing file writes
- Default to "general-purpose" if unsure
- If task is sequential ("X then Y"), set depends_on accordingly
- If task is a single unit with no parallelism, output one stream
```

**Output:** structured `streams` list with names, dependencies, criticality, and agent types.

**Single stream assessment:** If `len(streams) == 1`, assess whether blackboard adds value:
- **Use blackboard if:** Multi-phase with complex handoffs, structured output needed for parent coordinator, or context preservation critical
- **Skip blackboard if:** Simple single-phase task — just do it directly

Update `context.yaml` with the streams list.

### 1b. Cost/Benefit Analysis

Estimate parallel vs sequential execution using historical data when available.

**Step 1: Check execution history**

```
STATS_FILE = ~/.claude/blackboard-stats.yaml
if STATS_FILE exists:
  Load historical medians per stream keyword category
else:
  Use cold-start defaults
```

**Cold-start defaults:**

| Category | Default (min) |
|----------|--------------|
| research | 15 |
| test | 10 |
| frontend / backend | 20 |
| default | 10 |

**Step 2: Calculate**

```
stream_times = {s.name: historical_median_or_default(s) for s in streams}

# Parallel: max(independent streams) + overhead
parallelization_overhead = 2 + (len(streams) * 1)  # 2 min base + 1 min per agent
parallel_time = max(stream_times.values()) + parallelization_overhead

# Sequential: sum(stream_times)
sequential_time = sum(stream_times.values())

# Decision: parallelize if parallel < 0.7 * sequential
threshold = 0.7 * sequential_time
should_parallelize = parallel_time < threshold
```

**Decision:**
- `should_parallelize == False` → ERROR: "Parallelization overhead ({parallel_time} min) exceeds benefit (threshold: {threshold} min). Do this sequentially."
- `should_parallelize == True` → proceed

Update `context.yaml` with estimates and decision.

Log to user:
```
✓ Complexity Analysis Complete

Streams detected: {N}
Parallel estimate: {N} min ({max_time} + {overhead} overhead)
Sequential estimate: {N} min
Decision: PARALLELIZE (saves {sequential - parallel} min)
```

### 1c. Dependency Cycle Check

Before spawning agents, validate the dependency graph:

```
Build directed graph from streams[].depends_on
Run topological sort
If cycle detected:
  ERROR: "Dependency cycle: {A} → {B} → {A}. Flatten or linearize."
  BLOCK
```

## Phase 2: Create Team

```
TEAM_NAME = "{TASK_SLUG}-team"

TeamCreate(
  team_name: TEAM_NAME,
  description: task_description
)
```

Export board context for nested invocations:
```
export _BLACKBOARD_PARENT_BOARD = BOARD_DIR
export _BLACKBOARD_DEPTH = NESTING_DEPTH
```

## Phase 3: Spawn Agents

### 3a. Agent Naming

```
For each stream, generate: {slugify(stream.name)}-{index}
Truncate to 20 chars.
```

### 3b. Board Signal Schema

**CRITICAL: Board signals MUST be file-based YAML.** This is the architectural core — files survive session kills, context compaction, and agent crashes. Messages don't.

Each agent writes this schema when complete:

```yaml
task_id: N
agent_name: "{name}"
stream_description: "{original stream desc}"
status: complete
timestamp: "{ISO8601}"
branch_name: "worktree-{agent-name}"  # from worktree isolation
commit_sha: "{sha}"                    # last commit in worktree
deliverables:
  - file_path: "{path}"
    description: "{what}"
  - description: "{what}"  # if not file-based
depends_on_completed: [list of task IDs]
ready_for: [list of agent names that were waiting]
errors: []
duration_seconds: N  # actual execution time for stats tracking
```

### 3c. Worktree Isolation

Claude Code natively supports subagent worktree isolation. Each agent gets its own worktree at `.claude/worktrees/{agent-name}/` with an isolated branch. Auto-cleanup on completion.

**Blackboard does NOT manage worktree lifecycle.** Claude Code handles creation, branch naming, and cleanup. Blackboard only reads the `branch_name` and `commit_sha` from board signals for the merge step.

To enable: use a custom agent definition with `isolation: worktree` in frontmatter, or spawn agents that create their own worktrees via the `--worktree` pattern.

### 3d. Spawn Each Agent

```
for each stream in dependency-sorted order:
  agent = agent_name(stream, index)
  taskId = index

  # Build dependency wait instruction
  if stream.depends_on is not empty:
    dep_files = [board path for each dependency]
    wait_instruction = """
    WAIT: Before starting, check that these board files exist: {dep_files}.
    Poll every 15s. Max wait: 10 minutes.
    If you receive a message saying "dependency ready", check immediately.
    """
  else:
    wait_instruction = ""

  Task(
    subagent_type: stream.agent_type,  # right-sized per LLM recommendation
    name: agent,
    team_name: TEAM_NAME,
    prompt: """
    You are working on: {stream.name}
    Description: {stream.description}

    {wait_instruction}

    CRITICAL INSTRUCTIONS:
    1. Work in your worktree (isolation: worktree is set)
    2. Complete your task with commits in your worktree branch
    3. When complete, write {BOARD_DIR}/board/{agent}-complete.yaml with:
       - task_id: {taskId}
       - agent_name: "{agent}"
       - stream_description: "{stream.description}"
       - status: complete
       - timestamp: (ISO8601)
       - branch_name: (your worktree branch name)
       - commit_sha: (your last commit SHA)
       - deliverables: [list what you produced]
       - depends_on_completed: [{dep task IDs}]
       - ready_for: [{agents waiting on you}]
       - errors: [any non-fatal errors]
       - duration_seconds: (how long you took)
    4. Use ABSOLUTE paths for all file references
    5. Board signal file is the source of truth — write it even if you also send messages
    """
  )

  # Optional: notify dependent agents when this stream has known dependents
  # (latency optimization — not required for correctness)

  agents_spawned.append({name, task_id, stream, agent_type, spawned_at})
```

### 3e. Dual-Channel Notification (Optional)

After an agent writes its board signal, it MAY also send a message to waiting agents:

```
SendMessage(
  type: "message",
  recipient: "{waiting-agent-name}",
  content: "Dependency ready — check board signal at {path}",
  summary: "Dependency {stream.name} ready"
)
```

**Rules:**
- Message is a latency optimization, NOT required for correctness
- Waiting agent MUST still validate by reading the board YAML
- If session dies and restarts, polling recovers — no message history needed
- Messages consume context; files don't. Keep messages short.

Update `context.yaml`:
```yaml
agents_spawned: [list]
phase_completed: "spawn"
```

## Phase 4: Monitor Board

### 4a. Polling Loop

```
TIMEOUT_MIN = context.yaml.agent_timeout_min or 10
START_TIME = now()
EXPECTED_SIGNALS = len(agents)

# Adaptive polling interval
poll_interval = 5  # start at 5s

while true:
  elapsed = now() - START_TIME

  # Escalate polling interval
  if elapsed > 120:  poll_interval = 10
  if elapsed > 300:  poll_interval = 30

  # Check timeout
  if elapsed > TIMEOUT_MIN * 60:
    handle_timeout()
    break

  # Count valid signals
  signal_count = count valid YAML files in {BOARD_DIR}/board/*-complete.yaml

  if signal_count == EXPECTED_SIGNALS:
    log "✓ All {EXPECTED_SIGNALS} agents completed"
    break

  log "Waiting: {signal_count}/{EXPECTED_SIGNALS} complete..."
  sleep(poll_interval)
```

### 4b. Timeout Handling (Criticality-Aware)

```
completed = [agents with valid board signals]
missing = [agents without board signals]

# Check criticality
critical_missing = [a for a in missing if a.stream.critical]
non_critical_missing = [a for a in missing if not a.stream.critical]

if critical_missing:
  # Critical stream failed — cannot proceed
  log failures to failures.yaml
  BLOCK and escalate to user:
    "Critical stream(s) did not complete: {names}. Cannot synthesize."

elif len(completed) / len(agents) >= 0.7:
  # >= 70% complete and no critical missing → proceed with partial synthesis
  log warnings for missing non-critical agents
  proceed to Phase 5

else:
  # < 70% complete — escalate
  BLOCK and escalate to user
```

### 4c. Validate Board Signals

After collection (or timeout), validate each signal:

```
for each agent:
  signal_file = {BOARD_DIR}/board/{agent}-complete.yaml

  if not exists → log critical failure, continue
  if not valid YAML → log critical failure, continue

  required = [task_id, status, deliverables, duration_seconds]
  if missing fields → log high failure, continue

  # Record actual duration for stats
  actual_durations.append({
    category: categorize(agent.stream),
    duration: signal.duration_seconds
  })
```

Update `failures.yaml` with any validation errors.

### 4d. Update Execution History

After monitoring completes, append actual durations to stats file:

```
STATS_FILE = ~/.claude/blackboard-stats.yaml

for each actual_duration:
  Append to rolling window (last 20 runs per category)
  Recalculate median
```

This makes future cost/benefit analyses increasingly accurate.

## Phase 5: Synthesize

### 5a. Merge Worktree Branches

Before synthesis, merge all agent worktree branches into the main feature branch:

```
for each completed agent (in dependency order):
  branch = signal.branch_name
  sha = signal.commit_sha

  git merge {branch} --no-ff -m "Merge {agent.stream.name} from blackboard"

  if merge conflict:
    log conflict details to failures.yaml
    flag in synthesis output
    # Design-ops or user resolves conflicts

# Run integration tests on merged result
test_result = run project test suite
if tests fail:
  log which tests failed and which agent's changes likely caused it
```

Skip this step if agents didn't use worktrees (e.g., research-only streams).

### 5b. Determine Synthesis Format

Check `context.yaml` for caller-defined schema or named preset:

```
if context.yaml.synthesis_schema is not null:
  Use caller-defined schema — map board signal data to requested fields
elif context.yaml.synthesis_format is a named preset:
  Use preset template
else:
  Default to markdown-report
```

**Named presets** (shorthand for common schemas):

| Preset | Output | Use Case |
|--------|--------|----------|
| `markdown-report` (default) | Human-readable markdown | Standalone invocations |
| `demo-deployment` | YAML with URLs + resource IDs | Demo-factory build |
| `artifact-metadata` | YAML with artifact paths + types | Content-factory render |
| `research-synthesis` | Markdown with sources + findings | Research agents |
| `build-result` | YAML with test results + commits | Design-ops parallel build |

**Caller-defined schema** (extensible without editing blackboard):

```yaml
synthesis_schema:
  required_fields:
    - artifact_paths
    - quality_scores
    - deployment_urls
    - merge_status
  output_format: yaml       # yaml | markdown
  include_timeline: false
  include_board_signals: true
```

Blackboard maps board signal data to the requested fields and returns exactly what the caller needs.

### 5c. Write Synthesis

Write to `{BOARD_DIR}/artifacts/SYNTHESIS.{md|yaml}` depending on format.

**Markdown report format (default):**

```markdown
# Blackboard Synthesis: {Task Description}

**Board:** `{BOARD_DIR}`
**Started:** {start timestamp}
**Completed:** {end timestamp}
**Duration:** {minutes}
**Streams:** {N} ({N} completed, {N} missing)

---

## Executive Summary

{1-2 sentence summary}

**Deliverables:**
- {count} files produced
- {count} tasks completed
- {count} errors/warnings
- Merge status: {clean | conflicts}

---

## Deliverables

| Agent | Stream | Deliverable | Path |
|-------|--------|-------------|------|
| {agent} | {stream} | {desc} | `{path}` |

---

## Coordination Timeline

| Time | Agent | Event |
|------|-------|-------|
| {HH:MM} | {agent-1} | Spawned |
| {HH:MM} | {agent-1} | Completed ({N}s) |

**Parallel time:** {minutes}
**Sequential estimate:** {minutes}
**Time saved:** {delta} minutes

---

## Merge Results

{merge status per branch, conflict details if any}

## Integration Test Results

{pass/fail, which tests, which agent's changes caused failures}

## Errors & Warnings

{from failures.yaml}
```

Update `context.yaml`:
```yaml
phase_completed: "synthesis"
synthesis_file: "{path}"
```

## Phase 6: Cleanup

### 6a. Shutdown Agents

```
for each agent in agents_spawned:
  SendMessage(type: "shutdown_request", recipient: agent.name, content: "Work complete.")

Wait max 30s for confirmations.
Log any agents that didn't confirm.
```

### 6b. Delete Team

```
TeamDelete()
```

### 6c. Worktree Cleanup

**Claude Code handles worktree cleanup automatically.** When agents finish:
- No changes → worktree and branch removed automatically
- Changes committed → branches persist until merge in Phase 5

After successful merge in Phase 5, clean up merged branches:
```
for each merged branch:
  git branch -d {branch_name}
```

### 6d. Archive Board

```
if MODE == "standalone":
  # Archive to .pipeline/completed/
  mv {BOARD_DIR} .pipeline/completed/blackboard-{TASK_SLUG}-{TIMESTAMP}/
  log "Board archived at: .pipeline/completed/..."
elif MODE == "nested":
  # Leave in place for parent coordinator
  log "Nested board available to parent at: {BOARD_DIR}"
```

Update `context.yaml`:
```yaml
phase_completed: "complete"
cleanup_verified: true
```

## Phase 7: Report to Caller

```
✓ BLACKBOARD COMPLETE
=====================
Task: {task description}
Board: {BOARD_DIR}
Mode: {standalone|nested|resume}
Depth: {nesting level}

Streams: {N} ({N} completed, {N} missing)
Duration: {minutes} (saved {delta} min vs sequential)

Deliverables:
  - {summary}

Merge: {clean | N conflicts}
Integration tests: {pass | fail}

Synthesis: {path to SYNTHESIS.md or .yaml}

{If nested:}
→ Parent coordinator can read: {BOARD_DIR}/artifacts/SYNTHESIS.{format}
```

## Resume Mode

When invoked with `--resume {board_dir}`:

1. Read `context.yaml` — get `phase_completed`, `agents_spawned`, `streams`
2. Scan `board/*-complete.yaml` — identify which agents already finished
3. Diff: `agents_spawned - completed_signals = missing_agents`
4. Re-create team (Phase 2)
5. Re-spawn ONLY missing agents (Phase 3) with same stream definitions
6. Continue monitoring (Phase 4) — existing board signals count toward completion
7. Synthesize, cleanup, report as normal

**Why this works:** All state is on disk. Board signals from the previous run are still in `board/`. The new agents write their signals to the same directory. Synthesis reads all signals regardless of which run produced them.

## Integration with Design-Ops v3.1

### /design discover — Parallel Interface Exploration

When `/design discover` identifies a key module boundary, it invokes blackboard to explore design alternatives in parallel:

```
blackboard(
  task: "Explore interface designs for {module}",
  streams: [
    {name: "minimize-interface", agent_type: "Plan", critical: false},
    {name: "maximize-flexibility", agent_type: "Plan", critical: false},
    {name: "optimize-common-caller", agent_type: "Plan", critical: false},
    {name: "ports-and-adapters", agent_type: "Plan", critical: false}
  ],
  synthesis_schema: {
    required_fields: [interface_signature, usage_example, hidden_complexity, tradeoffs],
    output_format: markdown
  }
)
```

Design-ops reads the synthesis and presents alternatives to the user.

### /design prp — Parallel Validator + Red-Team (LARGE tier)

```
blackboard(
  task: "Validate and red-team PRP: {prp_name}",
  streams: [
    {name: "invariant-validation", agent_type: "general-purpose", critical: true},
    {name: "red-team-review", agent_type: "general-purpose", critical: true}
  ],
  synthesis_schema: {
    required_fields: [blocking_violations, advisory_violations, adversarial_findings, confidence_adjustment],
    output_format: yaml
  }
)
```

Design-ops reads synthesis to decide go/no-go on the PRP.

### /design build — Parallel Independent Issues (biggest win)

After `/prp-to-issues` produces the dependency graph, design-ops identifies groups of independent issues:

```
# Issues #2 and #3 both depend on #1 but not each other
# After #1 completes in main branch:

blackboard(
  task: "Parallel TDD build: issues #2 and #3",
  streams: [
    {name: "issue-2-api-endpoints", agent_type: "general-purpose", critical: true},
    {name: "issue-3-auth-middleware", agent_type: "general-purpose", critical: true}
  ],
  synthesis_schema: {
    required_fields: [tests_passed, integration_status, files_modified, commit_sha, branch_name, merge_status],
    output_format: yaml
  }
)

# Each agent:
# 1. Works in its own worktree (isolation: worktree)
# 2. Runs full TDD cycle (red-green-refactor) for its issue
# 3. Commits to worktree branch
# 4. Writes board signal with branch_name + commit_sha
#
# Blackboard synthesis:
# 1. Merges both branches into feature branch
# 2. Runs integration tests on merged result
# 3. Reports merge status + test results
#
# Design-ops reads synthesis, continues to next issue group
```

## Integration with Other Coordinators

### Content-Factory

```
blackboard(
  task: "Render artifacts in parallel",
  streams: [
    {name: "render-deck", agent_type: "general-purpose", critical: true},
    {name: "render-cheatsheet", agent_type: "general-purpose", critical: false},
    {name: "render-one-pager", agent_type: "general-purpose", critical: false}
  ],
  synthesis_format: "artifact-metadata"
)
```

### Demo-Factory

```
blackboard(
  task: "Build demo components",
  streams: [
    {name: "scaffold-app", agent_type: "general-purpose", critical: true},
    {name: "deploy-resources", agent_type: "Bash", critical: true},
    {name: "generate-frontend", agent_type: "general-purpose", critical: true}
  ],
  synthesis_format: "demo-deployment"
)
```

## Error Handling

### Agent Timeout
```
If agent hasn't signaled after timeout:
1. Check TaskOutput for agent's last output
2. If stuck (repeating same error):
   - Send unblock message with hint
   - Extend timeout by 5 minutes
   - Max 1 retry per agent
3. If crashed:
   - Log to failures.yaml
   - Apply criticality rules (Phase 4b)
```

### Malformed Board Signal
```
If board YAML is malformed:
1. Try best-effort parse (extract what's readable)
2. Send message: "Board signal malformed. Please fix and rewrite."
3. Wait 2 minutes
4. If still malformed → apply criticality rules
```

### Merge Conflicts
```
If worktree branch merge conflicts:
1. Log conflict details (files, markers) to failures.yaml
2. Include in synthesis output
3. Design-ops or user resolves manually
4. Blackboard does NOT attempt auto-resolution
```

## Code Quality Mandates

When agents write code during blackboard streams, they MUST follow these rules:

**Decomposition rule**: If a function has 3+ independent responsibilities — decompose it. Each sub-function gets its own name, docstring, and failure logging. The dispatcher reads like a table of contents.

**Silent drop rule**: When a precondition fails, log at WARNING level. Never silently skip with `if row: ... else: pass`.

**Consistent filter rule**: If the same lookup appears in multiple code paths, extract it into a shared helper so all paths use the same WHERE clause.

## Anti-Patterns

- Don't use for trivial work (cost/benefit analysis prevents this)
- Don't nest beyond configured max depth
- Don't skip cleanup verification (resource leaks)
- Don't auto-retry indefinitely (max 1 retry per agent)
- Don't parallelize dependent work (dependency detection prevents this)
- Don't manage worktree lifecycle manually (Claude Code handles it)
- Don't rely on messages for state (files are truth)
- Don't use regex to parse task descriptions (LLM decomposes natively)
