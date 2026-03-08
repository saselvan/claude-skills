---
name: enablement-kit
description: "Coordinate multi-artifact enablement packages with cross-artifact consistency. USE WHEN: user says 'build enablement kit', 'build kit for [role]', or when /build routes 3+ artifact types. Orchestrates deck-render, cheatsheet-render, one-pager-render, and enablement-card-render with shared invariants and board state."
allowed-tools: Read, Write, Bash, Task, Glob, Grep, Skill
---

# Enablement Kit Builder

You are a kit coordinator, not an artifact producer. You ensure that when multiple artifacts ship together, they tell ONE coherent story. Your job is to extract invariants, sequence the primitives, pass board context between them, and verify consistency at the end.

## Trigger

Invoke when:
- User says `/build enablement-kit [topic]`
- User requests "build kit for [role] on [topic]"
- User requests multiple artifacts (deck + cheatsheet + one-pager) for the same initiative
- content-factory coordinator routes here when manifest includes 3+ artifact types

Do NOT invoke for single-artifact requests. Route those directly to the primitive.

## Source Material

Required:
- `strategy-contract.yaml` or `strategy.yaml` — from `/strategy`, content-factory handoff (Phase 4), or user-provided
- `knowledge.md` or research atoms — the knowledge base for this topic

**If invoked via content-factory handoff:** content-factory runs research + strategy before handing off. Expect `strategy-contract.yaml` and `knowledge.md` pre-seeded in `.pipeline/enablement-kit/`. If invoked directly by the user, prompt for or generate a strategy contract in Phase 0.

Optional:
- `_System/tailoring/hls-tailoring-map.yaml` — audience profiles (if HLS domain)
- `references/design-rules.md` — shared brand palette

## Phase 0: Assess Parallelization Opportunity

**CRITICAL: Use blackboard for multi-artifact kits (3+ artifacts).**

If the kit includes 3+ artifacts (deck + cheatsheet + one-pager, or any combination with enablement cards):
1. Count independent artifacts to render
2. If ≥3 artifacts → invoke `/blackboard` to parallelize artifact rendering
3. Each artifact becomes a board stream with dedicated agent
4. Board signals preserve artifact metadata for consistency check synthesis

**Example blackboard invocation:**
```
/blackboard Parallelize: render deck, render cheatsheet, render one-pager, render enablement-card-bdr

Synthesis format: artifact-metadata

Parent board: .pipeline/enablement-kit/
```

**Recursive nesting (max depth 3):**
- If deck agent discovers 50+ slides, invoke blackboard with `--nested` for parallel slide batch rendering
- Example: Deck with 80 slides → spawn nested blackboard for 4 agents (slides 1-20, 21-40, 41-60, 61-80)
- Deck-render skill already supports batch rendering coordination

**When NOT to use blackboard:**
- Single artifact request (deck only, cheatsheet only) → invoke primitive directly
- 2 artifacts where one is trivial (deck + enablement-card) → overhead may exceed benefit
- Artifacts with hard sequential dependencies (NOT the case here — proof point deconfliction happens via board signals)

**After blackboard completes:**
- Read synthesis from `.pipeline/enablement-kit/artifacts/SYNTHESIS.yaml`
- Extract artifact paths and metadata
- Proceed to Phase 5 (Cross-Artifact Consistency Check) using board signals from each artifact

**If NOT using blackboard (manual/small kits):**
- Proceed with sequential pipeline (Phases 1-4) as documented below

---

## Board Setup (Phase 0a)

### 0a. Create board directory

```
.pipeline/enablement-kit/
├── strategy-contract.yaml    ← copy or symlink from source, add _meta + version
├── invariants.yaml           ← you extract this in Phase 0
├── board/                    ← skill outputs land here
├── artifacts/                ← rendered files land here
└── failures.yaml             ← error log (create empty)
```

Create this structure using Write/Bash before proceeding.

### 0b. Seed the strategy contract with _meta

Read the source strategy YAML. Write it to `.pipeline/enablement-kit/strategy-contract.yaml` with these fields added at the top:

