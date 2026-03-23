# Scaffold Reference

One-read reference for building scaffold.js at the start of every deck. Contains palette, fonts, spacing, shadow factory, icon pipeline, fitText utility, element patterns, and pitfalls — all in pptxgenjs JavaScript.

---

## 1. Official Databricks Brand Palette

### Dark Theme (Default — Navy 900 Background System)

**Primary palette:**

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **bg** | Navy 900 | `0B2026` | Slide background |
| **bgCard** | Navy 800 | `1B3139` | Card backgrounds |
| **bgLight** | Gray - Navigation | `303F47` | Lighter card variant, interactive elements |
| **primary** | Lava 600 | `FF3621` | Databricks red (use sparingly) |
| **green** | Green 600 | `00A972` | Success, complete, positive |
| **blue** | Blue 600 | `3B8FD4` | Info, neutral emphasis |
| **yellow** | Yellow 600 | `FFAB00` | Warning, highlight, next |
| **maroon** | Maroon 600 | `C4243E` | Deep emphasis (18pt+ only, never body text) |

**Secondary palette:**

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **Lava 500** | Lava light | `FF5F46` | Lighter red variant |
| **Oat Medium** | Oat | `EEEDE9` | Light backgrounds (light theme only) |
| **Oat Light** | Oat light | `F9F7F4` | Lightest background (light theme only) |
| **Gray - Lines** | Lines | `DCE0E2` | Borders, dividers, body text on dark bg |
| **Gray - Text** | Text | `9EADB5` | Muted text, captions, footnotes on dark bg |
| **Gray - Navigation** | Nav | `303F47` | Navigation elements, card fills on dark bg |

**Light callout background variants** (darken to ~15% visible on dark bg):

| Key | Hex |
|-----|-----|
| greenLight | `0D2920` |
| blueLight | `0D1F2D` |
| yellowLight | `2D2510` |
| lavaLight | `2D1510` |
| maroonLight | `1D0D10` |

**Text hierarchy (dark theme):**

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| **t1** | White | `FFFFFF` | Titles, hero text |
| **t2** | Gray - Lines | `DCE0E2` | Body text, bullet points |
| **t3** | Gray - Text | `9EADB5` | Secondary labels, captions, footnotes (~7:1 on bg, ~5:1 on bgCard) |

Note: The brand palette supports 3 text contrast levels on Navy 900 backgrounds, not 4. Gray-Navigation (`303F47`) is too low-contrast for readable text on Navy 900 — use it only for backgrounds and borders, never for text.

### Dark Palette Code

```javascript
const DARK_PALETTE = {
  bg: "0B2026", bgCard: "1B3139", bgLight: "303F47",
  lava: "FF3621", lavaLight: "2D1510",
  green: "00A972", greenLight: "0D2920",
  blue: "3B8FD4", blueLight: "0D1F2D",
  yellow: "FFAB00", yellowLight: "2D2510",
  maroon: "C4243E", maroonLight: "1D0D10",
  navy: "1B5162",
  t1: "FFFFFF", t2: "DCE0E2", t3: "9EADB5",
  border: "303F47"
};
```

### Light Theme (Scaffolded — Dark Recommended)

Light theme is scaffolded but incomplete. Use dark theme for production decks.

**Light theme text colors (on white/oat backgrounds):**

