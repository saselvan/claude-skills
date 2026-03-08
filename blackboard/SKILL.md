---
name: blackboard
description: Recursive parallel work coordinator - spawns agents with board-based coordination, supports nesting
---

# Blackboard - Recursive Parallel Coordination

Coordinate multiple agents on a shared task using board signals. Supports recursive invocation (coordinators calling blackboard, blackboard calling blackboard).

## Trigger

Invoke when:
- Task has 2+ truly independent work streams (parallel work)
- Sequential pipeline with complex handoffs requiring context preservation
- Multi-phase workflow where board signals prevent context loss
- Need structured synthesis of agent outputs

**The board serves two purposes:**
1. **Parallelization** — coordinate independent work streams
2. **External memory** — preserve context across complex handoffs

Do NOT invoke when:
- Simple linear task with no handoff complexity
- Trivial work (< 5 min total, overhead exceeds benefit)
- Already at nesting depth 3 (max recursion limit)

## Entry Point

Parse args to detect mode:

- If args start with `--nested` → extract parent board dir, increment depth
- Otherwise → standalone mode, depth = 1

## Phase 0: Board Setup

### 0a. Detect Nesting

Check if we're being invoked from within a coordinator:

```bash
# Check for parent board context
if [ -n "$_BLACKBOARD_PARENT_BOARD" ]; then
  PARENT_BOARD="$_BLACKBOARD_PARENT_BOARD"
  PARENT_DEPTH="${_BLACKBOARD_DEPTH:-0}"
  NESTING_DEPTH=$((PARENT_DEPTH + 1))
  MODE="nested"
else
  PARENT_BOARD=""
  NESTING_DEPTH=1
  MODE="standalone"
fi

# Max depth check
if [ $NESTING_DEPTH -gt 3 ]; then
  echo "ERROR: Max nesting depth (3) exceeded. Flatten your task decomposition."
  exit 1
fi
```

### 0b. Create Board Directory

Location depends on mode:

```bash
TASK_SLUG="$(echo "$TASK_DESCRIPTION" | sed 's/[^a-z0-9-]/-/g' | cut -c1-40)"
TIMESTAMP="$(date +%s)"

if [ "$MODE" = "nested" ]; then
  # Nested mode — board under parent
  BOARD_DIR="${PARENT_BOARD}/board/blackboard-${TIMESTAMP}"
else
  # Standalone mode
  BOARD_DIR="/Users/samuel.selvan/scratch/${TASK_SLUG}/board"
fi

mkdir -p "${BOARD_DIR}/board"
mkdir -p "${BOARD_DIR}/artifacts"
```

### 0c. Write context.yaml

```yaml
_meta:
  board_dir: "{BOARD_DIR}"
  coordinator: "blackboard"
  parent_coordinator: "{parent if nested, else null}"
  run_id: "{ISO timestamp}"
  nesting_depth: N
  mode: "{standalone|nested}"

task_description: "{user's task}"
phase_completed: null  # null → analysis → spawn → monitor → synthesis → cleanup → complete
streams_detected: null
agents_spawned: []
synthesis_format: "{format requested, default: markdown-report}"

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

Write to `${BOARD_DIR}/context.yaml`.

### 0d. Write failures.yaml

```yaml
failures: []
warnings: []
```

Write to `${BOARD_DIR}/failures.yaml`.

## Phase 1: Analyze Complexity

### 1a. Parse Work Streams

Analyze task description for parallelizable work:

**Pattern matching:**

| Pattern | Streams | Example |
|---------|---------|---------|
| "build X with Y and Z" | [X, Y, Z] | "build API with auth and tests" → ["API", "auth", "tests"] |
| "X and Y and Z" | [X, Y, Z] | "frontend and backend and tests" → ["frontend", "backend", "tests"] |
| "research A, B, C" | [A, B, C] | "research Snowflake, AWS, GCP" → ["Snowflake", "AWS", "GCP"] |
| "X then Y" | [X, Y] (sequential) | "research then write" → ["research", "write"] with dep |
| Single unit | [X] | "build a dashboard" → ["dashboard"] |

**Sequential detection:**
- "then" keyword → second stream depends on first
- "after" keyword → dependency
- "once X, do Y" → dependency

**Implementation:**

```python
import re

