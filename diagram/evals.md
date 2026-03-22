# Evals: diagram

## Test Inputs

Four inputs at increasing complexity. Input 1 tests positioned layout (Excalidraw) with the Databricks layout spine. Inputs 2-4 test auto-layout formats (Mermaid, PlantUML C4, D2).

### Input 1: Lakebase Agent Memory Architecture (Excalidraw, positioned layout)
Create a Databricks reference architecture diagram showing how Lakebase powers AI agent memory. This is for a customer presentation to enterprise architects evaluating Databricks for agentic AI workloads.

Use Excalidraw (positioned layout required — this diagram has horizontal spanning bars).

Follow Databricks visual standards v3.2.

The architecture has six zones, left to right:

(1) Data Sources — left stack. User interactions, enterprise systems (EHR, CRM, ERP), external APIs.

(2) Agent Runtime — left-center. LangGraph or OpenAI Agents SDK on Databricks Apps. Mosaic AI Model Serving for the foundation model. Agent tools: Unity Catalog Function Calling for tool access, Mosaic AI Vector Search for enterprise knowledge retrieval (RAG over docs, guidelines, policies — this is a tool, not memory). Agent lifecycle: Observe, Reason, Act, Learn.

(3) Lakebase Memory Layer — center, this is the hero. Three memory zones, all scoped to the agent's own interactions:
  - Short-term: conversation checkpoints, session state, tool history. By thread_id.
  - Long-term: user profiles, preferences, cross-session insights. JSONB lookups.
  - Semantic (pgvector): agent's own past interaction embeddings. Episodic recall, resolution patterns. NOT enterprise knowledge.

(4) Lakehouse Feedback Loop — below center. Agent data auto-syncs to Delta tables. Feeds: Agent Evaluation (Mosaic AI), model fine-tuning, analytics and observability (Databricks SQL).

(5) Governance — full-width foundation bar at the bottom. Unity Catalog. Access control, PII masking, lineage, audit trail.

(6) Agent Surfaces — right stack. Databricks Apps (Streamlit/chat), AI/BI Genie, Slack/Teams/portals, MLflow for tracing.

Numbered flow steps. All arrows labeled. Databricks product names throughout. Governance spans the full width as a structural bar, not a node.

### Input 2: Medallion architecture for a retail customer (Mermaid, auto-layout)
Create a diagram showing a medallion architecture for a retail company. They have data coming from Shopify (orders), Stripe (payments), and Snowplow (clickstream). Show the bronze-silver-gold layers flowing into Databricks SQL and a Tableau dashboard. This is for a customer presentation. Use Mermaid format.

### Input 3: C4 container diagram for a compliance review (PlantUML C4, auto-layout)
Create a C4 container diagram for a healthcare data platform. The audience is a compliance officer and a CISO doing a security review. They need to see where PHI enters the system, where it's masked, and how access is governed. The platform uses Databricks with Unity Catalog, Lakeflow Jobs, and an S3 data lake. External systems are Epic EHR and a clinical trials portal. Use PlantUML C4 format.

### Input 4: Complex event-driven architecture (D2, auto-layout stress test)
Diagram an event-driven analytics platform for a large insurance company. Sources: claims processing system, underwriting engine, agent portal, customer mobile app, third-party weather API, and a fraud detection service. Data flows through Kafka into Databricks with bronze/silver/gold layers. Gold serves three consumers: a real-time fraud scoring API (via Mosaic AI Model Serving), an actuarial reporting warehouse (Databricks SQL → Tableau), and a regulatory submission pipeline that exports to a secure FTP for state regulators. Show Unity Catalog governing everything. Use D2 format. This is for an enterprise architect audience doing a design review.

---

## Binary Evals

Answer YES or NO for each. Score = count(YES) / total.