| Role | Hex | Contrast | Usage |
|------|-----|----------|-------|
| **Body text** | `333333` | 12.6:1 | Primary body copy |
| **Subtitle/secondary** | `545454` | 7.1:1 | Secondary descriptive text |
| **Source/fine print** | `595959` | 7.0:1 | Citations, footnotes, legal text |
| **Accent text (large)** | `C42B1A` | 7.0:1 | Hero metrics, emphasized numbers (use `FF3621` for borders only) |
| **Card borders** | `B0B0B0` | 3.2:1 | Visual separation |
| **Metric card bg** | `E8E8E8` | - | Subtle background differentiation |
| **CTA contact (on #1B3139)** | `E0E0E0` | 9.0:1 | Contact info in dark CTA sections |

```javascript
const LIGHT_PALETTE = {
  bg: "FFFFFF", bgCard: "F9F7F4", bgLight: "EEEDE9",
  lava: "FF3621", lavaLight: "FFF0ED",
  green: "00A972", greenLight: "E6F7F0",
  blue: "3B8FD4", blueLight: "E8F2FC",
  yellow: "FFAB00", yellowLight: "FFF8E6",
  maroon: "C4243E", maroonLight: "FCEDEF",
  navy: "1B5162",
  t1: "333333", t2: "545454", t3: "595959",
  border: "B0B0B0"
};
```

### Theme Switch

```javascript
// Config: set theme at top of scaffold.js
const THEME = "dark"; // "dark" | "light"
const C = THEME === "dark" ? DARK_PALETTE : LIGHT_PALETTE;
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
| Section labels | Rotate: green, blue, yellow |

**Rule:** Lava red is the Databricks signature. Use it for ONE accent per slide max (title accent, CTA button, or key stat). Overuse dilutes brand impact.

### Display Accessibility Mandate

Slides will be shown on cheap LCD TVs in bright conference rooms, old Windows laptops with TN panels, and projectors — NOT just Retina MacBooks. Design for worst-case: assume 30-50% contrast loss from ambient light and panel quality.

| Minimum contrast targets | Ratio | Why |
|--------------------------|-------|-----|
| All readable text on bg | **7:1+** | Survives bright-room washout |
| Accent text (large, 18pt+) | **5:1+** | Still visible on cheap panels |
| Decorative only (bars, shapes) | **3:1+** | Non-text, supplementary |

**Rules:**
- Card body text: always `t2`, never `t3` — t3 on card backgrounds is reserved for 12pt+ footnotes only
- Maroon (`C4243E`): decorative elements and 18pt+ text only — never body text
- Blue (`3B8FD4`): text-safe on both bg and bgCard
- `t3` (`9EADB5`): ~7:1 on bg (`0B2026`), ~5:1 on bgCard — safe for secondary labels
- When in doubt, bump UP one contrast level — nobody ever complained a slide was too readable

### Alternative Themes

| Theme | bg | bgCard | primary | secondary | accent | t1 | t2 | t3 |
|-------|-----|--------|---------|-----------|--------|------|------|------|
| **Midnight** | 1A1A2E | 16213E | 0F3460 | 533483 | E94560 | FFFFFF | C8D6E5 | 9DAFC0 |
| **Ocean** | 0A1628 | 142238 | 065A82 | 1C7293 | F5A623 | FFFFFF | B8D4E3 | 96B8CC |
| **Teal Trust** | 0B1E25 | 132E38 | 028090 | 00A896 | 02C39A | FFFFFF | C8E6E0 | 95C4BA |
| **Forest** | 1B2A1B | 2C3E2C | 2C5F2D | 97BC62 | F5A623 | FFFFFF | D4E2D4 | A8BFA8 |

---

## 2. Typography

### Font Constants

DM Sans is the Databricks brand font. It must be installed locally for accurate eval PNGs:

```bash
brew install --cask font-dm-sans
```

Fallbacks when DM Sans is unavailable: Trebuchet MS for headers, Calibri for body.

```javascript
const FH = "DM Sans";       // Header font (fallback: "Trebuchet MS")
const FB = "DM Sans";       // Body font   (fallback: "Calibri")
```

### Font Size Rules

| Element | Size | Style |
|---------|------|-------|
| Slide title | 28-40pt | Bold, FH |
| Section label | 9-10pt | Bold, UPPERCASE, `charSpacing: 3` |
| Card/row title | 14pt | Bold, FH |
| Body/description | 14pt | Normal, FB |
| Caption/source | 9pt | Normal, muted color (t3), italic |
| Stat hero number | 72pt (56pt if >5 chars) | Bold, accent color |
| Stat context | 18pt (= stat / 4, floor 16pt) | Normal, t2 |

### Section Label Pattern

Spaced uppercase above every content slide title. Rotate colors: green, blue, yellow.

```javascript
s.addText("SECTION NAME", {
  x: 0.8, y: 0.35, w: 3, h: 0.3,
  fontSize: 10, fontFace: FB, bold: true,
  color: C.lava, charSpacing: 3, margin: 0
});
```

---

## 3. Spacing Rules

### Required Spacing Values

| Between | Minimum |
|---------|---------|
| Cards (horizontal) | 0.3" |
| Cards (vertical) | 0.4" |
| Card padding (all sides) | 0.2" |
| Bullet groups | 0.15" vertical |
| Title to content | 0.5" vertical |

### Slide Dimensions

- Layout: `LAYOUT_16x9` = 10" wide x 5.625" tall
- Margins: 0.5" minimum from all edges
- Gaps: 0.3" minimum between content blocks

---

## 4. Shadow Factory

pptxgenjs mutates shadow objects in place. MUST be a factory function — never reuse a shadow object.

```javascript
const shd = () => ({
  type: "outer",
  blur: 6,
  offset: 2,
  angle: 135,
  color: "000000",
  opacity: 0.25
});
```

---

## 5. Icon Pipeline

react-icons rendered to SVG, converted to PNG via sharp, then embedded as base64.

### Setup

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
```

### Icon Render Function

```javascript
async function iconPng(IC, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IC, { color: "#" + color, size: String(size) })
  );
  return "image/png;base64," +
    (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}
```

### Pre-render ALL Icons Before Building Slides

```javascript
const { FaCheckCircle, FaChartBar, FaDatabase } = require("react-icons/fa");

const I = {};
I.check = await iconPng(FaCheckCircle, C.green);
I.chart = await iconPng(FaChartBar, C.blue);
I.db    = await iconPng(FaDatabase, C.lava);
```

### Use in Slide

Display size set by w/h in inches, NOT the render size:

```javascript
s.addImage({ data: I.check, x: 0.85, y: 1.0, w: 0.22, h: 0.22 });
```

### Available Icon Sets

| Package | Library |
|---------|---------|
| `react-icons/fa` | Font Awesome |
| `react-icons/md` | Material Design |
| `react-icons/hi` | Heroicons |
| `react-icons/bi` | Bootstrap Icons |

---

## 6. Image Placement Standards

### Dark Slide Image Framing

Most documentation diagrams and product screenshots have white backgrounds. On dark slides (`bg: 0B2026`), a white-background image has invisible edges. Always add a white rounded-rectangle frame behind the image:

```javascript
// White frame (slightly larger than image, with shadow)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: imgX - 0.1, y: imgY - 0.1, w: imgW + 0.2, h: imgH + 0.2,
  fill: { color: "FFFFFF" },
  rectRadius: 0.1,
  shadow: shd()
});
// Image on top
s.addImage({
  path: './images/diagram.png',
  x: imgX, y: imgY, w: imgW, h: imgH,
  sizing: { type: 'contain', w: imgW, h: imgH }
});
```

On light slides (oat bg, white bg), the white frame is unnecessary.

### Image Sizing Presets (10" x 5.625" slide)

| Use Case | Position & Size | Notes |
|---|---|---|
| Full-width hero diagram | `x:0.5, y:1.5, w:9.0, h:3.5` | Title above, caption below. Max image-to-slide ratio. |
| Image-right with text | `x:5.0, y:1.2, w:4.5, h:3.8` | Text occupies left 4.5". |
| Image-left with text | `x:0.5, y:1.2, w:4.5, h:3.8` | Text occupies right 4.5". |
| Side-by-side comparison | `x:0.3, y:1.5, w:4.4, h:3.2` + `x:5.3, y:1.5, w:4.4, h:3.2` | Two images compared. |
| Small supporting inset | `x:6.5, y:3.5, w:3.0, h:2.0` | Reinforces a text-dominant slide. Not the hero element. |

**Always use `sizing: { type: 'contain' }`** to prevent aspect-ratio distortion.

### Caption Standards

Every real image gets a source caption. Captions use `t3` color, 9pt, italic, centered below the image:

```javascript
s.addText("Source: Databricks documentation — Lakehouse architecture", {
  x: imgX, y: imgY + imgH + 0.1, w: imgW, h: 0.25,
  fontSize: 9, fontFace: FB, color: C.t3, italic: true, align: "center"
});
```

On light backgrounds, use `595959` instead of `C.t3`.

### Image Accessibility

- **Minimum resolution**: Images must look crisp at 200% zoom. 72dpi screenshots pixelate on projection. Prefer 2x resolution source images.
- **Dense diagrams**: Add a speaker note: "NOTE: This diagram has fine detail. Pause to let the audience absorb it."
- **Low-contrast images**: Some docs use light gray on white. These vanish on washed-out projectors. Rebuild key elements as shapes where you control contrast, or flag in speaker notes.

---

## 7. Element Patterns (pptxgenjs Code)

### Card with Left Accent Bar

```javascript
// Card background
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 2.85, h: 1.3,
  fill: { color: C.bgCard }, shadow: shd()
});
// Left accent bar (layered on top)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 0.06, h: 1.3,
  fill: { color: C.blue }
});
// Card title
s.addText("Card Title", {
  x: 0.72, y: 1.5, w: 2.4, h: 0.35,
  fontSize: 14, fontFace: FH, bold: true, color: C.t1, margin: 0
});
// Card body
s.addText("Description text", {
  x: 0.72, y: 1.85, w: 2.4, h: 0.75,
  fontSize: 14, fontFace: FB, color: C.t2, margin: 0, valign: "top"
});
```

### Icon in Colored Circle

```javascript
// Circle background
s.addShape(pres.shapes.OVAL, {
  x: 0.85, y: 1.75, w: 0.5, h: 0.5,
  fill: { color: C.blue }
});
// Icon centered inside (offset ~0.11" from oval edge)
s.addImage({ data: I.check, x: 0.96, y: 1.86, w: 0.28, h: 0.28 });
```

### Callout Bar

Full-width or partial-width bar at bottom of slide for key messages:

```javascript
// Background bar
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 4.7, w: 10, h: 0.65,
  fill: { color: C.blueLight }
});
// Callout text
s.addText("Key message for this slide", {
  x: 0.8, y: 4.7, w: 8.4, h: 0.65,
  fontSize: 14, fontFace: FB, bold: true,
  color: C.blue, align: "center", valign: "middle"
});
```

### Cover Slide Geometric Accent

L-shaped lines in top-right corner:

```javascript
// Horizontal line
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.5, y: 0, w: 2.5, h: 0.06,
  fill: { color: C.lava }
});
// Vertical line
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.94, y: 0, w: 0.06, h: 2.5,
  fill: { color: C.lava }
});
```

### Arrow Between Boxes

Horizontal connector arrow for architecture flows:

```javascript
s.addShape(pres.shapes.LINE, {
  x: 4.6, y: 2.9, w: 0.5, h: 0,
  line: { color: C.t3, width: 2.5, dashType: "solid",
          endArrowType: "triangle" }
});
```

### Section Label

```javascript
s.addText("SECTION NAME", {
  x: 0.8, y: 0.35, w: 3, h: 0.3,
  fontSize: 10, fontFace: FB, bold: true,
  color: C.lava, charSpacing: 3, margin: 0
});
```

### Text Patterns

**Title:**
```javascript
s.addText("Slide Title", {
  x: 0.8, y: 0.7, w: 8, h: 0.5,
  fontSize: 28, fontFace: FH, bold: true, color: C.t1, margin: 0
});
```

**Body text:**
```javascript
s.addText("Description text here", {
  x: 0.8, y: 1.3, w: 4, h: 0.6,
  fontSize: 14, fontFace: FB, color: C.t2, margin: 0, valign: "top"
});
```

**Rich text (mixed formatting):**
```javascript
s.addText([
  { text: "Bold part ", options: { bold: true, color: C.t1 } },
  { text: "normal part", options: { color: C.t2 } }
], { x: 1, y: 3, w: 8, h: 0.4, fontSize: 14, fontFace: FB, margin: 0 });
```

**Multi-line (MUST use breakLine: true):**
```javascript
s.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }
], { x: 0.5, y: 0.5, w: 8, h: 2, fontSize: 14, fontFace: FB, color: C.t2 });
```

**Critical:** Set `margin: 0` whenever aligning text with shapes/icons at the same x-position.

### Shapes

**Card background with shadow:**
```javascript
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 2.85, h: 1.3,
  fill: { color: C.bgCard }, shadow: shd()
});
```

**Left accent bar:**
```javascript
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 0.06, h: 1.3,
  fill: { color: C.blue }
});
```

**Line (dividers/connectors):**
```javascript
s.addShape(pres.shapes.LINE, {
  x: 2.6, y: 3.0, w: 0.5, h: 0,
  line: { color: C.t3, width: 2.5 }
});
```

**Oval (icon circle background):**
```javascript
s.addShape(pres.shapes.OVAL, {
  x: 0.85, y: 1.75, w: 0.5, h: 0.5,
  fill: { color: C.blue }
});
```

**Transparent overlay:**
```javascript
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "000000", transparency: 40 }
});
```

### Tables

```javascript
const rows = [
  // Header row
  [
    { text: "Dimension", options: { fill: { color: C.bgLight }, color: C.t1, bold: true, fontSize: 11, fontFace: FB } },
    { text: "Value", options: { fill: { color: C.bgLight }, color: C.t1, bold: true, fontSize: 11, fontFace: FB, align: "center" } }
  ],
  // Data rows
  [
    { text: "Row 1", options: { fill: { color: C.bgCard }, fontSize: 11, fontFace: FB, color: C.t2 } },
    { text: "Data", options: { fill: { color: C.bgCard }, fontSize: 12, fontFace: FB, bold: true, color: C.green, align: "center" } }
  ]
];
s.addTable(rows, {
  x: 0.5, y: 2.8, w: 9,
  colW: [3, 6],
  border: { pt: 0.5, color: C.border },
  rowH: [0.4, 0.4]
});
```

### Charts

```javascript
s.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1", "Q2", "Q3"], values: [45, 55, 62]
}], {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",
  chartColors: [C.blue, C.green, C.lava],
  chartArea: { fill: { color: C.bgCard }, roundedCorners: true },
  catAxisLabelColor: C.t3, valAxisLabelColor: C.t3,
  valGridLine: { color: C.border, size: 0.5 },
  catGridLine: { style: "none" },
  showValue: true, dataLabelColor: C.t1, showLegend: false
});
```

### Backgrounds and Notes

```javascript
// Solid background
s.background = { color: C.bg };

// Base64 image background
s.background = { data: "image/png;base64,..." };

// Speaker notes
s.addNotes("Talk Track (60s): Key message.\n\nPoint 1.\nPoint 2.");
```

---

## 8. fitText() Utility

Before rendering any text box, call `fitText()` to calculate the minimum box height needed. Prevents "text crushed into too-small box" failures.

```javascript
/**
 * Estimates required height for text at given fontSize within maxWidth.
 * Uses character-count heuristic (not pixel-perfect, but prevents gross overflow).
 *
 * @param {string} text - The text to measure
 * @param {number} fontSize - Font size in points
 * @param {number} maxWidth - Available width in inches
 * @returns {{ lines: number, height: number }} - Estimated line count and required height in inches
 */
function fitText(text, fontSize, maxWidth) {
  const charsPerInch = 72 / fontSize * 1.8;  // approximate chars per inch at fontSize
  const charsPerLine = Math.floor(maxWidth * charsPerInch);
  const lineCount = Math.ceil(text.length / charsPerLine);
  const lineHeight = fontSize / 72 * 1.4;    // fontSize in points -> inches, with 1.4x line spacing
  return { lines: lineCount, height: lineCount * lineHeight };
}
```

**Usage:** Before rendering any text box, call `fitText()`. If required height > allocated height, either increase the box or split the content across slides.

```javascript
const bodyText = "A long paragraph that might overflow the card...";
const fit = fitText(bodyText, 14, 2.4); // 14pt in 2.4" wide box
const boxH = Math.max(0.75, fit.height); // minimum 0.75", expand if needed

s.addText(bodyText, {
  x: 0.72, y: 1.85, w: 2.4, h: boxH,
  fontSize: 14, fontFace: FB, color: C.t2, margin: 0, valign: "top"
});
```

---

## 9. Pitfalls (File Corruption & Visual Bugs)

| Mistake | Fix |
|---------|-----|
| `color: "#FF0000"` | Remove `#` prefix. Use `color: "FF0000"` |
| 8-char hex in shadow color `"00000020"` | Use `color: "000000", opacity: 0.12` |
| Reusing shadow object across calls | Use factory function: `const shd = () => ({...})` |
| Unicode bullets `"\u2022 item"` | Use `bullet: true` property |
| Missing `breakLine: true` in text arrays | Text runs together without it |
| Negative shadow offset | Corrupts file. Must be >= 0 |
| `ROUNDED_RECTANGLE` with accent overlay bar | Overlay doesn't cover corners. Use plain `RECTANGLE` for cards with accent bars |
| `lineSpacing` with bullets | Causes huge gaps. Use `paraSpaceAfter` instead |
| `letterSpacing` (silently ignored) | Use `charSpacing` instead |
| Colors with `#` prefix | pptxgenjs uses raw hex strings without `#` everywhere |

---

## 10. Template Icons & Illustrations Library

The Databricks Corporate Template contains 34 slides of brand icons (slides 52-85) and 11 illustration slides (slides 87-97).

### Icon Categories

| Category | Template Slides | Use For |
|----------|----------------|---------|
| **High Level Icons** | Slide 53 | Simple, Open, Collaborative, Training, Support, Professional Services |
| **Industry Icons** | Slide 54 | 14 industry tiles (illustrated squares) — vertical-specific pitches |
| **Platform** | Slides 56-57 | Analytics, Business Insights, Collaborative Data Science, Data Pipelines |
| **Feature** | Slide 58 | Accelerator-Aware Scheduler, Built-in Functions, JDK 11, Join Hints |
| **Monitoring** | Slide 59 | Monitoring-related icons |
| **Connectors** | Slide 60 | Integration and connector icons |
| **Performance** | Slide 61 | Performance-related icons |
| **Financial Services** | Slide 67 | Credit Analysis, Customer Analysis, Financial Modeling |
| **Healthcare and Life Sciences** | Slide 68 | Clinical Data, Genomics, Healthcare, Medical Imaging, Medical IoT, Social Medicine |
| **Media and Entertainment** | Slide 69 | M&E vertical icons |
| **Retail / CPG** | Slide 70 | Retail vertical icons |
| **Public Sector** | Slide 71 | Government/public sector icons |
| **Security** | Slides 73-79 | 7 pages of security icons — governance, compliance, NFR slides |
| **Miscellaneous** | Slides 80-85 | General-purpose icons, arrows |

### Illustration Categories

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
| **Healthcare / HLS** | Slide 68 | Slide 92 (Lakehouse) or Slide 95 (Solutions) |
| **Financial Services** | Slide 67 | Slide 90 (Customers) or Slide 95 (Solutions) |
| **Retail / CPG** | Slide 70 | Slide 90 (Customers) or Slide 95 (Solutions) |
| **Public Sector** | Slide 71 | Slide 95 (Solutions) |
| **General platform** | Slides 56-57 + Slide 53 | Slide 92 (Lakehouse) |
| **Security / Governance** | Slides 73-79 | Slide 97 (Unity Catalog) |
| **Data Engineering** | Slide 58 + Slides 56-57 | Slide 98 (Data Engineering) or Slide 91 (DLT) |

### How to Use Template Icons

Icons are embedded as image elements on template slides. To use them:
1. **Copy from the template slide** — extract specific icon images from the source slide
2. **Position and resize** — 0.4-0.6" for category markers in cards, 0.8-1.2" for hero visual elements
3. **Don't overuse** — 1-3 icons per content slide maximum

---

## 11. Complete Scaffold.js Template

This is what the agent writes at the start of every deck build. All subsequent slide scripts import from this module.

```javascript
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// ── Icon imports (adjust per deck) ──────────────────────────────
const {
  FaCheckCircle, FaChartBar, FaDatabase, FaShieldAlt,
  FaArrowRight, FaLightbulb, FaExclamationTriangle
} = require("react-icons/fa");

// ── Icon renderer ───────────────────────────────────────────────
async function iconPng(IC, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IC, { color: "#" + color, size: String(size) })
  );
  return "image/png;base64," +
    (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

// ── Palette ─────────────────────────────────────────────────────
const DARK_PALETTE = {
  bg: "0B2026", bgCard: "1B3139", bgLight: "303F47",
  lava: "FF3621", lavaLight: "2D1510",
  green: "00A972", greenLight: "0D2920",
  blue: "3B8FD4", blueLight: "0D1F2D",
  yellow: "FFAB00", yellowLight: "2D2510",
  maroon: "C4243E", maroonLight: "1D0D10",
  navy: "1B5162",
  t1: "FFFFFF", t2: "DCE0E2", t3: "9EADB5",
  border: "303F47"
};

const LIGHT_PALETTE = {
  bg: "FFFFFF", bgCard: "F9F7F4", bgLight: "EEEDE9",
  lava: "FF3621", lavaLight: "FFF0ED",
  green: "00A972", greenLight: "E6F7F0",
  blue: "3B8FD4", blueLight: "E8F2FC",
  yellow: "FFAB00", yellowLight: "FFF8E6",
  maroon: "C4243E", maroonLight: "FCEDEF",
  navy: "1B5162",
  t1: "333333", t2: "545454", t3: "595959",
  border: "B0B0B0"
};

const THEME = "dark"; // "dark" | "light"
const C = THEME === "dark" ? DARK_PALETTE : LIGHT_PALETTE;

// ── Fonts ───────────────────────────────────────────────────────
const FH = "DM Sans";  // Header font (fallback: "Trebuchet MS")
const FB = "DM Sans";  // Body font   (fallback: "Calibri")

// ── Shadow factory (MUST be function — pptxgenjs mutates in place) ──
const shd = () => ({
  type: "outer", blur: 6, offset: 2, angle: 135,
  color: "000000", opacity: 0.25
});

// ── fitText utility ─────────────────────────────────────────────
function fitText(text, fontSize, maxWidth) {
  const charsPerInch = 72 / fontSize * 1.8;
  const charsPerLine = Math.floor(maxWidth * charsPerInch);
  const lineCount = Math.ceil(text.length / charsPerLine);
  const lineHeight = fontSize / 72 * 1.4;
  return { lines: lineCount, height: lineCount * lineHeight };
}

// ── Presentation setup ──────────────────────────────────────────
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" x 5.625"
pres.author = "Databricks";
pres.title = "DECK_TITLE";

// ── Pre-render icons ────────────────────────────────────────────
async function preRenderIcons() {
  const I = {};
  I.check    = await iconPng(FaCheckCircle, C.green);
  I.chart    = await iconPng(FaChartBar, C.blue);
  I.db       = await iconPng(FaDatabase, C.lava);
  I.shield   = await iconPng(FaShieldAlt, C.blue);
  I.arrow    = await iconPng(FaArrowRight, C.t2);
  I.bulb     = await iconPng(FaLightbulb, C.yellow);
  I.warning  = await iconPng(FaExclamationTriangle, C.yellow);
  return I;
}

// ── Exports ─────────────────────────────────────────────────────
module.exports = {
  pres, C, FH, FB, shd, fitText,
  iconPng, preRenderIcons,
  DARK_PALETTE, LIGHT_PALETTE
};
```

**Usage from slide scripts:**

```javascript
const { pres, C, FH, FB, shd, fitText, preRenderIcons } = require("./scaffold");

async function main() {
  const I = await preRenderIcons();

  // === SLIDE 1: Cover ===
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    // ... elements
  }

  // === SLIDE 2: Content ===
  {
    const s = pres.addSlide();
    s.background = { color: C.bg };
    // ... elements
  }

  await pres.writeFile({ fileName: "output.pptx" });
  console.log("Done: output.pptx");
}

main().catch(e => { console.error(e); process.exit(1); });
```

Each slide in its own block scope `{ const s = ... }` keeps variables clean and avoids conflicts.

### File Output

```javascript
await pres.writeFile({ fileName: "output.pptx" });
```
