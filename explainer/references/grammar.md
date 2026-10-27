# Grammar: mechanism → physical meaning → motion

Worked examples, not law. For anything not listed, ask the six questions (SKILL.md, phase 0, step 2) and reason the
same way. Check the mechanism against the domain facts file before you draw it. Platform-specific rows live in
`domains/<domain>.md`; this file holds the kinds of thing any system is made of.

## Why these choices hold (Bertin's visual variables)

Position is read most accurately: use it for what matters most (distance means similarity; left to right means
time). Size shows amount. Lightness shows order and emphasis and survives greyscale: use it for lit vs dimmed. Hue
separates kinds, never amounts: one hue per source, product or concept. Texture and shape separate storage models.
Motion quality is the added channel: snap = exact and discrete; flow with easing = approximate and continuous; constant
speed = a camera or time passing.

## Lookup, search and inference

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| Exact lookup (key, index, hash) | A machine reading a grid | A rigid grid. The pointer goes straight to the row and the row lights on one frame. Linear travel, no easing on the hit, no glow. |
| Nearness search (vectors, geo, fuzzy) | Distance in a space | The query drops in and rings spread. Points light by distance: bright near, faint far. Flag the dimensions ("1,024, shown as 2"). |
| Term match (keyword, BM25) | A highlighter on paper | A marker wash over the matching words inside the page. Frequency as small stacked ticks. |
| Fused ranking (hybrid) | Two rankings combined | Two ranked lists zip into one; each item keeps the colour of the list that ranked it higher. If the real fusion is a weighted sum, draw two scores added, not rank fusion. |
| Following a reference (join, pointer, link) | A wire between pages | A straight line snaps from page to page. Exact, so it never drifts. |
| Iterative rounds (agent loop, retry) | A trail through the corpus | All pages sit faint like a map. Each round lights one page, draws one wire, adds one clause in that page's colour. Rounds speed up. Never a circle. |
| Check against evidence (grounding, validation) | Each claim tied to its source | A thread from claim to quote. A claim with no quote has a loose thread that points forward to where the answer is; that is the visible cause of the next round. |
| Scope lock | Narrowing the set | Things outside dim in place; the boundary closes around the rest. |
| Second-reader judgement | Another reader marks the work | A different-family reader marks each claim; agreement in one colour, disagreement in another. |
| Index build vs query (graph indexes) | Building a map, then using it | The build lays the graph down layer by layer, over time. A query is a probe hopping along edges toward the nearest points. Never draw a query as building anything. |
| Trade-off frontier (Pareto) | A taut string over the best points | The string rests on the outer points; better configurations push it out; dominated points dim behind it. |

## Storage and data movement

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| Mutable rows | Pages of rows that change in place | A modular grid of cells; an update changes a cell where it is. |
| Immutable files (columnar) | Files that are added, never edited | Vertical stripes; new data adds stripes; old ones stay until compaction. Never the same cylinder as mutable rows. |
| Append-only log | A tape that only grows | A horizontal tape growing right. A position on it (an offset, an LSN) is a pointer clamped to one spot. |
| Fork at a point in time (branch, snapshot) | A new track from one position on the tape | A track splits off at one position in its own colour and is usable at once. It shows the parent as it was; its own writes appear in its colour; the parent does not change. Draw a slow copy only if the system really copies. Claim shared storage only if the docs say so. |
| Restore to a past moment | A fork from the past | The cursor moves back; a new track splits off there; the live track keeps moving. |
| Mirror (sync, replica) | A governed copy that follows a source | A change ripples from source to copy. Mode matters: full redraw, triggered ripple, continuous ripple. |
| Change stream (CDC, CDF) | Changes leaving as packets | Row changes leave the grid as small packets and land as new files. |
| Pipeline (ETL, hop chain) | Extra hops, extra copies | Long multi-hop spans with a queue at each hop. Latency is drawn as length. A failure backs a queue up; show what is stale downstream, with a label. |
| Cache | A nearer, smaller copy that can be wrong | A small grid beside the caller; a hit lights it; a miss travels past it to the source; staleness is a dim overlay with its age. |
| Partition / shard | The same shape, cut into pieces | One grid cut along lines; a key routes to one piece; a hot piece lights brighter than the rest. |

## Access and governance

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| One governance boundary | A field everything inside obeys | One boundary around every object; permission rows that existed per system merge into one set. |
| Row filters and masks | Rows or cells you may not see | They go dark in place; they do not vanish; the hidden count can show. |
| Refusal at a boundary | A copy that is not allowed to happen | The sync or read is refused at the line; nothing crosses. Draw the refusal, not a leak. |
| Identity travelling with a request | A badge on the request | The caller's identity rides every hop and the data read is limited to it. |
| Receipts (audit, lineage, trace) | A card left behind at every step | Each step leaves a receipt; at the end the receipts line up as one trail. Receipts come at the end, not on every frame. |
| Encryption in transit / at rest | A sealed envelope; a locked store | The envelope seals before it leaves; the store's cells are unreadable until a key arrives. No padlock icons. |

## Compute, cost and failure

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| Autoscaling | Capacity follows load | Compute grows and shrinks with the load line, in step. |
| Scale to zero and cold start | Nothing runs when idle; the first request waits | Compute dims to nothing; storage stays. The next request waits at the gate until compute is back: draw the wait. |
| Connection pooling | Many callers, few connections | Many short client lines narrow into a few steady ones before the database. |
| Serverless | Nothing to run yourself | Boxes leave the customer's side of the line. Not a cloud. |
| Backpressure | The slow stage is felt upstream | Pressure runs opposite to the data: the blocked upstream darkens; the first busy stage downstream is the cause and is lit. |
| Retry and idempotency | The same request again, with the same result | The second arrow lands on the same cell and changes nothing; a non-idempotent retry adds a wrong duplicate in the warning colour. |
| Timeout and circuit breaker | A clock on a call; a switch that opens | A thin timer along the call; when it runs out the call drops; the breaker opens and later calls stop at it. |
| Consensus / quorum | Most members agree before a write counts | A write fans to members; it commits when the quorum lights; a lagging member catches up from the log afterwards. |
| Durable execution (workflow engine) | Every step's result written down before the next | Each step leaves a saved card; after a crash the run resumes from the last card, replaying nothing above it. |

## Writing the row

For each beat the storyboard names: the mechanism, its physical meaning, the visual variable that carries it
(position, size, lightness, hue, shape, motion quality), what is lit vs dimmed, and the one element that changes.
If two of these are missing, the beat is not designed yet.
