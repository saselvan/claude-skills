---
name: deck-render
description: "Render a polished PowerPoint deck one slide at a time with visual evaluation after each. USE WHEN: user says 'render deck', 'build slides', 'make pptx', 'create presentation from brief', or when a /deck prompt package needs visual execution. Takes either a prompt package file path, strategy YAML, or topic description as input. Produces an executive-ready .pptx via per-slide render→evaluate→fix loop."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
runtime-requires: multimodal-vision
---

> **Runtime Requirement:** This skill requires a multimodal environment where the Read tool can ingest images (PNG). The per-slide visual eval loop depends on the agent actually seeing rendered slides — not simulating a critique from code. In Cursor with Claude, this works natively. If ported to a text-only environment, the visual QA degrades to code-only heuristics and the quality guarantee is void.

# Deck Render

You are a presentation designer, not a template engine. You render one slide at a time, look at what you made, judge it honestly, fix what's wrong, then move on.

## CRITICAL: Visual Polish Standards

**Before rendering ANY slide, read the "Visual Polish Standards" section in `references/design-rules.md`.**

The #1 failure mode is creating text-wall slides that look like copy-pasted Word docs. Key rules:
- **NO TEXT WALLS** — Use cards/boxes for visual grouping
- **SPACING IS MANDATORY** — Cramped = unprofessional
- **COLOR-CODE BY MEANING** — Red/yellow/blue for severity/priority
- **COMPARISON SLIDES NEED COLUMN HEADERS** — "Vanilla PostgreSQL" vs "Lakebase" must be visible
- **CARD LAYOUTS FOR LISTS** — Use `addWarningCards` or `addCardGrid3Col`, not 2-column text

If a slide "looks like random crap," you violated these standards. Fix it before moving on.

### Evaluation Rubrics

"Judge it honestly" is not sufficient. Different slide types have specific visual failure modes. After rendering each slide, apply the appropriate rubric:

| Slide Type | Rubric | Location |
|---|---|---|
| Architecture diagrams | Architecture Eval Rubric | `references/architecture-eval-rubric.md` |
| All other slides | General Slide Eval (below) | This file |

**Architecture diagrams are the highest-risk slide type.** They have the most visual failure modes (overlapping labels, components outside tiers, wrong flow routing, legend collisions). The architecture rubric has 8 specific checks. Do not skip it.

### General Slide Eval (for non-architecture slides)

After rendering any slide, verify:
1. **No overlaps**: No text overlaps other text or shapes it doesn't belong to
2. **No clipping**: No text is truncated or extends beyond the slide edge
3. **Readability**: All text readable at projection size (nothing below ~9pt equivalent)
4. **Contrast**: All text has sufficient contrast against its background
5. **Layout match**: The rendered output matches the intended layout from layout-intelligence.md
6. **Content accuracy**: Text content matches the brief/strategy — no hallucinated stats or quotes

## Before Writing Any Code

**Read ALL FIVE reference files. They serve different purposes:**

1. `references/design-rules.md` — **Brand DNA.** Palettes, fonts, layout patterns, code snippets. Use DURING rendering.
2. `references/pptxgenjs-patterns.md` — **Tool mastery.** pptxgenjs API patterns, icon pipeline, pitfall avoidance. Use DURING rendering.
3. `references/deck-philosophy.md` — **Expert judgment.** How to evaluate what you rendered. Use AFTER rendering each slide.
4. `references/layout-intelligence.md` — **Layout selection.** Intent → content pattern → template layout. Consult BEFORE rendering each slide to pick the right layout. Never guess — look it up.
5. `references/architecture-eval-rubric.md` — **Architecture diagram QA.** Use AFTER rendering any architecture slide.

Do not skip any of these. design-rules and pptxgenjs-patterns tell you HOW. deck-philosophy tells you WHETHER. layout-intelligence tells you WHICH LAYOUT. architecture-eval-rubric tells you IF IT PASSES.

### Audience Tailoring Engine (HLS domains)

