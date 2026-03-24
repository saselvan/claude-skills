---
name: demo-factory
description: "End-to-end demo creation from concept to deployed application with board coordination. USE WHEN: user wants a full demo pipeline from brainstorm through build, or when the demo skill's phases need cross-phase context passing. Wraps the demo skill's 3 phases with board protocols and adds Phase 4 (build) with Databricks infrastructure adapters."
allowed-tools: Read, Write, Bash, Task, Glob, Grep, Skill, WebSearch, WebFetch
---

# Demo Factory

You are a demo production coordinator. Your job is to take a demo concept through brainstorming, research, spec generation, and (optionally) infrastructure build — passing accumulated context between phases via the board. Each phase produces a concrete artifact and a board entry, so subsequent phases benefit from prior findings.

**You wrap the existing `demo` skill's phases.** For Phases 1-3, invoke the demo skill and capture its output for board entries. Phase 4 (build) is new — it invokes Databricks infrastructure skills via adapter protocols.

## Trigger

Invoke when:
- User runs `/demo [concept]` with intent for full pipeline
- User requests "build a demo end-to-end"
- User wants to chain brainstorm → research → spec → build with context continuity

Do NOT invoke for:
- Single-phase demo work (e.g., just `/demo brainstorm`) — route to demo skill directly
- Demos that already have a DEMO_SPEC.md and just need building — route to databricks-apps/lakebase directly
- Demo ideation without intent to build — route to demo skill

## Source Material

Required:
- Demo concept or industry brief (user provides)

Optional:
- Existing gap analysis from a prior `/demo brainstorm`
- Existing research synthesis from a prior `/demo research`
- Outcome map (Healthcare Outcome Map PDF or industry equivalent)
- Existing demo inventory (lakebase-demo-scorecard.md, genie-demo-scorecard.md)

## Blackboard Integration (Context Preservation + Parallelization)

**Primary Objective:** Use blackboard's board signals as external memory to preserve context across complex handoffs and prevent context loss during long-running pipelines.

**Secondary Objective:** Parallelize independent work streams when beneficial.

### When to Use Blackboard at the Factory Level

Invoke blackboard skill at the factory coordinator level when:
- Multi-phase pipeline has complex handoffs requiring context preservation (brainstorm → research → spec → build)
- Pipeline spans multiple sessions (mandatory stops between phases mean context will be lost)
- Accumulated findings from early phases must inform later phases (research insights → spec generation)
- Session boundaries create risk of losing critical decisions or rationale

**Pattern:** Blackboard creates a durable board that survives session boundaries and context compaction. Each phase writes board signals that subsequent phases read.

**Example invocation at factory level:**
```
# At Phase 1 completion, before mandatory stop
Task(
  subagent_type: "blackboard",
  prompt: "Coordinate demo-factory pipeline phases with board signals.

  Phases: brainstorm (complete) → research (next) → spec → build

  Synthesis format: demo-pipeline-state

  Parent board: .pipeline/demo-factory/

  Primary goal: Preserve brainstorm findings for research phase (gap analysis, outcome map position, plugin stack decisions)"
)
```

### When to Use Blackboard Within a Phase

Invoke blackboard skill within a specific phase when:
- Phase has 2+ independent work streams that can run in parallel
- Work streams have non-trivial complexity (each >5 min estimated)
- Parallelization saves meaningful time (≥30% reduction vs sequential)
- Board signals are needed to coordinate between work streams

**Example: Phase 4b (Build Database) with Complex Setup**

If the database setup involves:
- Creating Lakebase instance
- Executing DDL (tables, indexes, triggers)
- Seeding synthetic data
- Setting up PostGIS extension

And these can be partially parallelized:

```python
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize: create database instance, prepare DDL scripts, generate seed data

  Synthesis format: demo-deployment

  Parent board: .pipeline/demo-factory/

  Note: Instance creation and DDL prep can run in parallel, but DDL execution depends on instance availability. Seed generation can happen anytime."
)
```

**Example: Phase 4 Build Steps (scaffold + resources + frontend)**

If Phase 4c-4e can be partially parallelized:

```python
# After 4b (database provisioned), parallelize app build steps
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize: scaffold application structure, deploy Databricks resources (notebooks/jobs), generate frontend components

  Synthesis format: demo-deployment

  Parent board: .pipeline/demo-factory/board/

  Note: Scaffold must complete before resource deployment (needs app.yaml), but frontend generation can happen in parallel with scaffold."
)
```

### Board Signal Schema for Factory Coordination

When blackboard is used at the factory level, it should produce synthesis files that demo-factory can read:

**demo-pipeline-state.yaml** (for cross-phase coordination):
```yaml
pipeline: "demo-factory"
current_phase: "research"
phase_dependencies:
  research:
    needs: ["brainstorm"]
    reads_from: [".pipeline/demo-factory/board/brainstorm-output.yaml"]
    writes_to: ".pipeline/demo-factory/board/research-output.yaml"
  spec:
    needs: ["brainstorm", "research"]
    reads_from: [".pipeline/demo-factory/board/brainstorm-output.yaml", ".pipeline/demo-factory/board/research-output.yaml"]
    writes_to: ".pipeline/demo-factory/board/spec-output.yaml"
  narrative:
    needs: ["spec"]
    reads_from: [".pipeline/demo-factory/board/spec-output.yaml", ".pipeline/demo-factory/board/brainstorm-output.yaml", ".pipeline/demo-factory/board/research-output.yaml"]
    writes_to: ".pipeline/demo-factory/board/narrative-output.yaml"

accumulated_context:
  gap_analysis_key_findings: []
  outcome_map_position: {}
  plugin_stack_decisions: []
  research_coverage: {}

ready_for_next_phase: true/false
blocking_issues: []
```

**demo-deployment.yaml** (for Phase 4 build coordination):
```yaml
deployment:
  workspace_url: ""
  app_url: ""
  resource_ids: []
  database: ""
  lakebase_instance_id: ""
  tables_created: []

status: "complete|partial|failed"
parallelized_steps:
  - step: "scaffold"
    status: "complete"
    agent: "scaffold-agent-1"
  - step: "resources"
    status: "complete"
    agent: "resources-agent-2"
  - step: "frontend"
    status: "complete"
    agent: "frontend-agent-3"
```

### When NOT to Use Blackboard

Do NOT invoke blackboard when:
- Phase is simple linear work (<5 min total)
- No parallelization opportunity exists (strict sequential dependencies)
- Session is fresh and context is clean (early in a phase)
- Board signals would add overhead without benefit

**Anti-pattern:** Using blackboard for every tiny step. Reserve it for:
1. Cross-session coordination (mandatory stops)
2. Non-trivial parallelization (saves ≥30% time)
3. Complex handoffs where context preservation is critical

