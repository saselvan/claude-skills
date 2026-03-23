# Cheat Sheet Design Rules (Addendum to Shared design-rules.md)

> These rules extend the shared design-rules.md with cheat-sheet-specific visual grammar.

---

## Grid System

### Card Dimensions
```
Desktop (3-column):
  Container max-width: 1200px
  Card width: calc((100% - 2 × gap) / 3)
  Gap: 0.8rem (12.8px)
  Card padding: 1rem (16px)
  Card border-radius: 8px

Desktop (4-column):
  Container max-width: 1400px
  Card width: calc((100% - 3 × gap) / 4)
  Gap: 0.6rem (9.6px)
  Card padding: 0.8rem (12.8px)

Tablet (2-column):
  Breakpoint: ≤1024px
  Gap: 0.8rem

Mobile (1-column):
  Breakpoint: ≤768px
  Gap: 0.6rem
```

### Card Internal Structure
```
┌──────────────────────────────┐
│ [Icon] CARD TITLE            │  ← Title zone: 1 line max
├──────────────────────────────┤
│                              │
│  Body content                │  ← Content zone: 5-9 items
│  (items, table, triggers)    │
│                              │
└──────────────────────────────┘
   No footer zone. No sub-navigation.
```

---

## Typography Scale

All sizes assume a base of `13px` body text (cheat sheets are denser than standard documents).

| Element | Size | Weight | Font |
|---------|------|--------|------|
| Sheet title | 1.1rem (14.3px) | Bold | System sans-serif (Segoe UI, -apple-system, sans-serif) |
| Card title | 0.95rem (12.35px) | Bold | Same |
| Item label (left column in tables) | 0.85rem (11.05px) | Semi-bold (600) | Same |
| Item detail (right column / body) | 0.8rem (10.4px) | Normal (400) | Same |
| Metadata (footer, version) | 0.7rem (9.1px) | Normal | Same |

**Rules:**
- Exactly 3 levels of hierarchy visible: card title → item label → item detail
- Never use ALL CAPS for body text (sentence case is faster to read — Gawande)
- Card titles may use ALL CAPS sparingly if the sheet has ≤9 cards and titles are ≤3 words
- Line height: 1.4 for body, 1.2 for titles

---

## Color System

### Semantic Palette (Maximum 4 colors + neutrals)

Colors are semantic, not decorative. Each color has exactly one meaning.

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Primary accent** | Brand-defined (see shared design-rules.md) | `#FF3621` (Databricks Lava) | Card title text, active borders, hero stat emphasis |
| **Alert / Critical** | Red | `#FF3621` (doubles as brand accent) | Danger states, critical warnings, "stop" signals |
| **Caution / Attention** | Amber/Yellow | `#F7B070` | Warnings, conditional items, "check first" signals |
| **Safe / Positive** | Green | `#2DC98E` (Databricks Green) | Confirmed states, "go" signals, success indicators |
| **Neutral background** | Dark slate | `#1A1A2E` | Sheet background (dark mode default) |
| **Card background** | Slightly lighter | `#1D1D31` | Card containers |
| **Body text** | Light gray | `#E8E8E8` | All body content |
| **Muted text** | Medium gray | `#A8A8A8` | Metadata, secondary labels |

