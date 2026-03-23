# Layout Reference — Unified Key System

Single source of truth for slide layout selection. One key system, one lookup path.

**Canonical keys** come from the scaffold (e.g., `title`, `content_basic`, `content_2col`).
**Strategy terms** come from the strategy YAML (e.g., `title_slide`, `stat_hero`, `before_after`).
Both resolve to the same pptxgenjs code pattern.

---

## 1. How to Use This Table

1. **From strategy YAML**: Find the strategy term in the left column. Read across to get the scaffold key and pptxgenjs function.
2. **From content shape**: Skip to Section 3 (Secondary Lookup). Match what's on the slide to a scaffold key.
3. **Direct scaffold key**: If you already know the key (e.g., `content_card_right`), find it in the Scaffold Key column.

Every row gives you enough to write the slide. No cross-referencing other files.

---

## 2. Primary Lookup: Strategy Term -> Scaffold Key -> Code

### Strategy-Mapped Layouts

These are the terms that appear in strategy YAML `layout:` fields. Each maps to a canonical scaffold key.

| Strategy Term | Scaffold Key | pptxgenjs Function | Notes |
|---|---|---|---|
| `title_slide` | `title` | `addTitleSlideDark()` | Dark default. Light variant: swap `C.bg1` to `"F9F7F4"` and invert text colors. |
| `stat_hero` | `big_number` | `addBigNumber()` | Auto-sized. See Section 5 for sizing rules. |
| `feature_grid` | `content_3col_cards` | `addCardGrid3Col()` | 3-column card grid with accent bars. For 4 items use `content_card_quad`. |
| `two_column_validation` | `content_2col` | `addComparison()` | Two-column with colored accent borders. |
| `before_after` | `content_2col` | `addComparison(left_accent="maroon", right_accent="green")` | Pain/muted left, solution/bright right. |
| `architecture_diagram` | `blank` | Custom build | Delegate to diagram/arch-diagram skills. Embed output as image. See design-rules.md Architecture Flow. |
| `proof_points` | `content_3col_cards` or `content_card_right` | `addCardGrid3Col()` or custom | Metric cards: use 3col_cards. Customer story with image: use content_card_right. |
| `comparison_table` | `blank` | Custom `addTable()` | Blue header row (`3B8FD4`), dark body rows (`1B3139`). |
| `timeline` | `blank` | Custom timeline build | Style 1: numbered circles on line. Style 2: cards with arrows. |
| `discussion` | `content_3col_cards` | `addCardGrid3Col()` | Numbered next-step cards. Add number circles above each card. |
| `story` | `power_statement_2` | `addQuote()` | Dark bg, italic white text, maroon quotation mark. |
| `agenda` | `content_basic` | `addContentBasic()` | Numbered items with accent-colored dots or circles. |
| `objection_handling` | `content_2col` | `addComparison(left_accent="maroon", right_accent="green")` | Left: myth/objection (italic, muted t3). Right: reality (bold t1, evidence bullets). |
| `image_showcase` | `blank` or `content_card_large` | Custom image placement | Full-width real image with title above + caption below. White frame on dark bg. |
| `section_break` | `section_break` | `addSectionBreak()` | Rotate through variants across the deck. |
| `closing` | `closing` | `addClosing()` | Must have specific CTA. See Section 9 for enforcement. |

### Direct Scaffold Keys (Content-Shape Driven)

These are used when choosing layout based on content shape rather than strategy term. They do not appear in strategy YAML — the agent selects them during rendering.