```yaml
_meta:
  board_dir: ".pipeline/enablement-kit/"
  coordinator: "enablement-kit"
  run_id: "{ISO timestamp}"
version: 1
amendments_log: []
# ... rest of original strategy fields ...
```

The `_meta.board_dir` field is how primitives discover they are in coordinated mode. Without it, they run standalone.

### 0c. Extract invariants

Read the strategy contract and extract shared constraints. Write to `.pipeline/enablement-kit/invariants.yaml`:

```yaml
hero_message: "{the single most important message — extract from strategy's headline or value_proposition}"
proof_points:
  - point: "{proof point 1}"
    source: "{attribution}"
    assigned_to: ["deck", "one-pager"]    # distribute, don't duplicate
    max_artifacts: 2
  - point: "{proof point 2}"
    source: "{attribution}"
    assigned_to: ["cheatsheet", "enablement-card"]
    max_artifacts: 2
  - point: "{proof point 3}"
    source: "{attribution}"
    assigned_to: ["deck", "cheatsheet"]
    max_artifacts: 2
  # ... distribute ALL proof points from strategy. Each appears in at most 2 artifacts.
competitive_frame:
  positioning: "{from strategy's competitive_analysis or positioning}"
  tone: "{from strategy's tone or infer: 'confident, not aggressive' for healthcare}"
call_to_action: "{unified CTA from strategy}"
audience_assumptions:
  - artifact_type: "deck"
    assumed_audience: "{from strategy — e.g., 'VP Engineering + CMIO'}"
    intentional: true
  - artifact_type: "cheatsheet"
    assumed_audience: "{from strategy — e.g., 'Field SA (mid-call reference)'}"
    intentional: true
  - artifact_type: "one-pager"
    assumed_audience: "{from strategy — e.g., 'same as deck (leave-behind)'}"
    intentional: true
  - artifact_type: "enablement-card"
    assumed_audience: "{from strategy — e.g., 'BDR (cold outreach)'}"
    intentional: true
# Deck mode per artifact (from strategy contract)
# Enables machine-verifiable audience coherence in Phase 5
deck_mode_per_artifact:
  - artifact_type: "deck"
    audience_class: "{from strategy deck_mode.audience_class for this artifact}"
    deck_class: "{persuasion|equipping}"
    arc_template: "{from strategy deck_mode.arc_template}"
    framing_style: "{loss|ease|recognition}"
  - artifact_type: "cheatsheet"
    audience_class: "{same as deck — cheatsheet is companion}"
    deck_class: "{same as deck}"
    arc_template: null  # Cheatsheets don't have arc templates
    framing_style: "{same as deck}"
  - artifact_type: "one-pager"
    audience_class: "{same as deck — leave-behind for same audience}"
    deck_class: "{same as deck}"
    arc_template: null  # One-pagers don't have arc templates
    framing_style: "{same as deck}"
  - artifact_type: "enablement-card"
    audience_class: "{from strategy — may differ, e.g., bdr_enablement}"
    deck_class: "{from strategy — may be equipping even if deck is persuasion}"
    arc_template: "{from strategy if applicable, else null}"
    framing_style: "{from strategy — may differ from deck}"
```

**`deck_mode_per_artifact` extraction rules:**

1. **Deck, cheatsheet, one-pager** typically share the same `audience_class` and `deck_class` because they're produced for the same meeting/audience. The cheatsheet is the mid-call companion; the one-pager is the leave-behind.

2. **Enablement cards** often target a different audience class than the deck. A kit might have a `customer`-class deck and a `bdr_enablement`-class enablement card. This is intentional — flag it as such.

3. If the strategy contract has a single `deck_mode` block (one audience for the whole program), apply it to all artifacts. If the strategy contract has per-artifact `deck_mode` blocks (because the manifest has multiple audiences), use the per-artifact values.

4. `arc_template` is only meaningful for deck artifacts. Set to `null` for cheatsheets, one-pagers, and enablement cards — they don't have narrative arcs in the deck-philosophy sense.

