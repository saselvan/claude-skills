---
name: one-pager-render
description: "Render a polished one-pager as HTML→PDF with layer-by-layer evaluation. USE WHEN: user says 'render one-pager', 'build one-pager', 'make one-pager PDF', or when /build routes an artifact_type of 'one-pager'. Takes a strategy YAML (with one_pager_strategy block) + knowledge.md as input. Produces an executive-ready single-page PDF via layered build→evaluate→fix workflow."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
---

# One-Pager Render

You are an information designer, not a template filler. You build the one-pager in layers, evaluate each layer against expert heuristics, fix what fails, then move to the next layer. You do not write the full page and evaluate at the end.

## Before Writing Any Code

**Read ALL THREE reference files. They serve different purposes:**

1. `references/design-rules.md` — **Brand DNA.** Palettes, fonts, layout grid, spacing rules. Use DURING rendering to get colors, typography, and spacing right.
2. `references/one-pager-patterns.md` — **Tool mastery.** HTML table layout patterns, wkhtmltopdf pitfalls, typography, image handling, the complete HTML skeleton. Use DURING rendering to write correct markup.
3. `references/one-pager-philosophy.md` — **Expert judgment.** How to evaluate what you built. Use AFTER each layer to decide if it passes. Contains the 12-criteria rubric, 7 named failure modes, anti-pattern library, and variant matrix.

design-rules and one-pager-patterns tell you HOW. one-pager-philosophy tells you WHETHER.

### Audience Tailoring Engine (HLS domains)

If the one-pager's audience or domain involves healthcare/HLS/clinical content, read the shared tailoring map:

```
_System/tailoring/hls-tailoring-map.yaml   (relative to workspace/vault root)
```

This file defines 4 audience profiles (`clinical_executive`, `technical_gatekeeper`, `commercial_lead`, `customer_success`). Match the one-pager's target audience to the closest profile and use its `lava_element` for the hero metric, its `kill_list` to exclude irrelevant content (e.g., architecture patterns for executives), its `mental_model` for the framing metaphor, and its `card_types.exclude` as hard content exclusions.

## Board Read Protocol (Coordinated Mode)

Check the strategy contract (strategy YAML or strategy-contract.yaml) for a `_meta.board_dir` field.

**If `_meta.board_dir` is present** — you are running inside a coordinator pipeline:
1. Read `{board_dir}/invariants.yaml` if it exists (enablement-kit coordinator). These are HARD constraints:
   - `hero_message` — must appear in the one-pager (typically as the hero banner or lead sentence)
   - `proof_points[].assigned_to` — only use proof points assigned to "one-pager" or "all"
   - `competitive_frame` — use this positioning for any competitive comparison section
   - `call_to_action` — unified CTA must appear in the one-pager's closing section
2. Read `{board_dir}/board/` for prior skill outputs:
   - If `deck-render-output.yaml` exists: read `proof_points_used` and `hero_message_as_rendered` to ensure consistency. The one-pager must match the deck's hero message (exact or semantic equivalent).
   - If `cheatsheet-render-output.yaml` exists: read `proof_points_used` to avoid duplication. The one-pager should COMPLEMENT — use different proof points or different angles on shared ones.
   - Read `recommendations_for_downstream` entries where `target_skill` = "one-pager-render".
3. `{board_dir}/strategy-contract.yaml` (at the coordinator root, NOT in `board/`) is the LIVING strategy. Use it instead of any stale copy. Check its `version` field — higher = more recent amendments.

**If `_meta.board_dir` is absent** — standalone mode. Skip this section entirely. Zero cost.

## Board Write Protocol (Coordinated Mode)

**Only when `_meta.board_dir` is present.** Execute this AFTER Layer 5 (Final Evaluation) and BEFORE copying artifacts to the output location.

Write a board entry to `{board_dir}/board/one-pager-render-output.yaml`:

