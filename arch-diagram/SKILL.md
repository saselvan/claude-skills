---
name: architecture-diagram
version: "3.0"
description: "Customer-grade architecture diagrams as draw.io XML. Positioned layout with Databricks icons, branded zones, and cloud vendor icon libraries. Output opens in draw.io, Lucidchart, or any tool that imports .drawio files. USE WHEN reference architecture, customer presentation diagram, Databricks architecture, professional architecture diagram, draw.io, positioned layout, architecture with icons."
changelog: |
  v3.0: Lakebase diagram learnings — arrow semantics (READ/WRITE), container idiom rule, HTML label patterns, step action labels, cap row pattern, accent bars, self-eval checklist, Lucid-clean export, data sources formatting, spatial honesty.
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

STEP 5: Self-Eval Checklist
  Run ALL checks before saving. Fix any failures.

  Structural (blocking — diagram is wrong without these):
    ✓ Every vertex="1" cell has mxGeometry with x and y
    ✓ Every edge="1" cell has a non-empty value attribute
    ✓ Governance/UC bar width spans full platform interior or full canvas
    ✓ At least 4 Databricks product names in node labels
    ✓ Data sources are OUTSIDE the platform border (they're external systems)
    ✓ Arrow semantics: READ arrows are dashed, WRITE arrows are solid
    ✓ Correct Databricks terminology (DeltaSync not "Reverse ETL", Lakeflow not "ETL")

  Quality (diagram works but looks amateur without these):
    ✓ Every step circle has a companion italic action label
    ✓ Data Sources box uses HTML formatting with category headers, not plain text lists
    ✓ Two container idioms only — no mixed styles
    ✓ Step indicator gap >= 50px between zones they sit in
    ✓ No node overlaps (verify x+w of left node < x of right node)
    ✓ Zone padding >= 20px on all sides
    ✓ Foundation bars use Databricks product names, not generic terms

STEP 6: Write Files
  1. Write {name}.drawio to canonical path (see Output Convention below)
  2. Write {name}-lucid.drawio — Lucid-clean copy with draw.io-specific icons stripped
     (Remove any cells using img/lib/, mxgraph.aws4.*, or other draw.io shape library refs)
  3. Write {name}-guide.md companion guide with frontmatter (see Output Convention) containing:
     - Numbered steps matching the diagram's teal circles (① → paragraph explaining what happens)
     - Talking points for the stated audience
     - Polish notes: list of rectangles to swap for official Databricks icons
  4. If MCP server is available, open the .drawio file for visual review
  5. Call vault_reindex(full=false, embed=false) after writing all files

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
- Numbered flow steps using teal circles (#00A972) with **italic action labels** (see Step Indicators below).
- Medallion layers with descriptive labels ("Bronze — {what's in it}").
- Use Databricks product names (see naming table below).
- **Internal vs external placement tells the architecture story.** What's inside vs outside the platform border is a design decision, not just layout. Data sources are external systems — they go outside. Managed services (Apps, Genie) go inside. Third-party integrations (Slack/Teams) go outside. Placement IS the architecture.

### Container Idiom Rule (Two Idioms Only)
Every container must use exactly one of these two idioms. Never mix styles or invent a third.

| Idiom | When | Style |
|---|---|---|
| **Dashed + no fill** | Internal groupings (zones, clusters) | `dashed=1;dashPattern=8 4;fillColor=none;strokeColor=#CCCCCC;` |
| **Solid + fill** | Primary elements, platform boundary, foundation bars | `dashed=0;fillColor=#FFFFFF;strokeColor=#0A6EBD;strokeWidth=2;` |

### Arrow Semantics (READ vs WRITE)
Arrow style communicates architectural intent, not just connection:

| Pattern | Style | Meaning | Example |
|---|---|---|---|
| **Solid, thick** | `strokeWidth=2;dashed=0;` | Synchronous WRITE — must succeed | Checkpoint persist, session create |
| **Dashed, normal** | `strokeWidth=1.5;dashed=1;dashPattern=6 3;` | Async READ — pull/retrieval | Context loading, memory retrieval |
| **Solid, thin gray** | `strokeColor=#AAAAAA;strokeWidth=1;` | Delivery/routing — no step number | Passing results to a surface |
| **Dashed, colored** | `strokeWidth=1;dashed=1;dashPattern=6 3;` | Tool dispatch — optional/conditional | Tool calls from serving to functions |

### Spacing Rules (prevents text overlap when rendered)
- **Minimum gap between sibling nodes:** 30px between edges (both x and y). If two nodes would be closer than 30px, move one.
- **Minimum node size:** 140w × 50h for primary boxes. Secondary boxes (surfaces, tool buttons) can go to 100w × 34h minimum.
- **Zone internal padding:** 20px from zone container border to any child node edge. Never place a node flush against a zone boundary.
- **Step indicator gap budget:** Reserve 50-70px of whitespace between major zones for step circles and action labels. Step indicators need breathing room — they cannot sit in a 20px crack.
- **Arrow label clearance:** Arrow labels must not overlap any node or zone header. Use `offset` or reposition the arrow path if the label would collide.
- **Gutter between external and platform:** Minimum 15px between any element outside the platform border and the border itself. Prevents visual cramping.

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
Use `&#xa;` for line breaks in plain text values:
```xml
value="Bronze&#xa;Raw HL7 messages, DICOM images"
```

### HTML Labels (Rich Text — Preferred for Multi-Style Content)
Set `html=1` in the style, then use HTML in the `value` attribute. This is how you get bold headers with lighter subtitles, category groupings, and multi-color text in a single cell.

```xml
<!-- Product box with bold name + gray subtitle -->
<mxCell id="rt-fw" value="&lt;b&gt;Mosaic AI Agent Framework&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#888888&quot;&gt;Orchestrator · Tool use&lt;/font&gt;"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1B3A4B;strokeWidth=1.5;fontSize=10;verticalAlign=middle;align=center;"
  vertex="1" parent="1">
  <mxGeometry x="210" y="126" width="220" height="52" as="geometry"/>
</mxCell>
```

```xml
<!-- Data Sources with category headers — NEVER use plain text lists -->
<mxCell id="ds" value="&lt;b style=&quot;font-size:12px;letter-spacing:1px&quot;&gt;DATA SOURCES&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#8AABB5&quot;&gt;&lt;b&gt;User Interactions&lt;/b&gt;&lt;br&gt;Chat · Voice · Events&lt;/font&gt;&lt;br&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;color:#8AABB5&quot;&gt;&lt;b&gt;Enterprise Systems&lt;/b&gt;&lt;br&gt;CRM · ERP · EHR&lt;/font&gt;"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1B3A4B;strokeColor=#1B3A4B;fontColor=#FFFFFF;fontSize=10;verticalAlign=middle;align=center;spacing=6;"
  vertex="1" parent="1">
  <mxGeometry x="10" y="100" width="140" height="300" as="geometry"/>
</mxCell>
```

**Rule:** If a box contains more than 3 items, use HTML formatting with category headers in a lighter color. Plain text lists inside colored boxes look like MS Word copy-paste.

### Step Indicator with Action Label (Paired Pattern)
Every numbered step circle MUST have a companion italic action label positioned 12-14px above it. The circle tells you the ORDER, the label tells you WHAT HAPPENS.

```xml
<!-- Step circle -->
<mxCell id="n1" value="①"
  style="ellipse;whiteSpace=wrap;html=1;fillColor=#1B3A4B;strokeColor=#1B3A4B;fontColor=#FFFFFF;fontSize=11;fontStyle=1;verticalAlign=middle;align=center;"
  vertex="1" parent="1">
  <mxGeometry x="473" y="160" width="24" height="24" as="geometry"/>
</mxCell>

<!-- Action label (12px above the circle) -->
<mxCell id="lbl-1" value="&lt;i&gt;session resolve&lt;/i&gt;"
  style="text;html=1;align=center;verticalAlign=bottom;resizable=0;points=[];autosize=0;strokeColor=none;fillColor=none;fontSize=8;fontColor=#1B3A4B;"
  vertex="1" parent="1">
  <mxGeometry x="455" y="146" width="60" height="12" as="geometry"/>
</mxCell>
```

### Capability Strip (Cap Row)
A text row above a hero element that lists product capabilities. Adds marketing messaging without cluttering the main boxes.

```xml
<mxCell id="caps" value="Lakebase  ·  INSTANT BRANCHING · AUTO-SCALING · OAUTH TOKEN ROTATION · ACID TRANSACTIONS"
  style="text;html=1;align=center;verticalAlign=top;resizable=0;points=[];autosize=0;strokeColor=none;fillColor=none;fontSize=9;fontColor=#1B3A4B;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="525" y="92" width="440" height="14" as="geometry"/>
</mxCell>
```

### Left Accent Bars
Color-coded 6px bars on the left edge of list items or slabs. Creates visual hierarchy and scanability.

```xml
<!-- Accent bar (same y and height as the slab it decorates) -->
<mxCell id="lb-a1" value=""
  style="rounded=0;whiteSpace=wrap;html=1;fillColor=#0A6EBD;strokeColor=none;"
  vertex="1" parent="1">
  <mxGeometry x="528" y="150" width="6" height="50" as="geometry"/>
</mxCell>
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
- **Keep node labels concise.** Product names only: 1-3 words per node (e.g., "Mosaic AI", "Databricks SQL", "Auto Loader"). Never put schemas, column names, SQL snippets, or multi-sentence descriptions inside a node box. If a node needs a qualifier, use one line max: "Lakebase\npgvector" — not a paragraph. Technical detail belongs in the companion guide, not the diagram.
- **Use built-in cloud icons, branded rectangles for Databricks.** Document icon swaps in the companion guide.

---

## Output Convention

**Write path:** `Artifacts/{account-slug}/diagrams/{YYYY-MM-DD}-{slug}.drawio`
- Lucid copy: `Artifacts/{account-slug}/diagrams/{YYYY-MM-DD}-{slug}-lucid.drawio`
- Guide: `Artifacts/{account-slug}/diagrams/{YYYY-MM-DD}-{slug}-guide.md`
- Cross-account diagrams: `Artifacts/_cross/diagrams/`
- Internal diagrams: `Artifacts/_internal/diagrams/`

**Account slugs** (active): `nwm`, `chn`. Load from `_System/account-slugs.yaml`.

**Frontmatter** — embed in the `-guide.md` file (the .drawio is binary-equivalent, so guide.md IS the sidecar):
```yaml
---
artifact_id: "{account}-diagram-{YYYY-MM-DD}-{slug}"
account: "{slug}"
artifact_type: "diagram"
title: "{human title}"
created: "YYYY-MM-DD"
source_skill: "arch-diagram"
related_session: null
---
```

**After save:** Call `vault_reindex(full=false, embed=false)`.

**Example:**
```
Artifacts/nwm/diagrams/2026-04-14-epic-integration-architecture.drawio
Artifacts/nwm/diagrams/2026-04-14-epic-integration-architecture-lucid.drawio
Artifacts/nwm/diagrams/2026-04-14-epic-integration-architecture-guide.md  ← has frontmatter
```

---

## Anti-Patterns

- **Using this skill for quick sketches** — use the `diagram` skill instead. This skill's XML output is heavy for a Slack message.
- **Forgetting the governance bar** — every Databricks diagram needs it. Check before saving.
- **Generic product names** — "ETL" instead of "Lakeflow Jobs" breaks the Databricks brand voice. "Reverse ETL" instead of "DeltaSync" is a third-party term.
- **Nodes without coordinates** — auto-placed nodes defeat the purpose. Every mxGeometry needs x and y.
- **Plain text lists in colored boxes** — the #1 visual quality killer. "CRM, ERP, EHR, APIs, Chat, Voice" as plain text in a dark box looks like MS Word. Use HTML formatting with category headers and sub-items in a lighter color.
- **Step circles without action labels** — numbers alone force the viewer to read the companion guide to understand each step. Always pair with a short italic label.
- **draw.io-specific icons without a Lucid-clean copy** — `mxgraph.aws4.*` and `img/lib/azure2/*` shapes only render in draw.io. Always produce a `-lucid.drawio` variant with these stripped.

## Spatial Honesty

LLMs reliably produce structurally correct XML (all elements present, correct relationships, proper naming). LLMs struggle with spatial layout (overlaps, arrow routing, visual balance). This is a known limitation — structural eval pass rates hit 100%, visual layout evals hit 0-56%.

**The skill's contract:** Architecturally correct output with reasonable positioning. Final visual polish (pixel-perfect alignment, arrow path cleanup, breathing room adjustments) happens in draw.io or Lucid by a human. Do not promise pixel-perfect output. Do not iterate endlessly on spatial tweaks in XML — the tool is not designed for that.

---

*"Architecture is the decision. The diagram is the proof. The XML is the delivery vehicle."*
