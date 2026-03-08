# Design Rules

## Before Starting

1. **Topic-specific palette** — If swapping your colors into a different deck would still "work," your choices aren't specific enough.
2. **Color dominance** — One color at 60-70% visual weight, 1-2 supporting tones, one sharp accent. Never equal weight.
3. **Dark or light, commit** — Dark throughout = premium feel (recommended for technical decks). Or dark sandwich (title + conclusion dark, content light).
4. **One visual motif, everywhere** — Pick ONE and repeat across every slide: left-edge accent bars, icons in colored circles, spaced uppercase section labels, consistent card shadows.
5. **Template-first** — Always use a Databricks template layout when one fits. Only build from scratch when no template layout matches the content pattern.

## Visual Polish Standards (NON-NEGOTIABLE)

**These standards define "professional" vs "copy-pasted garbage." Violating these ruins the deck.**

### 0. The Aesthetic Test (Above All Else)

Before the technical rules, ask yourself:

**"Does this slide look *pleasing* to the eye, or does it tire someone out?"**

Technical correctness (spacing, cards, colors) is necessary but not sufficient. A slide can pass all rules and still feel:
- Heavy (too much visual weight)
- Exhausting (too many elements competing for attention)
- Cluttered (no breathing room)
- Forced (trying too hard to be "designed")

**Aesthetic quality means:**
- **Effortless comprehension** — You "get it" in <3 seconds without working hard
- **Generous whitespace** — Empty space is not wasted space; it gives the eye rest
- **Visual lightness** — Slides feel airy, not dense
- **Pleasant to look at** — You *want* to read it, not dread it
- **Professional restraint** — Don't use every design element available

**Red flags that a slide is "technically correct but aesthetically bad":**
- You filled every available inch with content
- Every card has the same visual weight (no hierarchy)
- Text size is "readable" but feels cramped
- There are 6 visual elements (cards/boxes/lines/icons) on one slide
- You maximized information density instead of optimizing for comprehension

**The fix:**
- Cut content to 3-5 items instead of 6-8
- Increase card padding and spacing by 50%
- Make titles bigger, body text slightly smaller
- Use whitespace to guide the eye, not fill it
- Less is more — one clear slide beats one packed slide

### 1. NO TEXT WALLS — Use Visual Containers

❌ **BAD:** Floating bullets with no structure
```
• Item 1
• Item 2
• Item 3
```

✅ **GOOD:** Cards, boxes, or visual groupings
```
┌─────────────────┐
│ CATEGORY HEADER │
│ • Item 1        │
│ • Item 2        │
└─────────────────┘
```

**Rule:** If a slide has >5 bullets, use cards/boxes to group them. Never dump text directly onto a dark background.

### 2. SPACING IS NOT OPTIONAL

**Required spacing:**
- Between cards: Minimum 0.3" horizontal, 0.4" vertical
- Card padding: Minimum 0.2" on all sides
- Between bullet groups: Minimum 0.15" vertical
- Title to content: Minimum 0.5" vertical

**If it looks cramped, it IS cramped.** Add more space.

### 3. COLOR-CODE BY MEANING

When showing multiple categories (e.g., "Hard Blockers" vs "Warnings"):
- **Use colored borders or backgrounds** to distinguish severity/priority
- Red = critical/blocker
- Yellow = warning/caution
- Blue = info/tip
- Gray = deprecated/legacy

**Never** use the same visual treatment for items with different priorities.

### 4. HEADERS MUST BE VISIBLE

If your content has categories, the category headers MUST appear on the slide.

❌ **BAD:** "DISQUALIFY IMMEDIATELY" is in your code but invisible on slide
✅ **GOOD:** "DISQUALIFY IMMEDIATELY" is a visible header above the content

### 5. COMPARISON SLIDES NEED SYMMETRY

