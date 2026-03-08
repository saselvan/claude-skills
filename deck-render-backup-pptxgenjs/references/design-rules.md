# Design Rules

## Before Starting

1. **Topic-specific palette** — If swapping your colors into a different deck would still "work," your choices aren't specific enough.
2. **Color dominance** — One color at 60-70% visual weight, 1-2 supporting tones, one sharp accent. Never equal weight.
3. **Dark or light, commit** — Dark throughout = premium feel (recommended for technical decks). Or dark sandwich (title + conclusion dark, content light).
4. **One visual motif, everywhere** — Pick ONE and repeat across every slide: left-edge accent bars, icons in colored circles, spaced uppercase section labels, consistent card shadows.

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

```javascript
// Official Databricks brand palette
const C = {
  bg1: "0B2026", bgCard: "1B3139", bgLight: "303F47",  // Navy 900, Navy 800, Gray-Navigation
  lava: "FF3621", lavaLight: "2D1510",      // Lava 600 - use sparingly
  green: "00A972", greenLight: "0D2920",    // Green 600
  blue: "2272B4", blueLight: "0D1F2D",      // Blue 600
  yellow: "FFAB00", yellowLight: "2D2510",  // Yellow 600
  maroon: "98102A", maroonLight: "1D0D10",  // Maroon 600
  navy: "1B5162",                           // Mid-tone for variety
  t1: "FFFFFF", t2: "DCE0E2", t3: "5A6F77", t4: "5A6F77",  // White, Gray-Lines, Gray-Text, Gray-Text
  border: "303F47"                                            // Gray-Navigation
};
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
```

## Slide Layouts (Vary — Never Repeat Same Layout Consecutively)

### Card Grid (2×3 or 2×2)
Best for: feature lists, capabilities, comparison points
```
[accent bar][icon] Title    [accent bar][icon] Title    [accent bar][icon] Title
            Description                 Description                 Description
```

### Two-Column Comparison
Best for: before/after, Delta vs Lakebase, pros/cons
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
```
[accent][icon] Title ──── Bold Spec ──── Muted description
[accent][icon] Title ──── Bold Spec ──── Muted description
```

### Architecture Flow (left → right)
Best for: data flow, architecture, pipelines
```
┌──────┐  ─▶  ┌──────┐  ─▶  ┌═══════════╗  ─▶  ┌──────┐
│SOURCE│      │BRIDGE│      ║ HERO STEP  ║      │TARGET│
│ sub  │      │ sub  │      ║  KEY STAT  ║      │ sub  │
└──────┘      └──────┘      ╚═══════════╝      └──────┘
```

**Mandatory requirements for architecture slides:**
- **Arrows between EVERY box** — use `pres.shapes.LINE` with `endArrowType: "triangle"`. No arrows = no flow. The audience must never have to infer reading order.
- **Hero step callout** — the most important/differentiating step (e.g., "~15s sync", "zero-copy") should be visually larger, use a standout color, and have its key metric in 16-22pt bold. If nothing stands out, the architecture is a wall of equal boxes.
- **4-5 boxes per flow path max** — consolidate related steps into one box with subtitle text. "Bronze → Jobs → Gold" = one "Delta Lakehouse" box.
- **Path labels** — if multiple paths exist (READ/WRITE, ingest/serve), use small bold headers above each path with distinct accent colors.
- **Connecting bar** — a full-width callout bar (e.g., "One Platform — governed by Unity Catalog") between paths ties the architecture together conceptually.
- **Zero-crossing-lines rule** — if connector lines cross each other, the diagram reads as spaghetti. Rearrange boxes to eliminate crossings. One crossing maximum in complex diagrams; zero is the target.
- **NFR governance wrapper** — technical gatekeepers look for security, scale, and governance. Wrap the architecture with a subtle "Governed by Unity Catalog" or "HIPAA-compliant environment" bar along the bottom or top. This pre-empts the gatekeeper's primary objection before they ask it. Use `bgLight` fill with `t3` text — visible but not dominant.

