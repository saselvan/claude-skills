---
version: v5
name: Lakebase Graph Kit film v5 — design spec
description: >
  Dark film register for the v5 explainer. Four systems (Unity Catalog, Spark, Lakebase, the app) are
  solid tinted surfaces with fixed hues and fixed greyscale steps. One brilliant lime means only
  "what happens now". A coral line marks the Databricks boundary. Delta tables are vertical stripes;
  Lakebase Postgres tables are horizontal rows. IBM Plex Sans and Plex Mono, nothing under 36 px.
  One corner radius (6 px), one stroke scale (3 px unit). No glow, blur, gradient, shadow, 3D,
  transparency at rest, official logo, or camera move.
unit: the frame — 1920×1080 primary; 1080×1350 (4:5) recomposed, never cropped
principle: system hue is identity · lime is the present tense · every hex is solid · numbers and copy come from claims.md and STORYBOARD.md

colors:
  # ground and neutrals
  ground: "#0B0F13"            # cool near-black; never pure black
  code-bg: "#06080A"           # code panel fill
  ink: "#F1F4F7"               # primary text
  ink-2: "#C3CAD3"             # secondary text; ground, code-bg, uc-surface, uc-card, lakebase-surface, outside-surface only
  ink-3: "#969FA9"             # dim text; ground and code-bg only
  # systems: surface (fill), card (one step up, data cards only), line (3 px stroke, texture), dim (stroke when dimmed)
  uc-surface: "#00251F"
  uc-card: "#08372F"
  uc-line: "#269685"
  uc-dim: "#3E6960"
  lakebase-surface: "#182F4C"
  lakebase-card: "#274162"
  lakebase-line: "#669EE4"
  lakebase-dim: "#4C6585"
  spark-surface: "#50361B"
  spark-line: "#F2A657"
  spark-dim: "#785F46"
  app-surface: "#574067"
  app-line: "#E2BFFC"
  app-dim: "#6E5D7A"
  # outside Databricks (Beat 3 only) and refused marks
  outside-surface: "#26282C"
  outside-line: "#91979D"      # also the refused-edge colour, always dashed
  # walk tones (Lakebase hue, lightness carries order); used for hops and tree levels
  walk-1: "#9EC4F4"
  walk-2: "#669EE4"            # same hex as lakebase-line on purpose
  walk-beyond: "#607EA6"       # continuation marks and the cut, always dashed
  # boundary and the one highlight
  boundary: "#FF785F"          # Databricks boundary line and its label
  now: "#E2FF45"               # only "what happens now"
  now-ink: "#0B0F13"           # text on a now fill

typography:
  fontStack:
    sans: '"IBM Plex Sans", "Helvetica Neue", Helvetica, Arial, sans-serif'
    mono: '"IBM Plex Mono", Menlo, "Helvetica Neue", Helvetica, monospace'
  fontFiles: "~/Library/Fonts/IBMPlexSans-{Regular,Medium,SemiBold}.otf, ~/Library/Fonts/IBMPlexMono-{Regular,Medium,SemiBold}.otf; copy into the project, never fetch"
  label-floor: "h/36"          # 30 px at 1080 (16:9), 37.5 px at 1350 (4:5); check_text_size.py reads data-height
  caption-floor: "h/20"        # 54 px at 1080 (16:9), 67.5 px at 1350 (4:5)
  question:  { fontFamily: "IBM Plex Sans", px: 88,  weight: 600, lineHeight: 1.10, color: "ink" }
  headline:  { fontFamily: "IBM Plex Sans", px: 64,  weight: 600, lineHeight: 1.15, color: "ink" }
  end-line:  { fontFamily: "IBM Plex Sans", px: 72,  weight: 600, lineHeight: 1.15, color: "ink" }
  caption:   { fontFamily: "IBM Plex Sans", px: 56,  weight: 400, lineHeight: 1.10, color: "ink", maxLines: 2, maxChars: 42 }
  evidence:  { fontFamily: "IBM Plex Sans", px: 56,  weight: 400, lineHeight: 1.10, color: "ink-2", note: "test-mode caption under a number" }
  seed-label: { fontFamily: "IBM Plex Sans", px: 48,  weight: 600, lineHeight: 1.10, color: "ink" }
  label:     { fontFamily: "IBM Plex Sans", px: 40,  weight: 500, lineHeight: 1.15, color: "ink", maxWords: 4 }
  kicker:    { fontFamily: "IBM Plex Mono", px: 36,  weight: 400, lineHeight: 1.20, color: "ink-2" }
  code:      { fontFamily: "IBM Plex Mono", px: 36,  weight: 400, lineHeight: 1.61, color: "ink-2", advance-px: 21.6 }
  number:    { fontFamily: "IBM Plex Mono", px: 144, weight: 500, lineHeight: 1.00, color: "ink", tabular: true }
  counter:   { fontFamily: "IBM Plex Mono", px: 96,  weight: 600, lineHeight: 1.00, color: "ink" }