# Extract streams
if " with " in task and " and " in task:
    # "build X with Y and Z" pattern
    parts = task.split(" with ", 1)
    main = parts[0].replace("build ", "").strip()
    rest = parts[1].split(" and ")
    streams = [main] + [r.strip() for r in rest]
elif " and " in task:
    # "X and Y and Z" pattern
    streams = [s.strip() for s in task.split(" and ")]
elif ", " in task and ("research" in task or "analyze" in task):
    # "research A, B, C" pattern
    items = re.split(r",\s*(?:and\s+)?", task)
    streams = [i.strip() for i in items if i.strip()]
else:
    # Single stream
    streams = [task.strip()]

# Detect dependencies
dependencies = {}
if " then " in task or " after " in task:
    # Sequential - later streams depend on earlier
    for i, stream in enumerate(streams[1:], start=1):
        dependencies[stream] = [streams[i-1]]
```

Output: `streams_detected`, `dependencies` dict

**Single stream assessment:**
If `len(streams) == 1`, assess whether blackboard adds value:
- **Use blackboard if:** Multi-phase task with complex handoffs, structured output needed for parent coordinator, or context preservation critical
- **Skip blackboard if:** Simple single-phase task with no coordination complexity

Update `context.yaml`:
```yaml
streams_detected: [list]
dependencies: {dict}
```

### 1b. Cost/Benefit Analysis

Estimate parallel vs sequential execution:

```python
# Estimate per-stream time (heuristic)
def estimate_stream_time(stream_desc):
    keywords = stream_desc.lower()
    if "research" in keywords:
        return 15  # 15 min per research task
    elif "test" in keywords:
        return 10  # 10 min for test suite
    elif "frontend" in keywords or "backend" in keywords:
        return 20  # 20 min for app component
    else:
        return 10  # default

stream_times = {s: estimate_stream_time(s) for s in streams}

# Parallel: max(stream_times) + overhead
parallelization_overhead = 2 + (len(streams) * 1)  # 2 min base + 1 min per agent
parallel_time = max(stream_times.values()) + parallelization_overhead

# Sequential: sum(stream_times)
sequential_time = sum(stream_times.values())

# Decision: parallelize if parallel < 0.7 * sequential
threshold = 0.7 * sequential_time
should_parallelize = parallel_time < threshold
```

**Decision:**
- If `should_parallelize == False` → ERROR: "Parallelization overhead ({parallel_time} min) exceeds benefit (threshold: {threshold} min). Do this sequentially instead."
- If `should_parallelize == True` → proceed

Update `context.yaml`:
```yaml
estimated_parallel_time_min: N
estimated_sequential_time_min: N
parallelization_decision: "{parallelize|sequential}"
parallelization_reason: "{explanation}"
```

Log decision to user:
```
✓ Complexity Analysis Complete

Streams detected: {N}
Parallel estimate: {N} min ({max_time} + {overhead} overhead)
Sequential estimate: {N} min
Decision: PARALLELIZE (saves {sequential - parallel} min)
```

## Phase 2: Create Team

### 2a. Team Creation

```bash
TEAM_NAME="${TASK_SLUG}-team"

# Export board context for nested invocations
export _BLACKBOARD_PARENT_BOARD="${BOARD_DIR}"
export _BLACKBOARD_DEPTH="${NESTING_DEPTH}"
```

Invoke TeamCreate:

```javascript
TeamCreate(
  team_name: "${TEAM_NAME}",
  description: "${TASK_DESCRIPTION}",
  agent_type: "blackboard-coordinator"
)
```

## Phase 3: Spawn Agents

### 3a. Agent Naming

For each stream, generate agent name:

```python
def agent_name(stream_desc, index):
    # Sanitize stream desc to valid name
    name = stream_desc.lower()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = name[:20]  # truncate
    return f"{name}-{index}"