**Dark mode is the default** for cheat sheets (Gery's research + color cognition studies show white-on-dark yields superior performance under high cognitive load).

**Light mode alternative** (if required by org brand):
| Role | Hex |
|------|-----|
| Background | `#FFFFFF` |
| Card background | `#F8F9FA` |
| Body text | `#1A1A2E` |
| Muted text | `#555E66` |

### Color Rules
1. Never use more than 4 semantic colors (excluding neutrals)
2. Every color must be explainable in one sentence ("Red means stop/danger")
3. Never use color as the ONLY differentiator (accessibility — always pair with shape, icon, or label)
4. Card borders: 1px solid `#4A4A68` (subtle, not prominent)
5. Accent color used for: card titles, table headers, hero numbers. Never for body text.

---

## Density Targets

| Metric | Target | Hard Limit |
|--------|--------|------------|
| Words per card | 40-80 | 120 max |
| Items per card | 5-7 | 9 max |
| Total cards | 9 | 12 max |
| Total sheet words | 400-700 | 1000 max (750 for AE/Sales/BDR) |
| Scroll depth | 0 (single viewport) | 1 scroll max on tablet |
| Characters per card title | 15-30 | 40 max |
| Characters per table cell | 20-50 | 80 max |

---

## Icon Usage

### When to Use Icons
- **Yes:** Category markers at the start of card titles (one icon per card, consistent style)
- **Yes:** Semantic indicators replacing text (✅ = pass, ❌ = fail, ⚠️ = warning)
- **No:** Decorative icons that don't aid scanning
- **No:** Multiple icons per card (creates "icon wall" anti-pattern)
- **No:** Mixing icon styles (all outline OR all solid, never both)

### Icon Placement
- Card title: Icon precedes text, same line: `[Icon] CARD TITLE`
- Inline semantic: Icon replaces label: `✅ Complete` not `Status: Complete ✅`
- Maximum 1 icon per card title, unlimited semantic icons in body (if consistent)

### Recommended Icon Set (Unicode — no image dependencies)
| Icon | Meaning |
|------|---------|
| 🔊 | Trigger/audio cue ("When you hear...") |
| 📖 | Glossary/decoder |
| 👤 | Persona |
| ❓ | Discovery questions |
| 📊 | Metrics/data |
| 🔀 | Decision/branching |
| ✅ | Checklist |
| ⚡ | Quick reference/commands |
| 🎯 | Key takeaway/target |

---

## Card Borders and Containers

```css
/* Standard card */
.card {
  background: #1D1D31;
  border: 1px solid #4A4A68;
  border-radius: 8px;
  padding: 1rem;
}

/* Card title bar */
.card-title {
  color: var(--accent-color);
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #4A4A68;
}

/* Table inside card */
.card table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

.card td {
  padding: 0.25rem 0.4rem;
  border-bottom: 1px solid #1D1D31;
  vertical-align: top;
}
```

---

## Red Alert Banner

For compliance, liability, or "stop before you start" constraints that must be visible before any card content.

**Placement:** Full width, between sheet title and card grid. Not inside a card.

**Format:** One line: `⚠️ [CONSTRAINT] — [consequence] • [safe path]`

```css
.alert-banner {
  background: rgba(255, 54, 33, 0.12);
  border: 1px solid rgba(255, 54, 33, 0.5);
  border-radius: 4px;
  padding: 0.2rem 0.5rem;
  font-size: 0.7rem;
  font-weight: 600;
  color: #FF3621;
  text-align: center;
  margin: 0.3rem 0;
}
.alert-banner .safe { color: #F7B070; font-weight: 400; font-style: italic; }
```

**Rules:**
1. Maximum 1 banner per sheet (if you need more, you have a compliance problem, not a cheat sheet problem)
2. Must contain all three elements: constraint + consequence + safe alternative
3. Uses brand red (#FF3621) for constraint, amber (#F7B070) for safe path
4. Triggers a Liability Audit check during self-evaluation (Step 5 in SKILL.md)

---

## Subtitle Hero Area

An optional one-line subtitle under the sheet title for anchoring the core mental model or metaphor.

```css
h1 span {
  color: #ccc;
  font-weight: 400;
  font-size: 0.75rem;
  display: block;
  margin-top: 0.1rem;
}
h1 span em { color: #F7B070; font-style: normal; font-weight: 600; }
```

**Rules:**
1. Maximum 1 subtitle per sheet
2. Under 15 words
3. Anchoring metaphor or mental model in amber accent (`#F7B070`)
4. Format: `[Metaphor] for [Domain] — [Product positioning]`
5. Example: `The Nurse's Station for Your Data Lake — Postgres, built into Databricks`

---

## Sheet Footer

Every cheat sheet includes a footer with:

```
[Sheet Title] — v[X.Y] — [Owner] — Updated: [YYYY-MM-DD] — Next review: [trigger]
```

Example:
```
Healthcare Provider Cheat Sheet — v2.1 — Samuel Garcia — Updated: 2025-01-08 — Next review: After Q1 product release
```

Footer sits below the card grid, full width, centered, in muted text (0.7rem).
