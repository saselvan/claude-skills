# Demo-Narrative Skill — Grill-Me Agreements

14 decisions + 2 gap resolutions. This is the complete spec for building the skill.

## Decision 1: Architecture

One act-generation pipeline, three methodology "lenses" (Cohan, Demo2Win, Challenger).

- Three DISTINCT opening act generators (different generation logic, not just different prompts)
- Shared pipeline after the opening act
- Nesting depth as a parameter (for Demo2Win's Tell-Show-Tell recursion)

**Cohan open:** Generate rendered end-state, narrate backward. Requires completed outcome artifact.
**Demo2Win open:** Generate problem statement grounded in customer's stated pain. Requires discovery inputs.
**Challenger open:** Generate commercial reframe — non-obvious insight contradicting buyer's current framing. Requires domain knowledge + contrast logic. SA MUST supply `current_buyer_frame` before generation.

## Decision 2: Input Tiers

Three-tier input resolution:

- **Tier 1**: DEMO_SPEC.md with structured wow moments → extract + supplement with 2 sales-context questions
- **Tier 1.5**: DEMO_SPEC.md with inline prose script → parse + restructure, then same 2 questions
- **Tier 2**: No spec → read README + routes + any prose → 5-question compressed discovery → generate with confidence flagging

Tier 2 outputs flagged with `[INFERRED — confirm before use]` on wow moments and outcome statements. Make confidence level visible so SA knows what to validate.

## Decision 3: acts.json Schema

Superset schema, single file. Backward-compatible with existing Clinical VA format.

Top-level `schemaVersion` field. Remotion ignores unknown fields.

Fields per act:
```json
{
  "act": "context",
  "label": "Setting the Stage",
  "startMs": 0,
  "durationTargetSec": 45,
  "chapters": ["intro", "clean-slate"],
  "narration": "...",
  "wowMoment": false,
  "wowSource": "spec | methodology",
  "screenState": "dashboard-empty",
  "methodology": "cohan",
  "inferredConfidence": "spec-derived | inferred"
}
```

**Gap Resolution 1 — startMs:** Must be numeric `0`, not `null`. Remotion `Sequence` requires number. `null` coerces silently (masks bugs), `undefined` produces NaN (crashes `from=`). Remotion pass overwrites with real timestamps post-render.

Top-level fields:
```json
{
  "schemaVersion": 1,
  "methodology": "cohan",
  "voiceId": "default-kokoro",
  "invariantOverrides": [...],
  "acts": [...]
}
```

## Decision 4: YAML Scaffold for Demo-Machine

Emit chapter scaffold with:

1. **CHAPTER INTENT** comment block at top of each chapter — one sentence describing what viewer should understand. SA-facing framing that survives narration rewrites.

2. **AUTOMATION REQUIRED** comment block:
```yaml
# AUTOMATION REQUIRED:
#   1. Add navigate/click/type/press steps before each wait block
#   2. Add bare wait steps (no narration) after actions that trigger async UI changes
#   3. Validate selector targeting against live app before full run
#   4. Run `demo-machine validate` before `demo-machine run`
```

3. Narration on `wait` steps with approximate timeouts (~15 chars/sec + 1500ms buffer for Kokoro). These are human-readable hints, not precise calculations — demo-machine's `adjustTiming` handles real audio sync at runtime.

4. **Gap Resolution 2 — voiceId:** Demo-level `voiceId` field in YAML, overridable per chapter. Added now before multi-voice demos require migration.

Example scaffold:
```yaml
meta:
  voiceId: "default-kokoro"

chapters:
  - name: morning_briefing
    voiceId: null  # inherits from meta
    # CHAPTER INTENT: Viewer sees the agent running autonomously and surfacing
    # the right patient flags without manual input.
    # AUTOMATION REQUIRED:
    #   1. Add navigate/click/type/press steps before each wait block
    #   2. Add bare wait steps (no narration) after actions that trigger async UI changes
    #   3. Validate selector targeting against live app before full run
    #   4. Run `demo-machine validate` before `demo-machine run`
    steps:
      - wait:
          timeout: 4200
          narration: "Watch what happens when the agent runs its morning briefing..."
      # TODO: click agent trigger button
      # TODO: wait 3000ms for API response
      - wait:
          timeout: 3800
          narration: "In production this fires at 5 AM via Lakeflow..."
```

## Decision 5: Wow Moment Ownership

- **Consume** existing wow moments from DEMO_SPEC.md's `## Wow Moments` section
- **Augment** with methodology-derived narrative wow moments (Challenger reframe beat, Cohan money shot reveal, Demo2Win reinforcement callback)
- **Tag each** with `wowSource: "spec"` vs `wowSource: "methodology"`
- Methodology wow moments are spoken moments (not UI interactions) — excluded from Phase 4.5 "all wow moments have code paths" verification gate

## Decision 6: Decision Matrix

4-rule hardcoded decision table. Produces single recommendation with rationale string. User confirms via AskUserQuestion.

```
IF competitive_pressure == high AND criteria_already_shaped == true
  → Challenger ("Reframe needed — buyer's criteria shaped by {competitor}")

ELIF repeat_demo == true
  → Demo2Win ("Skip to unvalidated modules — buyer has seen the outcome")

ELIF audience == executive OR format == recorded
  → Cohan ("Outcome-first for time-constrained/visual-first context")

ELSE
  → Demo2Win ("Structured walkthrough for technical/evaluation context")
```

`criteria_already_shaped` = "Is the buyer evaluating against a specific competitor or using criteria that competitor defined?" Yes/no from SA's pre-call notes.

`repeat_demo` = Is this a second or third demo to the same buyer?

## Decision 7: Challenger Reframe Validation

When `methodology == challenger`:

1. **SA supplies `current_buyer_frame` BEFORE generation** — blocking input. If empty, skill asks for it. Does not generate without it.

Input field label: "What does *this buyer specifically* believe today, based on your discovery calls?"

2. **4-field validation block** checks against SA-supplied ground truth:
```markdown
### Reframe Validation
- **Supplied buyer frame:** [echoed from SA input — not generated]
- **Reframe insight:** [generated — contradicts the supplied frame?]
- **Adequacy gap exposed:** [generated — does this follow from the insight?]
- **Frame used in opening:** yes / no / partial
```

SA verifies the bottom field. "Partial" or "no" → regenerate. Five-second check.

Remaining failure mode (weak/generic SA-supplied frame) is a discovery quality problem, not a generation quality problem. The skill can't fix it.

## Decision 8: Demo2Win Nesting

Depth 2 maximum, enforced structurally (not configurable).

**Schema enforcement:** `parentAct` may only reference an act with no `parentAct` itself. A sub-act cannot be a parent. One validation rule hard-caps depth at 2.

Additional fields on sub-acts:
- `parentAct`: references the container act's ID
- `moduleIndex`: zero-based ordering within parent (for reconstruction without relying on array position)

Container acts get:
- `isContainer: true` — downstream tools know not to expect narration or chapter content

```json
{
  "act": "show",
  "label": "Product Walkthrough",
  "isContainer": true,
  "methodology": "demo2win"
}
```

```json
{
  "act": "show-module-a",
  "label": "Charge Capture Gap Detection",
  "parentAct": "show",
  "moduleIndex": 0,
  "methodology": "demo2win",
  "narration": "Here's where the charge capture team loses 4 hours every day...",
  "durationTargetSec": 90,
  "wowMoment": true,
  "chapters": ["charge-gap-detection"]
}
```

## Decision 9: Output Locations

Adaptive 3-tier resolution:

1. **Board exists** (`.pipeline/demo-factory/`) → write to `artifacts/narrative/` per board protocol
2. **Demo repo detected** (`~/repos/{name}/` exists) → narrative artifacts to `~/repos/{name}/demo-narrative/`, YAML scaffold to `~/repos/{name}/demos/`
3. **Neither** → create `.pipeline/demo-narrative/{demo-name}/` (log visibly — something probably wrong with invocation)

**Scaffold placement rule:** YAML scaffold goes to `demos/{name}.demo.yaml` (where `demo-machine run` looks). Filename matches demo-machine naming convention exactly.

**Draft naming for collision avoidance:** Before writing to `demos/`, check for existing `.demo.yaml`. If exists:
- Write to `demos/{name}.draft.demo.yaml`
- Surface warning: `⚠ Existing YAML detected at demos/{name}.demo.yaml — Scaffold written to demos/{name}.draft.demo.yaml — Review and merge manually`

**Per-artifact announcement format:**
```
Artifacts written:
  acts.json        → ~/repos/clinical-va/demo-narrative/acts.json
  demo-script.md   → ~/repos/clinical-va/demo-narrative/demo-script.md
  YAML scaffold    → ~/repos/clinical-va/demos/clinical-va.draft.demo.yaml
                     ⚠ Draft — existing YAML preserved at clinical-va.demo.yaml
```

## Decision 10: demo-script.md Structure

```markdown
# Demo Narrative: {demo-name}
## Methodology: {lens} — {one-line rationale}

## Context
- **Audience:** {seniority + role}
- **Sales stage:** {stage}
- **Competitive context:** {competitor/none}
- **Format:** {live / recorded / self-service}
- **Total target duration:** {X minutes}

## Reframe Validation  ← (Challenger only)
- **Supplied buyer frame:** ...
- **Reframe insight:** ...
- **Adequacy gap:** ...
- **Frame used in opening:** yes/no/partial

## Act Structure
| Act | Label | Duration | Wow? | Screen State |
|-----|-------|----------|------|-------------|
| 1   | ...   | 45s      | no   | dashboard   |
| 2   | ...   | 90s      | YES  | agent-run   |

## Scripts

### Act 1: {label}
> **CHAPTER INTENT:** {what the viewer should understand}

[PRESENTER: {setup note — read the room, set expectations}]

**Script:** (for live) / **Narration:** (for recorded)
[For live: sub-note: "Adapt for live delivery — this is a guide, not a teleprompter"]

> "{Exact narration text}"

[PRESENTER: {inline note — pause, watch for reaction}]

> "{More narration}"

[PRESENTER: {post-delivery note — listen for objection, transition trigger}]

**Transition:** "{bridge line to next act}"

---

## Discovery Prompts
| Act | Prompt | Purpose |
|-----|--------|---------|
| 1   | "How are you handling X today?" | Validate pain |
| 3   | "What happens when Y fails?" | Quantify impact |

Discovery prompts: {N} placed (Act 1: {n}, Act 2: {n}, Act 3: {n})
[Warning if all in same act]

## Objection Flags
| Objection | One-Line Response |
|-----------|-------------------|
| "We already do X with {competitor}" | "{response}" |
| "Can it handle our scale?" | "{response}" |
```

Presenter notes are POSITIONAL:
- Above narration: setup, read the room
- Inline with narration: pause, watch for reaction
- Below narration: transition trigger, listen for objection

## Decision 11: Pipeline Position

**Phase 3.5** (after spec, before build). Spec → narrative dependency at runtime.

Narrative consumes spec (wow moments, persona-to-view mappings, UI route table). Spec's thin Talk Track is generated first and overwritten by narrative when present.

**Board entry:**
```yaml
phase: 3.5
skill: demo-narrative
input: DEMO_SPEC.md + {name}-research.md + brainstorm board entry
output: acts.json + demo-script.md + {name}.draft.demo.yaml
writes: .pipeline/demo-factory/artifacts/narrative/
```

Mandatory stop after Phase 3 (spec) before Phase 3.5 (narrative).

The indirect influence (narrative improving spec template) operates at design time, not runtime — improve the spec's wow moment format once, every future narrative run benefits. Not a phase ordering change.

## Decision 12: HLS Quality Gates

### #31 — Show End Result First
Machine-readable invariant override in acts.json when methodology deviates:
```json
"invariantOverrides": [
  {
    "invariant": 31,
    "status": "intentional-deviation",
    "rationale": "Challenger methodology — outcome appears in Act 3, not Act 1",
    "actWithOutcome": "act-3"
  }
]
```
Phase 4.5 reads `intentional-deviation` and skips the #31 check.

### #35 — Discovery First
Distribute discovery prompts across acts, not front-loaded:
```
Discovery prompts: 3 placed (Act 1: 1, Act 2: 1, Act 3: 1) ✓
```
If all three land in same act, surface warning.

### #39 — Persona-Narration Alignment (NEW, owned by demo-narrative)
Every act's narration must reference at least one named persona from the spec. Narration that describes features without anchoring to who cares and why is selling to no one. Checked mechanically at generation time.

## Decision 13: Invocation & Iteration

### Command surface (v1):
```
/demo-narrative {demo-name}                          # interactive, full questions
/demo-narrative {demo-name} [flags]                  # flags override, gaps trigger questions
/demo-narrative {demo-name} --recommend-only         # matrix output only, no generation
```

### Flags:
- `--methodology cohan|demo2win|challenger` — skip matrix, still asks for `current_buyer_frame` if challenger
- `--audience executive|technical|mixed`
- `--stage discovery|scoping|evaluation|onboarding`
- `--format live|recorded|self-service`
- `--recommend-only` — runs decision matrix, prints recommendation with rationale, exits

### Iteration:
**v1: Regeneration only.** `/demo-narrative {name}` again with adjusted inputs. No edit mode.

**Reserved for v2:** `/demo-narrative iterate {name}` — reads existing output, applies targeted feedback.

**Logging:** When SA regenerates, capture `regeneration_reason` in board entry. After 10-15 demos, use distribution of feedback types to design v2 iteration mode against real patterns.

## Decision 14: TTS Timing

Approximate `timeout` values as human-readable pacing hints. Formula: `chars / 15 * 1000 + 1500` (Kokoro default).

Demo-machine does NOT estimate TTS from character count. At recording time it synthesizes audio, gets exact duration from WAV buffer, and `timing.js` positions segments with overlap prevention. The `timeout` in YAML is a playback constraint (how long browser waits), not a TTS duration estimate.

The skill doesn't need provider-specific rates or shared constants with demo-machine. Reasonable defaults for YAML readability. Demo-machine handles precise sync at runtime.

## Gap Resolution 2: voiceId Field

`voiceId` at demo level in YAML scaffold, overridable per chapter. Added now before multi-voice demos require migration.

```yaml
meta:
  voiceId: "default-kokoro"

chapters:
  - name: morning_briefing
    voiceId: null  # inherits from meta
```