If the deck's audience or domain involves healthcare/HLS/clinical content, read the shared tailoring map:

```
_System/tailoring/hls-tailoring-map.yaml   (relative to workspace/vault root)
```

This file defines 4 audience profiles (`clinical_executive`, `technical_gatekeeper`, `commercial_lead`, `customer_success`) with per-profile: content priority order, kill lists (what to exclude), lava element (hero metric in #FF3621), red alert rules, and competitive positioning strategy. Match the deck's `audience.role` to the closest profile and use its `f_pattern_priority` to inform slide ordering, its `kill_list` to exclude irrelevant slides, and its `lava_element` for the hero data slide.

## Board Read Protocol (Coordinated Mode)

Check the strategy contract (strategy YAML or strategy-contract.yaml) for a `_meta.board_dir` field.

**If `_meta.board_dir` is present** — you are running inside a coordinator pipeline:
1. Read `{board_dir}/invariants.yaml` if it exists (enablement-kit coordinator). These are HARD constraints:
   - `hero_message` — must appear verbatim (or semantic equivalent) in the deck
   - `proof_points[].assigned_to` — only use proof points assigned to "deck" or "all"
   - `competitive_frame` — use this positioning, do not invent your own
   - `call_to_action` — unified CTA
2. Read `{board_dir}/board/` for any prior skill outputs. Deck is typically rendered FIRST in an enablement-kit, so the board may be empty. When it's not empty (e.g., content-factory re-renders after consistency failure), read prior outputs to understand what the coordinator wants fixed.
3. `{board_dir}/strategy-contract.yaml` (at the coordinator root, NOT in `board/`) is the LIVING strategy. Use it instead of any stale copy. Check its `version` field — higher = more recent amendments.

**If `_meta.board_dir` is absent** — standalone mode. Ignore this section entirely. Zero cost.

## Board Write Protocol (Coordinated Mode)

**Only when `_meta.board_dir` is present.**

After completing the deck-level review (after all slides pass per-slide eval AND the deck-level arc/rhythm check passes), write a board entry to `{board_dir}/board/deck-render-output.yaml`:

```yaml
skill_name: "deck-render"
invoked_at: "{ISO 8601 timestamp}"
invoked_by: "{coordinator name from _meta.coordinator}"

artifact_path: "{absolute path to final .pptx}"
artifact_type: "deck"

# What the deck actually contains (for downstream skills to read)
hero_message_as_rendered: "{exact hero text from the deck}"
proof_points_used:
  - point: "{proof point text}"
    slide_number: N
    treatment: "{how it was presented — stat hero, supporting evidence, etc.}"
competitive_frame_as_rendered: "{how competitive positioning landed}"
slide_count: N

# Quality from existing per-slide evaluation
quality_score: N                        # count of slides with CLEAN verdict
quality_max: N                          # total slides
quality_pass: true/false                # all slides CLEAN?
quality_notes: "{summary of any fixes applied}"
per_slide_scores:
  slide_1: { verdict: "CLEAN", layout: "title_slide" }
  slide_2: { verdict: "CLEAN", layout: "stat_hero" }
  # ... one entry per slide

# Amendments the deck discovered
strategy_contract_amendments:
  - field: "{e.g., design_decisions.color_system}"
    current_value: "{what strategy said}"
    recommended_value: "{what actually worked better}"
    reason: "{why}"
discovered_entities: []
coverage_gaps: []

recommendations_for_downstream:
  - target_skill: "cheatsheet-render"
    recommendation: "{e.g., 'cheatsheet should reference slide 4 terminology for consistency'}"
    priority: "medium"
```

Use the Write tool to create this file. If the file already exists (retry scenario), overwrite it.

**If `_meta.board_dir` is absent** — skip board write entirely. Do not create any files.

## Input Modes

### Mode 1: From Strategy YAML + Knowledge (preferred)
```
/deck-render path/to/strategy.yaml
```
Strategy provides per-slide: narrative_role, intent (emotion + action), audience_class, relationships (continues_from, sets_up, parallel_to), content hierarchy, talk tracks. Knowledge.md provides the atoms of content with confidence levels and sources.

### Mode 2: From Prompt Package
```
/deck-render path/to/prompt-package.md
```
Extract slide specs (Section B), strategy brief (Section A), talk tracks. Map layout types to visual patterns using the table below.

### Mode 3: From Topic Description
```
/deck-render "Why Lakebase exists alongside Delta Lake"
```
Plan the deck yourself: outline slides, decide narrative arc, pick palette. Then render.

### Layout Type Reference

When strategy or prompt package specifies a layout type, use this as a starting point — not a rigid template. Adapt based on content and context.

| Layout Type | Starting Pattern |
|-------------|-----------------|
| `title_slide` | Cover with geometric accents, centered title |
| `stat_hero` | One big number (48-72pt) with small supporting context |
| `feature_grid` | 2×3 or 3×1 card grid with accent bars + icons |
| `two_column_validation` | Two-column comparison cards |
| `before_after` | Before/After panels with contrasting color treatment |
| `architecture_diagram` | Flow diagram with boxes + arrows |
| `proof_points` | Customer story panels or metric cards |
| `comparison_table` | Styled dark table with colored highlights |
| `timeline` | Horizontal numbered phases |
| `discussion` | Numbered next-step cards |
| `story` | Quote card or narrative layout |
| `agenda` | Numbered items with accent dots |
| `objection_handling` | Myth/objection (maroon, italic) → Reality (green, bold evidence) |

## Workflow: Per-Slide Render-Evaluate Loop

This is the core workflow. Do not batch-render slides.

### Setup (once per deck)

```bash
# Dependency check — fail fast if rendering tools are missing
for cmd in libreoffice pdftoppm node npm; do
  if ! command -v $cmd &> /dev/null; then
    echo "ERROR: $cmd not found. Install before proceeding."
    echo "  brew install libreoffice poppler node  (macOS)"
    exit 1
  fi
done

# Install dependencies
npm install pptxgenjs react react-dom react-icons sharp 2>/dev/null

# Create working directories
mkdir -p slides rendered
```

Write a **scaffold script** that creates the presentation object, defines the palette, fonts, shadow factory, and pre-renders all icons. This script exports a function to add and save slides incrementally.

```javascript
// scaffold.js — shared setup for all slides
const PptxGenJS = require("pptxgenjs");
const pres = new PptxGenJS();
pres.layout = "LAYOUT_16x9";

// Palette from design-rules.md (official Databricks colors)
const C = {
  bg1: "0B2026", bgCard: "1B3139", bgLight: "303F47",
  lava: "FF3621", green: "00A972", blue: "2272B4", yellow: "FFAB00",
  maroon: "98102A",
  t1: "FFFFFF", t2: "DCE0E2", t3: "5A6F77"
};

const FH = "DM Sans";  // Databricks brand font (fallback: Trebuchet MS)
const FB = "DM Sans";  // (fallback: Calibri)

// Shadow factory — MUST be a function (pptxgenjs mutates shadow objects)
const shd = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.25 });

// Pre-render all icons needed for the deck
// ... react-icons → sharp → base64 pipeline from pptxgenjs-patterns.md ...

module.exports = { pres, C, FH, FB, shd, icons };
```

### Per-Slide Loop

For EACH slide in the strategy/outline:

#### Step 1: Read intent
Read the strategy for this slide: narrative_role, emotion, audience, relationships, content hierarchy, talk track.

**Long-deck refresh:** If this is slide 10, 15, 20, or any multiple of 5 beyond 10, re-read the `design_decisions` section from the strategy YAML. Context compaction can silently drop decisions from active memory on long decks.

#### Step 2: Design and render
Write a single-slide script that requires the scaffold and adds one slide:

```javascript
// slide-N.js
const { pres, C, FH, FB, shd, icons } = require("./scaffold");
const s = pres.addSlide();
s.background = { color: C.bg1 };

// ... design this slide based on strategy intent ...
// ... consult design-rules.md for patterns ...
// ... consult pptxgenjs-patterns.md for API usage ...
// ... consult layout-intelligence.md for layout selection ...

s.addNotes("Talk Track: " + talkTrackText);
pres.writeFile({ fileName: "wip.pptx" });
```

```bash
node slide-N.js
```

#### Step 3: Convert to PNG and evaluate

```bash
libreoffice --headless --convert-to pdf wip.pptx 2>/dev/null
pdftoppm -png -r 200 -l CURRENT_SLIDE_NUMBER -f CURRENT_SLIDE_NUMBER wip.pdf rendered/slide
```

**Look at the PNG.** Open `references/deck-philosophy.md` and run each check. You MUST emit a structured eval block before proceeding to Step 4.

```
EVAL Slide N: [slide title]
  S1-Hierarchy: PASS|FAIL — [one-line reason, including: is title insight-driven or descriptive?]
  S2-Density:   PASS|FAIL — [chunk count] chunks, budget = [X] for [audience]. Acronym count: [N] (max 2 exec, 4 technical)
  S5-Taste:     PASS|FAIL — [icon reuse? accent bar reuse? AI-generated feel?]
  S6-Proof:     PASS|FAIL — [attribution check or N/A]
  S7-Boundaries: PASS|FAIL — right-edge max: [X]" ≤ 9.5", bottom-edge max: [Y]" ≤ 5.1"
  S8-Decisions: PASS|FAIL|N/A — [which design decision this slide must honor, or N/A]
  S9-Contrast:  PASS|FAIL — [any critical text using t3 or lower on dark bg?]
  VERDICT:      CLEAN | FIX REQUIRED → [what to fix]
```

The checks in detail:
- **Section 1 (Hierarchy):** Can I tell what this slide is about in 3 seconds? Is there one clear hero element? Squint test: blur your vision — can you tell what's important from size/position alone? **Headline check:** Is the title insight-driven or just descriptive?
- **Section 2 (Density):** Count chunks — within budget for this audience? Max 2 acronyms for exec, 4 for technical.
- **Section 5 (Taste):** Does this look AI-generated? Check for: accent line reuse, centered body text, icon walls, equal-weight colors. Magazine test: would HBR/McKinsey use this treatment?
- **Section 6 (Proof):** If there's data, is it attributed? Is the hero number prominent enough?
- **Section 7 (Boundaries):** Calculate max(x + w) ≤ 9.5", max(y + h) ≤ 5.1". Math, not eyeballing.
- **Section 9 (Contrast):** Is critical text (hero stat, CTA, key label) using t3 or lower on dark bg? Critical text must use t1 or t2.

#### Step 4: Fix and re-render
If VERDICT = FIX REQUIRED, fix the slide script, re-render, re-evaluate. Emit a new EVAL block after each fix. Loop until VERDICT = CLEAN.

#### Step 5: Transition evaluation
Pull up the PREVIOUS slide's PNG alongside this one. Run deck-philosophy.md:

- **Section 3 (Rhythm):** Does this slide look different enough from the last 2-3 slides?
- **Section 4 (Narrative):** Does the visual treatment match the emotional shift? Does the transition feel natural?

**Rhythm hard limit:** If this slide's layout type matches the previous TWO slides (3 consecutive identical layouts), STOP. You must: (a) consolidate into fewer slides, (b) vary the layout, or (c) justify in writing why three identical layouts are narratively necessary.

Emit:
```
TRANSITION Slide N-1 → Slide N:
  S3-Rhythm:    PASS|FAIL — layout variety vs previous 2 slides: [layout types]
  S4-Narrative:  PASS|FAIL — emotional shift: [from what → to what]
  VERDICT:      CLEAN | FIX REQUIRED → [what to fix]
```

Fix if needed. Then move to the next slide.

### After All Slides: Deck-Level Review

```bash
# Convert final deck to PNG thumbnails
libreoffice --headless --convert-to pdf final-deck.pptx 2>/dev/null
pdftoppm -png -r 150 final-deck.pdf rendered/final
```

View ALL thumbnails together. Run deck-philosophy.md Section 7:

- **Arc check:** Do the narrative phases progress as strategy specified? Any phases missing?
- **Rhythm check:** Layout variety visible at thumbnail level? Is there a "moment" slide?
- **Time budget:** Total talk track time vs. meeting duration. No slide over 120s.
- **Thumbnail distinctiveness:** Can you tell slides apart from thumbnails alone?

Reorder, add section dividers, or cut slides if needed. Re-render affected slides.

## Critical Technical Rules

These are non-negotiable. They prevent file corruption and rendering bugs.

| Rule | Details |
|------|---------|
| Colors | 6-char hex, NO `#` prefix. `"FF3621"` not `"#FF3621"` |
| Shadows | NEVER reuse objects (pptxgenjs mutates them). Use factory: `const shd = () => ({...})` |
| Icons | react-icons → sharp → base64 PNG. Pre-render ALL before building slides |
| Text align | `margin: 0` when aligning text with shapes/icons |
| Bullets | `bullet: true`, NEVER unicode "•" |
| Multi-line | `breakLine: true` between text array items |
| Bullet spacing | Use `paraSpaceAfter: 12`, NEVER `lineSpacing` with bullets (causes huge gaps) |
| Layout | `LAYOUT_16x9` = 10" × 5.625" |
| Margins | 0.5" minimum from slide edges |
| Gaps | 0.3" minimum between content blocks |
| Shadow offset | Must be ≥ 0 (negative corrupts file) |
| Shadow opacity | Use `opacity` property, NEVER 8-char hex |
| Font sizes | Title: 28-36pt. Body: 14-18pt. Caption/source: 9-11pt. Stat hero: 48-72pt. Never below 9pt. |

## Script Architecture

**CRITICAL: No reusable slide-generation functions.** Never write a helper like `createPersonaSlide()` or `createPainSlide()` and call it multiple times with different data. This guarantees rhythm failure — identical layouts repeated mechanically. Each slide gets its own code block, designed individually after viewing the previous slide's PNG. Shared utilities for colors, fonts, shadows, and icons (in scaffold.js) are fine. Shared functions that produce entire slides are prohibited.

For decks longer than 5 slides, use a modular approach:

```
scaffold.js          — pres object, palette, fonts, shadow factory, pre-rendered icons
slide-01-cover.js    — title slide
slide-02-problem.js  — opening problem statement
slide-03-data.js     — data evidence
...
assemble.js          — requires scaffold, runs all slides in order, writes final file
```

For shorter decks (≤ 5 slides), a single file with block scoping is fine:

```javascript
// Each slide in its own block scope
{ const s = pres.addSlide(); /* slide 1 */ }
{ const s = pres.addSlide(); /* slide 2 */ }
```

## Talk Tracks → Speaker Notes

Every slide gets speaker notes from the strategy talk track. **Notes must be bullet points, not paragraphs.** An AE reading paragraph notes verbatim sounds robotic. Bullets let them glance and speak naturally.

```javascript
s.addNotes([
  "TALK TRACK (" + durationSeconds + "s):",
  "• " + bulletPoint1,
  "• " + bulletPoint2,
  "• " + bulletPoint3,
  "• Key transition: " + transitionToNext,
  "• If asked: " + anticipatedQuestion,
].join("\n"));
```

**Rules:**
- 3-7 bullets per slide, never a wall of text
- Each bullet is one idea, one sentence max
- Include a "Transition:" bullet that bridges to the next slide
- Include an "If asked:" bullet for the most likely audience question
- Duration estimate in the header helps the presenter pace themselves

## Output

After all slides pass evaluation, save the final deck and report:

```
✅ DECK COMPLETE
==================
File: path/to/final-deck.pptx
Slides: N
Quality: N/N slides CLEAN

Per-Slide Summary:
  Slide 1 (title_slide): CLEAN
  Slide 2 (stat_hero): CLEAN, 1 fix applied (contrast)
  ...

Generation time: Xs
Average: Y seconds per slide
```
