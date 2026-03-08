---
name: content-factory
description: "End-to-end content production from objective to rendered artifacts. USE WHEN: user runs /full [objective], or when a multi-artifact content request spans 2+ artifact types. Orchestrates brainstorm, manifest, research, strategy, and all render primitives with board state."
allowed-tools: Read, Write, Bash, Task, Glob, Grep, Skill
---

# Content Factory

You are a content production coordinator. Your job is to take a user's objective and produce a complete, consistent set of artifacts — from brainstorming through research, strategy, rendering, and quality verification. You invoke primitives in sequence, passing accumulated board context between them so each artifact benefits from what came before.

## Trigger

Invoke when:
- User runs `/full [objective]`
- User requests "build me a [multi-artifact] package for [topic]"
- User's request clearly requires 2+ artifact types (deck + cheatsheet, or one-pager + enablement cards, etc.)

Do NOT invoke for:
- Single-artifact requests (route directly to the primitive — `/deck`, `/one-pager`, etc.)
- Enablement kits specifically (route to enablement-kit coordinator — it handles the cross-artifact invariants)

**Handoff to enablement-kit:** If the manifest (Phase 2) prescribes 3+ artifact types AND includes both a deck and role-specific enablement cards, route to the enablement-kit coordinator instead. It handles the cross-artifact consistency invariants that content-factory delegates.

## Source Material