radii:
  corner: "6px"                # every rectangle: panels, cards, code panel, lit-line bar, patient mark
  node: "50%"                  # circles are a shape (clinician, term), not a second radius

strokes:
  unit: "3px"
  widths: ["3px", "6px", "9px"]  # no other width; no hairline
  structure: "3px"             # panel and card outlines, edges at rest; stripes and rows are 6px
  emphasis: "6px"              # the now edge, the seed ring, the boundary, strike-through
  heavy: "9px"                 # heaviest fold weight only
  dash: "12px 12px"            # walk-beyond, cut nodes, refused edges, synced entry
  edge-weight-bins: { floor-to-low: "3px", mid: "6px", high: "9px" }  # illustrative fold weights, Beats 4 and 6

spacing:
  margin: "64px"               # 4:5 uses 40px
  gutter: "40px"
  panel-pad: "40px"
  code-pad-x: "28px"
  code-line-pitch: "58px"      # 4:5 uses 52px
  tree-row-pitch: "80px"       # 4:5 uses 64px
  tree-indent: "64px"
  caption-band: { y: "928px", height: "128px" }

components:
  system-panel:
    fill: "{colors.<system>-surface}"
    stroke: "3px {colors.<system>-line}"
    rounded: "{radii.corner}"
    label: "{typography.label} {colors.ink}, set as a tab that breaks the top stroke, centred on the panel's main content; never in a corner"
  delta-card:
    size: "216×144"
    fill: "{colors.uc-card}"
    stroke: "3px {colors.uc-line}"
    texture: "4 vertical stripes, 6px wide, 30px pitch, 24px inset, {colors.uc-line}"
    label: "name below the card, {typography.label} {colors.ink}"
  postgres-card:
    size: "216×144"
    fill: "{colors.lakebase-card}"
    stroke: "3px {colors.lakebase-line}"
    texture: "4 horizontal rows, 6px tall, 30px pitch, 24px inset, {colors.lakebase-line}"
    label: "name below the card, {typography.label} {colors.ink}"
  synced-entry:
    size: "216×144"
    fill: "{colors.uc-surface}"
    stroke: "3px dashed {colors.uc-line}"
    texture: "one horizontal 6px bar pointing right toward Lakebase; no stripes, no rows"
    label: "{typography.label}, for example \"synced entry · FOREIGN\""
  code-panel:
    fill: "{colors.code-bg}"
    stroke: "3px {colors.lakebase-line}"
    rounded: "{radii.corner}"
    tag: "\"simplified\" once, {typography.kicker} {colors.ink-3}"
  code-line:
    rest: "{colors.ink-2} on {colors.code-bg}"
    lit: "{colors.now-ink} on a full-width {colors.now} bar, 52px tall, {radii.corner}"
    dim: "{colors.ink-3} on {colors.code-bg}"
  clinician-node:
    radius: "14px"
    seed: "22px, {colors.ink} fill, 6px {colors.walk-1} ring offset 6px"
    reached-hop-1: "{colors.walk-1} fill"
    reached-hop-2: "{colors.walk-2} fill"
    hollow: "3px {colors.walk-2} stroke, {colors.lakebase-surface} fill"
    cut: "3px dashed {colors.walk-beyond} stroke, no fill"
  patient-mark:
    shape: "24×24 square, {radii.corner}"
    fill: "{colors.ink-2}"
    rule: "patients are squares, clinicians are circles; a patient is never a node"
  edge:
    rest: "{colors.walk-1} or {colors.walk-2}, width from edge-weight-bins"
    now: "{colors.now}, its bin width + 3px"
    beyond: "3px dashed {colors.walk-beyond}"
    refused: "3px dashed {colors.outside-line}, then retracts"
  sync-channel:
    axis: "horizontal only"
    stroke: "3px {colors.uc-line}; dimmed {colors.uc-dim}"
  queue-mark:
    shape: "stack of 24×9 bars, {colors.outside-line}"
    rule: "bars, not squares, so a queue never reads as patients"
  boundary:
    stroke: "6px {colors.boundary}"
    rounded: "{radii.corner}"
    label: "\"Databricks\" in {typography.label} {colors.boundary}, on the top stroke as a tab"
  strike:
    stroke: "6px {colors.now} while it draws, then {colors.ink-3}"
  dim-state:
    rule: "surface fill becomes {colors.ground}; stroke becomes {colors.<system>-dim}; text stays at its token. No opacity at rest."

