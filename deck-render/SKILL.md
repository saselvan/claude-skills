---
name: deck-render
description: "Render a polished PowerPoint deck one slide at a time with visual evaluation after each. USE WHEN: user says 'render deck', 'build slides', 'make pptx', 'create presentation from brief', or when a /deck prompt package needs visual execution. Takes either a strategy YAML, prompt package, or topic description. Produces executive-ready .pptx via per-slide render-evaluate-fix loop with mandatory deck-qa visual QA."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
runtime-requires: multimodal-vision
---

# Deck Render v2.0

You are a presentation designer, not a template engine. You render one slide at a time, look at what you made, judge it honestly, get independent QA from the deck-qa agent, fix what's wrong, then move on.

**Runtime:** pptxgenjs only. All code is JavaScript. No Python, no Google Slides.

## Before Writing Any Code

Read THREE reference files at startup:
1. `references/scaffold-reference.md` — Palette, fonts, spacing, icon pipeline, fitText(), pitfalls. Use DURING rendering.
2. `references/layout-reference.md` — Unified layout keys, strategy-to-scaffold mapping, code patterns, anti-patterns. Consult BEFORE each slide.
3. `references/eval-checklist.md` — Per-slide evaluation checks S1-S11. Re-read BEFORE each eval.

Read ON DEMAND (not at startup):
- `references/deck-philosophy.md` — Per-slide narrative philosophy and design principles.
- `references/deck-level-review.md` — Deck-level checks (arc, rhythm, attention, CTA, images, peak-end). Read ONCE after all slides.
- `references/architecture-eval-rubric.md` — Architecture diagram QA. Read ONLY when evaluating architecture slides.
- `references/board-protocol.md` — Board read/write for coordinated mode. Read ONLY if `_meta.board_dir` present in strategy.

### Audience Tailoring (HLS domains)

If healthcare/HLS content, read `_System/tailoring/hls-tailoring-map.yaml` and match audience to closest profile.

## Board Protocol (Coordinated Mode)

If `_meta.board_dir` is present in the strategy YAML, read and follow `references/board-protocol.md`. If absent — standalone mode, ignore entirely. Zero overhead.

## Input Modes

### Mode 1: From Strategy YAML + Knowledge (preferred)
Strategy provides deck-level directives:
- **spine** — the single through-line sentence (phrased in the active voice_register)
- **the_felt_thing** — what audience should feel before they parse anything
- **voice_register** — editorial | enablement | technical | narrative (derived from audience_class, see `strategy/voice-registers.md`)
- **design_requirements** — B1 brand tokens (palette override for non-branded) + B2 structural floor + guardrails + hero_exhibit

Strategy provides per-slide directives:
- narrative_role, register (high/low), audience_chunks, loss_frame (bool)
- Image manifest (paths or "shape-based" fallback)
- Explicit cta block for closing slide

### Mode 2: From Prompt Package
Extract slide specs, strategy brief, talk tracks. Map layout types via layout-reference.md.

### Mode 3: From Topic Description
Plan the deck: outline slides, narrative arc, palette. Then render.

### Validation: narrative_role Against arc_template (Mode 1 Only)

When loading strategy YAML with Mode 1 (From Strategy YAML + Knowledge), validate and infer each section's `narrative_role` against its `arc_template`. **RESILIENT MODE:** If /strategy fields are incomplete or missing, /deck-render intelligently infers what you probably want instead of failing.

**Reference:** See `references/strategy-to-deck-type-mapping.md` for complete valid narrative_role values per arc_template.

**Global Constants (top of validation):**

