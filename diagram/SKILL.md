---
name: diagram
version: "2.0"
description: "Technical architecture diagrams for solutions architects. Multi-format via uml-mcp (D2, PlantUML, C4, Mermaid, Graphviz, ERD, BPMN). Excalidraw for presentations. USE WHEN diagram, architecture, data flow, state diagram, sequence diagram, system design, medallion, lakehouse, pipeline, Unity Catalog, C4."
---

# Diagram

Generate technical architecture diagrams using multiple formats. Built for solutions architects working with Databricks, AWS, and data platforms.

## Tool Selection

```
C4 architecture (Context/Container/Component)?  → uml-mcp (PlantUML C4)
Clean, modern layout with good theming?          → uml-mcp (D2)
Needs to render in GitHub markdown?              → uml-mcp (Mermaid) or mermaid server (live reload)
Graph/network topology?                          → uml-mcp (Graphviz)
Entity-relationship / data model?                → uml-mcp (ERD)
Business process / workflow?                     → uml-mcp (BPMN)
Presentation-ready, hand-drawn aesthetic?         → Excalidraw
Quick preview with live reload?                  → mermaid server (fallback)
```

**Default to uml-mcp** — it covers the most formats via Kroki. Use the dedicated `mermaid` server only when you need live browser reload during iteration.

## MCP Tools Available

**uml-mcp** (`uml-mcp` server — primary, covers 16 diagram types):
- `generate_uml` — render diagram to file (SVG/PNG/PDF)
  - `diagram_type`: class, sequence, activity, usecase, state, component, deployment, object, mermaid, d2, graphviz, tikz, erd, blockdiag, bpmn, c4
  - `code`: diagram source code in the chosen format
  - `output_format`: svg (default), png, pdf
  - `output_dir`: where to save (optional)
  - `theme`, `scale`: styling options
- `generate_diagram_url` — returns URL + base64 (no file saved)

**Mermaid** (`mermaid` server — fallback, live reload):
- `mermaid_preview` — render + live preview in browser
- `mermaid_save` — export to SVG/PNG/PDF

**Excalidraw** (`excalidraw` server — requires canvas on localhost:3000):
- `create_element`, `batch_create_elements` — draw shapes, arrows, text
- `export_to_image`, `export_scene` — export to PNG/SVG/JSON
- `create_from_mermaid` — convert Mermaid to Excalidraw
- `describe_scene`, `get_canvas_screenshot` — visual feedback loop

## Format Selection Guide

| Use case | Best format | Why |
|---|---|---|
| System context / containers / components | **PlantUML C4** | Purpose-built for C4 model, best tooling |
| Complex architecture with clean layout | **D2** | Multiple layout engines, sketch mode, modern |
| GitHub PR / README embedding | **Mermaid** | Native GitHub rendering |
| Network/infra topology | **Graphviz** | Best automatic layout for graphs |
| Database schema | **ERD** | Purpose-built for entity relationships |
| Business process flows | **BPMN** | Industry standard |
| Quick iteration with live preview | **Mermaid** (via mermaid server) | Live browser reload |
| Customer-facing slides | **Excalidraw** | Hand-drawn aesthetic |

## Workflow

```
1. Clarify what diagram the user needs (type, audience, output format)
2. Choose format and tool (see selection guide above)
3. Generate diagram via uml-mcp (or mermaid server for live preview)
4. Preview — show to user or open in browser
5. Iterate — refine based on feedback
6. Save — export to the requested format and path
```

**Always preview before saving.** Never save a diagram the user hasn't seen.

---

## Architecture Patterns Library

Reference patterns for common solutions architect work. Use these as starting templates — adapt to the user's specific context.

### Medallion Architecture (Databricks)

```mermaid
flowchart LR
    subgraph Bronze["Bronze (Raw)"]
        B1[Landing Zone]
        B2[Raw Ingestion]
    end
    subgraph Silver["Silver (Cleaned)"]
        S1[Schema Enforcement]
        S2[Dedup & Quality]
        S3[Conformed Types]
    end
    subgraph Gold["Gold (Business)"]
        G1[Aggregations]
        G2[Feature Tables]
        G3[Serving Layer]
    end

    B1 --> B2 --> S1 --> S2 --> S3 --> G1 & G2 & G3

    style Bronze fill:#CD7F32,color:#fff
    style Silver fill:#C0C0C0,color:#000
    style Gold fill:#FFD700,color:#000
```

### Unity Catalog Hierarchy

```mermaid
flowchart TD
    MC[Metastore] --> C1[Catalog: prod]
    MC --> C2[Catalog: dev]
    C1 --> S1[Schema: raw]
    C1 --> S2[Schema: curated]
    C1 --> S3[Schema: serving]
    S1 --> T1[Table: events]
    S1 --> T2[Table: users]
    S2 --> T3[Table: user_sessions]
    S2 --> T4[Volume: models]
    S3 --> T5[Table: dashboard_metrics]
    S3 --> T6[Function: score_lead]
```

