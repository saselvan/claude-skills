# Evals: architecture-diagram

## Render Pipeline

The arch-diagram skill produces draw.io XML. To score visual quality, the XML must be rendered to PNG.

```
render_tool: drawio
render_command: |
  # 1. Extract XML from execution output (between ```xml and ``` markers, or full content if pure XML)
  # 2. Save as temp .drawio file
  # 3. Render to PNG
  drawio --export --format png --scale 2 -o {output_png} {input_drawio}
render_output: PNG
scorer_receives: source + rendered_image
```

The scorer reads the source XML for structural evals (E1-E8) and the rendered PNG for visual evals (E9-E12).

## Test Inputs

### Input 1: Lakebase Agent Memory Architecture
Create a Databricks reference architecture diagram showing how Lakebase powers AI agent memory. Audience is enterprise architects. Use draw.io XML output.

Six zones: (1) Data sources on the left — user interactions, enterprise systems, external APIs. (2) Agent runtime — LangGraph/OpenAI Agents SDK on Databricks Apps, Mosaic AI Model Serving, agent tools including Unity Catalog Function Calling and Mosaic AI Vector Search for enterprise knowledge retrieval (Vector Search is a tool, not memory). (3) Lakebase memory layer at center — short-term (checkpoints by thread_id), long-term (user profiles in JSONB), semantic (pgvector for agent's own past interactions, not enterprise knowledge). (4) Lakehouse feedback loop — agent data auto-syncs to Delta tables, feeds Agent Evaluation, model fine-tuning, and Databricks SQL analytics. (5) Governance bar — Unity Catalog, full width. (6) Agent surfaces on the right — Databricks Apps, AI/BI Genie, Slack/Teams, MLflow.

### Input 2: Healthcare Data Lakehouse
Create a Databricks reference architecture for a healthcare data lakehouse. Audience is a CISO and compliance officer. Draw.io XML output.

Sources: EHR (Epic), claims systems, pharmacy data, lab results. Ingestion via Lakeflow Connect and Auto Loader. Medallion layers: Bronze (raw FHIR, HL7, claims files), Silver (de-identified, FHIR-normalized), Gold (patient cohorts, HEDIS measures, trial-ready datasets). Processing via Lakeflow Jobs and Mosaic AI. Serving via Databricks SQL and Model Serving. Consumers: clinical research, regulatory reporting, BI dashboards. Governance with HIPAA emphasis.

### Input 3: Manufacturing IoT Analytics (stress test)
Create a reference architecture for a manufacturing IoT analytics platform on Databricks. Audience is enterprise architects at an auto manufacturer. Draw.io XML.

Sources: 6 IoT sensor types across 12 production lines, MES system, ERP (SAP), quality management system. Streaming ingestion via Kafka into Databricks. Medallion layers with descriptive labels. Real-time anomaly detection via Mosaic AI Model Serving. Gold layer serves: live ops dashboards (Databricks SQL → Tableau), predictive maintenance API, regulatory batch reports for NHTSA. Unity Catalog governs everything. Foundation bar with Delta Lake, Iceberg, Spark, Photon.

## Binary Evals

### Structural Evals (scored from source XML)

### E1: Valid draw.io XML
Does the output contain valid draw.io XML wrapped in `<mxfile><diagram><mxGraphModel><root>` tags? Can it be opened in draw.io without parse errors? Scores NO if the XML is malformed, uses wrong tag names, or is missing the root structure.
Example YES: Complete XML with mxfile, diagram, mxGraphModel, root, mxCell elements
Example NO: D2 code, Mermaid code, partial XML, or XML that doesn't start with mxfile

### E2: Explicit x,y coordinates on every node
Does every mxCell with vertex="1" have an mxGeometry element with explicit x and y values? Scores NO if any node is missing coordinates (would result in auto-placement).
Example YES: `<mxGeometry x="500" y="200" width="160" height="60" as="geometry"/>`
Example NO: mxGeometry without x or y attributes, or nodes without mxGeometry at all

### E3: Governance is a full-width bar
Is the governance element a wide rectangle (width >= the platform container width) positioned at the bottom, with dark teal fill (#1B3A4B)? Scores NO if governance is a regular-sized node, or positioned inside the platform as a peer of other nodes.
Example YES: mxCell with width matching platform width, y-position below platform content, fillColor=#1B3A4B
Example NO: A 160x60 box labeled "Unity Catalog" among other boxes, or governance missing

### E4: All arrows have labels
Does every mxCell with edge="1" have a non-empty value attribute describing what flows through the connection? A single unlabeled arrow scores NO.
Example YES: `value="CDC events"`, `value="Save checkpoint"`, `value="JDBC/ODBC"`
Example NO: `value=""` or edge cells with no value attribute

### E5: Left-to-right zone positioning
Are data sources positioned at lower x-coordinates (left) and consumers at higher x-coordinates (right)? The platform should be in the center. Check the mxGeometry x values across zones.
Example YES: Sources x=0-200, Platform x=400-1000, Consumers x=1100-1400
Example NO: Sources and consumers at similar x values, or consumers to the left of sources

### E6: Databricks product names present
Does the XML use at least 4 of these official names in node labels: Lakebase, Mosaic AI, Unity Catalog, Databricks Apps, Databricks SQL, AI/BI Genie, Lakeflow Jobs, Lakeflow Connect, Delta Sharing? Check the value attributes of mxCells. Generic terms instead of product names score NO.
Example YES: Nodes with value="Mosaic AI Model Serving", value="Unity Catalog", value="Databricks SQL"
Example NO: value="ML Platform", value="Data Catalog", value="SQL Warehouse"

### E7: Descriptive medallion labels (when medallion layers present)
If the diagram includes Bronze/Silver/Gold layers, does each layer label include a description of what it contains for this specific use case? Generic labels score NO. Skip this eval if the diagram doesn't use medallion layers.
Example YES: `value="Bronze&#xa;Raw FHIR messages, HL7, claims files"`
Example NO: `value="Bronze (Raw)"` or `value="Bronze"` with no description

### E8: Zones are visually grouped
Are related components grouped into container mxCells (parent-child relationships) or visually bounded regions? Flat lists of 20+ ungrouped nodes at the same level score NO.
Example YES: Nodes with parent="zone-platform" or parent="zone-sources" showing hierarchical grouping
Example NO: All nodes with parent="1" (all at root level, no grouping)

### Visual Evals (scored from rendered PNG)

### E9: No overlapping text or labels [visual]
When the diagram is rendered, are ALL text labels fully readable without overlapping other labels, nodes, or arrows? Score NO if any label collides with another element, is partially hidden behind a node, or if two labels overlap each other making either unreadable. Pay special attention to arrow labels crossing zones and step indicator circles colliding with node boundaries.
Example YES: Every label has clear space around it; arrow labels sit in open space between source and target; step numbers are positioned in whitespace gaps
Example NO: "Load episodic" overlaps with "Load semantic"; a numbered circle sits on top of a node edge; an arrow label crosses through a zone title

### E10: Breathing room between components [visual]
Does the rendered diagram have generous whitespace between components — similar to official Databricks reference architectures? Score NO if components are packed tightly with minimal gaps, if boxes are touching or nearly touching adjacent boxes, or if the overall impression is "crowded." The Databricks standard is roughly 30-50px visible gaps between sibling nodes and 20px+ padding inside zone containers.
Example YES: Clear visual separation between all components; each box has whitespace buffer; zones have visible internal margins; the diagram feels "open" and scannable
Example NO: Boxes crammed together with <10px gaps; annotation notes pressed against component edges; the center of the diagram is a wall of overlapping elements

### E11: Concise node labels (no schema dumps) [visual]
Are node labels SHORT — ideally 1-3 words for product names, max 2 lines for any node? Score NO if any node contains SQL schemas, configuration parameters, multi-line technical annotations, or paragraph-length descriptions INSIDE the box. Technical detail belongs in a companion guide, not inside diagram nodes. The Databricks standard is product name only (e.g., "Databricks SQL", "Auto Loader", "Spark / Photon").
Example YES: `value="Mosaic AI"`, `value="Delta Live Tables"`, `value="Lakebase&#xa;pgvector"` (name + one qualifier)
Example NO: `value="agent_knowledge:&#xa;entity_type · entity_id · fact_key&#xa;fact_value JSONB · pgvector · confidence&#xa;access_count · EMA scoring"` (schema dump inside a box)

### E12: Clean arrow routing without spaghetti [visual]
When rendered, do arrows follow clean orthogonal paths without creating a tangled "spaghetti" effect? Score NO if arrows cross through unrelated zones, if more than 2 arrows cross at the same point, if arrow paths create visual noise that makes the data flow hard to follow, or if there are more than 15 arrows total (Databricks reference architectures use spatial proximity over explicit connections — fewer arrows is better).
Example YES: Arrows follow clear L-shaped or straight paths; arrows connect adjacent components without crossing distant zones; total arrow count is proportional to node count (roughly 1:2 arrows-to-nodes ratio or less)
Example NO: An arrow from the top-left crosses through the center to reach the bottom-right; 5 arrows converge at one point; arrows labeled "Tool dispatch" and "Build prompt" create a knot in the middle of the framework zone
