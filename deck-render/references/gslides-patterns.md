# Google Slides API Patterns

Reference for `gslides_scaffold.py` — the DeckBuilder API for `deck-render` skill.

## Setup

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/deck-render/references"))
from gslides_scaffold import DeckBuilder, C, CL, FONT, FH, FB

deck = DeckBuilder("My Deck", theme="dark")
```

DeckBuilder copies the Databricks Corporate Template, scans it for layout IDs and background rects, and defers sample slide cleanup until the first slide is added (prevents master garbage collection).

## Coordinate System

- **Canvas:** 13.33" x 7.5" (Databricks Corporate Template, 16:9)
- **EMU:** 1 inch = 914400 EMU. Use `gb.inches_to_emu(x)` — never hardcode.
- **Content zone:** y = 2.175" to y = 6.713" (height ~4.538")
- **Margins:** 0.833" all edges
- **Content width:** 11.667" (SLIDE_W - 2 * MARGIN)
- **Footer:** y = 7.079"

Constants: `SLIDE_W`, `SLIDE_H`, `MARGIN`, `CONTENT_TOP`, `CONTENT_BOTTOM`, `CONTENT_HEIGHT`, `CONTENT_W`, `FOOTER_Y`

## Two Slide Creation Paths

### Path 1: Template-Native (preferred)

Keeps template placeholders, fills them via `replace_shape_text()`, clears unfilled. Auto-applies dark theme overrides on shared content layouts.

```python
s = deck.add_title_slide("Title", "Subtitle")        # uses template title layout
s = deck.add_section_break("Section Name")            # uses artistic divider layout
s = deck.add_content_slide("content_a_basic", {...})  # fills template placeholders
s = deck.add_comparison(before={...}, after={...})    # 2-column template layout
s = deck.add_card_grid(title="...", cards=[...])      # 3-col or quad template
s = deck.add_quote("Quote text", "Attribution")       # Power Statement 2
s = deck.add_closing("Thank You", "email@db.com")     # closing layout + text boxes
```

### Path 2: Custom Canvas

Deletes ghost placeholders, gives a blank slide for hand-placed elements.

```python
s = deck.add_slide("blank")
deck.set_background(s, "bg")
deck.add_section_label(s, "SECTION", "lava")
deck.add_slide_title(s, "Custom Layout")
deck.add_card(s, x, y, w, h, accent="blue", title="...", body="...")
```

**When to use which:** Template-native for standard slide types. Custom canvas for architecture diagrams, timelines, bespoke layouts, or any slide not covered by a template layout.

## Template-Native Methods

### add_title_slide(title, subtitle=None, variant="b")

```python
s = deck.add_title_slide("Databricks for Healthcare", "From data to insight")
```
- variant "b" (default): Text-only, CENTERED_TITLE. Dark/light auto-resolved.
- variant "a": With hero image area, TITLE placeholder.
- Auto-font-size reduction: <=40 chars → 44pt, <=60 → 36pt, <=90 → 32pt, >90 → 28pt.
- **Warning:** Titles over 120 chars will clip even at 28pt. Use `\n` to break lines.

### add_section_break(title, variant=1)

```python
s = deck.add_section_break("The Problem", variant=2)
```
- variant 1-3 rotates Artistic Divider styles.
- Auto-uses dark variant when `theme="dark"`.

### add_content_slide(layout_name, content, illustration=None)

**Layout-aware fill logic (v3):** Now supports card layouts and multi-column layouts. No longer destroys non-BODY(0) placeholders.

| Layout family | Content dict keys | Illustration param |
|---|---|---|
| `content_basic`, `content_basic_white` | `title`, `subtitle`, `body` | Not supported (ignored) |
| `power_statement`, `power_statement_3`, `power_statement_4` | `title`, `body` | Not supported |
| `content_card_right`, `content_card_left`, `content_card_large` | `title`, `subtitle`, `body` | **Required** — `{"url": str, "width": float, "height": float}` |
| `content_2col`, `content_2col_icon` | `title`, `left_body`, `right_body` | Not supported |
| `content_3col`, `content_3col_icon` | `title`, `col1`, `col2`, `col3` | Not supported |

**Basic example:**
```python
s = deck.add_content_slide("content_basic", {
    "title": "The Analytics Gap",
    "subtitle": "Why it matters",
    "body": "Supporting text here"
})
```

**Card layout example:**
```python
s = deck.add_content_slide("content_card_right", {
    "title": "The Lakehouse Architecture",
    "subtitle": "Combining data lakes and data warehouses",
    "body": "The lakehouse paradigm eliminates the need to maintain separate systems."
}, illustration={
    "url": "https://example.com/lakehouse-diagram.png",
    "width": 5.0,
    "height": 3.5
})
```

**3-column example:**
```python
s = deck.add_content_slide("content_3col", {
    "title": "Three Pillars of the Lakehouse",
    "col1": "Built on open standards and open source. No vendor lock-in.",
    "col2": "One platform for all data workloads. No ETL between systems.",
    "col3": "Shared workspace for engineers, scientists, and analysts."
})
```

- Returns page_id for adding custom elements on top (stat hero, callout bar, etc.).
- Dark theme: auto-overrides bg to Navy 900, forces t1/t2 text colors.
- **Behavior on multi-column layouts:** Unfilled placeholders are cleared (empty text), not deleted. This preserves template layout structure.

**Layout aliases:**

| Alias | Template Layout |
|-------|----------------|
| `content_a_basic` / `content_basic` | 7 Content A - Basic |
| `content_b_2_column` / `content_2col` | 9 Content B - 2 Column |
| `content_c_3_column_cards` / `content_3col_cards` | 13 Content C - 3 Column Cards |
| `content_d_card_quad` / `content_card_quad` | 17 Content D - Card Quad |
| `content_card_right` | Content with image right |
| `content_card_left` | Content with image left |
| `content_card_large` | Content with large image |
| `content_3col` | 3-column text |
| `content_3col_icon` | 3-column with icons |
| `blank` | Content E - Blank |
| `power_statement` | Content E - Power Statement 1 |
| `power_statement_2` | Content E - Power Statement 2 |
| `power_statement_3` | Content E - Power Statement 3 |
| `power_statement_4` | Content E - Power Statement 4 |

### add_comparison(before, after, title=None, left_accent=None, right_accent=None, layout="content_2col")

```python
s = deck.add_comparison(
    before={"title": "Before", "points": ["Siloed data", "Slow queries"]},
    after={"title": "After", "points": ["Unified lakehouse", "Seconds to insight"]},
    title="The Transformation"
)
```
- Uses content_b_2_column layout by default.
- Template provides a vertical divider between columns.
- `points` list becomes bulleted text.

**Accent color example (objection handling, before/after):**
```python
s = deck.add_comparison(
    before={"title": "Traditional Approach", "points": ["Siloed warehouses", "Manual governance", "Months to deploy ML"]},
    after={"title": "Lakehouse Approach", "points": ["Unified platform", "Automated governance with UC", "Days to production"]},
    title="Before & After",
    left_accent="maroon",
    right_accent="green"
)
```
- `left_accent`/`right_accent`: color key strings (e.g., `"maroon"`, `"green"`, `"blue"`). Draws thin vertical accent bar on left edge of each column card.

**Icon variant example:**
```python
s = deck.add_comparison(
    before={"title": "Before", "points": ["..."]},
    after={"title": "After", "points": ["..."]},
    layout="content_2col_icon"
)
```

### add_card_grid(title=None, subtitle=None, cards=[], cols=None)

```python
# 3 cards → uses template 3-column cards layout
s = deck.add_card_grid(
    title="Key Results",
    cards=[
        {"title": "Providence", "body": "Scaled to 1,000 clinics"},
        {"title": "Geisinger", "body": "40% faster analytics"},
        {"title": "Mayo Clinic", "body": "Population-scale genomics"},
    ]
)