```yaml
skill_name: "one-pager-render"
invoked_at: "{ISO 8601 timestamp}"
invoked_by: "{coordinator name from _meta.coordinator}"

artifact_path: "{absolute path to final .pdf and .html}"
artifact_type: "one-pager"

# What the one-pager contains (for downstream skills to read)
hero_message_as_rendered: "{exact hero text from the one-pager}"
proof_points_used:
  - point: "{proof point text}"
    section: "{which section contains it}"
    treatment: "{how it was presented — stat callout, supporting evidence, etc.}"
competitive_frame_as_rendered: "{how competitive positioning landed, if any}"
variant_type: "{awareness|consideration|validation|champion|reference}"
word_count: N

# Quality from existing 12-criterion rubric
quality_score: N                        # total from rubric (0-24)
quality_max: 24
quality_pass: true/false                # >= 18
quality_notes: ""
standalone_comprehension: true/false    # can this be understood without a presenter?
forwarding_meta_test: true/false        # from existing forwarding test — would recipient forward this?
per_dimension_scores:
  audience_intentionality: N
  hero_clarity: N
  minto_structure: N
  word_budget: N
  section_count: N
  scan_path: N
  typography_hierarchy: N
  white_space: N
  proof_credibility: N
  cta_clarity: N
  visual_authenticity: N
  forwardability: N

# Amendments the one-pager discovered
strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []

recommendations_for_downstream:
  - target_skill: "enablement-card-render"
    recommendation: "{e.g., 'enablement card should reference the competitive comparison framing from the one-pager'}"
    priority: "medium"
```

Use the Write tool to create this file. If the file already exists (retry scenario), overwrite it.

**If `_meta.board_dir` is absent** — skip board write entirely. Do not create any files.

## SA Usage Guide: When to Reach for a One-Pager

A one-pager sits between an email (too ephemeral) and a deck (too heavy). Use it when you need a **leave-behind that survives forwarding** — something the champion sends to someone you haven't met.

| SA Deal Moment | One-Pager Variant | Hero Message Pattern | Trigger |
|---|---|---|---|
| **Post-Discovery** | `consideration` | "Based on what we heard, here's the architecture bet" | Session `meeting_type: discovery` with ≥3 pain points identified |
| **Post-Demo** | `validation` | "[Capability] addresses [their pain], reducing [metric] by [X]%" | Session `meeting_type: demo` with aha moment detected |
| **Architecture Review** | `validation` | "Agreed design: [approach] — prerequisites and next steps" | Session `meeting_type: architecture_review` with decisions made |
| **Pre-EBC** | `champion` | "Executive summary: why [initiative] and why now" | Session `meeting_type: ebc` scheduled, executive attendees |
| **Competitive Evaluation** | `validation` | "Side-by-side: why [our approach] wins on [their criteria]" | Competitive mention in transcript signals |
| **Stalled Deal** | `champion` | "Cost of inaction: [X] per month while [status quo continues]" | `going_dark` signal on active use case |

### Quick Invocation (Three Pillars)

For Mode 2 (no strategy YAML), provide these three things and the skill handles the rest:

1. **Audience Profile** — Role + their specific concern: *"For a CMIO worried about clinician burnout and EHR data silos"*
2. **Hero Message** — The one answer they should remember: *"Unified patient records reduce charting time by 40%"*
3. **Technical Atoms** — 2-3 constraints from discovery: *"3 legacy EHRs, 2s latency requirement, HIPAA required"*

### Orchestrator Integration

**Coordinator integration:** When running inside a coordinator pipeline (detected via `_meta.board_dir` in the strategy contract), the one-pager reads board state from prior skills and writes its own board entry after completion. When invoked standalone, behavior is unchanged. See Board Read/Write Protocol sections above.

The `/orchestrate` pipeline can also auto-trigger one-pager generation via `draft-followup`'s leave-behind assessment. In coordinated mode, the `post-meeting` coordinator reads the board entry and decides whether to invoke one-pager-render. Legacy queue paths are deprecated.

