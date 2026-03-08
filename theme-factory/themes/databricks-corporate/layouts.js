/**
 * Databricks Corporate Theme - Layout Functions
 * For use with pptxgenjs
 */

const fs = require('fs');
const path = require('path');

// Load theme configuration
const THEME_DIR = __dirname;
const colors = JSON.parse(fs.readFileSync(path.join(THEME_DIR, 'colors.json'), 'utf8'));
const typography = JSON.parse(fs.readFileSync(path.join(THEME_DIR, 'typography.json'), 'utf8'));

// Color palette
const C = {
  ...colors.primary,
  ...colors.backgrounds,
  ...colors.accents,
  ...colors.text,
  border: colors.border
};

// Typography
const FH = typography.fonts.header;
const FB = typography.fonts.body;
const T = typography.sizes;
const S = typography.spacing;

// Shadow helper
function shd() {
  return { type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.25 };
}

// ============================================================================
// LAYOUT FUNCTIONS
// ============================================================================

function addTitleSlideDark(pres, title, subtitle) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 2.5, w: 8, h: 1.5,
    fontSize: T.title, fontFace: FH, bold: true, color: C.t1, align: "left", valign: "top"
  });

  if (subtitle) {
    s.addText(subtitle, {
      x: 0.8, y: 4.2, w: 8, h: 0.6,
      fontSize: T.subtitle, fontFace: FB, color: C.t2, align: "left"
    });
  }

  s.addShape(pres.ShapeType.rect, {
    x: 0, y: 5.4, w: 10, h: 0.05,
    fill: { color: C.lava }, line: { type: "none" }
  });

  return s;
}

function addSectionBreak(pres, title) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addShape(pres.ShapeType.rect, {
    x: 0, y: 2.5, w: 10, h: 0.05,
    fill: { color: C.lava }, line: { type: "none" }
  });

  s.addText(title, {
    x: 1, y: 2.8, w: 8, h: 1,
    fontSize: 36, fontFace: FH, bold: true, color: C.t1, align: "center"
  });

  return s;
}

function addContentBasic(pres, sectionLabel, title, body) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  if (sectionLabel) {
    s.addText(sectionLabel.toUpperCase(), {
      x: 0.8, y: 0.4, w: 4, h: 0.35,
      fontSize: T.sectionLabel, fontFace: FH, bold: true, color: C.lava, charSpacing: S.charSpacing
    });
  }

  s.addText(title, {
    x: 0.8, y: 0.85, w: 8.4, h: 0.6,
    fontSize: T.heading, fontFace: FH, bold: true, color: C.t1
  });

  s.addText(body, {
    x: 0.8, y: 1.6, w: 8.4, h: 4.2,
    fontSize: T.body, fontFace: FB, color: C.t2, valign: "top", paraSpaceAfter: S.paraSpaceAfter
  });

  return s;
}

function addContent2Col(pres, sectionLabel, title, leftContent, rightContent) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  if (sectionLabel) {
    s.addText(sectionLabel.toUpperCase(), {
      x: 0.8, y: 0.4, w: 4, h: 0.35,
      fontSize: T.sectionLabel, fontFace: FH, bold: true, color: C.lava, charSpacing: S.charSpacing
    });
  }

  s.addText(title, {
    x: 0.8, y: 0.85, w: 8.4, h: 0.6,
    fontSize: T.heading, fontFace: FH, bold: true, color: C.t1
  });

  // Left column
  s.addText(leftContent, {
    x: 0.8, y: 1.6, w: 4.1, h: 4.2,
    fontSize: T.body, fontFace: FB, color: C.t2, valign: "top", paraSpaceAfter: S.paraSpaceAfter
  });

  // Right column
  s.addText(rightContent, {
    x: 5.1, y: 1.6, w: 4.1, h: 4.2,
    fontSize: T.body, fontFace: FB, color: C.t2, valign: "top", paraSpaceAfter: S.paraSpaceAfter
  });

  return s;
}

function addCardGrid3Col(pres, title, cards) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 0.5, w: 8.4, h: 0.6,
    fontSize: T.heading, fontFace: FH, bold: true, color: C.t1
  });

  const cardW = 2.8, cardH = 3.2, cardY = 1.4, cardX = [0.8, 3.8, 6.8];

  cards.slice(0, 3).forEach((card, i) => {
    // White card with shadow
    s.addShape(pres.ShapeType.rect, {
      x: cardX[i], y: cardY, w: cardW, h: cardH,
      fill: { color: "FFFFFF" },
      line: { type: "none" },
      rectRadius: 0.1,
      shadow: shd()
    });

    // Colored accent bar
    s.addShape(pres.ShapeType.rect, {
      x: cardX[i], y: cardY, w: cardW, h: 0.05,
      fill: { color: card.color || C.lava },
      line: { type: "none" }
    });

    // Card title (dark text on white)
    s.addText(card.title, {
      x: cardX[i] + 0.2, y: cardY + 0.3, w: cardW - 0.4, h: 0.4,
      fontSize: 16, fontFace: FH, bold: true, color: C.bg1
    });

    // Card body
    s.addText(card.body, {
      x: cardX[i] + 0.2, y: cardY + 0.8, w: cardW - 0.4, h: 2.2,
      fontSize: T.caption, fontFace: FB, color: C.t3, valign: "top"
    });
  });

  return s;
}