# 4 cards → uses template quad layout
s = deck.add_card_grid(title="Four Pillars", cards=[...four...])

# Other counts → custom-drawn cards on blank canvas
s = deck.add_card_grid(title="Five Items", cards=[...five...], cols=3)

# Per-card icons — forces custom-drawn path for positioning control
s = deck.add_card_grid(
    title="Key Capabilities",
    cards=[
        {"title": "Unity Catalog", "body": "Unified governance", "color": "green",
         "icon": "https://example.com/icon.png"},
        {"title": "Delta Lake", "body": "ACID transactions", "color": "blue",
         "icon": "https://example.com/icon.png"},
    ]
)
```

- If any card has an `icon` key, the custom-drawn path is forced (bypasses template 3-col/quad) for full positioning control.
- Icons render as colored circles above each card with the image centered inside.
- **No icon name mapping** — `icon` must be a direct PNG/JPEG URL (e.g., `"https://example.com/icon.png"`).
- SVG URLs will fail silently (Slides API limitation). Use distinct URLs per card to avoid visual repetition.

**Dark theme note:** Card text on 3-col and quad layouts keeps template-inherited dark colors because the card shapes have light backgrounds. Only the main title/subtitle get dark overrides.

### add_quote(quote, attribution=None)

```python
s = deck.add_quote(
    "The lakehouse changed how we think about clinical data.",
    "Chief Data Officer, Regional Health System"
)
```
- Uses Power Statement 2 layout (DARK1 bg).
- Forces white italic text on quote (36pt), gray on attribution (18pt).
- Quotes auto-wrapped in curly quotes.

### add_closing(title=None, subtitle=None)

```python
s = deck.add_closing("Thank You", "samuel.selvan@databricks.com")
```
- Template provides centered Databricks logo.
- Title/subtitle added as text boxes (no text placeholders on closing layouts).

### add_timeline(steps, title=None, style=1)

```python
# Style 1: Numbered circles on horizontal connector line
s = deck.add_timeline(
    steps=[
        {"title": "Discovery", "body": "Identify data sources", "color": "blue"},
        {"title": "Ingestion", "body": "Bronze layer landing", "color": "green"},
        {"title": "Transformation", "body": "Silver/gold via DLT", "color": "yellow"},
        {"title": "Analytics", "body": "SQL Analytics + BI", "color": "lava"},
    ],
    title="Implementation Journey"
)