**Distribution rules for proof points:**
- Each proof point appears in at most 2 artifacts
- Deck gets the highest-impact points (presented visually)
- Cheatsheet gets the mid-call reference points (with "When to use" triggers)
- One-pager gets the standalone-comprehensible points (must work without presenter)
- Enablement card gets the role-specific points (BDR qualifying questions, AE objection counters)
- If the strategy has fewer than 4 proof points, some artifacts share — but never all 4 artifacts using the same point

## Pipeline Sequence

**Preferred mode (3+ artifacts):** Invoke blackboard (Phase 0) for parallel execution.
**Fallback mode (1-2 artifacts or blackboard unavailable):** Execute Phases 1-4 sequentially as documented below.

When running sequential mode, do not parallelize primitives — each reads the prior one's board output to avoid proof point duplication.

### Phase 1: Render Deck

The deck sets visual tone and locks the hero message rendering. It goes first.

**RECURSIVE NESTING (max depth 3):**
If deck agent discovers 50+ slides OR complex multi-section deck, invoke blackboard with `--nested` for parallel slide batch rendering.

Example recursive invocation:
```
/blackboard --nested

Parallelize: render slides 1-20, render slides 21-40, render slides 41-60, render slides 61-80

Synthesis format: artifact-metadata

Parent board: .pipeline/enablement-kit/
```

Deck-render skill already supports batch coordination — nested blackboard invocation delegates batch assembly.

**Sequential mode (fallback):**
1. Invoke `deck-render` with the strategy-contract.yaml (which contains `_meta.board_dir`)
   - The deck-render skill will read `_meta.board_dir`, find invariants.yaml, and honor it
   - It will write `board/deck-render-output.yaml` after completion
2. Read `board/deck-render-output.yaml`
3. **Quality gate**: Check `quality_pass`
   - If `true` → proceed to Phase 2
   - If `false` → **BLOCK**. Deck sets tone for entire kit. Do not proceed with a failing deck.
     - Retry: Re-invoke deck-render. Pass the failure notes as additional context.
     - Max retries: 1
     - If retry also fails → write to `failures.yaml` and STOP. Escalate to user: "Deck quality below threshold after retry. Fix deck before proceeding with kit."
4. Check `strategy_contract_amendments`. If any:
   - Merge amendments into `strategy-contract.yaml` (increment `version`, append to `amendments_log`)
   - Note: downstream skills will read the updated version

### Phase 2: Render Cheatsheet

The cheatsheet is the mid-call companion to the deck. It must complement, not repeat.

1. Invoke `cheatsheet-render` with the strategy-contract.yaml (contains `_meta.board_dir`)
   - cheatsheet-render will read invariants.yaml AND deck-render-output.yaml
   - It will avoid duplicating the deck's proof points
   - It will write `board/cheatsheet-render-output.yaml`
2. Read the board output
3. **V2 Quality Gate with Enrichment**:
   Check `quality_pass` (threshold: 15/20)
   - If `true` → proceed to Phase 3
   - If `false`:
     ```
     READ ALL board outputs written so far:
       - board/deck-render-output.yaml
       - {board_dir}/invariants.yaml

     CONSTRUCT enrichment_context:
       - deck's hero_message_as_rendered (match this exactly)
       - deck's proof_points_used (avoid these — use complementary ones)
       - deck's recommendations_for_downstream where target_skill = "cheatsheet-render"
       - The specific per_dimension_scores that fell below 2 (focus improvement there)

     RE-INVOKE cheatsheet-render with:
       - Original strategy-contract.yaml
       - enrichment_context as additional context
       - Specific failure notes: "Previous attempt scored {X}/20. Low dimensions: {list}. Improve these specifically."

     MAX 1 retry.
     IF retry also fails → produce with warnings, log to failures.yaml, continue
     ```
4. Merge any strategy amendments

### Phase 3: Render One-Pager

The one-pager is the leave-behind. It must stand alone without a presenter.

