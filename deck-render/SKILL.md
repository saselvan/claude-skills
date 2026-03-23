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
2. `references/layout-intelligence.md` — Unified layout keys, strategy-to-scaffold mapping, code patterns, anti-patterns. Consult BEFORE each slide.
3. `references/eval-checklist.md` — Per-slide evaluation checks S1-S11. Re-read BEFORE each eval.

Read ON DEMAND (not at startup):
- `references/deck-philosophy.md` — Full narrative philosophy. Read ONCE at deck-level review (after all slides).
- `references/architecture-eval-rubric.md` — Architecture diagram QA. Read ONLY when evaluating architecture slides.
- `references/board-protocol.md` — Board read/write for coordinated mode. Read ONLY if `_meta.board_dir` present in strategy.

### Audience Tailoring (HLS domains)

If healthcare/HLS content, read `_System/tailoring/hls-tailoring-map.yaml` and match audience to closest profile.

## Board Protocol (Coordinated Mode)

If `_meta.board_dir` is present in the strategy YAML, read and follow `references/board-protocol.md`. If absent — standalone mode, ignore entirely. Zero overhead.

## Input Modes

### Mode 1: From Strategy YAML + Knowledge (preferred)
Strategy provides per-slide directives including:
- narrative_role, register (high/low), audience_chunks, loss_frame (bool)
- Image manifest (paths or "shape-based" fallback)
- Explicit cta block for closing slide

### Mode 2: From Prompt Package
Extract slide specs, strategy brief, talk tracks. Map layout types via layout-intelligence.md.

### Mode 3: From Topic Description
Plan the deck: outline slides, narrative arc, palette. Then render.

### CTA Enforcement

Strategy YAML must have a cta block:
```yaml
closing:
  cta_primary: "Scope a 2-week POV with your referral data"
  cta_contact: "Samuel Selvan, SA"
  cta_timeline: "Workshop available next Thursday"
```
Refuse to render closing without `cta_primary`. Flag generic CTAs ("Schedule a demo", "Let's connect").

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
  theme: dark  # or "light"
```
Dark theme: fully implemented. Light theme: palette values defined but layout functions and eval criteria not yet tuned. Use dark unless specifically requested. If light is requested, emit warning: "Light theme available but incomplete — dark recommended."

### Per-Slide Loop

For EACH slide in the strategy:

#### Step 1: Read intent and source visuals

- Read strategy directives for this slide (register, audience_chunks, loss_frame, image, etc.)
- Image resolution: strategy manifest specifies images upfront. Use what's given. If no image provided and one would help, build shape-based with speaker note: "Enhancement: replace with [description]." No mid-render blocking questions.
- Architecture slides: delegate to diagram or arch-diagram skill, save to images/, embed output. Don't build complex architecture from pptxgenjs shapes.
- Long-deck refresh: every 5th slide, re-read scaffold.js `design_decisions` section.

#### Step 2: Design and render

Consult layout-intelligence.md for layout selection. Layout functions are vocabulary, not stamps — **never call the same layout function for consecutive slides.**

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

NOW read deck-philosophy.md (full file, one time).

```bash
libreoffice --headless --convert-to pdf final-deck.pptx 2>/dev/null
pdftoppm -png -r 150 final-deck.pdf rendered/final
```

View all thumbnails. Run deck-philosophy.md Section 7 checks:
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
  "- [PAUSE] \"Referral leakage costs...\" [LET THE NUMBER LAND]",
  "- $2.4M annually -- that's not a Databricks estimate, that's your claims data",
  "- [SOFTER] And that's just the referrals you can track",
  "- Transition: \"So what does this actually look like for a patient?\"",
  "- If asked: \"How did you calculate that?\" -> \"We ran your FY24 claims...\"",
].join("\n"));
```

**Delivery cue mapping** (applied silently from narrative_role — no phase labels in notes):
- High-stakes data slides: [PAUSE] before hero stat, [LET IT LAND] after
- Emotional/personal slides: [SOFTER], [SLOWER]
- Insight/disruption slides: [DIRECT], [PAUSE FOR REACTION]
- Solution/capability slides: [CONFIDENT PACE]
- Action/closing slides: [SPECIFIC], [NAME THE NEXT STEP]

**Rules:** 3-7 bullets, one idea per bullet, include Transition and If Asked bullets.

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
Quality: N/N slides CLEAN (self-eval + deck-qa)

Per-Slide Summary:
  Slide 1 (title): CLEAN
  Slide 2 (stat_hero): CLEAN, 1 fix applied (contrast)
  ...

Scripts: slides/ directory preserved for revision
Eval log: eval-log.md
```