# Style 2: Cards with arrows between them
s = deck.add_timeline(
    steps=[
        {"title": "Assess", "body": "Current state analysis", "color": "maroon"},
        {"title": "Design", "body": "Architecture blueprint", "color": "blue"},
        {"title": "Build", "body": "Lakehouse implementation", "color": "green"},
    ],
    title="Engagement Phases",
    style=2
)
```
- Style 1: Numbered circles (ELLIPSE) on a horizontal connector line, centered text below each step.
- Style 2: Cards with colored accent bars and arrows between them. Reuses `add_card` and `add_arrow`.
- Custom canvas (blank slide with bg, section label, title).
- Each step dict: `title` (required), `body` (optional), `color` (optional, defaults to "blue").

### add_architecture(layers, title=None, subtitle=None)

```python
s = deck.add_architecture(
    layers=[
        {"title": "Sources", "items": ["EHR/Epic", "Claims", "IoT"], "color": "maroon"},
        {"title": "Ingestion", "items": ["Auto Loader", "DLT", "Streaming"], "color": "blue"},
        {"title": "Lakehouse", "items": ["Bronze", "Silver", "Gold"], "color": "green"},
        {"title": "Consumption", "items": ["SQL Analytics", "ML/AI", "BI"], "color": "yellow"},
    ],
    title="Healthcare Data Architecture"
)
```
- Stacked horizontal bands, evenly divided across content zone.
- Each band: bgCard fill, colored accent bar on left, layer title (colored text), component boxes (bgLight fill) on right.
- Custom canvas (blank slide with bg, section label, title).
- Each layer dict: `title` (required), `items` (list of component names), `color` (optional).

### add_architecture_advanced(tiers, flows, title, scaling_boundaries, speaker_notes)

**Complex architecture diagrams with flows and corridors — drawn directly on Google Slides.**

Replaces D2/ELK for presentation-quality diagrams. Every component and flow is positioned
with exact coordinates. No layout engine. No crossing prayers.

```python
s = deck.add_architecture_advanced(
    tiers=[
        {
            "label": "Compute Layer",
            "sublabel": "(Scales to Zero)",
            "color": "lava",
            "zones": {
                "left": [
                    {"name": "R/W Compute", "subtitle": "Auto-scale\nScale-to-zero",
                     "shape": "rect", "accent": "lava"},
                ],
                "right": [
                    {"name": "Replica 1", "shape": "cylinder"},
                    {"name": "Replica 2", "shape": "cylinder"},
                    {"name": "Replica 3", "shape": "cylinder"},
                ],
            },
        },
        {
            "label": "WAL Consensus",
            "sublabel": "(Fixed Size)",
            "color": "yellow",
            "items": ["Safekeepers (Paxos 2/3, 3x AZ)"],
        },
        {
            "label": "Page Cache",
            "sublabel": "(Scales with Read Load)",
            "color": "green",
            "items": ["Pageservers (Multi-AZ Cache)"],
        },
        {
            "label": "Persistent Storage",
            "sublabel": "(99.999999999% Durability)",
            "color": "blue",
            "items": ["Object Storage"],
        },
    ],
    flows=[
        # WRITE PATH (left corridor, lava/red)
        {"from": (0, "left", 0), "to": (1, None, 0),
         "label": "writes", "color": "lava", "corridor": "left"},

        # READ PATH (right corridor, green)
        {"from": (0, "right", 1), "to": (2, None, 0),
         "label": "reads", "color": "green", "corridor": "right"},

        # STORAGE OPS (center, yellow)
        {"from": (1, None, 0), "to": (2, None, 0),
         "label": "WAL stream (3x)", "color": "yellow", "corridor": "center"},
        {"from": (1, None, 0), "to": (3, None, 0),
         "label": "archive (3x)", "color": "yellow", "style": "dashed", "corridor": "left"},
        {"from": (2, None, 0), "to": (3, None, 0),
         "label": "persist", "color": "yellow", "corridor": "center"},
    ],
    title="Lakebase Architecture",
    scaling_boundaries=True,
    speaker_notes="Key point: every tier scales independently...",
)
```

**When to use which:**

| Use Case | Method |
|---|---|
| Simple layered architecture (Sources → Lakehouse → Consumption) | `add_architecture()` |
| Complex architecture with multiple flow types and corridors | `add_architecture_advanced()` |
| Quick draft / iteration on topology (not for final slides) | D2 + ELK (import PNG) |

**Flow corridor assignments:**
- `"left"`: Arrow routes down the left gutter — use for write paths
- `"right"`: Arrow routes down the right gutter — use for read paths
- `"center"`: Arrow routes between source and destination centers — use for internal ops

**Zone layout:**
- `"left"` zone components render in the left ~38% of the tier band
- `"right"` zone components render in the right ~58% of the tier band
- Tiers without zones use simple `"items"` (evenly distributed, no corridors)

**Design thinking integration:**
This method implements the design thinking framework from d2-design-thinking.md:
- Phase 1 (Layout): Always vertical stack — tiers top-to-bottom
- Phase 2 (Visual Star): `scaling_boundaries=True` makes tier separators prominent
- Phase 3 (Corridors): `zones` + flow `corridor` enforce spatial separation
- Phase 4 (Component Filter): Only include what serves the argument

### add_logo_strip(logos, title=None, y=None, show_captions=False, bg_strip_opacity=None)

**Logo input modes (v3):**

| Mode | Input | When to use |
|---|---|---|
| Registry (preferred) | `{"id": "databricks"}` | Logo is in the variant registry |
| Registry + size override | `{"id": "databricks", "width": 2.0, "height": 0.7}` | Registry logo, custom sizing |
| Raw URL (fallback) | `{"url": "https://...", "width": 1.8, "height": 0.6}` | Logo NOT in registry |

**Registry example (recommended):**
```python
s = deck.add_logo_strip(logos=[
    {"id": "databricks"},
    {"id": "spark"},
    {"id": "hadoop"},
    {"id": "python"},
], title="Technology Ecosystem")
```

**Mixed example (registry + raw URL):**
```python
s = deck.add_logo_strip(logos=[
    {"id": "databricks"},
    {"id": "mlflow"},
    {"url": "https://example.com/custom-partner.png", "width": 1.5, "height": 0.8},
], title="Our Stack")
```

- **Logo variant registry:** Pass `{"id": "databricks"}` — scaffold auto-resolves correct variant (white logo on dark bg, dark logo on light bg) and default sizing.
- **Adaptive background strip:** Auto-computes strip fill using WCAG luminance-based contrast (1.5:1 target). No caller tuning needed.
- `bg_strip_opacity`: Optional override (0.0 = disable strip). Auto-compute is the default.
- `show_captions`: False by default. Set True only for abstract icons.
- **Registry contents:** databricks, spark, delta_lake, mlflow, unity_catalog, python, hadoop, docker, aws, azure, gcp, kubernetes, tableau, power_bi, snowflake, kafka, airflow, dbt, terraform, github. Each stores dark_bg URL, light_bg URL, default width, default height.
- Custom canvas (blank slide with bg, section label, title).
- **Important:** All URLs must be publicly accessible PNGs/JPEGs. SVG URLs fail silently.

### add_table(headers, rows, title=None, subtitle=None)

```python
s = deck.add_table(
    headers=["Capability", "Traditional", "Databricks", "Impact"],
    rows=[
        ["Query Speed", "Hours", "Seconds", "100x faster"],
        ["Data Freshness", "Days", "Real-time", "Streaming"],
        ["Cost", "$2M+/year", "$400K/year", "80% reduction"],
    ],
    title="Platform Comparison"
)
```
- Uses `gb.create_table`, `gb.fill_table`, `gb.style_table_header`, `gb.style_table_for_dark_background`.
- Header row: blue background (#2272B4), t1 (white) bold text — clearly distinct from body rows. Data rows: bg fill, t2 text.
- Table auto-sized to fit content zone. Row height 0.45".
- Custom canvas (blank slide with bg, section label, title).

## Custom-Drawn Elements

Add these to any slide (template-native or custom canvas):

### add_stat_hero(page_id, number, label, source=None, color="blue", icon=None)

```python
deck.add_stat_hero(s, "72%", "of health systems report delays", "KLAS 2024")

