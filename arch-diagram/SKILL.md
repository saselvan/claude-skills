---
name: architecture-diagram
version: "2.0"
description: "Customer-grade architecture diagrams as draw.io XML. Positioned layout with Databricks icons, branded zones, and cloud vendor icon libraries. Output opens in draw.io, Lucidchart, or any tool that imports .drawio files. USE WHEN reference architecture, customer presentation diagram, Databricks architecture, professional architecture diagram, draw.io, positioned layout, architecture with icons."
changelog: |
  v2.0: Grill-me redesign — direct .drawio file output, MCP server preferred, T-shirt canvas sizes, companion guide with numbered steps, programmatic XML validation, icon strategy, cross-skill routing.
  v1.0: Initial skill with draw.io XML, visual standards, 8 evals.
---

# Architecture Diagram

Generate customer-grade architecture diagrams as draw.io XML with absolute positioning, branded zones, vendor icons, and labeled arrows. Writes a `.drawio` file directly (not XML-in-markdown) plus a companion `{name}-guide.md` with numbered step walkthrough.

**When to use which skill:**
- **This skill (`arch-diagram`):** Standalone customer-facing reference architectures. Produces `.drawio` files editable in draw.io/Lucidchart. Positioned layout with icons.
- **`diagram` skill:** Quick internal sketches, GitHub READMEs, sequence diagrams, ERDs, C4 models. Auto-layout formats (Mermaid, D2, PlantUML).
- **`deck-render` skill:** Diagrams embedded inside PowerPoint slides as part of a deck.
- **`diagram` → Excalidraw:** Live whiteboarding sessions where you're building on screen with the customer.

## MCP Tools

**Highly preferred: next-ai-drawio MCP server**
```
claude mcp add drawio -- npx @next-ai-drawio/mcp-server@latest
```

Check if the MCP server is available. If yes, generate the full XML first, then open it in the MCP server for visual review. If unavailable, write the `.drawio` file directly — the output is identical, you just don't get live preview.

## Icons

**Strategy:** Use built-in draw.io shapes for cloud services (AWS/Azure/GCP icons are built-in). Use labeled rectangles with Databricks brand colors for Databricks products. Document which rectangles to swap for official icons during polish.

**Built-in cloud icons:**
- AWS: `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{service}`
- Azure: `shape=mxgraph.azure.{service}`
- GCP: `shape=mxgraph.gcp2.{service}`