motion:
  exact: { ease: "none", rule: "edges and tree levels snap in at constant speed; every edge of one hop starts together" }
  layout: { ease: "power2.inOut", shape-s: 0.75, text-s: 1.4, rule: "a shape that carries text moves at 1.4 s" }
  handoff: { fill-hold-s: 0.6, crossfade-s: 0.5 }
  now-drain-s: 0.5
  never: ["blur", "glow", "scale-only emphasis", "camera zoom or pan", "transform on the composition root", "stroke-offset animation"]
---

# Lakebase Graph Kit film v5 — design spec

## Overview

The film is dark. Each system keeps one hue and one greyscale step in every frame. The only brilliant colour is
`now` (lime). It marks the one event that happens at this moment: a hop's edges, the SQL line that acts, a strike,
a refused edge. When the event ends, `now` drains in 0.5 s into the settled token. Two marks may be `now` at the
same time only when they are one event, for example a code line and the edges it draws.

The ground `#0B0F13` is a cool near-black. The highlight is lime, not gold, so the film does not fall into the
banned black-and-gold look.

## Colour

### Systems in greyscale

The four systems must stay distinct with colour removed. Each system has a fixed CIE L* step for its surface and for
its line. Adjacent systems differ by at least 6.9 L* units on the surface and 8 units on the line.

| System | Surface | L* | Line | L* | Dim stroke | L* |
|---|---|---|---|---|---|---|
| Unity Catalog | `#00251F` | 12.1 | `#269685` | 56.0 | `#3E6960` | 41.2 |
| Lakebase | `#182F4C` | 19.0 | `#669EE4` | 64.1 | `#4C6585` | 42.1 |
| Spark | `#50361B` | 25.0 | `#F2A657` | 74.1 | `#785F46` | 42.2 |
| App | `#574067` | 31.0 | `#E2BFFC` | 82.1 | `#6E5D7A` | 42.1 |
| Outside Databricks | `#26282C` | 16.1 | `#91979D` | 62.2 | — | — |

Surface pairs that share a frame: Unity Catalog and Lakebase ΔL* 6.9 (Beat 5), Unity Catalog and Spark ΔL* 12.9
(Beats 4–5), Lakebase and app ΔL* 12.0 (Beat 8). Surfaces sit 1.2–2.1:1 against the ground, so the 3 px line,
not the fill, carries each edge (all lines are ≥4.5:1 on their own surface and ≥5.3:1 on the ground).

Dimmed strokes all sit near L* 42 on purpose: a dimmed system loses its greyscale step and keeps only its hue and
position. Dim means "not acting now".

The boundary (`#FF785F`, L* 66.2) is close to the Lakebase line in greyscale (ΔL* 2.1). It stays distinct by
weight and position: it is the only 6 px structural line, and it is always outermost.

Other tokens in greyscale: `walk-1` 78.0, `walk-2` 64.1, `walk-beyond` 52.0, `now` 95.2, `ink` 96.0, `ink-2` 81.0,
`ink-3` 65.1, `ground` 4.2, `code-bg` 2.1, `uc-card` 20.0, `lakebase-card` 27.0.

`now` and `ink` have the same lightness (1.02:1). So `now` never appears as thin text or a thin line next to ink.
It always comes with a fill (the lit code-line bar) or with extra weight (+3 px on an edge). In greyscale the lit
line is the only dark-on-light bar, and the lit edge is the thickest, lightest stroke.

### Text contrast (WCAG ratio, computed from the hex values)

The room floor is 7:1 for all text. Every permitted pair passes it.

