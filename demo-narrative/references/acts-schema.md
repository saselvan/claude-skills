# acts.json Schema Reference

Source of truth for the acts.json file format. Derived from grill-me agreements: Decision 3 (schema), Decision 5 (wowSource), Decision 8 (Demo2Win nesting), Decision 12 (invariantOverrides), Gap Resolution 1 (startMs).

Remotion ignores unknown fields. The schema is a superset — every methodology uses the same file, methodology-specific fields are simply absent when not applicable.

---

## Top-Level Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `schemaVersion` | `number` | Yes | Schema version. Current: `1`. Consumers check this before parsing. |
| `methodology` | `string` | Yes | Which narrative lens generated this file. One of: `"cohan"`, `"demo2win"`, `"challenger"`. |
| `voiceId` | `string` | Yes | TTS voice identifier for the demo. Default: `"default-kokoro"`. Per-chapter overrides live in the YAML scaffold, not here. |
| `invariantOverrides` | `array` | No | Explicit deviations from HLS quality invariants (e.g., #31). Omit entirely when no deviations exist. See [invariantOverrides Schema](#invariantoverrides-schema). |
| `acts` | `array` | Yes | Ordered array of act objects. Minimum 1 act. |

```json
{
  "schemaVersion": 1,
  "methodology": "cohan",
  "voiceId": "default-kokoro",
  // omit invariantOverrides when no overrides; see Omission Rules below
  "acts": []
}
```

---

## Per-Act Fields

Every act object supports the following fields. Fields marked methodology-specific are only present when that methodology generates the acts.

| Field | Type | Required | Description |
|---|---|---|---|
| `act` | `string` | Yes | Act identifier. Unique within the file. Used as reference target for `parentAct`. Examples: `"context"`, `"show"`, `"show-module-a"`, `"reframe"`. |
| `label` | `string` | Yes | Human-readable act title. Appears in demo-script.md act structure table. Examples: `"Setting the Stage"`, `"Product Walkthrough"`. |
| `startMs` | `number` | Yes | Start time in milliseconds. **Must be numeric `0` for the first act. Never `null`, never `undefined`.** See [startMs Rules](#startms-rules). |
| `durationTargetSec` | `number` | Yes* | Target duration in seconds. Approximate — demo-machine adjusts at runtime. *Omit only on container acts (`isContainer: true`), which have no direct content. |
| `chapters` | `array<string>` | Yes* | Chapter names mapping to YAML scaffold chapters. *Omit only on container acts. |
| `narration` | `string` | Yes* | Full narration text for the act. *Omit only on container acts. |
| `wowMoment` | `boolean` | Yes | Whether this act contains a wow moment. `true` triggers Phase 4.5 verification for spec-sourced wow moments. |
| `wowSource` | `string` | Conditional | Required when `wowMoment: true`. See [wowSource Semantics](#wowsource-semantics). One of: `"spec"`, `"methodology"`. |
| `screenState` | `string` | Yes* | UI state visible during this act. Maps to Remotion scene composition. Examples: `"dashboard-empty"`, `"agent-run"`, `"results-table"`. *Omit only on container acts. |
| `methodology` | `string` | Yes | Redundant with top-level field for flat schemas, but required for nested Demo2Win where container and sub-acts share the same methodology tag. Always matches top-level `methodology`. |
| `inferredConfidence` | `string` | Conditional | Present when input tier is Tier 2 (no DEMO_SPEC.md). See [inferredConfidence Semantics](#inferredconfidence-semantics). One of: `"spec-derived"`, `"inferred"`. |
| `parentAct` | `string` | Conditional | Demo2Win only. References the container act's `act` field. See [Demo2Win Nesting Rules](#demo2win-nesting-rules). |
| `moduleIndex` | `number` | Conditional | Demo2Win only. Zero-based ordering within the parent container. See [Demo2Win Nesting Rules](#demo2win-nesting-rules). |
| `isContainer` | `boolean` | Conditional | Demo2Win only. `true` marks this act as a grouping container. Container acts have no `narration`, `chapters`, `durationTargetSec`, or `screenState`. See [Demo2Win Nesting Rules](#demo2win-nesting-rules). |

---

## startMs Rules

**Source:** Gap Resolution 1.

Remotion's `<Sequence from={startMs}>` requires a numeric value. The first act's `startMs` must be `0`.

| Value | Behavior | Verdict |
|---|---|---|
| `0` (numeric) | Remotion positions correctly | Correct |
| `null` | JavaScript coerces silently — `from=0` works by accident, masks bugs downstream | Forbidden |
| `undefined` / missing | Produces `NaN` — crashes Remotion's `from=` prop | Forbidden |
| Negative number | Nonsensical — Remotion clips to 0 but intent is unclear | Forbidden |

**Subsequent acts:** `startMs` values are placeholder zeros at generation time. The Remotion pass overwrites them with real timestamps after audio synthesis. The generation pipeline writes `0` for all acts; it does not attempt timing calculation.

---

## wowSource Semantics

**Source:** Decision 5.

Every act with `wowMoment: true` must declare where the wow moment originated.

| Value | Meaning | Phase 4.5 Gate |
|---|---|---|
| `"spec"` | Wow moment was consumed from DEMO_SPEC.md's `## Wow Moments` section. It represents a UI interaction or feature demonstration. | **Included** in "all wow moments have code paths" verification. Must have a corresponding automation step in the YAML scaffold. |
| `"methodology"` | Wow moment was generated by the narrative methodology. It is a spoken moment — a Challenger reframe beat, a Cohan money-shot reveal, or a Demo2Win reinforcement callback. Not a UI interaction. | **Excluded** from Phase 4.5 code path verification. These are narration-only moments with no automation dependency. |

---

## inferredConfidence Semantics

**Source:** Decision 2 (Input Tiers).

Present only when the skill operated in Tier 2 mode (no DEMO_SPEC.md provided). Signals how much the SA should trust each act's content.

| Value | Meaning | SA Action |
|---|---|---|
| `"spec-derived"` | Content was extracted or directly informed by structured spec inputs (Tier 1 or Tier 1.5). High confidence. | Use as-is. |
| `"inferred"` | Content was generated from README, routes, or compressed discovery. The skill inferred wow moments and outcome statements without explicit spec confirmation. | Marked with `[INFERRED -- confirm before use]` in demo-script.md. SA must validate before delivery. |

When `inferredConfidence` is absent, the act was generated from a spec (Tier 1 / Tier 1.5) and confidence is implicitly high.

---

## Demo2Win Nesting Rules

**Source:** Decision 8.

Demo2Win methodology uses Tell-Show-Tell structure where the "Show" phase contains multiple product modules. This creates parent-child relationships between acts.

### Depth Enforcement

**Maximum depth: 2. Hard-enforced, not configurable.**

- Depth 1: Top-level acts (no `parentAct`). These include container acts and standalone acts.
- Depth 2: Sub-acts (have `parentAct`). These are the leaf nodes with actual narration and chapters.

**Validation rule:** `parentAct` may only reference an act that has no `parentAct` itself. A sub-act cannot be a parent. If any act has a `parentAct` that itself has a `parentAct`, the schema is invalid.

```
VALID:
  show (depth 1, isContainer: true)
    show-module-a (depth 2, parentAct: "show")
    show-module-b (depth 2, parentAct: "show")

INVALID:
  show (depth 1, isContainer: true)
    show-module-a (depth 2, parentAct: "show")
      show-module-a-detail (depth 3, parentAct: "show-module-a")  <-- REJECTED
```

### Container Acts

A container act groups sub-acts but carries no content of its own.

| Field | Value | Notes |
|---|---|---|
| `isContainer` | `true` | Signals downstream tools to skip narration/chapter rendering for this act |
| `narration` | absent | Container has no spoken content |
| `chapters` | absent | Container maps to no YAML chapters |
| `durationTargetSec` | absent | Duration is the sum of child acts |
| `screenState` | absent | No direct UI state |
| `wowMoment` | absent | Wow moments live on sub-acts, not containers |

### Sub-Act Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `parentAct` | `string` | Yes | Must match the `act` field of a container act. The referenced act must have `isContainer: true` and no `parentAct` of its own. |
| `moduleIndex` | `number` | Yes | Zero-based index for ordering within the parent. Exists so reconstruction does not depend on array position — a consumer can sort sub-acts by `moduleIndex` regardless of JSON array order. |

All other standard act fields (`narration`, `chapters`, `durationTargetSec`, `screenState`, `wowMoment`, etc.) are required on sub-acts as they are leaf nodes with real content.

---

## invariantOverrides Schema

**Source:** Decision 12.

When a methodology intentionally deviates from an HLS quality gate invariant, the deviation is declared machine-readably. Phase 4.5 reads `"intentional-deviation"` status and skips the corresponding check.

### Structure

`invariantOverrides` is a top-level array. Each element is an object:

| Field | Type | Required | Description |
|---|---|---|---|
| `invariant` | `number` | Yes | The invariant number being overridden (e.g., `31` for "Show End Result First"). |
| `status` | `string` | Yes | Always `"intentional-deviation"`. No other status values are currently defined. |
| `rationale` | `string` | Yes | Human-readable explanation of why this methodology deviates from the invariant. Must reference the methodology by name and explain the structural reason. |
| `actWithOutcome` | `string` | Conditional | For invariant #31 specifically: which act contains the outcome that would normally appear in Act 1. References an `act` field value. |

### When to Use

| Invariant | Methodology | Deviation | Override Required? |
|---|---|---|---|
| #31 (Show End Result First) | Cohan | No deviation — Cohan shows outcome first by definition | No |
| #31 (Show End Result First) | Demo2Win | Outcome appears in Tell-2 (final tell), not opening | Yes |
| #31 (Show End Result First) | Challenger | Outcome appears after reframe + show, typically Act 3 | Yes |
| #35 (Discovery First) | All | No deviation expected — discovery prompts distributed across acts | No (but warn if all prompts cluster in one act) |

### Omission Rule

If no invariants are overridden, omit the `invariantOverrides` field entirely. Do not include an empty array — its absence signals "no deviations."

---

## Example: Flat Cohan acts.json

Cohan methodology — outcome-first, no nesting. All acts are flat (depth 1). No invariant overrides because Cohan naturally satisfies #31.

```json
{
  "schemaVersion": 1,
  "methodology": "cohan",
  "voiceId": "default-kokoro",
  "acts": [
    {
      "act": "outcome",
      "label": "The End State",
      "startMs": 0,
      "durationTargetSec": 30,
      "chapters": ["outcome-reveal"],
      "narration": "This is where we end up. The care team sees every flag resolved, every protocol matched, every patient on track. Zero manual chart review. Let me show you how we got here.",
      "wowMoment": true,
      "wowSource": "methodology",
      "screenState": "dashboard-complete",
      "methodology": "cohan"
    },
    {
      "act": "context",
      "label": "Setting the Stage",
      "startMs": 0,
      "durationTargetSec": 45,
      "chapters": ["intro", "clean-slate"],
      "narration": "But first, here's where most teams start their day. Thirty open charts. No prioritization. The nurse manager is triaging by memory.",
      "wowMoment": false,
      "screenState": "dashboard-empty",
      "methodology": "cohan"
    },
    {
      "act": "build",
      "label": "Building Toward the Outcome",
      "startMs": 0,
      "durationTargetSec": 90,
      "chapters": ["agent-config", "first-run", "flag-detection"],
      "narration": "The clinical agent runs its morning briefing. It reads overnight vitals, lab results, and nursing notes. Watch — it flags three patients the care team would have missed until rounds.",
      "wowMoment": true,
      "wowSource": "spec",
      "screenState": "agent-run",
      "methodology": "cohan"
    },
    {
      "act": "payoff",
      "label": "Full Circle",
      "startMs": 0,
      "durationTargetSec": 40,
      "chapters": ["resolution"],
      "narration": "And now we're back to where we started — but this time you've seen every step. That dashboard isn't magic. It's the agent doing what your best nurse does, at 5 AM, across every patient.",
      "wowMoment": false,
      "screenState": "dashboard-complete",
      "methodology": "cohan"
    }
  ]
}
```

---

## Example: Nested Demo2Win acts.json

Demo2Win methodology — Tell-Show-Tell with nested modules inside the Show phase. Invariant #31 overridden because outcome appears in the closing Tell, not the opening.

```json
{
  "schemaVersion": 1,
  "methodology": "demo2win",
  "voiceId": "default-kokoro",
  "invariantOverrides": [
    {
      "invariant": 31,
      "status": "intentional-deviation",
      "rationale": "Demo2Win methodology -- outcome appears in Tell-2 (Act: closing-tell), not opening act",
      "actWithOutcome": "closing-tell"
    }
  ],
  "acts": [
    {
      "act": "opening-tell",
      "label": "The Problem You Told Us About",
      "startMs": 0,
      "durationTargetSec": 60,
      "chapters": ["pain-statement"],
      "narration": "You told us your charge capture team spends four hours a day reconciling missed charges. Four hours. That's not a workflow problem — that's a staffing problem disguised as a process problem. Let me show you what changes.",
      "wowMoment": false,
      "screenState": "title-slide",
      "methodology": "demo2win"
    },
    {
      "act": "show",
      "label": "Product Walkthrough",
      "isContainer": true,
      "methodology": "demo2win"
    },
    {
      "act": "show-module-a",
      "label": "Charge Capture Gap Detection",
      "parentAct": "show",
      "moduleIndex": 0,
      "startMs": 0,
      "durationTargetSec": 90,
      "chapters": ["charge-gap-detection"],
      "narration": "Here's where the charge capture team loses four hours every day. The agent scans overnight encounters against the CDM and flags unbilled procedures. Watch — it just found three CT scans with no corresponding charge.",
      "wowMoment": true,
      "wowSource": "spec",
      "screenState": "charge-gap-table",
      "methodology": "demo2win"
    },
    {
      "act": "show-module-b",
      "label": "Automated Charge Reconciliation",
      "parentAct": "show",
      "moduleIndex": 1,
      "startMs": 0,
      "durationTargetSec": 75,
      "chapters": ["auto-reconcile"],
      "narration": "Now the agent matches each flagged procedure to the correct charge code. No manual lookup. It pulls from your CDM directly and drafts the charge entry for review. Your team approves — they don't create.",
      "wowMoment": true,
      "wowSource": "spec",
      "screenState": "reconciliation-view",
      "methodology": "demo2win"
    },
    {
      "act": "show-module-c",
      "label": "Revenue Impact Dashboard",
      "parentAct": "show",
      "moduleIndex": 2,
      "startMs": 0,
      "durationTargetSec": 60,
      "chapters": ["revenue-dashboard"],
      "narration": "And here's the number your CFO cares about. Recovered charges this month: $2.1 million. That's not projected — that's already billed. The dashboard updates in real time as the agent processes encounters.",
      "wowMoment": true,
      "wowSource": "methodology",
      "screenState": "revenue-dashboard",
      "methodology": "demo2win"
    },
    {
      "act": "closing-tell",
      "label": "The Outcome Realized",
      "startMs": 0,
      "durationTargetSec": 45,
      "chapters": ["outcome-reinforcement"],
      "narration": "You came in losing $2 million a month in missed charges. You just saw the agent find them, code them, and present them for one-click approval. That four-hour daily reconciliation? It's now a fifteen-minute review.",
      "wowMoment": true,
      "wowSource": "methodology",
      "screenState": "summary-slide",
      "methodology": "demo2win"
    }
  ]
}
```

### Nesting Validation Checklist

For any Demo2Win acts.json, verify:

1. Every act with `parentAct` references an act that has `isContainer: true`.
2. Every act with `parentAct` references an act that does NOT itself have a `parentAct` (depth-2 max).
3. Every act with `parentAct` has a `moduleIndex` (zero-based, sequential within parent).
4. Container acts have NO `narration`, `chapters`, `durationTargetSec`, or `screenState`.
5. `moduleIndex` values within a parent are contiguous starting from 0.

---

## Example: Challenger acts.json with invariantOverrides

Challenger methodology — commercial reframe opening. Invariant #31 overridden because the outcome appears after the reframe and show, not in Act 1. No nesting (Challenger uses flat act structure).

```json
{
  "schemaVersion": 1,
  "methodology": "challenger",
  "voiceId": "default-kokoro",
  "invariantOverrides": [
    {
      "invariant": 31,
      "status": "intentional-deviation",
      "rationale": "Challenger methodology -- outcome appears in Act 3 (resolution), not Act 1. Opening act delivers the commercial reframe.",
      "actWithOutcome": "resolution"
    }
  ],
  "acts": [
    {
      "act": "reframe",
      "label": "What You Believe vs. What's True",
      "startMs": 0,
      "durationTargetSec": 60,
      "chapters": ["reframe-open"],
      "narration": "Your team believes the bottleneck is staffing. You've told us you need more coders. But here's what your own data shows: 60% of your denied claims have the same three root causes. You don't have a staffing problem — you have a pattern recognition problem. And you're solving it with headcount.",
      "wowMoment": true,
      "wowSource": "methodology",
      "screenState": "insight-slide",
      "methodology": "challenger"
    },
    {
      "act": "show",
      "label": "The Pattern Your Team Can't See",
      "startMs": 0,
      "durationTargetSec": 90,
      "chapters": ["denial-patterns", "agent-detection"],
      "narration": "Let me show you those three patterns. Here's your denial data from the last quarter — clustered by root cause, not by payer. See the concentration? Modifier errors, auth gaps, and timely filing. An agent trained on your CDM catches all three before submission.",
      "wowMoment": true,
      "wowSource": "spec",
      "screenState": "denial-heatmap",
      "methodology": "challenger"
    },
    {
      "act": "resolution",
      "label": "The Outcome Without the Headcount",
      "startMs": 0,
      "durationTargetSec": 50,
      "chapters": ["outcome-without-headcount"],
      "narration": "Three fewer FTEs in your coding queue. Not because you cut staff — because the agent eliminated the repetitive pattern matching that consumed them. Your experienced coders now handle the complex cases. The agent handles the patterns.",
      "wowMoment": true,
      "wowSource": "methodology",
      "screenState": "staffing-comparison",
      "methodology": "challenger"
    },
    {
      "act": "close",
      "label": "The Question You Should Be Asking",
      "startMs": 0,
      "durationTargetSec": 30,
      "chapters": ["challenger-close"],
      "narration": "The question isn't whether you can afford this. It's how many more quarters you can afford to solve a pattern problem with people.",
      "wowMoment": false,
      "screenState": "closing-slide",
      "methodology": "challenger"
    }
  ]
}
```

### Challenger-Specific Notes

- The `reframe` act is always Act 1. It delivers the commercial insight that contradicts the buyer's current frame.
- `wowSource: "methodology"` on the reframe act — the reframe itself is the wow moment, and it is a spoken insight, not a UI interaction. Phase 4.5 does not look for a code path.
- `invariantOverrides` must include #31 with `actWithOutcome` pointing to whichever act delivers the outcome (typically Act 3).
- The SA supplies `current_buyer_frame` before generation (Decision 7). The Reframe Validation block appears in demo-script.md, not in acts.json.

---

## Field Presence Summary by Methodology

| Field | Cohan | Demo2Win (top-level) | Demo2Win (container) | Demo2Win (sub-act) | Challenger |
|---|---|---|---|---|---|
| `act` | Yes | Yes | Yes | Yes | Yes |
| `label` | Yes | Yes | Yes | Yes | Yes |
| `startMs` | Yes | Yes | No | Yes | Yes |
| `durationTargetSec` | Yes | Yes | No | Yes | Yes |
| `chapters` | Yes | Yes | No | Yes | Yes |
| `narration` | Yes | Yes | No | Yes | Yes |
| `wowMoment` | Yes | Yes | No | Yes | Yes |
| `wowSource` | If wow | If wow | No | If wow | If wow |
| `screenState` | Yes | Yes | No | Yes | Yes |
| `methodology` | Yes | Yes | Yes | Yes | Yes |
| `inferredConfidence` | If Tier 2 | If Tier 2 | No | If Tier 2 | If Tier 2 |
| `parentAct` | No | No | No | Yes | No |
| `moduleIndex` | No | No | No | Yes | No |
| `isContainer` | No | No | Yes | No | No |

---

## Validation Rules (Machine-Checkable)

1. **startMs numeric:** Every act with `startMs` must have `typeof startMs === "number"`. Reject `null`, `undefined`, strings, and negative values.
2. **Unique act IDs:** No two acts share the same `act` value.
3. **Depth-2 max:** If `acts[i].parentAct` exists, then the referenced act must NOT have a `parentAct` of its own.
4. **parentAct references valid container:** If `acts[i].parentAct === X`, then exactly one act with `act === X` must exist, and it must have `isContainer: true`.
5. **Container acts are empty:** If `isContainer: true`, then `narration`, `chapters`, `durationTargetSec`, and `screenState` must all be absent.
6. **moduleIndex contiguous:** Within each parent, `moduleIndex` values form a zero-based contiguous sequence (0, 1, 2, ...).
7. **wowSource required when wowMoment:** If `wowMoment: true`, `wowSource` must be `"spec"` or `"methodology"`.
8. **invariantOverrides well-formed:** Each override has `invariant` (number), `status` ("intentional-deviation"), and `rationale` (non-empty string).
9. **methodology consistent:** Every act's `methodology` field matches the top-level `methodology`.
10. **schemaVersion present:** Top-level `schemaVersion` must be a positive integer.