```javascript
// Arrow helper with triangle head
function arrow(s, x, y, w, color) {
  s.addShape(pres.shapes.LINE, {
    x, y, w, h: 0,
    line: { color, width: 1.5, endArrowType: "triangle" },
  });
}

// Hero step — visually larger, standout color
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.85, y: rY - 0.1, w: 1.3, h: bH + 0.2,  // taller than siblings
  fill: { color: C.blueLight }, shadow: shd(),
});
s.addText("~15 sec", {
  x: 5.95, y: rY, w: 1.1, h: 0.3,
  fontSize: 18, fontFace: FH, bold: true, color: C.blue,  // 2-3× larger than other boxes
  align: "center", margin: 0,
});
```

### Quote Card
Best for: objections, customer quotes, key statements
```
❝ (icon)
┌─ gold bar ──────────────────────┐
│ "The quote text goes here..."   │
└─────────────────────────────────┘
```

### Before/After Panels (Competitive Framing)
Best for: proof points, transformation stories, "Why [Product]" slides, differentiator arguments
```
┌─ muted header ──────┐      ┌─ green header ────────┐
│ Pain / traditional   │  ──▶ │ ✓ With product        │
│ (t3 muted text)      │      │ (t2 bright text)      │
│                      │      │ [icon] highlight       │
└──────────────────────┘      └───────────────────────┘
```

**This is the preferred layout for any "Why [Product]" or "Key Differentiators" slide.** A vertical list of product features is not differentiation — it's a brochure. The Before/After layout forces competitive positioning by requiring you to articulate what the alternative looks like.

**Visual treatment:**
- **Left column ("Without"):** muted background (`maroonLight` or `bgCard`), t3 text color, no icons. This should feel old/painful.
- **Right column ("With"):** highlighted with green accent bars, t2 text, icons per row. This should feel modern/confident.
- **Arrow between headers** (optional): a single arrow icon between the column headers reinforces the transformation narrative.
- **Each row is a contrast pair:** don't just list features on the right — state the specific pain on the left that each feature resolves.

```javascript
// Left: "Without" header
s.addShape(pres.shapes.RECTANGLE, {
  x: leftX, y: headerY, w: colW, h: 0.45,
  fill: { color: C.maroonLight },
});
s.addText("Without [Product]", { /* ... t1 color, bold ... */ });

// Right: "With" header
s.addShape(pres.shapes.RECTANGLE, {
  x: rightX, y: headerY, w: colW, h: 0.45,
  fill: { color: C.greenLight },
});
s.addText("With [Product]", { /* ... green color, bold ... */ });

// Each comparison row:
// Left: pain text in t3 (muted)
// Right: solution text in t2 (bright) with green accent bar + icon
```

### Objection Handling / "The Elephant in the Room"
Best for: Dismantling competitor claims, addressing NFRs (security, scale), resolving known internal resistance
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
- **Left column ("The Objection"):** `maroon` top accent bar, italic `t3` text framed as a quote. This should feel like "what people say" — not your words.
- **Right column ("The Reality"):** `green` top accent bar, bold `t1` header with `t2` evidence bullets. This should feel authoritative, not defensive.
- **The pivot:** Never just say "no, we do that." Provide a specific mechanism or proof point on the right side. Name a feature, cite a customer, show a number.

```javascript
// Left Card: The Objection
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.8, w: 4.0, h: 2.2,
  fill: { color: C.bgCard }, shadow: shd()
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.8, w: 4.0, h: 0.08,
  fill: { color: C.maroon }
});
s.addText('"Databricks is too complex for our BI analysts."', {
  x: 0.8, y: 2.2, w: 3.4, h: 1.2,
  fontSize: 16, fontFace: FB, italic: true, color: C.t3, margin: 0
});

// Arrow between cards
s.addShape(pres.shapes.LINE, {
  x: 4.6, y: 2.9, w: 0.5, h: 0,
  line: { color: C.t3, width: 1.5, endArrowType: "triangle" },
});

// Right Card: The Reality
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.8, w: 4.3, h: 2.2,
  fill: { color: C.bgCard }, shadow: shd()
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.8, w: 4.3, h: 0.08,
  fill: { color: C.green }
});
s.addText("Serverless SQL + AI/BI", {
  x: 5.5, y: 2.1, w: 3.7, h: 0.4,
  fontSize: 18, fontFace: FH, bold: true, color: C.t1, margin: 0
});
s.addText([
  { text: "Analysts query in standard SQL or plain English.", options: { breakLine: true } },
  { text: "Zero infrastructure to manage or tune.", options: { breakLine: true } },
], {
  x: 5.5, y: 2.6, w: 3.7, h: 1.0,
  fontSize: 12, fontFace: FB, color: C.t2, bullet: true, margin: 0
});
```

