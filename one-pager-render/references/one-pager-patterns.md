# One-Pager Patterns: HTML → PDF Tool Mastery

This is your reference for writing HTML that renders correctly as a PDF. Consult this DURING rendering. It tells you what works, what breaks, and how to build it right the first time.

**The fundamental approach:** HTML `<table>` for layout. CSS for styling. This combination renders identically in wkhtmltopdf, Puppeteer, WeasyPrint, browsers, and email clients. No workarounds needed.

---

## 1. The Rendering Pipeline

```
HTML (single file, all styles in <style> block)
  → wkhtmltopdf
    → PDF
      → pdftoppm (for visual evaluation)
        → PNG
```

### The Command

```bash
wkhtmltopdf \
  --enable-local-file-access \
  --page-size Letter \
  --margin-top 0 --margin-bottom 0 \
  --margin-left 0 --margin-right 0 \
  --dpi 150 \
  --print-media-type \
  --no-outline \
  --encoding UTF-8 \
  input.html output.pdf 2>/dev/null
```

| Flag | Why |
|------|-----|
| `--enable-local-file-access` | **Required.** Without it, local images/fonts silently vanish. |
| `--margin-* 0` | We control margins in HTML, not wkhtmltopdf. Both = double margins. |
| `--dpi 150` | Screen/email quality. Use `300` for `distribution_method: print`. |
| `--print-media-type` | Forces `@media print` rules — required for background colors. |
| `--encoding UTF-8` | Prevents em dashes, smart quotes, and bullets from garbling. |

### PNG for Evaluation

```bash
pdftoppm -png -r 200 -singlefile output.pdf rendered/one-pager
```

---

## 2. Layout: HTML Tables

Tables handle structure. CSS handles appearance. Keep them separate.

### The Core Pattern

Every one-pager is a single outer table with rows for each zone:

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr><td colspan="2"><!-- HERO ZONE --></td></tr>
  <tr>
    <td width="55%" valign="top"><!-- PRIMARY CONTENT --></td>
    <td width="45%" valign="top"><!-- SECONDARY CONTENT --></td>
  </tr>
  <tr><td colspan="2"><!-- CTA ZONE --></td></tr>
</table>
```

Rules:
- `cellpadding="0" cellspacing="0" border="0"` on every table — reset browser defaults
- `width` in percentages on `<td>` elements — controls column proportions
- `valign="top"` on every content cell — prevents vertical centering
- Use `colspan` for full-width rows (hero, CTA, section dividers)
- Nest tables for sub-layouts (metric card rows, multi-column proof points)

### Layout Patterns from Strategy

**z_pattern** (hero → two columns → CTA):
```html
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr><td colspan="2" style="padding: 0 0 18px 0;">
    <div class="hero-message"><!-- hero --></div>
    <div class="hero-sub"><!-- subtext --></div>
  </td></tr>
  <tr>
    <td width="55%" valign="top" style="padding-right: 14px;">
      <!-- Sections 1 & 2 -->
    </td>
    <td width="45%" valign="top" style="padding-left: 14px;">
      <!-- Section 3 + proof metrics -->
    </td>
  </tr>
  <tr><td colspan="2" style="padding-top: 14px;">
    <div class="cta"><!-- CTA content --></div>
  </td></tr>
</table>
```

**layer_cake** (sequential, single column):
```html
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr><td style="padding-bottom: 18px;"><!-- Hero --></td></tr>
  <tr><td style="padding-bottom: 14px;"><!-- Section 1 --></td></tr>
  <tr><td style="padding-bottom: 14px;"><!-- Section 2 --></td></tr>
  <tr><td style="padding-bottom: 14px;"><!-- Section 3 --></td></tr>
  <tr><td><!-- CTA --></td></tr>
</table>
```

**vertical_flow** (primary + sidebar):
```html
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr><td colspan="2" style="padding-bottom: 18px;"><!-- Hero --></td></tr>
  <tr>
    <td width="63%" valign="top" style="padding-right: 14px;">
      <!-- Primary argument (sections 1, 2, 3) -->
    </td>
    <td width="37%" valign="top" style="padding-left: 14px;">
      <!-- Sidebar: metrics, proof, key stats -->
    </td>
  </tr>
  <tr><td colspan="2" style="padding-top: 14px;"><!-- CTA --></td></tr>
