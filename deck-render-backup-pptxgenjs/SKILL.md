---
name: deck-render
description: "Render a polished PowerPoint deck one slide at a time with visual evaluation after each. USE WHEN: user says 'render deck', 'build slides', 'make pptx', 'create presentation from brief', or when a /deck prompt package needs visual execution. Takes either a prompt package file path, strategy YAML, or topic description as input. Produces an executive-ready .pptx via per-slide render→evaluate→fix loop."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
runtime-requires: multimodal-vision
---

> **Runtime Requirement:** This skill requires a multimodal environment where the Read tool can ingest images (PNG). The per-slide visual eval loop depends on the agent actually seeing rendered slides — not simulating a critique from code. In Cursor with Claude, this works natively. If ported to a text-only environment, the visual QA degrades to code-only heuristics and the quality guarantee is void.

# Deck Render

You are a presentation designer, not a template engine. You render one slide at a time, look at what you made, judge it honestly, fix what's wrong, then move on.

## Before Writing Any Code

**Read ALL THREE reference files. They serve different purposes:**

1. `references/design-rules.md` — **Brand DNA.** Palettes, fonts, layout patterns, code snippets. Use DURING rendering to get colors, typography, and layout right.
2. `references/pptxgenjs-patterns.md` — **Tool mastery.** API patterns, icon pipeline, pitfall avoidance. Use DURING rendering to write correct pptxgenjs code.
3. `references/deck-philosophy.md` — **Expert judgment.** How to evaluate what you rendered. Use AFTER rendering each slide to decide if it's good enough.

Do not skip any of these. design-rules and pptxgenjs-patterns tell you HOW. deck-philosophy tells you WHETHER.

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
Strategy provides per-slide: narrative_role, intent (emotion + action), audience_type, relationships (continues_from, sets_up, parallel_to), content hierarchy, talk tracks. Knowledge.md provides the atoms of content with confidence levels and sources.

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
const C = { /* ... from design-rules.md ... */ };
const FH = "Segoe UI"; // or brand font
const FB = "Segoe UI";
const shd = () => ({ type: "outer", blur: 3, offset: 2, color: "000000", opacity: 0.4 });

// Pre-render all icons needed for the deck
// ... react-icons → sharp → base64 pipeline ...

module.exports = { pres, C, FH, FB, shd, icons };
```

### Pre-Render Arc Gate (mandatory)

Before rendering any slide, map the full deck to narrative phases and validate ordering. This is a hard gate — do not render slide 1 until this passes.

1. **Identify meeting type:** Customer pitch, partner meeting, internal enablement, executive briefing, or technical deep-dive. This determines which emotional arc applies.

1b. **Bind audience profile (HLS decks only):** If the HLS tailoring map was loaded, match `audience.role` to a profile. Read `cognitive_budget_max`, `required_arc_peak`, `kill_list`, and `preferred_layouts` from the bound profile. Scan the proposed slide list and **purge** any slide whose topic matches a `kill_list` entry. Log each purge with reason.

2. **List every slide with its narrative_role** (WARM, DROWN, FEEL, REFRAME, SOLVE, PROVE, EQUIP, ACTION).

3. **Verify phase ordering:** DROWN or emotional peak must appear before any SOLVE slide. If SOLVE precedes problem establishment, stop and revise the strategy.

4. **Verify emotional peak exists (context-dependent):**
   - **Customer pitch:** FEEL slide required (patient story, human impact)
   - **Partner meeting:** OPPORTUNITY slide required (revenue, relationship value) — NOT a traditional FEEL slide
   - **Internal enablement:** EQUIP slide with confidence-building content
   - **Executive briefing:** REFRAME slide with strategic insight
   - **Technical deep-dive:** PROVE slide with validation evidence

   **If an HLS profile is bound**, use its `required_arc_peak` instead of the generic mapping above. The profile's peak overrides the meeting-type default (e.g., a customer pitch to a CISO uses PROVE, not FEEL).

   If the appropriate emotional peak for the meeting type is missing, add one. Don't force a FEEL slide into a partner meeting where it doesn't belong.

5. **Verify PROVE exists:** At least one slide must reference real evidence (customer story, attributed metric, third-party validation). If no evidence exists yet, flag it: "⚠ PROVE slide blocked — no customer evidence available. Deck ships with this gap visible."

6. **Verify "Why Us? Why Now?" triad (customer pitches only):**
   - **"Why Us?"** — at least one SOLVE or PROVE slide must contain a differentiator that a competitor cannot credibly claim. If every claim is generic ("scalable," "secure," "integrated"), flag it.
   - **"Why Now?"** — at least one EQUIP or ACTION slide must state the cost of inaction (revenue at risk, competitive window, compliance deadline). If urgency is missing, add it.

Emit the phase map in this format before proceeding:

```
ARC GATE:
  Meeting type: [customer pitch | partner meeting | enablement | exec briefing | technical]
  Required emotional peak: [FEEL | OPPORTUNITY | EQUIP | REFRAME | PROVE]

  # If HLS profile is bound:
  Bound Profile: [profile name]
  Cognitive Budget: [N] chunks max per slide
  Lava Element: [metric from profile]
  [PURGED] Slide: "[title]" (Reason: matches kill_list "[topic]")   ← one line per purged slide, or "None" if no purges

  Slide 1: WARM ✓
  Slide 2: WARM ✓
  Slide 3: DROWN ✓
  ...
  Slide 7: [EMOTIONAL PEAK] ✓   ← Required peak present
  ...
  Slide 10: SOLVE ✓             ← SOLVE after problem establishment ✓
  ...
  Slide 14: PROVE ✓             ← Evidence: [source]
  ...