When showing "Vanilla PostgreSQL vs Lakebase" or any A vs B comparison:
- **Column headers required** — "Vanilla PostgreSQL" and "Lakebase" must be visible
- **Centered divider** — Vertical line at true center (x=5.1 on 10" wide slide)
- **Equal column widths** — Both sides get same space
- **Aligned content starts** — Left bullets and right bullets start at same Y coordinate

### 6. CARD-BASED LAYOUTS FOR LISTS

When presenting 3-6 distinct items (gotchas, action steps, feature lists):
- **Use card grid layout** (2×2 or 3-column)
- Each card: Colored header + body text + border + shadow
- **Never** use a 2-column text layout for this — it looks like a Word doc

**Example use cases for card layouts:**
- Field gotchas (hard blockers, warnings, tips)
- Action plans (step 1, step 2, step 3)
- Feature comparisons (feature A, B, C with pros/cons)
- Key takeaways (3-5 main points)

### 7. REFERENCE EXISTING LAYOUTS FIRST

Before creating ANY slide, check if a layout already exists:
- `addCardGrid3Col` — 3-column card grid
- `addWarningCards` — 2×2 card grid with severity colors
- `addSideBySideComparison` — Two-column comparison with headers
- `addContent2Col` — Two-column text (use ONLY for narrative content, not lists)

**If none fit, create a NEW layout function.** Do not hack together layouts inline.

## Palettes (Extended for Dark Themes)

Dark themes need: background, card background, primary brand, secondary brand, accent, plus 4 text levels (bright → muted).

### Official Databricks Brand Colors (USE THIS)

Source: https://brandguides.brandfolder.com/databricks-extended-brand-guidelines/colors

**Primary palette:**

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **bg** | Navy 900 | 0B2026 | Slide background |
| **bgCard** | Navy 800 | 1B3139 | Card backgrounds |
| **bgLight** | Gray - Navigation | 303F47 | Lighter card variant, interactive elements |
| **primary** | Lava 600 | FF3621 | Databricks red (use sparingly) |
| **green** | Green 600 | 00A972 | Success, complete, positive |
| **blue** | Blue 600 | 2272B4 | Info, neutral emphasis |
| **yellow** | Yellow 600 | FFAB00 | Warning, highlight, next |
| **maroon** | Maroon 600 | 98102A | Deep emphasis |

**Secondary palette:**

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **Lava 500** | Lava light | FF5F46 | Lighter red variant |
| **Oat Medium** | Oat | EEEDE9 | Light backgrounds (light theme only) |
| **Oat Light** | Oat light | F9F7F4 | Lightest background (light theme only) |
| **Gray - Lines** | Lines | DCE0E2 | Borders, dividers, body text on dark bg |
| **Gray - Text** | Text | 5A6F77 | Muted text, captions, footnotes on dark bg |
| **Gray - Navigation** | Nav | 303F47 | Navigation elements, card fills on dark bg |

**Text hierarchy (dark theme):**

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **t1** | White | FFFFFF | Titles, hero text |
| **t2** | Gray - Lines | DCE0E2 | Body text, bullet points |
| **t3** | Gray - Text | 5A6F77 | Secondary labels, section headers |
| **t4** | Gray - Text | 5A6F77 | Captions, footnotes (same as t3 — palette has 3 usable dark-theme text levels) |

**Note:** The brand palette supports 3 text contrast levels on Navy 900 backgrounds, not 4. Gray-Navigation (#303F47) is too low-contrast for readable text on Navy 900 — use it only for backgrounds and borders, never for text.

**Projector contrast warning:** Conference room projectors wash out low-contrast pairings. Critical data (hero stats, key labels, CTA text) must use `t1` (FFFFFF) or `t2` (DCE0E2) on dark backgrounds — never `t3` for anything the audience needs to read from 10+ feet away. Reserve `t3` for secondary labels and footnotes that are only relevant in leave-behind mode. When in doubt, bump up one contrast level.

**Light variants for callout backgrounds** (darken to ~15% visible):
- greenLight: 0D2920
- blueLight: 0D1F2D
- yellowLight: 2D2510
- lavaLight: 2D1510

```python
# Official Databricks brand palette (gslides_scaffold.C)
# C["bg"], C["bgCard"], C["lava"], C["green"], C["blue"], C["yellow"], C["maroon"]
# C["t1"], C["t2"], C["t3"]  # Text hierarchy
# CL["greenLight"], CL["blueLight"], etc.  # Light callout backgrounds
```

### Color Usage Guidelines

| Slide Element | Recommended Color |
|---------------|-------------------|
| Complete/Success badges | green |
| In-progress/Next badges | yellow |
| CTA/Action items | lava (sparingly) |
| Info cards | blue |
| Quotes/Objections | maroon |
| Callout bars | Varies by intent |
| Section labels | Rotate: green → blue → yellow |

**Rule:** Lava red is the Databricks signature. Use it for ONE accent per slide max (title accent, CTA button, or key stat). Overuse dilutes brand impact.

### Alternative Themes

| Theme | bg | bgCard | primary | secondary | accent | t1 | t2 | t3 | t4 |
|-------|-----|--------|---------|-----------|--------|------|------|------|------|
| **Midnight** | 1A1A2E | 16213E | 0F3460 | 533483 | E94560 | FFFFFF | C8D6E5 | 8395A7 | 576574 |
| **Ocean** | 0A1628 | 142238 | 065A82 | 1C7293 | F5A623 | FFFFFF | B8D4E3 | 7A9BB5 | 4A6B80 |
| **Teal Trust** | 0B1E25 | 132E38 | 028090 | 00A896 | 02C39A | FFFFFF | C8E6E0 | 7AADA3 | 4A8078 |
| **Forest** | 1B2A1B | 2C3E2C | 2C5F2D | 97BC62 | F5A623 | FFFFFF | D4E2D4 | 8FA88F | 5C755C |

---

## Layout Selection Guide

Use this table to map content intent to a template layout. **Always prefer a template layout over building from scratch.**

### Title & Opening Slides

| Intent | Template Layout | Key | Theme Options |
|--------|----------------|-----|---------------|
| Opening title (with hero image area) | 1 Title Slide A - Light / 2 Title Slide A - Dark | `title_slide_a_light` / `title_slide_a_dark` | Light or dark; right-side image placeholder |
| Opening title (text-only, clean) | 3 Title Slide B - Light / 4 Title Slide B - Dark | `title_slide_b_light` / `title_slide_b_dark` | Light or dark; no right image |
| Closing / thank you | Z - Closing Light / Z - Closing Dark | `z_closing_light` / `z_closing_dark` | Centered Databricks logo |

### Section Dividers

| Intent | Template Layout | Key | Notes |
|--------|----------------|-----|-------|
| Artistic section break (geometric shapes, light) | Content F - Artistic Divider 1/2/3 | `content_f_artistic_divider_1` / `_2` / `_3` | Rotate styles for visual variety |
| Artistic section break (dark) | Content F - Artistic Divider Dark 1/2/3 | `content_f_artistic_divider_dark_1` / `_2` / `_3` | Dark bg; use for REFRAME / DROWN transitions |
| Power statement / big quote | Content E - Power Statement 1 (light) / 2 (dark DARK1) / 3 (ACCENT4) / 4 (ACCENT1 red) | `content_e_power_statement_1` through `_4` | Full-slide TITLE placeholder; use for FEEL slides, key insights, reframe moments |

### Content Slides

| Intent | Template Layout | Key | Notes |
|--------|----------------|-----|-------|
| General content (title + subtitle + body) | 7 Content A - Basic | `content_a_basic` | Oat bg (LIGHT1); workhorse layout |
| General content (white bg) | 8 Content A - Basic White 1 | `content_a_basic_white_1` | Same structure, white bg |
| Two-column comparison | 9 Content B - 2 Column | `content_b_2_column` | Vertical divider line; column subtitles + body areas |
| Two-column with icon spots | 10 Content B - 2 Column w/ Icon Spot | `content_b_2_column_with_icon_spot` | Same + upper zone for icons/images per column |
| Three-column (text) | 11 Content C - 3 Column | `content_c_3_column` | 3 equal columns with subtitles; divider lines |
| Three-column with icon spots | 12 Content C - 3 Column w/ Icon Spot | `content_c_3_column_with_icon_spot` | Same + upper icon zone per column |
| Three-column cards | 13 Content C - 3 Column Cards | `content_c_3_column_cards` | White card rectangles on oat bg; built-in card shadows |
| Card + text (right card) | 14 Content D - Card Right | `content_d_card_right` | Left text + right white card; good for text + visual/diagram |
| Card + text (left card) | 15 Content D - Card Left | `content_d_card_left` | Left white card + right text |
| Full-width card | 16 Content D - Card Large | `content_d_card_large` | Single large white card on oat bg |
| Four-card quad | 17 Content D - Card Quad | `content_d_card_quad` | 2×2 grid of white cards; ideal for 4-item comparisons |
| Blank canvas (Databricks theme) | Content E - Blank | `content_e_blank` | Full LIGHT1 bg, no placeholders; build from scratch |
| Big number / stat hero | big_number (Simple Light) | `big_number` | Large TITLE + BODY; use for hero stat slides |

### Mapping Content Patterns to Template Layouts

| Content Pattern | Best Template Layout | Scaffold Helpers Needed |
|-----------------|---------------------|------------------------|
| **Stat hero** (one big number + context) | `big_number` or `content_e_power_statement_1` | `add_stat_hero()` for formatting the number; or just set title to "48%" in the TITLE placeholder |
| **Card grid (2×2)** | `content_d_card_quad` | None — use the 4 SUBTITLE placeholders |
| **Card grid (3-col)** | `content_c_3_column_cards` | None — template provides white cards with shadows |
| **Two-column comparison** | `content_b_2_column` or `content_b_2_column_with_icon_spot` | `add_icon_circle()` in the icon spot zone if using icon variant |
| **Before/After panels** | `content_b_2_column` | Color the left column subtitle with maroon, right with green; add accent shapes via scaffold |
| **Architecture flow** | `content_e_blank` or `content_a_basic` (title only) | Build from scratch: `add_card()`, `add_arrow()` per box. No template layout provides pre-built flow diagrams |
| **Quote card** | `content_e_power_statement_2` (dark) or `content_e_power_statement_3` (accent) | Set TITLE to the quote text; use large italic formatting |
| **Timeline** | `content_a_basic` | Build from scratch on the BODY area. Reference timeline samples on slides 41-43 for visual treatment |
| **Horizontal stacked rows** | `content_a_basic` or `content_d_card_large` | Build rows using `add_card()` inside the card area |
| **Numbered takeaway cards** | `content_c_3_column_cards` | Use card columns; add numbered circles via `add_icon_circle()` |
| **Objection handling** | `content_b_2_column` | Left col = objection (maroon accent), right col = reality (green accent), with `add_arrow()` between |
| **Section transition** | Rotate: `content_f_artistic_divider_1` → `_dark_2` → `_3` → `_dark_1` | None — just set TITLE text |

---

## Slide Layouts (Vary — Never Repeat Same Layout Consecutively)

### Card Grid (2×3 or 2×2)
Best for: feature lists, capabilities, comparison points
- **Use template:** `content_c_3_column_cards` (3-col) or `content_d_card_quad` (2×2)
- Template provides white card rectangles with correct drop shadows on oat background
- Add icons via `add_icon_circle()` positioned above each card's subtitle placeholder

```
[accent bar][icon] Title    [accent bar][icon] Title    [accent bar][icon] Title
            Description                 Description                 Description
```

### Two-Column Comparison
Best for: before/after, Delta vs Lakebase, pros/cons
- **Use template:** `content_b_2_column` (text) or `content_b_2_column_with_icon_spot` (with icons)
- Template provides vertical divider line between columns, column subtitles, and body areas
- Color-code column subtitles: maroon for "without," green for "with"

```
┌─ blue bar ──────────┐  ┌─ teal bar ──────────┐
│ [icon] OPTION A      │  │ [icon] OPTION B      │
│ · point 1            │  │ · point 1            │
│ · point 2            │  │ · point 2            │
│ "sample question"    │  │ "sample question"    │
│ tagline              │  │ tagline              │
└──────────────────────┘  └──────────────────────┘
```

### Horizontal Stacked Rows
Best for: requirements, specs, feature details
- **Use template:** `content_a_basic` for title/subtitle, then build rows in the BODY area using `add_card()`
- Alternatively use `content_d_card_large` for a single large card containing stacked rows

```
[accent][icon] Title ──── Bold Spec ──── Muted description
[accent][icon] Title ──── Bold Spec ──── Muted description
```

### Architecture Flow (left → right)
Best for: data flow, architecture, pipelines
- **Build from scratch** on `content_e_blank` or `content_a_basic` (title only, build in body zone)
- No template layout provides pre-built flow boxes — this pattern must be constructed with scaffold helpers

**Mandatory requirements for architecture slides:**
- **Arrows between EVERY box** — use `deck.add_arrow()` for horizontal connectors. No arrows = no flow. The audience must never have to infer reading order.
- **Hero step callout** — the most important/differentiating step (e.g., "~15s sync", "zero-copy") should be visually larger, use a standout color, and have its key metric in 16-22pt bold. If nothing stands out, the architecture is a wall of equal boxes.
- **4-5 boxes per flow path max** — consolidate related steps into one box with subtitle text. "Bronze → Jobs → Gold" = one "Delta Lakehouse" box.
- **Path labels** — if multiple paths exist (READ/WRITE, ingest/serve), use small bold headers above each path with distinct accent colors.
- **Connecting bar** — a full-width callout bar (e.g., "One Platform — governed by Unity Catalog") between paths ties the architecture together conceptually.
- **Zero-crossing-lines rule** — if connector lines cross each other, the diagram reads as spaghetti. Rearrange boxes to eliminate crossings. One crossing maximum in complex diagrams; zero is the target.
- **NFR governance wrapper** — technical gatekeepers look for security, scale, and governance. Wrap the architecture with a subtle "Governed by Unity Catalog" or "HIPAA-compliant environment" bar along the bottom or top. This pre-empts the gatekeeper's primary objection before they ask it. Use `bgLight` fill with `t3` text — visible but not dominant.

```python
# Arrow between boxes
deck.add_arrow(page_id, x=4.6, y=2.9, w=0.5, color="t3")

# Hero step — visually larger, standout color
deck.add_card(page_id, x=5.85, y=rY - 0.1, w=1.3, h=bH + 0.2, accent="blue")
deck.add_slide_title(page_id, "~15 sec", x=5.95, y=rY, w=1.1, h=0.3)  # 28pt default
```

### Quote Card
Best for: objections, customer quotes, key statements
- **Use template:** `content_e_power_statement_2` (dark bg) or `content_e_power_statement_3` (accent bg) for full-slide quotes
- For smaller quote cards embedded in a content slide, use `add_card()` on `content_a_basic`

```
❝ (icon)
┌─ gold bar ──────────────────────┐
│ "The quote text goes here..."   │
└─────────────────────────────────┘
```

### Before/After Panels (Competitive Framing)
Best for: proof points, transformation stories, "Why [Product]" slides, differentiator arguments
- **Use template:** `content_b_2_column` — built-in vertical divider, dual body areas, column subtitles
- Color the left subtitle/body with maroon (pain), right with green (solution)

```
┌─ muted header ──────┐      ┌─ green header ────────┐
│ Pain / traditional   │  ──▶ │ ✓ With product        │
│ (t3 muted text)      │      │ (t2 bright text)      │
│                      │      │ [icon] highlight       │
└──────────────────────┘      └───────────────────────┘
```

**This is the preferred layout for any "Why [Product]" or "Key Differentiators" slide.** A vertical list of product features is not differentiation — it's a brochure. The Before/After layout forces competitive positioning by requiring you to articulate what the alternative looks like.

**Visual treatment:**
- **Left column ("Without"):** Use left column subtitle + body placeholders. Apply maroon accent color to subtitle text. Use `t3` text color for body. This should feel old/painful.
- **Right column ("With"):** Use right column subtitle + body placeholders. Apply green accent color to subtitle text. Use `t2` text color for body, add icons via `add_icon_circle()`. This should feel modern/confident.
- **Arrow between headers** (optional): a single arrow element between the column subtitles reinforces the transformation narrative.
- **Each row is a contrast pair:** don't just list features on the right — state the specific pain on the left that each feature resolves.

### Objection Handling / "The Elephant in the Room"
Best for: Dismantling competitor claims, addressing NFRs (security, scale), resolving known internal resistance
- **Use template:** `content_b_2_column` — same structure as Before/After but different color treatment
- Left column subtitle uses maroon accent, right uses green

```
┌─ maroon top bar ────────┐      ┌─ green top bar ─────────┐
│ "The Objection"         │  ──▶ │ The Reality             │
│ (italic, muted t3 text) │      │ (bold t1 header)        │
│                         │      │ · Specific proof point  │
│                         │      │ · Specific mechanism    │
└─────────────────────────┘      └─────────────────────────┘
```

**When to use this vs Before/After:** Before/After shows transformation (old way → new way). Objection Handling puts the audience's exact doubt on screen in quotes, validates it, then dismantles it with evidence. Use when you *know* the room is thinking something specific — a competitor claim, a past failure, a cost concern.

**Visual treatment:**
- **Left column ("The Objection"):** maroon accent on subtitle, italic `t3` text in body framed as a quote. This should feel like "what people say" — not your words.
- **Right column ("The Reality"):** green accent on subtitle, bold `t1` text in body with evidence bullets. This should feel authoritative, not defensive.
- **The pivot:** Never just say "no, we do that." Provide a specific mechanism or proof point on the right side. Name a feature, cite a customer, show a number.

### Numbered Takeaway Cards
Best for: summary, key messages
- **Use template:** `content_c_3_column_cards` for 3 takeaways, `content_d_card_quad` for 4
- Add numbered circles using `add_icon_circle()` positioned at the top of each card

```
┌─ accent bar ─────────────────────────────────────────┐
│ [numbered circle] Title in brand color               │
│                   Description in muted text           │
└──────────────────────────────────────────────────────┘
```

---

## Icons & Illustrations Library

The template contains 34 slides of brand icons (slides 52-85) and 11 illustration slides (slides 87-97). **Use these to add visual richness to content slides — a text-only slide fails the magazine test when the design calls for visual support.**

### Icon Categories and When to Use Them

| Category | Template Slides | Use For |
|----------|----------------|---------|
| **High Level Icons** | Slide 53 | Simple, Open, Collaborative, Training, Support, Professional Services — general purpose |
| **Industry Icons** | Slide 54 | 14 industry tiles (illustrated squares) — use for vertical-specific pitches |
| **Platform** | Slides 56-57 | Analytics, Business Insights, Collaborative Data Science, Data Pipelines — platform capability slides |
| **Feature** | Slide 58 | Accelerator-Aware Scheduler, Built-in Functions, JDK 11, Join Hints — technical deep-dive slides |
| **Monitoring** | Slide 59 | Monitoring-related icons |
| **Connectors** | Slide 60 | Integration and connector icons |
| **Performance** | Slide 61 | Performance-related icons |
| **Financial Services** | Slide 67 | Credit Analysis, Customer Analysis, Financial Modeling — FSI pitches |
| **Healthcare and Life Sciences** | Slide 68 | Clinical Data, Genomics, Healthcare, Medical Imaging, Medical IoT, Social Medicine — HLS pitches |
| **Media and Entertainment** | Slide 69 | M&E vertical icons |
| **Retail / CPG** | Slide 70 | Retail vertical icons |
| **Public Sector** | Slide 71 | Government/public sector icons |
| **Security** | Slides 73-79 | 7 pages of security icons — governance, compliance, NFR slides |
| **Miscellaneous** | Slides 80-85 | General-purpose icons, arrows |

### Illustration Categories and When to Use Them

| Category | Template Slide | Use For |
|----------|---------------|---------|
| **Careers** | Slide 88 | Internal enablement, team slides |
| **Company** | Slide 89 | Company overview, "about us" |
| **Customers** | Slide 90 | Customer-facing, trust-building slides |
| **Delta Live Tables** | Slide 91 | DLT-specific content |
| **Lakehouse** | Slide 92 | General lakehouse architecture, platform overview |
| **Learn** | Slide 93 | Training, education, onboarding |
| **Partners** | Slide 94 | Partner slides, SI/GSI content |
| **Solutions** | Slide 95 | Solution architecture, use case slides |
| **SQL Analytics** | Slide 96 | SQL, BI, analytics content |
| **Unity Catalog** | Slide 97 | Governance, catalog, data management |
| **Data Engineering** | Slide 98 | ETL, pipeline, engineering slides |

### Industry-Specific Icon Recommendations

| Pitch Context | Icon Source | Illustration Source |
|---------------|-----------|-------------------|
| **Healthcare / HLS** | Slide 68 (Clinical Data, Genomics, Healthcare, Medical Imaging, Medical IoT, Social Medicine) | Slide 92 (Lakehouse) or Slide 95 (Solutions) |
| **Financial Services** | Slide 67 (Credit Analysis, Customer Analysis, Financial Modeling) | Slide 90 (Customers) or Slide 95 (Solutions) |
| **Retail / CPG** | Slide 70 (Retail/CPG icons) | Slide 90 (Customers) or Slide 95 (Solutions) |
| **Public Sector** | Slide 71 (Public Sector icons) | Slide 95 (Solutions) |
| **General platform** | Slides 56-57 (Platform) + Slide 53 (High Level) | Slide 92 (Lakehouse) |
| **Security / Governance** | Slides 73-79 (Security, 7 pages) | Slide 97 (Unity Catalog) |
| **Data Engineering** | Slide 58 (Feature) + Slides 56-57 (Platform) | Slide 98 (Data Engineering) or Slide 91 (DLT) |

### How to Use Template Icons

Icons are embedded as image elements on template slides. To use them in your deck:
1. **Copy from the template slide** — use `copy_element_from_slide()` to copy specific icon images from the source slide to your target slide
2. **Position and resize** — icons should be 0.4-0.6 inches when used as category markers in cards, 0.8-1.2 inches when used as hero visual elements
3. **Don't overuse** — 1-3 icons per content slide maximum. More than that becomes an "icon wall" (see deck-philosophy.md Section 5)

---

## Element Patterns (Code Snippets)

### Section label (spaced uppercase above every title)
```python
deck.add_section_label(page_id, "SECTION NAME", color="lava", x=0.8, y=0.35)
```

### Card with left accent bar
```python
deck.add_card(page_id, x=0.5, y=1.4, w=2.85, h=1.3, accent="blue",
              title="Card Title", body="Description text")
```

### Icon in colored circle
```python
deck.add_icon_circle(page_id, "check", "blue", x=0.85, y=1.75, size=0.5)
```

### Callout bar (bottom of slide)
```python
deck.add_callout_bar(page_id, "Key message", color="blue", y=4.7)
```

### Cover slide geometric accent
```python
# L-shaped lines in top-right
deck.add_cover_accent(page_id, color="lava")
# Or manually: two thin rectangles at (7.5,0) 2.5×0.06 and (9.94,0) 0.06×2.5
```

## Typography

| Element | Size | Style |
|---------|------|-------|
| Slide title | 28-40pt | Bold, header font |
| Section label | 9-10pt | Bold, UPPERCASE, charSpacing:3 |
| Card/row title | 14pt | Bold, header font |
| Body/description | 14pt | Normal, body font |
| Caption/source | 9pt | Normal, muted color (t3) |
| Stat hero number | 72pt (56pt if >5 chars) | Bold, accent color |
| Stat context | 18pt (= stat / 4, floor 16pt) | Normal, t2 |

**Font:** The Databricks template uses DM Sans as the brand font. When rendering via Google Slides API, text inserted into template placeholders inherits DM Sans automatically. For manually created text boxes, specify DM Sans explicitly.

## Cross-Cutting Elements

Template layouts from the Databricks Theme master handle chrome (slide numbers, branding) automatically via the SLIDE_NUMBER placeholder (positioned at x:12.137, y:7.079). **Do not add manual slide numbers or footers when using Databricks Theme layouts.**

For Simple Light master layouts (generic), use `deck.add_chrome()`:

```python
deck.add_chrome(page_id, slide_num=3, total=12, confidential=True)
```

## Avoid

- Same layout on consecutive slides
- Centered body text (left-align; center only titles and labels)
- Generic blue (pick topic-specific colors)
- Text-only **content** slides (content slides with 3+ bullet points or feature lists need a visual element — icon, card, or chart. Power Statement slides, breather slides, and section dividers are intentionally text-dominant and don't need added visuals)
- Accent lines under titles (AI hallmark)
- Low-contrast elements (both icons AND text need contrast)
- Equal-weight colors (one must dominate)
- Building card grids from scratch when `content_c_3_column_cards` or `content_d_card_quad` exists
- Drawing rectangle backgrounds when a Card layout (`content_d_card_right/left/large`) provides them
- Using `content_a_basic` for everything — rotate through the layout family for rhythm