### Integration with Existing Board

Demo-factory already has a board at `.pipeline/demo-factory/`. When blackboard is invoked:
- Nested mode: `--nested` flag tells blackboard to create sub-board under demo-factory's board
- Board location: `.pipeline/demo-factory/board/blackboard-{timestamp}/`
- Synthesis files: Written to demo-factory's board for consumption by subsequent phases

**Critical:** Blackboard's board signals are FILE-BASED YAML. They must be durable, not ephemeral messages. This ensures context survives session boundaries and context compaction.

### Recursive Nesting (Automatic Multi-Level Parallelization)

**Rule:** If you discover a parallelization opportunity while working on a task (even if you were already spawned by blackboard), invoke blackboard again with `--nested`.

**Pattern:** Blackboard → blackboard → blackboard (up to depth 3)

**Example Flow:**

```
Level 0: demo-factory (coordinator)
  ↓
Level 1: blackboard coordinates Phase 4 build steps
  ├─ Agent 1: Scaffold app
  ├─ Agent 2: Deploy resources ← discovers 3 independent notebooks
  │   ↓
  │   Level 2: blackboard coordinates resource deployment
  │     ├─ Agent 2a: Deploy notebook A
  │     ├─ Agent 2b: Deploy notebook B
  │     └─ Agent 2c: Deploy notebook C
  └─ Agent 3: Generate frontend
```

**When to nest:**
- You're inside an agent (spawned by blackboard or factory)
- You discover 2+ independent sub-tasks within your assigned work
- Each sub-task is non-trivial (>2 min estimated)
- Parallelizing them saves ≥30% time

**How to nest:**

```python
# Inside Agent 2 (deploy resources), discovers 5 notebooks to deploy
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize: deploy notebook-1, deploy notebook-2, deploy notebook-3, deploy notebook-4, deploy notebook-5

  Synthesis format: demo-deployment

  Parent board: {current_agent_board_path}

  Note: All notebooks are independent, can deploy in parallel."
)
```

**Max depth:** 3 levels (hard limit in blackboard skill to prevent infinite recursion)

**Example depth-3 scenario:**
1. **demo-factory** invokes blackboard for Phase 4 (build)
2. **build-blackboard** spawns "deploy resources" agent
3. **deploy-resources agent** invokes blackboard for 5 notebooks
4. **notebook-blackboard** spawns agent per notebook
5. ❌ **notebook agent CANNOT** invoke blackboard again (depth limit reached)

**Detection pattern:** Always check for parallelization before executing sequential work. Ask: "Can I break this into 2+ independent streams?"

**Anti-pattern:** Don't nest for trivial splits (e.g., 2 tasks that each take 30 seconds). Overhead exceeds benefit.

## Entry Point Routing

Parse $ARGUMENTS to determine entry point:

- If $ARGUMENTS starts with "--build":
  → Skip to Phase 4 (Build)
  → Read `.pipeline/demo-factory/context.yaml` → verify `phase_completed` is "spec" or "narrative"
  → If phase_completed is null or earlier than "spec", tell user: "Spec not complete. Run `/demo [concept]` first."
  → Otherwise, proceed to Phase 4 preamble

- If $ARGUMENTS is empty or starts with anything else:
  → Treat entire $ARGUMENTS as the demo concept
  → Start from Phase 0

## Board Setup (Phase 0)

### 0a. Create board directory

```
.pipeline/demo-factory/
├── context.yaml              ← concept, industry, personas, scope
├── board/                    ← phase outputs land here
├── artifacts/                ← gap-analysis.md, research.md, DEMO_SPEC.md, .mdc
│   └── narrative/            ← acts.json, demo-script.md, YAML scaffold (Phase 3.5)
└── failures.yaml             ← error log (create empty)
```

### 0b. Write context.yaml

Extract from user's concept:

```yaml
_meta:
  board_dir: ".pipeline/demo-factory/"
  coordinator: "demo-factory"
  run_id: "{ISO timestamp}"

phase_completed: null          # null → brainstorm → research → spec → narrative → build-infra → build-app → verification → complete
spec_prp_status: null
workspace_provisioned: false
lakebase_provisioned: false
infra_tool_calls: 0
research_retry_count: 0

concept: "{user's demo concept}"
industry: "{HLS|FSI|etc.}"
scope: "{full|urgent}"
tier: null                              # determined during brainstorm
plugin_stack: []                        # determined during brainstorm
existing_demo_to_fork: null             # determined during brainstorm
```

## Pipeline Sequence

### Phase 1: Brainstorm

Invoke the `demo` skill's brainstorm phase: `/demo brainstorm [concept]`

1. The demo skill runs Socratic discovery, Glean outcome map search, plugin resolution
2. It produces `gap-analysis.md`
3. After the demo skill completes, capture output and write board entry to `board/brainstorm-output.yaml`:

```yaml
skill_name: "demo"
phase: "brainstorm"
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"

artifact_path: "{absolute path to gap-analysis.md}"
artifact_type: "gap-analysis"

# What brainstorm discovered
concept_name: ""
outcome_map_position:
  industry: ""
  pillar: ""
  use_case: ""
  coverage_status: "{gap|extends|forks}"
target_buyer: ""
production_user: ""
wow_moment: ""
plugin_stack: []
scaffold_source: "{custom|genai-app-template}"
ai_dev_kit_modules: []
scope: "{full|urgent}"
tier: N

# Open questions for research
open_questions: []

quality_score: N                        # count of HLS gates satisfiable
quality_max: 8                          # 8 HLS gates
quality_pass: true/false
quality_notes: ""

strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []
recommendations_for_downstream:
  - target_skill: "demo-research"
    recommendation: "{e.g., 'Focus research on Delta Lake CDC patterns — customer uses Debezium today'}"
    priority: "high"

# OUTPUT FORMAT CONTRACT with demo/SKILL.md:
# The demo skill writes markdown with YAML frontmatter + specific headings.
# demo-factory parses these using the heading names defined in demo/SKILL.md Phase 1 output.
# If the demo skill changes its heading names, these parsing rules MUST be updated.
#
# Heading → Field mapping:
#   "# {name} — Gap Analysis" (H1)           → concept_name
#   "## Outcome Map Position" section         → outcome_map_position (parse bullet points)
#   "## Target Audience"                      → target_buyer ("Demo buyer:" line)
#                                             → production_user ("Production user:" line)
#   "## Wow Moment"                           → wow_moment (paragraph text)
#   "## Plugin Stack" (table)                 → plugin_stack (first column values)
#   "**Scaffold source:**" line               → scaffold_source
#   "## Scope" → "**Decision:**" line         → scope
#   "## Complexity Tier" (first word/number)  → tier
#
# Frontmatter fields (always available):
#   demo_name, industry, phase, created
#
# If a heading is not found in the markdown, set the field to "" and add to coverage_gaps.
```