1. Invoke `one-pager-render` with the strategy-contract.yaml (which contains `_meta.board_dir`)
   - one-pager-render will read `_meta.board_dir`, find invariants.yaml, and honor it
   - It will read deck-render-output.yaml AND cheatsheet-render-output.yaml for proof point deconfliction
   - It will write `board/one-pager-render-output.yaml` after completion
2. Read `board/one-pager-render-output.yaml`
3. **V2 Quality Gate with Enrichment**:
   Check `quality_pass` (threshold: 18/24)
   - If `true` → proceed to Phase 4
   - If `false`:
     ```
     READ ALL board outputs written so far:
       - board/deck-render-output.yaml
       - board/cheatsheet-render-output.yaml
       - {board_dir}/invariants.yaml

     CONSTRUCT enrichment_context:
       - deck's hero_message_as_rendered + cheatsheet's hero_message_as_rendered (must match)
       - Combined proof_points_used from both (avoid all of these)
       - All recommendations_for_downstream where target_skill = "one-pager-render"
       - The specific per_dimension_scores that fell below 2

     RE-INVOKE one-pager-render with:
       - Original strategy-contract.yaml
       - enrichment_context as additional context
       - Specific failure notes: "Previous attempt scored {X}/24. Low dimensions: {list}. Improve these specifically."

     MAX 1 retry.
     IF retry also fails → produce with warnings, log to failures.yaml, continue
     ```
4. Check `standalone_comprehension` and `forwarding_meta_test` — log warnings if either is false
5. Check `strategy_contract_amendments`. If any:
   - Merge amendments into `strategy-contract.yaml` (increment `version`, append to `amendments_log`)

### Phase 4: Render Enablement Card(s)

Role-specific job aids. May produce multiple variants (BDR, AE, SA).

1. For each role variant in the strategy:
   a. Invoke `enablement-card-render` with the strategy-contract.yaml (which contains `_meta.board_dir`)
      - enablement-card-render will read `_meta.board_dir`, find invariants.yaml, and honor it
      - It will read ALL prior board outputs (deck, cheatsheet, one-pager) for proof point deconfliction
      - It will write `board/enablement-card-render-{role}-output.yaml` after completion
   b. Read `board/enablement-card-render-{role}-output.yaml`
   c. **V2 Quality Gate with Enrichment** per variant: Check `quality_pass` (threshold: 15/20)
      - If `true` → proceed to next variant
      - If `false`:
        ```
        READ ALL board outputs: deck, cheatsheet, one-pager outputs + invariants.yaml
        CONSTRUCT enrichment_context with all prior hero messages, proof points,
          competitive frames, and recommendations_for_downstream where target_skill = "enablement-card-render"
        RE-INVOKE enablement-card-render with enrichment + failure notes
        MAX 1 retry per variant.
        IF retry fails → skip this variant, log to failures.yaml
        ```
   d. Check `anti_patterns_detected` — log warnings if any detected
   e. Check `strategy_contract_amendments`. If any, merge into strategy-contract.yaml
2. After all variants complete, proceed to Phase 5

### Phase 5: Cross-Artifact Consistency Check

This is the killer feature of the enablement-kit coordinator. It catches the inconsistencies that standalone rendering misses.

1. Read ALL board output files:
   - `board/deck-render-output.yaml`
   - `board/cheatsheet-render-output.yaml`
   - `board/one-pager-render-output.yaml` (primitive — always writes directly, no adapter)
   - `board/enablement-card-render-{role}-output.yaml` (or adapter entries)

