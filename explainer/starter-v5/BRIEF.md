---
workflow: general-video
flow: companion
storyboard: yes
message: "The graph is built from Unity Catalog Delta tables and served from Lakebase Postgres. There is no graph database outside Databricks: the copy that Lakebase serves is a Databricks-managed synced table."
destination: [linkedin, medium]
aspect: [1920x1080, 1080x1350]
language: en
length: 84s
audience: senior enterprise architects
---

## Intent

Lakebase Graph Kit film v5. One 84-second explainer, published on LinkedIn (4:5, direct upload) and in the Medium
article (16:9, unlisted YouTube embed). The owner does both uploads. The film shows a senior enterprise architect how
the kit builds a graph from Unity Catalog tables and serves walks from Lakebase Postgres, and every mechanism is drawn
the way the kit runs it. Small, true and finished beats a long, unfinished film.

The message is GK-C1, word for word (`git show 550256b:docs/release/post-claims.md`, row 47). The closing headline is
the tighter wording: "Built from Unity Catalog. Served by Lakebase. No graph database outside Databricks." It does not
widen GK-C1.

Look and feel: dark film register (design.md). Strong system colours on a near-black ground, one lime that means only
"what happens now", one shape that becomes the next, large type, holds after each idea. The voice carries the
sentences; the frame carries the picture and a few words.

## Assets

- `design.md` — tokens, type scale, Beat 6 and Beat 9 compositions, 4:5 boxes. Every hex and size comes from here.
- `claims.md` — every number, SQL line, narrator line and MONDO term, with its source file and line.
- `objections.md` — the 55-item hostile-reviewer list; each item names the film rule that blocks it.
- `GLOSSARY.md` — every term on screen and in the script; its _Avoid_ words stay out.
- `sql/web_folded.sql`, `sql/web_unfolded.sql`, `sql/tree.sql` — the printed walk SQL. Each displayed line is a
  substring of one generated line.
- `data/diabetes_terms.json` — exact MONDO labels, derived offline from release `v2026-10-06`.
- `.scratch/explainer-v2/contact-v6.png` — target grammar (local reference).
- `.scratch/explainer-v2/v4hf/style-frame.png` — the dark look the owner liked (local reference).

## Customizations

- Signature picture: the graph and the SQL grow together; each CTE line lights while its hop draws (Beat 6). It
  returns in Beat 7 (hops 3 and 4) and as `WITH RECURSIVE` in Beat 9. The thumbnail is a Beat 6 frame.
- Sound: one soft sine tick per hop and per tree turn, the same tone, a little higher on each deeper step, under the
  voice. Made on the laptop with ffmpeg. No music bed.
- Two layouts: 1920×1080 and 1080×1350. The 4:5 cut is its own stacked layout, never a crop.
- Narration script and `.srt` from the same text. Scratch voice with Mac `say` for timing only. The final voice is the
  owner's pick, asked in words: "my own voice" or "a computer voice".

## Notes

### Correction carried from the earlier brief text

An earlier brief text said `NOT IN` merges the hop-2 clinician who is reached from two hop-1 clinicians. That is
wrong. In `sql/web_folded.sql:15-16`:

- `GROUP BY e.dst_node_id` merges: two routes to one clinician become one row, with `MIN(e.weight)` as its support.
- `NOT IN (... hop0 ... hop1)` refuses: a clinician already reached in an earlier hop is not counted again.

The SQL applies `NOT IN` (a `WHERE` filter) before `GROUP BY`. So Beat 6 lights `NOT IN` first, then `GROUP BY`. The
claims.md Beat 6 narrator line says grouping first; the script must swap those two sentences (see open items).

### Negatives (all of them)

From the prompt's "Negatives":

