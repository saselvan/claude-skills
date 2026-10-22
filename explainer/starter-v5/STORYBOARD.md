---
format: 1920x1080
duration: 90.6s
mode: autonomous
message: "The graph is built from Unity Catalog Delta tables and served from Lakebase Postgres. There is no graph database outside Databricks: the copy that Lakebase serves is a Databricks-managed synced table."
audience: senior enterprise architects
arc: Question → usual paths struck → build in Spark → sync to Lakebase → the walk (signature) → deeper → timed → tree → version → checked → claim
aspects: [1920x1080, 1080x1350]
---

## How to read this file

- One `## Frame N` section per beat, 12 beats, 90.6 s. Times are absolute seconds from frame 0.
- Text in quotes renders verbatim. Every number comes from set B or the kit settings in [BRIEF.md](BRIEF.md#number-set-b-the-only-numbers-allowed).
  Sources for every number, SQL line, narrator fact and MONDO term: [claims.md](claims.md). Attacks this plan blocks:
  [objections.md](objections.md).
- Tokens (hex, px, radius, stroke) are names from `design.md`. This file names them; it does not restate them.
- `voiceover` is the timing guide, trimmed to fit (open item 5 in BRIEF.md). The verbatim claims.md line is named under
  each beat.

## Global motion rules (every beat)

1. **One shape becomes the next.** In each beat, the main object of the end frame is on screen in the start frame,
   and the changed element has a name (listed under "verbs").
2. **Exact things are linear.** Edges, hop expansions, tree levels, pointer switches and request lines use
   `ease: "none"`, constant speed, and every edge of one event starts on the same frame. Edge speed: 1,200 px/s.
3. **Layout eases.** Panel resizes and card moves use `power2.inOut`, 0.75 s for a shape, 1.4 s for a shape that
   carries text. Text and its shape arrive together.
4. **Scene handoff.** Where a beat goes into a new element, that element fills with its system colour, holds 0.6 s,
   and then a 0.5 s crossfade runs. Everywhere else, panels resize in place.
5. **`now` lives only while the event runs.** Then it drains in 0.5 s to the settled token. Two `now` marks at the same
   time are one event (a code line and the edges it draws).
6. **No camera.** No transform on the composition root. No zoom, pan, glow, blur, 3D, shadow or gradient. No
   stroke-offset animation: reveals use clip-path, transform and opacity.
7. **Numbers roll** (old value rises out, new value rises in). They never count through values.
8. **Captions roll as whole lines** at 1.4 s. The caption band is the `.srt` cue for that time. Where an evidence
   caption owns the band (Beats 5 and 8), the `.srt` cue for those seconds is the evidence caption, and the narrated
   words for those seconds sit in the headline.

### Text classes

| Class | Rule | Examples |
|---|---|---|
| label | 4 words or fewer, on its mark, never in a corner, 40 px | "hop 1", "reader: views only", "cut: 25 per hop" |
| headline | the beat's finding, 64 px (72 px at the end) | "Each hop is one step of the walk." |
| kicker | one mono line, 36 px, on the headline baseline | "synthetic graph · names and counts are illustrative" |
| caption | 56 px, at most 2 lines of 42 characters, about 15 characters per second, 1–7 s hold | narration cue; GK-C24 line |
| evidence caption | a caption under a number; caption rules apply; it is not a label | `"client p95 · warm connection"` / `"prepared statements off · in-region · 4 CU"` |
| code | mono 36 px in the code panel; each line a substring of one printed line | `HAVING MIN(e.weight) >= 11` |
| data value | exact MONDO labels; an allowlist in `check_words.py`, not a label | "maturity-onset diabetes of the young" |

Labels that the prompt wrote with more than 4 words became headlines: "Spark SQL on a SQL warehouse builds the graph."
and "Web walks go up to 4 hops." The cut label is "cut: 25 per hop" (the glossary defines the cut as the most a hop
keeps). The narration says "up to 25 per hop".

### Sound

- One tick per hop and per tree turn, on the frame the hop's edges start. Nothing else makes a sound. No music bed.
- Tick: sine, 70 ms, 4 ms linear attack, 60 ms exponential fade, peak −24 dBFS, under the voice.
- Pitch ladder (+2 semitones per deeper step): hop 1 and tree depth 1 at 660 Hz; hop 2 and depth 2 at 741 Hz; hop 3 at
  831 Hz; hop 4 at 933 Hz.
- Made on the laptop with ffmpeg (`sine`, `afade`) by `generate_audio.py --ticks-only`, into each composition's
  `assets/ticks.wav`; the tick times are `ticks` in `screen-copy.json`. Nothing is downloaded.

### Beat 6 graph geometry (16:9; replaces design.md's radii, open item 8)

Dr. A at (674, 518). Hop 1 at radius 150, hop 2 at 240, hop 3 stubs to 285, hop 4 stubs to 318.

| Node | Position | Hop | Edge in (illustrative width) |
|---|---|---|---|
| Dr. A | (674, 518) | seed | — |
| Dr. B | (780, 412), NE | 1 | from Dr. A, 9 px |
| Dr. C | (780, 624), SE | 1 | from Dr. A, 6 px |
| Dr. D | (568, 624), SW | 1 | from Dr. A, 6 px |
| Dr. F | (568, 412), NW | 1 | from Dr. A, 3 px |
| shared clinician (no name) | (914, 518), E | 2 | from Dr. B 9 px and Dr. C 6 px; support is the smaller (6 px ring) |
| refused back-edge | Dr. B → Dr. C | 2 candidate | 6 px; refused by `NOT IN` |
| other hop-2 clinicians | at radius 240: one more from Dr. B (N), two more from Dr. C (SE, S-E), two more from Dr. D (SW, W-S), three from Dr. F (NW, N-W, W) | 2 | 3 or 6 px |
| past-the-cut candidates | three dashed hollow circles at radius 240, W sector, from Dr. F | 2 candidate | 3 px dashed |

At most three hop-2 edges leave each hop-1 clinician. Hop-2 nodes appear hollow (candidates) and fill with `walk-2`
only when the cut keeps them. Names are illustrative.

### 4:5 (1080×1350)

Stacked, recomposed from design.md's 4:5 boxes, never cropped. Headline at the top, the main panel in the middle, the
code panel under the graph, the caption band at the foot. Per-beat 4:5 notes are one line each. Overflow to check at
the style-frame stage: Beat 7 needs 9 code lines and Beat 8 needs 10 slots; the 4:5 code panel (452 px at 52 px pitch)
holds 8. In 4:5, the code panel grows to 560 px in Beats 7–8 by a layout resize of the graph region (hop 1 radius
100, hop 2 radius 160).

## Frame 1 — The question

- time: 0.0–4.0 s
- duration: 4s
- transition_in: none (frame 0 is settled)
- scene: The full question and Dr. A are on screen at frame 0
- voiceover: "Which clinicians share patients with Dr. A?"
- poster: 0
- status: outline

**Concept.** A real question opens the film, at rest, readable at frame 0 in a muted feed. One clinician, Dr. A, sits
under it: the start of every walk that follows.

**Event.** Nothing moves until 2.6 s; the frame is reading time. At 2.6–4.0 s the question slides up into the headline
slot and steps from 88 px to 64 px (layout, 1.4 s), and Dr. A slides left toward where Unity Catalog will open.

**Cause.** The film answers this question; every later beat is a step toward the answer.

**Lit / dimmed.** Lit: none (`now` is not used; nothing happens yet). At rest: the question (`ink`), the kicker
(`ink-2`), Dr. A (seed node, `ink` fill, 6 px `walk-1` ring).

**Physical grammar.** None. No mechanism acts.

**On-screen copy.** Question: "Which clinicians share patients with Dr. A?" Kicker: "synthetic graph · names and
counts are illustrative".

**Labels.** "Dr. A".

**SQL.** None.

**Technique / registry search intent.** Search hyperframes-registry for a title-card block with a settled first frame;
adapt only its frame-0 contract, not its entrance motion.

**Verbs.** Question HOLDS, then SLIDES up and SETTLES. Dr. A HOLDS, then SLIDES left.

**Transition out.** In place. No crossfade.

**Sound.** None (voice only).

**Six physical questions.** No mechanism is shown.

**Do not.**
- Do not show a blank, black or partly drawn frame 0.
- Do not animate the question in; it is settled at frame 0.
- Do not use the word "doctor" or "care network".
- Do not put a number on screen.

Claims.md narrator line: Beat 1. 4:5: question in 2 lines at 40, 96; kicker under it; Dr. A centred at y 700.

## Frame 2 — Unity Catalog holds the source tables

- time: 4.0–8.0 s
- duration: 4s
- transition_in: in place
- scene: Dr. A becomes one key in the clinicians Delta table inside Unity Catalog
- voiceover: "The source tables sit in Unity Catalog, as Delta tables."
- poster: 7
- status: outline

**Concept.** Before any graph, there is data in the lakehouse. The clinician we asked about is a key in a governed
Delta table.

**Event.** 4.0–5.4 s: the Unity Catalog panel opens in one left-to-right sweep (clip-path), carrying two Delta cards,
"clinicians" and "visits". 4.6–6.0 s: Dr. A travels into the clinicians card and becomes one cell of its first stripe
(the key column): the circle narrows into a 6 px stripe segment (layout, 1.4 s). 6.0–8.0 s: hold.

**Cause.** The kit reads its graph from these two source tables (`src/lgk/steps/build.py:81-83`).

**Lit / dimmed.** Lit: the key-stripe cell that was Dr. A, `now` for 6.0–6.5 s, then it drains to `uc-line`. At rest:
the Unity Catalog panel (`uc-surface`, 3 px `uc-line`), both Delta cards (`uc-card`, four vertical stripes).

**Physical grammar.** "Delta / Parquet — immutable columnar files": vertical stripes. "Unity Catalog — one field that
everything inside obeys": the boundary only; its "permission rows merge into one set" move is not used.

**On-screen copy.** Headline stays: "Which clinicians share patients with Dr. A?" Kicker stays.

**Labels.** Panel tab: "Unity Catalog". Cards: "clinicians", "visits". First-use label under both cards: "Delta tables".

**SQL.** None.

**Technique / registry search intent.** Search for a "card with texture" or "data table card" block; adapt to
design.md `delta-card` (stripes, no column names).

**Verbs.** Panel SWEEPS open. Cards travel WITH the sweep. Dr. A MORPHS into a stripe cell and LOCKS IN.

**Transition out.** In place. No crossfade.

**Sound.** None.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Source Delta tables in Unity Catalog | Exact stored values | Discrete rows in columnar files | One copy, registered once in Unity Catalog | At rest in this beat | Unity Catalog grants on these tables | Nothing changes; the tables stay |

**Do not.**
- Do not draw column names, types, a grid or a cylinder.
- Do not draw the two tables as horizontal rows; Delta is vertical stripes.
- Do not merge permission rows; this film does not use that Unity Catalog move.
- Do not make the panel fade in; it sweeps.

Claims.md narrator line: Beat 2. 4:5: Unity Catalog panel full width at 40, 256, 1000 × 600; cards side by side.

## Frame 3 — The two usual paths, struck through

- time: 8.0–14.5 s
- duration: 6.5s
- transition_in: in place
- scene: A copy leaves Databricks with queues and lag; an app request starts a warehouse query each time; both are struck
- voiceover: "One path copies data out of Databricks. One starts a warehouse query per request."
- poster: 12.95
- status: outline

**Concept.** Two familiar answers, each shown by its cause, each struck in place. This is framing from
`550256b:medium-article.md:19-26`, with no claim row and no number.

**Event.**
1. 8.0–8.6 s: the Unity Catalog panel narrows to the left third (layout, 0.75 s). The Databricks boundary draws as one
   6 px coral line around it, with an open edge on the right.
2. 8.6–10.35 s: path 1. A long horizontal span leaves the clinicians card, crosses the boundary, and reaches an outside
   graph-database card (`outside-surface`). Two queue stacks (bars) sit on the span. The outside card is a whole copy,
   labelled "graph database outside Databricks" and "another system to run". The span draws at constant speed. The
   Databricks tab shows at 8.75 s, after the Unity Catalog tab settles, so the two tabs never touch.
3. 10.35–10.85 s: a 6 px strike draws across path 1 (`now`), from the span's start to the copy's far edge, inside the
   frame; then it settles to `ink-3`; path 1 dims.
4. 10.85–12.85 s: path 2. An app card below sends three requests, one after another; each request starts one new query
   mark at a "SQL warehouse" card (`spark-surface`). The marks stack; nothing about time is drawn.
5. 12.85–13.3 s: a strike draws across path 2 (`now`), then settles to `ink-3`; path 2 dims (0.5 s).
6. 13.3–14.5 s: hold, 1.2 s. Both struck paths stay on screen so the reader sees why each one fails.

**Cause.** Path 1: a copy outside Databricks needs its own copy job and is another system to run. Path 2: each app
request starts a warehouse query.

**Lit / dimmed.** Lit, one at a time: the span as it draws, then strike 1; each request line, then strike 2. Dimmed
after their strikes: both paths (dim strokes, `ink-3` labels). At rest: Unity Catalog panel, boundary.

**Physical grammar.** "Pipeline / ETL / CDC chain — extra hops, extra copies": long span, queue at each hop, latency as
length (path 1 only). Path 2 uses no length and no time: only the cause (one query per request).

**On-screen copy.** Headline stays: "Which clinicians share patients with Dr. A?"

**Labels.** Boundary tab: "Databricks". Path 1: "its own copy job", "graph database outside Databricks", "another
system to run", first-use "queue" on one stack. Path 2: "app", "SQL warehouse", "per app request".

**SQL.** None.

**Technique / registry search intent.** Search for a "strike-through" or "crossed-out" callout block and a
"flow/pipeline" connector; adapt to a clip-path strike with 6 px stroke.

**Verbs.** Panel NARROWS. Boundary DRAWS. Span DRAWS at constant speed; queue bars STACK. Requests STEP; query marks
STACK. Strikes WIPE across, then SETTLE grey.

**Transition out.** In place: as Frame 4 starts, both struck paths retract toward their sources (layout, 0.75 s); the
boundary line leaves with path 1 (it returns in Frame 12).

**Sound.** None.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Copy to an outside graph database | Exact copy | Discrete batches in queues | Copied, outside Databricks | Over time, by its own copy job | Another system to run | A whole copy appears outside; the source stays |
| Warehouse SQL per app request | Exact | Discrete: one query per request | Shared (reads the tables in place) | Each request waits on its own query; no time is drawn | Unity Catalog grants on the warehouse read | A new query starts per request; the data stays |

**Do not.**
- Do not draw path 2 as a longer line, a clock, or a time value. No warehouse time was measured.
- Do not name a graph-database vendor.
- Do not show a number.
- Do not draw the boundary as a camera frame or move it.
- Do not use red-X icons; the strike is a 6 px line.

Claims.md narrator line: Beat 3. 4:5: path 1 on top, path 2 under it, Unity Catalog on the left edge as a 280 px column.

## Frame 4 — Spark SQL builds the graph

- time: 14.5–26.0 s
- duration: 11.5s
- transition_in: in place
- scene: Keys become nodes, visits fold into weighted edges, a pair under 11 makes no line
- voiceover: "Spark SQL on a SQL warehouse builds the graph. Keys become nodes and edges. Shared patients fold into one count. Under the floor of 11, no line."
- poster: 24.3
- status: outline

**Concept.** The build is a batch of SQL statements on a SQL warehouse. Patients never become nodes: their shared
visits fold into one count on a line, and a small count makes no line.

**Event.**
1. 14.5–15.9 s: Unity Catalog narrows to a 48 px sliver on the left with its two striped stubs; the Spark panel grows in
   place to fill the frame (layout, 1.4 s). Headline rolls to the Spark line.
2. 15.9–18.6 s: the key stripe of the clinicians card slides out into Spark and splits into five circles: Dr. A, Dr. B,
   Dr. C, Dr. D, Dr. F (layout, 1.4 s, labels with them). "nodes" label.
3. 18.6–22.1 s: patient squares (`ink-2`, 24 px) drop from the visits card between pairs of clinicians who share them
   (vertical, inside Spark). For each pair, the shared squares slide onto the gap and merge into one line. The line's
   width is its count bin (3, 6 or 9 px). The squares are gone; the line stays. "one count", "edges".
4. 22.1–24.9 s: one pair (Dr. C and Dr. F) has only two shared squares. They merge into a 3 px dashed `outside-line`
   stub that retracts at once; no line stays. "privacy floor: 11", "no line".
5. 24.9–26.0 s: hold.

**Cause.** The build runs `CREATE OR REPLACE TABLE` and `INSERT INTO` through the SQL warehouse
(`src/lgk/uc_sql.py:45`); the fold and the floor are in `build.py:270-293,400-429` and `floor.py:18`.

**Lit / dimmed.** Lit, one event at a time: the key stripe as it splits (15.9–17.3 s); the merging squares and the new
lines (18.6–20.6 s); the refused stub (22.1–22.9 s). Dimmed: the Unity Catalog sliver (`uc-dim`). At rest: Spark panel
(`spark-surface`, 3 px `spark-line`).

**Physical grammar.** "Show one thing becoming the next": a key column becomes nodes; two lines merge into one count.
Patients are squares, clinicians are circles (design.md `patient-mark`).

**On-screen copy.** Headline: "Spark SQL on a SQL warehouse builds the graph." Kicker stays.

**Labels.** Panel tab: "Spark SQL". "nodes", "edges", "patients" (first use, on the squares), "a few patients drawn",
"one count", "privacy floor: 11", "no line".

**SQL.** None on screen (the build SQL is not the walk; no code panel in this beat).

**Technique / registry search intent.** Search for a "morph / shape transition" block (circle from bar, squares to
line); hand-build if none keeps the stroke scale.

**Verbs.** Spark panel GROWS. Key stripe SLIDES out and SPLITS into nodes. Squares DROP, SLIDE together and MERGE into a
line. The weak pair's stub DRAWS and RETRACTS.

**Transition out.** In place (Frame 5 shrinks Spark).

**Sound.** None.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Build on a SQL warehouse | Exact (deterministic SQL) | Discrete statements | New derived tables are written; the source is read, not moved | Over time, one batch | Runs inside Unity Catalog; reads source tables, writes kit tables | Keys become nodes and edges; source tables stay |
| Fold | Exact count per pair | Discrete integer per pair | Derived; no patient is copied into the graph | During the build | Nobody sees a patient in the graph | Shared patients become one count; visits stay in the source |
| Build-time privacy floor | Exact (count ≥ 11) | Discrete yes/no per pair | — | During the build | A pair under 11 is never written | No edge for that pair; the source stays |

**Do not.**
- Do not write or say "SDP", "pipeline", "cluster" or "job" here.
- Do not draw a patient as a circle or as a node.
- Do not print a count on any line.
- Do not imply the squares drawn are the real count; "a few patients drawn" stays on screen while squares are on screen.
- Do not ease the line widths; the merge is a layout move, the resulting line snaps.

Claims.md narrator line: Beat 4. 4:5: Spark panel at 40, 256, 1000 × 928; nodes in a ring at the centre.

## Frame 5 — Delta tables in Unity Catalog, synced into Lakebase

- time: 26.0–32.0 s
- duration: 6s
- transition_in: in place
- scene: Nodes and edges land as Delta tables; synced tables copy them in full as Postgres rows; 788 seconds to first served graph
- voiceover: "Nodes and edges sync into Lakebase Postgres. First served graph: 788 seconds."
- poster: 30.0
- status: outline

**Concept.** The graph lands in Unity Catalog as Delta. A Databricks-managed synced table copies each one, whole, into
Lakebase Postgres, where it changes texture from stripes to rows. Its Unity Catalog entry stays behind, hollow.

**Event.**
1. 26.0–27.4 s: Spark shrinks to a 136 px column on the left (layout, 1.4 s). The nodes and the lines drop down into
   two new Delta cards, "nodes" and "edges", inside the Unity Catalog panel, which widens to the centre (vertical
   write).
   The kicker swaps to the graph kicker "synthetic provider graph · 1,000,000 nodes · 1,519,226 edges · 4 CU".
2. 26.6–27.75 s: the Lakebase panel opens on the right. For each Delta card, one solid card silhouette slides right
   along its own horizontal channel, Delta to Postgres directly (constant speed, 27.15–27.75 s, no ripple). As it
   crosses into Lakebase, a left-to-right clip-path replaces its vertical stripes with horizontal rows: a full copy.
   The Delta card stays. A dashed hollow "UC entry · synced table" card shows below each copy line, off the line,
   inside Unity Catalog. "snapshot" labels the first channel.
3. 27.75–30.3 s: "first served graph" and the number roll in over the Lakebase panel. 788 is settled 28.25–30.3 s
   under the graph kicker and leaves at 30.3 s. The evidence caption owns the caption band.
4. 30.9–31.5 s: the Lakebase panel fills with `lakebase-surface` and holds (0.6 s).
5. 31.5–32.0 s: 0.5 s crossfade into the signature frame.

**Cause.** Provisioning creates synced tables in SNAPSHOT mode by default (`src/lgk/steps/provision.py:193-234`; the
TRIGGERED mode exists only for a streaming source, `provision.py:271`).

**Lit / dimmed.** Lit, one at a time: the two dropping cards (26.4–27.2 s); the two sliding silhouettes and the channel
(27.4–28.8 s); the number (29.2–29.7 s). Dimmed: Spark column (`spark-dim`). At rest: Unity Catalog panel and its
cards, Lakebase panel.

**Physical grammar.** "Synced table (Delta → Lakebase)", SNAPSHOT row: a full copy, never ripples, in its own
horizontal channel. "Postgres / Lakebase tables": horizontal rows. "Keep motion on separate axes": the write into Unity
Catalog is vertical; the sync is horizontal.

**On-screen copy.** Headline: "Synced tables copy the graph into Lakebase in full." Number line: "first served graph" over
"788" (`number`, 144 px) and "seconds" (`headline`, 64 px, same baseline). Evidence caption (caption band):
"sum of step run times ·" / "preflight to switch".

**Labels.** "nodes", "edges" (Delta cards), "UC entry · synced table" (once), "snapshot" on the first channel, Lakebase tab "Lakebase Postgres", "nodes", "edges" (Postgres cards), "first served graph".

**SQL.** None.

**Technique / registry search intent.** Search for a "data sync" or "transfer between panels" block and a "big number
with caption" stat block; adapt the stat block to the number roll and the evidence caption.

**Verbs.** Spark SHRINKS. Cards DROP into Unity Catalog. Silhouettes SLIDE along the channel at constant speed; texture
WIPES from stripes to rows. Synced entries LOCK IN. Number ROLLS in. Lakebase panel FILLS and HOLDS.

**Transition out.** Scene handoff: fill (30.9 s), hold 0.6 s, crossfade 0.5 s, ending at 32.0 s.

**Sound.** None.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Kit nodes and edges as Delta tables | Exact | Discrete files | New tables in Unity Catalog | Written at the end of the build | Unity Catalog grants | New tables appear; the source stays |
| Synced table, SNAPSHOT | Exact full copy | Discrete: the whole table at once | Copied: a Databricks-managed synced table in Lakebase | Over time, one full copy per build, never row by row | In Lakebase, Postgres grants decide | Lakebase rows are replaced whole; the Delta table stays |
| Synced table's Unity Catalog entry | Exact | Discrete entry | Not a copy: `table_type FOREIGN`, a federated read of Lakebase Postgres | Stays | Unity Catalog | Nothing; it stays, hollow, inside Unity Catalog |
| First served graph, 788 seconds | Measured once | One value | — | A sum of step run times, preflight to switch; not wall-clock | — | — |

**Do not.**
- Do not ripple, stream packets, or animate rows one by one.
- Do not move the sync vertically or the write horizontally.
- Do not put stripes or rows in the synced entry; it holds no data.
- Do not draw the Lakebase database as a Unity Catalog catalog or inside the Unity Catalog panel.
- Do not write "788 s" or round it; do not drop its evidence caption.
- Do not claim lineage or governance for the synced copy beyond "UC entry · synced table".
- Do not draw the copy line through the synced entry; the entry sits below the line.

Claims.md narrator line: Beat 5. 4:5: Unity Catalog on top (40, 256, 1000 × 420), Lakebase under it (40, 716,
1000 × 460); the sync runs as a short horizontal channel between a Delta card and its Postgres card placed side by side
across the two panels' shared edge, so the sync stays horizontal.

## Frame 6 — The walk: graph and SQL grow together (signature)

- time: 32.0–49.5 s
- duration: 17.5s
- transition_in: crossfade 0.5s (from the Lakebase fill)
- scene: Each CTE line lights as its hop draws; NOT IN refuses, GROUP BY merges, HAVING refuses, the cut keeps
- voiceover: "The app begins at Dr. A. Each hop is one step of the query. Earlier clinicians stay out. Two routes to one clinician become one row. The privacy floor runs again. The cut keeps up to 25 per hop."
- poster: 36.3
- status: outline

**Concept.** The film's centre and its thumbnail. One clinician, one code panel. Every line of the walk lights only at
the moment it acts on the graph, and the graph shows what that line did.

**Layout.** design.md "Beat 6 composition", with this file's graph geometry. Lakebase panel 152, 136, 1704 × 764;
Unity Catalog sliver (dim) at 64; served views strip (dim) at 192, 380; graph region 352–996; code panel 1036, 176,
780 × 684; tag "simplified" at y 216; code lines from y 300 at 58 px pitch.

**Event and SQL line state.** Code lines: L1 `WITH hop0 AS (...)` (`sql/web_folded.sql:1`); L2 `hop1 AS (` (`:2`);
L3 `hop2 AS (` (`:11`); L4 `  NOT IN (... hop0 ... hop1)` (`:15`); L5 `  GROUP BY e.dst_node_id` (`:16`); L6
`  HAVING MIN(e.weight) >= 11` (`:16`); L7 `  LIMIT 25` (`:19`). L4–L7 are indented under L3: they act inside hop 2.

| Time (s) | Graph event | L1 | L2 | L3 | L4 | L5 | L6 | L7 |
|---|---|---|---|---|---|---|---|---|
| 32.0–33.4 | Dr. A's ring turns `now` (the start row) | lit | rest | rest | rest | rest | rest | rest |
| 33.4–35.4 | Four hop-1 edges snap out together (33.4–33.6); Dr. B, C, D, F arrive with names; "hop 1" | rest | lit | rest | rest | rest | rest | rest |
| 35.4–37.5 | Hop-2 candidate edges snap out from all four hop-1 clinicians together (35.4–35.6); candidates appear hollow; "hop 2", "a few nodes drawn" | rest | rest | lit | rest | rest | rest | rest |
| 37.5–40.0 | The Dr. B → Dr. C edge turns `now`, then dashed `outside-line`, then retracts (38.1–38.5); "already reached" | rest | rest | rest | lit | rest | rest | rest |
| 40.0–42.5 | The two edges into the shared clinician turn `now`; one 6 px ring closes on it (the smaller support); "one row" | rest | rest | rest | rest | lit | rest | rest |
| 42.5–45.0 | Every kept candidate edge turns `now` together, then settles without changing; "floor checked again" | rest | rest | rest | rest | rest | lit | rest |
| 45.0–47.5 | The kept hop-2 candidates fill with `walk-2` at once; three W-sector candidates turn dashed `walk-beyond`; "cut: 25 per hop" | rest | rest | rest | rest | rest | rest | lit |
| 47.5–49.5 | Hold: the signature frame, 2 s, no caption | rest | rest | rest | rest | rest | rest | rest |

Each filter row (`NOT IN`, `GROUP BY`, `HAVING`, `LIMIT`) lasts 2.5 s: the event runs, then the graph holds so the
reader can match the lit line to what it did. The last caption leaves at 47.5 s; the 2 s hold after `LIMIT` has no
caption.

"lit" is the `now` bar (`now-ink` on `now`); "rest" is `ink-2` on `code-bg`. Each lit line and its edges drain together
in 0.5 s.

**Cause.** The generated app sends the kit's web walk over the served views (`walk.py.tmpl`). Each hop is one CTE that joins
`edges_view` to the previous hop. Edges are indexed on `src_node_id` and `dst_node_id` (commit `4948a69`), so a hop is
an exact lookup.

**Lit / dimmed.** Lit: the one acting line and its graph event (table above). Dimmed for the whole beat: Unity Catalog
sliver (`uc-dim`), sync stub, served views strip (dim state). At rest: Lakebase panel, settled nodes and edges.

**Physical grammar.** "SQL lookup, exact match": an exact jump, linear, no easing. "Following a reference": each edge is
a straight line that snaps and never drifts. "A walk through a graph": the frontier grows from every node of the last
hop, not one path. Refusal: a dashed `outside-line` edge that retracts.

**On-screen copy.** Headline: "Each hop is one step of the walk." Kicker: "synthetic graph · names and counts are
illustrative". Code tag: "simplified".

**Labels.** Tab "Lakebase Postgres"; "served views" (dim strip, first use); "Dr. A" (`seed-label`); "Dr. B", "Dr. C",
"Dr. D", "Dr. F"; "hop 1" and "hop 2" (once each, on an edge of that hop, `ink-2`); "already reached"; "one row";
"floor checked again"; "cut: 25 per hop"; "a few nodes drawn".

**Technique / registry search intent.** Search hyperframes-registry for a "code panel" or "syntax highlight / line
focus" block and a "network graph / node-link" data-viz block. Adapt: the code block must take a full-width 52 px lit
bar with 6 px radius; the graph block must take linear edge draws and design.md node tokens. Do not paste either.

**Verbs.** Code lines LIGHT and DRAIN. Edges SNAP out at constant speed. Nodes LOCK IN at edge tips with their names.
Refused edges TURN dashed and RETRACT. The shared clinician's ring CLOSES. Kept nodes FILL together.

**Transition out.** In place into Frame 7.

**Sound.** Tick hop 1 at 33.4 s (660 Hz). Tick hop 2 at 35.4 s (741 Hz). No tick for the filters or the cut.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| A hop (CTE joins `edges_view` to the previous hop) | Exact indexed lookup | Discrete: whole hop at once | Shared: reads the served views over the synced tables; nothing is copied | One step of one query | The reader, through served views | The frontier grows; edges stay |
| `NOT IN` the earlier hops | Exact set exclusion | Discrete per candidate | Shared | Inside the same query, before grouping | Reader | A clinician already reached is not counted again; it keeps its earlier hop |
| `GROUP BY e.dst_node_id` with `MIN(e.weight)` | Exact | Discrete: one row per clinician | Shared | Inside the query | Reader | Two candidate rows become one row, support the smaller weight; both edges stay in the table |
| `HAVING MIN(e.weight) >= 11` at walk time | Exact (≥ 11) | Discrete yes/no | Shared | Inside the query, every walk | Reader never receives a row under the floor | Every default-floor candidate passes again; the graph stays |
| The cut, `LIMIT 25` per hop (after `ORDER BY c.support DESC`) | Exact, deterministic order | Discrete: at most 25 rows | Shared | Per hop, inside the query | Reader | The hop keeps at most 25; the rest stay in the graph, not in this answer |

**Do not.**
- Do not light `NOT IN` for the merge. `GROUP BY` merges; `NOT IN` refuses a node from an earlier hop.
- Do not draw a walk-time edge below 11; the build already removed it.
- Do not print a support value, "2", or a sum on the shared clinician or on any edge.
- Do not put "1,000,000" on this graph; it is the timing graph's size (Frame 8).
- Do not ease any edge or hop; only layout eases.
- Do not light a line before or after its graph event; do not light two lines for two events.
- Do not draw a hop as one path from one node.
- Do not use glow, blur, a halo or a pulse on Dr. A; the ring is a solid 6 px stroke.
- Do not show `ORDER BY` as a separate lit event; the cut is one event.
- Do not show SECURITY DEFINER functions or any function call.
- Do not show "4 CU" or any latency here.
- Do not use a corner label.

Thumbnail: the 36.3 s frame (L3 lit, hop-2 edges `now`, hop-1 settled). Greyscale read: one dark-on-light code bar and
one set of thick light edges.

Claims.md narrator line: Beat 6, with the two middle sentences swapped (BRIEF open item 4). 4:5: design.md 4:5 Beat 6
boxes; graph at y 296–688 with hop 1 radius 100, hop 2 radius 160.

## Frame 7 — The same pattern, deeper

- time: 49.5–53.5 s
- duration: 4s
- transition_in: in place
- scene: hop3 and hop4 lines append; two faint rings of stubs grow from the kept frontier
- voiceover: "The same exact pattern appends hop 3 and hop 4."
- poster: 53.0
- status: outline

**Concept.** Depth is the same CTE again. The signature returns, faint: nothing new to learn, only further to go.

**Event.**
1. 49.5–51.1 s: the code panel grows one line in place (layout, 0.75 s) and L8 `hop3 AS (` rolls in (1.4 s); it
   lights at 50.3 s. At 50.3 s dashed `walk-beyond` stubs snap out together from every kept hop-2 clinician to radius
   285 (constant speed). "hop 3".
2. 51.1–52.7 s: L9 `hop4 AS (` appends the same way and lights at 51.9 s; stubs snap from every hop-3 stub tip to
   radius 318. "hop 4".
3. 52.7–53.5 s: hold. L8 and L9 settle to `ink-3` (faint).

**Cause.** `sql/web_folded.sql:20-37`: hop 3 joins to hop 2, hop 4 joins to hop 3, with the same filters. Web walks go
at most 4 hops (`src/lgk/walks/sql.py:43`, GK-C34).

**Lit / dimmed.** Lit: L8 with the hop-3 stubs; then L9 with the hop-4 stubs. Dimmed: L1–L7 to `ink-3` while the new
lines act; the Frame 6 graph stays settled. Dashed past-the-cut candidates do not grow stubs.

**Physical grammar.** "SQL lookup, exact match" (linear). "Show progress, not repetition": each hop leaves a new ring
behind.

**On-screen copy.** Headline: "Web walks go up to 4 hops."

**Labels.** "hop 3", "hop 4".

**SQL line state.** L1–L7 dim (`ink-3`); L8 `hop3 AS (` (`sql/web_folded.sql:20`) lit 50.3–51.1 s, then `ink-3`;
L9 `hop4 AS (` (`:29`) lit 51.9–52.7 s, then `ink-3`.

**Technique / registry search intent.** Same code-panel block as Frame 6 (append a line in place).

**Verbs.** Panel GROWS one line. Lines ROLL in and LIGHT. Stubs SNAP out at constant speed. Lines SETTLE faint.

**Transition out.** In place.

**Sound.** Tick hop 3 at 50.3 s (831 Hz). Tick hop 4 at 51.9 s (933 Hz).

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Hops 3 and 4 | Exact indexed lookup | Discrete | Shared | One more step of the same query each | Reader | The frontier grows two rings; at most 4 hops; the graph stays |

**Do not.**
- Do not zoom out or scale the graph group to make room.
- Do not name hop-3 or hop-4 clinicians or show their count.
- Do not draw a fifth hop.
- Do not grow stubs from past-the-cut candidates.

Claims.md narrator line: Beat 7. 4:5: code panel grows to 560 px; stubs to radius 190 and 210.

## Frame 8 — The app, as reader, and the timed walk

- time: 53.5–61.5 s
- duration: 8s
- transition_in: in place
- scene: The app sets its role, sends the walk to the served views, gets the answer back over a short path; then the timed result on its own graph
- voiceover: "The app reads served views only. On the timing graph, 19 of 20 walks answer in 4.2 milliseconds or less."
- poster: 60.5
- status: outline

**Concept.** The answer path is short and narrow: one role, views only. Then the number, on the graph it was measured
on, with its test mode, and with the floor line visibly not part of that walk.

**Event.**
1. 53.5–54.9 s: layout (1.4 s). The Unity Catalog sliver narrows to zero. An app panel (`app-surface`) opens at 64, 136,
   360 × 764. The Lakebase panel resizes to 464–1856. The served views strip moves to 504–624, next to the app panel.
   The clinician graph slides 24 px and leaves (opacity), with its names. The code panel stays at 1036.
2. 54.9–55.9 s: "SET ROLE" / "reader" (mono, one statement shown on two lines) lights inside the app panel. The served
   views strip leaves the dim state; "reader: views only" arrives under it.
3. 55.9–56.7 s: a request line snaps from the app panel to the served views strip (80 px, constant speed, `now`); the
   code panel's outline steps from 3 px to 6 px `now` (the walk is sent; one event).
4. 56.7–57.3 s: the answer returns as one short horizontal row bar from the strip to the app (constant speed); `now`
   drains.
5. 57.3–58.7 s: headline and kicker roll. A field of small unnamed `walk-beyond` dots fills the graph region at once
   (opacity with a 4 px move): the timing graph. L6 `HAVING` goes to `ink-3`; the lines under it move down one pitch
   (layout, 0.75 s) and "not in timed walk" sits in the freed slot. The evidence caption owns the caption band.
6. 58.7–61.5 s: hold (reading time).

**Cause.** The app runs `SET ROLE reader` (`reader.py.tmpl:16`) and sends the web walk over the served views
(`walk.py.tmpl`, GK-C6). The
timed walks used the unfolded SQL (`sql/web_unfolded.sql`), which has no `HAVING` clause; the timing graph is
`src/lgk/loaders/scale_graph.py` at `550256b`: referral and membership edges, no patients, no fold.

**Lit / dimmed.** Lit, one event at a time: "SET ROLE reader"; the request line with the code outline; the return
bar. Dimmed: L6 `HAVING` (`ink-3`) and its label; L8–L9 stay `ink-3`. At rest: app panel, Lakebase panel, served views
strip, L1–L5 and L7 (`ink-2`).

**Physical grammar.** New entry, reasoned with the six questions: "Postgres grant (reader role) — access that stops at
the views": the request line ends at the views strip and never reaches a table card. "Latency is distance": the path is
drawn 80 px long, the shortest path in the film.

**On-screen copy.** Headline (53.5–57.3 s): "The app reads served views only." Headline (57.3–61.5 s): "Web and tree walks, depth 1 to 4:
19 of 20 answer in 4.2 ms or less" (2 lines). The app box dims at 57.3 s and carries "timed: kit measure step". Kicker
(57.3–61.5 s): "synthetic 1,000,000-node provider graph". Evidence caption (caption band, 57.3–61.5 s, 4.2 s hold):
"client p95 · warm connection" / "prepared statements off · in-region · 4 CU".

**Labels.** App tab "app"; "reader: views only" (Postgres grant, in Lakebase); "not in timed walk"; on the field "a few
drawn" and "no patients · no fold".

**SQL line state.** App panel: "SET ROLE" / "reader" lit 54.9–55.9 s, then rest. Code panel: L1–L5, L7 rest; L6 `HAVING
MIN(e.weight) >= 11` dim from 57.3 s with "not in timed walk" under it; L8–L9 dim. No line lights during the timing.

**Technique / registry search intent.** Search for a "stat callout" block (headline with a number and an evidence
caption) and a "request/response connector" block; adapt the connector to a constant-speed 80 px line.

**Verbs.** App panel OPENS; Lakebase RESIZES; views strip SLIDES next to the app. Role line LIGHTS. Request SNAPS across;
answer bar SNAPS back. Field APPEARS at once. HAVING DIMS; lines below STEP down. Headline ROLLS.

**Transition out.** In place.

**Sound.** None (no hop is drawn in this beat).

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Reader role and served views | Exact grant | Discrete: allowed or not | Shared views over the synced tables | Set once per connection | The reader sees views only; no raw table, schema or column (a Postgres grant, not a Unity Catalog permission) | Nothing changes; the grant stays |
| App sends the walk and gets the answer | Exact | Discrete request and response | Shared | A short round trip | The app, as reader | The app gets rows; the graph stays |
| Timed result, 4.2 ms | Measured: client p95 on a warm connection, prepared statements off, in-region, 4 CU | 19 of 20 timed walks per depth at or under the value | — | Over the timing run | — | Measured on the timing graph only, not on the clinician graph |

**Do not.**
- Do not light `HAVING` in this beat; the timed walks did not use it.
- Do not show the clinician graph, its names or patient squares while "4.2 ms" is on screen.
- Do not drop or shorten the evidence caption; do not set it as a label.
- Do not show a SECURITY DEFINER function or any function surface.
- Do not draw the reader role as a Unity Catalog permission or inside the Unity Catalog panel.
- Do not let the request line reach a table card.
- Do not show `0.69 ms`, `1,615,105`, `180 of 180`, or any other latency.
- Do not draw a pool, a cloud or a server icon.

Claims.md narrator line: Beat 8. 4:5: app panel as a band on top (40, 256, 1000 × 200), Lakebase under it; the request
line is vertical here only because the band is above (it is a request, not a sync); the evidence caption in the
caption band.

## Frame 9 — Question 2: the tree walk on MONDO

- time: 61.5–70.5 s
- duration: 9s
- transition_in: in place
- scene: The code panel becomes WITH RECURSIVE; the tree grows one is-a level per turn as the depth counter climbs
- voiceover: "The same kit walks a tree. From diabetes mellitus, one recursive loop adds one is-a level per turn."
- poster: 68.0
- status: outline

**Concept.** A second real question, on real public terms. One loop, one level per turn, and a counter that shows
progress. The web walk does not rerun; its clinician leaves.

**Layout.** design.md "Beat 9 composition". Tree region 192, 136, 804 × 764; seed at (212, 276); depth-1 nodes at x 276,
y 356 / 436 / 516 / 596; depth-2 nodes at x 340, y 676 / 756; depth counter at 820, 300; credit at x 212, baseline 852.

**Event.**
1. 61.5–62.9 s: layout (1.4 s). The app panel narrows out; the Lakebase panel returns to 152–1856; the served views strip
   narrows to zero width; the timing field leaves. The code lines roll, as whole lines, into T1–T5. The seed term
   arrives at its place with its label. Headline and kicker roll. "depth" over "0".
2. 62.9–64.7 s: turn 1. T3 lights. The counter rolls 0 → 1 (`now`). Four depth-1 terms snap in together with straight
   3 px `walk-1` edges from the seed (constant speed).
3. 64.7–66.5 s: turn 2. T3 lights again. The counter rolls 1 → 2. Two depth-2 terms snap in under "monogenic diabetes"
   with `walk-2` edges.
4. 66.5–67.7 s: T5 `WHERE w.depth < 2` lights as the two-turn loop stops.
5. 67.7–70.5 s: hold. The credit and "a few terms drawn" stay.

**Cause.** `sql/tree.sql:1-19`: one `WITH RECURSIVE walk(depth, frontier, seen)` loop. Each turn selects
`w.depth + 1` and the children of the frontier that are not yet seen, ordered by `node_id COLLATE "C"`, at most 25.
The displayed loop runs while `w.depth < 2`.

**Lit / dimmed.** Lit, one turn at a time: T3 with the new level and the counter; T5 at the stop. T4 never lights:
no drawn term is reached twice, so it refuses nothing on screen. At rest: T1, T2, T4. Dimmed: nothing else is on screen.

**Physical grammar.** "Show progress, not repetition": each turn leaves a level and a counter step behind. "SQL lookup,
exact match": levels snap in, linear. Tree edges are straight parent-to-child lines, not elbows.

**On-screen copy.** Headline: "Which diseases are kinds of diabetes?" Kicker: "public ontology · real terms". Dataset
label: "MONDO · public disease ontology". Credit: "MONDO · CC BY 4.0".

**Terms (data values, exactly as claims.md; order by MONDO ID).**
- Seed, depth 0: "diabetes mellitus" (MONDO:0005015).
- Depth 1: "type 1 diabetes mellitus" (MONDO:0005147), "type 2 diabetes mellitus" (MONDO:0005148), "gestational
  diabetes" (MONDO:0005406), "monogenic diabetes" (MONDO:0015967).
- Depth 2, under monogenic diabetes: "neonatal diabetes mellitus" (MONDO:0016391), "maturity-onset diabetes of the
  young" (MONDO:0018911; it may wrap after "diabetes").

The release has 8 direct children and 9 grandchildren (`data/diabetes_terms.json`). The film draws 4 and 2 and says so.

**Labels.** "depth" (over the counter); "a few terms drawn".

**SQL line state.** T1 `WITH RECURSIVE` and T2 `walk(depth, frontier, seen)` (`sql/tree_display.sql:1`, one line shown on two)
 lit 62.1–62.9 s as the seed arrives; T3 `SELECT w.depth + 1` (`:4`) lit 62.9–63.9 and 64.7–65.7 s; T4
`NOT (e.dst_node_id = ANY(w.seen))` (`:11`) rest throughout; T5 `WHERE w.depth < 2` (`:18`) lit 66.5–67.7 s.

**Technique / registry search intent.** Search for a "tree / hierarchy" data-viz block and a "number roll / counter"
block; adapt the counter to the roll pattern (no count-through) and the tree to straight edges at fixed row pitch.

**Verbs.** Panels RESIZE. Code lines ROLL into new lines. Seed LOCKS IN. Counter ROLLS one step per turn. Levels SNAP in
together. Stubs SNAP out. T5 LIGHTS as the loop STOPS.

**Transition out.** In place.

**Sound.** Tick depth 1 at 62.9 s (660 Hz). Tick depth 2 at 64.7 s (741 Hz).

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| `WITH RECURSIVE` tree walk | Exact | Discrete levels | Shared (served views) | Turns inside one query, one level per turn, at most 100 levels in the kit | Reader | Depth, frontier and seen grow; the terms stay |
| `NOT (... = ANY(w.seen))` | Exact | Discrete | Shared | Each turn | Reader | A term is reached at most once (no drawn case); stays at rest |
| `WHERE w.depth < 2` | Exact | Discrete | — | At the last turn | Reader | The loop stops |
| MONDO terms | Exact labels from release `v2026-10-06` | Discrete | Public data, CC BY 4.0, no patient data | Fixed release | Anyone | Nothing changes |

**Do not.**
- Do not show a time, a latency, or any number other than the depth numeral.
- Do not change, shorten or translate a MONDO label.
- Do not let Dr. A become a disease term, and do not keep any clinician mark on screen.
- Do not rerun the web walk or show web CTE lines.
- Do not draw a loop arrow or a circle that goes round.
- Do not light T4.
- Do not show patient squares.
- Do not use elbows or curves for tree edges.

Claims.md narrator line: Beat 9 (its MONDO sentence moves to the on-screen label). 4:5: tree region 88, 256,
952 × 520 at 64 px pitch; code panel 128, 800, 872 × 340.

## Frame 10 — A new version, in one transaction

- time: 70.5–75.5 s
- duration: 5s
- transition_in: in place
- scene: v2 tables are written; every served view's pointer moves from v1 to v2 at the same frame
- voiceover: "A new version moves every served view in one transaction, or none moves."
- poster: 74.0
- status: outline

**Concept.** The app never reads half a graph. All the views move together, or none do. A short beat; the article
carries the detail.

**Event.**
1. 70.5–71.9 s: layout. The code panel and the tree narrow out (clip, layout, 1.4 s). Inside Lakebase: the served views
   strip returns at the left as three small view cards ("served views"); two Postgres cards, "v1", sit to their right
   with pointer lines from each view.
2. 71.3–72.3 s: two "v2" Postgres cards drop in below the v1 cards (a write inside the database: vertical).
3. 72.3–73.1 s: one bracket ("one transaction") closes around all pointer lines; every pointer snaps from v1 to v2 on the
   same frame (constant speed, 0.3 s, `now`).
4. 73.1–75.5 s: the v1 cards go to the dim state; "all or none" sits on the bracket; hold.

**Cause.** `src/lgk/versions.py:284-296` `switch_views`, GK-C25: one Postgres transaction; if any statement fails, no
view moves and the app keeps the version it read before.

**Lit / dimmed.** Lit: the v2 cards as they drop; then the bracket and all pointers at once. Dimmed after the switch: the
v1 cards. At rest: the Lakebase panel, the view cards.

**Physical grammar.** New entry, reasoned with the six questions: "Version switch — pointers that move together": all
pointers move in one frame; nothing is copied at the switch. "Writes inside a database move vertically."

**On-screen copy.** Headline: "Every served view moves in one transaction."

**Labels.** "served views", "nodes", "edges", "v1", "v2", "one transaction", "all or none".

**SQL.** None on screen (the switch SQL is not in claims.md).

**Technique / registry search intent.** Search for a "pointer / reference swap" or "bracket callout" block; hand-build
if none keeps straight constant-speed pointers.

**Verbs.** Panels NARROW. v2 cards DROP. Bracket CLOSES. Pointers SNAP together. v1 DIMS.

**Transition out.** In place.

**Sound.** None.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Version switch | Exact | Discrete: all views or none | Pointers move; nothing is copied at the switch | One transaction, one commit | The reader sees v1 until the commit, then v2, never a mix | View targets change; the app's walk SQL stays |

**Do not.**
- Do not move the pointers one at a time or stagger them.
- Do not show a number, a time, or a "zero downtime" claim.
- Do not say or write "snapshot", "release" or "deploy" for a version.
- Do not claim when v1 is removed.

Claims.md narrator line: Beat 10 ("Postgres" dropped for time). 4:5: view cards on top, v1 and v2 side by side under
them; the v2 write drops vertically and the pointers run diagonally, so the two motions stay on separate axes.

## Frame 11 — Each answer equals a reference from the source tables

- time: 75.5–80.5 s
- duration: 5s
- transition_in: in place
- scene: A reference computed from the source tables and the served answer slide together and match
- voiceover: "Each answer equals a reference computed from the source tables."
- poster: 79.5
- status: outline

**Concept.** The served answer is checked against an answer computed apart from the kit, from the source tables, never
from the kit's own tables.

**Event.**
1. 75.5–76.9 s: layout. Unity Catalog widens on the left. It shows the source Delta cards ("providers", "referrals")
   and the dim kit cards ("nodes", "edges"). A "reference (SQL warehouse + Python)" box sits outside Unity Catalog
   and reads only from the source cards. No read line or answer bar touches the nodes or edges cards. Lakebase on the
   right shows one "served answer" row bar.
2. 76.9–78.1 s: a "reference" row bar leaves the reference card; the two bars slide toward a centre line (layout,
   0.75 s) and stack.
3. 78.1–78.7 s: one 6 px `now` bar spans both: "equal".
4. 78.7–80.5 s: `now` drains; hold.

**Cause.** GK-C10: the reference code (`src/lgk/measure/reference.py`, called from `src/lgk/steps/measure.py`) reads only
the source schema on the SQL warehouse and computes each walk in Python. On the timing graph, 20 of 20 seeds matched
for web and tree walks, depths 1 to 4 (`medium-article.md:98`).

**Lit / dimmed.** Lit: the read line, then the match bar. Dimmed: the kit's nodes and edges Delta cards, the synced
entries. At rest: source cards, reference card, served answer.

**Physical grammar.** New entry, reasoned with the six questions: "Reference check — two answers from two paths, laid
side by side". Close to "Validator / grounding check": each answer is tied to an independent source.

**On-screen copy.** Headline: "Web and tree, depths 1 to 4: 20 of 20 seeds equal".

**Labels.** "source tables", "reference (SQL warehouse + Python)", "served answer", "equal".

**SQL.** None.

**Technique / registry search intent.** Search for a "comparison / match" callout block; adapt to two row bars and one
bar that spans them.

**Verbs.** Unity Catalog WIDENS. Read line DRAWS. Bars SLIDE together and STACK. Match bar LOCKS IN.

**Transition out.** In place.

**Sound.** None.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Correctness check | Exact equality | Discrete: equal or not, per seed | Two separate computations; the reference reads source tables only | Over the measure step | The measure step | Nothing changes; it records "equal" |

**Do not.**
- Do not draw the reference reading the kit's nodes or edges tables.
- Do not write "180 of 180", a total, or a percent.
- Do not show a tick-mark icon; "equal" is a bar and a word.

Claims.md narrator line: Beat 11 (its second sentence moves to the headline). 4:5: source cards on top, reference and
served answer stacked under them.

## Frame 12 — The claim, inside Databricks

- time: 80.5–90.6 s
- duration: 10.1s
- transition_in: in place
- scene: The Databricks boundary grows around Unity Catalog, Lakebase, the app and the faint walk; the claim, the limit, the end card
- voiceover: "Built from Unity Catalog. Served by Lakebase. No graph database outside Databricks. Graph databases still win for ad hoc walks of unknown length."
- poster: 90.3
- status: outline

**Concept.** Pull nothing back; grow the boundary around what is already on screen. Then state the claim at its exact
width, and say where a graph database still wins.

**Event.**
1. 80.5–81.9 s: layout (1.4 s). The panels resize into one map: Unity Catalog (left, with source Delta cards, kit Delta
   cards and the hollow synced entries), Lakebase Postgres (centre, rows cards, served views, the faint Frame 6 walk
   with Dr. A), the app (right). The coral Databricks boundary grows outward from the panels' edges to enclose all
   three. The headline rolls in with it.
2. 81.9–83.9 s: hold.
3. 83.9–88.7 s: the GK-C24 caption owns the caption band (4.8 s, 82 characters).
4. 88.7–90.1 s: the caption band rolls to the end card lines; the kicker rolls to the README address.
5. 90.1–90.6 s: hold; the last frame carries the claim, the map and the end card.

**Cause.** GK-C1: built from Unity Catalog Delta tables, served from Lakebase Postgres, no graph database outside
Databricks. GK-C24: where a native graph database still wins. GK-C36: the README lists the prerequisites.

**Lit / dimmed.** Lit: the boundary as it grows (`now` for its draw, then it settles to `boundary`). At rest: all three
panels. Faint: the walk (settled `walk-1` / `walk-2`, no `now`).

**Physical grammar.** "Unity Catalog — one boundary around tables": used for the Unity Catalog frame only. The Databricks
boundary is outermost and the only 6 px structural line. "Grow the diagram in place" (from contact-v6, without its
pull-back).

**On-screen copy.** Headline (`end-line`, 72 px): "Built from Unity Catalog. Served by Lakebase. No graph database
outside Databricks." Caption (83.9–88.7 s): "Graph databases still win for ad hoc" / "walks of unknown length."
End card (caption band, 88.7–90.6 s): "Full numbers: the Medium article" / "Run it: the kit's README". Kicker
(88.7–90.6 s): "github.com/saselvan/graph-kit-for-lakebase".

**Labels.** Boundary tab "Databricks"; panel tabs "Unity Catalog", "Lakebase Postgres", "app"; "UC entry ·
synced table" (once); "reader: views only" (once, on the views).

**SQL.** None.

**Technique / registry search intent.** Search for an "end card" block; adapt to type only, no logo.

**Verbs.** Panels RESIZE into the map. Boundary GROWS outward. Headline ROLLS in. Caption ROLLS. End card ROLLS in and
HOLDS.

**Transition out.** None. The film ends on a settled frame (it is also the loop point for LinkedIn and the last frame of
a Medium GIF).

**Sound.** None.

**Six physical questions.**

| Mechanism | Exact or approximate | Discrete or continuous | Copied or shared | Instant or over time | Who sees it | What changes / what stays |
|---|---|---|---|---|---|---|
| Databricks boundary | Exact (inside or outside) | Discrete | Holds Unity Catalog, Lakebase and the app; the synced copy is Databricks-managed | Stays | — | Nothing changes; everything is inside |

**Do not.**
- Do not zoom out or pan to reveal the map; the boundary grows, the frame stays.
- Do not use an official logo; "Databricks" and "Lakebase" are set in IBM Plex Sans.
- Do not show a number for the first time here; this beat repeats none.
- Do not widen the claim ("all graph workloads", "replaces graph databases").
- Do not name a graph-database vendor.
- Do not draw the reader grant inside the Unity Catalog frame.
- Do not let the Unity Catalog and Databricks tabs touch.
- Do not add "I work at Databricks".

Claims.md narrator line: Beat 12, with GK-C24 compressed (BRIEF open item 9). 4:5: the map stacks top to bottom (Unity
Catalog, Lakebase, app) inside the boundary at 40, 256, 1000 × 900; headline at 40, 96 in 3 lines; caption band at 40,
1208.

## Local-reference bar fit check

No web source was opened in this pass. The only references are the two attached local images. No other prior capture
was opened, and nothing here describes one.

| Reference | Beat | Ruling for that beat | Fit |
|---|---|---|---|
| `contact-v6.png`: question at frame 0 | 1 | Question at frame 0; dark film | Fits after the ground turns dark and the type goes to 88 px |
| `contact-v6.png`: "Spend $5,000" struck in place | 3 | Strike in place; no number on path 2 | Fits; the strike is a 6 px `now` line that settles grey |
| `contact-v6.png`: "every hop is a copy, a queue and a delay" | 3 | Queues on long spans; latency as length, path 1 only | Fits |
| `contact-v6.png`: pull-back to the seven-system ring | 12 | No camera move | Does not fit as drawn; replaced by the boundary that grows in place |
| `contact-v6.png`: one Postgres database with a table list | 6, 12 | No row grids or schema boxes | Does not fit as drawn; tables are textured cards |
| `v4hf/style-frame.png`: Dr. A in the middle, hop 2 from every hop-1 node, direct hop labels, dashed continuation | 6, 7 | Exact snaps; labels on marks; glossary words | Fits after lime replaces gold, "clinician" replaces "doctor", and edges use 3/6/9 px |
| `v4hf/style-frame.png`: "Lakebase Postgres · 4 CU" corner label | 6 | No corner labels; "4 CU" belongs to the timing graph | Does not fit; removed; "4 CU" appears only in the Frame 8 evidence caption |

Verdict: both references fit after the listed changes. No conflict needs an owner decision.