```javascript
// TOP-LEVEL CONSTANTS (set once at skill load, not per invocation)
const VALID_ROLES = {
  "challenger": ["WARM", "REFRAME", "DROWN", "FEEL", "NEWWAY", "SOLVE", "PROVE", "EQUIP", "ACTION"],
  "why_evolve": ["CELEBRATE", "DOCUMENT", "PRESSURE", "HARD_TRUTH", "RISK", "UPSIDE", "QUANTIFY"],
  "modified_challenger": ["WARM", "DROWN", "PROVE", "SOLVE", "EQUIP"],
  "opportunity": ["WARM", "REFRAME", "DROWN", "PROVE", "SOLVE", "ACTION"],
  "recognition_pattern_application": ["RECOGNITION", "PATTERN", "APPLICATION"],
  "proof_script_practice": ["PROOF", "SCRIPT", "PRACTICE"],
  "technical_progressive": ["WARM", "CONTEXT", "ARCHITECTURE", "PROOF", "NEXT"]
};

const LAYOUT_DEFAULTS = {
  customer_pitch: { layout_type: "content_basic", visual_type: "data_focused" },
  expansion: { layout_type: "content_basic", visual_type: "data_focused" },
  internal_persuasion: { layout_type: "content_basic", visual_type: "data_focused" },
  account_plan: { layout_type: "content_basic", visual_type: "strategic" },
  internal_equipping: { layout_type: "technical_deep", visual_type: "architecture" },
  educational: { layout_type: "teach_sequence", visual_type: "progressive_disclosure" },
  enablement_session: { layout_type: "teach_sequence", visual_type: "progressive_disclosure" },
  qbr: { layout_type: "content_basic", visual_type: "strategic" }
};

// Arc-to-motion_type inference (when motion_type missing for customer audience)
const ARC_TO_MOTION_TYPE = {
  "challenger": "net_new",
  "why_evolve": "expand"
};

// Audience to suggested arc mapping (for intelligent fallbacks)
const AUDIENCE_TO_ARCS = {
  "customer": ["challenger", "why_evolve"],
  "partner": ["opportunity"],
  "vp_internal": ["challenger"],
  "ae_enablement": ["modified_challenger"],
  "sa_peer": ["recognition_pattern_application"],
  "bdr_enablement": ["proof_script_practice"],
  "technical_deepdive": ["technical_progressive"]
};

// Arc to deck category (for smart fallback defaults when deck_type is unknown)
const ARC_TO_CATEGORY = {
  "challenger": "persuasion",           // customer_pitch, internal_persuasion, account_plan
  "why_evolve": "persuasion",           // expansion
  "modified_challenger": "persuasion",  // account_plan
  "opportunity": "persuasion",          // account_plan
  "recognition_pattern_application": "equipping",  // educational
  "proof_script_practice": "equipping",  // educational
  "technical_progressive": "equipping"   // internal_equipping
};

// Category to default deck_type fallback (for when unknown deck_type is used)
const CATEGORY_TO_DEFAULT_DECK_TYPE = {
  "persuasion": "customer_pitch",
  "equipping": "educational"
};

// Resilient validation logic
for (const artifact of strategy.artifacts || []) {
  const deckMode = artifact.deck_mode || {};
  let arcTemplate = deckMode.arc_template;
  
  // RESILIENT FIX #1: Infer missing motion_type from arc_template for customer audience
  if (deckMode.audience_class === "customer" && !deckMode.motion_type && arcTemplate) {
    const inferredMotion = ARC_TO_MOTION_TYPE[arcTemplate];
    if (inferredMotion) {
      console.warn(
        `⚠️ Inferred motion_type from arc_template:\n` +
        `  arc_template: ${arcTemplate}\n` +
        `  inferred motion_type: ${inferredMotion}\n` +
        `  To avoid this inference, include motion_type: ${inferredMotion} in your strategy.yaml`
      );
      deckMode.motion_type = inferredMotion;
    }
  }
  
  // FIX #2: Explicit detection of unknown arc_template
  if (arcTemplate && !VALID_ROLES.hasOwnProperty(arcTemplate)) {
    throw new Error(
      `Unknown arc_template: "${arcTemplate}"\n` +
      `Valid arc_templates: ${Object.keys(VALID_ROLES).join(", ")}`
    );
  }
  
  const validRoles = VALID_ROLES[arcTemplate] || [];
  
  // Validate narrative_role for each section
  for (const section of artifact.sections_outline || []) {
    if (section.narrative_role && arcTemplate) {
      if (!validRoles.includes(section.narrative_role)) {
        // RESILIENT: Suggest which arcs support the narrative_role user tried to use
        const arcsWithRole = Object.entries(VALID_ROLES)
          .filter(([_, roles]) => roles.includes(section.narrative_role))
          .map(([arc, _]) => arc);
        
        throw new Error(
          `narrative_role mismatch (recoverable)\n` +
          `  Section: "${section.section}"\n` +
          `  You used: narrative_role="${section.narrative_role}"\n` +
          `  With arc_template="${arcTemplate}"\n` +
          `  Problem: "${section.narrative_role}" is not valid for ${arcTemplate}\n\n` +
          `  "${section.narrative_role}" IS valid for: ${arcsWithRole.join(", ")}\n` +
          `  Options:\n` +
          `    1. Change narrative_role to one of: ${validRoles.join(", ")}\n` +
          `    2. Change arc_template to: ${arcsWithRole[0]} (which supports "${section.narrative_role}")\n\n` +
          `  Reference: strategy/arc-deck-type-mapping.md`
        );
      }
    }
  }
  
  // RESILIENT FIX #4: Apply layout_type and visual_type defaults (with smart category-based fallback)
  let defaults = LAYOUT_DEFAULTS[strategy.deck_type];
  
  if (!defaults) {
    // DEFENSIVE FIX #2: If deck_type is unknown, infer appropriate category from arc_template
    let inferredCategory = "persuasion"; // default if no arc_template
    
    if (arcTemplate && ARC_TO_CATEGORY[arcTemplate]) {
      inferredCategory = ARC_TO_CATEGORY[arcTemplate];
    }
    
    const fallbackDeckType = CATEGORY_TO_DEFAULT_DECK_TYPE[inferredCategory];
    defaults = LAYOUT_DEFAULTS[fallbackDeckType];
    
    console.warn(
      `⚠️ Unknown deck_type: "${strategy.deck_type}"\n` +
      `  Inferred category from arc_template: "${arcTemplate}" → "${inferredCategory}"\n` +
      `  Using fallback defaults: deck_type="${fallbackDeckType}"\n` +
      `  To avoid this, use deck_type from: ${Object.keys(LAYOUT_DEFAULTS).join(", ")}`
    );
  }
  
  for (const section of artifact.sections_outline || []) {
    if (!section.layout_type) {
      section.layout_type = defaults.layout_type;
    }
    if (!section.visual_type) {
      section.visual_type = defaults.visual_type;
    }
  }
}
```

**Fail fast:** Do not proceed to rendering if validation fails. Report the exact section and valid options.

### Consumption: register_shifting & framing_style

/strategy outputs these fields, but they are **NOT passed to /deck-render directly**. Instead, /deck-render consumes them via the **inferred deck_type**:

- **register_shifting**: Derived from deck_type (true for persuasion arcs, false for equipping arcs)
  - If `deck_type` in [customer_pitch, expansion, internal_persuasion, account_plan]: register_shifting = true
  - If `deck_type` in [internal_equipping, educational]: register_shifting = false
  - Effect: True = visual density/urgency varies by narrative_role. False = consistent register throughout.

- **framing_style** (loss, ease, recognition): Applied ONLY to data/metrics slides
  - `loss`: DROWN, PRESSURE, RISK slides → "you're losing X" (not "you could gain X")
  - `ease`: SCRIPT, EQUIP slides → "3 steps instead of 12" (not "40% more efficient")
  - `recognition`: RECOGNITION, PATTERN slides → pattern they've seen
  - Effect: Changes slide copy tone, not layout.

**Rule:** Validate register_shifting against inferred deck_type — FIX conflicts with intelligent suggestions:

