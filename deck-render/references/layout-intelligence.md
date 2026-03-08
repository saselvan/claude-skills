# Layout Intelligence — Intent → Pattern → Template

This table is the single source of truth for slide layout selection. The rendering agent consults this table for every slide. Never guess a layout — look it up.

## How to Read This Table

1. **Start from the leftmost column that matches.** If you know the communication intent, start there. If you already know the content shape, start at Content Pattern.
2. **Follow across to get the template layout key and scaffold method.**
3. **Every row is READY.** All scaffold methods support their documented layouts. No workarounds needed.

## Primary Lookup: Intent → Content Pattern → Layout

| Communication Intent | Content Pattern | Template Layout Key | Scaffold Method | Notes |
|---|---|---|---|---|
| **Opening / deck title** | Title + subtitle | `title` | `add_title_slide()` | Variant "b" = text only (default). Variant "a" = hero image. |
| **Opening with hero image** | Title + subtitle + image | `title_alt` | `add_title_slide(variant="a")` | Image area on right. |
| **Topic transition** | Section heading | `section_break_1` through `_3` | `add_section_break(variant=1-3)` | Scaffold clamps to 3 variants. Auto-selects dark variants on dark theme. |
| **Explain one concept** | Title + body text (no visual) | `content_basic` | `add_content_slide("content_basic", {...})` | Single column, full width. ONLY when NO visual element exists. |
| **Explain one concept (light bg)** | Title + body on white | `content_basic_white` | `add_content_slide("content_basic_white", {...})` | White background variant. Light theme only. |
| **Explain with visual** | Title + body + image right | `content_card_right` | `add_content_slide("content_card_right", {...}, illustration={...})` | Text left, image right. Scaffold fills text placeholders and places image in card zone. |
| **Explain with visual (image emphasis)** | Title + small text + large image | `content_card_large` | `add_content_slide("content_card_large", {...}, illustration={...})` | Image dominates. Use when the visual IS the point. |
| **Explain with visual (image left)** | Image left + title + body right | `content_card_left` | `add_content_slide("content_card_left", {...}, illustration={...})` | Mirror of card_right. Vary with card_right to avoid repetition. |
| **Compare two things** | Left column vs right column | `content_2col` | `add_comparison(left_title, left_body, right_title, right_body)` | Before/after, old/new, competitor/us, Option A/B. |
| **Compare with accent colors** | Left vs right with visual treatment | `content_2col` | `add_comparison(..., left_accent="maroon", right_accent="green")` | Objection handling: maroon = pain, green = response. Before/after: muted/bright. |
| **Compare with icons** | Left vs right + icon spots | `content_2col_icon` | `add_comparison(..., layout="content_2col_icon")` | Same as 2col but with icon placeholders above each column header. |
| **Show 3 items equally** | 3 parallel items, no cards | `content_3col` | `add_content_slide("content_3col", {"title": "...", "col1": "...", "col2": "...", "col3": "..."})` | 3 text columns, no card backgrounds. |
| **Show 3 items with icons** | 3 items + icon spots | `content_3col_icon` | `add_content_slide("content_3col_icon", {"title": "...", "col1": "...", "col2": "...", "col3": "..."})` | 3 columns with icon placeholders above each. |
| **Show 3 capabilities/features** | 3 cards with descriptions | `content_3col_cards` | `add_card_grid(cards=[3 items])` | Designer-built card proportions with accent bars. Preferred for feature/capability slides. |
| **Show 4 items equally** | 2x2 card grid | `content_card_quad` | `add_card_grid(cards=[4 items])` | Template quad layout. |
| **Show 5-6 items** | Custom card grid | `blank` + custom draw | `add_card_grid(cards=[5+ items], cols=3)` | No template fits. Scaffold draws cards on blank canvas. |
| **Hero statistic** | Big number + context | `content_basic` | `add_stat_hero(page_id, stat, context, source)` | Centered, auto-sized. 80pt if stat <= 5 chars, 64pt if <= 8, 48pt otherwise. Context = stat_size/4, floor 16pt. |
| **Impactful quote** | Centered quote + attribution | `power_statement_2` | `add_quote()` | Dark background, italic white text. |
| **Bold statement** | Centered statement | `power_statement` | `add_content_slide("power_statement", {...})` | Single bold line, centered. |
| **Bold statement (variant 3)** | Centered statement alt | `power_statement_3` | `add_content_slide("power_statement_3", {...})` | Alternate power statement style. |
| **Bold statement (variant 4)** | Centered statement alt | `power_statement_4` | `add_content_slide("power_statement_4", {...})` | Alternate power statement style. |
| **Data comparison table** | Headers + rows | `blank` + custom table | `add_table()` | Blue header row (#2272B4), dark body rows. |
| **Process / journey** | Sequential steps | `blank` + custom timeline | `add_timeline()` | Style 1 = numbered circles on line. Style 2 = cards with arrows. |
| **Architecture (simple layers)** | Stacked horizontal bands | `blank` + custom bands | `add_architecture()` | Simple layers with component boxes. No flows or arrows. |
| **Architecture (complex flows)** | Tiers + corridor-routed flows | `blank` + custom draw | `add_architecture_advanced()` | Multiple flow types, scaling boundaries, corridor separation. Replaces D2/ELK. |
| **Partner / ecosystem logos** | Row of logos | `blank` + custom strip | `add_logo_strip()` | Adaptive background strip. Logo variant registry for auto-contrast. |
| **Closing / thank you** | Logo + contact | `closing` | `add_closing()` | Template provides centered Databricks logo. |

## Secondary Lookup: Content Shape -> Layout (Quick Reference)

| What's on the slide | Layout key | Scaffold call |
|---|---|---|
| Text only, single topic | `content_basic` | `add_content_slide("content_basic", {...})` |
| Text + image right | `content_card_right` | `add_content_slide("content_card_right", {...}, illustration={...})` |
| Text + image left | `content_card_left` | `add_content_slide("content_card_left", {...}, illustration={...})` |
| Text + large image (image IS the point) | `content_card_large` | `add_content_slide("content_card_large", {...}, illustration={...})` |
| 2 parallel things | `content_2col` | `add_comparison(...)` |
| 2 parallel things + accent colors | `content_2col` | `add_comparison(..., left_accent="maroon", right_accent="green")` |
| 2 parallel things + icons | `content_2col_icon` | `add_comparison(..., layout="content_2col_icon")` |
| 3 parallel things (short) | `content_3col` | `add_content_slide("content_3col", {col1, col2, col3})` |
| 3 parallel things + icons | `content_3col_icon` | `add_content_slide("content_3col_icon", {col1, col2, col3})` |
| 3 features with descriptions | `content_3col_cards` | `add_card_grid(cards=[3])` |
| 4 items | `content_card_quad` | `add_card_grid(cards=[4])` |
| Big number | `content_basic` | `add_stat_hero()` — auto-centered, auto-sized |
| Quote | `power_statement_2` | `add_quote()` |
| Bold statement | `power_statement` | `add_content_slide("power_statement", {...})` |
| Table | `blank` | `add_table()` |
| Timeline / process | `blank` | `add_timeline()` |
| Architecture layers | `blank` | `add_architecture()` |
| Logos | `blank` | `add_logo_strip()` — adaptive strip + variant registry |

## Anti-Patterns (Never Do This)

| Wrong approach | Why it fails | Correct approach |
|---|---|---|
| Image overlaid on `content_basic` | Text and image overlap — no reserved image zone | Use `content_card_right`, `content_card_left`, or `content_card_large` |
| Hand-drawn 3 cards on `blank` | Ignores designer-built card layout with proper proportions | Use `content_3col_cards` via `add_card_grid()` |
| Hand-drawn 2 columns on `blank` | Ignores template divider and column proportions | Use `content_2col` via `add_comparison()` |
| `content_basic` for everything | Wastes template variety, creates visual monotony | Match content shape to the right layout |
| Same layout on consecutive slides | Feels like a wall of text | Alternate between layout families |
| `power_statement` for body text | Statement layouts are for 1-2 lines max, not paragraphs | Use `content_basic` for multi-paragraph text |
| Raw logo URLs on dark slides | Dark logos vanish on dark backgrounds | Use `{"id": "databricks"}` — scaffold resolves white variant automatically |
| Manual `bg_strip_opacity` tuning | Guessing opacity is fragile | Let the scaffold auto-compute strip contrast via WCAG luminance |

## Logo Strip Intelligence

The scaffold handles logo contrast end-to-end. No caller tuning required.

### Logo Variant Registry

Pass `{"id": "databricks"}` instead of a raw URL. The scaffold resolves the correct variant for the slide background:

```python
# Preferred: let scaffold pick the right variant
deck.add_logo_strip(logos=[
    {"id": "databricks"},
    {"id": "spark"},
    {"id": "hadoop"},
    {"id": "python"},
], title="Technology Ecosystem")

# Fallback: raw URL for logos not in registry
deck.add_logo_strip(logos=[
    {"id": "databricks"},
    {"url": "https://example.com/custom-partner-logo.png", "width": 1.8, "height": 0.6},
], title="Partners")
```

**How it works:**
1. Scaffold checks slide background luminance (from theme)
2. If luminance < 0.2 (dark slide): uses `dark_bg` variant from registry (white/light logos)
3. If luminance > 0.6 (light slide): uses `light_bg` variant (dark logos)
4. In between: uses `dark_bg` (safer default)
5. If id not in registry: raises clear error with suggestion to use raw URL

**Registry includes:** databricks, spark, delta_lake, mlflow, unity_catalog, python, hadoop, docker, aws, azure, gcp, kubernetes, tableau, power_bi, snowflake, kafka, airflow, dbt, terraform, github. Additional logos added on request.

**Per-logo sizing is automatic** from registry defaults. Override with explicit `width`/`height` if needed.

### Adaptive Background Strip

The scaffold auto-computes the strip fill color using WCAG luminance:

- Dark backgrounds: strip blends toward white to hit minimum 1.5:1 contrast ratio
- Light backgrounds: strip blends toward dark
- Mid-range: picks the direction with more contrast
- `bg_strip_opacity` parameter exists as optional override (0.0-1.0) but should rarely be needed

### Agent Guidance for Logos NOT in Registry

When a logo is not in the registry and the caller must supply a raw URL:

1. Identify the logo's dominant colors from general knowledge
2. If dark-dominant on a dark slide: source a white/light variant URL if one exists publicly
3. If no light variant exists: the adaptive strip will provide some contrast, but note this in speaker notes as a visual limitation
4. Set explicit `width`/`height` for visual weight normalization (wordmarks wider, icons square)

## Illustration / Diagram Placement Intelligence

When a slide includes both text and a visual element (diagram, screenshot, illustration):

**Decision tree:**
1. Is the visual supplementary to the text, or IS IT the point?
   - Supplementary -> `content_card_right` (text dominant, image secondary)
   - The visual IS the point -> `content_card_large` (image dominant, text minimal)
2. Has the previous slide used `content_card_right`?
   - Yes -> use `content_card_left` for visual variety
3. Is the visual a full-width diagram (architecture, flow)?
   - Yes -> don't use a card layout. Use `blank` + `add_architecture()` or place the image below the title zone
4. **Never place an image on `content_basic` or `power_statement`.** These layouts have no reserved image zone.

**Scaffold call for illustration slides:**
```python
deck.add_content_slide("content_card_right", {
    "title": "The Lakehouse Architecture",
    "subtitle": "Combining data lakes and data warehouses",
    "body": "The lakehouse paradigm eliminates the need..."
}, illustration={
    "url": "https://example.com/lakehouse-diagram.png",
    "width": 5.0,
    "height": 3.5
})
```

## Stat Hero Sizing

The scaffold auto-sizes stat heroes. No caller tuning needed:

| Stat length | Font size | Example |
|---|---|---|
| <= 5 chars | 80pt | "< 15s", "72%", "$31K" |
| <= 8 chars | 64pt | "10-20x", "$400K/yr" |
| > 8 chars | 48pt | "1.2 million" |

Context text = stat_font_size / 4 (floor 16pt). Source text = 9pt. All centered.