agents = [agent_name(s, i) for i, s in enumerate(streams, start=1)]
```

### 3b. Board Signal Schema

**CRITICAL: Board signals MUST be file-based YAML.**

Board signals are YAML files written to `${BOARD_DIR}/board/` when agents complete work. They serve as:
- **Durable state** — survives agent lifecycle
- **Structured handoff** — schema enforces completeness
- **Audit trail** — timestamped record of all work

**NOT acceptable:**
- Sending messages instead of writing files
- Partial signals (missing required fields)
- Non-YAML formats

Instruct each agent to write this schema when complete:

```yaml
task_id: N
agent_name: "{name}"
stream_description: "{original stream desc}"
status: complete
timestamp: "{ISO8601}"
deliverables:
  - file_path: "{path}"
    description: "{what}"
  - description: "{what}" (if not file-based)
depends_on_completed: [list of task IDs]
ready_for: [list of agent names that were waiting]
errors: []  # if any non-fatal errors occurred
```

### 3c. Spawn Each Agent

```javascript
for (let i = 0; i < streams.length; i++) {
  const stream = streams[i];
  const agent = agents[i];
  const taskId = i + 1;
  const deps = dependencies[stream] || [];

  // Build dependency wait instruction
  let waitInstruction = "";
  if (deps.length > 0) {
    const depFiles = deps.map(d => {
      const depIndex = streams.indexOf(d) + 1;
      return `${BOARD_DIR}/board/${agents[depIndex-1]}-complete.yaml`;
    });
    waitInstruction = `WAIT: Before starting, check that these board files exist: ${depFiles.join(", ")}. Poll every 30s. Max wait: 10 minutes.`;
  }

  Task(
    subagent_type: "general-purpose",
    name: agent,
    team_name: TEAM_NAME,
    prompt: `
You are working on: ${stream}

${waitInstruction}

Your task:
${stream}

CRITICAL: When complete, write ${BOARD_DIR}/board/${agent}-complete.yaml with:
- task_id: ${taskId}
- agent_name: "${agent}"
- stream_description: "${stream}"
- status: complete
- timestamp: (ISO8601)
- deliverables: [list what you produced - file paths or descriptions]
- depends_on_completed: [${deps.map(d => streams.indexOf(d) + 1).join(", ")}]
- ready_for: [list agent names waiting on you, or empty]
- errors: [list any non-fatal errors]

Board signal must be written to the FULL PATH above, not a relative path.
Use absolute paths for all file references in deliverables.
    `.trim()
  );

  agents_spawned.push({
    name: agent,
    task_id: taskId,
    stream: stream,
    dependencies: deps,
    spawned_at: new Date().toISOString()
  });
}
```

Update `context.yaml`:
```yaml
agents_spawned: [list from above]
phase_completed: "spawn"
```

Log to user:
```
✓ Agents Spawned

{N} agents working in parallel:
  [1] {agent-1} → {stream-1}
  [2] {agent-2} → {stream-2} (waits for [1])
  ...