**Databricks products:** Use colored rectangles (Databricks blue #137CBD for functional blocks, rose #9B2D5E for ML/AI). Include a "Polish notes" section in the companion guide listing which rectangles to swap for official Databricks icons from the `databricks-drawio-icons` library.

---

## Workflow

```
STEP 0: Confirm Audience, Intent & Output Path
  Q: Who sees this? (customer exec, enterprise architect, compliance, internal team?)
  Q: What's the story? (platform overview, specific solution, migration path?)
  Q: Cloud context? (AWS, Azure, GCP, multi-cloud?)
  Q: Where should I save the .drawio file? (ALWAYS ask before writing)

STEP 1: Define Zones
  Map the architecture into the Databricks layout spine:
    Left: Data Sources (vertical stack)
    Left-center: Connectivity / Ingestion
    Center: Data Intelligence Platform (the main bounded region)
    Right-center: Serving / Processing
    Right: Consumers / Applications
    Bottom: Governance bar (full width) + Foundation bar

STEP 2: Select Canvas Size
  Pick based on zone count and node density:
    Size S (1200x700):  Simple flows, ≤4 zones, ≤15 nodes (e.g., compliance audit, migration before/after)
    Size M (1500x900):  Standard reference architectures, 5-6 zones, 15-25 nodes (e.g., medallion lakehouse, IoT analytics)
    Size L (1800x1100): Complex multi-zone with feedback loops, 6+ zones, 25+ nodes (e.g., agent memory, multi-consumer platforms)

STEP 3: Plan Coordinates (Size M defaults shown — scale proportionally for S/L)
    Sources:      x=0,    y=100,  w=180
    Ingestion:    x=220,  y=100,  w=180
    Platform:     x=440,  y=60,   w=560, h=600
    Serving:      x=1040, y=100,  w=180
    Consumers:    x=1260, y=100,  w=180
    Governance:   x=0,    y=700,  w=FULL_CANVAS_WIDTH, h=50
    Foundation:   x=440,  y=760,  w=560, h=40

STEP 4: Generate draw.io XML
  Build the full XML. Add numbered teal step indicators (①②③...) at key flow transitions.
  Every node needs: id, value (label), style, x, y, width, height
  Every arrow needs: source id, target id, value (label describing what flows)

STEP 5: Validate XML
  Before saving, run programmatic checks:
    ✓ Every vertex="1" cell has mxGeometry with x and y
    ✓ Every edge="1" cell has a non-empty value attribute
    ✓ Governance bar width >= full canvas width
    ✓ At least 4 Databricks product names in node labels
  Fix any failures before proceeding.

STEP 6: Write Files
  1. Write {name}.drawio — the diagram file (ask user for path first)
  2. Write {name}-guide.md — companion guide with:
     - Numbered steps matching the diagram's teal circles (① → paragraph explaining what happens)
     - Talking points for the stated audience
     - Polish notes: list of rectangles to swap for official Databricks icons
  3. If MCP server is available, open the .drawio file for visual review

STEP 7: Present
  Show the user a brief summary of what was generated.
  Do NOT paste XML into the chat — it's in the file.
```

---

## Databricks Visual Standards

Identical to the `diagram` skill v3.2 standards. Apply these when generating XML:

### Color Palette
```
Platform banner:    fill=#FF3621, fontColor=#FFFFFF    (coral — top bar)
Orchestration bar:  fill=#1B3A4B, fontColor=#FFFFFF    (dark teal)
Governance bar:     fill=#1B3A4B, fontColor=#FFFFFF    (dark teal, full width)
Foundation bar:     fill=#FF3621, fontColor=#FFFFFF    (coral, full width)
Functional blocks:  fill=#137CBD, fontColor=#FFFFFF    (Databricks blue)
AI/ML zones:        fill=#9B2D5E, fontColor=#FFFFFF    (rose/mauve)
Operational:        fill=#FFC107, fontColor=#000000    (amber)
Source/consumer bg: fill=#F5F5F5, fontColor=#000000    (light gray)
Content area:       fill=#FFFFFF, fontColor=#000000    (white)
Bronze:             fill=#CD7F32, fontColor=#FFFFFF
Silver:             fill=#C0C0C0, fontColor=#000000
Gold:               fill=#FFD700, fontColor=#000000
```

### Layout Rules
- Left-to-right primary flow. Always.
- Governance as full-width bar at bottom — never a peer node.
- Foundation technology bar below governance (Delta Lake, Iceberg, Spark, Photon).
- Dashed borders for internal zones, solid for external systems and platform boundary.
- Platform boundary uses coral stroke (#FF3621).
- Numbered flow steps using teal circles (#00A972).
- Medallion layers with descriptive labels ("Bronze — {what's in it}").
- Use Databricks product names (see naming table below).

### Product Naming
| Generic | Databricks Name |
|---|---|
| Data catalog | Unity Catalog |
| ETL pipelines | Lakeflow Jobs |
| Data warehouse | Databricks SQL |
| ML platform | Mosaic AI |
| Data ingestion | Auto Loader / Lakeflow Connect |
| Feature store | Feature Store (Unity Catalog) |
| Model serving | Model Serving (Mosaic AI) |
| NL query | AI/BI Genie |
| Data sharing | Delta Sharing |
| Operational DB | Lakebase |

---

## draw.io XML Reference

### Minimal Valid Structure
```xml
<mxfile>
  <diagram name="Architecture" id="arch-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="900">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Nodes go here -->
        <!-- Arrows go here -->
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Node (Rectangle with Label)
```xml
<mxCell id="node-1" value="Databricks SQL" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=12;fontStyle=1;" 
  vertex="1" parent="1">
  <mxGeometry x="500" y="200" width="160" height="60" as="geometry"/>
</mxCell>
```

### Zone Container (Grouped Region)
```xml
<!-- Container -->
<mxCell id="zone-platform" value="Data Intelligence Platform" 
  style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF3621;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=14;fontColor=#FF3621;dashed=0;" 
  vertex="1" parent="1">
  <mxGeometry x="440" y="60" width="560" height="600" as="geometry"/>
</mxCell>

<!-- Child node inside container -->
<mxCell id="node-sql" value="Databricks SQL" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;fontSize=11;" 
  vertex="1" parent="zone-platform">
  <mxGeometry x="40" y="400" width="140" height="50" as="geometry"/>
</mxCell>
```

### Governance Bar (Full Width)
```xml
<mxCell id="gov-bar" value="Governance — Unity Catalog&#xa;Access control · PII masking · Lineage · Audit trail" 
  style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#1B3A4B;fontSize=11;fontStyle=1;verticalAlign=middle;" 
  vertex="1" parent="1">
  <mxGeometry x="0" y="700" width="1500" height="50" as="geometry"/>
  <!-- NOTE: width must span the FULL diagram (all zones), not just the platform container -->
</mxCell>
```

### Foundation Bar
```xml
<mxCell id="foundation" value="Delta Lake · Iceberg · Apache Spark · Photon" 
  style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=11;fontStyle=1;" 
  vertex="1" parent="1">
  <mxGeometry x="440" y="760" width="560" height="40" as="geometry"/>
</mxCell>
```

### Labeled Arrow
```xml
<mxCell id="arrow-1" value="CDC events" 
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;" 
  edge="1" source="node-source" target="node-target" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### Dashed Zone (Internal)
```xml
<mxCell id="zone-etl" value="ETL Zone" 
  style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;dashed=1;dashPattern=8 4;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#666666;" 
  vertex="1" parent="zone-platform">
  <mxGeometry x="20" y="80" width="520" height="200" as="geometry"/>
</mxCell>
```

### Numbered Step Indicator
```xml
<mxCell id="step-1" value="1" 
  style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
  vertex="1" parent="1">
  <mxGeometry x="10" y="100" width="28" height="28" as="geometry"/>
</mxCell>
```

### AWS Icon Example
```xml
<mxCell id="aws-s3" value="S3" 
  style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#3F8624;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;" 
  vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="48" height="48" as="geometry"/>
</mxCell>
```

### Multiline Labels
Use `&#xa;` for line breaks in XML values:
```xml
value="Bronze&#xa;Raw HL7 messages, DICOM images"
```

---

## GTM Scenario Library

Industry-specific reference architecture examples with complete draw.io XML. Each scenario is a self-contained file that can be used as a template.

| # | Scenario | Audience | Canvas | File |
|---|----------|----------|--------|------|
| 1 | Healthcare Oncology Data Unification | C-suite + medical informatics | S | `scenarios/01-healthcare-oncology.md` |
| 2 | Genomics Data Pipeline | Data eng + research biology | M | `scenarios/02-genomics-pipeline.md` |
| 3 | Unity Catalog Migration | Enterprise architects | S | `scenarios/03-unity-catalog-migration.md` |
| 4 | Manufacturing Quality Control (IoT) | Operations + quality teams | M | `scenarios/04-manufacturing-iot.md` |
| 5 | Compliance Audit Trail | Compliance officers | S | `scenarios/05-compliance-audit.md` |
| 6 | Lakebase AI Agent Memory | Enterprise architects | L | `scenarios/06-lakebase-agent-memory.md` |

When generating a new diagram, read the closest matching scenario for structural reference. Adapt the zone layout, node count, and content to the user's specific request.

## Constraints

- **Always write a `.drawio` file directly.** Do NOT paste XML into chat. Write the file, tell the user where it is.
- **Always ask for the output path before writing.** Never assume a directory.
- **Always write a companion `{name}-guide.md`.** Numbered steps matching diagram circles, audience-specific talking points, polish notes.
- **Always label every arrow.** Use the `value` attribute on edge cells. An unlabeled arrow is ambiguous.
- **Always position elements with explicit x,y coordinates.** Never rely on auto-layout.
- **Always validate XML before saving.** Check: every vertex has x/y, every edge has a label, governance bar spans full width.
- **Governance is always a full-width bar.** x=0, width=full canvas. It governs everything. Never a peer node.
- **Use Databricks product names.** See the naming table.
- **Medallion layers need descriptive labels.** "Bronze — {what's specifically in this layer}" not just "Bronze (Raw)".
- **Keep node count manageable.** If >20 top-level nodes, decompose or use C4 drill-down.
- **Use built-in cloud icons, branded rectangles for Databricks.** Document icon swaps in the companion guide.

---

## Anti-Patterns

- **Using this skill for quick sketches** — use the `diagram` skill instead. This skill's XML output is heavy for a Slack message.
- **Expecting pixel-perfect output** — the XML provides correct architecture, positioning, and labeling. Final visual polish happens in draw.io/Lucid.
- **Forgetting the governance bar** — every Databricks diagram needs it. Check before saving.
- **Generic product names** — "ETL" instead of "Lakeflow Jobs" breaks the Databricks brand voice.
- **Nodes without coordinates** — auto-placed nodes defeat the purpose. Every mxGeometry needs x and y.

---

*"Architecture is the decision. The diagram is the proof. The XML is the delivery vehicle."*