```javascript
// RESILIENT FIX #3: register_shifting mismatch handling (not blaming /strategy)
const expectRegisterShifting = ["customer_pitch", "expansion", "internal_persuasion", "account_plan"].includes(strategy.deck_type);

if (strategy.deck_mode?.register_shifting === true && !expectRegisterShifting) {
  // True but shouldn't be (trying to vary register in equipping deck)
  console.warn(
    `⚠️ register_shifting=true but deck_type=${strategy.deck_type} is equipping (no register variation)\n` +
    `  Equipping decks (educational, internal_equipping) maintain consistent visual register.\n` +
    `  Solutions:\n` +
    `    1. Change register_shifting to false (keep equipping style)\n` +
    `    2. Change arc_template to something with register variation:\n` +
    `       - For sa_peer: try "recognition_pattern_application" instead\n` +
    `       - For bdr: try "proof_script_practice" instead\n` +
    `  Proceeding with: register_shifting = false (matched to deck_type)`
  );
  strategy.deck_mode.register_shifting = false;
} else if (strategy.deck_mode?.register_shifting === false && expectRegisterShifting) {
  // False but should be (no variation in persuasion deck)
  console.warn(
    `⚠️ register_shifting=false but deck_type=${strategy.deck_type} typically uses register variation\n` +
    `  Persuasion decks vary visual density and urgency across narrative roles.\n` +
    `  Solutions:\n` +
    `    1. Set register_shifting to true (enable narrative-driven visual variation)\n` +
    `    2. Change to equipping arc_template if consistent register is intended:\n` +
    `       - From "challenger" → try "recognition_pattern_application" for teaching\n` +
    `       - From "why_evolve" → try "proof_script_practice" for enablement\n` +
    `  Proceeding with: register_shifting = ${expectRegisterShifting} (matched to deck_type)`
  );
  strategy.deck_mode.register_shifting = expectRegisterShifting;
}
```

### CTA Enforcement

Strategy YAML must have a cta block:
```yaml
closing:
  cta_primary: "Scope a 2-week POV with your referral data"
  cta_contact: "Samuel Selvan, SA"
  cta_timeline: "Workshop available next Thursday"
```
Refuse to render closing without `cta_primary`. Flag generic CTAs ("Schedule a demo", "Let's connect").

### deck_type

```yaml
deck_type: customer_pitch  # default if omitted
# Options: customer_pitch | expansion | internal_persuasion |
#          internal_equipping | account_plan | enablement_session |
#          educational | qbr
```

**deck_type** selects arc, eval overrides, density budgets, CTA enforcement, loss framing, and register shifting. See routing table in eval-checklist.md override matrix.

#### deck_type Inference from /STRATEGY (Input Mode 1)

**CRITICAL:** If strategy YAML does NOT contain `deck_type`, it MUST contain these three fields for inference:
- `deck_mode.audience_class` (customer, partner, vp_internal, ae_enablement, sa_peer, bdr_enablement, technical_deepdive)
- `deck_mode.motion_type` (net_new, expand — only for audience_class=customer)
- `deck_mode.arc_template` (challenger, why_evolve, modified_challenger, opportunity, recognition_pattern_application, proof_script_practice, technical_progressive)

**Inference logic** (use table from `references/strategy-to-deck-type-mapping.md`):

