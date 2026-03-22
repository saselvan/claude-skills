# Evals: diagram

## Test Inputs

Three inputs at increasing complexity. Input 1 is a happy-path Databricks diagram. Input 2 forces format selection and audience adaptation. Input 3 is a stress test with high node count and multiple concerns.

### Input 1: Medallion architecture for a new customer
Create a diagram showing a medallion architecture for a retail company. They have data coming from Shopify (orders), Stripe (payments), and Snowplow (clickstream). Show the bronze-silver-gold layers flowing into Databricks SQL and a Tableau dashboard. Use Mermaid format.

### Input 2: C4 container diagram for a compliance audience
Create a C4 container diagram for a healthcare data platform. The audience is a compliance officer and a CISO doing a security review. They need to see where PHI enters the system, where it's masked, and how access is governed. The platform uses Databricks with Unity Catalog, DLT, and an S3 data lake. External systems are Epic EHR and a clinical trials portal. Use PlantUML C4 format.

### Input 3: Complex event-driven architecture (stress test)
Diagram an event-driven analytics platform for a large insurance company. Sources: claims processing system, underwriting engine, agent portal, customer mobile app, third-party weather API, and a fraud detection service. Data flows through Kafka into Databricks with bronze/silver/gold layers. Gold serves three consumers: a real-time fraud scoring API (via model serving), an actuarial reporting warehouse (Databricks SQL → Tableau), and a regulatory submission pipeline that exports to a secure FTP for state regulators. Show Unity Catalog governing everything. Use D2 format. This is for an enterprise architect audience.

## Binary Evals

Answer YES or NO for each. Score = count(YES) / total.

### E1: Valid syntax
Does the diagram source code use valid syntax for the declared format? (Mermaid syntax for Mermaid, PlantUML with C4 includes for C4, D2 syntax for D2.) A diagram with syntax errors that would fail to render scores NO.
Example YES: Well-formed `flowchart LR` with proper arrow syntax `A --> B`
Example NO: Mixed Mermaid and D2 syntax, missing `@startuml`/`@enduml`, unclosed subgraphs

### E2: Format matches use case
Did the skill select the format specified or recommended by the format selection guide? (Input 1 asks for Mermaid → Mermaid. Input 2 asks for PlantUML C4 → PlantUML C4. Input 3 asks for D2 → D2.) Scores NO if the format doesn't match the request.
Example YES: Input 2 produces PlantUML with `!include <C4/C4_Container>`
Example NO: Input 2 produces a Mermaid flowchart instead of PlantUML C4

### E3: Every arrow has a text label
Does every connection/arrow in the diagram have a text label describing what flows through it? Check ALL arrows — a single unlabeled arrow scores NO. This is a core style guide promise: "every arrow should say what flows through it."
Example YES: `Rel(sources, dlt, "Ingest", "Auto Loader")` or `A -->|CDC events| B`
Example NO: `A --> B` with no label, or `sources -> ingestion` with no description

### E4: Node count under 20 per diagram
Does the diagram contain 20 or fewer top-level nodes (not counting sub-elements within subgraphs/containers)? If the system requires more, was it split into multiple diagrams? The style guide says "max 15-20 nodes per diagram."
Example YES: 14 nodes across 4 subgroups
Example NO: 25+ top-level nodes crammed into one diagram

### E5: Subgraphs used for logical grouping
Are related components grouped into subgraphs, system boundaries, or containers (not scattered as flat nodes)? The style guide says "group by team, environment, or data zone."
Example YES: Medallion layers in separate subgraphs, source systems grouped together
Example NO: All nodes at the same level with no grouping or hierarchy

### E6: Color semantics are consistent
If colors are used, do they follow a consistent semantic scheme? Bronze/silver/gold for medallion layers, or other deliberate color assignments with visual logic. Scores NO if colors are random or absent when the diagram type warrants them.
Example YES: Bronze=#CD7F32, Silver=#C0C0C0, Gold=#FFD700 (or similar semantic mapping)
Example NO: Random colors assigned to nodes with no pattern, or all nodes default gray when the diagram shows medallion layers

### E7: Diagram has a title
Does the diagram have a title — either via format-native title syntax (Mermaid frontmatter, PlantUML `title`, D2 top-level label) or a markdown heading immediately above the code block?
Example YES: `title Data Platform - Container Diagram` inside PlantUML, or `## Retail Medallion Architecture` above the code block
Example NO: Diagram code with no title anywhere

### E8: Audience-appropriate depth
Is the level of technical detail appropriate for the stated audience? Executive/compliance audiences should see systems and data flows, not implementation details. Engineering audiences should see specific technologies, protocols, and configurations.
Example YES: Input 2 (compliance audience) shows PHI flow boundaries and access controls, not Spark configuration details
Example NO: Input 2 dumps DLT pipeline internals and cluster configs at a compliance officer

### E9: Accessibility — contrast and labeling
Does the diagram use readable text contrast (dark text on light fills, light text on dark fills) and not rely solely on color to convey meaning? The accessibility section requires shape + color + label differentiation.
Example YES: Bronze layer uses `style.font-color: "#fff"` on dark fill, plus the label "Bronze"
Example NO: Red and green nodes with no labels distinguishing them, or dark text on dark fill

### E10: Data flow direction is consistent
Does the diagram maintain a consistent primary flow direction (left-to-right OR top-to-bottom) without arrows going backward against the main flow? The style guide warns against spaghetti flow.
Example YES: All major flows go left-to-right with `direction: right` or `flowchart LR`
Example NO: Main flow goes left-to-right but multiple arrows loop back right-to-left creating visual spaghetti