### Numbered Takeaway Cards
Best for: summary, key messages
```
┌─ accent bar ─────────────────────────────────────────┐
│ [numbered circle] Title in brand color               │
│                   Description in muted text           │
└──────────────────────────────────────────────────────┘
```

## Element Patterns (Code Snippets)

### Section label (spaced uppercase above every title)
```javascript
s.addText("SECTION NAME", {x:0.8, y:0.35, w:3, h:0.3, fontSize:10, fontFace:FB, bold:true, color:C.accent, charSpacing:3, margin:0});
```

### Card with left accent bar
```javascript
s.addShape(pres.shapes.RECTANGLE, {x, y, w:2.85, h:1.3, fill:{color:C.bgCard}, shadow:shd()});
s.addShape(pres.shapes.RECTANGLE, {x, y, w:0.06, h:1.3, fill:{color:brandColor}});
```

### Icon in colored circle
```javascript
s.addShape(pres.shapes.OVAL, {x:0.85, y:1.75, w:0.5, h:0.5, fill:{color:brandColor}});
s.addImage({data:iconBase64, x:0.96, y:1.86, w:0.28, h:0.28}); // offset ~0.11" to center
```

### Callout bar (bottom of slide)
```javascript
s.addShape(pres.shapes.RECTANGLE, {x:0.5, y:4.7, w:9, h:0.45, fill:{color:C.blueLight}});
s.addShape(pres.shapes.RECTANGLE, {x:0.5, y:4.7, w:0.06, h:0.45, fill:{color:C.blue}});
s.addText("Key message", {x:0.8, y:4.7, w:8.5, h:0.45, fontSize:13, fontFace:FB, bold:true, color:C.blue, valign:"middle", margin:0});
```

### Cover slide geometric accent
```javascript
s.addShape(pres.shapes.RECTANGLE, {x:7.5, y:0, w:2.5, h:0.06, fill:{color:C.accent}});
s.addShape(pres.shapes.RECTANGLE, {x:9.94, y:0, w:0.06, h:2.5, fill:{color:C.accent}});
```

## Typography

| Element | Size | Style |
|---------|------|-------|
| Slide title | 28-40pt | Bold, header font |
| Section label | 9-10pt | Bold, UPPERCASE, charSpacing:3 |
| Card/row title | 12-14pt | Bold, header font |
| Body/description | 10.5-13pt | Normal, body font |
| Caption/muted | 7.5-10pt | Normal, muted color |

**Font pairings:** Trebuchet MS + Calibri (modern), Georgia + Calibri (authoritative), Arial Black + Arial (bold)

## Cross-Cutting Elements

Add these to every slide. Define them as helper functions in scaffold.js so they're consistent across the deck.

### Slide Number (bottom-right)
```javascript
function addSlideNumber(s, num, total) {
  s.addText(`${num} / ${total}`, {
    x: 9.0, y: 5.3, w: 0.8, h: 0.25,
    fontSize: 8, fontFace: FB, color: C.t3,
    align: "right", valign: "middle", margin: 0,
  });
}
```

### Confidentiality Footer (bottom-left)
```javascript
function addFooter(s) {
  s.addText("Databricks Confidential", {
    x: 0.3, y: 5.3, w: 2.5, h: 0.25,
    fontSize: 7, fontFace: FB, color: C.t3,
    align: "left", valign: "middle", margin: 0,
  });
}
```

### Combined Helper
```javascript
function addChromeElements(s, slideNum, totalSlides) {
  addFooter(s);
  addSlideNumber(s, slideNum, totalSlides);
}
```

**Note:** If the user will import into a branded Google Slides / PowerPoint template that provides its own footer/numbering, skip these — the template handles chrome.

## Avoid

- Same layout on consecutive slides
- Centered body text (left-align; center only titles and labels)
- Generic blue (pick topic-specific colors)
- Text-only slides (every slide needs a visual: icon, shape, chart, or card)
- Accent lines under titles (AI hallmark)
- Low-contrast elements (both icons AND text need contrast)
- Forgetting `margin:0` (causes misalignment with shapes)
- Equal-weight colors (one must dominate)