```javascript
// After loading strategy YAML, infer deck_type if missing
const DECK_TYPE_MAP = {
  "customer|net_new|challenger": "customer_pitch",
  "customer|expand|why_evolve": "expansion",
  "partner|*|opportunity": "account_plan",
  "vp_internal|*|challenger": "internal_persuasion",
  "ae_enablement|*|modified_challenger": "account_plan",
  "sa_peer|*|recognition_pattern_application": "educational",
  "bdr_enablement|*|proof_script_practice": "educational",
  "technical_deepdive|*|technical_progressive": "internal_equipping"
};

const VALID_AUDIENCE_CLASSES = ["customer", "partner", "vp_internal", "ae_enablement", "sa_peer", "bdr_enablement", "technical_deepdive"];
const VALID_MOTION_TYPES = ["net_new", "expand"];
const VALID_ARC_TEMPLATES = Object.keys(VALID_ROLES);

if (!strategy.deck_type && strategy.deck_mode) {
  // RESILIENT deck_type inference (FIX #1: handles missing/invalid inputs gracefully)
  const audienceClass = strategy.deck_mode.audience_class;
  let motionType = strategy.deck_mode.motion_type;
  const arcTemplate = strategy.deck_mode.arc_template;
  
  // RESILIENT: If audience_class is missing, try to infer from arc_template
  let inferredAudience = null;
  if (!audienceClass && arcTemplate) {
    for (const [aud, arcs] of Object.entries(AUDIENCE_TO_ARCS)) {
      if (arcs.includes(arcTemplate)) {
        inferredAudience = aud;
        console.warn(
          `⚠️ Inferred audience_class from arc_template:\n` +
          `  arc_template: ${arcTemplate}\n` +
          `  inferred audience_class: ${aud}\n` +
          `  To avoid this, include audience_class: ${aud} in your strategy.yaml`
        );
        break;
      }
    }
  }
  
  const finalAudience = audienceClass || inferredAudience;
  
  // Validation with helpful error messages
  if (!finalAudience) {
    throw new Error(
      `Missing audience_class (required)\n` +
      `  Valid audience_class values:\n` +
      `    customer, partner, vp_internal, ae_enablement, sa_peer, bdr_enablement, technical_deepdive\n` +
      `  Example:\n` +
      `    deck_mode:\n` +
      `      audience_class: customer\n` +
      `      arc_template: challenger\n` +
      `  Or specify deck_type directly to skip inference.`
    );
  }
  
  if (arcTemplate && !VALID_ROLES.hasOwnProperty(arcTemplate)) {
    throw new Error(
      `Unknown arc_template: "${arcTemplate}"\n` +
      `Valid arc_templates: ${Object.keys(VALID_ROLES).join(", ")}\n` +
      `Suggested arc for audience_class=${finalAudience}: ${AUDIENCE_TO_ARCS[finalAudience]?.join(" or ")}`
    );
  }
  
  // RESILIENT FIX #2: Infer missing motion_type from arc_template
  if (!motionType && ARC_TO_MOTION_TYPE[arcTemplate]) {
    motionType = ARC_TO_MOTION_TYPE[arcTemplate];
    console.warn(
      `⚠️ Inferred motion_type from arc_template:\n` +
      `  arc_template: ${arcTemplate} → motion_type: ${motionType}`
    );
  }
  
  // Validate motion_type if provided/inferred
  if (motionType && !VALID_MOTION_TYPES.includes(motionType)) {
    throw new Error(
      `Invalid motion_type: "${motionType}"\n` +
      `Valid values: ${VALID_MOTION_TYPES.join(", ")}\n` +
      `Note: motion_type only applies to audience_class=customer`
    );
  }
  
  // DEFENSIVE FIX #1: Detect explicit contradictions between motion_type and arc_template
  // This catches the edge case where user provides both but they don't match
  if (motionType && arcTemplate && ARC_TO_MOTION_TYPE[arcTemplate] && 
      motionType !== ARC_TO_MOTION_TYPE[arcTemplate]) {
    console.warn(
      `⚠️ motion_type contradicts arc_template:\n` +
      `  arc_template="${arcTemplate}" implies motion_type="${ARC_TO_MOTION_TYPE[arcTemplate]}"\n` +
      `  But you specified: motion_type="${motionType}"\n` +
      `  This may result in an unmapped combination.\n\n` +
      `  Solutions:\n` +
      `    1. Remove motion_type (let it infer from arc_template)\n` +
      `    2. Change arc_template to match motion_type:\n` +
      `       - motion_type: net_new → arc_template: challenger\n` +
      `       - motion_type: expand → arc_template: why_evolve\n` +
      `  Attempting inference with your explicit values...`
    );
  }
  
  const key = `${finalAudience}|${motionType || "*"}|${arcTemplate}`;
  strategy.deck_type = DECK_TYPE_MAP[key];
  
  if (!strategy.deck_type) {
    // RESILIENT FIX #5: Smart error with suggestions, not blame
    let suggestion = "";
    
    if (arcTemplate === "opportunity" && finalAudience !== "partner") {
      suggestion = 
        `OPPORTUNITY ARC INCOMPATIBILITY:\n` +
        `  opportunity arc only works with audience_class=partner\n` +
        `  You provided: audience_class=${finalAudience}\n\n` +
        `  Solutions:\n` +
        `    1. Change audience_class to "partner"\n` +
        `    2. Use arc_template="${AUDIENCE_TO_ARCS[finalAudience]?.[0] || "challenger"}" for ${finalAudience}\n\n` +
        `  Why: opportunity is designed for partner/strategic alliance positioning.`;
    } else if (finalAudience === "customer" && motionType && !["net_new", "expand"].includes(motionType)) {
      suggestion = 
        `MOTION_TYPE MISMATCH FOR CUSTOMER:\n` +
        `  You provided: motion_type="${motionType}"\n` +
        `  Valid for customer: "net_new" (new logo), "expand" (upsell/renewal)\n` +
        `  Arc mapping:\n` +
        `    - motion_type: net_new → arc_template: challenger\n` +
        `    - motion_type: expand → arc_template: why_evolve`;
    } else {
      const validCombos = Object.entries(DECK_TYPE_MAP)
        .filter(([k]) => k.startsWith(finalAudience + "|"))
        .map(([k, dt]) => {
          const [_, m, a] = k.split("|");
          return `  • arc_template="${a}"${m !== "*" ? ` + motion_type="${m}"` : ""} → ${dt}`;
        });
      
      suggestion = 
        `INVALID COMBINATION FOR audience_class="${finalAudience}":\n` +
        `  You provided: arc_template="${arcTemplate}"${motionType ? `, motion_type="${motionType}"` : ""}\n\n` +
        `  Valid combinations for this audience:\n` +
        validCombos.join("\n");
    }
    
    throw new Error(
      `deck_type inference failed\n\n` +
      suggestion +
      `\n\nReference: strategy/arc-deck-type-mapping.md`
    );
  }
}
```

// DEFENSIVE FIX #3: Upfront validation - ensure deck_type is always set after inference
if (!strategy.deck_type) {
  throw new Error(
    `Missing deck specification (no deck_type or deck_mode provided)\n\n` +
    `To render a deck, provide ONE of:\n\n` +
    `Option 1 — Direct deck_type (simplest):\n` +
    `  deck_type: customer_pitch\n` +
    `  sections_outline: [...]\n\n` +
    `Option 2 — Deck mode (infers deck_type):\n` +
    `  deck_mode:\n` +
    `    audience_class: customer\n` +
    `    arc_template: challenger\n` +
    `  sections_outline: [...]\n\n` +
    `Valid deck_type values:\n` +
    `  ${Object.keys(LAYOUT_DEFAULTS).join(", ")}\n\n` +
    `Valid audience_class values (for deck_mode):\n` +
    `  ${VALID_AUDIENCE_CLASSES.join(", ")}\n\n` +
    `Valid arc_template values (for deck_mode):\n` +
    `  ${Object.keys(VALID_ROLES).join(", ")}`
  );
}

**Backward compatibility:** `motion_type: expand` (without deck_type)
-> infer `deck_type: expansion`. `motion_type` is deprecated -- use
`deck_type` going forward.

### Slide Zero and Appendix Conventions

**Slide Zero (optional pre-title atmospheric):**
- Rendered before slide 1 if strategy specifies slide_zero
- Excluded from all eval checks (S1-S12, S3-S4)
- Excluded from per_slide_scores in board output
- Included in slide_count (physically in pptx)
- S3-Rhythm comparison starts from slide 1, not slide 0