# With icon circle above stat
deck.add_stat_hero(s, "< 15s", "average query response time",
    source="Internal benchmark, 2024", color="green",
    icon="https://example.com/icon.png")
```
- **Auto-sized (v3):** Formula-driven font sizing based on stat string length:
  - `len(stat) <= 5` → 80pt (e.g., "< 15s", "72%", "$31K")
  - `len(stat) <= 8` → 64pt (e.g., "10-20x", "$400K/yr")
  - `len(stat) > 8` → 48pt (e.g., "1.2 million")
- Context text = `stat_font_size / 4`, floor 16pt. Source text = 9pt always.
- **Centered:** Full-width text boxes with CENTER paragraph alignment. No caller tuning needed.
- Vertically centered in content zone. Pass `x` and `y` to override position.
- Optional `icon`: URL to PNG image. Renders as colored circle (0.6") with image inside, centered above the stat number.

### add_card(page_id, x, y, w, h, accent="blue", title=None, body=None)

```python
deck.add_card(s, 0.833, 2.175, 3.5, 2.0, accent="lava", title="Card", body="Details")
```
- bgCard fill, thin accent bar on left, no outline.
- Dynamic body font: scales with card width (4" baseline = 14pt, clamped 12-18pt).

### add_callout_bar(page_id, text, color="blue")

```python
deck.add_callout_bar(s, "One Platform — governed by Unity Catalog")
```
- Full-width bar at y=6.0" with accent stripe and colored text.

### add_section_label(page_id, text, color="lava")

```python
deck.add_section_label(s, "THE PROBLEM", "lava")
```
- 10pt uppercase spaced label above the title zone.

### add_slide_title(page_id, text)

```python
deck.add_slide_title(s, "Key Challenge")
```
- 28pt bold white title at template title position.

### add_card_grid_on_slide(page_id, cards, cols=3)

```python
deck.add_card_grid_on_slide(s, cards, cols=2, accent="green")
```
- Draws cards on an existing slide (for custom layouts).

### add_chrome(page_id, slide_num, total, confidential=True)

```python
deck.add_chrome(s, 3, 8)
```
- Footer: "Databricks Confidential" left, "3 / 8" right.

### add_speaker_notes(page_id, notes_text)

```python
deck.add_speaker_notes(s, "TALK TRACK (45s):\n• Point 1\n• Key transition: ...")
```

### add_cover_accent(page_id, color="lava")

L-shaped geometric accent in top-right corner.

### add_arrow(page_id, x, y, w, color="t3")

Thin horizontal line (0.03" tall rectangle).

### add_icon_circle(page_id, icon_name, bg_color, x, y, size=0.5)

Colored circle with icon image centered inside.

## Architecture Diagrams (ArchDiagramBuilder)

For low-level architecture diagrams with absolute coordinate control, use `ArchDiagramBuilder`:

```python
from gslides_scaffold import ArchDiagramBuilder