PHASE ORDER: VALID
MISSING PHASES: None
TAILORING VERDICT: ALIGNED | NOT APPLICABLE   ← ALIGNED if profile bound and enforced, N/A if no HLS profile
```

If the phase map fails, revise the strategy outline and re-emit until it passes. Do not write any slide code until the arc gate passes.

### Design Decisions Gate (mandatory if present)

If the strategy YAML contains a `design_decisions` section, read it now. This section captures refinements made after the initial strategy — color systems, required messaging, layout overrides, visual treatments. **If a decision isn't in the YAML, it doesn't exist.** Conversational decisions that weren't written to the YAML will not survive context compaction and will be lost.

Emit an acknowledgment block listing every decision:

```
DESIGN DECISIONS:
  1. color_system: green/yellow/red qualification states
     → Affects slides: [list]
  2. required_messaging: "Why AI agents need databases" on slide 5
     → Affects slides: [list]
  3. layout_override: flowchart for qualification gate (slides 29-30)
     → Affects slides: [list]
ACKNOWLEDGED: [count] decisions will be enforced during rendering
```

Do not render until all decisions are acknowledged. During per-slide evaluation (Step 3), each affected slide must pass an S8-Decisions check confirming compliance. At deck-level review, emit a decisions summary confirming every decision landed.

### Per-Slide Loop

For EACH slide in the strategy/outline:

#### Step 1: Read intent
Read the strategy for this slide: narrative_role, emotion, audience, relationships, content hierarchy, talk track.

**Long-deck refresh:** If this is slide 10, 15, 20, or any multiple of 5 beyond 10, re-read the `design_decisions` section from the strategy YAML. Context compaction can silently drop decisions from active memory on long decks. This costs a few seconds per refresh and prevents drift on slides 15+.

#### Step 2: Design and render
Write a single-slide script that requires the scaffold and adds one slide:

```javascript
// slide-N.js
const { pres, C, FH, FB, shd, icons } = require("./scaffold");
const s = pres.addSlide();

// ... design this slide based on strategy intent ...
// ... consult design-rules.md for patterns ...
// ... consult pptxgenjs-patterns.md for API usage ...

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

**Look at the PNG.** Open `references/deck-philosophy.md` and run each check. You MUST emit a structured eval block before proceeding to Step 4. This is not optional — it is the audit trail that proves you ran the checks.

```
EVAL Slide N: [slide title]
  S1-Hierarchy: PASS|FAIL — [one-line reason, including: is the title insight-driven or just descriptive?]
  S2-Density:   PASS|FAIL — [chunk count] chunks, budget = [X] for [audience]. Acronym count: [N] (max 2 for exec, 4 for technical)
  S5-Taste:     PASS|FAIL — [one-line reason, specifically: icon reuse? accent bar reuse? AI-generated feel?]
  S6-Proof:     PASS|FAIL — [attribution check or N/A]
  S7-Boundaries: PASS|FAIL — right-edge max: [X]" ≤ 9.5", bottom-edge max: [Y]" ≤ 5.1"
  S8-Decisions: PASS|FAIL|N/A — [which design decision this slide must honor, or N/A if no decisions apply]
  S9-Contrast:  PASS|FAIL — [any critical text (hero stat, CTA, key label) using t3 or lower on dark bg?]
  VERDICT:      CLEAN | FIX REQUIRED → [what to fix]
```