| Scaffold Key | pptxgenjs Pattern | When to Use |
|---|---|---|
| `title` | `addTitleSlideDark()` | Opening slide. Variant "a" has hero image area on right. |
| `title_alt` | `addTitleSlideDark()` with image zone | Opening with hero image on right side. |
| `content_basic` | `addContentBasic()` | Single column, title + body. ONLY when no visual element exists. |
| `content_basic_white` | `addContentBasic()` with white bg | White background variant. Light theme only. |
| `content_card_right` | Custom: text left, image/card right | Text-dominant slide with supplementary visual on right. |
| `content_card_left` | Custom: image/card left, text right | Mirror of card_right. Alternate with card_right for rhythm. |
| `content_card_large` | Custom: large card/image dominant | When the visual IS the point, not supplementary. |
| `content_card_quad` | Custom: 2x2 card grid | 4 items of equal weight. |
| `content_2col` | `addComparison()` | Any two-column comparison. Accent colors distinguish intent. |
| `content_2col_icon` | `addComparison()` with icon spots | Two columns + icon placeholders above each header. |
| `content_3col` | `addContent3Col()` | 3 parallel text columns, no card backgrounds. |
| `content_3col_icon` | `addContent3Col()` with icon spots | 3 columns with icon placeholders above each. |
| `content_3col_cards` | `addCardGrid3Col()` | 3 features/capabilities with card backgrounds and accent bars. |
| `power_statement` | Custom: centered bold statement | Single bold line, centered. 1-2 lines max. |
| `power_statement_2` | `addQuote()` | Dark bg, italic white quote text. |
| `power_statement_3` | Custom: accent bg statement | Alternate power statement style. |
| `power_statement_4` | Custom: alternate accent | Alternate power statement style. |
| `big_number` | `addBigNumber()` | Hero statistic. Auto-sized. |
| `section_break` | `addSectionBreak()` | Topic transition. Rotate variants. |
| `blank` | `pres.addSlide()` | Full custom: architecture, table, timeline, logo strip. |
| `closing` | `addClosing()` | Final slide. CTA required. |

---

## 3. Secondary Lookup: Content Shape -> Layout (Quick Reference)

Start here when you know what's on the slide but not which layout to use.

| What's on the slide | Scaffold Key | Function |
|---|---|---|
| Text only, single topic | `content_basic` | `addContentBasic()` |
| Text + image right | `content_card_right` | Custom build |
| Text + image left | `content_card_left` | Custom build |
| Text + large image (image IS the point) | `content_card_large` | Custom build |
| 2 parallel things | `content_2col` | `addComparison()` |
| 2 parallel things + accent colors | `content_2col` | `addComparison(..., left_accent, right_accent)` |
| 2 parallel things + icons | `content_2col_icon` | `addComparison(..., layout="content_2col_icon")` |
| 3 parallel things (short text) | `content_3col` | `addContent3Col()` |
| 3 parallel things + icons | `content_3col_icon` | `addContent3Col()` with icon spots |
| 3 features with descriptions | `content_3col_cards` | `addCardGrid3Col()` |
| 4 items equally weighted | `content_card_quad` | Custom 2x2 grid |
| 5-6 items | `blank` + custom grid | `addCardGrid3Col()` adapted for 2 rows |
| Big number | `big_number` | `addBigNumber()` |
| Quote | `power_statement_2` | `addQuote()` |
| Bold statement (1-2 lines) | `power_statement` | Custom centered |
| Table | `blank` | `addTable()` |
| Timeline / process | `blank` | Custom timeline |
| Architecture (simple layers) | `blank` | Custom bands |
| Architecture (complex flows) | `blank` | Custom with corridor routing |
| Row of logos | `blank` | `addLogoStrip()` |

---

## 4. Layout Function Code (pptxgenjs)

**These are building blocks, not templates.** Use them as starting points but **never call the same layout function for consecutive slides**. Each slide must be individually designed after viewing the previous slide's PNG. Repetition kills visual rhythm.

### Setup (Required for All Layouts)

```javascript
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// Databricks brand palette
const C = {
  bg1: "0B2026", bgCard: "1B3139", bgLight: "303F47",
  lava: "FF3621", lavaLight: "2D1510",
  green: "00A972", greenLight: "0D2920",
  blue: "3B8FD4", blueLight: "0D1F2D",
  yellow: "FFAB00", yellowLight: "2D2510",
  maroon: "C4243E", maroonLight: "1D0D10",
  navy: "1B5162",
  t1: "FFFFFF", t2: "DCE0E2", t3: "9EADB5",
  border: "303F47"
};

const FH = "DM Sans";  // Headers (fallback: "Trebuchet MS")
const FB = "DM Sans";  // Body (fallback: "Calibri")
const shd = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.25 });

// Icon pipeline: react-icons -> sharp -> base64 PNG
async function iconPng(IC, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IC, { color: "#" + color, size: String(size) })
  );
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}
```

### addTitleSlideDark

Scaffold key: `title`

```javascript
function addTitleSlideDark(pres, title, subtitle) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 2.5, w: 8, h: 1.5,
    fontSize: 44, fontFace: FH, bold: true,
    color: C.t1, align: "left", valign: "top"
  });

  if (subtitle) {
    s.addText(subtitle, {
      x: 0.8, y: 4.2, w: 8, h: 0.6,
      fontSize: 24, fontFace: FB,
      color: C.t2, align: "left"
    });
  }

  // Lava accent bar (bottom)
  s.addShape(pres.ShapeType.rect, {
    x: 0, y: 5.4, w: 10, h: 0.05,
    fill: { color: C.lava }, line: { type: "none" }
  });

  return s;
}
```