---

## Input Modes

### Mode 1: From Strategy YAML + Knowledge (preferred)
```
/one-pager-render path/to/strategy.yaml
```
Strategy provides the `one_pager_strategy` block with: variant_type, audience (role + deal_stage + cognitive_budget), hero_message, supporting_arguments, proof_strategy, competitive_frame, cta, word_budget, distribution_method, why_now, layout_pattern, visual_hierarchy. Knowledge.md provides atoms of content with confidence levels and sources.

### Mode 2: From Topic + Audience Description
```
/one-pager-render "Lakebase for HLS provider CIOs, consideration stage"
```
Plan the one-pager yourself. You MUST produce a strategy contract (see Strategy Contract Gate below) before rendering. Do not skip this — a one-pager without a defined variant and audience is a one-pager for no one.

### Mode 3: From Existing Content (rewrite/improve)
```
/one-pager-render path/to/existing-one-pager.md --rewrite
```
Read the existing content, score it against the 12-criteria rubric (one-pager-philosophy.md → Evaluation Rubric), identify failures, then rebuild using the layer workflow below. Emit the BEFORE score alongside the AFTER score at completion.

---

## Workflow: Layer-by-Layer Build-Evaluate Loop

A one-pager is a single page. There is no slide sequence to iterate through. Instead, you build in five layers. Each layer has an evaluation gate. Do not proceed to the next layer until the current layer passes.

### Setup (once per one-pager)

```bash
mkdir -p onepager rendered
```

Decide on the rendering approach based on `distribution_method` from strategy:

| Distribution Method | Rendering Approach | Why |
|--------------------|--------------------|-----|
| `email_pdf` | HTML → wkhtmltopdf | Clean PDF, predictable page breaks, works in all readers |
| `print` | HTML → wkhtmltopdf (300dpi) | Higher resolution for physical printing |
| `digital_room` | HTML standalone | Interactive links remain clickable |
| `slack_share` | HTML → wkhtmltopdf | PDF thumbnail renders in Slack |

Default to `email_pdf` if not specified.

### Strategy Contract Gate (mandatory)

Before writing any HTML, validate or create the strategy contract. This is a hard gate — do not render until this passes.

If the strategy YAML contains a `one_pager_strategy` block, validate it:

```
STRATEGY CONTRACT:
  variant_type:       [value] ✓|✗ (must be one of: awareness, consideration, validation, champion, reference)
  audience.role:      [value] ✓|✗ (must be a specific role, not "general")
  audience.deal_stage:[value] ✓|✗
  cognitive_budget:   [value] ✓|✗ (sections ≤ budget from variant matrix)
  hero_message:       [value] ✓|✗ (must contain a verb and point of view)
  supporting_args:    [count] ✓|✗ (2-3 required)
  proof_strategy:     [value] ✓|✗ (must name specific proof points)
  cta.action:         [value] ✓|✗ (must be specific, not "learn more")
  cta.secondary:      [value] ✓|✗ (must work for forwardee)
  framing_style:      [value] ✓|✗|N/A (if present in strategy via deck_mode.framing_style — loss|ease|recognition — use it for hero and proof framing. In coordinated mode, must match deck's framing.)
  word_budget:        [value] ✓|✗ (150-300 based on variant)
  why_now:            [value] ✓|✗ (must reference a time-bound trigger)
  layout_pattern:     [value] ✓|✗
CONTRACT: VALID | INVALID → [list what's missing]
```

If Mode 2 (no strategy YAML), generate the contract yourself by asking the user for clarifications or inferring from context. Emit the contract for approval before proceeding.

If INVALID, stop and request the missing fields. Do not guess at audience or hero message — these are the two inputs that, if wrong, invalidate everything downstream.

### Anti-Pattern Pre-Screen (mandatory)