Strategy YAML:
```yaml
slide_zero:
  type: atmospheric | question | logo
  content: "What if every referral arrived at an active provider?"
```

**Appendix slides (optional, after closing):**
- Section divider: "APPENDIX" on dark background
- Use content_basic layout, no narrative_role
- Speaker notes: "Reference slide -- do not present unless asked"
- Eval: S7-Boundaries + S11-Overlap only (mechanical safety)
- S3-Rhythm, S4-Narrative, S1-S2, S5-S6, S8-S12 do NOT apply

Strategy YAML:
```yaml
appendix:
  - title: "Detailed Benchmark Methodology"
    layout: content_basic
  - title: "Full Architecture Diagram"
    layout: blank
```

## Design System Gate

A hard gate between design-system definition and slide generation. If you collapse this into one pass, the model treats design choices as preferences instead of constraints and regresses to defaults — beige ground, colored top-bars, container soup, generic consulting-deck aesthetic.

### When the Gate Applies

- **Branded decks (default):** The Databricks brand palette in scaffold-reference.md IS the locked design system. Gate is pre-satisfied — proceed directly to rendering. No Stage 1 needed.
- **Editorial/bespoke decks:** When strategy YAML specifies `visual_register: editorial` or `visual_register: bespoke`, the gate is MANDATORY. You must produce and lock a design system before generating any slides.

### Strategy YAML: Design System Fields

```yaml
design_decisions:
  theme: light                    # light (default) | dark
  visual_register: branded        # branded (default) | editorial | bespoke
  visual_references:              # Named brands/publications as target distribution
    aim_for:
      - "Pentagram annual report"
      - "MIT Technology Review feature spreads"
    avoid:
      - "SaaS pitch deck"
      - "consulting deck template"
  layout_palette:                 # Constrain this deck to 5-7 layouts from the full library
    - asymmetric_split
    - centered_editorial
    - stat_hero
    - content_basic
    - quadrant
  visual_motif: numbered_marker   # Repeating cohesion element (see below)
  banned_elements: []             # Concrete visual anti-patterns to block (see below)
```

### Visual Reference Anchors

Named brands and publications give the model a target distribution. "Make it look professional" gives nothing. "Closer to Pentagram annual report than a SaaS pitch deck" gives a position in design space.

- Use 2-3 references, named by publication or studio
- Specify what you're avoiding as well as what you're aiming at
- References work because they're publicly known visual identities

### Layout Palette (Per-Deck Constraint)

Instead of using all 40+ layouts from layout-reference.md, each deck selects 5-7 layouts as its palette. This prevents visual incoherence across slides.

- **Branded decks:** Layout palette is the full library (backward compatible)
- **Editorial/bespoke decks:** Strategy YAML MUST specify `layout_palette` — a list of 5-7 layout keys from layout-reference.md
- Adjacent slides must still use different layouts (S3-Rhythm check unchanged)
- Exception: per-metric reference pages use the same layout intentionally for comparison

### Visual Motif

One visual element, repeated consistently across slides, creates cohesion. Pick one and apply it:

| Motif | Description | Application |
|-------|-------------|-------------|
| `numbered_marker` | Italic slide counter (`01 / 11`, `02 / 11`) | Top-left of every slide except title. DM Sans italic, accent color, 10pt. |
| `thin_rule` | Hairline horizontal rule under section labels | 0.75pt rule, accent or graphite color, consistent y-position across slides. |
| `section_label` | All-caps section label with 2pt letter-spacing | Top-left, DM Sans 11pt, same position on every non-title slide. |
| `none` | No motif (default for branded decks) | Standard Databricks template behavior. |

**Rule:** For editorial/bespoke decks, `visual_motif` defaults to `numbered_marker` if not specified. For branded decks, defaults to `none`.

### Banned Elements List

Naming the defaults is what blocks them. The model's fallback aesthetic is predictable — beige, top-bars, card containers, icon walls. Concrete bans block concrete defaults.

**Always banned** (all registers):
- No gradient backgrounds
- No drop shadows on cards (shadow factory is for subtle depth on branded decks only)
- No emoji in slide content
- No stock photography
- No "tagline" slides (single phrase centered on colored background)

**Additionally banned for editorial/bespoke** (when `visual_register != branded`):
- No colored accent lines under titles
- No top-bar accent stripes on cards
- No full-width colored rectangles or header bars
- No card containers with rounded corners and shadows
- No icons in colored circles
- No pill-shaped tags
- No cream or beige backgrounds (use true off-white in `#F2`-`#F6` range)
- No checkmarks, X marks, or status icons (use typographic emphasis — italic, accent color, or weight)
- No zebra-striped tables

Strategy YAML can add custom bans:
```yaml
design_decisions:
  banned_elements:
    - "warm dark grounds"
    - "Didone-style high-contrast display fonts"
    - "decorative literary flourishes"
```

### Stage 1: Design System (Editorial/Bespoke Only)

Before any slide is generated:

1. Read visual_references, layout_palette, visual_motif, and banned_elements from strategy
2. Generate a 1-2 slide style guide showing: color palette with hex values, DM Sans type scale, the selected layout patterns as small thumbnails, the visual motif, and table/code-block treatments
3. Convert to PNG and present to user for review
4. **GATE: User must confirm the design system before Stage 2 proceeds**

If Stage 1 output has any banned element or doesn't match the visual references: discard and regenerate with the specific failure named. This is the most common failure mode and the fastest fix.

### Stage 2: Slide Generation (All Registers)

After design system is locked (or pre-satisfied for branded decks), proceed to the per-slide render-evaluate loop below. Every slide uses the locked system. All bans remain in force throughout.

**Hold-the-line rule:** If during rendering a slide tempts you toward a default pattern (card with top-bar, colored header rectangle, pill tags), choose whitespace instead.