4. Update `context.yaml` with resolved fields (tier, plugin_stack, scope)
5. **Phase gate**: Present brainstorm summary. Do NOT auto-advance. User decides when.

### Phase 2: Research

Invoke the `demo` skill's research phase: `/demo research [concept]`

1. The demo skill runs parallel research agents + optional Gemini prompt + devil's advocate
2. It produces `{name}-research.md`
3. After completion, capture output and write board entry to `board/research-output.yaml`:

```yaml
skill_name: "demo"
phase: "research"
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"

artifact_path: "{absolute path to research.md}"
artifact_type: "research-synthesis"

# Coverage assessment
source_count: N
agent_count: N
gemini_used: true/false
devil_advocate_findings: N

coverage_per_dimension:
  personas: "{high|medium|low}"
  data_model: "{high|medium|low}"
  competitive: "{high|medium|low}"
  existing_assets: "{high|medium|low}"
  ui_ux: "{high|medium|low}"

# Key findings
central_differentiator: ""
existing_assets_found: []
data_sources_identified: []

quality_pass: true/false
quality_notes: ""

strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []
recommendations_for_downstream:
  - target_skill: "demo-spec"
    recommendation: "{e.g., 'Spec should include Kafka→Delta ingestion path — research found customer is evaluating this'}"
    priority: "high"
```

4. **V2 Decision: Post-Research Coverage Loop-Back**

```
READ board/research-output.yaml → coverage_per_dimension
READ context.yaml → research_retry_count (default 0 if absent)

critical_dimensions = {personas, data_model, competitive}
thin_dimensions = [d for d in critical_dimensions if coverage_per_dimension[d] == "low"]

IF len(thin_dimensions) > 0:
  IF research_retry_count < 2:
    SET research_retry_count = research_retry_count + 1
    WRITE research_retry_count back to context.yaml (persist before re-invoke)
    PRESENT to user:
      "Research has thin coverage on: {thin_dimensions}.
       I can re-research these specific areas. Proceed? (Y/N/skip)"

    IF user approves:
      RE-INVOKE /demo research with focused queries on thin_dimensions only
      PASS prior research-output.yaml as context
      WRITE updated board/research-output.yaml
      RE-EVALUATE
    ELSE:
      PROCEED with gaps noted
  ELSE:
    LOG: "Coverage thin on {thin_dimensions} after 2 retries"
    PROCEED with gaps noted in spec
ELSE:
  PROCEED to Phase 3
```

5. **Phase gate**: Present research summary. Do NOT auto-advance.

### Phase 3: Spec

Invoke the `demo` skill's spec phase: `/demo spec [concept]`

1. The demo skill reads gap analysis + research, produces DEMO_SPEC.md + optional .mdc
2. After completion, capture output and write board entry to `board/spec-output.yaml`:

```yaml
skill_name: "demo"
phase: "spec"
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"

artifact_path: "{absolute path to DEMO_SPEC.md}"
artifact_type: "demo-spec"

# Spec completeness
table_count: N
platform_features_count: N
build_phases: N
estimated_complexity: "{low|medium|high}"

# Plugin readiness
plugin_mappings:
  - plugin: "{/databricks-lakebase}"
    spec_section: "{lakebase.*}"
    status: "ready"
  - plugin: "{/databricks-apps}"
    spec_section: "{app.*}"
    status: "ready"

# Cursor rules
mdc_path: "{path to .mdc file, or null}"

# Quality gate
domain_gates_satisfied: N
domain_gates_total: N
domain_gates_failed: []

quality_pass: true/false
quality_notes: ""

strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []
recommendations_for_downstream:
  - target_skill: "build"
    recommendation: "{e.g., 'Deploy Lakebase first — app depends on PostGIS extension being available'}"
    priority: "high"
```

3. **Quality gate**: Invoke `prp-gate-verification` on the DEMO_SPEC.md
   - If pass → proceed (if user wants Phase 4)
   - If fail → iterate spec against PRP feedback (max 2 iterations)
   - If still fails → **BLOCK**. Do not build from a failing spec. Escalate to user.
4. Update `context.yaml`:
   ```yaml
   phase_completed: "spec"
   spec_prp_status: "{PASS|FAIL}"
   ```

5. **MANDATORY STOP.** Print:

```
Demo Factory — Phase 3 (Spec) Complete
=======================================
Board: .pipeline/demo-factory/
Concept: {concept}
Industry: {industry}
Tier: {tier}

Completed:
  ✓ Brainstorm → gap-analysis.md
  ✓ Research → {name}-research.md ({N} sources, {coverage summary})
  ✓ Spec → DEMO_SPEC.md ({N} tables, {N} platform features, {N} build phases)
  ✓ PRP Gate: {PASS|FAIL}
  {if .mdc generated: ✓ Cursor Rules → {path}}

Next: Phase 3.5 (Demo Narrative)
  Run: /demo-narrative {concept}
  This generates the structured narrative (acts.json, demo-script.md,
  YAML scaffold) from the spec. The spec's Talk Track section is
  superseded by narrative output when present.

Options:
  a) Generate narrative → run /demo-narrative {concept} (recommended)
  b) Skip narrative, build with Claude Code → /demo --build
  c) Build with Cursor → copy .mdc file, open in Cursor
  d) Stop here → spec is complete, build later
```

Do NOT proceed to Phase 3.5 or Phase 4 in this session. Phases 1-3
involve extensive reasoning (Socratic discovery, parallel research,
spec generation, PRP iteration). That context is irrelevant to
narrative generation and infrastructure provisioning, and actively
degrades quality if retained.

### Phase 3.5: Demo Narrative

**Session entry:** This phase runs in a NEW session after Phase 3 completed and stopped.

**Purpose:** Generate structured demo narrative artifacts — act sequence, presenter script, and YAML scaffold for demo-machine — from the completed spec. When narrative output exists, it supersedes the spec's thin Talk Track section.

1. Read `.pipeline/demo-factory/context.yaml` → verify `phase_completed == "spec"`
2. Invoke the `demo-narrative` skill with board context:

```
Skill(skill: "demo-narrative", args: "{concept}")
```

The demo-narrative skill consumes:
- `DEMO_SPEC.md` — wow moments, persona-to-view mappings, UI route table
- `{name}-research.md` — domain context, competitive landscape, audience insights
- `board/brainstorm-output.yaml` — outcome map position, plugin stack, target buyer

3. After completion, capture output and write board entry to `board/narrative-output.yaml`:

