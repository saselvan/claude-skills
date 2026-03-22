# Evals: diagram

## Test Inputs

Three inputs at increasing complexity. All are Databricks-facing to test the visual standards. Input 1 is a happy-path medallion. Input 2 forces C4 format and compliance audience. Input 3 is a stress test with high node count and multiple consumer paths.

### Input 1: Medallion architecture for a retail customer
Create a diagram showing a medallion architecture for a retail company. They have data coming from Shopify (orders), Stripe (payments), and Snowplow (clickstream). Show the bronze-silver-gold layers flowing into Databricks SQL and a Tableau dashboard. This is for a customer presentation. Use Mermaid format.

### Input 2: C4 container diagram for a compliance review
Create a C4 container diagram for a healthcare data platform. The audience is a compliance officer and a CISO doing a security review. They need to see where PHI enters the system, where it's masked, and how access is governed. The platform uses Databricks with Unity Catalog, Lakeflow Jobs, and an S3 data lake. External systems are Epic EHR and a clinical trials portal. Use PlantUML C4 format.

### Input 3: Complex event-driven architecture (stress test)
Diagram an event-driven analytics platform for a large insurance company. Sources: claims processing system, underwriting engine, agent portal, customer mobile app, third-party weather API, and a fraud detection service. Data flows through Kafka into Databricks with bronze/silver/gold layers. Gold serves three consumers: a real-time fraud scoring API (via Mosaic AI Model Serving), an actuarial reporting warehouse (Databricks SQL → Tableau), and a regulatory submission pipeline that exports to a secure FTP for state regulators. Show Unity Catalog governing everything. Use D2 format. This is for an enterprise architect audience doing a design review.

---

## Binary Evals

Answer YES or NO for each. Score = count(YES) / total.

### E1: Valid syntax
Does the diagram source code use valid syntax for the declared format? (Mermaid flowchart syntax for Mermaid, PlantUML with `!include <C4/C4_Container>` for C4, D2 syntax for D2.) A diagram with syntax errors that would fail to render scores NO.
Example YES: Well-formed `flowchart LR` with proper arrow syntax `A -->|label| B`, or valid D2 with `direction: right` and proper connection syntax
Example NO: Mixed Mermaid and D2 syntax, missing `@startuml`/`@enduml`, unclosed subgraphs, invalid arrow operators

### E2: Format matches request
Did the output use the format specified in the input? (Input 1 → Mermaid. Input 2 → PlantUML C4. Input 3 → D2.) Scores NO if the output uses a different format than requested.
Example YES: Input 2 produces PlantUML with `!include <C4/C4_Container>` and `Container()` macros
Example NO: Input 2 produces a Mermaid flowchart or D2 instead of PlantUML C4

### E3: Every arrow has a text label
Does every connection/arrow in the diagram have a text label describing what flows through it? Check ALL arrows — a single unlabeled arrow scores NO.
Example YES: `Rel(sources, dlt, "Ingest", "Auto Loader")`, `A -->|CDC events| B`, `sources.erp -> ingestion.dms: CDC`
Example NO: `A --> B` with no label, `sources -> ingestion` with no description, `Rel(a, b, "")` with empty string

### E4: Governance is structural, not a peer node
Is Unity Catalog / Governance represented as a structural element — either a full-width foundation bar at the bottom or an overarching header spanning the platform — rather than as a regular box among other nodes? Scores NO if governance appears as a sibling node next to Bronze/Silver/Gold or other processing components.
Example YES: A dedicated governance bar with dark fill spanning the platform width, or a `System_Boundary` wrapper labeled "Governance"
Example NO: `uc: Unity Catalog` placed inside the platform container as a peer of Bronze, Silver, Gold

### E5: Medallion layers have descriptive labels
Does each medallion tier (Bronze, Silver, Gold) include a description of what data it contains for this specific use case — not just the generic tier name? The label must say what's IN the layer.
Example YES: "Bronze — Raw Shopify orders, Stripe transactions, Snowplow clickstream events" or "Silver — Deduplicated orders joined with payment status"
Example NO: "Bronze (Raw)", "Silver (Cleaned)", "Gold (Analytics)" with no use-case-specific content description

### E6: Databricks product names used (not generic terms)
Does the diagram use official Databricks product names instead of generic terms? Check for: Unity Catalog (not "data catalog"), Lakeflow Jobs or Delta Live Tables (not "ETL pipelines"), Databricks SQL (not "data warehouse"), Mosaic AI (not "ML platform"), Auto Loader (not "data ingestion").
Example YES: Nodes labeled "Unity Catalog", "Lakeflow Jobs", "Databricks SQL", "Mosaic AI"
Example NO: Nodes labeled "Governance Layer", "ETL Pipeline", "SQL Warehouse", "ML Platform"

### E7: Left-to-right primary flow direction
Does the diagram use a left-to-right primary flow for data movement? Sources should be on the left, consumers on the right. The layout declaration should be `flowchart LR`, `direction: right`, or equivalent. Scores NO if the primary data flow goes top-to-bottom or right-to-left.
Example YES: `flowchart LR`, `direction: right`, or C4 diagrams with sources on left flowing right to consumers
Example NO: `flowchart TD` for a data pipeline, or sources placed on top with consumers at the bottom

### E8: Subgraphs used for logical grouping
Are related components grouped into subgraphs, system boundaries, or containers? Sources should be grouped, platform components should be bounded, consumers should be grouped. Scores NO if all nodes are flat/ungrouped.
Example YES: `subgraph sources["Data Sources"]`, `System_Boundary(platform, "Data Intelligence Platform")`, D2 nested containers
Example NO: All nodes at the same level with no grouping — flat list of 20+ nodes

### E9: Color palette is consistent and semantic
If colors are applied, do they follow a consistent semantic scheme? Bronze/Silver/Gold for medallion layers, dark fill for governance, and distinct colors for different functional zones. Scores NO if colors are random, absent when the diagram warrants them, or if the same color is used for unrelated purposes.
Example YES: Bronze=#CD7F32, Silver=#C0C0C0, Gold=#FFD700, governance uses dark teal, processing uses a consistent accent color
Example NO: All nodes the same default color, or random colors with no semantic pattern

### E10: Diagram has a title
Does the diagram have a title — either via format-native title syntax (`title` in PlantUML, Mermaid title frontmatter, D2 top-level label) or a markdown heading immediately above the code block?
Example YES: `title Data Intelligence Platform — Container Diagram` inside PlantUML, or `## Retail Medallion Architecture` above the code block
Example NO: Diagram code starts with no title, heading, or identifying label

### E11: Audience-appropriate depth
Is the level of technical detail appropriate for the stated audience? Customer presentations and compliance reviews should show systems, data flows, and governance — not Spark configs or cluster settings. Engineering design reviews should show specific technologies, protocols, and data formats.
Example YES: Input 2 (compliance audience) emphasizes PHI flow paths, masking points, and access control boundaries — not DLT pipeline implementation details
Example NO: Input 2 shows cluster autoscaling settings and Spark shuffle partition counts to a compliance officer

### E12: Node count manageable (≤20 top-level nodes per diagram)
Does the diagram contain 20 or fewer top-level nodes (not counting sub-elements within subgraphs/containers)? If the system requires more, was it decomposed into multiple diagrams or C4 levels? Especially relevant for Input 3 which has many components.
Example YES: 14 nodes across 4-5 subgroups, or complex system split into Context + Container diagrams
Example NO: 25+ nodes crammed into one diagram with no grouping
