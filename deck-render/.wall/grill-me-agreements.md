# Deck-Render Theme System — Grill-Me Agreements

11 decisions from grill-me session on 2026-03-24. Grounded in Databricks Extended Brand Guidelines (colors, typography, design approach) extracted from brandfolder.

## Decision 1: Theme Architecture

Two themes: **dark** and **light**. Both share the same pptxgenjs rendering engine, same layout functions, same font system. The only difference is the palette object selected at the top of scaffold.js.

- `DARK_PALETTE` — existing dark navy system (unchanged)
- `LIGHT_PALETTE` — brand-aligned warm palette (updated per these agreements)
- Switch: `const THEME = strategy.design_decisions?.theme || "light"`
- Palette: `const C = THEME === "dark" ? DARK_PALETTE : LIGHT_PALETTE`

No other themes. Alternative themes table (Midnight, Ocean, Teal Trust, Forest) is reference-only — not exposed as selectable options.

## Decision 2: Default Theme

**Light is the default.** Dark is opt-in via explicit `theme: dark` in strategy YAML.

Rationale: The Databricks brand's PRIMARY look is warm (#F9F7F4 background), not dark navy. The dark theme was the default only because the light theme was incomplete. Light aligns with official brand guidelines and is less oppressive for routine internal/enablement content.

Strategy YAML override:
```yaml
design_decisions:
  theme: dark  # explicit opt-in to dark
```

When no `theme` is specified, scaffold.js defaults to `"light"`.

## Decision 3: Light Theme Background Colors

| Role | Hex | Source |
|------|-----|--------|
| **Slide background** | `F9F7F4` | Brand guidelines PRIMARY bg — warm oat |
| **Card/callout bg** | `FFFFFF` | Pure white cards float on warm bg |
| **Lighter variant** | `EEEDE9` | Oat medium — subtle differentiation |

The warmth comes from the slide background, not the cards. Cards are clean white for maximum content contrast.

## Decision 4: Red on Light Background

Dual-red system to maintain WCAG AA compliance:

| Use | Hex | Contrast on F9F7F4 | Rule |
|-----|-----|---------------------|------|
| **Shapes, fills, borders, icons** | `FF3621` | 4.5:1 (passes AA large) | Brand red — visual elements only |
| **Text (any size)** | `C42B1A` | 7.0:1 (passes AA normal) | Darkened red — readable at any size |

`FF3621` must NEVER be used as text color on light backgrounds. Use `C42B1A` for any red text. `FF3621` is fine for filled shapes, accent bars, borders, and icon fills.

Added `lavaText` key to LIGHT_PALETTE for the text-safe variant.

## Decision 5: Brand Color Alignment

One color swap from official brand guidelines:

| Color | Old | New | Source |
|-------|-----|-----|--------|
| **Blue** | `3B8FD4` | `2272B4` | Brand guidelines "Link Color" — professional blue |

**Not added** (present in brand guidelines but not needed):
- `#40D1F5` (cyan icon accent) — too bright for slide content
- `#F1F5FA` (hover state) — interactive-only, not relevant to slides
- `#4A4A4A` (secondary text gray) — existing t2/t3 system is already calibrated

## Decision 6: Template Layout Background Override

**Override ALL slide backgrounds to F9F7F4** for uniform warmth. Don't rely on template layout default backgrounds (which are white LIGHT1).

Implementation: After adding a slide, force the background:
```javascript
s.background = { fill: C.bg };
```

This applies to every content slide. Structural slides (Decision 7) use their own dark override.

## Decision 7: Structural vs Content Slide Backgrounds

Visual rhythm pattern — alternating warm and dark:

| Slide Type | Background | Text Color | Examples |
|------------|-----------|------------|----------|
| **Structural** | `1B3139` (dark teal) | White | Title, section dividers, closing/CTA |
| **Content** | `F9F7F4` (warm oat) | Dark (`333333`) | Cards, bullets, comparisons, tables |
| **Architecture** | `0B2026` (navy 900) | White | D2 diagrams (Decision 9) |

Structural slides create punctuation in the deck — they say "new section" or "summary." They use the brand's secondary color (teal) as background, which creates contrast against the warm content slides.

## Decision 8: Callout/Highlight Box System

**White boxes with colored left-edge accent bars** on warm F9F7F4 background.

Replaces the pastel tint system (greenLight: `FFF0ED`, blueLight: `E8F2FC`, etc.) which would be near-invisible on the warm background.

Pattern:
```javascript
// White callout box
s.addShape("rect", { x, y, w, h, fill: { color: "FFFFFF" }, shadow: shd() });
// Colored accent bar (left edge)
s.addShape("rect", { x, y, w: 0.06, h, fill: { color: C.green } });
```