```yaml
skill_name: "demo-narrative"
phase: "3.5"
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"

artifact_paths:
  acts_json: ".pipeline/demo-factory/artifacts/narrative/acts.json"
  demo_script: ".pipeline/demo-factory/artifacts/narrative/demo-script.md"
  yaml_scaffold: ".pipeline/demo-factory/artifacts/narrative/{name}.draft.demo.yaml"
artifact_type: "demo-narrative"

# Narrative details
methodology: "{cohan|demo2win|challenger}"
methodology_rationale: ""
act_count: N
total_duration_target_sec: N
wow_moments_total: N
wow_moments_spec_derived: N
wow_moments_methodology_derived: N

# Challenger-specific (null if not challenger)
reframe_validation:
  supplied_buyer_frame: ""
  reframe_insight: ""
  frame_used_in_opening: "{yes|no|partial}"

# Quality
discovery_prompts_placed: N
discovery_prompts_distribution: "{e.g., 'Act 1: 1, Act 2: 1, Act 3: 1'}"
persona_narration_alignment: true/false  # HLS gate #39
invariant_overrides: []  # e.g., gate #31 intentional deviation

quality_pass: true/false
quality_notes: ""

strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []
recommendations_for_downstream:
  - target_skill: "build"
    recommendation: "{e.g., 'YAML scaffold expects morning_briefing chapter — ensure agent trigger route exists'}"
    priority: "high"
```

4. Verify narrative artifacts were written to `.pipeline/demo-factory/artifacts/narrative/`:
   - `acts.json` — structured act sequence with timing, narration, screen states
   - `demo-script.md` — human-readable presenter script with act structure, scripts, discovery prompts, objection flags
   - `{name}.draft.demo.yaml` — chapter scaffold for demo-machine with CHAPTER INTENT and AUTOMATION REQUIRED blocks

5. Update `context.yaml`:
   ```yaml
   phase_completed: "narrative"
   narrative_methodology: "{cohan|demo2win|challenger}"
   ```

6. **MANDATORY STOP.** Print:

```
Demo Factory — Phase 3.5 (Narrative) Complete
==============================================
Board: .pipeline/demo-factory/
Concept: {concept}
Methodology: {methodology} — {one-line rationale}

Completed:
  ✓ Brainstorm → gap-analysis.md
  ✓ Research → {name}-research.md
  ✓ Spec → DEMO_SPEC.md (PRP: {PASS|FAIL})
  ✓ Narrative → {act_count} acts, {total_duration}s target
    acts.json        → .pipeline/demo-factory/artifacts/narrative/acts.json
    demo-script.md   → .pipeline/demo-factory/artifacts/narrative/demo-script.md
    YAML scaffold    → .pipeline/demo-factory/artifacts/narrative/{name}.draft.demo.yaml

Options:
  a) Build with Claude Code → start new session, run: /demo --build
  b) Build with Cursor → copy .mdc file, open in Cursor
  c) Stop here → narrative + spec complete, build later

If building with Claude Code, the new session will read the board
and provision workspace → database → app → resources → frontend.
```

Do NOT proceed to Phase 4 in this session. Narrative generation
involves methodology selection, act structuring, and script writing.
That context is irrelevant to infrastructure provisioning.

### Phase 4: Build (V2 — Adapter-Heavy)

**Session entry:** This phase runs in a NEW session after Phases 0-3 completed and stopped.

1. Read `.pipeline/demo-factory/context.yaml` → verify `phase_completed` is `"spec"` or `"narrative"`
2. Read `.pipeline/demo-factory/artifacts/DEMO_SPEC.md` — this is your build blueprint
3. Read `.pipeline/demo-factory/board/spec-output.yaml` → get plugin mappings and quality status
4. If `phase_completed == "narrative"`, also read `board/narrative-output.yaml` for methodology context and YAML scaffold location
5. Do NOT read gap-analysis.md or research.md. The spec (and narrative, if present) is your distilled input.

**This phase invokes Databricks infrastructure skills via adapters.** It is optional — the user may choose to build manually in Cursor using the .mdc file instead.

**CRITICAL: Use ALL Applicable FE-VIBE Skills**

Each build step below specifies which fe-vibe skill to invoke. The spec dictates which components are needed:

**Core Infrastructure Skills (by component type):**
- **Workspace:** `/databricks-fe-vm-workspace-deployment` OR `/databricks-oneenv-workspace-deployment`
- **Lakebase (Postgres):** `/databricks-lakebase`
- **Unity Catalog:** `/databricks-resource-deployment` (for catalogs, schemas, grants)
- **SQL Warehouses:** `/databricks-warehouse-selector` + `/databricks-resource-deployment`
- **Genie / Lakeview Dashboards:** `/databricks-lakeview-dashboard`
- **Delta Tables / Volumes:** `/databricks-resource-deployment`
- **ML / Model Serving:** `/databricks-resource-deployment` (for endpoints)
- **Vector Search:** `/databricks-resource-deployment`
- **Jobs / Workflows:** `/databricks-resource-deployment`
- **Notebooks:** `/databricks-resource-deployment`
- **Apps:** `/databricks-apps`
- **Frontend:** `/frontend-design`

**Auxiliary Skills:**
- **ALWAYS** use `/databricks-authentication` before any Databricks CLI operations
- **Consider** `/databricks-query` for validation queries or data exploration
- **Consider** `/databricks-lakeview-dashboard-analyzer` to analyze existing dashboards
- **Consider** `/databricks-workspace-files` for exploring workspace structure
- **Consider** `/fe-snowflake` if integrating with Snowflake
- **Consider** `/databricks-troubleshooting` if encountering deployment issues

**Pattern:** Read spec → identify components → invoke applicable skills → aggregate outputs → write board.

The skill invocations are explicit below for the core build steps. For auxiliary operations (auth, validation, troubleshooting), use your judgment to invoke the appropriate fe-vibe skill via the Skill tool.

**Skip condition:** User says "I'll build in Cursor" or "skip build." Or if no DEMO_SPEC.md exists (Phases 1-3 not complete).

#### 4a. Provision or Identify Workspace

**FE-VIBE SKILL:** Use `/databricks-fe-vm-workspace-deployment` OR `/databricks-oneenv-workspace-deployment` (if provisioning new workspace)

1. Read DEMO_SPEC.md `infrastructure.workspace` for requirements
2. **Check if workspace already exists:**

```
IF user provided workspace_url OR context.yaml has workspace_provisioned=true:
  # Use existing workspace
  READ workspace credentials from user or board/workspace-output.yaml
  VERIFY workspace is accessible (databricks workspace list --profile PROFILE)
  LOG: "Using existing workspace: {workspace_url}"
  SKIP to step 5 (write board entry with existing workspace info)
ELSE:
  # Provision new workspace
  PROCEED to step 3
```

3. **V2 Decision: Workspace Type Selection** (only if provisioning new workspace)