2. Check 5 invariants:

   **a. Hero Message Consistency**
   Compare `hero_message_as_rendered` across all outputs using the rubric in `.pipeline/schemas/README.md → Hero Message Semantic Equivalence Rubric`.
   - PASS: All match exactly OR are semantic equivalents (same metric, same direction, same subject)
   - FAIL: Different numbers, different claims, or contradictory framing

   **b. Proof Point Distribution**
   Collect `proof_points_used` from all outputs.
   - PASS: No proof point appears in more than 2 artifacts (per invariants.yaml assignment)
   - FAIL: Same proof point in 3+ artifacts = duplication, not distribution

   **c. Competitive Frame Consistency**
   Compare `competitive_frame_as_rendered` across all outputs.
   - PASS: Same positioning, same tone
   - FAIL: Different competitors emphasized, contradictory claims

   **d. CTA Consistency**
   Check that call-to-action is unified.
   - PASS: All artifacts point to the same next step
   - FAIL: Deck says "schedule demo", cheatsheet says "request trial" = confusion

   **e. Audience Assumption Coherence**
   Two-level check using both free-text `audience_assumptions` and structured `deck_mode_per_artifact` from invariants.yaml.

   **Level 1 (structured):** Compare `deck_mode_per_artifact` entries.
   - Same-audience artifacts (deck, cheatsheet, one-pager) must have identical `audience_class` and `deck_class`.
   - Different-audience artifacts (e.g., enablement-card with `bdr_enablement` while deck is `customer`) must be flagged as `intentional: true` in `audience_assumptions`.
   - If two artifacts have different `framing_style` values without an intentional flag → FAIL.

   **Level 2 (semantic):** Cross-reference free-text `assumed_audience` from `audience_assumptions` with what each artifact actually produced.
   - PASS: Intentional audience differences are documented AND deck_mode values are consistent within same-audience groups.
   - FAIL: Two artifacts in the same audience group have different `audience_class` or `deck_class` values — this is an unintentional mismatch.
   - FAIL: Different-audience artifacts are not flagged as intentional.

3. Write `board/consistency-check.yaml`:

```yaml
checked_at: "{ISO timestamp}"
artifacts_checked:
  - deck-render
  - cheatsheet-render
  - one-pager-render
  - enablement-card-{role}
results:
  hero_message: { pass: true, notes: "" }
  proof_point_distribution: { pass: true, notes: "" }
  competitive_frame: { pass: true, notes: "" }
  cta_consistency: { pass: true, notes: "" }
  audience_coherence: { pass: true, notes: "" }
overall_pass: true
failures: []         # list of { criterion, artifact, details } for any failures
```

4. **V2 Smart Re-Render with Blast Radius Analysis**:

If `overall_pass` is false:

```
READ board/consistency-check.yaml → failures[]

FOR each failure:
  IDENTIFY divergent artifact(s)
  CALCULATE blast_radius:
    deck → 3 (everything reads deck output)
    cheatsheet → 2 (one-pager, enablement-card)
    one-pager → 1 (enablement-card)
    enablement-card → 0 (nothing downstream)

  SORT by blast_radius ASCENDING

  SPECIAL CASE: If deck diverged on hero_message:
    DO NOT re-render deck (it set the tone, it's probably right)
    INSTEAD: Re-render the OTHER artifact(s) to match the deck's hero_message
    This is the "deck is authoritative" rule

  FOR each divergent artifact (lowest blast_radius first):
    RE-RENDER with:
      - strategy-contract.yaml
      - ALL non-divergent board outputs as enrichment
      - Explicit constraint: "Your {criterion} must match: {correct value from authoritative artifact}"
    MAX 1 re-render per artifact

  AFTER re-renders:
    RE-RUN full consistency check (all 5 criteria)
    IF all pass → proceed to Phase 5.5
    IF still failing → **BLOCK**. Escalate to user with remaining mismatches.
```

