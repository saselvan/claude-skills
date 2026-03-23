---
name: architecture-diagram
version: "1.0"
description: "Customer-grade architecture diagrams as draw.io XML. Positioned layout with Databricks icons, branded zones, and cloud vendor icon libraries. Output opens in draw.io, Lucidchart, or any tool that imports .drawio files. USE WHEN reference architecture, customer presentation diagram, Databricks architecture, professional architecture diagram, draw.io, positioned layout, architecture with icons."
---

# Architecture Diagram

Generate customer-grade architecture diagrams as draw.io XML with absolute positioning, branded zones, vendor icons, and labeled arrows. Output is a `.drawio` file that opens in draw.io, Lucidchart, or any compatible editor for manual polish.

**When to use this skill vs the `diagram` skill:**
- This skill: Customer presentations, reference architectures, diagrams that need to look like official Databricks/AWS/Azure marketing materials. Positioned layout. Icons.
- `diagram` skill: Quick internal sketches, GitHub READMEs, email explanations, sequence diagrams, ERDs, C4 models. Auto-layout is fine.

## MCP Tools

**Primary: next-ai-drawio MCP server**
```
claude mcp add drawio -- npx @next-ai-drawio/mcp-server@latest
```

If the MCP server is unavailable, generate the draw.io XML directly as a `.drawio` file. The XML is the same format — the MCP server just provides live preview.

## Icon Libraries

**Databricks icons:** github.com/nihil0/databricks-drawio-icons — import into draw.io via File > Open Library.

**Cloud vendor icons (built into draw.io):**
- AWS: `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{service}`
- Azure: `shape=mxgraph.azure.{service}` or use the Azure icon libraries
- GCP: `shape=mxgraph.gcp2.{service}`

When generating XML, use the `shape` style attribute to reference icons. If the exact icon shape ID is unknown, use a labeled rectangle with the correct brand color — the user can swap in the icon during manual polish.

---

## Workflow

```
STEP 0: Confirm Audience & Intent
  Q: Who sees this? (customer exec, enterprise architect, compliance, internal team?)
  Q: What's the story? (platform overview, specific solution, migration path?)
  Q: Cloud context? (AWS, Azure, GCP, multi-cloud?)
  Q: Will this be polished in Lucid/draw.io after? (always yes for this skill)

STEP 1: Define Zones
  Map the architecture into the Databricks layout spine:
    Left: Data Sources (vertical stack)
    Left-center: Connectivity / Ingestion
    Center: Data Intelligence Platform (the main bounded region)
    Right-center: Serving / Processing
    Right: Consumers / Applications
    Bottom: Governance bar (full width) + Foundation bar

STEP 2: Plan Coordinates
  Use a 1400x900 canvas (standard widescreen).
  Assign x,y coordinates to each zone:
    Sources:      x=0,    y=100,  w=180
    Ingestion:    x=220,  y=100,  w=180
    Platform:     x=440,  y=60,   w=560, h=600
    Serving:      x=1040, y=100,  w=180
    Consumers:    x=1260, y=100,  w=180
    Governance:   x=0,    y=700,  w=1500, h=50 (full DIAGRAM width, not just platform)
    Foundation:   x=440,  y=760,  w=560, h=40  (full platform width)
  
  These are starting coordinates — adjust based on content density.

STEP 3: Generate draw.io XML
  Use the XML structure in references/drawio-template.md
  Every node needs: id, value (label), style, x, y, width, height
  Every arrow needs: source id, target id, value (label)

STEP 4: Save and Present
  Save as {name}.drawio
  Tell user: "Open in draw.io or Lucid to polish. All elements are positioned and labeled — adjust spacing, swap in vendor icons, add branding as needed."
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

## Constraints

- **Always label every arrow.** An unlabeled arrow is ambiguous. Use the `value` attribute on edge cells.
- **Always position elements with explicit x,y coordinates.** Never rely on auto-layout. The whole point of this skill is positioned layout.
- **Governance is always a full-width bar.** The governance bar must span the ENTIRE diagram width — from the leftmost source to the rightmost consumer — not just the platform container. Set x=0 and width equal to the full canvas width. It governs everything, not just the platform. Never a peer node.
- **Use Databricks product names.** See the naming table.
- **Medallion layers need descriptive labels.** "Bronze — {what's specifically in this layer}" not just "Bronze (Raw)".
- **Keep node count manageable.** If >20 top-level nodes, decompose into multiple diagrams or use C4 drill-down.
- **Save as .drawio file.** This opens in draw.io desktop, draw.io web, and Lucidchart import.
- **Tell the user to polish.** This skill produces the architecture and layout. The user adds final visual polish (icon swaps, font tuning, spacing) in their editor of choice.

---

## Anti-Patterns

- **Using this skill for quick sketches** — use the `diagram` skill instead. This skill's XML output is heavy for a Slack message.
- **Expecting pixel-perfect output** — the XML provides correct architecture, positioning, and labeling. Final visual polish happens in draw.io/Lucid.
- **Forgetting the governance bar** — every Databricks diagram needs it. Check before saving.
- **Generic product names** — "ETL" instead of "Lakeflow Jobs" breaks the Databricks brand voice.
- **Nodes without coordinates** — auto-placed nodes defeat the purpose. Every mxGeometry needs x and y.

---

*"Architecture is the decision. The diagram is the proof. The XML is the delivery vehicle."*