function addComparison(pres, title, leftTitle, leftContent, rightTitle, rightContent) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 0.5, w: 8.4, h: 0.6,
    fontSize: T.heading, fontFace: FH, bold: true, color: C.t1
  });

  // Left box
  s.addShape(pres.ShapeType.rect, {
    x: 0.8, y: 1.4, w: 4.1, h: 4.4,
    fill: { color: C.bgCard },
    line: { color: C.blue, width: 3 },
    rectRadius: 0.12
  });
  s.addText(leftTitle, {
    x: 0.8, y: 1.5, w: 4.1, h: 0.5,
    fontSize: 18, fontFace: FH, bold: true, color: C.blue, align: "center"
  });
  s.addText(leftContent, {
    x: 1, y: 2.15, w: 3.7, h: 3.4,
    fontSize: T.body, fontFace: FB, color: C.t2, valign: "top", paraSpaceAfter: S.paraSpaceAfter
  });

  // Right box
  s.addShape(pres.ShapeType.rect, {
    x: 5.1, y: 1.4, w: 4.1, h: 4.4,
    fill: { color: C.bgCard },
    line: { color: C.green, width: 3 },
    rectRadius: 0.12
  });
  s.addText(rightTitle, {
    x: 5.1, y: 1.5, w: 4.1, h: 0.5,
    fontSize: 18, fontFace: FH, bold: true, color: C.green, align: "center"
  });
  s.addText(rightContent, {
    x: 5.3, y: 2.15, w: 3.7, h: 3.4,
    fontSize: T.body, fontFace: FB, color: C.t2, valign: "top", paraSpaceAfter: S.paraSpaceAfter
  });

  return s;
}

function addSideBySideComparison(pres, sectionLabel, title, leftContent, rightContent, whatThisMeans) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  // Section label
  s.addText(sectionLabel.toUpperCase(), {
    x: 0.8, y: 0.4, w: 4, h: 0.35,
    fontSize: T.sectionLabel, fontFace: FH, bold: true, color: C.lava, charSpacing: S.charSpacing
  });

  // Title
  s.addText(title, {
    x: 0.8, y: 0.85, w: 8.4, h: 0.6,
    fontSize: T.heading, fontFace: FH, bold: true, color: C.t1
  });

  // Column headers
  s.addText("Vanilla PostgreSQL", {
    x: 0.8, y: 1.5, w: 3.9, h: 0.3,
    fontSize: 14, fontFace: FH, bold: true, color: C.blue, align: "center"
  });

  s.addText("Lakebase", {
    x: 5.3, y: 1.5, w: 3.9, h: 0.3,
    fontSize: 14, fontFace: FH, bold: true, color: C.green, align: "center"
  });

  // Vertical divider line (centered, starting below headers)
  s.addShape(pres.ShapeType.line, {
    x: 5.1, y: 1.85, w: 0, h: 2.5,
    line: { color: C.border, width: 2 }
  });

  // Left column (Vanilla PG)
  s.addText(leftContent, {
    x: 0.8, y: 1.9, w: 3.9, h: 2.4,
    fontSize: T.body, fontFace: FB, color: C.t2, valign: "top", paraSpaceAfter: S.paraSpaceAfter
  });

  // Right column (Lakebase)
  s.addText(rightContent, {
    x: 5.3, y: 1.9, w: 3.9, h: 2.4,
    fontSize: T.body, fontFace: FB, color: C.t2, valign: "top", paraSpaceAfter: S.paraSpaceAfter
  });

  // "WHAT THIS MEANS" callout box
  s.addShape(pres.ShapeType.rect, {
    x: 0.8, y: 4.6, w: 8.4, h: 0.75,
    fill: { color: C.bgCard },
    line: { color: C.lava, width: 2 },
    rectRadius: 0.08
  });

  s.addText(whatThisMeans, {
    x: 1.0, y: 4.7, w: 8.0, h: 0.55,
    fontSize: T.caption, fontFace: FB, color: C.t1, valign: "middle", paraSpaceAfter: S.paraSpaceAfter
  });

  return s;
}

function addWarningCards(pres, title, cards) {
  const s = pres.addSlide();
  s.background = { color: C.bg1 };

  s.addText(title, {
    x: 0.8, y: 0.5, w: 8.4, h: 0.6,
    fontSize: T.heading, fontFace: FH, bold: true, color: C.t1
  });

  const cardW = 4.0, cardH = 2.3, cardY = 1.4;
  const cardX = [0.8, 5.2]; // Two columns
  const colors = { red: C.maroon, yellow: C.yellow, blue: C.blue, gray: "666666" };

  cards.slice(0, 4).forEach((card, i) => {
    const x = cardX[i % 2];
    const y = cardY + Math.floor(i / 2) * 2.5;

    // Card background
    s.addShape(pres.ShapeType.rect, {
      x, y, w: cardW, h: cardH,
      fill: { color: C.bgCard },
      line: { color: colors[card.severity] || C.border, width: 3 },
      rectRadius: 0.12,
      shadow: shd()
    });

    // Card header
    s.addText(card.header, {
      x: x + 0.2, y: y + 0.2, w: cardW - 0.4, h: 0.4,
      fontSize: 16, fontFace: FH, bold: true, color: colors[card.severity] || C.t1
    });

    // Card body
    s.addText(card.body, {
      x: x + 0.2, y: y + 0.7, w: cardW - 0.4, h: 1.4,
      fontSize: T.caption, fontFace: FB, color: C.t2, valign: "top"
    });
  });

  return s;
}

// Export all layouts
module.exports = {
  colors: C,
  fonts: { header: FH, body: FB },
  typography: T,
  spacing: S,
  helpers: { shd },
  layouts: {
    addTitleSlideDark,
    addSectionBreak,
    addContentBasic,
    addContent2Col,
    addCardGrid3Col,
    addComparison,
    addSideBySideComparison,
    addWarningCards
  }
};