</table>
```

### Nested Tables for Sub-Layouts

**Metric cards row:**
```html
<table width="100%" cellpadding="0" cellspacing="8" border="0">
  <tr>
    <td width="33%" class="metric-card" align="center">
      <div class="metric-number">40%</div>
      <div class="metric-label">Reduction in ETL cycles</div>
    </td>
    <td width="33%" class="metric-card" align="center">
      <div class="metric-number">&lt;5ms</div>
      <div class="metric-label">Point-read latency</div>
    </td>
    <td width="33%" class="metric-card" align="center">
      <div class="metric-number">1</div>
      <div class="metric-label">Unified governance layer</div>
    </td>
  </tr>
</table>
```

**Two-column proof points:**
```html
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td width="48%" valign="top" class="card" style="padding: 10px;">
      <!-- Customer story 1 -->
    </td>
    <td width="4%"></td><!-- gutter -->
    <td width="48%" valign="top" class="card" style="padding: 10px;">
      <!-- Customer story 2 -->
    </td>
  </tr>
</table>
```

Use empty `<td>` cells for gutters when `cellspacing` doesn't give you enough control.

---

## 3. Page Containment

A one-pager is one page. Content overflow is a content problem, not a rendering problem.

```css
@page { size: letter; margin: 0; }

html, body {
  width: 8.5in;
  height: 11in;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.page {
  width: 7.5in;
  height: 10in;
  margin: 0.5in;
  overflow: hidden;
}
```

`overflow: hidden` is the hard stop. If content is clipped, cut words — don't add pages.

---

## 4. Typography

### Font Strategy

**System fonts first.** wkhtmltopdf reliably renders installed system fonts. Custom fonts via `@font-face` may silently fail.

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif;
}
```

If brand fonts are required (e.g., DM Sans), install them on the system:
```bash
cp DMSans-*.ttf /usr/share/fonts/truetype/
fc-cache -f -v
```

Base64 `@font-face` as last resort — use `truetype` format only, remove `local()` from `src`, always provide a system fallback.

### Type Scale

Use `pt` for print. It's the native PDF unit.

| Element | Size | Weight | Line-height |
|---------|------|--------|-------------|
| Hero message | 22–28pt | 700 | 1.2 |
| Section heading | 12–14pt | 600 | 1.3 |
| Body text | 10pt | 400 | 1.45 |
| Proof metric | 20pt | 700 | 1.1 |
| Caption / source | 8pt | 400 | 1.3 |
| Fine print | 7pt | 400 | 1.3 |

Minimum readable: 9pt for body, 7pt for legal. Gap between adjacent levels must be ≥4pt for visual distinction.

### Line Length

Optimal: 45–75 characters per line. At 10pt in a 7.5" content area, single column runs ~90 chars — too wide. Two columns at 55/45 split gives ~50 and ~40 chars, which is ideal.

---

## 5. Styling Inside Table Cells

Tables do layout. These CSS properties handle all visual design — and all work reliably inside `<td>` elements.

### What Works

```css
/* Background colors — REQUIRES print-color-adjust */
@media print {
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
}
td.dark-bg  { background-color: #1B3139; color: #FFFFFF; }
td.light-bg { background-color: #F5F5F5; }

/* Accent borders — the workhorse of visual hierarchy */
.section-head { border-left: 3px solid #FF3621; padding-left: 8px; }
.card         { border: 1px solid #E0E0E0; padding: 10px; }
.highlight    { border-top: 2px solid #00A972; }

/* Typography — full control */
.hero-message { font-size: 24pt; font-weight: 700; color: #1B3139; }
.body-text    { font-size: 10pt; color: #333333; line-height: 1.45; }
.accent       { color: #FF3621; font-weight: 600; }

/* Spacing */
td { padding: 0; } /* reset, then set per-cell */
.section { margin-bottom: 14px; }
```

### What Doesn't Work in wkhtmltopdf

| CSS Property | Problem | Use Instead |
|-------------|---------|-------------|
| `box-shadow` | Renders as solid block or vanishes | `border: 1px solid #E0E0E0` |
| `rgba()` | Inconsistent transparency | Pre-calculate solid hex |
| `opacity` | May render fully opaque or invisible | Use lighter hex color |
| `border-radius` | Partially supported, may render square | Accept or test |
| CSS `filter` | Not supported | Skip |
| `linear-gradient` | Needs `-webkit-` prefix, still unreliable | Use solid colors |

### Color Reference

Use 6-character hex only (#RRGGBB). WCAG AA contrast check:

```
#333333 on #FFFFFF → 12.6:1 ✅  (body text)
#1B3139 on #FFFFFF → 13.8:1 ✅  (headings)
#FFFFFF on #1B3139 → 13.2:1 ✅  (white on dark)
#FF3621 on #FFFFFF →  4.0:1 ⚠️  (red — decorative borders only; use #C42B1A for text at 7.0:1)
#545454 on #FFFFFF →  7.1:1 ✅  (secondary text)
#595959 on #FFFFFF →  7.0:1 ✅  (source/fine print text)
```

---

## 6. Images

### Reliable

```html
<!-- Base64 in <img> tag — most reliable -->
<img src="data:image/png;base64,iVBORw0KGgo..." width="120" height="40" alt="Logo">

<!-- Inline SVG — ideal for icons and diagrams -->
<svg width="20" height="20" viewBox="0 0 24 24">
  <path d="M12 2L2 7l10 5 10-5-10-5z" fill="#FF3621"/>
</svg>

<!-- Local file with absolute path (requires --enable-local-file-access) -->
<img src="file:///absolute/path/image.png" width="120" height="40">
```

Always specify `width` and `height` attributes. Without them, wkhtmltopdf may miscalculate size.

### Unreliable

- Base64 in CSS `background-image` — silently ignored in some versions
- External URLs — blocked by default
- Relative file paths — may not resolve
- `<img>` without dimensions — renders at 0×0 or full resolution

---

## 7. Common Pitfalls

| # | Symptom | Cause | Fix |
|---|---------|-------|-----|
| 1 | Background colors missing | Print mode strips them | `-webkit-print-color-adjust: exact` AND `--print-media-type` |
| 2 | Two pages instead of one | Content exceeds page height | `overflow: hidden` on `.page`. Cut content. |
| 3 | Custom fonts wrong | @font-face silently failed | Install on system. Provide fallback stack. |
| 4 | Images missing | External URL or base64 in CSS | Use `<img>` with base64 `src`. Pass `--enable-local-file-access`. |
| 5 | Blurry output | Low DPI | `--dpi 150` (screen) or `--dpi 300` (print) |
| 6 | Garbled characters | Missing encoding | `<meta charset="UTF-8">` AND `--encoding UTF-8` |
| 7 | Double margins | Margins in both @page and CSS | Set `@page { margin: 0 }`, control in CSS only |

---

## 8. The Complete HTML Skeleton

Copy and adapt. Table structure handles layout, CSS classes handle appearance.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    @page { size: letter; margin: 0; }
    @media print {
      * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
      width: 8.5in; height: 11in;
      margin: 0; padding: 0; overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                   'Helvetica Neue', Arial, sans-serif;
      font-size: 10pt; line-height: 1.45; color: #333333;
    }

    .page { width: 7.5in; height: 10in; margin: 0.5in; overflow: hidden; position: relative; }

    /* Typography */
    .hero-message { font-size: 24pt; font-weight: 700; color: #1B3139; line-height: 1.2; }
    .hero-sub     { font-size: 11pt; color: #545454; margin-top: 6px; }
    .section-head { font-size: 12pt; font-weight: 600; color: #1B3139;
                    border-left: 3px solid #FF3621; padding-left: 8px; margin-bottom: 6px; }
    .body-text    { font-size: 10pt; color: #333333; line-height: 1.45; }

    /* Metrics */
    .metric-card   { background: #E8E8E8; padding: 10px; text-align: center; }
    .metric-number { font-size: 20pt; font-weight: 700; color: #C42B1A; } /* Darkened for accessibility */
    .metric-label  { font-size: 8pt; color: #545454; margin-top: 3px; }

    /* CTA */
    .cta         { background: #1B3139; color: #FFFFFF; padding: 10px 12px; }
    .cta-action  { font-size: 11pt; font-weight: 600; }
    .cta-contact { font-size: 8pt; margin-top: 3px; color: #E0E0E0; }

    /* Utility */
    .accent { color: #FF3621; } /* For borders; use #C42B1A for text */
    .source { font-size: 7pt; color: #595959; font-style: italic; }
    .card   { border: 1px solid #B0B0B0; padding: 10px; }
  </style>
</head>
<body>
<div class="page">

  <!-- Logo -->
  <div style="position: absolute; top: 0; right: 0;">
    <!-- <img src="data:image/png;base64,..." width="100" height="30" alt="Logo"> -->
  </div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0">

    <!-- HERO -->
    <tr><td colspan="2" style="padding-bottom: 18px;">
      <div class="hero-message"><!-- Hero from strategy --></div>
      <div class="hero-sub"><!-- Context / why now --></div>
    </td></tr>

    <!-- CONTENT: two columns -->
    <tr>
      <td width="55%" valign="top" style="padding-right: 14px;">

        <div style="margin-bottom: 14px;">
          <div class="section-head"><!-- Section 1 --></div>
          <div class="body-text"><!-- Content --></div>
        </div>

        <div style="margin-bottom: 14px;">
          <div class="section-head"><!-- Section 2 --></div>
          <div class="body-text"><!-- Content --></div>
        </div>

      </td>
      <td width="45%" valign="top" style="padding-left: 14px;">

        <div style="margin-bottom: 14px;">
          <div class="section-head"><!-- Section 3 --></div>
          <div class="body-text"><!-- Content --></div>
        </div>

        <table width="100%" cellpadding="0" cellspacing="8" border="0">
          <tr>
            <td width="50%" class="metric-card">
              <div class="metric-number"><!-- Stat --></div>
              <div class="metric-label"><!-- Label --></div>
            </td>
            <td width="50%" class="metric-card">
              <div class="metric-number"><!-- Stat --></div>
              <div class="metric-label"><!-- Label --></div>
            </td>
          </tr>
        </table>

      </td>
    </tr>

    <!-- CTA -->
    <tr><td colspan="2" style="padding-top: 14px;">
      <div class="cta">
        <div class="cta-action"><!-- Primary CTA --></div>
        <div class="cta-contact"><!-- Contact / secondary --></div>
      </div>
    </td></tr>

  </table>

</div>
</body>
</html>
```

---

## 9. Pre-Flight Checklist

```
□ Single HTML file — no external CSS, JS, or images
□ <meta charset="UTF-8"> present
□ @page { size: letter; margin: 0; } set
□ -webkit-print-color-adjust: exact in @media print
□ overflow: hidden on body and .page
□ All layout via <table> with cellpadding="0" cellspacing="0" border="0"
□ All <td> cells have explicit width (%) and valign="top"
□ All images use <img> tags with base64 src and explicit width/height
□ All colors in #RRGGBB hex — no rgba(), no opacity
□ No box-shadow — border instead
□ System fonts with fallback stack
□ wkhtmltopdf flags: --enable-local-file-access --print-media-type --encoding UTF-8
□ Body text ≥ 9pt, fine print ≥ 7pt
```

---

## 10. Alternative Renderers

wkhtmltopdf is unmaintained (last release 2020) but fast and dependency-free. If you hit its limits:

| Tool | When |
|------|------|
| **wkhtmltopdf** | Default. Fast, simple, tables work perfectly. |
| **Puppeteer** | Need modern CSS (border-radius, shadows). Heavier. |
| **WeasyPrint** | Python environments. Good CSS Paged Media support. |

Puppeteer fallback:
```bash
node -e "
  const puppeteer = require('puppeteer');
  (async () => {
    const b = await puppeteer.launch({args: ['--no-sandbox']});
    const p = await b.newPage();
    await p.goto('file:///path/to/input.html', {waitUntil: 'networkidle0'});
    await p.pdf({ path: 'output.pdf', format: 'Letter', printBackground: true,
                  margin: {top: 0, right: 0, bottom: 0, left: 0} });
    await b.close();
  })();
"
```

Start with wkhtmltopdf. Only switch if tables + CSS can't deliver what you need.