ab = ArchDiagramBuilder(pres_id, page_id)
ab.add_rect("zone1", x, y, w, h, fill_rgb, border_rgb=None, border_weight=2)
ab.add_component("comp1", "ROUND_RECTANGLE", "Label", x, y, w, h, fill_rgb, border_rgb)
ab.add_connection("flow1", "comp1", "comp2", CONN_BOTTOM, CONN_TOP, color_rgb, weight=2.5)
ab.execute()  # Submits batched requests
```

### Architecture Diagram Narrative Header (Required)

Every architecture diagram script MUST begin with this block before
any coordinates. The eval rubric (Check 0) verifies it exists and
that the rendered diagram matches it.

```python
# ============================================================
# NARRATIVE INTENT — define before placing any shapes
# ============================================================
# ARGUMENT: [One sentence. What should the audience conclude?]
#
# STRUCTURE: [What spatial arrangement carries the argument?]
#
# INVENTORY:
#   Zones:
#     - [zone name]: [what it represents, why it's on the slide]
#   Components:
#     - [component name]: [what it represents, why it's on the slide]
#   Arrows:
#     - [color] [source] → [target]: [what this flow represents]
# ============================================================
```

### Connectors (BENT auto-routing)

```python
# Vertical connection: compute to storage layer
ab.add_connection("flow_write", "postgres_inst_2", "safekeeper_0",
    ArchDiagramBuilder.CONN_BOTTOM, ArchDiagramBuilder.CONN_TOP,
    C["blue"], weight=2.5)