- No camera zoom.
- No glow, blur or 3D.
- No row grids or schema boxes.
- No set A number: `1,615,105`, `0.69 ms`, `180 of 180` (also `180/180`, `1,350 s`).
- No "SDP" on screen or in the script.
- No SECURITY DEFINER functions.
- No support value printed for a hop-2 clinician. Never print "2" or a sum for the merged clinician.
- No similar walk.
- No payer or referral-leakage framing.
- No upload. Every HyperFrames command runs as `env -u GEMINI_API_KEY npx hyperframes ...`, including registry,
  preview, lint, check, snapshot and render. `capture` also uses `--skip-vision`. No `media-use` voice or music that
  calls out.

From "What must never happen":

- Unity Catalog is never drawn as governing what it does not govern. It holds the source Delta tables, the kit's
  nodes and edges Delta tables, and each synced table's `FOREIGN` entry. The reader role and the served views are
  Postgres grants inside Lakebase ("reader: views only"). The Lakebase database is not drawn as a Unity Catalog
  catalog. No governance or lineage claim about the synced copy beyond "Databricks-managed synced table".
- No number outside set B, and no number worded wider than its record.
- No SQL on screen that the kit does not run. No SQL line lit at a moment it does not act.
- No Postgres-manual look: no schema boxes, grids of rows, 1 px grey outlines, or labels in corners.
- No whiteboard look: no thin hand-placed lines, no fades used in place of mechanism motion.
- No frame, voice or file leaves the laptop. No live, paid, deploy or Databricks step. No OWNER-APPROVAL.md.

From the motion rules:

- No camera movement of any kind; no transform on the composition root. Panels resize in place.
- No glow, blur, gradient, shadow, 3D, texture noise, or transparency at rest. Emphasis is a solid ring or a thicker
  stroke plus a lightness change.
- No easing on exact edges, hops or tree levels (`ease: "none"`). Easing (`power2.inOut`) is for layout only.
- No stroke-offset animation. Reveals use clip-path, transform and opacity only.
- No scene change without a cause: the element you go into fills with its colour, holds 0.6 s, then a 0.5 s crossfade.
- No text that arrives after its shape. No caption cut in; captions roll as whole lines.
- No scale-only emphasis. No counter that counts through values that did not happen.
- No ripple or packet stream for the synced tables: SNAPSHOT is a full redraw.
- No sync and database write on the same axis: sync is horizontal, writes inside a store are vertical.

From the glossary and the owner:

- No "care network", no "doctor" as the noun, no "traversal", "query" (on screen), "BFS", "limit" (on screen),
  "top-N", "threshold", "k-anonymity", "aggregate", "snapshot" (for a version), "API", "endpoint".
- No official logos. "Lakebase" and "Databricks" are set in IBM Plex Sans.
- No adjectives that sell ("blazing", "seamless", "powerful").
- No "I work at Databricks" in the film (it goes in the post text).
- No text under 36 px in either layout.
- No teaser cut. One film, at most 90 s, in two layouts.

### Number set B (the only numbers allowed)

