# PptxGenJS Patterns

## Setup

```javascript
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";  // 10" × 5.625"
pres.author = "Author";
pres.title = "Title";
```

## Icon Pipeline (react-icons → sharp → base64 PNG)

This is the only reliable way to get crisp icons in pptxgenjs slides.

```javascript
// Import specific icons
const { FaCheckCircle, FaChartBar, FaDatabase } = require("react-icons/fa");

// Render function
async function iconPng(IC, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IC, { color: "#" + color, size: String(size) })
  );
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

// Pre-render ALL icons before building slides
const I = {};
I.check = await iconPng(FaCheckCircle, "2DD4A8");
I.chart = await iconPng(FaChartBar, "4A90E2");
I.db    = await iconPng(FaDatabase, "FF6B4A");

// Use in slide (display size set by w/h in inches, NOT the render size)
s.addImage({ data: I.check, x: 0.85, y: 1.0, w: 0.22, h: 0.22 });
```

**Icon sets:** `react-icons/fa` (Font Awesome), `react-icons/md` (Material), `react-icons/hi` (Heroicons), `react-icons/bi` (Bootstrap)

## Color & Shadow Helpers

```javascript
// Palette object — single source of truth
const C = {
  bg1: "0D0F1A", bgCard: "1E2235", bgLight: "141729",
  blue: "4A90E2", blueLight: "1A2E4A",
  teal: "2DD4A8", tealLight: "132E28",
  accent: "FF6B4A", accentLight: "2E1A16",
  gold: "F5A623", goldLight: "2E2216",
  t1: "FFFFFF", t2: "E8ECF4", t3: "A0AAC0", t4: "6B7694",
  border: "2D3352"
};

// Font constants
const FH = "Trebuchet MS";  // headers
const FB = "Calibri";       // body

// Shadow factory — MUST be a function (pptxgenjs mutates shadow objects in place)
const shd = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.25 });
```

## Text

```javascript
// Title
s.addText("Slide Title", {
  x: 0.8, y: 0.7, w: 8, h: 0.5,
  fontSize: 28, fontFace: FH, bold: true, color: C.t1, margin: 0
});

// Section label (spaced uppercase — use on EVERY content slide)
s.addText("SECTION NAME", {
  x: 0.8, y: 0.35, w: 3, h: 0.3,
  fontSize: 10, fontFace: FB, bold: true, color: C.accent, charSpacing: 3, margin: 0
});

// Body text
s.addText("Description text here", {
  x: 0.8, y: 1.3, w: 4, h: 0.6,
  fontSize: 11, fontFace: FB, color: C.t3, margin: 0
});

// Rich text (mixed formatting)
s.addText([
  { text: "Bold part ", options: { bold: true, color: C.t2 } },
  { text: "normal part", options: { color: C.t3 } }
], { x: 1, y: 3, w: 8, h: 0.4, fontSize: 11, fontFace: FB, margin: 0 });

// Multi-line (MUST use breakLine: true)
s.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }
], { x: 0.5, y: 0.5, w: 8, h: 2, fontSize: 11, fontFace: FB, color: C.t3 });
```

**Critical:** Set `margin: 0` whenever aligning text with shapes/icons at the same x-position.

## Shapes

```javascript
// Card background with shadow
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 2.85, h: 1.3,
  fill: { color: C.bgCard }, shadow: shd()
});

// Left accent bar (layered on top of card)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 0.06, h: 1.3,
  fill: { color: C.blue }
});

// Line (for arrows/dividers)
s.addShape(pres.shapes.LINE, {
  x: 2.6, y: 3.0, w: 0.5, h: 0,
  line: { color: C.accent, width: 2.5 }
});

// Oval (icon circle background)
s.addShape(pres.shapes.OVAL, {
  x: 0.85, y: 1.75, w: 0.5, h: 0.5,
  fill: { color: C.blue }
});
// Icon centered inside (offset ~0.11" from oval edge)
s.addImage({ data: I.check, x: 0.96, y: 1.86, w: 0.28, h: 0.28 });

// Transparency
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "000000", transparency: 40 }
});
```

## Tables