# Horizontal connection: storage to compute
ab.add_connection("flow_read", "pageserver", "postgres_inst_0",
    ArchDiagramBuilder.CONN_LEFT, ArchDiagramBuilder.CONN_RIGHT,
    C["green"], weight=2.5)
```

**Connection points:**
- `CONN_TOP`, `CONN_BOTTOM`, `CONN_LEFT`, `CONN_RIGHT`

**BENT router behavior:**
- Creates orthogonal (90-degree) paths between components
- Auto-routes around obstacles when possible
- Prefers paths that match the connection point orientation

**Working with BENT routing:**
- Align source and target Y-coords for horizontal arrows
- Align source and target X-coords for vertical arrows
- Use connection points that match desired flow direction (BOTTOM→TOP flows down)
- If BENT produces ugly Z-bends, use `add_straight_arrow()` instead

### Straight Arrows (explicit path, no routing)

```python
# Diagonal arrow from compute to safekeeper
ab.add_straight_arrow("flow_write",
    x1=3.5, y1=3.0,    # right edge of source component
    x2=4.8, y2=4.6,    # left edge of target component
    color_rgb=C["blue"], weight=2.5)

# Horizontal arrow, right to left
ab.add_straight_arrow("flow_read",
    x1=4.85, y1=2.85,
    x2=2.3, y2=2.3,
    color_rgb=C["green"], weight=2.5)
```

**When to use `add_straight_arrow()` vs `add_connection()`:**

| Scenario | Use |
|---|---|
| Vertical or horizontal between aligned shapes | `add_connection()` — BENT routing works fine |
| Diagonal arrow | `add_straight_arrow()` — BENT can't do diagonals |
| Arrow crossing a zone boundary | `add_straight_arrow()` — BENT Z-bends at borders |
| Arrow where path matters for narrative | `add_straight_arrow()` — full control |
| Simple same-zone connection | `add_connection()` — less coordinate math |

**Computing coordinates from component constants:**
```python
# Arrow from right-center of a component to left-center of another
x1 = COMP_A_X + COMP_A_W          # right edge
y1 = COMP_A_Y + COMP_A_H / 2      # vertical center
x2 = COMP_B_X                     # left edge
y2 = COMP_B_Y + COMP_B_H / 2      # vertical center
ab.add_straight_arrow("flow_id", x1, y1, x2, y2, C["blue"])
```

## Shape Operations (via gslides_builder)

```python
import gslides_builder as gb

# Create shape
gb.create_shape(pres_id, page_id, "RECTANGLE", x, y, w, h, shape_id=gb.generate_id())

# Fill + suppress outline
deck._set_fill(shape_id, C["bgCard"])

# Update shape fill only
gb.update_shape_properties(pres_id, shape_id, fill_color=C["blue"])

# Text style on existing shape
gb.update_text_style(pres_id, shape_id, 0, 5, bold=True, font_size=14, foreground_color=C["t1"])

