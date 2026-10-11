---
name: leave-behind
description: "Produce a 2-3 page prose leave-behind brief that stands alone after the meeting ends. USE WHEN: user says 'leave-behind', 'brief', 'write up the meeting as a doc', 'reading document', or after a deck is delivered and needs a companion prose piece. Takes a completed .pptx, a strategy YAML + knowledge base, or raw meeting context. Outputs PDF via markdown-to-pdf."
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Leave-Behind Brief

You produce a reading document — not a slide dump, not an email, not a one-pager. This is a 2-3 page prose memo that carries the argument without a presenter's voice. The recipient reads it alone on their screen after the meeting.

**Voice:** Register 4 — narrative. Amazon 6-pager structure, Stripe prose texture. Section headers carry the spine when read alone. Plain, direct, unpretentious sentences a smart reader respects.

## Before Starting

Read `references/editorial-spec.md` — the editorial guardrails and voice rules.

## Input Modes

### Mode 1: From Completed Deck (.pptx)

The richest input. Invert the deck hierarchy:
- Slide headlines → section titles (already conclusions if the deck was built right)
- Speaker notes → prose body (the argument the presenter would have spoken)
- Hero exhibits → small inline figures (half-column width, one-line caption)

Read `references/inversion-workflow.md` for the extraction + mapping process.

### Mode 2: From Strategy YAML + Knowledge Base

No deck exists yet — build the brief directly from strategy.
- `sections_outline` → section structure
- `content_hierarchy.hero` per section → section titles
- `talk_track.script` per section → prose body (rewrite from spoken to written)
- Knowledge atoms → supporting evidence and data

### Mode 3: From Raw Meeting Context

Lightest input — user provides topic, audience, key points, and desired outcome. You build the argument from scratch applying the editorial spec.

## Process

### 1. Extract the Spine

Before writing anything, state the brief's spine in one sentence — the single through-line. Everything in the document serves this spine or gets cut.

```
Spine: "You governed it once — but the governance doesn't travel."
```

### 2. Map Sections

A brief has 4-6 sections max. Each section title is a declarative conclusion. Standard arc:

| Section | Purpose |
|---------|---------|
| The shift | Old question → new question (1 short para) |
| Where you are today | Affirm the win (IKEA effect) |
| The gap | The problem — prose, with one small figure if needed |
| What it's worth | Numbers, modeled-not-claimed |
| What changes | The resolution, framed as expansion |
| Where we go | The ask — decision the customer controls |

Adapt the arc to the content. Not every brief needs all six. Cut sections that don't serve the spine.

### 3. Write the Brief

**Per section:**
- Section title = declarative conclusion (headline test: "Does this read as a considered argument?")
- Body = 2-4 paragraphs of connected prose. No bullets unless listing discrete items.
- Figures = small inline, half-column, one-line caption. Never full-bleed.
- Tone = Stripe — plain, direct, sentences that earn respect through precision not decoration.

**Paragraph discipline:**
- One idea per paragraph
- Lead sentence carries the claim; following sentences provide evidence or context
- No "As you can see" or "It's worth noting" — just say the thing

### 4. Apply Integrity Guardrails (Tier 2)

Before finalizing, check every paragraph:

- [ ] No named stakeholders (reference roles, never names)
- [ ] Incumbent tool stays neutral (the villain is architecture, never a product)
- [ ] Numbers modeled-not-claimed ("Modeled on your revenue and volume" — never "you will save $X")
- [ ] Internal tool/analyst names scrubbed (credibility comes from their numbers, not our people)
- [ ] No shadow-IT / Excel shaming
- [ ] Affirm the win before any critique

### 5. Format and Deliver

**Structure:**
- Title (the spine, or a title that implies the spine)
- 4-6 section headers with prose body
- Small inline figures where they earn their space
- Quiet footer (date, "Prepared for [org]", no logos unless customer's)

**Output as PDF** using markdown-to-pdf skill:
- Serif or refined-sans body (never Inter, never monospace)
- Generous margins, readable at 100% zoom
- One accent color max (customer brand if known)
- No slide-y elements: no full-bleed images, no card grids, no pill badges

```bash
# After writing the .md, invoke markdown-to-pdf
# Output path follows artifact convention
```

**Length gate:** 2-3 pages. If it's longer, you're writing a report — cut. If it's shorter, you haven't developed the argument — expand the key sections.

## Output Convention

**Write path:** `Artifacts/{account-slug}/briefs/{YYYY-MM-DD}-{title-slug}.md` (source)
**PDF path:** `Artifacts/{account-slug}/briefs/{YYYY-MM-DD}-{title-slug}.pdf` (rendered)
**artifact_type:** `document`
**Sidecar:** Create `.artifact.md` alongside the PDF with canonical frontmatter.
**After save:** `vault_reindex(full=false, embed=false)`

## The Honest Caveat

Mode 1 (from deck) is only as good as the deck's speaker notes. If notes are thin, you're reconstructing the argument from headlines alone — weaker output. Flag this to the user and offer to enrich from strategy YAML or knowledge base.
