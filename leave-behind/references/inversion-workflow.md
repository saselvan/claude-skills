# Inversion Workflow — PPTX to Leave-Behind Brief

When building from a completed deck (Mode 1), the brief inverts the deck's hierarchy. This file documents the extraction and mapping process.

---

## The Core Principle: INVERT THE HIERARCHY

A deck and a brief are different documents:
- **Deck:** big headline + hidden speaker notes. Visual scaffolding for a live voice.
- **Brief:** the argument (currently in the notes) becomes the body prose; the slide headline becomes the section title; the visuals shrink to small inline figures.

The leave-behind stands alone on the recipient's screen after the meeting, with no one narrating.

---

## Step 1: Extract Everything from the Final PPTX

```python
from pptx import Presentation

def extract_deck(pptx_path):
    """Extract text and notes from every slide."""
    p = Presentation(pptx_path)
    slides = []
    for i, s in enumerate(p.slides, 1):
        slide_data = {"number": i, "texts": [], "notes": ""}
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                slide_data["texts"].append(sh.text_frame.text.strip())
        if s.has_notes_slide:
            slide_data["notes"] = s.notes_slide.notes_text_frame.text.strip()
        slides.append(slide_data)
    return slides
```

Per slide you get: on-slide text (headlines, captions) AND speaker notes (the real argument).

## Step 2: Map Deck Sections to Brief Sections

Not every slide becomes a section. Structural slides (title, section dividers, closing) become brief framing. Content slides become brief sections. Appendix slides are dropped.

| Deck slide type | Brief treatment |
|---|---|
| Title slide | Brief title + subtitle (the spine) |
| Section divider | Section header in the brief |
| Content slide with speaker notes | **Full section** — headline becomes title, notes become prose |
| Content slide without notes | Section title only — flag as thin, enrich from strategy/KB |
| Stat hero | Pull the number into inline prose ("$2.4M annually...") |
| Architecture diagram | Small inline figure with caption |
| Closing / CTA | Final section: "Where we go" |
| Appendix slides | Drop entirely — reference material doesn't belong in a brief |

### Typical HLS Deck → Brief Mapping

| Deck slides | Brief section |
|---|---|
| Title + shift | **The shift** (1 short para: old question → new question) |
| What they built | **Where you are today** (affirm the win) |
| Before/after diagram | **The gap** (prose, with the diptych as one small figure) |
| Dollar grid | **What it's worth** (numbers, modeled-not-claimed) |
| Flywheel | **How the value compounds** (optional small figure) |
| Access / unlock | **What changes when it's opened** |
| Questions + FDE | **Where we could go** (the ask, framed as builder's close) |

## Step 3: Write the Brief

For each mapped section:

1. **Section title** = the slide headline. If the deck was built right, this is already a conclusion. If it's a topic, rewrite it as a conclusion before proceeding.

2. **Body** = the speaker note, rewritten as prose. The note already contains the argument the presenter would have spoken. Strip stage directions (`[BEAT]`, `[BREATHE]`, "pause here," "if Danny asks") — those are presenter-only. Keep the substance. Convert bullet-form notes into connected paragraphs.

3. **Figures** = hero exhibits (diptych, flywheel, architecture) become small inline figures. Export from deck as PNG. Place at half-column width with a one-line caption. No full-bleed.

4. **Apply all Tier 2 integrity guardrails**: scrub named stakeholders, keep incumbent neutral, numbers modeled-not-claimed, no internal tool/analyst names.

## Step 4: Handle Thin Notes

If a slide has thin or missing notes, you're reconstructing the argument from headlines alone. Options:

1. **Enrich from strategy YAML** — if available, the `talk_track.script` field has the argument
2. **Enrich from knowledge base** — match the slide topic to knowledge atoms
3. **Flag to user** — mark the section `[THIN — speaker notes were sparse. Enriched from strategy/KB. Review.]`

Never silently invent the argument. If you can't reconstruct it from available sources, say so.

## Step 5: Output

- Write the brief as clean markdown first
- Render to PDF via markdown-to-pdf skill
- Title, section headers, prose body, small figures, quiet footer
- Serif or refined-sans body, generous margins
- One accent color, the customer's brand if known
- HBR-article feel, not deck-export feel