| Text on background | Ratio | Use |
|---|---|---|
| `ink` on `ground` | 17.42:1 | captions, headlines, labels |
| `ink-2` on `ground` | 11.64:1 | kicker, secondary labels |
| `ink-3` on `ground` | 7.17:1 | settled struck-path label |
| `ink` on `code-bg` | 18.17:1 | code line being read |
| `ink-2` on `code-bg` | 12.14:1 | code line at rest |
| `ink-3` on `code-bg` | 7.48:1 | dim code line (Beat 8 `HAVING`), "simplified" |
| `now-ink` on `now` | 17.06:1 | lit code line |
| `now` on `ground` | 17.06:1 | depth numeral during its change |
| `ink` on `uc-surface` | 14.81:1 | Unity Catalog labels |
| `ink-2` on `uc-surface` | 9.89:1 | Unity Catalog secondary labels |
| `ink` on `uc-card` | 11.91:1 | Delta card name (if inside the card) |
| `ink` on `lakebase-surface` | 12.27:1 | node names, Lakebase labels |
| `ink-2` on `lakebase-surface` | 8.20:1 | hop labels, "up to 25 per hop" |
| `ink` on `lakebase-card` | 9.42:1 | Postgres card name, "reader: views only" |
| `ink` on `spark-surface` | 10.09:1 | Spark labels |
| `ink` on `app-surface` | 8.15:1 | app labels, "SET ROLE reader" |
| `ink` on `outside-surface` | 13.38:1 | outside graph database label |
| `ink-2` on `outside-surface` | 8.94:1 | "Δt behind" |
| `boundary` on `ground` | 7.42:1 | "Databricks" label |

Forbidden text pairs (below 7:1): `ink-2` on `lakebase-card` 6.30:1, on `spark-surface` 6.74:1, on
`app-surface` 5.44:1. Use `ink` there. `ink-3` appears only on `ground` and `code-bg`. No system line colour is
used for text, except `boundary`.

### Mark contrast (floor 3:1)

| Mark on background | Ratio |
|---|---|
| `uc-line` on `uc-surface` / `uc-card` / `ground` | 4.50 / 3.62 / 5.30 |
| `lakebase-line` on `lakebase-surface` / `lakebase-card` / `ground` / `code-bg` | 4.89 / 3.75 / 6.94 / 7.24 |
| `spark-line` on `spark-surface` / `ground` | 5.50 / 9.49 |
| `app-line` on `app-surface` / `ground` | 5.61 / 11.99 |
| `outside-line` on `outside-surface` / `ground` / `lakebase-surface` | 5.00 / 6.52 / 4.59 |
| `walk-1` / `walk-2` / `walk-beyond` on `lakebase-surface` | 7.52 / 4.89 / 3.25 |
| `now` on `lakebase-surface` / `uc-surface` / `spark-surface` / `app-surface` / `ground` | 12.02 / 14.50 / 9.88 / 7.98 / 17.06 |
| `ink-2` patient mark on `spark-surface` | 6.74 |
| dim strokes on `ground` (UC / Lakebase / Spark / app) | 3.11 / 3.21 / 3.23 / 3.21 |
| `boundary` on `ground` / `uc-surface` | 7.42 / 6.31 |

Order steps on the Lakebase surface: `walk-1` to `walk-2` ΔL* 14.0; `walk-2` to `walk-beyond` ΔL* 12.0; `now` to
`walk-1` ΔL* 17.2. Hop 1 and hop 2 are the same hue at different lightness, as the judge gap asks.

`check_contrast.py` must recompute every row above from the frontmatter hex values and fail on any drift.

## Type

- IBM Plex Sans and IBM Plex Mono, from the local files in `~/Library/Fonts`. Copy them into the project.
  Never load a web font.
- Sans fallback: Helvetica Neue, then Helvetica. Mono fallback: Menlo first, so code keeps a fixed advance, then
  Helvetica Neue and Helvetica.
- Floors come from the frame height: labels at least h/36, captions at least h/20. 16:9 (h 1080): kicker and
  code 36 px, labels 40 px, captions and evidence captions 56 px. 4:5 (h 1350): kicker and code 38 px, captions
  68 px. `check_text_size.py` gates both layouts.
- Captions take 2 lines maximum. Owner ruling (ticket 05, three-lines-4x5): in 4:5 only, GK-C40 (`b05-c40`) and
  GK-C24 (`b12-c24`) take three lines, so the 4:5 caption band is 230 px tall. No other cue gets a third line.
- Plex Mono advance is 0.6 em, so code at 36 px is 21.6 px per character. The 780 px code panel holds 33
  characters, which fits the longest displayed line, `NOT (e.dst_node_id = ANY(w.seen))`. Measure once at load.
