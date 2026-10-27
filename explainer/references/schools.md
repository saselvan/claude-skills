# Schools, creators and moves

Pick 2 or 3 per piece, by theme. For each, say exactly what you borrow. Descriptions from another model are leads; look at the real piece before you copy a move.

## Which look for which job

- **The paper language** (paper ground, 1 px grey lines, one highlight, strike-through corrections, panels that grow in place) for architecture: layouts, pipeline boundaries, schemas, before and after. Its roots are Tufte, the Swiss grid and Distill; Ciechanowski, Red Blob Games and Hrishi Olickel's talks are examples.
- **The math language** (coordinate spaces, vector offsets, a setting tied to a live result) only when the camera goes inside the math: vector space, distances, dot products, Pareto frontiers. 3Blue1Brown is the best-known example; Ciechanowski does the same for physical mechanisms.
- One piece can use both: the paper layout holds the story, and a math inset opens when the math matters, then closes.
- Never credit one person or one video as "the" style. Name the tradition, then cite examples.

## Schools

| School | People and works | What to borrow |
|---|---|---|
| Information design | Edward Tufte: *Envisioning Information*, *Beautiful Evidence* | Cut marks that carry no data. Labels and notes on the picture, not in a legend. Small multiples. |
| Visual variables | Jacques Bertin, *Semiology of Graphics*; Cleveland & McGill; Jock Mackinlay | Pick the channel by what it must show: position for the main quantity, lightness for order, hue for kinds. |
| Swiss / International Typographic Style | Josef Müller-Brockmann, *Grid Systems* | Strict grid, a lot of empty space, type that does the work. |
| Explorable explanations | Bret Victor: *Up and Down the Ladder of Abstraction*, *Explorable Explanations*; Nicky Case | Learn by turning a real knob. Move between the concrete case and the abstract system. |
| Interactive technical essays | Distill.pub (Chris Olah, Shan Carter) | Thin-line figures inside the text that the reader can play with. |
| Mechanism essays | Bartosz Ciechanowski (ciechanow.ski: e.g. *Mechanical Watch*, *GPS*, *Internal Combustion Engine*) | One mechanism, taken apart step by step, with a live figure at every step. The closest match to "show how it works" for an architect. |
| Algorithm explorables | Red Blob Games (Amit Patel), e.g. its A* and hexagonal-grid guides | Algorithms you watch run on a grid, with real settings. Strong for search, graphs and indexes. |
| Sketch thinking | Dan Roam, *The Back of the Napkin*; Maggie Appleton | Built-up-while-I-talk drawings. Reads as thinking, not marketing. |
| Newsroom graphics | NYT graphics (Amanda Cox, Mike Bostock), The Pudding, The Economist | The headline states the finding. The story unfolds as you scroll. Direct labels. One chart, one message. |
| Information is Beautiful | David McCandless; informationisbeautiful.net (topics such as Tech & Digital, Ideas & Perception) | One big comparison you get in 5 seconds. Search the site by the piece's theme for layouts to borrow. |

## By mechanism (survey checked 2026-10-20)

Source: `/Users/samuel.selvan/src/lakebase-agentic-search/explainer-references-survey.md`. Every URL below returned 200, and its page text holds the words the claim depends on (curl and grep). JS-only pages (marked JS) were checked only for "it loads". No moment was checked by eye. Open the piece before you copy a move, and never copy a number from it.