```
READ DEMO_SPEC.md → infrastructure.workspace
READ DEMO_SPEC.md → infrastructure (all sections for requirements analysis)

# Evaluate requirements
needs_custom_iam = infrastructure.workspace.custom_iam_roles is not empty
needs_multi_cloud = infrastructure.workspace.clouds.length > 1
needs_hipaa = "HIPAA" in infrastructure.workspace.compliance
needs_specific_region = infrastructure.workspace.region not in FE-VM supported regions

IF needs_custom_iam OR needs_multi_cloud OR needs_hipaa OR needs_specific_region:
  workspace_type = "one-env"
  SKILL: databricks-oneenv-workspace-deployment
  LOG: "Routing to One-Env workspace (requires: {reasons})"
ELSE:
  workspace_type = "fe-vm"
  SKILL: databricks-fe-vm-workspace-deployment (default)
  LOG: "Routing to FE-VM workspace (standard requirements)"
```

4. Invoke the selected fe-vibe skill via the Skill tool:
   ```
   Skill(skill: "databricks-fe-vm-workspace-deployment", args: "[workspace requirements from spec]")
   OR
   Skill(skill: "databricks-oneenv-workspace-deployment", args: "[workspace requirements from spec]")
   ```

5. Capture: workspace_url, workspace_id, profile_name
6. Write adapter board entry to `board/workspace-output.yaml`

#### 4b. Provision Databricks Infrastructure Components

**FE-VIBE SKILLS:** Use applicable skills based on spec requirements

This phase provisions ALL Databricks infrastructure components specified in DEMO_SPEC.md. Read the spec and invoke the appropriate fe-vibe skill(s):

**1. Identify required components from spec:**

```
READ DEMO_SPEC.md → infrastructure section
PARSE for component keywords:
  - lakebase / database → databricks-lakebase
  - unity catalog / metastore / catalog / schema → databricks-resource-deployment
  - sql warehouse / serverless sql → databricks-warehouse-selector + databricks-resource-deployment
  - genie / ai-bi / lakeview dashboard → databricks-lakeview-dashboard
  - delta tables / data engineering → databricks-resource-deployment (for tables/volumes)
  - ml / mlflow / model serving → databricks-resource-deployment (for model endpoints)
  - streaming / kafka / kinesis → databricks-resource-deployment (for streaming jobs)
  - vector search / embeddings → databricks-resource-deployment (for vector search endpoints)
```

**2. Provision each component via appropriate skill:**

**Lakebase (if specified):**
```
IF infrastructure.lakebase exists:
  Skill(skill: "databricks-lakebase", args: "Create [instance_name] with DDL from spec, PostGIS=[true/false]")
  CAPTURE: instance_id, connection_string, tables_created
  WRITE: board/lakebase-output.yaml
```

**Unity Catalog structures (if specified):**
```
IF infrastructure.unity_catalog exists:
  Skill(skill: "databricks-resource-deployment", args: "Create catalog [name], schemas [list], manage permissions")
  CAPTURE: catalog_name, schemas_created
  WRITE: board/unity-catalog-output.yaml
```

**SQL Warehouses (if specified):**
```
IF infrastructure.sql_warehouse exists OR spec references BI/analytics:
  Skill(skill: "databricks-warehouse-selector", args: "Select or create warehouse for [use_case]")
  Skill(skill: "databricks-resource-deployment", args: "Deploy warehouse [config from spec]")
  CAPTURE: warehouse_id, warehouse_name
  WRITE: board/warehouse-output.yaml
```

**Genie/Lakeview Dashboards (if specified):**
```
IF infrastructure.genie OR infrastructure.lakeview exists:
  Skill(skill: "databricks-lakeview-dashboard", args: "Create dashboard [spec] for warehouse [warehouse_id]")
  CAPTURE: dashboard_id, dashboard_url
  WRITE: board/lakeview-output.yaml
```

**Delta Tables/Volumes (if specified):**
```
IF infrastructure.delta_tables OR infrastructure.volumes exists:
  Skill(skill: "databricks-resource-deployment", args: "Create tables [list from spec] in catalog.schema")
  CAPTURE: tables_created, volumes_created
  WRITE: board/delta-output.yaml
```

**ML/Model Serving Endpoints (if specified):**
```
IF infrastructure.model_serving exists:
  Skill(skill: "databricks-resource-deployment", args: "Deploy model serving endpoint [config from spec]")
  CAPTURE: endpoint_id, endpoint_url
  WRITE: board/model-serving-output.yaml
```

**Vector Search (if specified):**
```
IF infrastructure.vector_search exists:
  Skill(skill: "databricks-resource-deployment", args: "Create vector search endpoint [config from spec]")
  CAPTURE: vector_search_endpoint_id
  WRITE: board/vector-search-output.yaml
```

**3. Aggregate outputs:**

After all components provisioned:
```
AGGREGATE all board/*-output.yaml files
UPDATE context.yaml:
   ```yaml
   phase_completed: "build-infra"
   workspace_provisioned: true
   lakebase_provisioned: true
   infra_tool_calls: N    # count of Bash/Write/Task calls during 4a-4b
   ```

6. **Conditional stop — deterministic rule:**

   Count the total tool calls (Bash, Write, Task) consumed during Phases 4a and 4b combined. This is observable from the conversation — count the tool-use blocks.

   - If `infra_tool_calls > 15` → **mandatory stop.** Infrastructure provisioning was complex enough to consume significant context. Print:
     ```
     Demo Factory — Infrastructure Provisioned (complex setup detected)
     ==========================================
       ✓ Workspace: {workspace_url}
       ✓ Lakebase: {instance_id} ({N} tables)
       Tool calls: {N} (threshold: 15)

     Application build remaining: scaffold → resources → frontend
     Start new session and run: /demo --build
     ```

   - If `infra_tool_calls <= 15` → continue to Phase 4c in this session. Log: "Infrastructure provisioning was straightforward ({N} tool calls). Continuing to application build."

#### 4c. Scaffold Application

**FE-VIBE SKILL:** Use `/databricks-apps`

1. Read DEMO_SPEC.md `infrastructure.app` for scaffold config
2. Read `board/lakebase-output.yaml` (if Lakebase was provisioned in 4b) — extract `connection_string`, `instance_id`, `postgis_enabled`
3. Read `board/workspace-output.yaml` — extract `workspace_url`, `profile_name`
4. Invoke the fe-vibe skill via the Skill tool:
   ```
   Skill(skill: "databricks-apps", args: "Deploy [app_name] app with Lakebase connection [connection_string], workspace [workspace_url]")
   ```
   Pass context:
   - App config from DEMO_SPEC.md
   - `connection_string` from lakebase-output.yaml (so the app can configure its database connection)
   - `workspace_url` from workspace-output.yaml (for API endpoint configuration)
5. Capture: app_url, app_name, deploy_status, resource_ids
6. Write adapter board entry to `board/apps-output.yaml`

#### 4d. Deploy Resources

**FE-VIBE SKILL:** Use `/databricks-resource-deployment`

1. Read DEMO_SPEC.md build sequence for resources (notebooks, jobs, clusters, warehouses)
2. Read `board/workspace-output.yaml` — extract `workspace_url`, `profile_name`
3. Invoke the fe-vibe skill via the Skill tool:
   ```
   Skill(skill: "databricks-resource-deployment", args: "Deploy [list resources from spec: notebooks, jobs, clusters, warehouses] to workspace [workspace_url]")
   ```
4. Capture: resources_deployed, workspace_url
5. Write adapter board entry to `board/resources-output.yaml`

#### 4e. Design & Implement Frontend (Optional)

**FE-VIBE SKILL:** Use `/frontend-design` for custom, production-grade UIs (OPTIONAL - see decision tree below)

**1. Determine frontend approach from spec:**

```
READ DEMO_SPEC.md → frontend section

