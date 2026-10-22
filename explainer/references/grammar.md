# Grammar: mechanism → physical meaning → motion

Worked examples, not law. For anything not listed, ask the six questions in SKILL.md step 2 and reason the same way. Check the mechanism against `~/.claude/docs/lakebase-platform-facts.md` before you draw it.

## Why these choices hold (Bertin's visual variables)

Jacques Bertin (*Semiology of Graphics*, 1967) named the channels a graphic can use: position, size, lightness, texture, colour hue, orientation, and shape. Cleveland & McGill and Mackinlay later ranked them by how accurately people read them.
- **Position** is read most accurately. Use it for the thing that matters most (distance means similarity; left to right means time).
- **Size** shows amount (cost, storage, data volume).
- **Lightness** shows order and emphasis, and survives greyscale. Use it for "lit vs dimmed".
- **Hue** separates kinds, not amounts. One hue per source, product or concept.
- **Texture and shape** separate storage models (see Storage).
- **Motion quality** is our added channel: snap = exact and discrete; flow with easing = approximate and continuous; constant speed = a camera or time passing.

## Search and agents

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| SQL lookup, exact match | A machine reading a grid | A rigid grid. The index jumps straight to the row and the row lights at once. Linear, no easing, no glow. |
| Vector search | Nearness in a space | The query drops into a field of points and rings spread out from it. Points light by distance: bright when near, faint when far. Flag the dimensions ("1,024, shown as 2"). |
| Keyword search (BM25) | A highlighter on paper | A marker wash over the matching words inside the page. Term frequency as small stacked ticks. |
| Hybrid search | Two rankings fused | Two ranked lists zip into one. Each item keeps the colour of the list that ranked it higher. |
| Following a reference | A wire between pages | A straight line snaps from page to page. It is exact, so it never drifts. |
| Agentic rounds | A trail through the corpus | All pages sit faint like a map. Each round lights one page, draws one wire, and adds one clause to the answer in that page's colour. Rounds speed up. |
| Validator / grounding check | Each claim tied to a quote | A thread runs from each claim to its quote in the source. A claim with no quote has a loose thread that drops. That is the visible cause of the next round. |
| Scope lock | Narrowing the corpus | Pages outside the scope dim in place; the boundary closes around the rest. |
| LLM judge / evaluation | A second reader | A different-family reader marks each claim. Agreement shows in one colour, disagreement in another. Same-family agreement is shown as weaker evidence. |
| Vector index build vs query (HNSW) | Building a map, then using it | A build lays down the graph layer by layer over the points, over time. A query is a probe dropped into the finished graph, hopping along its edges toward the nearest points. Never draw a query as building anything. Check the index type first. |
| Pareto trade-off | A taut string over the best points | The string rests on the outer points. Better configurations push it outward; dominated points dim behind it. Moving along the string trades one axis for another. |

## Storage and data movement

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| Postgres / Lakebase tables | Mutable row pages | Modular grid cells (rows). Updates change a cell in place. |
| Delta / Parquet | Immutable columnar files | Vertical stripes (columns). New data adds new files; old files stay until vacuumed. Never draw both as the same cylinder. |
| Lakebase branch | A fork of the database at one point in time (verified: a branch holds the parent's rows, schema and roles at that time, can start at an exact LSN, and is READY in seconds; facts Part 1, "Branching and PITR"). How storage is shared underneath is docs-only. | A new track splits off the parent's timeline at one LSN, in the branch's colour, and is usable at once. It shows the parent's rows as they were at that point; rows the branch writes appear in its colour, and the parent does not change. Do not draw a slow copy job (it is READY in seconds). Do not claim "zero-copy" or shared blocks on screen unless you cite the docs as docs. |
| Write-ahead log (WAL) and LSN | An append-only tape | A horizontal tape of blocks that only grows to the right. A branch or a restore point is a pointer clamped to one position (LSN) on the tape. Check how Lakebase exposes it before naming it on screen. |
| Point-in-time restore | A fork from a past moment | On a timeline, the scrub cursor moves back and a new track splits off there. The live track keeps moving. |
| Synced table (Delta → Lakebase) | A governed mirror | A change in the Delta stripes ripples across to the Lakebase grid. Mode matters: SNAPSHOT is a full redraw; TRIGGERED and CONTINUOUS are ripples. |
| Lakebase CDF (Postgres → Delta) | A change stream into the lake | Row changes leave the grid as small packets and land as new Delta files. |
| Pipeline / ETL / CDC chain | Extra hops, extra copies | Long multi-hop spans with a queue at each hop. Latency is drawn as length. A failure backs up the queue. |

## Governance and access

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| Unity Catalog | One field that everything inside obeys | One boundary around tables, models, indexes and apps. Permission rows that existed per system merge into one set. |
| Row-level security, masks | Rows you may not see | They go dark in place. They do not vanish. The count of hidden rows can show. |
| Synced table from a secured source | A refusal, not a leak | The sync is refused at create; nothing unfiltered is copied (verified: Part 1 of the facts file). Draw the refusal at the boundary. |
| On-behalf-of identity | Your badge travels with the request | The user's identity stays on the request through every hop, and the data read is limited to it. |
| Audit, lineage, MLflow trace | A receipt for every step | Each step leaves a receipt card behind. At the end, the receipts line up as one trail. |

## Compute and cost

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| Autoscaling | Capacity follows load | Compute grows and shrinks with the load line, in step with it. |
| Scale to zero | Nothing runs when idle | Compute dims to nothing. Storage stays. |
| Connection pooling | Many callers, few connections | Many short client lines narrow into a few steady connections before they reach Postgres. Check whether and how Lakebase pools connections before you draw it. |
| Serverless | No servers to manage | Show what the customer no longer handles (boxes leave their side of the line), not a cloud. |