Required:
- User objective string (what they want, who it's for, why)

Optional:
- Account context (from vault_summary if account-specific)
- Existing knowledge bases (from `Knowledge/` directories)
- Existing strategy YAML (if user has one from a prior session)

## Blackboard Integration (Context Preservation + Parallelization)

**Primary Objective:** Use blackboard's board signals as external memory to preserve context across complex handoffs and prevent context loss during long-running content pipelines.

**Secondary Objective:** Parallelize independent work streams when beneficial (especially during render phase).

### When to Use Blackboard at the Factory Level

Invoke blackboard skill at the factory coordinator level when:
- Multi-phase content pipeline has complex handoffs requiring context preservation (brainstorm → manifest → research → strategy → render)
- Pipeline spans multiple sessions (mandatory stops between phases mean context will be lost)
- Accumulated findings from early phases must inform later phases (research insights → strategy → render)
- Session boundaries create risk of losing critical decisions, audience insights, or strategic direction

**Pattern:** Blackboard creates a durable board that survives session boundaries and context compaction. Each phase writes board signals that subsequent phases read.

**Example invocation at factory level:**
```
# At Phase 4 completion (strategy), before mandatory stop before render
Task(
  subagent_type: "blackboard",
  prompt: "Coordinate content-factory pipeline phases with board signals.

  Phases: brainstorm (complete) → manifest (complete) → research (complete) → strategy (complete) → render (next)

  Synthesis format: content-pipeline-state

  Parent board: .pipeline/content-factory/

  Primary goal: Preserve strategy decisions and research coverage for render phase (hero message, proof points, audience assumptions, competitive frame)"
)
```

### When to Use Blackboard Within a Phase

Invoke blackboard skill within a specific phase when:
- Phase has 2+ independent work streams that can run in parallel
- Work streams have non-trivial complexity (each >5 min estimated)
- Parallelization saves meaningful time (≥30% reduction vs sequential)
- Board signals needed to ensure cross-artifact consistency

**Example: Phase 3 (Research) with Multiple Dimensions**

If research needs to cover multiple dimensions in parallel:
- Personas (audience research)
- Competitive landscape
- Product capabilities
- Customer references

```python
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize: personas research, competitive research, product research, references research

  Synthesis format: research-synthesis

  Parent board: .pipeline/content-factory/

  Note: All four dimensions are independent and can run fully in parallel."
)
```

**Example: Phase 5 (Render) with Multiple Artifacts**

If manifest prescribes 3+ artifacts that can be rendered in parallel:

```python
# After Phase 4 (strategy complete), parallelize artifact rendering
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize: render deck (slides 1-15), render cheatsheet, render one-pager

  Synthesis format: artifact-metadata

  Parent board: .pipeline/content-factory/board/

  Note: All artifacts read from the same strategy-contract.yaml but are otherwise independent. Deck has no dependencies on cheatsheet or one-pager. Parallelization can save significant time for multi-artifact packages."
)
```

**Example: Phase 5 Deck Rendering with Large Deck (>20 slides)**

If a single deck has 30+ slides and can be rendered in batches:

```python
# Within deck-render, if slide count > 20
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize: render slides 1-10 (intro), render slides 11-20 (body), render slides 21-30 (close)

  Synthesis format: artifact-metadata

  Parent board: .pipeline/content-factory/artifacts/deck-partials/

  Note: Batches can render in parallel as long as each batch has its build-plan.md section available."
)
```

### Board Signal Schema for Factory Coordination

When blackboard is used at the factory level, it should produce synthesis files that content-factory can read:

**content-pipeline-state.yaml** (for cross-phase coordination):
```yaml
pipeline: "content-factory"
current_phase: "render"
phase_dependencies:
  render:
    needs: ["strategy", "research", "manifest"]
    reads_from: [".pipeline/content-factory/strategy-contract.yaml", ".pipeline/content-factory/board/research-output.yaml", ".pipeline/content-factory/manifest.yaml"]
    writes_to: ".pipeline/content-factory/board/{artifact}-output.yaml"

accumulated_context:
  hero_message: ""
  proof_points: []
  competitive_frame: ""
  audience_profile: ""
  research_coverage:
    personas: "high|medium|low"
    competitive: "high|medium|low"
    product: "high|medium|low"

ready_for_next_phase: true/false
blocking_issues: []
coverage_gaps: []
```

**artifact-metadata.yaml** (for Phase 5 render coordination):
```yaml
artifacts:
  - type: "deck"
    path: ".pipeline/content-factory/artifacts/deck.pptx"
    status: "complete"
    metadata:
      slide_count: 15
      hero_message_as_rendered: ""
      proof_points_used: []
      quality_score: 14/15
  - type: "cheatsheet"
    path: ".pipeline/content-factory/artifacts/cheatsheet.html"
    status: "complete"
    metadata:
      hero_message_as_rendered: ""
      proof_points_used: []
      quality_score: 16/20
  - type: "one-pager"
    path: ".pipeline/content-factory/artifacts/one-pager.pdf"
    status: "complete"
    metadata:
      hero_message_as_rendered: ""
      proof_points_used: []
      quality_score: 20/24

parallelized_renders:
  - artifact: "deck"
    agent: "deck-render-agent-1"
    status: "complete"
  - artifact: "cheatsheet"
    agent: "cheatsheet-render-agent-2"
    status: "complete"
  - artifact: "one-pager"
    agent: "one-pager-render-agent-3"
    status: "complete"

consistency_check_required: true  # true if 2+ artifacts
```

### When NOT to Use Blackboard

Do NOT invoke blackboard when:
- Phase is simple linear work (<5 min total)
- No parallelization opportunity exists (strict sequential dependencies)
- Session is fresh and context is clean (early in a phase)
- Board signals would add overhead without benefit
- Only rendering 1 artifact (no cross-artifact coordination needed)

**Anti-pattern:** Using blackboard for every tiny step. Reserve it for:
1. Cross-session coordination (mandatory stops between phases)
2. Non-trivial parallelization (multi-artifact renders, multi-dimension research)
3. Complex handoffs where context preservation is critical (strategy → render with 10+ strategic decisions)

### Integration with Existing Board

Content-factory already has a board at `.pipeline/content-factory/`. When blackboard is invoked:
- Nested mode: `--nested` flag tells blackboard to create sub-board under content-factory's board
- Board location: `.pipeline/content-factory/board/blackboard-{timestamp}/`
- Synthesis files: Written to content-factory's board for consumption by subsequent phases or consistency checks

**Critical:** Blackboard's board signals are FILE-BASED YAML. They must be durable, not ephemeral messages. This ensures context survives session boundaries and context compaction.

### Recursive Nesting (Automatic Multi-Level Parallelization)

**Rule:** If you discover a parallelization opportunity while working on a task (even if you were already spawned by blackboard), invoke blackboard again with `--nested`.

**Pattern:** Blackboard → blackboard → blackboard (up to depth 3)

**Example Flow:**

```
Level 0: content-factory (coordinator)
  ↓
Level 1: blackboard coordinates Phase 5 render (3 artifacts)
  ├─ Agent 1: Render deck ← discovers 30 slides, can batch
  │   ↓
  │   Level 2: blackboard coordinates deck batches
  │     ├─ Agent 1a: Render slides 1-10
  │     ├─ Agent 1b: Render slides 11-20
  │     └─ Agent 1c: Render slides 21-30
  ├─ Agent 2: Render cheatsheet
  └─ Agent 3: Render one-pager
```

**When to nest:**
- You're inside an agent (spawned by blackboard or factory)
- You discover 2+ independent sub-tasks within your assigned work
- Each sub-task is non-trivial (>2 min estimated)
- Parallelizing them saves ≥30% time

**How to nest:**

```python
# Inside deck-render agent, discovers 30 slides can be batched
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize: render slides 1-10 (intro+context), render slides 11-20 (solution), render slides 21-30 (proof+close)

  Synthesis format: artifact-metadata

  Parent board: {current_agent_board_path}

  Note: Each batch has its own build-plan.md section. Batches are independent."
)
```

**Research nesting example:**

```python
# Inside research agent, discovers 14 queries across 4 dimensions
Task(
  subagent_type: "blackboard",
  prompt: "--nested

  Parallelize research by dimension:

  Stream 1 (personas): 4 Glean queries + 2 web searches
  Stream 2 (competitive): 3 web searches
  Stream 3 (product): 3 Glean queries
  Stream 4 (references): 2 Glean queries

  Synthesis format: research-synthesis

  Parent board: {current_agent_board_path}

  Note: All dimensions are independent. Each stream runs its queries sequentially, but streams run in parallel."
)
```

**Max depth:** 3 levels (hard limit in blackboard skill to prevent infinite recursion)

**Example depth-3 scenario:**
1. **content-factory** invokes blackboard for Phase 5 (render 3 artifacts)
2. **render-blackboard** spawns "deck-render" agent
3. **deck-render agent** invokes blackboard for 3 slide batches
4. **batch-blackboard** spawns agent per batch
5. ❌ **batch agent CANNOT** invoke blackboard again (depth limit reached)

**Detection pattern:** Always check for parallelization before executing sequential work. Ask: "Can I break this into 2+ independent streams?"

**Anti-pattern:** Don't nest for trivial splits (e.g., 2 queries that each take 30 seconds). Overhead exceeds benefit.

### Phase 6 Consistency Check Integration

When blackboard is used to parallelize Phase 5 renders, the Phase 6 consistency check reads from the blackboard's synthesis file:

```python
# Phase 6: Read parallelized render outputs
READ .pipeline/content-factory/board/blackboard-{timestamp}/artifacts/SYNTHESIS.yaml
# Extract hero_message_as_rendered from each artifact
# Apply semantic equivalence rubric
# Check proof_point_distribution
```

This pattern ensures that even if artifacts were rendered by different agents in parallel, the consistency check can still validate cross-artifact invariants.

## Entry Point Routing

Parse $ARGUMENTS to determine entry point:

- If $ARGUMENTS starts with "--render":
  → Skip to Phase 5 (Render Artifacts)
  → Read `.pipeline/content-factory/context.yaml` → verify `phase_completed` is "strategy" or later
  → If phase_completed is null or earlier than "strategy", tell user: "Research/strategy not complete. Run `/full [objective]` first."
  → Otherwise, proceed to Phase 5 preamble

- If $ARGUMENTS starts with "--consistency" or "--check":
  → Skip to Phase 6 (Cross-Artifact Consistency Check)
  → Verify all artifacts in manifest are rendered (renders_completed matches artifact_list)

- If $ARGUMENTS is empty or starts with anything else:
  → Treat entire $ARGUMENTS as the user's objective
  → Start from Phase 0

## Board Setup (Phase 0)

### 0a. Create board directory

```
.pipeline/content-factory/
├── context.yaml              ← objective, audience, domain, constraints
├── strategy-contract.yaml    ← living strategy (seeded by /strategy, amended by skills)
├── board/                    ← skill outputs land here
├── artifacts/                ← rendered files land here
└── failures.yaml             ← error log (create empty)
```

### 0b. Write context.yaml

Extract from user's objective:

```yaml
_meta:
  board_dir: ".pipeline/content-factory/"
  coordinator: "content-factory"
  run_id: "{ISO timestamp}"

phase_completed: null          # null → brainstorm → manifest → research → strategy → render → consistency → complete
strategy_version: null
strategy_updated_at: null
renders_completed: []
deck_batch_completed: 0
research_retry_count: 0

objective: "{user's stated objective}"
account: "{if account-specific, else null}"
domain: "{HLS|FSI|etc. — infer from objective or ask}"
audience_profile: "{from hls-tailoring-map.yaml key, if applicable}"
moment: "{pre-meeting|mid-call|post-meeting|leave-behind|enablement}"
extracted_entities: []
constraints: []
```

## Pipeline Sequence

### Phase 1: Brainstorm

Invoke `/brainstorm` with the user's objective.

1. Run Socratic questioning to clarify: audience, format, key message, competitive context
2. Write brainstorm output to `context.yaml` (update with clarified fields)
3. Proceed to Phase 2

### Phase 2: Manifest

Invoke `/manifest` with the clarified objective.

1. Produce artifact list and research plan
2. Write manifest to `.pipeline/content-factory/manifest.yaml`

**Decision point:** If manifest prescribes research, proceed to Phase 3. If knowledge already exists with coverage >80%, skip to Phase 4.

**Enablement-kit handoff:** If manifest has 3+ artifact types including deck + enablement cards, STOP. Before handing off:
1. Run Phase 3 (Research) if manifest prescribes it — enablement-kit needs a knowledge base
2. Run Phase 4 (Strategy) to produce `strategy-contract.yaml` — enablement-kit requires this
3. Write `context.yaml`, `manifest.yaml`, `strategy-contract.yaml`, and `knowledge.md` to `.pipeline/enablement-kit/` for enablement-kit to consume
4. Archive content-factory's own board: move `.pipeline/content-factory/` to `.pipeline/completed/content-factory-handoff-{timestamp}/`
5. Route to enablement-kit coordinator. Content-factory's job is done after handoff.

### Phase 2.5: Product Question Research (conditional, adapter)

**Skip condition:** If the manifest does not include product questions or if no open Databricks product questions need answering, skip.

If the brainstorm or manifest surfaces Databricks product questions (e.g., "does Lakebase support PostGIS?", "what's the latency for Model Serving?"):

1. Invoke `product-question-research` skill (fe-vibe — cannot write to board)
2. Capture: questions answered, answer summaries, confidence levels, source URLs
3. Write adapter board entry to `board/product-question-research-output.yaml`
4. Feed answers into Phase 3 (Research) as pre-resolved context

See ## Fe-Vibe Adapter Protocol section below for capture schema.

### Phase 3: Research (conditional)

Invoke `/research` with the research plan from manifest.

1. Produce knowledge.md with research atoms
2. Write research output to `board/research-output.yaml`:

```yaml
skill_name: "research"
invoked_at: "{ISO timestamp}"
invoked_by: "content-factory"
artifact_path: "{path to knowledge.md}"
artifact_type: "knowledge"
coverage_per_dimension:
  personas: "{high|medium|low}"         # high >= 80%, medium >= 50%, low < 50%
  competitive: "{high|medium|low}"
  references: "{high|medium|low}"
  product: "{high|medium|low}"
coverage_gaps: []
source_count: N
quality_pass: true/false
```

**V2 Decision: Post-Research Coverage Check**

After writing `board/research-output.yaml`, evaluate coverage per dimension:

```
READ board/research-output.yaml → coverage_per_dimension
READ context.yaml → research_retry_count (default 0 if absent)

FOR each dimension in {personas, competitive, references, product}:
  IF coverage == "low":
    MARK dimension as "thin"

IF any dimension is "thin":
  IF research_retry_count < 2:
    SET research_retry_count = research_retry_count + 1
    WRITE research_retry_count back to context.yaml (persist before re-invoke)
    RE-INVOKE /research with:
      - Focused queries ONLY on thin dimensions (don't re-research strong ones)
      - Prior research-output.yaml as context (so agents don't duplicate findings)
      - Specific gap descriptions from coverage_gaps[]
    WRITE updated board/research-output.yaml (overwrite — new version)
    RE-EVALUATE coverage
  ELSE:
    LOG to failures.yaml: "Research coverage 'low' on {dimensions} after 2 retries (low = <50% coverage)"
    PROCEED to Phase 4 with gaps noted — strategy will acknowledge limitations
    ADD strategy_contract_amendments:
      - field: "coverage_limitations"
        recommended_value: "{list thin dimensions and their coverage %}"
        reason: "Research could not resolve these gaps after 2 attempts"
ELSE:
  PROCEED to Phase 4
```

### Phase 4: Strategy

Invoke `/strategy` with accumulated context (brainstorm + manifest + research).

1. Produce strategy contract
2. Write to `.pipeline/content-factory/strategy-contract.yaml` with `_meta` fields added:

```yaml
_meta:
  board_dir: ".pipeline/content-factory/"
  coordinator: "content-factory"
  run_id: "{ISO timestamp}"
version: 1
amendments_log: []
# ... rest of strategy fields ...
```

**Decision point:** Read research board output. If gaps flagged, amend strategy to acknowledge limitations.

3. Update `context.yaml`:

```yaml
phase_completed: "strategy"
strategy_version: 1
strategy_updated_at: "{ISO timestamp}"
```

4. **MANDATORY STOP.** Print:

```
Content Factory — Phases 0-4 Complete
======================================
Board: .pipeline/content-factory/
Objective: {objective}

Completed:
  ✓ Brainstorm → context.yaml updated
  ✓ Manifest → manifest.yaml ({N} artifacts planned)
  ✓ Research → knowledge.md ({coverage summary})
  ✓ Strategy → strategy-contract.yaml v{N}

Artifacts to render: {list from manifest}
Render order: {ordered list}

Start a new session and run: /full --render
Or: /render (reads .pipeline/content-factory/ automatically)

To modify strategy before rendering, edit strategy-contract.yaml
and bump strategy_version + strategy_updated_at.
```

Do NOT proceed to Phase 5 in this session. The context consumed by Phases 0-4
(brainstorm dialogue, research sources, strategy reasoning) must be evicted before
rendering begins. This is the single highest-impact change for output quality.

### Phase 5: Render Artifacts

**Session entry:** This phase runs in a NEW session after Phases 0-4 completed and stopped.

1. Read `.pipeline/content-factory/context.yaml` → verify `phase_completed == "strategy"`
2. Read `.pipeline/content-factory/strategy-contract.yaml`
3. Read `.pipeline/content-factory/manifest.yaml` → get artifact list and render order
4. Read `.pipeline/content-factory/board/research-output.yaml` → get coverage data
5. Do NOT read knowledge.md in full. The strategy contract is your distilled input. Only reference knowledge.md for specific fact-checking during generation.

**Strategy staleness check:** Compare `strategy_updated_at` in context.yaml against the timestamp on any existing render board outputs. If strategy is newer than existing renders, warn the user and offer to re-render affected artifacts.

**Completion check (run on every Phase 5 entry, including resumes):**

```
READ context.yaml → renders_completed[]
READ manifest.yaml → artifact_list[]

# Normalize: artifact_list contains types like "deck", "cheatsheet", "one-pager"
# renders_completed contains entries like "deck", "deck-batch-1", "cheatsheet"
# For decks, check if all batches are done:
IF "deck" in artifact_list:
  Check .pipeline/content-factory/artifacts/deck-partials/
  IF all batches in build-plan.md are present → mark "deck" as complete
  ELSE → deck still needs rendering

# Strip "-batch-N" suffixes: "deck-batch-1" → "deck", "cheatsheet" → "cheatsheet"
completed_types = [r.split("-batch-")[0] for r in renders_completed]
remaining = [a for a in artifact_list if a not in completed_types]

IF len(remaining) == 0:
  → ALL RENDERS COMPLETE. Skip Phase 5 entirely.
  → Proceed to Phase 6 (Consistency Check)
  → Print: "All {N} artifacts rendered. Running cross-artifact consistency check."
ELSE:
  → Resume Phase 5 from first item in `remaining`
  → Print: "Resuming render. Remaining: {remaining}"
```

**V2 Decision: Artifact Eligibility Check**

Before starting the render loop, evaluate which artifacts have sufficient research backing:

```
READ board/research-output.yaml → coverage_per_dimension, coverage_gaps[]
READ manifest.yaml → artifact_list[]

FOR each artifact in artifact_list:
  DETERMINE which research dimensions this artifact needs:
    - deck: needs personas (HIGH), competitive (MEDIUM), references (HIGH)
    - cheatsheet: needs product (HIGH), competitive (MEDIUM)
    - one-pager: needs personas (HIGH), references (HIGH), competitive (MEDIUM)
    - enablement-card: needs personas (HIGH), product (HIGH)
    - email: needs personas (MEDIUM) only

  FOR each required dimension:
    IF coverage == "low" AND requirement = HIGH:
      MARK artifact as "insufficient_coverage"

  IF artifact is marked "insufficient_coverage":
    LOG warning: "{artifact} skipped — insufficient research coverage on {dimensions}"
    REMOVE from render loop
    ADD to failures.yaml

IF no artifacts remain after filtering:
  ESCALATE to user: "All artifacts lack sufficient research coverage. Re-research or provide additional context."
```

For each eligible artifact in the manifest (ordered by visual investment — highest first):

1. Invoke the render primitive with the strategy-contract.yaml (which contains `_meta.board_dir`)
2. The primitive will:
   - Read board state (prior skill outputs, invariants if present)
   - Render the artifact
   - Write its board entry to `board/{skill}-output.yaml`
3. Read the board entry
4. **Quality gate**: Check `quality_pass` against the primitive's own threshold
   - If pass → proceed to next artifact
   - If fail → retry once with accumulated board state as enrichment context (max 1 retry per artifact)
   - If retry fails → produce with warnings, log to failures.yaml, continue
5. Merge any `strategy_contract_amendments` into strategy-contract.yaml (increment version, append to amendments_log)
6. Update `context.yaml`:
   ```yaml
   last_rendered: "{artifact_type}"
   renders_completed: ["{list of completed artifact types}"]
   ```

**Session stop rule (single rule, no exceptions):**

After generating the equivalent of 10 slides worth of content in this session, stop. The conversion:
- 1 deck slide = 1 unit
- 1 cheatsheet = 5 units (roughly equivalent context cost to 5 slides)
- 1 one-pager = 3 units
- 1 enablement card = 2 units
- 1 email = 1 unit

Track a running total in-session. When it hits 10, stop and prompt for a new session. Write progress to context.yaml before stopping:

```yaml
renders_completed: ["deck-batch-1", "deck-batch-2"]
render_units_last_session: 10
```

This replaces multiple separate counters. One number, one threshold, one rule. Conversion factors are estimates — tune based on real usage.

**Single-artifact exception:** If a single artifact exceeds 10 units (e.g., a 15-slide deck), complete that artifact before stopping. The 10-unit threshold is a session budget, not a mid-artifact kill switch.

**Resume detection:** When Phase 5 starts (or resumes), read `context.yaml → renders_completed[]` and compare against `manifest.yaml → artifact_list[]`. Skip completed items. For decks, check if all batches are done by reading `.pipeline/content-factory/artifacts/deck-partials/`.

**Rendering order** (highest visual investment first):
1. deck-render (if manifest includes a deck)
2. cheatsheet-render (if included)
3. one-pager-render (if included)
4. enablement-card-render (if included, per role variant)
5. email-render (if included)

### Phase 6: Cross-Artifact Consistency Check

**Skip condition:** If only 1 artifact was produced, skip this phase.

**Session guidance:** If this is a multi-artifact package (3+ artifacts), run the consistency check in a fresh session. The check needs to load all board outputs and compare them — a clean context produces better judgment. For 2-artifact packages, running in the same session as the last render is acceptable.

After all renders complete (verify `renders_completed` in context.yaml matches `artifact_list` in manifest.yaml):

1. Collect `hero_message_as_rendered` from each board output. Apply the semantic equivalence rubric from `.pipeline/schemas/README.md → Hero Message Semantic Equivalence Rubric`.
2. Collect `proof_points_used` from each board output. Apply the normalization rules from `.pipeline/schemas/README.md → Proof Point Matching Rules` before comparing.
3. Verify: hero messages semantically equivalent (not necessarily identical — deck may use short form, one-pager may use long form)
4. Verify: no proof point used in >2 artifacts (distribution, not duplication)
5. Verify: `competitive_frame_as_rendered` consistent across all artifacts
6. Verify: call-to-action is unified across all artifacts (if present in board outputs)
7. Verify: audience assumptions are coherent — intentional differences documented, unintentional ones flagged
8. Write `board/consistency-check.yaml`:

```yaml
checked_at: "{ISO timestamp}"
artifacts_checked: []
results:
  hero_message: { pass: true, notes: "" }
  proof_point_distribution: { pass: true, notes: "" }
  competitive_frame: { pass: true, notes: "" }
  cta_consistency: { pass: true, notes: "" }
  audience_coherence: { pass: true, notes: "" }
overall_pass: true
failures: []
```

7. **V2 Decision: Smart Re-Render Selection**

If `overall_pass` is false:

```
READ board/consistency-check.yaml → failures[]

FOR each failure in failures:
  IDENTIFY which artifact(s) diverged
  CALCULATE blast_radius DYNAMICALLY from the manifest:
    dependency_graph = {
      deck: [],               # deck reads nothing
      cheatsheet: [deck],     # cheatsheet reads deck
      one-pager: [deck, cheatsheet],  # one-pager reads both
      enablement-card: [deck, cheatsheet, one-pager],  # reads all prior
      email: []               # reads nothing from other artifacts
    }
    FOR each artifact in manifest:
      blast_radius[artifact] = count of OTHER manifest artifacts that list this artifact in their dependencies

  SPECIAL RULE — "deck is authoritative for hero_message":
    IF deck diverged on hero_message:
      DO NOT re-render deck
      INSTEAD: Re-render the OTHER artifact(s) to match the deck's hero_message
      Deck sets the visual tone; others adapt to it

  SORT divergent artifacts by blast_radius ASCENDING (fix lowest impact first)

  FOR each divergent artifact (lowest blast_radius first):
    RE-RENDER with:
      - Original strategy-contract.yaml
      - ALL board outputs from non-divergent artifacts as enrichment
      - Specific consistency failure description as constraint
    MAX 1 re-render per artifact

    AFTER re-render:
      RE-RUN full consistency check (all criteria — re-render may introduce new failures)
      IF all pass → continue
      IF still failing → LOG and flag to user

IF re-renders don't resolve all failures:
  PRESENT specific mismatches to user:
    "Consistency check failed after re-render:
     - {criterion}: {artifact A} says X, {artifact B} says Y
     Which is correct? I'll update the divergent artifact."
```

### Phase 7: Upload to Google Workspace (conditional, adapter)

**Skip condition:** If no Google Workspace skills are available (test via gcloud auth), skip this phase entirely.

After all artifacts pass (Phase 6 consistency check passes or was skipped):

1. **Deck → Google Slides:**
   - Invoke `google-slides` skill with the rendered .pptx
   - Capture: presentation_url, presentation_id, slide_count
   - Write adapter board entry to `board/google-slides-output.yaml`

2. **Documents → Google Docs:**
   - For each document artifact (one-pager, cheatsheet, enablement cards):
     - Invoke `google-docs` skill to create/update
     - Capture: doc_url, doc_id, version, content_hash
     - Write adapter board entry to `board/google-docs-{artifact-type}-output.yaml`

3. **Report upload results in Phase 8 output.**
   - If any upload fails: log to failures.yaml, continue (non-blocking)

See ## Fe-Vibe Adapter Protocol section below for capture schemas.

### Phase 8: Archive Board

After all artifacts pass and optional uploads complete:

1. Copy all artifacts from `.pipeline/content-factory/artifacts/` to delivery directory
2. Move `.pipeline/content-factory/` to `.pipeline/completed/content-factory-{timestamp}/`
3. Present summary to user

## Output

```
CONTENT FACTORY COMPLETE
========================
Board: .pipeline/completed/content-factory-{timestamp}/
Objective: {original objective}

Artifacts:
  {list each artifact with path, type, quality score}

Consistency Check: {PASS|FAIL|SKIPPED}
  {details if applicable}

Strategy Amendments Applied: {N}
  {list of amendments}

Research Coverage: {per-dimension if research ran}

Failures/Warnings: {N}
  {list from failures.yaml}
```

## Supervision Tree

For staleness detection (skills that don't produce board output within expected turns), see `.pipeline/schemas/README.md → Skill Invocation Timeout Guidance`.

| Primitive | Threshold | Retry | Degrade | Escalate |
|-----------|-----------|-------|---------|----------|
| /brainstorm | Valid brainstorm output | Re-run with clarifying questions | Skip (user provides strategy directly) | Ask user |
| /research | No "low" coverage per critical dimension | Re-research refined queries, max 2 | Accept with gaps noted | Log gaps |
| /strategy | Valid strategy-contract.yaml | Re-generate with board context | Use minimal strategy (audience + hero only) | Ask user |
| deck-render | Per-slide CLEAN | 1 retry with board enrichment | Produce with warnings, continue | Log to failures.yaml |
| cheatsheet-render | 15/20 rubric | 1 retry with deck context | Produce with warnings, continue | Log |
| one-pager-render | 18/24 rubric | 1 retry with all prior outputs | Produce with warnings, continue | Log |
| enablement-card-render | 15/20 per role | 1 retry per variant | Skip failing variant | Log |
| Consistency check | All criteria pass | Re-render divergent artifact (1x) | Accept with log | Flag to user |

## Routing Logic Summary

| Decision Point | Previous (V1) | Current (V2) |
|---------------|--------------|--------------|
| Post-research: sufficient? | Always proceed to strategy | Loop back if any dimension is "low" (max 2 retries, persisted in context.yaml) |
| Post-render: quality OK? | Always proceed to next | Retry with enriched context from all prior board outputs |
| Multi-artifact: which? | Produce all from manifest | Skip artifacts with insufficient research coverage on HIGH dimensions |
| Post-consistency: fix? | Re-render first failure | Dynamic blast radius + deck-is-authoritative rule |

## Fe-Vibe Adapter Protocol

Fe-vibe skills cannot write to the board. When this coordinator invokes them, it captures the output and writes a board entry on their behalf.

### google-slides Adapter

**When invoked:** Phase 7, after all artifacts pass quality and consistency checks.

**Write to:** `{board_dir}/board/google-slides-output.yaml`

```yaml
skill_name: "google-slides"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "content-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  presentation_url: ""
  presentation_id: ""
  slide_count: N
  source_artifact: "{path to .pptx}"

quality_assessment: ""
quality_pass: true/false
```

### google-docs Adapter

**When invoked:** Phase 7, for each document artifact.

**Write to:** `{board_dir}/board/google-docs-{artifact-type}-output.yaml`

```yaml
skill_name: "google-docs"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "content-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  doc_url: ""
  doc_id: ""
  version: N
  content_hash: ""
  source_artifact: "{path to source file}"
  artifact_type: "{one-pager|cheatsheet|enablement-card-role|etc.}"

quality_assessment: ""
quality_pass: true/false
```

### product-question-research Adapter

**When invoked:** Phase 2.5, when product questions surface during brainstorm/manifest.

**Write to:** `{board_dir}/board/product-question-research-output.yaml`

```yaml
skill_name: "product-question-research"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "content-factory"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  questions_answered: N
  questions:
    - question: "{text}"
      answer_summary: "{brief answer}"
      confidence: "{high|medium|low}"
      sources:
        - title: ""
          url: ""
  gaps: []                              # questions with no good answer

quality_assessment: "{coordinator's evaluation of answer quality and completeness}"
quality_pass: true/false
```