Before rendering, check whether the planned content matches any of the 7 anti-patterns from one-pager-philosophy.md:

```
ANTI-PATTERN SCREEN:
  "The Wikipedia Page":     ✓ CLEAR | ⚠ AT RISK — word budget [X] exceeds 300
  "The Feature Laundry List": ✓ CLEAR | ⚠ AT RISK — [X] capabilities listed, no hierarchy
  "The Everything Bagel":   ✓ CLEAR | ⚠ AT RISK — [X] sections planned, budget is [Y]
  "The Accidental Insider":  ✓ CLEAR | ⚠ AT RISK — [list terms needing definition]
  "The Timeless Wonder":    ✓ CLEAR | ⚠ AT RISK — no why_now element found
  "The Pretty Nothing":     ✓ CLEAR | (evaluated after render)
  "The Checkmark Grid":     ✓ CLEAR | ⚠ AT RISK — competitive comparison planned with no nuance
SCREEN: CLEAR | [N] RISKS — [list mitigations]
```

If any anti-pattern is AT RISK, document how you will avoid it. Proceed only with mitigations noted.

---

### Layer 1: Information Architecture

**Build:** Define the page structure. No visual design yet — just the skeleton.

Write a plain-text outline:
```
HERO: [hero_message from strategy]
SECTION 1: [title] — [what content goes here] — [word budget allocation]
SECTION 2: [title] — [what content goes here] — [word budget allocation]
SECTION 3: [title] — [what content goes here] — [word budget allocation]
CTA: [action from strategy]
TOTAL SECTIONS: [count] vs BUDGET: [cognitive_budget]
TOTAL WORDS: [estimated] vs BUDGET: [word_budget]
```

**Evaluate — Philosophy Section 1 (Hierarchy):**
```
LAYER 1 EVAL:
  3-Second Test:    PASS|FAIL — Is the hero message clearly the dominant element in this architecture?
  Minto Structure:  PASS|FAIL — Is the answer in the top 20% of the planned layout?
  Section Count:    PASS|FAIL — [count] sections vs [cognitive_budget] budget
  Word Budget:      PASS|FAIL — [estimated] words vs [word_budget] target
  VERDICT:          CLEAN | FIX REQUIRED → [what to restructure]
```

Fix and re-evaluate until CLEAN. Do not write any HTML until Layer 1 passes.

### Layer 2: Content Population

**Build:** Write the actual content for each section. Pull from knowledge.md atoms. Respect confidence levels — do not use LOW confidence content without flagging it.

For each content atom used, track provenance:
```
CONTENT MAP:
  Hero: ← knowledge.md ATOM: [atom_name] | Confidence: [level]
  Section 1: ← knowledge.md ATOM: [atom_name] | Confidence: [level]
  Section 2: ← knowledge.md ATOM: [atom_name] | Confidence: [level]
  Proof point: ← knowledge.md ATOM: [atom_name] | Confidence: [level]
  ⚠ LOW CONFIDENCE: [list any atoms below HIGH]
```

**Evaluate — Philosophy Section 2 (Density):**
```
LAYER 2 EVAL:
  Word Count:       PASS|FAIL — [actual] words vs [word_budget] target
  Duarte Budget:    PASS|FAIL — Primary content 150-250 words (excl headers/CTA/footer)
  Tufte Erasure:    PASS|FAIL — Each section survives "cover and check" test
  Benefit Language:  PASS|FAIL — Features translated to benefits for this audience
  VERDICT:          CLEAN | FIX REQUIRED → [what to cut or rewrite]
```

Cut until it breathes. Every word on a one-pager has to earn its pixel.

### Layer 3: Visual Design & Render

**Build:** Write HTML + inline CSS. Single file, no external dependencies except brand fonts.

Key technical constraints (consult one-pager-patterns.md for details):