**Key difference from content-factory**: enablement-kit BLOCKS on consistency failure (it's the kit-level quality gate). Content-factory logs and continues.

### Phase 5.5: Upload to Google Workspace (conditional, adapter)

**Skip condition:** If no Google Workspace skills are available (test via gcloud auth), skip this phase.

After all artifacts pass the consistency check, upload them to Google Workspace for collaborative review:

1. **Deck → Google Slides:**
   - Invoke `google-slides` skill with the rendered .pptx
   - Capture: presentation_url, presentation_id, slide_count
   - Write adapter board entry (see Fe-Vibe Adapter Protocol below)

2. **One-pager + Cheatsheet → Google Docs:**
   - For each document artifact (.html or .pdf):
     - Invoke `google-docs` skill to create/update a Google Doc
     - Capture: doc_url, doc_id, version, content_hash
     - Write adapter board entry

3. **Enablement Cards → Google Docs:**
   - For each role variant card:
     - Invoke `google-docs` skill
     - Capture same fields
     - Write adapter board entry

4. **Report upload results:**
   - Count successful uploads vs failures
   - If any upload fails: log to failures.yaml, continue (non-blocking — local artifacts are the source of truth)

### Phase 6: Archive Board

After all artifacts pass and consistency check passes:

1. Copy all artifacts from `.pipeline/enablement-kit/artifacts/` to the user's delivery directory
2. Move `.pipeline/enablement-kit/` to `.pipeline/completed/enablement-kit-{timestamp}/`
3. Present summary to user

## Output

After all phases complete:

```
ENABLEMENT KIT COMPLETE
=======================
Board: .pipeline/completed/enablement-kit-{timestamp}/
Artifacts:
  - Deck: {path} ({N} slides, quality {score}/{max})
  - Cheatsheet: {path} ({N} cards, quality {score}/{max})
  - One-Pager: {path} (quality {score}/{max})
  - Enablement Card [{role}]: {path} (quality {score}/{max})

Consistency Check: PASS
  - Hero message: consistent across {N} artifacts
  - Proof points: {N} distributed, 0 over-duplicated
  - Competitive frame: consistent
  - CTA: unified
  - Audience: coherent (intentional differences documented)

Strategy Amendments Applied: {N}
  {list of amendments}

Failures/Warnings: {N}
  {list from failures.yaml}
```

## Supervision Tree

For staleness detection (skills that don't produce board output within expected turns), see `.pipeline/schemas/README.md → Skill Invocation Timeout Guidance`.

| Primitive | Threshold | Retry | Degrade | Escalate |
|-----------|-----------|-------|---------|----------|
| deck-render | Per-slide CLEAN | 1 retry with enriched context | **BLOCK** — deck sets tone | Stop pipeline, ask user |
| cheatsheet-render | 15/20 rubric | 1 retry with deck-output context | Produce with warnings, continue | Log to failures.yaml |
| one-pager-render | 18/24 rubric | 1 retry with all prior context | Produce with warnings, continue | Log |
| enablement-card-render | 15/20 per role | 1 retry per role variant | Skip failing variant | Log skipped variants |
| Consistency check | All 5 criteria | Re-render divergent artifact (1x) | **BLOCK** — inconsistent kit damages credibility | Stop, show mismatches to user |

**Two BLOCKING failure modes**: deck quality and consistency check. Everything else degrades gracefully.

## Fe-Vibe Adapter Protocol

Fe-vibe skills (google-docs, google-slides) cannot write to the board. When this coordinator invokes them, it captures the output and writes a board entry on their behalf.

### google-slides Adapter

**When invoked:** Phase 5.5, after deck passes consistency check.

**Capture from skill output:**
- `presentation_url` — the Google Slides URL
- `presentation_id` — the Slides ID
- `slide_count` — number of slides uploaded

**Write to:** `{board_dir}/board/google-slides-output.yaml`

```yaml
skill_name: "google-slides"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "enablement-kit"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  presentation_url: ""
  presentation_id: ""
  slide_count: N
  source_artifact: "{path to .pptx}"

quality_assessment: "Upload successful — slides match source deck"
quality_pass: true/false
```

### google-docs Adapter

**When invoked:** Phase 5.5, for one-pager, cheatsheet, and enablement cards.

**Capture from skill output:**
- `doc_url` — the Google Docs URL
- `doc_id` — the Docs ID
- `version` — document version
- `content_hash` — hash of uploaded content for change detection

**Write to:** `{board_dir}/board/google-docs-{artifact-type}-output.yaml` (one per artifact)

```yaml
skill_name: "google-docs"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "enablement-kit"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  doc_url: ""
  doc_id: ""
  version: N
  content_hash: ""
  source_artifact: "{path to source .html/.pdf}"
  artifact_type: "{one-pager|cheatsheet|enablement-card-bdr|enablement-card-ae|etc.}"

quality_assessment: "Upload successful — content matches source"
quality_pass: true/false
```