```javascript
const rows = [
  // Header row
  [
    { text: "Dimension", options: { fill: { color: "1B1F3B" }, color: C.t1, bold: true, fontSize: 11, fontFace: FB } },
    { text: "Value", options: { fill: { color: "1B1F3B" }, color: C.t1, bold: true, fontSize: 11, fontFace: FB, align: "center" } }
  ],
  // Data rows
  [
    { text: "Row 1", options: { fill: { color: C.bgCard }, fontSize: 11, fontFace: FB, color: C.t3 } },
    { text: "Data", options: { fill: { color: C.bgCard }, fontSize: 12, fontFace: FB, bold: true, color: C.teal, align: "center" } }
  ]
];
s.addTable(rows, {
  x: 0.5, y: 2.8, w: 9,
  colW: [3, 6],
  border: { pt: 0.5, color: C.border },
  rowH: [0.4, 0.4]
});
```

## Charts

```javascript
s.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1", "Q2", "Q3"], values: [45, 55, 62]
}], {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",
  chartColors: [C.blue, C.teal, C.accent],
  chartArea: { fill: { color: C.bgCard }, roundedCorners: true },
  catAxisLabelColor: C.t3, valAxisLabelColor: C.t3,
  valGridLine: { color: C.border, size: 0.5 },
  catGridLine: { style: "none" },
  showValue: true, dataLabelColor: C.t1, showLegend: false
});
```

## Backgrounds & Notes

```javascript
s.background = { color: C.bg1 };                          // Solid
s.background = { data: "image/png;base64,..." };           // Base64 image
s.addNotes("Talk Track (60s): Key message.\n\nPoint 1.\nPoint 2.");
```

## File Output

```javascript
await pres.writeFile({ fileName: "output.pptx" });
```

## Pitfalls (File Corruption & Visual Bugs)

| Mistake | Fix |
|---------|-----|
| `color: "#FF0000"` | Remove `#` → `color: "FF0000"` |
| 8-char hex in shadow color `"00000020"` | Use `color: "000000", opacity: 0.12` |
| Reusing shadow object across calls | Use factory function: `const shd = () => ({...})` |
| Unicode bullets `"• item"` | Use `bullet: true` property |
| Missing `breakLine: true` | Text runs together without it |
| Negative shadow offset | Corrupts file. Must be ≥ 0 |
| `ROUNDED_RECTANGLE` with accent overlay bar | Overlay doesn't cover corners. Use plain `RECTANGLE` |
| `lineSpacing` with bullets | Causes huge gaps. Use `paraSpaceAfter` instead |
| `letterSpacing` (silently ignored) | Use `charSpacing` instead |

## Complete Deck Script Structure

```javascript
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaIcon1, FaIcon2 } = require("react-icons/fa");

async function iconPng(IC, color, sz = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(IC, { color: "#" + color, size: String(sz) }));
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";

  const C = { /* palette */ };
  const FH = "Trebuchet MS", FB = "Calibri";
  const shd = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.25 });

  // Pre-render icons
  const I = {};
  I.icon1 = await iconPng(FaIcon1, C.teal);
  I.icon2 = await iconPng(FaIcon2, C.blue);

  // === SLIDE 1: Cover ===
  { const s = pres.addSlide(); s.background = { color: C.bg1 };
    // ... elements
  }

  // === SLIDE 2: Content ===
  { const s = pres.addSlide(); s.background = { color: C.bg1 };
    // ... elements
  }

  // ... more slides

  await pres.writeFile({ fileName: "output.pptx" });
  console.log("Done: output.pptx");
}

main().catch(e => { console.error(e); process.exit(1); });
```

Each slide in its own block scope `{ const s = ... }` keeps things clean and avoids variable conflicts.

## Databricks Template Layouts

Pre-built layout functions matching Databricks Corporate Template. Use these for fast, brand-compliant deck generation.

### Setup for Databricks Layouts

```javascript
// Databricks brand palette (from design-rules.md)
const C = {
  bg1: "0B2026", bgCard: "1B3139", bgLight: "303F47",
  lava: "FF3621", lavaLight: "2D1510",
  green: "00A972", greenLight: "0D2920",
  blue: "2272B4", blueLight: "0D1F2D",
  yellow: "FFAB00", yellowLight: "2D2510",
  maroon: "98102A", maroonLight: "1D0D10",
  navy: "1B5162",
  t1: "FFFFFF", t2: "DCE0E2", t3: "5A6F77", t4: "5A6F77",
  border: "303F47"
};

const FH = "DM Sans"; // Databricks font (fallback: "Trebuchet MS")
const FB = "DM Sans"; // Body font (fallback: "Calibri")
const shd = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.25 });
```

### Layout 1: Title Slide (Dark)