# Replace all text in a placeholder
gb.replace_shape_text(pres_id, shape_id, "New text")
```

Shape types: `RECTANGLE`, `ELLIPSE`, `TEXT_BOX`, `LINE`.

## Images

```python
gb.create_image(pres_id, page_id, image_url, x, y, w, h, image_id=gb.generate_id())
```

Image URLs must be publicly accessible. Drive files: `https://drive.google.com/uc?id=FILE_ID`.

## Tables

```python
table_id = gb.create_table(pres_id, page_id, rows, cols, x, y, w, h)
gb.fill_table(pres_id, table_id, [["Col1", "Col2"], ["A", "B"]])
gb.style_table_header(pres_id, table_id, cols, bg_color=C["bgCard"], text_color=C["t1"])
gb.style_table_for_dark_background(pres_id, table_id, rows, cols)
```

## Thumbnails

```python
deck.get_thumbnail_png(page_id, "rendered/slide-03.png")
```

Uses Slides API `GET .../pages/{pageId}/thumbnail?thumbnailSize=LARGE`.

## Palette

Dark theme (`C` dict — RGB 0-1 floats):

| Key | Hex | Use |
|-----|-----|-----|
| `bg` | #0B2026 | Slide background (Navy 900) |
| `bgCard` | #1B3139 | Card/panel fill |
| `bgLight` | #303F47 | Subtle elevation |
| `lava` | #FF3621 | Primary accent, section labels |
| `green` | #00A972 | Success, positive |
| `blue` | #2272B4 | Stats, links, neutral accent |
| `yellow` | #FFAB00 | Warning, attention |
| `maroon` | #98102A | Objections, negative |
| `t1` | #FFFFFF | Primary text |
| `t2` | #DCE0E2 | Secondary text |
| `t3` | #5A6F77 | Captions, footnotes |

Light backgrounds (`CL` dict): `greenLight`, `blueLight`, `yellowLight`, `lavaLight`, `maroonLight` — muted dark tones for callout bar fills.

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| EMU math wrong | Always use `gb.inches_to_emu(x)` |
| Tilde in sys.path | `os.path.expanduser("~/.claude/...")` — raw tilde doesn't expand |
| outline_weight=0 rejected | Use `propertyState: NOT_RENDERED` via `_set_fill()` |
| Placeholder index None for 0 | API omits index field when 0; `_fill_placeholder` normalizes this |
| Content layouts are bright | Shared layouts use LIGHT1 bg. `_apply_dark_content_overrides()` handles this |
| Card text on light cards | Card placeholders sit on white card shapes — DON'T force light text colors |
| Quote text invisible | Power Statement 2 TITLE inherits dark text on DARK1 bg. `add_quote()` forces white |
| Template master GC | Don't delete ALL sample slides before first `add_slide()` call |
| Layout names vs IDs | Names are stable across copies; IDs change. Use `_LAYOUT_DISPLAY_NAMES` |
| Quota | 60 req/min. Batch requests per slide. |
| batchUpdate ordering | Create shape before styling: create → fill → outline → text |
| Sample slide cleanup | Template has 98 sample slides. Batch-delete via `batchUpdate`, never loop `delete_slide()` |
| `create_text_box` no alignment | Use `updateParagraphStyle` with `alignment: "CENTER"` after creation |
| Raw Databricks logo URL on dark slide | Dark red logo vanishes against dark background. Use `{"id": "databricks"}` — scaffold picks white variant |
| Manual `bg_strip_opacity` for every logo strip | Fragile, different result per theme. Let scaffold auto-compute. Only override for edge cases |
| `illustration` on `content_basic` layout | Image overlaps body text — no reserved image zone. Use `content_card_right`, `_left`, or `_large` |
| `col1`/`col2`/`col3` keys on non-3col layout | Keys ignored, body filled instead. Match content dict keys to layout family |

## Complete Script Structure