### addContentBasic

Scaffold key: `content_basic`

```javascript
function addContentBasic(pres, sectionLabel, title, bodyText) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  if (sectionLabel) {
    s.addText(sectionLabel.toUpperCase(), {
      x: 0.8, y: 0.35, w: 3, h: 0.3,
      fontSize: 10, fontFace: FB, bold: true,
      color: C.lava, charSpacing: 3
    });
  }

  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true, color: C.t1
  });

  s.addText(bodyText, {
    x: 0.8, y: 1.3, w: 8, h: 3.5,
    fontSize: 14, fontFace: FB, color: C.t2, valign: "top"
  });

  return s;
}
```

### addCardGrid3Col

Scaffold key: `content_3col_cards`

```javascript
function addCardGrid3Col(pres, title, cards) {
  // cards = [{ title, body, color }, ...]
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true, color: C.t1
  });

  const cardW = 2.8, cardH = 3.2, cardY = 1.5;
  const cardX = [0.8, 3.8, 6.8];

  cards.slice(0, 3).forEach((card, i) => {
    // White card background
    s.addShape(pres.ShapeType.rect, {
      x: cardX[i], y: cardY, w: cardW, h: cardH,
      fill: { color: "FFFFFF" }, line: { type: "none" },
      rectRadius: 0.1, shadow: shd()
    });

    // Colored accent bar at top
    s.addShape(pres.ShapeType.rect, {
      x: cardX[i], y: cardY, w: cardW, h: 0.05,
      fill: { color: card.color || C.lava }, line: { type: "none" }
    });

    // Card title (dark text on white)
    s.addText(card.title, {
      x: cardX[i] + 0.2, y: cardY + 0.3, w: cardW - 0.4, h: 0.4,
      fontSize: 16, fontFace: FH, bold: true, color: C.bg1
    });

    // Card body (gray text on white)
    s.addText(card.body, {
      x: cardX[i] + 0.2, y: cardY + 0.8, w: cardW - 0.4, h: 2.2,
      fontSize: 11, fontFace: FB, color: C.t3, valign: "top"
    });
  });

  return s;
}
```

### addBigNumber

Scaffold key: `big_number`

```javascript
function addBigNumber(pres, number, label, context) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  if (label) {
    s.addText(label, {
      x: 1, y: 1, w: 8, h: 0.4,
      fontSize: 18, fontFace: FB, color: C.t2, align: "center"
    });
  }

  // Auto-size: see Section 5 for rules
  const len = number.length;
  const numSize = len <= 5 ? 80 : len <= 8 ? 64 : 48;

  s.addText(number, {
    x: 1, y: 1.5, w: 8, h: 2,
    fontSize: numSize, fontFace: FH, bold: true,
    color: C.lava, align: "center", valign: "middle"
  });

  if (context) {
    s.addText(context, {
      x: 1, y: 3.8, w: 8, h: 0.8,
      fontSize: Math.max(16, Math.floor(numSize / 4)),
      fontFace: FB, color: C.t3, align: "center"
    });
  }

  return s;
}
```

### addSectionBreak

Scaffold key: `section_break`

```javascript
function addSectionBreak(pres, title, subtitle) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addShape(pres.ShapeType.rect, {
    x: 0, y: 2.5, w: 10, h: 0.05,
    fill: { color: C.lava }, line: { type: "none" }
  });

  s.addText(title, {
    x: 1, y: 2.8, w: 8, h: 1,
    fontSize: 36, fontFace: FH, bold: true,
    color: C.t1, align: "center"
  });

  if (subtitle) {
    s.addText(subtitle, {
      x: 1, y: 3.9, w: 8, h: 0.5,
      fontSize: 18, fontFace: FB, color: C.t2, align: "center"
    });
  }

  return s;
}
```

### addComparison

Scaffold key: `content_2col`