Evals are split into **universal** (apply to all inputs) and **Input 1 only** (Lakebase-specific). For Input 1 evals scored against Inputs 2-4, automatically score YES (the eval doesn't apply).

---

### Universal Evals (all inputs)

### E1: Format matches request
Did the output use the format specified in the input? (Input 1 → Excalidraw. Input 2 → Mermaid. Input 3 → PlantUML C4. Input 4 → D2.) Scores NO if the output uses a different format than requested.
Example YES: Input 1 uses Excalidraw API calls or describes positioned Excalidraw elements. Input 3 produces PlantUML with `!include <C4/C4_Container>` and `Container()` macros.
Example NO: Input 1 produces a Mermaid flowchart instead of Excalidraw. Input 3 produces D2 instead of PlantUML C4.

### E2: Every arrow has a text label
Does every connection/arrow in the diagram have a text label describing what flows through it? Check ALL arrows — a single unlabeled arrow scores NO.
Example YES: `Rel(sources, dlt, "Ingest", "Auto Loader")`, `A -->|CDC events| B`, `sources.erp -> ingestion.dms: CDC`, Excalidraw arrows with text labels
Example NO: `A --> B` with no label, bare arrows with no description, `Rel(a, b, "")` with empty string

### E3: Governance is structural, not a peer node
Is Unity Catalog / Governance represented as a structural element — either a full-width foundation bar at the bottom or an overarching header spanning the platform — rather than as a regular box among other nodes? Scores NO if governance appears as a sibling node next to other processing components.
Example YES: A dedicated governance bar spanning the platform width, dark fill, visually distinct from content nodes
Example NO: `uc: Unity Catalog` placed inside the platform container as a peer of other components

### E4: Left-to-right primary flow direction
Does the diagram use a left-to-right primary flow for data movement? Sources should be on the left, consumers on the right. Scores NO if the primary data flow goes top-to-bottom or right-to-left.
Example YES: `flowchart LR`, `direction: right`, Excalidraw with sources placed at left edge and consumers at right edge
Example NO: `flowchart TD` for a data pipeline, or sources placed on top with consumers at the bottom

### E5: Databricks product names used (not generic terms)
Does the diagram use official Databricks product names instead of generic terms? At least 4 of these must appear: Unity Catalog, Lakeflow Jobs / Delta Live Tables, Databricks SQL, Mosaic AI, Auto Loader, Lakebase, Databricks Apps, AI/BI Genie.
Example YES: Nodes labeled "Unity Catalog", "Mosaic AI Model Serving", "Databricks SQL", "Lakebase"
Example NO: Nodes labeled "Governance Layer", "ETL Pipeline", "SQL Warehouse", "Postgres Database"

### E6: Logical grouping with zones or subgraphs
Are related components grouped into zones, subgraphs, system boundaries, or containers? Sources should be grouped, platform components should be bounded, consumers should be grouped. Scores NO if all nodes are flat/ungrouped.
Example YES: `subgraph sources["Data Sources"]`, `System_Boundary(platform, "...")`, D2 nested containers, Excalidraw rectangles grouping related elements
Example NO: All nodes at the same level with no grouping — flat list of nodes

### E7: Diagram has a title
Does the diagram have a title — either via format-native title syntax (`title` in PlantUML, Mermaid title frontmatter, D2 top-level label), a markdown heading above the code block, or an Excalidraw title element?
Example YES: `title Data Intelligence Platform — Container Diagram`, or `## Lakebase Agent Memory Architecture` above the output
Example NO: Diagram starts with no title, heading, or identifying label

### E8: Audience-appropriate depth
Is the level of technical detail appropriate for the stated audience? Customer presentations and compliance reviews should show systems, data flows, and governance — not Spark configs or cluster settings. Engineering design reviews should show specific technologies, protocols, and data formats.
Example YES: Input 3 (compliance audience) emphasizes PHI flow paths, masking points, and access control boundaries
Example NO: Input 3 shows cluster autoscaling settings and Spark shuffle partition counts to a compliance officer

---

### Input 1 Only — Lakebase Agent Memory (score YES automatically for Inputs 2-4)

### E9: Six zones present
Does the diagram contain all six architectural zones: data sources, agent runtime, Lakebase memory layer, lakehouse feedback loop, governance bar, and agent surfaces/consumers? All six must be identifiable. Missing any one scores NO.
Example YES: All six zones clearly bounded and labeled
Example NO: Feedback loop missing, or governance absent

### E10: Lakebase memory has three distinct types
Does the Lakebase zone show three separate memory types (short-term, long-term, semantic/pgvector) with descriptions of what each stores? Generic labels like "Memory 1, Memory 2" score NO.
Example YES: "Short-term — conversation checkpoints by thread_id", "Long-term — user profiles, JSONB", "Semantic — agent past interaction embeddings"
Example NO: Single "Lakebase" box with no memory type breakdown, or types present but no descriptions

### E11: Vector Search is a tool, not memory
Is Mosaic AI Vector Search positioned as an agent tool (alongside Function Calling, inside or adjacent to the agent runtime) rather than inside the Lakebase memory layer? The diagram must visually separate enterprise knowledge retrieval from agent memory.
Example YES: Vector Search in the agent tools zone, labeled as enterprise knowledge/RAG
Example NO: Vector Search inside the Lakebase container, or visually grouped with the three memory types

### E12: Feedback loop connects memory to analytics
Does the diagram show a path from the Lakebase memory layer to analytical workloads (evaluation, fine-tuning, or observability) via Delta tables or a lakehouse sync? The feedback loop is what closes the learning cycle.
Example YES: Arrow from Lakebase to Delta tables, then to Agent Evaluation and/or model fine-tuning
Example NO: Lakebase is a dead end with no path back to the analytical or training layer

---

### Input 2 Only — Medallion Retail (score YES automatically for Inputs 1, 3, 4)

### E13: Medallion layers have descriptive labels
Does each medallion tier (Bronze, Silver, Gold) include a description of what data it contains for this specific retail use case — not just the generic tier name?
Example YES: "Bronze — Raw Shopify orders, Stripe transactions, Snowplow clickstream events"
Example NO: "Bronze (Raw)", "Silver (Cleaned)", "Gold (Analytics)" with no use-case-specific content

---

### Input 4 Only — Insurance Stress Test (score YES automatically for Inputs 1, 2, 3)

### E14: Node count manageable (≤20 top-level nodes)
Does the diagram contain 20 or fewer top-level nodes (not counting sub-elements within subgraphs/containers)? If the system requires more, was it decomposed into multiple diagrams? Especially relevant for Input 4 which has many components.
Example YES: 14 nodes across 4-5 subgroups
Example NO: 25+ nodes crammed into one diagram with no grouping