```python
from gslides_scaffold import DeckBuilder

deck = DeckBuilder("Healthcare Analytics", theme="dark")

# Slide 1: Title
s1 = deck.add_title_slide("Databricks for Healthcare", "From data to insight")

# Slide 2: Section break
s2 = deck.add_section_break("The Problem")

# Slide 3: Stat hero on content slide (with optional icon)
s3 = deck.add_content_slide("content_a_basic", {"title": "The Analytics Gap"})
deck.add_stat_hero(s3, "72%", "of health systems report delays", "KLAS 2024",
    icon="https://example.com/icon.png")  # icon is optional

# Slide 4: Timeline
s4 = deck.add_timeline(
    steps=[
        {"title": "Discovery", "body": "Identify sources", "color": "blue"},
        {"title": "Ingestion", "body": "Bronze layer", "color": "green"},
        {"title": "Analytics", "body": "BI dashboards", "color": "yellow"},
    ],
    title="Implementation Journey"
)

# Slide 5: Architecture
s5 = deck.add_architecture(
    layers=[
        {"title": "Sources", "items": ["EHR", "Claims", "IoT"], "color": "maroon"},
        {"title": "Lakehouse", "items": ["Bronze", "Silver", "Gold"], "color": "green"},
        {"title": "Consumption", "items": ["SQL", "ML/AI", "BI"], "color": "yellow"},
    ],
    title="Data Architecture"
)

# Slide 6: Comparison
s6 = deck.add_comparison(
    before={"title": "Before", "points": ["Siloed data", "Days to query"]},
    after={"title": "After", "points": ["Unified lakehouse", "Seconds to insight"]},
    title="The Transformation"
)

# Slide 7: Table
s7 = deck.add_table(
    headers=["Capability", "Traditional", "Databricks"],
    rows=[["Speed", "Hours", "Seconds"], ["Cost", "$2M+", "$400K"]],
    title="Platform Comparison"
)

# Slide 8: Card grid (with optional per-card icons)
s8 = deck.add_card_grid(title="Results", cards=[
    {"title": "Providence", "body": "1,000 clinics unified"},
    {"title": "Geisinger", "body": "40% faster analytics"},
    {"title": "Mayo Clinic", "body": "Population genomics at scale"},
])
deck.add_callout_bar(s8, "One Platform — Unity Catalog")

# Slide 9: Content with illustration (text left, image right)
s9 = deck.add_content_slide("content_card_right", {
    "title": "The Lakehouse Architecture",
    "subtitle": "Combining data lakes and data warehouses",
    "body": "Eliminates the need to maintain separate systems for analytics and AI."
}, illustration={
    "url": "https://example.com/lakehouse-diagram.png",
    "width": 5.0,
    "height": 3.5
})

# Slide 10: Three pillars (parallel items)
s10 = deck.add_content_slide("content_3col", {
    "title": "Three Pillars of the Lakehouse",
    "col1": "Open standards. No vendor lock-in. Apache Spark, Delta Lake, MLflow.",
    "col2": "One platform for all workloads. No ETL between warehouses and lakes.",
    "col3": "Shared workspace with Unity Catalog governance."
})

# Slide 11: Before/after with accent colors
s11 = deck.add_comparison(
    before={"title": "Traditional Approach", "points": ["Siloed warehouses and lakes", "Manual governance", "Months to deploy ML"]},
    after={"title": "Lakehouse Approach", "points": ["Unified platform", "Automated governance with Unity Catalog", "Days to production"]},
    left_accent="maroon",
    right_accent="green"
)

# Slide 12: Logo strip (variant registry — scaffold picks correct logo for background)
s12 = deck.add_logo_strip(logos=[
    {"id": "databricks"},
    {"id": "spark"},
    {"id": "hadoop"},
    {"id": "python"},
], title="Technology Ecosystem")

# Slide 13: Quote
s13 = deck.add_quote("The lakehouse changed everything.", "CDO, Regional Health System")

# Slide 14: Closing
s14 = deck.add_closing("Thank You", "email@databricks.com")

url = deck.save()
print(f"Deck: {url}")

# Screenshot each slide
slides = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]
for i, page_id in enumerate(slides, 1):
    deck.get_thumbnail_png(page_id, f"rendered/slide-{i:02d}.png")
```

**Post-render evaluation (MANDATORY):**

After rendering any slide with `add_architecture_advanced()`, you MUST run the full
Architecture Eval Rubric from `references/architecture-eval-rubric.md` before presenting
to the user or moving to the next slide. This is not optional.

The rubric has 8 checks: containment, label accuracy, overlap detection, flow correctness,
corridor separation, visual hierarchy, readability, and legend. Write out each check result
explicitly. Do not skip checks. Do not score the diagram without running all 8.

Minimum passing score: 7/8 checks PASS. If below 7/8: fix and re-render.