| Mechanism | Work | Move to borrow | Fit |
|---|---|---|---|
| B-tree lookup | [Ben Dicken, *B-trees and database indexes*](https://planetscale.com/blog/btrees-and-database-indexes) (PlanetScale, 2024) | The probe visits one node per level; every page it does not read stays dim. | Motion |
| Copy-on-write branch | [Xata, *Branching*](https://xata.io/docs/core-concepts/branching) | Fork the metadata first; peel off a private copy of a block only when a branch writes it. Shared blocks stay drawn once. | Stills |
| PITR / timelines | [Hironobu Suzuki, *Internals of PostgreSQL* 10.3](https://www.interdb.jp/pg/pgsql10/03.html), Figure 10.6 | Recovery is a route through WAL history; the LSN is the junction where a new timeline starts. | Stills |
| MVCC visibility | [Bruce Momjian, *MVCC Unmasked*](https://momjian.us/main/writings/pgsql/mvcc.pdf) | Freeze one snapshot beside the tuple headers; visibility is a lookup. | Stills |
| HNSW search | [Sushant Lokhande, *HNSW Lab*](https://sushantlokhande14.github.io/hnsw-lab/) (JS; [source](https://github.com/sushantlokhande14/hnsw-lab)) | The probe hops along graph edges, drops a layer, and keeps its candidate frontier visible. | Motion |
| Hybrid search / RRF | [Sachin Gupta, *Hybrid Search*](https://www.guptasachinn.com/writing/hybrid-search) | Both ranked lists stay fixed while shared items rise in a third, fused list by `1/(k+rank)`. Our served search does not use RRF: both endpoints use a fixed weighted sum, 0.75 dense + 0.25 BM25 (`search/agent_tool.py:56-80`, `search/retail_dnb_live.py:59-62` at reference-package `92cf68ed`). Draw that as two scores added with fixed weights, not as rank fusion. | Motion |
| Embeddings | [Smilkov et al., *Embedding Projector*](https://projector.tensorflow.org/) ([paper](https://ar5iv.labs.arxiv.org/html/1611.05469)) | The 2D projection moves, but the neighbour list comes from the full space. That is "1,024 dimensions, shown as 3", made honest. | Motion |
| Agent loop with citations | [OpenAI, *WebGPT answer viewer*](https://openaipublic.blob.core.windows.net/webgpt-answer-viewer/index.html) (JS; [article](https://openai.com/index/webgpt/)) | The evidence highlight moves with each recorded browser state; claim-to-source numbers never change. | Replay |
| Agent loop, events | [Wenhao Yu, *How AI reads the web*](https://wenhaoyu-bryan.github.io/agent-anatomy/episodes/how-ai-reads-the-web/) (JS; [repo](https://github.com/wenhaoyu-bryan/agent-anatomy)) | Search, read, reject, check and cite on one scrubbable lane. The run is scripted ("real(istic)" in its README); copy the layout, not the claim. | Replay |
| Reason-act trace | [Yao et al., *ReAct*](https://react-lm.github.io/) | Each search sits beside the observation that causes the next action. | Stills |
| Queues and backlog | [Sam Rose, *Queueing*](https://encore.dev/blog/queueing) (Encore, 2024) | Arrivals pile up behind a visibly busy worker; delay, timeout, reorder and drop each look different. Use it for the "backed up" sync queue. | Motion |
| Consumer lag | [SoftwareMill, *Kafka Visualization*](https://softwaremill.com/kafka-visualisation/) (JS) | The append-only log runs ahead of a slow consumer, and its offset stays behind in place. Nothing is moved or deleted. | Motion |
| Backpressure | [Piotr Nowojski, *Source of backpressure*](https://flink.apache.org/2021/07/07/how-to-identify-the-source-of-backpressure/) (Apache Flink, 2021) | Pressure runs opposite to the data: the blocked upstream is black, and the first busy task downstream is red. | Motion |
| CDC | [Martin Kleppmann, *Logs for data infrastructure*](https://martin.kleppmann.com/2015/05/27/logs-for-data-infrastructure.html) | Each committed change becomes one ordered event, and each store reads it at its own offset. | Stills |
| Permissions | [AuthZed, *SpiceDB Playground*](https://play.authzed.com/) (JS; [post](https://authzed.com/blog/spicedb-playground-update)) | One set of relations drives the graph, the checks and the real allow or deny result. | Live |
| Column masking | [Snowflake, *Dynamic Data Masking* demo](https://www.snowflake.com/en/resources/video/dynamic-data-masking-artin-avanes/) | Hold the query and the role fixed; only the policy changes the cells. | Video |
| Row filter | [Microsoft, *Row-level security*](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security) | The full table sits beside the filtered result, and the identity under test is labelled ("Now viewing as"). | Stills |
| Scale to zero | [Fly.io, *Autoscale to zero*](https://autoscale-to-zero-demo.fly.dev/) | The process announces its own deadline, disappears, and the next request wakes it. | Live |
| Scale from zero | [Knative, *Autoscaling system*](https://raw.githubusercontent.com/knative/serving/d7bea3390c9fca2713c05b3bbd83690d430c7cfc/docs/scaling/SYSTEM.md) | The request waits at the Activator until the new pod is ready. Draw the wait. | Stills |

"Stills" means the states are right but the change is not animated: borrow the states and add the motion from `grammar.md`.

### Warnings (pieces that teach the mechanism wrong)

- [*PostgreSQL MVCC Visualized*](https://boringsql.com/visualizers/mvcc/) takes the Repeatable Read snapshot at `BEGIN`. PostgreSQL takes it at the first non-transaction-control statement ([docs](https://www.postgresql.org/docs/current/transaction-iso.html), checked).
- [*Serverless Visually Explained*](https://serverless-visually-explained.com/) shows scale-out as instant, which hides concurrency limits, bursts and cold starts ([AWS](https://aws.amazon.com/blogs/compute/operating-lambda-application-design-scaling-and-concurrency-part-2/)). JS page: the quote was not re-checked.
- [*SystemBlocks: Serverless Cold Starts*](https://systemblocks.dev/learn/serverless-scaling) merges Lambda MicroVMs with Knative pods. JS page: not re-checked.
- Tropes that misteach (a second survey, `Downloads/explainer_references_survey.md`): a B-tree drawn as a deep binary tree hides its fan-out; CDC drawn as a batch table copy hides the log; HNSW drawn as flat clusters hides its layers; scale-out drawn as an instant clone hides cold start. For agent loops, that survey says "draw a cycle, not a flowchart". Here the fix is a trail that grows, never a circle (see "Show progress, not repetition").

### Leads only (do not cite yet)

From the second survey. Its pages load, but it gives no second sources (only "widely cited" claims), and one claim is wrong:
- David Galles, [*B-Tree Visualization*](https://www.cs.usfca.edu/~galles/visualization/BTree.html); Ben Johnson, [*The Secret Lives of Data: Raft*](http://thesecretlivesofdata.com/raft/); Pinecone, [*HNSW*](https://www.pinecone.io/learn/series/faiss/hnsw/); Jay Alammar, [*The Illustrated Word2vec*](https://jalammar.github.io/illustrated-word2vec/); Tyler Akidau, [*Streaming 102*](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-102/); Auth0, [*Zanzibar Academy*](https://zanzibar.academy/); Zack Bloom, [*Cloud Computing without Containers*](https://blog.cloudflare.com/cloud-computing-without-containers/) (Cloudflare).
- Excluded: the "LangGraph animated DAG on the landing page" claim. That page now redirects to `docs.langchain.com`, and no such animation was found.

## Outside technology (leads, 2026-10-21; "check" until someone opens the real work)

The owner's words: "if there are folks outside of technology like other visual artists … then so be it. Thinking outside the box never hurts."

| Who | What to borrow | Good for |
|---|---|---|
| Kogonada (video essays on Ozu, Kubrick, Wes Anderson; director of *Columbus*, 2017), and Ozu before him (check) | A still frame; things move inside it; frames within frames; long, calm holds | Pacing, holds, comfort without boredom |
| Saul Bass (film title sequences) (check) | One simple shape turns into the next; the shape is the story | Openings; one object becoming the next |
| Harry Beck (London Tube map), Massimo Vignelli (NYC subway map) (check) | Show how things connect, not where they are | Graphs, networks, system maps |
| Charles and Ray Eames, *Powers of Ten* (check) | From one case to the whole system in one unbroken move | The pull-back, done as growth in place |
| Every Frame a Painting (Tony Zhou, Taylor Ramos) (check) | When to cut, when to hold, how a cut carries meaning | Beat order and timing |
| Dieter Rams, Otl Aicher (check) | "Less, but better"; one strict system of signs | Restraint; symbols and labels |

## Creators (leads from the owner, 2026-10-20)

| Creator | Toolchain | Signature move | Good for |
|---|---|---|---|
| 3Blue1Brown | Manim (Python) | Continuous geometric transformations | State spaces, vectors, embeddings |
| Branch Education | Blender / 3D | Zooming through physical scale, following data through hardware | Memory hierarchies, storage, networks |
| Reducible | Manim | Step-by-step state machines | Algorithms, caching, concurrency, data structures |
| Freya Holmér | Unity, custom tools | Interactive parameter sweeps | Spatial math, transforms, pipelines |
| Ordinary Folk | After Effects / Cinema 4D | Strict colour-coded structure and pacing | Platform overviews, enterprise systems |

## Moves seen in 3Blue1Brown, *Transformers* (Deep Learning ch. 5)

Seen in frames: the opening example sentence ("To date, the cleverest thinker of all time was ___"); "The Truth" vs "A Convenient Lie" (tokens vs words); vector arithmetic (king − man + woman ≈ queen) on 3D axes; temperature 0 vs 5 side by side; the GPT-3 weight count organised into matrices; a chapter map of the series.

- **Input and output before the inside.** Show what goes in and what comes out, then open the box.
- **Follow the data.** One token, one vector, through every step.
- **Flag the convenient lie.**
- **One colour per idea, across every formula and chart.**
- **A setting tied to a visible result** (temperature reshapes the bars), then the extremes side by side.
- **A big number made physical** (a wall of matrices you can count).
- **A chapter map** to say where you are in the whole.

## Moves seen in one example of the paper language: Hrishi Olickel, *Just-in-Time Ontologies* (AI Engineer)

Seen in frames: light paper ground; thin grey 1 px lines; one mint marker-wash highlight per frame; numbered panels that grow in place (1 Source, 2 Storage, 3 Decision); a sentence struck through in place ("…transformation is expensive"); a chapter map with 4 thumbnails, one labelled "Pareto surfing"; a thin chapter progress line at the bottom; a real schema (`Customer`) after the sketch. The talk opens on a failure: stripped minus signs turned a net $784,000 into $5.3 million of debt, and several models agreed on the wrong answer.

- **Open on a concrete failure.**
- **Grow one diagram in place.**
- **One highlight per frame; everything else stays grey.**
- **Strike through the old belief in place**, then write the new one.
- **End on a real artifact** (a schema, a log, a receipt).
- **A thin progress line** for where you are in the talk.
- **Pareto surfing:** show cost, speed and accuracy as a frontier you move along, not a single winner.