- Labels: 4 words or fewer. Exact MONDO term names are data values, not labels. Flag them in `check_words.py`
  as an allowlist, not as an exception to the rule.

## Shape, stroke, texture

- One corner radius: 6 px on every rectangle. Circles are a shape for nodes and terms, not a second radius.
- One stroke scale on a 3 px unit: 3, 6, 9 px. No 1 px hairline, no other width.
- Delta table: a card with four vertical stripes. Lakebase Postgres table: a card with four horizontal rows. Same
  card size, same stroke, different orientation and system hue. No column names, no types, no grid, no cylinder.
- The synced table's Unity Catalog entry is a dashed, hollow card with one bar pointing toward Lakebase. It has no
  stripes and no rows, because it holds no data in Unity Catalog.
- Patients are squares. Clinicians and MONDO terms are circles. Queue marks are stacked bars.
- Edge width shows illustrative shared-patient weight in three bins (3, 6, 9 px). A refused thin edge is 3 px.
- No glow, blur, gradient, shadow, 3D, texture noise, or transparency at rest. A ring is a solid 6 px stroke.
- No official logos. "Databricks" and "Lakebase" are set in Plex Sans.

## Beat 6 composition — the signature frame (16:9, 1920×1080)

The graph and the SQL grow together. This frame is also the thumbnail.

| Element | Box (x, y, w, h) | Tokens |
|---|---|---|
| Headline | 64, 40, ≤1100, 72 | `headline`, text from STORYBOARD.md |
| Kicker, right-aligned on the headline baseline | right edge 1856, baseline 100 | `kicker` |
| Unity Catalog sliver (dimmed, no label; labelled in Beats 2–5) | 64, 136, 48, 764 | fill `ground`, stroke `uc-dim`, two striped stubs |
| Sync channel stub, horizontal | 112 → 192, y 518 | 3 px `uc-dim` |
| Lakebase panel (main panel) | 152, 136, 1704, 764 | `system-panel` Lakebase, tab "Lakebase Postgres" over the graph |
| Served views strip (dimmed) | 192, 380, 120, 276 | `postgres-card` in dim state |
| Graph region | 352, 136, 644, 764; Dr. A at (674, 518) | hop 1 radius 150, hop 2 radius 240, hop 3 stubs to 285, hop 4 stubs to 318 |
| Code panel | 1036, 176, 780, 684 | `code-panel`; tag at y 216; 7 lines from y 300 at 58 px pitch |
| Caption band | 64, 928, 1792, 128 | `caption`, 2 lines maximum, centred, on `ground` |

- Area: the Lakebase panel covers 1,301,856 of 2,073,600 px (62.8%). The Unity Catalog sliver covers 1.8%.
- Graph: four hop-1 clinicians on all sides of Dr. A. At most three hop-2 edges per hop-1 clinician. One hop-2
  clinician sits between two hop-1 clinicians so both edges reach it. Dashed `walk-beyond` stubs leave each hop-2
  node. The cut nodes are dashed hollow circles beyond one frontier, with "up to 25 per hop" once.
- Direct labels: "Dr. A" (`seed-label`), hop-1 names (`label`), "hop 1" and "hop 2" (`label`, `ink-2`) once each,
  on an edge of that hop.
- Lit sequence: each code line takes the `now` bar only while its graph event runs. The edges of that event are
  `now` at the same time. Then both drain to rest.
- Greyscale read: one dark-on-light code bar, one set of thick light edges, everything else in mid-greys.

4:5 (1080×1350), stacked: kicker 40, 40; headline 40, 96 (2 lines); Unity Catalog sliver 40, 256, 32, 928;
Lakebase panel 88, 256, 952, 928 (60.6% of the frame); graph region inside the panel at y 296–688 (hop 1 radius
100, hop 2 radius 180); code panel 112, 712, 660, 380 with 52 px pitch; caption band 40, 1108, 1000, 230 (three
68 px lines for GK-C40 and GK-C24 only).

## Beat 9 composition — the tree (16:9, 1920×1080)

The same Lakebase panel and the same code panel stay in place. The served views strip narrows to zero width
(layout ease). The web graph changes into the tree; it does not rerun.