```javascript
function addTitleSlideDark(pres, title, subtitle) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Title (large, left-aligned)
  s.addText(title, {
    x: 0.8, y: 2.5, w: 8, h: 1.5,
    fontSize: 44, fontFace: FH, bold: true,
    color: C.t1, align: "left", valign: "top"
  });

  // Subtitle (below title)
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
    fill: { color: C.lava },
    line: { type: "none" }
  });

  return s;
}
```

### Layout 2: Content Basic (1-column)

```javascript
function addContentBasic(pres, sectionLabel, title, bodyText) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Section label (spaced uppercase, small)
  if (sectionLabel) {
    s.addText(sectionLabel.toUpperCase(), {
      x: 0.8, y: 0.35, w: 3, h: 0.3,
      fontSize: 10, fontFace: FB, bold: true,
      color: C.lava, charSpacing: 3
    });
  }

  // Title
  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true,
    color: C.t1
  });

  // Body text
  s.addText(bodyText, {
    x: 0.8, y: 1.3, w: 8, h: 3.5,
    fontSize: 14, fontFace: FB,
    color: C.t2, valign: "top"
  });

  return s;
}
```

### Layout 3: Card Grid (3-column)

```javascript
function addCardGrid3Col(pres, title, cards) {
  // cards = [{ title, body, color }, ...]
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Title
  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true,
    color: C.t1
  });

  // 3 white cards
  const cardW = 2.8;
  const cardH = 3.2;
  const cardY = 1.5;
  const cardX = [0.8, 3.8, 6.8];

  cards.slice(0, 3).forEach((card, i) => {
    // White card background
    s.addShape(pres.ShapeType.rect, {
      x: cardX[i], y: cardY, w: cardW, h: cardH,
      fill: { color: "FFFFFF" },
      line: { type: "none" },
      rectRadius: 0.1,
      shadow: shd()
    });

    // Colored accent bar at top
    s.addShape(pres.ShapeType.rect, {
      x: cardX[i], y: cardY, w: cardW, h: 0.05,
      fill: { color: card.color || C.lava },
      line: { type: "none" }
    });

    // Card title (dark text on white)
    s.addText(card.title, {
      x: cardX[i] + 0.2, y: cardY + 0.3, w: cardW - 0.4, h: 0.4,
      fontSize: 16, fontFace: FH, bold: true,
      color: C.bg1
    });

    // Card body (gray text on white)
    s.addText(card.body, {
      x: cardX[i] + 0.2, y: cardY + 0.8, w: cardW - 0.4, h: 2.2,
      fontSize: 11, fontFace: FB,
      color: C.t3, valign: "top"
    });
  });

  return s;
}
```

### Layout 4: Big Number (Hero Stat)

```javascript
function addBigNumber(pres, number, label, context) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Label above number (small)
  if (label) {
    s.addText(label, {
      x: 1, y: 1, w: 8, h: 0.4,
      fontSize: 18, fontFace: FB,
      color: C.t2, align: "center"
    });
  }

  // Hero number (large, lava red)
  s.addText(number, {
    x: 1, y: 1.5, w: 8, h: 2,
    fontSize: 96, fontFace: FH, bold: true,
    color: C.lava, align: "center", valign: "middle"
  });

  // Context below number
  if (context) {
    s.addText(context, {
      x: 1, y: 3.8, w: 8, h: 0.8,
      fontSize: 14, fontFace: FB,
      color: C.t3, align: "center"
    });
  }

  return s;
}
```

### Layout 5: Section Break

```javascript
function addSectionBreak(pres, title, subtitle) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Colored accent bar (centered)
  s.addShape(pres.ShapeType.rect, {
    x: 0, y: 2.5, w: 10, h: 0.05,
    fill: { color: C.lava },
    line: { type: "none" }
  });

  // Section title (large, centered)
  s.addText(title, {
    x: 1, y: 2.8, w: 8, h: 1,
    fontSize: 36, fontFace: FH, bold: true,
    color: C.t1, align: "center"
  });

  // Optional subtitle
  if (subtitle) {
    s.addText(subtitle, {
      x: 1, y: 3.9, w: 8, h: 0.5,
      fontSize: 18, fontFace: FB,
      color: C.t2, align: "center"
    });
  }

  return s;
}
```

### Layout 6: Two-Column Comparison