### Data Pipeline (DLT / Spark Streaming)

```mermaid
flowchart LR
    K[Kafka / Kinesis] -->|Auto Loader| DLT[Delta Live Tables]
    S3[S3 / ADLS] -->|Auto Loader| DLT
    API[REST APIs] -->|Batch| DLT

    DLT -->|Expectations| Q{Quality Gate}
    Q -->|Pass| Gold[Gold Tables]
    Q -->|Fail| Quarantine[Quarantine]

    Gold --> DS[Databricks SQL]
    Gold --> ML[ML Serving]
    Gold --> BI[BI / Tableau]
```

### AWS Data Platform

```mermaid
flowchart TD
    subgraph Ingestion
        KF[Kinesis Firehose]
        DMS[AWS DMS]
        GL[Glue Crawlers]
    end
    subgraph Storage
        S3R[S3: Raw]
        S3C[S3: Curated]
        Delta[Delta Lake]
    end
    subgraph Compute
        DBX[Databricks Workspace]
        EMR[EMR Serverless]
    end
    subgraph Serve
        RS[Redshift Serverless]
        ATH[Athena]
        QS[QuickSight]
    end

    KF & DMS --> S3R --> GL --> Delta
    Delta --> DBX & EMR --> S3C --> RS & ATH --> QS
```

### Sequence: API Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant L as Lambda
    participant DB as DynamoDB
    participant Q as SQS

    C->>GW: POST /orders
    GW->>L: Invoke handler
    L->>DB: PutItem (order)
    DB-->>L: Success
    L->>Q: SendMessage (process_order)
    Q-->>L: Ack
    L-->>GW: 202 Accepted
    GW-->>C: 202 + order_id
```

### State Diagram: Job Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Running : cluster_ready
    Running --> Succeeded : all_tasks_pass
    Running --> Failed : task_error
    Failed --> Pending : retry (max 3)
    Failed --> Terminated : max_retries
    Succeeded --> [*]
    Terminated --> [*]

    Running --> Cancelling : user_cancel
    Cancelling --> Terminated : cleanup_done
```

### C4 Context: Data Platform (PlantUML — use with `diagram_type: c4`)

```plantuml
@startuml
!include <C4/C4_Context>

title Data Platform - System Context

Person(analyst, "Data Analyst", "Queries curated data via SQL")
Person(eng, "Data Engineer", "Builds and monitors pipelines")
Person(ds, "Data Scientist", "Trains models, runs experiments")

System(platform, "Data Platform", "Databricks + AWS")

System_Ext(sources, "Source Systems", "ERP, CRM, IoT, SaaS APIs")
System_Ext(bi, "BI Tools", "Tableau, QuickSight")
System_Ext(apps, "Applications", "ML-powered features")

Rel(sources, platform, "Raw data", "Kafka, S3, DMS")
Rel(eng, platform, "Build & monitor", "Notebooks, DLT, Workflows")
Rel(analyst, platform, "SQL queries", "Databricks SQL")
Rel(ds, platform, "Experiments", "MLflow, Feature Store")
Rel(platform, bi, "Curated datasets", "JDBC/ODBC")
Rel(platform, apps, "Model endpoints", "REST API")
@enduml
```

### C4 Container: Data Platform (PlantUML — use with `diagram_type: c4`)

```plantuml
@startuml
!include <C4/C4_Container>

title Data Platform - Container Diagram

Person(eng, "Data Engineer", "Builds pipelines")

System_Boundary(platform, "Data Platform") {
    Container(uc, "Unity Catalog", "Databricks", "Governance, lineage, access control")
    Container(dlt, "Delta Live Tables", "Databricks", "Declarative ETL pipelines")
    Container(sql, "Databricks SQL", "Databricks", "Warehouse for analysts")
    Container(mlflow, "MLflow", "Databricks", "Experiment tracking, model registry")
    Container(s3, "S3 Data Lake", "AWS", "Bronze/Silver/Gold Delta tables")
    Container(workflows, "Workflows", "Databricks", "Orchestration, scheduling")
}

System_Ext(sources, "Source Systems")
System_Ext(bi, "BI Tools")

Rel(sources, dlt, "Ingest", "Auto Loader")
Rel(dlt, s3, "Write Delta", "Bronze → Silver → Gold")
Rel(uc, s3, "Govern access")
Rel(sql, s3, "Query", "Photon engine")
Rel(mlflow, s3, "Read features")
Rel(workflows, dlt, "Orchestrate")
Rel(eng, workflows, "Configure")
Rel(sql, bi, "Serve", "JDBC")
@enduml
```

### D2: Lakehouse Architecture (use with `diagram_type: d2`)