The checks in detail:
- **Section 1 (Hierarchy):** Can I tell what this slide is about in 3 seconds? Is there one clear hero element? Squint test: blur your vision — can you tell what's important from size/position alone? **Headline check:** Is the title insight-driven ("Unity Catalog unifies governance") or just descriptive ("Architecture Overview")? Descriptive titles are only acceptable on section dividers.
- **Section 2 (Density):** Does this feel cramped? Count the chunks — is it within budget for this audience? If an HLS profile is bound, use its `cognitive_budget_max` as the hard limit instead of the generic table in deck-philosophy. **Acronym check:** Count acronyms on the slide. Max 2 for exec/mixed audiences, 4 for technical. Each must be in the audience's known fluency or spelled out on first use.
- **Section 5 (Taste):** Does this look AI-generated? Check for: accent lines (has this element appeared on 2+ previous slides?), centered body text, icon walls (same icon reused?), equal-weight colors. Apply the magazine test: would HBR/McKinsey/Economist use this treatment?
- **Section 6 (Proof):** If there's data, is it attributed? Is the hero number prominent enough?
- **Section 7 (Boundaries):** Calculate max(x + w) for all elements — must be ≤ 9.5" (0.5" right margin). Calculate max(y + h) — must be ≤ 5.1" (0.5" bottom margin). This is math, not eyeballing. If any element exceeds these bounds, it will clip in the final render. Common failure: flowcharts and multi-column layouts where rightmost elements extend past the safe zone.
- **Section 9 (Contrast):** Is any critical text (hero stat, CTA, key label) using t3 or lower on a dark background? Critical text must use t1 or t2 — t3 washes out on conference room projectors. Reserve t3 for footnotes and secondary labels only.

#### Step 4: Fix and re-render
If VERDICT = FIX REQUIRED, fix the slide script, re-render, re-evaluate. Emit a new EVAL block after each fix. Loop until VERDICT = CLEAN. Do not proceed to Step 5 with any FAIL in the eval block.

#### Step 5: Transition evaluation
Pull up the PREVIOUS slide's PNG alongside this one. Run deck-philosophy.md:

- **Section 3 (Rhythm):** Does this slide look different enough from the last 2-3 slides?
- **Section 4 (Narrative):** Does the visual treatment match the emotional shift from strategy? Does the transition feel natural? Does this slide set up the next one?

**Rhythm hard limit:** If this slide's layout type matches the previous TWO slides (3 consecutive identical layouts), STOP. You must do one of: (a) consolidate the repeated content into fewer slides (e.g., table or comparison layout), (b) vary the layout for this slide, or (c) justify in writing why three identical layouts are narratively necessary — and that justification must reference a specific passage in deck-philosophy.md. "The content requires it" is not sufficient justification.

Emit a structured transition block:

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
- **Decisions compliance:** If `design_decisions` existed in strategy, emit a summary confirming every decision landed:

```
DECISIONS COMPLIANCE:
  1. color_system: green/yellow/red → HONORED on slides [list] | VIOLATED on slides [list]
  2. required_messaging: "agents need databases" → HONORED on slide 5 | MISSING
  3. layout_override: flowchart for qualification → HONORED on slides 29-30 | NOT IMPLEMENTED
RESULT: [all honored | N violations requiring fix]
```

This is the scannable audit trail. If any decision shows VIOLATED or MISSING, fix the affected slides before shipping.

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
| Layout | `LAYOUT_16x9` = 10" × 5.625" |
| Margins | 0.5" minimum from slide edges |
| Gaps | 0.3" minimum between content blocks |
| Shadow offset | Must be ≥ 0 (negative corrupts file) |
| Shadow opacity | Use `opacity` property, NEVER 8-char hex |
| Font sizes | Title: 28-36pt. Body: 14-18pt. Caption/source: 9-11pt. Stat hero: 48-72pt. Never below 9pt. |

## Cross-Cutting Deck Standards