```javascript
function addComparison(pres, title, leftCol, rightCol) {
  // leftCol/rightCol = { label, items: [strings], color }
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true, color: C.t1
  });

  const colW = 4, colH = 3.5, colY = 1.5;
  const leftX = 0.8, rightX = 5.2;

  // Left column
  s.addShape(pres.ShapeType.rect, {
    x: leftX, y: colY, w: colW, h: colH,
    fill: { color: C.bgCard },
    line: { width: 1, color: leftCol.color || C.blue }
  });
  s.addText(leftCol.label, {
    x: leftX + 0.2, y: colY + 0.2, w: colW - 0.4, h: 0.4,
    fontSize: 18, fontFace: FH, bold: true,
    color: leftCol.color || C.blue
  });
  s.addText(leftCol.items.map(item => `\u2022 ${item}`).join("\n"), {
    x: leftX + 0.2, y: colY + 0.8, w: colW - 0.4, h: 2.5,
    fontSize: 12, fontFace: FB, color: C.t2, valign: "top"
  });

  // Right column
  s.addShape(pres.ShapeType.rect, {
    x: rightX, y: colY, w: colW, h: colH,
    fill: { color: C.bgCard },
    line: { width: 1, color: rightCol.color || C.green }
  });
  s.addText(rightCol.label, {
    x: rightX + 0.2, y: colY + 0.2, w: colW - 0.4, h: 0.4,
    fontSize: 18, fontFace: FH, bold: true,
    color: rightCol.color || C.green
  });
  s.addText(rightCol.items.map(item => `\u2022 ${item}`).join("\n"), {
    x: rightX + 0.2, y: colY + 0.8, w: colW - 0.4, h: 2.5,
    fontSize: 12, fontFace: FB, color: C.t2, valign: "top"
  });

  return s;
}
```

### addQuote

Scaffold key: `power_statement_2`

```javascript
function addQuote(pres, quote, attribution) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText("\u201C", {
    x: 1.5, y: 1.8, w: 1, h: 1,
    fontSize: 72, fontFace: FH, color: C.maroon, align: "left"
  });

  s.addText(quote, {
    x: 1.5, y: 2.2, w: 7, h: 2,
    fontSize: 24, fontFace: FB, italic: true,
    color: C.t1, align: "center", valign: "middle"
  });

  if (attribution) {
    s.addText(`\u2014 ${attribution}`, {
      x: 1.5, y: 4.5, w: 7, h: 0.4,
      fontSize: 14, fontFace: FB, color: C.t3, align: "right"
    });
  }

  return s;
}
```

### addContent2Col

Scaffold key: `content_2col` (text-only variant without card borders)

```javascript
function addContent2Col(pres, title, leftText, rightText) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true, color: C.t1
  });

  const colW = 4, colY = 1.5;

  s.addText(leftText, {
    x: 0.8, y: colY, w: colW, h: 3.5,
    fontSize: 14, fontFace: FB, color: C.t2, valign: "top"
  });

  s.addText(rightText, {
    x: 5.2, y: colY, w: colW, h: 3.5,
    fontSize: 14, fontFace: FB, color: C.t2, valign: "top"
  });

  return s;
}
```

### addContent3Col

Scaffold key: `content_3col`

```javascript
function addContent3Col(pres, title, col1, col2, col3) {
  // col1/2/3 = { header, items: [strings] }
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true, color: C.t1
  });

  const colW = 2.8, colY = 1.5;
  const colX = [0.8, 3.8, 6.8];
  const colors = [C.blue, C.green, C.yellow];
  const cols = [col1, col2, col3];

  cols.forEach((col, i) => {
    s.addText(col.header.toUpperCase(), {
      x: colX[i], y: colY, w: colW, h: 0.3,
      fontSize: 10, fontFace: FB, bold: true,
      color: colors[i], charSpacing: 2
    });

    s.addText(col.items.map(item => `\u2022 ${item}`).join("\n"), {
      x: colX[i], y: colY + 0.5, w: colW, h: 3,
      fontSize: 12, fontFace: FB, color: C.t2, valign: "top"
    });
  });

  return s;
}
```

### addClosing

Scaffold key: `closing`

```javascript
function addClosing(pres, title, subtitle, cta) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 1, y: 2, w: 8, h: 1,
    fontSize: 44, fontFace: FH, bold: true,
    color: C.t1, align: "center"
  });

  if (subtitle) {
    s.addText(subtitle, {
      x: 1, y: 3.2, w: 8, h: 0.6,
      fontSize: 24, fontFace: FB, color: C.t2, align: "center"
    });
  }

  if (cta) {
    s.addText(cta, {
      x: 1, y: 4.2, w: 8, h: 0.5,
      fontSize: 18, fontFace: FB, bold: true,
      color: C.lava, align: "center"
    });
  }

  return s;
}
```

---

## 5. Stat Hero Sizing

The scaffold auto-sizes stat heroes. No caller tuning needed.