```javascript
function addComparison(pres, title, leftCol, rightCol) {
  // leftCol/rightCol = { label, items: [strings], color }
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Title
  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true,
    color: C.t1
  });

  const colW = 4;
  const colH = 3.5;
  const colY = 1.5;
  const leftX = 0.8;
  const rightX = 5.2;

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

  s.addText(leftCol.items.map(item => `• ${item}`).join("\n"), {
    x: leftX + 0.2, y: colY + 0.8, w: colW - 0.4, h: 2.5,
    fontSize: 12, fontFace: FB,
    color: C.t2, valign: "top"
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

  s.addText(rightCol.items.map(item => `• ${item}`).join("\n"), {
    x: rightX + 0.2, y: colY + 0.8, w: colW - 0.4, h: 2.5,
    fontSize: 12, fontFace: FB,
    color: C.t2, valign: "top"
  });

  return s;
}
```

### Layout 7: Quote/Statement

```javascript
function addQuote(pres, quote, attribution) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Opening quote mark (large, maroon)
  s.addText(""", {
    x: 1.5, y: 1.8, w: 1, h: 1,
    fontSize: 72, fontFace: FH,
    color: C.maroon, align: "left"
  });

  // Quote text (centered, large)
  s.addText(quote, {
    x: 1.5, y: 2.2, w: 7, h: 2,
    fontSize: 24, fontFace: FB, italic: true,
    color: C.t1, align: "center", valign: "middle"
  });

  // Attribution
  if (attribution) {
    s.addText(`— ${attribution}`, {
      x: 1.5, y: 4.5, w: 7, h: 0.4,
      fontSize: 14, fontFace: FB,
      color: C.t3, align: "right"
    });
  }

  return s;
}
```

### Layout 8: Content 2-Column

```javascript
function addContent2Col(pres, title, leftText, rightText) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Title
  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true,
    color: C.t1
  });

  const colW = 4;
  const colY = 1.5;
  const leftX = 0.8;
  const rightX = 5.2;

  // Left column
  s.addText(leftText, {
    x: leftX, y: colY, w: colW, h: 3.5,
    fontSize: 14, fontFace: FB,
    color: C.t2, valign: "top"
  });

  // Right column
  s.addText(rightText, {
    x: rightX, y: colY, w: colW, h: 3.5,
    fontSize: 14, fontFace: FB,
    color: C.t2, valign: "top"
  });

  return s;
}
```

### Layout 9: Closing Slide

```javascript
function addClosing(pres, title, subtitle, cta) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Title (large, centered)
  s.addText(title, {
    x: 1, y: 2, w: 8, h: 1,
    fontSize: 44, fontFace: FH, bold: true,
    color: C.t1, align: "center"
  });

  // Subtitle
  if (subtitle) {
    s.addText(subtitle, {
      x: 1, y: 3.2, w: 8, h: 0.6,
      fontSize: 24, fontFace: FB,
      color: C.t2, align: "center"
    });
  }

  // CTA (lava red accent)
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

### Layout 10: Content 3-Column

```javascript
function addContent3Col(pres, title, col1, col2, col3) {
  // col1/2/3 = { header, items: [strings] }
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Title
  s.addText(title, {
    x: 0.8, y: 0.7, w: 8, h: 0.5,
    fontSize: 28, fontFace: FH, bold: true,
    color: C.t1
  });

  const colW = 2.8;
  const colY = 1.5;
  const colX = [0.8, 3.8, 6.8];
  const cols = [col1, col2, col3];

  cols.forEach((col, i) => {
    // Column header (small, uppercase, accent color)
    s.addText(col.header.toUpperCase(), {
      x: colX[i], y: colY, w: colW, h: 0.3,
      fontSize: 10, fontFace: FB, bold: true,
      color: [C.blue, C.green, C.yellow][i], // Rotate colors
      charSpacing: 2
    });

    // Column items (bullets)
    s.addText(col.items.map(item => `• ${item}`).join("\n"), {
      x: colX[i], y: colY + 0.5, w: colW, h: 3,
      fontSize: 12, fontFace: FB,
      color: C.t2, valign: "top"
    });
  });

  return s;
}
```

### Usage Example

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

// Use Databricks layouts
addTitleSlideDark(pres, "Lakebase for Healthcare", "PostgreSQL-compatible data platform");
addSectionBreak(pres, "Why Lakebase?");
addCardGrid3Col(pres, "Key Capabilities", [
  { title: "PostgreSQL Compatible", body: "100% wire protocol", color: "2272B4" },
  { title: "Autoscaling", body: "1 to 1000 connections", color: "00A972" },
  { title: "Lakehouse Native", body: "Query Delta tables", color: "FFAB00" }
]);
addBigNumber(pres, "3-5x", "Faster than Aurora", "Ensemble Health benchmark");
addClosing(pres, "Thank You", "Let's build together", "Schedule a demo");

pres.writeFile({ fileName: "lakebase-deck.pptx" });
```