Run `624175097872827`, dated folder `dated_a967b82a4b90`, run commit `a967b82`, filled at commit `550256b`
(`docs/release/posts/medium-article.md`, `docs/KNOWN_LIMITS.md`). Full table: [claims.md](claims.md#number-allowlist).

| On screen | Beat | Source |
|---|---|---|
| `788 seconds`, caption `"sum of step run times · preflight to switch"` | 5 | GK-C23; `medium-article.md:118` |
| `4.2 ms` in `"19 of 20 answer in 4.2 ms or less"` | 8 | GK-C13; `medium-article.md:100,102` |
| `19 of 20` | 8 | GK-C13; `medium-article.md:100,102` |
| `1,000,000` in `"synthetic 1,000,000-node provider graph"` | 8 | `medium-article.md:102,118,122` |
| `4 CU` (evidence caption only) | 8 | `medium-article.md:102,118` |
| `"20 seeds per walk shape and depth: equal"` | 11 | GK-C10; `medium-article.md:98` |

Allowed in set B but not used on screen: `1,519,226 edges`, `3.6 ms`, `3.8 ms`, `3.9 ms`.

Kit settings (not run results), each with its source line:

| Setting | Beat | Source |
|---|---|---|
| `11` privacy floor | 4, 6 | `src/lgk/privacy/floor.py:18` |
| `25` cut per hop | 6 | `src/lgk/steps/walks.py:39` |
| `4` hops (web walks at most) | 7, 8 | `src/lgk/walks/sql.py:43`; GK-C34 |
| `2` in `WHERE w.depth < 2` (the displayed tree walk) | 9 | `sql/tree_display.sql:18` |
| depth numeral 0, 1, 2 | 9 | the loop's own counter, `sql/tree_display.sql:4` |

Version labels `v1` and `v2` are illustrative (claims.md "Illustrative elements").

`4.2 ms` always carries its evidence caption, `"client p95 · warm connection"` /
`"prepared statements off · in-region · 4 CU"`. That caption is a caption, not a label: it follows the caption rules
(56 px, at most 2 lines of 42 characters) and the 4-word label rule does not apply to it.

### Build-engine finding

`src/lgk/steps/build.py:1,44` says "SDP", but the build sends `CREATE OR REPLACE TABLE` and `INSERT INTO` statements
through `w.statement_execution.execute_statement(warehouse_id=...)` (`src/lgk/uc_sql.py:45`). The film says
"Spark SQL on a SQL warehouse" and says nothing about SDP. This is a docstring mismatch, logged in claims.md, not a code
edit.

### Run-time split

- Spark (Beat 4): 10 s, 11.9%.
- Lakebase as the main panel (Beats 6–11, 29–74 s): 45 s, 53.6%. With Beat 5, where the synced tables land in
  Lakebase: 51 s, 60.7%.
- Unity Catalog, the two usual paths and the close (Beats 1–3 and 12): 23 s.

### Local-reference bar fit check

No web source was opened. Only the two attached local images were used. No other prior capture was opened.

| Reference | Take | Ruling it meets or breaks | Change before use | Beats |
|---|---|---|---|---|
| `contact-v6.png` | Question on screen at frame 0; the wrong answer struck through in place; every claim tied to its source; "every hop is a copy, a queue and a delay" as queue marks on long spans; one Postgres database that holds every table | Breaks "dark film" (paper ground), the 36 px floor (small text), "no camera move" (its pull-back to the seven-system ring), and "no row grids" (its table list) | Dark ground; nothing under 36 px; the Databricks boundary grows in place around a still frame; tables are textured cards, not lists | 1, 3, 12 |
| `v4hf/style-frame.png` | Near-black ground; Dr. A in the middle with nodes on all sides; hop 2 grows from every hop-1 clinician; direct "hop 1" and "hop 2" labels; dashed continuation marks | Breaks "no black and gold" (gold seed), the glossary ("care network", "doctor"), "no corner labels" and the set-B scope ("Lakebase Postgres · 4 CU" in a corner on an illustrative graph), and the stroke scale (thin edges) | Lime replaces gold; "clinician" replaces "doctor"; the corner label goes, and "4 CU" appears only in the Beat 8 evidence caption; edges use the 3/6/9 px bins | 6, 7 |

Verdict: both references fit after the listed changes. No conflict needs an owner decision.

### Links

- Attacker list: [objections.md](objections.md)
- Claim, SQL and term sources: [claims.md](claims.md)
- Plan, frame by frame: [STORYBOARD.md](STORYBOARD.md)

### Resolved truth decisions

- `SET ROLE reader` comes from `src/lgk/app/template/backend/app/reader.py.tmpl:16`.
- The displayed tree walk uses depth 2 (`sql/tree_display.sql`), so the MONDO picture uses only the approved two
  levels below the seed.
- The walk-time `HAVING` line evaluates every candidate, but no default-floor edge fails because the build already
  enforced the same floor. Beat 6 uses the truthful "check-all-pass" picture.
- The closing limit uses one exact subset of GK-C24:
  `"Graph databases still win for ad hoc walks of unknown length."`