| Stat Length | Font Size | Context Size | Example |
|---|---|---|---|
| <= 5 chars | 80pt | 20pt | "< 15s", "72%", "$31K" |
| <= 8 chars | 64pt | 16pt | "10-20x", "$400K/yr" |
| > 8 chars | 48pt | 16pt (floor) | "1.2 million" |

Context text = `stat_font_size / 4` (floor 16pt). Source text = 9pt. All centered.

---

## 6. Visual Element Placement Decision Tree

When a slide includes a visual element (icon, illustration, real image, shape-based diagram), use this tree to pick the right layout.

**For WHEN to use each type of visual (real image vs shape-based vs icons vs text-only), consult deck-philosophy.md Section 9.** This section handles placement, not selection.

### Decision Tree

1. **Is the visual supplementary to the text, or IS IT the point?**
   - Supplementary: `content_card_right` (text dominant, visual secondary)
   - The visual IS the point: `content_card_large` (visual dominant, text minimal)

2. **Has the previous slide used `content_card_right`?**
   - Yes: use `content_card_left` for visual variety (rhythm)

3. **Is the visual a full-width diagram (architecture, flow, complex screenshot)?**
   - Custom shape-based architecture: `blank` + custom build. Run architecture eval rubric.
   - Real image (documentation diagram, product screenshot): `blank` + custom image placement. Title above, image centered, caption below.

4. **Is this a before/after with one real image and one shape-based side?**
   - Use `content_2col`. Real image in one column (framed if on dark bg), shape-based or text in the other.

5. **Never place an image on `content_basic` or `power_statement`.** These have no reserved image zone. This applies to ALL visual types.

### Image Role -> Layout Mapping

| Image Role | Layout | Detail |
|---|---|---|
| Image IS the slide (diagram, screenshot) | `content_card_large` or `blank` + custom | Use `content_card_large` when card frame fits. Use `blank` for full-width hero. |
| Image supports text explanation | `content_card_right` or `content_card_left` | Alternate sides across slides for rhythm. |
| Two images compared | `blank` + side-by-side | Each in white frame on dark slides. |
| Image as evidence (small) | Any text layout + small inset | `x:6.5, y:3.5, w:3.0, h:2.0` — supporting, not hero. |

### Image Sourcing

- **Real images**: Delegate to strategy/brief phase for sourcing. If strategy has `image: path`, use it. If not, build shape-based and add speaker note: "Enhancement: replace with [description]"
- **Architecture diagrams**: Delegate to diagram/arch-diagram skills, embed output as image
- **Template icons/illustrations**: Reference scaffold-reference.md for the icon library

### Real Image Code Pattern

```javascript
// Full-width hero image on blank slide
const s = pres.addSlide();
s.background = { color: C.bg1 };

s.addText(title, {
  x: 0.8, y: 0.5, w: 8, h: 0.5,
  fontSize: 28, fontFace: FH, bold: true, color: C.t1
});

// White frame on dark bg (skip on light bg)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.4, y: 1.4, w: 9.2, h: 3.7,
  fill: { color: "FFFFFF" }, rectRadius: 0.1, shadow: shd()
});

s.addImage({
  path: './images/diagram.png',
  x: 0.5, y: 1.5, w: 9.0, h: 3.5,
  sizing: { type: 'contain', w: 9.0, h: 3.5 }
});

// Caption
s.addText("Source: Databricks documentation", {
  x: 0.5, y: 5.1, w: 9.0, h: 0.25,
  fontSize: 9, fontFace: FB, color: C.t3, italic: true, align: "center"
});
```

### Image Sizing Presets (10" x 5.625" slide)

| Use Case | Position & Size | Notes |
|---|---|---|
| Full-width hero diagram | `x:0.5, y:1.5, w:9.0, h:3.5` | Title above, caption below. |
| Image-right with text | `x:5.0, y:1.2, w:4.5, h:3.8` | Text in left 4.5". |
| Image-left with text | `x:0.5, y:1.2, w:4.5, h:3.8` | Text in right 4.5". |
| Side-by-side comparison | `x:0.3, y:1.5, w:4.4, h:3.2` + `x:5.3, y:1.5, w:4.4, h:3.2` | Two images compared. |
| Small supporting inset | `x:6.5, y:3.5, w:3.0, h:2.0` | Not the hero element. |

---

## 7. Anti-Patterns

Every row here caused a real visual failure. Do not ignore.