Apply these to EVERY slide unless the user will import into a branded template (Google Slides, Keynote, corporate PowerPoint) that provides its own chrome. **Ask early:** "Will this be imported into a branded template?" If yes, skip slide numbers, footers, and logo placement — the template handles all of that.

### Slide Numbers & Confidentiality Footer (skip if using branded template)
If rendering a standalone .pptx that won't be imported into a template, add these to every slide:

```javascript
function addChromeElements(s, slideNum, totalSlides) {
  // Confidentiality footer (bottom-left)
  s.addText("Confidential", {
    x: 0.3, y: 5.3, w: 2.5, h: 0.25,
    fontSize: 7, fontFace: FB, color: C.t3,
    align: "left", valign: "middle", margin: 0,
  });
  // Slide number (bottom-right)
  s.addText(`${slideNum} / ${totalSlides}`, {
    x: 9.0, y: 5.3, w: 0.8, h: 0.25,
    fontSize: 8, fontFace: FB, color: C.t3,
    align: "right", valign: "middle", margin: 0,
  });
}
```

### Data Consistency Gate
Before rendering, cross-check ALL numbers, stats, and claims used in the deck against the source material (demo script, strategy YAML, knowledge.md). If a stat appears as "$31K" in the deck but "$25K-$40K" in the demo script, the audience will catch it. Pick one and use it everywhere. Emit a data consistency check in the pre-render arc gate:

```
DATA CONSISTENCY:
  "$25-40K" — used on slides [2, 4], matches demo script ✓
  "10-20%" — used on slides [2, 4], matches knowledge.md ✓
  "~15 seconds" — used on slides [3, 6], matches architecture doc ✓
RESULT: CONSISTENT
```

### Template Compatibility
If the user plans to convert the .pptx to Google Slides, Keynote, or a branded corporate template:
- **Skip logo placement** on the title slide — the template provides this
- **Skip brand-specific title formatting** — the template overrides this
- **Focus on content and layout** — the template handles chrome (headers, footers, slide masters)
- **Ask early:** "Will this be imported into a branded template?" This avoids wasted effort on branding that will be replaced.

### Product/App Decks Must Show the Product
If the deck is about a tool, application, dashboard, or visual product, **at least one slide must include a screenshot or mockup.** A deck about an app that contains zero imagery of the app is an abstract brief, not a presentation. If a live screenshot is unavailable, add a styled placeholder: a card with a muted image icon and "Replace with app screenshot" text.

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

## Symlink to Customer Folder

After the deck file is saved, symlink it into `~/Customer/[account]/02-Decks/` so it's accessible from Finder organized by account. The vault file remains the source of truth.

**Account name mapping** (vault account → folder name): spaces → underscores (e.g., "Mayo Clinic" → "Mayo_Clinic").

**Run via Bash after saving the .pptx:**
```bash
# Create account folder structure if it doesn't exist
for sub in 01-Emails 02-Decks 03-Reference_Docs 04-Notebooks 05-Proposals 06-Meeting_Prep 07-Contracts_Legal 08-Screenshots; do
  mkdir -p ~/Customer/[account_folder]/$sub
done

# Symlink the deck
ln -sf /absolute/path/to/[filename].pptx ~/Customer/[account_folder]/02-Decks/[filename].pptx
```

- Use `-sf` (force) to overwrite stale symlinks if re-rendering
- Always use full absolute paths in the symlink target
- If the deck has no specific account (e.g., internal enablement), skip this step

---

## Output

After deck-level review passes:

```
✓ Deck rendered: [filename].pptx ([N] slides)
✓ Per-slide QA: [N] slides evaluated, [X] fixes applied
✓ Transition QA: [N-1] transitions verified
✓ Deck-level QA: Arc complete, rhythm varied, time budget [X]min / [Y]min meeting
✓ Design decisions: [N] acknowledged, [N] honored, [X] violated

Slides:
1. [title] — [layout type] — [narrative role]
2. [title] — [layout type] — [narrative role]
...
```

## Reference Files

Read ALL THREE before starting any deck:
- **`references/design-rules.md`** — Brand palette, layout patterns, typography, element code snippets
- **`references/pptxgenjs-patterns.md`** — Icon pipeline, API patterns, script structure, pitfall catalog
- **`references/deck-philosophy.md`** — Visual evaluation rubric, failure mode diagnostics, Challenger arc guidance, per-slide and deck-level review checklists

$ARGUMENTS