| Rule | Details |
|------|---------|
| Page size | Letter (8.5 × 11") with 0.5" margins. Content area: 7.5" × 10" |
| Font stack | System fonts preferred. Brand font via system install → system fallback. Consult design-rules.md |
| Typography | Hero: 20-32pt. Headings: 14-18pt. Body: 10-12pt. Min: 9pt. ≥4pt gap between levels. Use `pt` units. |
| Colors | Brand palette from design-rules.md. WCAG AA contrast (4.5:1 for text). Use 6-char hex `#RRGGBB` — avoid `rgba()`. |
| Layout | **HTML `<table>` elements** for all structural layout. CSS for styling only. See one-pager-patterns.md Section 2. No CSS Grid, no Flexbox. |
| White space | ≥0.3" between sections. Content never touches page edges. `overflow: hidden` on body and page container. |
| Line length | 45-75 characters per line. Use columns or max-width if single-column exceeds 75 |
| Images | Base64 in `<img>` tags or inline SVG. **No base64 in CSS `background-image`** (unreliable). No external URLs. |
| Print CSS | `@page { size: letter; margin: 0; }` + `-webkit-print-color-adjust: exact` in `@media print`. Pass `--print-media-type` flag. |
| Shadows | **No `box-shadow`** (unreliable). Use `border` for visual separation. |
| Opacity | **No `rgba()` or `opacity`** for backgrounds. Pre-calculate solid hex colors instead. |

```bash
# Render to PDF (Chrome headless — always generate PDF alongside HTML)
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu \
  --print-to-pdf=onepager/one-pager.pdf --no-margins --print-background \
  onepager/one-pager.html

# Convert to PNG for visual evaluation
pdftoppm -png -r 200 -singlefile onepager/one-pager.pdf rendered/one-pager
```

**Look at the PNG.** Run Philosophy Sections 3 and 4:

**Evaluate — Section 3 (Readability / Arm's Length Test):**
```
LAYER 3a EVAL:
  Fridge Test:      PASS|FAIL — From arm's length, can I read the hero and section headings?
  Type Hierarchy:   PASS|FAIL — [count] distinct levels with ≥4pt gaps
  Contrast:         PASS|FAIL — All text meets WCAG AA 4.5:1
  Line Length:      PASS|FAIL — Body text 45-75 characters per line
  Min Font Size:    PASS|FAIL — Nothing below 9pt
  VERDICT:          CLEAN | FIX REQUIRED → [what to fix]
```

**Evaluate — Section 4 (Scan Path):**
```
LAYER 3b EVAL:
  Scan Pattern:     PASS|FAIL — Matches intended [layout_pattern] from strategy
  Entry Point:      PASS|FAIL — One unambiguous starting point for the eye
  Gestalt Grouping: PASS|FAIL — Related items grouped (proximity), different items separated
  CTA Position:     PASS|FAIL — CTA in terminal visual position (bottom or bottom-right)
  Headings Story:   PASS|FAIL — Reading only headings tells the argument
  VERDICT:          CLEAN | FIX REQUIRED → [what to fix]
```

Fix CSS, re-render, re-evaluate until both CLEAN.

### Layer 4: Proof & Credibility

**Evaluate — Philosophy Section 5 (Skeptic Test):**
```
LAYER 4 EVAL:
  Attribution:      PASS|FAIL — Every stat has source + year
  Audience Match:   PASS|FAIL — Proof points match audience's industry/scale/use case
  Competitive Honesty: PASS|FAIL — No "total dominance" claims (if competitive section exists)
  Precision:        PASS|FAIL — No fake precision ("42.7% improvement" → "~40% improvement")
  Benefit Language:  PASS|FAIL — Features presented as benefits, not specs
  LOW CONF FLAGS:   [list any LOW confidence atoms still present]
  VERDICT:          CLEAN | FIX REQUIRED → [what to fix]
```

If any proof point uses a LOW confidence atom from knowledge.md, either: (a) replace with a HIGH confidence alternative, or (b) flag it visibly: "⚠ Proof point blocked — no verified source. One-pager ships with this gap noted."

### Layer 5: Final Evaluation

Re-render final PDF and PNG. Run the full 12-criteria rubric from one-pager-philosophy.md:

```
FINAL RUBRIC:
  #1  Audience Intentionality:  [0|1|2] — [reason]
  #2  Hero Clarity (3-Second):  [0|1|2] — [reason]
  #3  Minto Structure (BLUF):   [0|1|2] — [reason]
  #4  Word Budget:              [0|1|2] — [actual] words
  #5  Section Count:            [0|1|2] — [count] sections
  #6  Scan Path:                [0|1|2] — [pattern type]
  #7  Typography Hierarchy:     [0|1|2] — [level count], min [Xpt]
  #8  White Space:              [0|1|2] — [reason]
  #9  Proof Credibility:        [0|1|2] — [attribution status]
  #10 CTA Clarity:              [0|1|2] — [action specificity]
  #11 Visual Authenticity:      [0|1|2] — [magazine test result]

**Variant-specific visual test:**
- `awareness` → Would this pass as a thought leadership piece in HBR or MIT Sloan Review?
- `validation` → Would this pass as a McKinsey case study summary?
- `champion` → Would this pass as a polished internal strategy memo at a Fortune 500?
- `consideration` → Would this pass as an analyst brief from Forrester or Gartner?
- `reference` → Would this pass as a customer success story in a vendor's annual report?

  #12 Forwardability:           [0|1|2] — [cold read assessment]
  ─────────────────────────────────────
  TOTAL: [X]/24
  THRESHOLD: 18/24 (75%) = PASS | 22/24 (90%) = GREAT
  RESULT: PASS | FAIL → [list criteria scoring 0, fix these first]
```

**If FAIL (<18/24):** Identify all criteria scoring 0. These are structural failures. Fix them, re-render, re-score. Do not ship a one-pager that scores below 18.

**If PASS but not GREAT (18-21/24):** Identify criteria scoring 1. These are refinement opportunities. Fix what you can within reasonable effort, but do not loop indefinitely. Two fix cycles maximum at this stage.

Run the forwarding meta-test last (Philosophy Section 7):

```
FORWARDING TEST:
  "If the champion forwarded this to their CFO with just 'take a look,'
   would the CFO understand the value proposition and know what to do next?"
  ANSWER: YES | NO → [what's missing for the secondary reader]
```

---

## Design Principles (non-negotiable)

These apply to every one-pager. They are drawn from the expert research in one-pager-philosophy.md.

| Principle | What It Means In Practice |
|-----------|--------------------------|
| **BLUF** (Minto) | Hero message in the top 20% of the page. Always. |
| **150-250 words** (Duarte) | Primary content only. Headers, footers, CTA labels don't count. |
| **3-4 sections max** (Miller/Cowan) | Revised cognitive load research: 3-4 chunks, not 7±2. |
| **Design for scan** (Nielsen) | 79% of readers scan. Bold key terms. Numerals not words. Headings carry the argument. |
| **Arm's length** (Evergreen) | Design for 18-24 inch reading distance. If you can't read the hero from 4 feet on a wall, it's too small. |
| **No presenter** (Duarte) | If any section requires verbal explanation, that section is broken. |
| **Content > chrome** (Tufte) | Every pixel carries information, provides structure, or wastes space. Remove decorative elements. |
| **Consultancy, not template** | McKinsey/Bain/HBR aesthetic: whitespace, type hierarchy, meaningful color, precision of language. No icon walls, gradients, stock art, checkmark grids. |

---

## HTML Architecture

Single-file HTML. All styles in a `<style>` block. No external CSS, no JavaScript, no external images. **Consult `references/one-pager-patterns.md` for the full skeleton and all pitfall workarounds.**

Layout approach: **HTML `<table>` elements for structure. CSS for styling.** This is the same approach used by every polished HTML email — it renders identically in wkhtmltopdf, Puppeteer, WeasyPrint, and browsers. No layout workarounds needed.

Rendering constraints (from research — these are facts, not preferences):
- **All page layout via `<table>` with `cellpadding="0" cellspacing="0" border="0"`.**
- **Every `<td>` gets explicit `width` (%) and `valign="top"`.**
- **Nest tables** for sub-layouts (metric card rows, multi-column proof points).
- **No CSS Grid** — wkhtmltopdf silently stacks grid items vertically.
- **No Flexbox** — unreliable without explicit widths. Tables are simpler and reliable.
- **No `box-shadow`** — use `border` instead.
- **No `rgba()`** — use pre-calculated solid hex colors.
- **Base64 images in `<img>` tags only** — CSS `background-image` with base64 is unreliable.
- **`-webkit-print-color-adjust: exact`** is REQUIRED or background colors vanish.

### Layout Pattern → Table Structure

| layout_pattern | Table Structure | Zones |
|---------------|----------------|-------|
| `z_pattern` | `<td colspan="2">` hero → `<td width="55%">` + `<td width="45%">` → `<td colspan="2">` CTA | Hero (full width) → two columns → CTA (full width) |
| `layer_cake` | Single-column `<td>` per row, no colspan needed | Hero → Section 1 → Section 2 → Section 3 → CTA |
| `vertical_flow` | `<td colspan="2">` hero → `<td width="63%">` + `<td width="37%">` → `<td colspan="2">` CTA | Hero → primary + sidebar → CTA |

See `references/one-pager-patterns.md` Section 2 for complete table implementations of each pattern, and Section 8 for the full HTML skeleton.

---

## Output

After final evaluation passes:

```
✓ One-pager rendered: [filename].pdf
✓ Variant: [variant_type] | Audience: [role] at [deal_stage]
✓ Word count: [actual] / [budget] target
✓ Rubric score: [X]/24 ([PASS|GREAT])
✓ Content provenance: [N] atoms from knowledge.md, [N] HIGH confidence, [N] flagged
✓ Anti-patterns: [N] screened, [N] clear, [N] mitigated

Strategy Contract:
  Hero: [hero_message]
  Sections: [list]
  CTA: [action]
  Why Now: [trigger]
```

Copy final PDF and HTML to the output location specified by `/build` or the user.

### Symlink to Customer Folder

After the PDF is saved, symlink it into `~/Customer/[account]/02-Decks/` so it's accessible from Finder organized by account. The source file remains the source of truth.

**Account name mapping:** spaces → underscores (e.g., "Mayo Clinic" → "Mayo_Clinic").

```bash
# Create account folder structure if it doesn't exist
for sub in 01-Emails 02-Decks 03-Reference_Docs 04-Notebooks 05-Proposals 06-Meeting_Prep 07-Contracts_Legal 08-Screenshots; do
  mkdir -p ~/Customer/[account_folder]/$sub
done

# Symlink the one-pager
ln -sf /absolute/path/to/[filename].pdf ~/Customer/[account_folder]/02-Decks/[filename].pdf
```

- Use `-sf` (force) to overwrite stale symlinks if re-rendering
- Always use full absolute paths in the symlink target
- If the one-pager has no specific account, skip this step

## Reference Files

Read ALL THREE before starting any one-pager:
- **`references/design-rules.md`** — Brand palette, fonts, spacing rules, color usage
- **`references/one-pager-patterns.md`** — HTML/CSS rendering patterns, PDF conversion rules, image handling, pitfall catalog
- **`references/one-pager-philosophy.md`** — Evaluation rubric (12 criteria, 0-2 scoring, 18/24 pass threshold), 7 failure-mode diagnostics, variant matrix, anti-pattern library, strategy contract schema, expert principles (Minto, Evergreen, Tufte, Duarte, Nielsen, Cutler)

$ARGUMENTS