| Wrong Approach | Why It Fails | Correct Approach |
|---|---|---|
| Image on `content_basic` | No reserved image zone — text and image overlap | Use `content_card_right`, `content_card_left`, or `content_card_large` |
| Hand-drawn 3 cards on `blank` | Ignores designer-built card layout with proper proportions | Use `content_3col_cards` via `addCardGrid3Col()` |
| Hand-drawn 2 columns on `blank` | Ignores template divider and column proportions | Use `content_2col` via `addComparison()` |
| `content_basic` for everything | Wastes layout variety, creates visual monotony | Match content shape to the right layout |
| Same layout on consecutive slides | Feels like a wall of text, kills rhythm | Alternate between layout families |
| `power_statement` for body text | Statement layouts are for 1-2 lines max, not paragraphs | Use `content_basic` for multi-paragraph text |
| White-bg image on dark slide without frame | Invisible edges, floating rectangle appearance | Add white rounded-rectangle frame behind image |
| Real image on REFRAME/FEEL slide | Wrong visual register — polished image signals "pitch" when the moment needs "insight" | Use sparse shapes or text-only. Reserve real images for SOLVE/PROVE/EQUIP. |
| Dense documentation diagram for exec audience | Exceeds audience chunk budget — they can't absorb 15 components | Build simplified 4-5 box shape version. Real diagram in speaker notes. |
| Shape-based architecture when official diagram exists | Reinventing what already has authority | Download the official diagram, frame it, let it carry the credibility. |
| Raw logo URL on dark slide | Dark logos vanish on dark backgrounds | Use `{"id": "databricks"}` — scaffold resolves white variant automatically |
| Manual `bg_strip_opacity` tuning | Guessing opacity is fragile | Let scaffold auto-compute strip contrast via WCAG luminance |

---

## 8. Logo Strip Intelligence

### Logo Variant Registry

Pass `{"id": "databricks"}` instead of a raw URL. The scaffold resolves the correct contrast variant for the slide background.

```javascript
// Preferred: scaffold picks the right variant
addLogoStrip(pres, [
  { id: "databricks" },
  { id: "spark" },
  { id: "python" }
], "Technology Ecosystem");

// Fallback: raw URL for logos not in registry
addLogoStrip(pres, [
  { id: "databricks" },
  { url: "https://example.com/partner-logo.png", width: 1.8, height: 0.6 }
], "Partners");
```

**How it works:**
1. Scaffold checks slide background luminance (from theme)
2. Luminance < 0.2 (dark slide): uses `dark_bg` variant (white/light logos)
3. Luminance > 0.6 (light slide): uses `light_bg` variant (dark logos)
4. In between: uses `dark_bg` (safer default)
5. ID not in registry: raises clear error with suggestion to use raw URL

**Registry includes:** databricks, spark, delta_lake, mlflow, unity_catalog, python, hadoop, docker, aws, azure, gcp, kubernetes, tableau, power_bi, snowflake, kafka, airflow, dbt, terraform, github.

Per-logo sizing is automatic from registry defaults. Override with explicit `width`/`height` if needed.

### Adaptive Background Strip

The scaffold auto-computes the strip fill color using WCAG luminance:
- Dark backgrounds: strip blends toward white to hit minimum 1.5:1 contrast ratio
- Light backgrounds: strip blends toward dark
- Mid-range: picks the direction with more contrast
- `bg_strip_opacity` parameter exists as optional override (0.0-1.0) but should rarely be needed

### Logos NOT in Registry

When a logo is not in the registry and the caller must supply a raw URL:
1. Identify the logo's dominant colors from general knowledge
2. If dark-dominant on a dark slide: source a white/light variant URL if one exists publicly
3. If no light variant exists: the adaptive strip provides some contrast, but note the limitation in speaker notes
4. Set explicit `width`/`height` for visual weight normalization (wordmarks wider, icons square)

---

## 9. CTA Enforcement

Strategy YAML must have an explicit `cta` block:

```yaml
closing:
  cta_primary: "Scope a 2-week POV with your referral data"
  cta_contact: "Samuel Selvan, SA — samuel.selvan@databricks.com"
  cta_timeline: "Workshop available as early as next Thursday"
```

**Enforcement rules:**
- Agent refuses to render the closing slide without `cta_primary`
- Agent flags generic CTAs and requests a rewrite:
  - "Schedule a demo" -- too vague
  - "Contact us" -- no specific action
  - "Learn more" -- no commitment
- A good CTA names the specific next step, the deliverable, and ideally a timeline
- `cta_contact` and `cta_timeline` are optional but recommended