IF frontend section is empty OR spec says "use default template":
  SKIP this phase (app scaffolded in 4c has default UI)
  LOG: "Using default template UI from databricks-apps scaffold"
  PROCEED to Phase 4.5

ELSE IF spec specifies "custom design" OR "distinctive aesthetic" OR "production-grade UI":
  PROCEED to step 2 (custom design)

ELSE:
  ASK USER: "Frontend approach for this demo?"
    a) Use default Databricks Apps template (fast, functional, generic)
    b) Generate custom design via /frontend-design skill (distinctive, production-grade)
    c) Skip frontend entirely (backend/data engineering demo)
    d) Design manually (highest quality, most control)
```

**2. If generating custom design, invoke frontend-design skill:**

```
READ DEMO_SPEC.md → frontend section for:
  - Personas (who uses this?)
  - Aesthetic direction (brutalist, retro-futuristic, editorial, etc.)
  - Components needed
  - Framework (React, Vue, HTML/CSS/JS)
  - Technical constraints

Skill(skill: "frontend-design", args: "
  Create [framework] frontend for [personas].

  Aesthetic direction: [BOLD direction from spec - e.g., 'brutalist medical dashboard with raw data visualization' or 'soft pastel patient portal with organic forms']

  Components: [list from spec]

  Constraints: [performance, accessibility, responsive requirements]

  Differentiation: [the ONE thing that makes this unforgettable - from spec's wow moment]
")
```

**3. Quality gate - evaluate generated design:**

```
REVIEW generated frontend code for:
  - Aesthetic distinctiveness (NOT generic Inter/purple gradients/cookie-cutter)
  - Production-grade code quality (functional, maintainable)
  - Context alignment (matches spec's personas and purpose)
  - Wow factor (memorable, cohesive, intentional)

IF design meets quality bar:
  CAPTURE: component_files, framework, aesthetic applied
  WRITE: board/frontend-output.yaml
  PROCEED to Phase 4.5

ELSE IF design is generic or low-quality:
  OPTION A: Iterate with more specific aesthetic direction
  OPTION B: Fall back to default template
  OPTION C: Flag for manual design (user builds it themselves)

  LOG to failures.yaml: "Frontend design quality below standard - [reason]"
```

**4. Fallback options if frontend-design skill doesn't meet quality bar:**

- **Iterate:** Re-invoke with more extreme aesthetic direction (e.g., "brutalist" → "brutalist with neon accents and monospace typography")
- **Template:** Use databricks-apps default template (functional but generic)
- **Manual:** User designs frontend manually after Phase 4 completes
- **Skip:** No frontend (backend-only demo, or Lakeview/Genie provides UI)

**5. Write board entry:**

```yaml
# board/frontend-output.yaml
skill_name: "frontend-design"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"

captured_output:
  approach: "{custom_design|default_template|manual|skipped}"
  component_files: []
  framework: "{react|vue|html}"
  aesthetic_direction: "{description}"
  quality_gate_passed: true/false
  quality_notes: ""

# If custom design
custom_design_details:
  typography: "{font choices}"
  color_theme: "{palette description}"
  differentiation_factor: "{the memorable element}"

quality_assessment: ""
quality_pass: true/false
```

**Note:** If the demo doesn't need a custom frontend (data engineering, notebooks-only, Lakeview dashboards provide UI), skip this phase entirely. Default templates from databricks-apps are perfectly fine for functional demos where UI isn't the differentiator.

**Build retry logic:** If any step fails:
- Retry with error context (max 2 retries per step)
- If 2 failures on same step → **BLOCK**. Stop and escalate to user with error details.
- Continue with other steps if they're independent (4a must precede 4b-4e)

### Phase 4.5: Verification

**Purpose:** Verify that the built code delivers what the spec promised. This phase runs after all build steps complete but before archival. It catches the gap between "code exists" and "code delivers the experience."

**Mandatory.** Cannot be skipped or bypassed. All four gates must pass or produce actionable failure reports.

#### 4.5a. Demo Narrative Gate

**Prevents:** Dead features that exist in spec but not in runtime (F1, F4, F5, F19 from sentiment sensor failures)

1. If `board/narrative-output.yaml` exists, read `artifacts/narrative/acts.json` for wow moments (acts with `wowMoment: true`). Methodology-derived wow moments (`wowSource: "methodology"`) are spoken moments, not UI interactions — exclude them from code path verification. Otherwise, read `DEMO_SPEC.md` → extract `## Wow Moments` section
2. Parse each wow moment into verification criteria:
   - What user action triggers it?
   - What data should be visible?
   - What backend endpoint serves it?
   - What frontend component renders it?
3. For each wow moment, verify code path exists:

```bash
# Example verification for "agent analyzes patient and shows learned patterns"
# Endpoint check
grep -r "analyze.*patient" app/server/ --include="*.py"
# UI component check
grep -r "learned.*pattern\|agent.*memory" app/frontend/ --include="*.tsx" --include="*.jsx"
# Data flow check
grep -r "agent_memory\|patient_analysis" app/server/ --include="*.py"
```

4. **Pass criteria:** Every wow moment has ≥1 code reference in (backend endpoint OR database query) AND ≥1 UI component reference
5. **Fail criteria:** Any wow moment has zero code paths
6. Write results to `board/verification-narrative-gate.yaml`:

```yaml
gate: "demo-narrative"
invoked_at: "{ISO timestamp}"
wow_moments_total: N
wow_moments_verified: N

findings:
  - wow_moment: "{text from spec}"
    backend_path: "{file:line or MISSING}"
    frontend_path: "{file:line or MISSING}"
    data_path: "{table/endpoint or MISSING}"
    status: "{PASS|FAIL}"
    evidence: "{grep output or explanation}"

gate_pass: true/false
blocking_failures: []  # moments with status=FAIL
recommendations: []
```

7. **If fail:** Present findings table to user. Do NOT proceed to 4.5b until user either:
   - Fixes the missing code paths and re-runs gate, OR
   - Explicitly acknowledges the gap and accepts partial demo

#### 4.5b. Dead Code Gate

**Prevents:** Modules/components built but never imported (F1, F11, F12, F19)

1. List all Python modules in `app/server/` (exclude `__init__.py`, `__main__.py`)
2. For each module, check if it's imported anywhere outside itself:

```bash
# For each module like server/llm.py
module_name="llm"
grep -r "from.*${module_name} import\|import.*${module_name}" app/ \
  --include="*.py" | grep -v "${module_name}.py:"
# If output is empty → ORPHANED
```

3. List all API functions in `app/frontend/lib/api.ts` (or equivalent)
4. For each API function, check if any React component calls it:

```bash
# For each function like fetchPatientAnalysis
grep -r "fetchPatientAnalysis" app/frontend/src/ --include="*.tsx" --include="*.jsx"
# If output is empty → ORPHANED
```

5. List all Pydantic models in `app/server/` with `class.*BaseModel`
6. For each model, check if it's used as `response_model=` or in a route handler:

```bash
# For each model like PatientAnalysisResponse
grep -r "response_model=.*PatientAnalysisResponse\|: PatientAnalysisResponse" app/server/
# If output is empty → ORPHANED
```

7. Write results to `board/verification-dead-code-gate.yaml`:

```yaml
gate: "dead-code"
invoked_at: "{ISO timestamp}"

python_modules:
  total: N
  orphaned: N
  orphaned_list: []

api_functions:
  total: N
  orphaned: N
  orphaned_list: []

pydantic_models:
  total: N
  orphaned: N
  orphaned_list: []

gate_pass: true/false  # false if any category has orphaned > 0
blocking_failures: []
recommendations:
  - type: "delete"
    target: "{file:line}"
    reason: "Never imported"
```

8. **If fail:** Present orphaned code list. User decides: delete it, or document why it's intentionally unused (e.g., future extension point).

#### 4.5c. Script Execution Gate

**Prevents:** Scripts that crash on first run (F2, F3)

1. List all executable scripts in `scripts/` and `app/scripts/`:

```bash
find app/scripts/ scripts/ -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null
```

2. For each script, attempt dry-run execution:

**Python scripts:**
```bash
# Check for --help flag
python script.py --help 2>&1
# If --help works, check for --dry-run
python script.py --dry-run 2>&1 || echo "No dry-run flag"
# If neither, check if it parses without error
python -m py_compile script.py
```

**Shell scripts:**
```bash
# Check syntax
bash -n script.sh
# If has --help, run it
bash script.sh --help 2>&1 || echo "No help flag"
```

3. Classify results:
   - **PASS**: `--help` or `--dry-run` runs without exit code != 0
   - **PARTIAL**: Script parses but has no dry-run mode
   - **FAIL**: Syntax error, import error, or crashes on `--help`

4. Write results to `board/verification-script-gate.yaml`:

```yaml
gate: "script-execution"
invoked_at: "{ISO timestamp}"

scripts_total: N
scripts_pass: N
scripts_partial: N
scripts_fail: N

findings:
  - script_path: ""
    dry_run_available: true/false
    help_available: true/false
    status: "{PASS|PARTIAL|FAIL}"
    error: "{error output if FAIL}"
    recommendation: "{e.g., 'Add --dry-run flag'}"

gate_pass: true/false  # false if any FAIL
blocking_failures: []
```

5. **If fail:** Scripts with syntax errors BLOCK. Scripts with no dry-run mode are warnings (note but proceed).

#### 4.5d. Build Manifest Gate

**Prevents:** Orphaned scripts that exist but are never called (F2, F3)

1. List all files in `scripts/` and `app/scripts/`
2. For each file, check if it's referenced in:
   - `README.md` or `DEMO_SPEC.md` (documentation)
   - Any other script (called by setup flow)
   - Any Python module (imported)
   - Any notebook (via `%run` or subprocess)

```bash
# For each script like setup-delta-sync.sh
script_name="setup-delta-sync.sh"

# Check README
grep -i "$script_name" README.md DEMO_SPEC.md

# Check called by other scripts
grep -r "$script_name" scripts/ app/scripts/ --exclude="$script_name"

# Check imported by Python
grep -r "import.*$(basename $script_name .py)" app/ --include="*.py"

# Check %run in notebooks
grep -r "%run.*$script_name" notebooks/ --include="*.py"
```

3. Classify:
   - **REFERENCED**: Found in ≥1 location
   - **ORPHANED**: Found in 0 locations

4. Write results to `board/verification-manifest-gate.yaml`:

```yaml
gate: "build-manifest"
invoked_at: "{ISO timestamp}"

files_total: N
files_referenced: N
files_orphaned: N

orphaned_files:
  - file_path: ""
    file_type: "{setup|seed|util}"
    recommendation: "{delete|document|move-to-archive}"

gate_pass: true/false  # false if orphaned > 0
blocking_failures: []
```

5. **If fail:** Present orphaned files. User decides: delete, or add to README as optional/future.

#### 4.5e. Verification Summary

After all four gates complete, write summary to `board/verification-summary.yaml`:

```yaml
phase: "verification"
invoked_at: "{ISO timestamp}"
gates_total: 4
gates_passed: N
gates_failed: N

gate_results:
  - gate: "demo-narrative"
    pass: true/false
    blocking_failures: N
  - gate: "dead-code"
    pass: true/false
    blocking_failures: N
  - gate: "script-execution"
    pass: true/false
    blocking_failures: N
  - gate: "build-manifest"
    pass: true/false
    blocking_failures: N

overall_pass: true/false  # true only if all 4 gates pass
recommendations_for_user: []
```

**Phase gate:** If `overall_pass == false`, **BLOCK**. Present the verification summary with failures highlighted. User must either:
- Fix the failures and re-run Phase 4.5
- Explicitly override with rationale (logged to `context.yaml` as `verification_override: true`)

If `overall_pass == true`, update `context.yaml`:
```yaml
phase_completed: "verification"
verification_passed: true
```

Proceed to Phase 5 (Archive Board).

### Phase 5: Archive Board

After all phases complete (or user stops after Phase 3):

1. Copy artifacts from `board/` to `artifacts/`
2. Move `.pipeline/demo-factory/` to `.pipeline/completed/demo-factory-{timestamp}/`
3. Present summary

## Output

```
DEMO FACTORY COMPLETE
=====================
Board: .pipeline/completed/demo-factory-{timestamp}/
Concept: {concept}
Industry: {industry}
Tier: {tier}
Scope: {scope}

Artifacts:
  - Gap Analysis: {path} (brainstorm)
  - Research Synthesis: {path} ({N} sources)
  - DEMO_SPEC.md: {path} ({N} tables, {N} features)
  - Cursor Rules: {path to .mdc} (if generated)
  - Narrative: {path to artifacts/narrative/} ({N} acts, {methodology}) (if generated)
    - acts.json, demo-script.md, {name}.draft.demo.yaml

Build Status: {NOT_STARTED | COMPLETE | PARTIAL}
  {if built: list deployed resources with URLs}
  {if partial: list what failed}

Quality Gates: {N}/{N} domain gates satisfied
PRP Verification: {PASS|FAIL|NOT_RUN}

Failures/Warnings: {N}
  {list from failures.yaml}
```

## Supervision Tree

For staleness detection (skills that don't produce board output within expected turns), see `.pipeline/schemas/README.md → Skill Invocation Timeout Guidance`.

| Primitive | Threshold | Retry | Degrade | Escalate |
|-----------|-----------|-------|---------|----------|
| demo brainstorm | Valid gap-analysis.md | 1 retry with constraints | Accept partial, flag gaps | Ask user for direction |
| demo research | >=3 sources per dimension | 2 retries on thin dimensions | Accept with coverage gaps noted | Log coverage gaps |
| demo spec | PRP gate pass | 2 iterations against PRP feedback | **BLOCK** — do not build from failing spec | Escalate with PRP failures |
| demo-narrative | acts.json + demo-script.md + YAML scaffold produced | 1 retry with adjusted methodology | Skip narrative, proceed to build with spec's Talk Track | Log methodology selection rationale |
| workspace (adapter) | Workspace accessible | 2 retries | **BLOCK** — no workspace = no demo | Escalate with error |
| lakebase (adapter) | Instance created, tables exist | 2 retries | **BLOCK** — no database = no demo | Escalate with error |
| apps (adapter) | App deploys, endpoints respond | 2 retries | Deploy API-only (no frontend) | Escalate with deploy logs |
| resources (adapter) | Resources deployed | 2 retries | Skip optional resources, deploy core | Escalate |
| frontend (adapter) | Components render | 1 retry with simplified layout | Use default template UI | Log, continue |
| **verification: narrative gate** | All wow moments have code paths | 1 retry with missing paths highlighted | **BLOCK** — cannot ship partial experience | Escalate with missing moments list |
| **verification: dead code gate** | Zero orphaned modules/functions | 0 retries (deterministic check) | Document orphans as "future extension" | Escalate with deletion recommendations |
| **verification: script execution gate** | All scripts parse without error | 0 retries (deterministic check) | Allow scripts without dry-run if documented | **BLOCK** on syntax errors |
| **verification: manifest gate** | Zero unreferenced scripts | 0 retries (deterministic check) | Document orphans as "optional/future" | Escalate with deletion recommendations |

## Routing Logic Summary

| Decision Point | Previous (V1) | Current (V2) |
|---------------|---------------------|---------------------|
| Post-research: coverage OK? | Always proceed to spec | Loop back if dimension coverage = "low" |
| Post-spec: PRP pass? | Iterate (max 2), then block | Same |
| Post-spec: narrative? | N/A (no narrative phase) | Mandatory stop, then Phase 3.5 via `/demo-narrative` |
| Post-narrative: proceed to build? | N/A | Mandatory stop, then Phase 4 in new session |
| Build: workspace type? | Always FE-VM | Route based on cloud/IAM reqs |
| Build: step failure? | Retry 2x, then block | Retry with error-informed fix |

## Fe-Vibe Adapter Protocol

Fe-vibe skills cannot write to the board. When this coordinator invokes them during Phase 4, it captures the output and writes a board entry on their behalf.

### databricks-fe-vm-workspace-deployment Adapter

**Write to:** `{board_dir}/board/workspace-output.yaml`

```yaml
skill_name: "databricks-fe-vm-workspace-deployment"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  workspace_url: ""
  workspace_id: ""
  profile_name: ""
  cloud: "{azure|aws|gcp}"
  region: ""

quality_assessment: ""
quality_pass: true/false
```

### databricks-oneenv-workspace-deployment Adapter

**Write to:** `{board_dir}/board/workspace-output.yaml` (same file as FE-VM — only one workspace is provisioned per demo)

```yaml
skill_name: "databricks-oneenv-workspace-deployment"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  workspace_url: ""
  workspace_id: ""
  profile_name: ""
  cloud: "{azure|aws|gcp}"
  region: ""
  deployment_type: "one-env"
  one_env_reason: "{custom_iam|multi_cloud|hipaa|postgis}"

quality_assessment: ""
quality_pass: true/false
```

The schema matches the FE-VM adapter. The additional `deployment_type` and `one_env_reason` fields document why this workspace was routed to One-Env. Downstream steps (4b, 4c, 4d) read `workspace-output.yaml` and are agnostic to which provisioner was used.

### databricks-lakebase Adapter

**Write to:** `{board_dir}/board/lakebase-output.yaml`

```yaml
skill_name: "databricks-lakebase"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  instance_id: ""
  connection_string: ""
  database_name: ""
  tables_created:
    - table_name: ""
      schema: ""
      row_count: N
  postgis_enabled: true/false

quality_assessment: ""
quality_pass: true/false
```

### databricks-apps Adapter

**Write to:** `{board_dir}/board/apps-output.yaml`

```yaml
skill_name: "databricks-apps"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  app_url: ""
  app_name: ""
  deploy_status: "{deployed|failed|partial}"
  resource_ids: []
  framework: "{fastapi-react|etc.}"
  scaffold_source: "{custom|genai-app-template}"

quality_assessment: ""
quality_pass: true/false
```

### databricks-resource-deployment Adapter

**Write to:** `{board_dir}/board/resources-output.yaml`

```yaml
skill_name: "databricks-resource-deployment"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  resources_deployed:
    - resource_type: "{notebook|job|cluster|warehouse}"
      resource_id: ""
      name: ""
      status: "{deployed|failed}"
  workspace_url: ""
  total_deployed: N
  total_failed: N

quality_assessment: ""
quality_pass: true/false
```

### frontend-design Adapter

**Write to:** `{board_dir}/board/frontend-output.yaml`

```yaml
skill_name: "frontend-design"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  component_files: []
  framework: "{react|vue|html}"
  aesthetic_direction: ""
  responsive: true/false
  accessibility_level: "{WCAG_AA|WCAG_AAA|basic}"

quality_assessment: ""
quality_pass: true/false
```