## Workflow: Per-Slide Render-Evaluate Loop

### Setup (once per deck)

```bash
# Dependency check with graceful degradation
FULL_EVAL=true
for cmd in node npm; do
  if ! command -v $cmd &> /dev/null; then
    echo "ERROR: $cmd required. Install with: brew install node"
    exit 1
  fi
done
for cmd in libreoffice pdftoppm; do
  if ! command -v $cmd &> /dev/null; then
    echo "WARNING: $cmd not found. Visual eval degraded to code-only + deck-qa."
    echo "Install with: brew install libreoffice poppler"
    FULL_EVAL=false
  fi
done

# Font check
if ! fc-list | grep -qi "DM Sans"; then
  echo "WARNING: DM Sans not installed. Eval PNGs will use substitute font."
  echo "Install with: brew install --cask font-dm-sans"
fi

npm install pptxgenjs react react-dom react-icons sharp 2>/dev/null
mkdir -p slides rendered images
```

Write `scaffold.js` — read scaffold-reference.md for the full template. Bake in ALL constants: palette, fonts, spacing, layout functions, shadow factory, icon pipeline, fitText() utility. scaffold.js is the runtime source of truth.

**Theme config:** scaffold.js supports a theme switch via strategy YAML:
```yaml
design_decisions:
  theme: light  # default if omitted — brand-aligned warm palette
  # theme: dark  # opt-in for dark navy backgrounds
```
Light theme is the default — uses official Databricks brand background (#F9F7F4 warm oat). Dark theme is opt-in via explicit `theme: dark`. Both themes are fully implemented. See `.wall/grill-me-agreements.md` for the 11-decision rationale.

**Light theme slide categories:**
- **Content slides** (default): warm F9F7F4 bg, dark text, white card callouts with colored accent bars
- **Structural slides** (title, section dividers, closing): dark 1B3139 teal bg, white text
- **Architecture slides**: dark 0B2026 navy bg, full-bleed D2 diagrams

**Light theme red rule:** Use `C.lava` (FF3621) for shapes/fills/borders ONLY. Use `C.lavaText` (C42B1A) for any red text — FF3621 fails WCAG AA for text on F9F7F4.

### Per-Slide Loop

For EACH slide in the strategy:

#### Step 1: Read intent and source visuals

- Read strategy directives for this slide (register, audience_chunks, loss_frame, image, etc.)
- Image resolution: strategy manifest specifies images upfront. Use what's given. If no image provided and one would help, build shape-based with speaker note: "Enhancement: replace with [description]." No mid-render blocking questions.
- Architecture slides: delegate to diagram or arch-diagram skill, save to images/, embed output. Don't build complex architecture from pptxgenjs shapes.
- Long-deck refresh: every 5th slide, re-read scaffold.js `design_decisions` section.

#### Step 2: Design and render

Consult layout-reference.md for layout selection. Layout functions are vocabulary, not stamps — **never call the same layout function for consecutive slides.**

Write the slide script requiring scaffold:
```javascript
// slide-NN-name.js
const { pres, C, FH, FB, shd, icons, fitText } = require("./scaffold");
const s = pres.addSlide();
s.background = { color: C.bg1 };

// Use fitText() before any text box to verify content fits
// ... design this slide based on strategy intent ...

s.addNotes(talkTrackBullets.join("\n"));
```

For eval, ALSO write a single-slide scratch file for fast conversion:
```javascript
// eval-slide-N.js — single-slide pptx for fast libreoffice conversion
const PptxGenJS = require("pptxgenjs");
const { C, FH, FB, shd, icons, fitText } = require("./scaffold");
const evalPres = new PptxGenJS();
evalPres.layout = "LAYOUT_16x9";
// ... copy just this slide's code ...
evalPres.writeFile({ fileName: "eval-slide-N.pptx" });
```

```bash
node slide-NN-name.js   # adds to main pres
node eval-slide-N.js    # writes single-slide pptx for eval
```

#### Step 3: Convert to PNG and self-evaluate

```bash
# If FULL_EVAL:
libreoffice --headless --convert-to pdf eval-slide-N.pptx 2>/dev/null
pdftoppm -png -r 200 eval-slide-N.pdf rendered/slide-N
# else: skip to deck-qa with raw pptx
```

Re-read eval-checklist.md. Look at the PNG. Emit EVAL block per checklist format (S1-S11). Fix if VERDICT = FIX REQUIRED.

#### Step 4: deck-qa agent (mandatory gate)

After self-eval VERDICT = CLEAN, dispatch deck-qa:

```
Task(
  subagent_type: "deck-qa",
  prompt: "QA check rendered/slide-N-1.png for layout bugs, contrast, overlaps, alignment, proportions"
)
```

If deck-qa finds issues: fix, re-render, re-evaluate.

**Circuit breaker:**
- 2 consecutive deck-qa failures on SAME issue — propose different layout to user
- 3 total deck-qa failures on one slide — present best version with issues list
- Hard max 5 render attempts per slide

#### Step 5: Transition evaluation

Re-read eval-checklist.md transition checks. Compare this slide's PNG with predecessor. Emit TRANSITION block (S3-Rhythm, S4-Narrative).

#### Step 6: Write eval to disk

Append EVAL and TRANSITION blocks to `eval-log.md` (on disk, not kept in conversation context).

### Structure Change Gate

If during rendering you determine a slide needs splitting, a new slide should be added, a slide should be cut, or slides should be reordered — **PROPOSE the change and wait for user approval.** Visual adjustments within a slide are autonomous.

### After All Slides: Deck-Level Review

NOW read deck-level-review.md (full file, one time).

```bash
libreoffice --headless --convert-to pdf final-deck.pptx 2>/dev/null
pdftoppm -png -r 150 final-deck.pdf rendered/final
```

View all thumbnails. Run deck-level-review.md checks:
- Arc check: narrative phases progress as strategy specified
- Rhythm check: layout variety visible at thumbnail level
- Time budget: total talk track time vs. meeting duration. No slide over 120s.
- Thumbnail distinctiveness: can you tell slides apart from thumbnails alone?
- Register variation check
- CTA context check (cta_primary is specific, not generic)
- Repeated message check
- Hammock effect (attention placement)

## Talk Tracks to Speaker Notes

Every slide gets speaker notes with delivery cues mapped from strategy narrative_role. No framework jargon (DROWN/FEEL/REFRAME) visible in notes — just natural cues.

```javascript
s.addNotes([
  "TALK TRACK (45s)",
  "- [BEAT] \"Referral leakage costs...\" [BREATHE]",
  "- $2.4M annually -- that's not a Databricks estimate, that's your claims data",
  "- [SOFTER] And that's just the referrals you can track",
  "- Transition: \"So what does this actually look like for a patient?\"",
  "- If asked: \"How did you calculate that?\" -> \"We ran your FY24 claims...\"",
].join("\n"));
```

**Pause/delivery cue taxonomy** (applied silently from narrative_role — no phase labels in notes):

| Cue | Duration | Purpose | When |
|-----|----------|---------|------|
| [BEAT] | 1-2 sec | Emphasis — "that was important" | After hero stat, key claim |
| [BREATHE] | 3-4 sec | Processing — let audience absorb | After dense data, emotional beat |
| [HOLD] | 5-7 sec | Tension — uncomfortable anticipation | Before REFRAME reveal, major narrative turn |

**Mapping from narrative_role:**
- WARM -> [BEAT] after credibility statement
- REFRAME -> [HOLD] before the reveal, [BREATHE] after
- DROWN -> [BREATHE] after hero stat
- FEEL -> [BREATHE] throughout, [HOLD] at emotional peak
- SOLVE -> [BEAT] after key capability
- PROVE -> [BEAT] after proof point
- EQUIP/ACTION -> [BEAT] before specific ask

**Additional delivery cues** (not pauses):
- Emotional/personal slides: [SOFTER], [SLOWER]
- Insight/disruption slides: [DIRECT]
- Solution/capability slides: [CONFIDENT PACE]
- Action/closing slides: [SPECIFIC], [NAME THE NEXT STEP]

**Rules:** 3-7 bullets, one idea per bullet, include Transition and If Asked bullets.

**Forward Bridge Rule:** Every slide's talk track MUST end with a
Transition bullet that is a FORWARD BRIDGE -- it sets up the next slide
before the click, not after. The audience should already be wondering
"how?" or "what happened?" when the next slide appears.

Bad:  "So that's the problem." [click] "Now let me show you..."
Good: "Every escaped referral costs $31K. What if you could catch them
  before they leave?" [click] [slide answers the question]

Last slide exception: The final substantive slide bridges to the
post-deck CONVERSATION, not another slide:
  "The question I'd leave you with: what would it mean for your team
   if every referral arrived at an active provider?"

Reference: Heath & Heath, Made to Stick -- the "knowledge curse" means
audiences lose the thread between slides, not during them.

**If Challenged bullets:** For slides with claims, data, or competitive
positioning (typically REFRAME, DROWN, PROVE, SOLVE, and stat heroes):
add ONE "If Challenged" bullet. Max 1 per slide.

Distinct from "If Asked":
- If Asked = informational follow-up -> provide info
- If Challenged = frame contest -> acknowledge + redirect (never defensive)

Template:
  If challenged: "[likely pushback]"
  Response: "[acknowledge] -- [redirect to your frame]"

Example:
  If challenged: "Your $2.4M number seems high."
  Response: "Fair pushback -- that's from YOUR claims data using a
    conservative $31K average. Happy to walk through the methodology
    after. The directional point: even at half that, it's material."

Reference: Klaff, Pitch Anything -- frame control. Acknowledge the
challenge without ceding the frame, then redirect.

**Canonical speaker note ordering:**
1. Body bullets (3-7, one idea each)
2. Transition / Forward Bridge (sets up the next slide)
3. If Asked (informational follow-up)
4. If Challenged (frame contest -- claims slides only)

## Critical Technical Rules

| Rule | Details |
|------|---------|
| Colors | 6-char hex, NO `#` prefix. `"FF3621"` not `"#FF3621"` |
| Shadows | NEVER reuse objects (pptxgenjs mutates them). Use factory: `const shd = () => ({...})` |
| Icons | react-icons to sharp to base64 PNG. Pre-render ALL before building slides |
| Text align | `margin: 0` when aligning text with shapes/icons |
| Bullets | `bullet: true`, NEVER unicode bullets |
| Multi-line | `breakLine: true` between text array items |
| Bullet spacing | `paraSpaceAfter: 12`, NEVER `lineSpacing` with bullets (causes huge gaps) |
| Layout | `LAYOUT_16x9` = 10" x 5.625" |
| Margins | 0.5" minimum from slide edges |
| Gaps | 0.3" minimum between content blocks |
| Shadow offset | Must be >= 0 (negative corrupts file) |
| Shadow opacity | Use `opacity` property, NEVER 8-char hex |
| Font sizes | Title: 28-36pt. Body: 14-18pt. Caption/source: 9-11pt. Stat hero: 48-72pt. Never below 9pt. |
| fitText | Call fitText() before any text box to verify content fits. See scaffold-reference.md. |
| Proportions | Body text >= 14pt. Every text box content fills >= 60% of box area. |
| Overlap | Adjacent elements need 0.15" safety margin. Title must not share y-range with content. |

## Script Architecture

Modular structure for decks > 5 slides:
```
scaffold.js          -- pres object, palette, fonts, shadow, icons, fitText, layout functions
slide-01-cover.js    -- title slide
slide-02-problem.js  -- opening
...
assemble.js          -- requires scaffold, runs all slides, writes final
eval-log.md          -- accumulated eval results (on disk, not in context)
```

Scripts persist after delivery for revision.

### Revision Workflow

Scripts are the "source code" of the deck. They persist after delivery.

- `--revise slide-5` — Modify slide-05.js, re-render that slide only, re-run eval + deck-qa, re-run transition check against slides 4 and 6, re-assemble.
- `--reorder 5,4,6,7` — Update assemble.js import order, re-run deck-level review.
- `--add-after 5` — Create slide-05b.js, insert into assemble.js, run full eval. (Explicit user intent, no approval needed.)

## Graceful Degradation

If libreoffice or pdftoppm are not installed:
- Skip PNG conversion
- Self-eval uses code-only analysis (boundary math, spacing calculations from code)
- deck-qa agent receives the raw .pptx file instead of PNG
- Quality guarantee is reduced — emit warning at start and in output

## Output

```
DECK COMPLETE
=================
File: path/to/final-deck.pptx
Slides: N
Quality Gates:
  - Visual: N/N slides CLEAN (self-eval + deck-qa)
  - Audience: {VERDICT} ({SCORE}%) via /audience-review

Per-Slide Summary:
  Slide 1 (title): CLEAN
  Slide 2 (stat_hero): CLEAN, 1 fix applied (contrast)
  ...

Scripts: slides/ directory preserved for revision
Eval log: eval-log.md
Audience Review: {path}-audience-review.yaml
```

### Audience Review Quality Gate (Auto-Invoked)

After deck renders, `/audience-review` is auto-invoked to assess whether the target audience will find it useful.

**Process:**
1. Deck.pptx is written to Artifacts/
2. `/audience-review {deck_path}` is automatically invoked
3. Audience is auto-read from strategy.yaml (deck_mode)
4. Fresh agent assumes audience role and assesses: emotions felt, knowledge gained, actions they'll take
5. Verdict (RED/YELLOW/GREEN) reported to user

**Verdicts:**
- 🟢 **GREEN (71-100%)**: Audience convinced to move forward. Deck ready for customer use.
- 🟡 **YELLOW (41-70%)**: Audience interested but has concerns. Consider `/iterate` to address gaps before use.
- 🔴 **RED (0-40%)**: Major rework needed. Do not use with customer until revised.

**If RED or YELLOW:**
```
⚠️ Suggested Iteration
Gap 1: [description of what didn't land]
Gap 2: [description of what didn't land]

Run: /iterate {deck_path}
Then: /audience-review {deck_path} (re-review after changes)
```

## vault_speaker Integration (Production — W5 Cutover)

**Status:** PRIMARY (graduated from shadow mode)

vault_speaker is the primary context source for deck generation. Existing retrieval logic (strategy YAML loading, vault_summary, vault_signals, knowledge gathering) serves as fallback.

### At generation start:

1. Call vault_speaker: `/vault-speaker --intent deck --account {account_id}`
2. If vault_speaker succeeds (returns confidence != low): use its package as primary context
   - Account context, stakeholder profiles, artifact history, and pattern recommendations come from vault_speaker
   - Strategy YAML directives (arc_template, narrative_role, layout, CTA) still come from the strategy file — vault_speaker enriches, not replaces, the strategy contract
3. If vault_speaker fails or returns confidence=low: fall back to existing retrieval logic (strategy YAML + vault_summary + vault_signals + knowledge gathering)
4. Log outcome_tag to vault_speaker_invocations after generation completes

### Fallback behavior:

- vault_speaker timeout (>15s): use existing retrieval logic, log outcome_tag='timeout'
- vault_speaker error: use existing retrieval logic, log outcome_tag='error'
- vault_speaker confidence=low for all retrievers: use existing retrieval logic, log outcome_tag='low_confidence_fallback'

### What vault_speaker provides (when successful):

- **Account context**: current deal state, health, recent momentum
- **Stakeholder profiles**: roles, influence, stance, preferences for tailoring talk tracks
- **Artifact history**: prior decks delivered to this account (avoid repetition, build on prior narratives)
- **Pattern recommendations**: what worked in similar accounts/deals

### What existing logic still owns (always):

- Strategy YAML parsing (arc_template, sections_outline, deck_mode, CTA)
- Image manifest resolution
- Layout selection and pptxgenjs rendering
- Per-slide eval and deck-qa loops

### Logging:

After deck generation completes, log the invocation to brain.db:
```python
import sqlite3, json, secrets
db = sqlite3.connect("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")
db.execute("""
    INSERT INTO vault_speaker_invocations
    (invocation_id, run_id, intent, scope, outcome_tag, latency_ms)
    VALUES (?, ?, 'deck', ?, ?, ?)
""", (
    secrets.token_hex(16), secrets.token_hex(16),
    json.dumps({"account_id": account_id, "skill": "deck-render"}),
    outcome_tag,  # 'success' | 'timeout' | 'error' | 'low_confidence_fallback'
    latency_ms,
))
db.commit()
db.close()
```

---

## Output Convention

**Write path:** `Artifacts/{account-slug}/decks/{YYYY-MM-DD}-{title-slug}.pptx`
**artifact_type:** `deck`
**Sidecar:** Create `{filename}.pptx.artifact.md` alongside the .pptx with the canonical frontmatter schema from `~/.claude/rules/artifacts-write-path.md`.
**Audience Review:** Auto-generated `{filename}.pptx-audience-review.yaml` (read-only, for reference)
**After save:** Call `vault_reindex(full=false, embed=false)`.

Example:
```
Artifacts/nwm/decks/2026-04-09-demand-planning-workshop.pptx
Artifacts/nwm/decks/2026-04-09-demand-planning-workshop.pptx.artifact.md
Artifacts/nwm/decks/2026-04-09-demand-planning-workshop.pptx-audience-review.yaml
```