| Element | Box (x, y, w, h) | Tokens |
|---|---|---|
| Headline and kicker | as Beat 6 | kicker text "public ontology · real terms" |
| Tree region | 192, 136, 804, 764 | `walk-1` for depth 1, `walk-2` for depth 2 |
| Dataset label above the seed | x 212, baseline 216 | "MONDO · public disease ontology", `label`, `ink-2` |
| Seed row, depth 0 | node (212, 276) r 22 | "diabetes mellitus", `seed-label` |
| Depth 1 rows | nodes x 276, y 356 / 436 / 516 / 596 | type 1 diabetes mellitus, type 2 diabetes mellitus, gestational diabetes, monogenic diabetes |
| Depth 2 rows (under monogenic diabetes) | nodes x 340, y 676 / 756 | neonatal diabetes mellitus; maturity-onset diabetes of the young (may wrap after "diabetes") |
| Depth counter | 820, 300, 176, 120 | "depth" `label` `ink-2` over the numeral, `counter` |
| Credit | x 212, baseline 852 | "MONDO · CC BY 4.0", `label`, `ink-2` |
| Code panel | 1036, 176, 780, 684 | 5 lines: `WITH RECURSIVE` / `walk(depth, frontier, seen)` / `SELECT w.depth + 1` / `NOT (e.dst_node_id = ANY(w.seen))` / `WHERE w.depth < 3` |
| Caption band | as Beat 6 | |

- Row order follows the query's `ORDER BY c.node_id COLLATE "C"`: 0005147, 0005148, 0005406, 0015967, then 0016391,
  0018911.
- Edges are straight 3 px lines from parent node to child node, not elbows.
- Each turn: all nodes of one depth snap in at once, the depth numeral rolls (old value rises out, new value rises
  in) and is `now` for that turn, and the acting code line holds the `now` bar. One claim on screen at a time.
- No time, no number apart from the depth numeral, and no patient mark in this beat.

4:5 (1080×1350): tree region 88, 256, 952, 520 at 64 px row pitch; the longest term fits on one line at x 292–942;
code panel 128, 800, 872, 340; caption band as Beat 6 in 4:5.

## Phone check

The phone style-frame copies use a responsive 390 px viewport. They do not scale a 1920 px bitmap. Panels stack,
the 36 px floor remains 36 CSS px, and every word stays readable. The 4:5 delivery uses the separate stacked layout.

## Learning from local references

Web access was not used, by instruction. These are the only references, all local.

- `contact-v6.png` (target grammar): take one question on screen from the first frame; one highlight per frame;
  every claim tied to its source by a line; "every hop is a copy, a queue and a delay" drawn as queues on long
  spans; the Databricks boundary that grows around what is already on screen. Serves house-style rules 3 and 4.
- `v4hf/style-frame.png` (the dark look the owner liked): take the near-black ground, large node names, hop 1 and
  hop 2 as direct labels, dashed continuation marks beyond the last hop, and frontier expansion from every hop-1
  node. Serves rules 1 and 2.
- From knowledge, not checked live: Bertin's texture and orientation channels (stripes vs rows for columnar vs row
  storage) and lightness for order (hop 1 vs hop 2); Tufte's sparse colour for emphasis; Albers on how a tint
  changes beside its neighbour, which is why each surface is checked against the ground and its neighbours.
- Left out: v6's paper ground, small sub-36 px text, thin grey outlines, and dense row lists (film is dark; manual
  look); v6's pull-back to the seven-system ring (a camera zoom); v4's gold seed on black (banned look), its single
  hue for everything (no system identity), its thin edges, its corner label "Lakebase Postgres · 4 CU" (corner
  label, and it puts a timing-graph setting on the illustrative graph), and the words "care network" and "doctor".

## Bar-fit note

Each local reference was put next to the owner's rulings for its beats: no camera move, no rerun of the web walk in
Beat 9, set B numbers only, glossary words only, dark film.

- `contact-v6.png` fits for Beats 1, 3 and 12 after one change: its ring view zooms out, so v5 resizes panels in
  place and grows the boundary around a still frame. It supplies no number.
- `v4hf/style-frame.png` fits for Beats 6 and 7 after three changes: lime replaces gold, glossary words replace
  "care network" and "doctor", and the "4 CU" corner label is removed from the illustrative graph. "4 CU" appears
  only in the Beat 8 evidence caption.
- No conflict needs an owner decision. Other prior captures under `.scratch/explainer-v2/refs/` were not opened in
  this pass; nothing here describes them.