```d2
direction: right

sources: Source Systems {
  erp: ERP
  crm: CRM
  iot: IoT Streams
  saas: SaaS APIs
}

ingestion: Ingestion Layer {
  autoloader: Auto Loader
  kafka: Kafka Connect
  dms: AWS DMS
}

lakehouse: Databricks Lakehouse {
  bronze: Bronze {
    style.fill: "#CD7F32"
    raw_events: Raw Events
    raw_users: Raw Users
  }
  silver: Silver {
    style.fill: "#C0C0C0"
    clean_events: Clean Events
    user_profiles: User Profiles
  }
  gold: Gold {
    style.fill: "#FFD700"
    daily_metrics: Daily Metrics
    feature_store: Feature Store
    serving_tables: Serving Tables
  }

  unity_catalog: Unity Catalog {
    style.fill: "#4A90D9"
    style.font-color: "#fff"
  }
}

consumers: Consumers {
  sql_warehouse: Databricks SQL
  ml_serving: ML Serving
  tableau: Tableau
  quicksight: QuickSight
}

sources.erp -> ingestion.dms: CDC
sources.crm -> ingestion.autoloader: Files
sources.iot -> ingestion.kafka: Streaming
sources.saas -> ingestion.autoloader: API dumps

ingestion.autoloader -> lakehouse.bronze
ingestion.kafka -> lakehouse.bronze
ingestion.dms -> lakehouse.bronze

lakehouse.bronze -> lakehouse.silver: DLT expectations
lakehouse.silver -> lakehouse.gold: Aggregations
lakehouse.unity_catalog -> lakehouse.bronze: Govern
lakehouse.unity_catalog -> lakehouse.silver: Govern
lakehouse.unity_catalog -> lakehouse.gold: Govern

lakehouse.gold.serving_tables -> consumers.sql_warehouse
lakehouse.gold.feature_store -> consumers.ml_serving
consumers.sql_warehouse -> consumers.tableau: JDBC
consumers.sql_warehouse -> consumers.quicksight: JDBC
```

---

## Diagram Type Selection Guide

| User asks about... | Diagram type | Mermaid syntax |
|---|---|---|
| How data flows through the system | `flowchart LR` | Left-to-right flow |
| How components interact over time | `sequenceDiagram` | Message arrows between participants |
| What states a process goes through | `stateDiagram-v2` | State transitions |
| How systems relate at a high level | `C4Context` | People, systems, relationships |
| What's inside a system | `C4Container` | Containers within a system boundary |
| What's inside a container | `C4Component` | Components within a container |
| Database schema / relationships | `erDiagram` | Entity-relationship |
| Deployment / infrastructure | `flowchart TD` | Top-down with subgraphs |
| Sprint planning / timeline | `gantt` | Timeline bars |
| Decision logic | `flowchart TD` with diamonds | Decision nodes |

---

## Output Conventions

```
Mermaid files:  docs/diagrams/{name}.mmd       (source)
                docs/diagrams/{name}.svg       (rendered)
Excalidraw:     docs/diagrams/{name}.excalidraw (source)
                docs/diagrams/{name}.png       (exported)
```

Embed in markdown:
````markdown
![Architecture](docs/diagrams/medallion-architecture.svg)
````

---

## Style Guide

- **Labels over arrows** — every arrow should say what flows through it
- **Subgraphs for boundaries** — group by team, environment, or data zone
- **Color semantics** — Bronze/Silver/Gold for medallion; blue for compute, green for storage, orange for ingestion
- **Keep it readable** — max 15-20 nodes per diagram. Split into multiple diagrams if larger.
- **Title every diagram** — use Mermaid's `---\ntitle: ...\n---` frontmatter or a markdown heading above

### Accessibility

- **Color-blind safe palette** — never use red/green distinction alone. Use shape + color + label to differentiate.
- **Alt text** — every embedded diagram needs descriptive alt text: `![Medallion architecture showing bronze-silver-gold data flow](...)` not `![diagram](...)`
- **Contrast** — ensure text is readable against fill colors. Dark text on light fills, light text on dark fills.
- **Labeled arrows** — don't rely on color or position alone to convey meaning. Every connection should have a text label.

### Anti-Patterns (Diagram Smells)

- **Spaghetti flow** — if lines cross more than twice, restructure the layout or split into multiple diagrams
- **Box overload** — more than 15-20 nodes = unreadable. Decompose into C4 levels (Context → Container → Component)
- **Unlabeled arrows** — an arrow without a label is a guess. Always say what flows through it.
- **Symmetric layout lie** — don't make unequal things look equal. If one path handles 95% of traffic, make it visually dominant.
- **Stale diagram** — a diagram that doesn't match the code is worse than no diagram. Date every diagram and note the source of truth.

---

*"A diagram is a conversation compressed into a picture. If it needs a paragraph to explain, it needs another iteration."*