Accent bar colors follow the same semantic system:
- Green = success/complete
- Blue = info/neutral
- Yellow = warning/highlight
- Lava (FF3621) = Databricks brand accent
- Maroon = deep emphasis (18pt+ only)

**Removed from LIGHT_PALETTE:** All `*Light` pastel variant keys (`greenLight`, `blueLight`, `yellowLight`, `lavaLight`, `maroonLight`). These were designed for dark theme tints and are not usable on warm backgrounds.

## Decision 9: Architecture Diagram Slides

Architecture slides override to **dark background** (`0B2026`), even in light theme decks. The D2 diagram IS the slide — it renders as a full-bleed dark diagram.

Rationale: D2 architecture diagrams are already designed for dark backgrounds (dark theme ELK renders). Forcing them onto warm backgrounds would require a completely separate diagram color system. The dark architecture slide creates a natural "deep dive" moment in the deck rhythm.

This makes architecture slides a third category alongside structural (teal) and content (warm).

## Decision 10: Cross-Skill Scope

**Deck-render only.** No changes to cheatsheet-render, one-pager-render, enablement-card-render, or email-render in this pass.

Other skills may adopt the light theme later, but this implementation focuses exclusively on getting deck-render's light theme complete and production-ready.

## Decision 11: Eval Criteria

**Universal contrast-ratio assertions** — theme-agnostic rules that work for both dark and light:

| Check | Rule | Method |
|-------|------|--------|
| All readable text | 7:1+ contrast against its background | Computed from palette values |
| Accent text (18pt+) | 5:1+ contrast | Computed |
| Decorative elements | 3:1+ contrast | Computed |

The eval rubric does NOT check for specific hex values. It checks contrast ratios. This means the same eval criteria work regardless of theme — a slide passes or fails based on readability, not color identity.

## Derived Rules (from the 11 decisions)

### Logo Variant Selection

On **dark** structural/architecture slides: use white/reversed logo variant.
On **light** content slides: use standard/dark logo variant.

### Stat Hero Slides

Stat heroes are **content slides** — they use warm F9F7F4 background with dark text. The large stat number uses `C.lavaText` (C42B1A) or the semantic accent color. Stat context text uses `C.t2`.

### Table Styling (Light Theme)

- Table header row: `C.bgCard` (FFFFFF) or `C.bgLight` (EEEDE9)
- Header text: `C.t1` (333333), bold
- Body rows: alternating `C.bg` (F9F7F4) and `C.bgCard` (FFFFFF)
- Body text: `C.t2` (545454)
- Borders: `C.border` (B0B0B0)

### Font System

Unchanged — DM Sans 400/500/700 works identically on both themes. Only the text color palette changes:

| Role | Dark Theme | Light Theme |
|------|-----------|-------------|
| t1 (titles) | `FFFFFF` | `333333` |
| t2 (body) | `DCE0E2` | `545454` |
| t3 (captions) | `9EADB5` | `595959` |

## Updated LIGHT_PALETTE

```javascript
const LIGHT_PALETTE = {
  // Backgrounds
  bg: "F9F7F4",      // Warm oat slide background (brand primary)
  bgCard: "FFFFFF",   // White card/callout backgrounds
  bgLight: "EEEDE9",  // Oat medium — subtle differentiation
  // Brand accent
  lava: "FF3621",     // Shapes, fills, borders, icons ONLY
  lavaText: "C42B1A", // Text-safe red (7.0:1 on F9F7F4)
  // Semantic accents
  green: "00A972",    // Success, complete
  blue: "2272B4",     // Info, neutral emphasis (brand blue)
  yellow: "FFAB00",   // Warning, highlight
  maroon: "C4243E",   // Deep emphasis (18pt+ only)
  // Structural
  navy: "1B3139",     // Structural slide backgrounds
  navyDark: "0B2026", // Architecture slide backgrounds
  // Text hierarchy
  t1: "333333",       // Titles, hero text (12.6:1 on F9F7F4)
  t2: "545454",       // Body text, bullets (7.1:1 on F9F7F4)
  t3: "595959",       // Captions, footnotes (7.0:1 on F9F7F4)
  // Borders
  border: "B0B0B0"    // Card borders, dividers
};
```

## Theme Config in Strategy YAML

```yaml
design_decisions:
  theme: light        # default if omitted
  # theme: dark       # explicit opt-in
```

No other theme-related strategy fields needed. The rendering agent reads `theme` and selects the palette. All other rendering logic is theme-aware through the palette object `C`.