Board: ${BOARD_DIR}/board/
```

## Phase 4: Monitor Board

### 4a. Polling Loop

Monitor for completion signals:

```bash
TIMEOUT_MIN=10
START_TIME=$(date +%s)
EXPECTED_SIGNALS=${#agents[@]}

while true; do
  # Check timeout
  ELAPSED=$(( $(date +%s) - START_TIME ))
  if [ $ELAPSED -gt $((TIMEOUT_MIN * 60)) ]; then
    echo "ERROR: Timeout after ${TIMEOUT_MIN} minutes"
    # Check which agents haven't signaled
    for agent in "${agents[@]}"; do
      if [ ! -f "${BOARD_DIR}/board/${agent}-complete.yaml" ]; then
        echo "  Missing signal from: ${agent}"
        # Attempt to unblock
        echo "  Checking agent status..."
        # Use TaskOutput to check if agent is still running
      fi
    done
    break
  fi

  # Count existing signals
  SIGNAL_COUNT=$(ls -1 "${BOARD_DIR}/board/"*-complete.yaml 2>/dev/null | wc -l)

  if [ "$SIGNAL_COUNT" -eq "$EXPECTED_SIGNALS" ]; then
    echo "✓ All ${EXPECTED_SIGNALS} agents completed"
    break
  fi

  # Log progress
  echo "  Waiting: ${SIGNAL_COUNT}/${EXPECTED_SIGNALS} complete..."
  sleep 5
done
```

### 4a-1. Polling Best Practices

**Interval strategy:**
- **Start with 5-second polls** for fast tasks (< 2 min expected)
- **Escalate to 10-second polls** after 2 minutes
- **Cap at 30-second polls** for long-running tasks (> 5 min expected)

**Timeout strategy:**
- Base timeout: 10 minutes (default)
- Complex tasks: 20-30 minutes (explicitly set in context.yaml)
- Never infinite — always have a hard timeout

**Graceful degradation:**
- If ≥ 70% of agents completed → proceed with partial synthesis
- If < 70% completed → BLOCK and escalate to user
- Log missing agents explicitly in failures.yaml

**What to check:**
- File existence: `[ -f "${BOARD_DIR}/board/${agent}-complete.yaml" ]`
- YAML validity: Try parsing with `yq` or Python before counting as "complete"
- Timestamp freshness: Warn if signal timestamp is > 15 min old (stale signal)

**What NOT to do:**
- Don't poll faster than 5 seconds (wastes CPU, creates log spam)
- Don't assume message receipt means board signal written (they're different channels)
- Don't wait indefinitely for missing signals (timeout must fire)

**Error handling:**

If timeout occurs:
1. Read `board/*.yaml` files that DO exist
2. Check `failures.yaml` for any logged errors
3. Decide:
   - If ≥ 70% of agents completed → proceed with partial synthesis, flag missing
   - If < 70% completed → BLOCK, escalate to user

### 4b. Validate Board Signals

After all signals collected (or timeout), validate each:

```python
for agent in agents:
    signal_file = f"{BOARD_DIR}/board/{agent}-complete.yaml"

    if not os.path.exists(signal_file):
        failures.append({
            "agent": agent,
            "error": "No signal file produced",
            "severity": "critical"
        })
        continue

    # Parse YAML
    try:
        with open(signal_file) as f:
            signal = yaml.safe_load(f)
    except yaml.YAMLError as e:
        failures.append({
            "agent": agent,
            "error": f"Malformed YAML: {e}",
            "severity": "critical"
        })
        continue

    # Validate schema
    required = ["task_id", "status", "deliverables"]
    missing = [r for r in required if r not in signal]
    if missing:
        failures.append({
            "agent": agent,
            "error": f"Missing fields: {missing}",
            "severity": "high"
        })
```

Update `failures.yaml` with any validation errors.

Update `context.yaml`:
```yaml
phase_completed: "monitor"
signals_received: N
signals_expected: N
validation_errors: N
```

## Phase 5: Synthesize

### 5a. Determine Synthesis Format

Check `context.yaml` for `synthesis_format` or use default:

| Format | Output Structure | Use Case |
|--------|------------------|----------|
| `markdown-report` (default) | Human-readable markdown | Standalone blackboard invocations |
| `demo-deployment` | Deployment URLs + resource IDs | Demo-factory Phase 4 build |
| `artifact-metadata` | Artifact paths + types | Content-factory Phase 4 render |
| `research-synthesis` | Sources + findings | Research agents |

### 5b. Markdown Report Format (Default)

Read all `board/*-complete.yaml` files, create synthesis:

**File:** `${BOARD_DIR}/artifacts/SYNTHESIS.md`

```markdown
# Blackboard Synthesis: {Task Description}

**Board:** `{BOARD_DIR}`
**Started:** {start timestamp}
**Completed:** {end timestamp}
**Duration:** {minutes}
**Streams:** {N}
**Agents:** {N}

---

## Executive Summary

{1-2 sentence summary of what was accomplished}

**Deliverables:**
- {count} files produced
- {count} tasks completed
- {count} errors/warnings

---

## Board Signals (Full Detail)

### Agent 1: {name} ({stream})
```yaml
{full YAML content from board file}
```

### Agent 2: {name} ({stream})
```yaml
{full YAML content}
```

...

---

## Deliverables by Category

### Files Produced
| Agent | File | Description |
|-------|------|-------------|
| {agent} | `{path}` | {desc} |

### Non-File Deliverables
| Agent | Deliverable | Description |
|-------|-------------|-------------|
| {agent} | {name} | {desc} |

---

## Coordination Timeline

| Time | Agent | Event |
|------|-------|-------|
| {HH:MM} | {agent-1} | Spawned |
| {HH:MM} | {agent-2} | Spawned (waiting on agent-1) |
| {HH:MM} | {agent-1} | Completed |
| {HH:MM} | {agent-2} | Unblocked, started |
| {HH:MM} | {agent-2} | Completed |

**Total parallel time:** {minutes}
**Estimated sequential time:** {minutes} (from cost/benefit analysis)
**Time saved:** {sequential - parallel} minutes

---

## Errors & Warnings

{If any failures from failures.yaml, list here}
{If validation errors, list here}
{If partial completion (timeout), note which agents didn't finish}

---

## Integration Readiness

✓ All agents completed successfully
✓ All deliverables validated
✓ Board signals conform to schema
→ Ready for next phase / integration
```

### 5c. Alternative Formats

**demo-deployment format:**
```yaml
deployment:
  workspace_url: "{from agent signals}"
  app_url: "{from agent signals}"
  resource_ids: []
  database: "{from agent signals}"
status: "{complete|partial}"
```

**artifact-metadata format:**
```yaml
artifacts:
  - type: "{deck|cheatsheet|one-pager}"
    path: "{absolute path}"
    status: "{complete|draft}"
    metadata: {}
```

**research-synthesis format:**
```markdown
# Research Synthesis

## Sources
{N} sources across {N} agents

## Key Findings
{bullet points from each agent's deliverables}

## Open Questions
{from agent errors or incomplete deliverables}
```

### 5d. Write Synthesis

Write to `${BOARD_DIR}/artifacts/SYNTHESIS.{md|yaml}` depending on format.

Update `context.yaml`:
```yaml
phase_completed: "synthesis"
synthesis_file: "{path}"
```

## Phase 6: Cleanup

### 6a. Shutdown Agents

```javascript
for (const agent of agents_spawned) {
  SendMessage(
    type: "shutdown_request",
    recipient: agent.name,
    content: "Work complete. Thank you."
  );
}

// Wait for confirmations (max 30s)
const shutdownDeadline = Date.now() + 30000;
const shutdownConfirmed = [];

while (Date.now() < shutdownDeadline && shutdownConfirmed.length < agents_spawned.length) {
  // Check for shutdown responses
  // (Implementation depends on message queue access)
  await sleep(1000);
}

if (shutdownConfirmed.length < agents_spawned.length) {
  const stuck = agents_spawned.filter(a => !shutdownConfirmed.includes(a.name));
  console.warn(`Warning: ${stuck.length} agents did not confirm shutdown: ${stuck.map(a => a.name).join(", ")}`);
}
```

### 6b. Delete Team

```javascript
TeamDelete();
```

### 6c. Verify Cleanup

```bash
# Check team directory is gone
if [ -d "${TEAM_DIR}" ]; then
  echo "WARNING: Team directory still exists at ${TEAM_DIR}"
  echo "Manual cleanup may be required"
fi

# Archive board if standalone, leave if nested
if [ "$MODE" = "standalone" ]; then
  echo "Board archived at: ${BOARD_DIR}"
  echo "Synthesis available at: ${BOARD_DIR}/artifacts/SYNTHESIS.md"
else
  echo "Nested board available to parent at: ${BOARD_DIR}"
fi
```

Update `context.yaml`:
```yaml
phase_completed: "complete"
cleanup_verified: true
```

## Phase 7: Report to Caller

### 7a. Present Summary

```
✓ BLACKBOARD COMPLETE
=====================
Task: {task description}
Board: {BOARD_DIR}
Mode: {standalone|nested}
Depth: {nesting level}

Streams: {N}
Agents: {N}
Duration: {minutes}

Deliverables:
  - {summary of deliverables}

Synthesis: {path to SYNTHESIS.md or .yaml}

{If errors:}
⚠ Warnings: {N}
  - {list}

{If nested:}
→ Parent coordinator can read: {BOARD_DIR}/artifacts/SYNTHESIS.{format}
```

### 7b. Return to Caller

If invoked by another coordinator:
- Coordinator reads `${BOARD_DIR}/artifacts/SYNTHESIS.{format}`
- Coordinator writes adapter board entry per their protocol

If standalone:
- User reads synthesis file directly
- Board archived for reference

## Recursive Invocation Support

When a coordinator (like demo-factory Phase 4) or an artifact (like deck-render) needs to invoke blackboard:

### From Coordinator

```javascript
// In demo-factory Phase 4c (scaffold + resources + frontend)
Task(
  subagent_type: "blackboard",
  prompt: `
--nested

Parallelize: scaffold application, deploy resources, generate frontend

Synthesis format: demo-deployment

Parent board: ${BOARD_DIR}
  `,
  team_name: "demo-factory"
);

// Blackboard will:
// 1. Detect --nested flag
// 2. Read parent board from args
// 3. Create nested board at ${BOARD_DIR}/board/blackboard-{timestamp}/
// 4. Spawn 3 agents (scaffold, resources, frontend)
// 5. Write synthesis to nested board as demo-deployment.yaml
// 6. Return control to demo-factory
// 7. Demo-factory reads demo-deployment.yaml for URLs/IDs
```

### From Artifact

```javascript
// In deck-render (if 30+ slides)
if (slide_count > 30) {
  // Too complex for sequential rendering
  Task(
    subagent_type: "blackboard",
    prompt: `
--nested

Parallelize: render slides 1-10, render slides 11-20, render slides 21-30

Synthesis format: artifact-metadata

Parent board: .deck-render/mayo-tre/
    `
  );

  // Blackboard will:
  // 1. Spawn 3 slide-batch renderers
  // 2. Each writes PNG files for their range
  // 3. Synthesis contains paths to all PNGs
  // 4. deck-render stitches PNGs into final PPTX
}
```

## Error Handling & Retry

### Agent Timeout

```
If agent hasn't signaled after 10 minutes:
1. Check TaskOutput for agent's last output
2. If agent is stuck (repeating same error):
   - Send unblock message with hint
   - Extend timeout by 5 minutes
   - Max 1 retry per agent
3. If agent crashed:
   - Log to failures.yaml
   - Continue with partial results if ≥70% complete
   - Otherwise BLOCK and escalate
```

### Malformed Board Signal

```
If board YAML is malformed:
1. Try best-effort parse (extract what's readable)
2. Send message to agent: "Your board signal is malformed. Please fix and rewrite."
3. Wait 2 minutes
4. If still malformed → BLOCK, escalate with error details
```

### Dependency Cycle

```
Before spawning agents:
1. Build dependency graph
2. Check for cycles using topological sort
3. If cycle detected:
   - ERROR: "Dependency cycle detected: {A} → {B} → {A}"
   - Suggest linearization: "Run in sequence: {A}, then {B}"
   - BLOCK
```

## Anti-Patterns

❌ **Don't use for trivial work** (cost/benefit analysis prevents this)
❌ **Don't nest beyond depth 3** (hard limit)
❌ **Don't skip cleanup verification** (resource leaks)
❌ **Don't auto-retry indefinitely** (max 1 retry per agent)
❌ **Don't parallelize dependent work** (dependency detection prevents this)

✅ **Do check cost/benefit before parallelizing**
✅ **Do support nested invocation**
✅ **Do verify cleanup**
✅ **Do handle partial completion gracefully**
✅ **Do respect dependency ordering**

## Integration with Existing Coordinators

### Demo-Factory

```yaml
# Phase 4c: Build (can invoke blackboard)
Task(
  subagent_type: "blackboard",
  prompt: "
    Parallelize: scaffold app, deploy resources, generate frontend
    Synthesis format: demo-deployment
  "
)
# Blackboard returns demo-deployment.yaml with URLs
# Demo-factory reads and continues to Phase 4.5 verification
```

### Content-Factory

```yaml
# Phase 4: Render (can invoke blackboard)
Task(
  subagent_type: "blackboard",
  prompt: "
    Parallelize: render deck, render cheatsheet, render one-pager
    Synthesis format: artifact-metadata
  "
)
# Blackboard returns artifact-metadata.yaml with paths
# Content-factory reads and continues to quality gates
```

### Deck-Render (Nested in Content-Factory)

```yaml
# If deck has 30+ slides and independent sections
Task(
  subagent_type: "blackboard",
  prompt: "
    --nested
    Parallelize: render intro (slides 1-5), render body (6-25), render close (26-30)
    Synthesis format: artifact-metadata
    Parent board: .pipeline/content-factory/
  "
)
# Blackboard creates nested board at .pipeline/content-factory/board/blackboard-{ts}/
# Returns artifact-metadata.yaml with PNG paths
# Deck-render stitches into final PPTX
```
