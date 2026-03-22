---
name: interactive-diagrams
version: "1.0"
description: "Interactive, clickable diagrams with zoom, pan, tooltips, and real-time updates. D3.js, Cytoscape.js, Vis.js. USE WHEN clickable, interactive, zooming, real-time updating, dashboard integration, network visualization, graph exploration."
---

# Interactive Diagrams

Build clickable, zoomable diagrams that respond to user interaction. Use when a static diagram isn't enough — e.g., exploring a large network, drilling into details, real-time metric updates, or dashboard embedding.

## Tool Selection

```
Large network / graph exploration?              → D3.js (force-directed, custom styling)
Biological networks (protein, gene)?            → Cytoscape.js (biological layout algorithms)
Workflow / state machine with interactions?     → Vis.js (timeline, network, hierarchy)
Real-time updating metrics dashboard?           → Chart.js + D3.js hybrid
Knowledge graph / entity relationships?         → Cytoscape.js or D3.js
Timeline or Gantt with drill-down?              → Vis.js Timeline
Simple tree structure + click to expand?        → D3.js Tree Layout
Fast, responsive, minimal dependencies?         → SVG + vanilla JS (event handlers)
```

**Default to D3.js** — most flexible, best documentation, performs well even with thousands of nodes. Use Cytoscape.js for specialized biological/network layouts. Vis.js for timeline / Gantt workflows.

## MCP / Library Support

The following libraries are available in Artifacts via CDN:
- **D3.js** — `https://cdnjs.cloudflare.com/ajax/libs/d3/7.x.x/d3.min.js`
- **Cytoscape.js** — `https://unpkg.com/cytoscape@latest/dist/cytoscape.min.js`
- **Vis.js** — `https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js`

No MCP integration required — use HTML canvas or SVG + JavaScript directly in React or HTML artifacts.

---

## Use Cases & Patterns

### 1. Network Topology (Data Platform)

**Scenario:** Visualize data flow between 50+ systems, show which are active/inactive, click to see lineage

**Libraries:** D3.js (force-directed) or Cytoscape.js  
**Interaction:** Click node → expand lineage, hover → show metrics

```html
<!-- Pseudocode example -->
<svg id="network"></svg>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
  const data = {
    nodes: [
      { id: 1, label: "S3", type: "storage", metrics: { size: "2.5TB", latency: "45ms" } },
      { id: 2, label: "Kafka", type: "ingestion", metrics: { throughput: "100k msg/s" } },
      { id: 3, label: "Databricks", type: "compute", metrics: { running_jobs: 12 } }
    ],
    links: [
      { source: 2, target: 1, label: "Write" },
      { source: 1, target: 3, label: "Read" }
    ]
  };

  // D3 force simulation with zoom/pan
  // Click node → show details in sidebar
  // Hover link → highlight path + show throughput
</script>
```

**Talking Points for Customers:**
- See all integrations at a glance
- Identify bottlenecks (high latency, low throughput)
- Drill into lineage (where did this data come from?)
- Monitor real-time health (red = error, green = healthy)

---

### 2. Data Lineage Explorer (Unity Catalog)

**Scenario:** Click table → see all upstream tables, downstream dashboards, and who has access

**Libraries:** D3.js Tree Layout or Cytoscape.js  
**Interaction:** Click node → expand children, right-click → show access control, hover → show data quality metrics

```html
<!-- Pseudocode -->
<div id="lineage-explorer"></div>
<script>
  const table = "prod.curated.patient_cohorts";
  
  // Fetch lineage from UC API
  fetch(`/api/lineage?table=${table}`)
    .then(r => r.json())
    .then(data => {
      // Render interactive tree:
      // - Upstream (sources): raw_patients, raw_claims, raw_labs
      // - Current: patient_cohorts
      // - Downstream: trial_ready_dataset, dashboard_metrics
      // 
      // Click any node → highlight path + show:
      //   - Schema
      //   - Last updated
      //   - Row count
      //   - Owner
      //   - Data quality expectations
      //   - Who can access (roles + users)
    });
</script>
```

**Databricks Integration:**
- Query Unity Catalog API for table lineage
- Show column-level lineage (which input columns feed this output column?)
- Display data quality expectations as nodes
- Overlay access control (role badges)

---

### 3. Real-Time Metrics Dashboard

**Scenario:** Show pipeline health: ingestion throughput, data quality score, job run times — all updating live

**Libraries:** D3.js + Chart.js or custom SVG  
**Interaction:** Hover bar → show tooltip, click bar → drill into job details, timeline slider → show metrics over time

```html
<!-- Pseudocode -->
<div id="dashboard">
  <div id="throughput-chart"></div>           <!-- Ingestion rate (msgs/sec) -->
  <div id="quality-gauge"></div>              <!-- Data quality %: green > 95%, yellow 80-95%, red < 80 -->
  <div id="job-timeline"></div>               <!-- Last 24h job runs, colored by status -->
  <div id="error-log"></div>                  <!-- Recent errors, click to drill -->
</div>

<script>
  // WebSocket to real-time metrics endpoint
  const ws = new WebSocket("wss://metrics.databricks.com/stream");
  
  ws.onmessage = (event) => {
    const metric = JSON.parse(event.data);
    
    // Update D3 charts:
    // - Throughput line chart (rolling 1h window)
    // - Quality gauge (spin to new %)
    // - Job timeline (append new bar)
    // - Error log (prepend new entry)
    
    // Color coding:
    // - Green: healthy (throughput stable, quality > 95%, no errors)
    // - Yellow: degraded (quality 80-95%, errors but recovering)
    // - Red: critical (quality < 80%, jobs failing)
  };
</script>
```

**Talking Points:**
- Ops team sees health at a glance (no manual log digging)
- Alert thresholds (auto-red when quality drops below 80%)
- Drill into failing job to see error + fix time
- Historical comparison (is today's performance better/worse than last week?)

---

### 4. Workflow State Explorer (DLT / Jobs)

**Scenario:** Show all pipeline stages, their dependencies, and which are blocked/running/failed

**Libraries:** Vis.js Network or D3.js  
**Interaction:** Click stage → expand tasks, hover → show run time + data quality expectations

```html
<!-- Pseudocode -->
<div id="workflow-explorer"></div>
<script>
  const workflow = {
    stages: [
      { id: 1, name: "Ingest", status: "success", duration: "2m", data_in: "500MB" },
      { id: 2, name: "Clean", status: "running", duration: "1m 30s so far", expectations: 3 },
      { id: 3, name: "Aggregate", status: "blocked", reason: "waiting for Clean", expectations: 5 }
    ],
    dependencies: [
      { from: 1, to: 2, label: "success → start" },
      { from: 2, to: 3, label: "success → start" }
    ]
  };

  // Render as interactive DAG:
  // - Green box: completed stage
  // - Blue box: running stage (progress bar inside)
  // - Gray box: blocked stage (tooltip explains why)
  // - Red box: failed stage (click → error details)
  //
  // Click stage → sidebar shows:
  //   - Task breakdown (map, filter, shuffle, etc.)
  //   - Input/output rows
  //   - Data quality expectations + pass/fail
  //   - Logs (tail last 100 lines)
</script>
```

---

### 5. Entity Resolution Visualization (Healthcare)

**Scenario:** Show patient deduplication: which records matched, confidence scores, which fields aligned

**Libraries:** D3.js or Cytoscape.js  
**Interaction:** Click match → highlight matched fields, adjust confidence threshold → redraw

```html
<!-- Pseudocode -->
<div id="entity-resolution"></div>
<script>
  // Left side: raw patient records (10k rows)
  // Right side: unified patient profiles (8.5k rows)
  // Middle: links showing which records merged
  //
  // Color intensity = match confidence (0-100%)
  // Width of link = number of matching fields
  //
  // Hover link → show:
  //   - Name match: "John Smith" == "Jon Smyth" (typo tolerance: 95%)
  //   - DOB match: "1980-01-15" == "1980-01-15" (exact: 100%)
  //   - Address match: "123 Main St, Boston" == "123 Main St, Boston, MA" (fuzzy: 98%)
  //
  // Slider: adjust confidence threshold (only show links > X%)
  // → Watch graph re-cluster in real time
</script>
```

**Use Case:**
- Reduce patient record duplication (medical records fragmented across labs)
- Verify matching logic before committing to database
- Highlight edge cases (ambiguous matches for manual review)

---

## Implementation Patterns

### Pattern 1: Force-Directed Graph (D3.js)

```javascript
// Minimal D3.js force-directed layout
const svg = d3.select("#network");
const width = 960, height = 600;

const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(80))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .on("tick", () => {
    // Update node and link positions
  });

// Zoom & pan
svg.call(d3.zoom().on("zoom", (e) => {
  g.attr("transform", e.transform);
}));

// Click interaction
node.on("click", (e, d) => {
  console.log("Clicked:", d.id);
  // Expand details sidebar
  // Highlight path to root
});
```

### Pattern 2: Cytoscape.js (Biological Networks)

```javascript
const cy = cytoscape({
  container: document.getElementById('cy'),
  elements: [
    { data: { id: 'a' } },
    { data: { id: 'b' } },
    { data: { source: 'a', target: 'b' } }
  ],
  layout: { name: 'cose' },  // or 'grid', 'circle', 'concentric'
  style: [
    {
      selector: 'node',
      style: {
        'background-color': '#555',
        'label': 'data(id)'
      }
    }
  ]
});

cy.on('tap', 'node', (e) => {
  const node = e.target;
  cy.elements().addClass('faded');
  node.predecessors().union(node).removeClass('faded');
});
```

### Pattern 3: Real-Time Updates (D3 + WebSocket)

```javascript
const lines = d3.select("#chart").selectAll("line");
const ws = new WebSocket("wss://metrics.example.com");

ws.onmessage = (event) => {
  const newData = JSON.parse(event.data);
  
  lines.data(newData, d => d.id)
    .join(
      enter => enter.append("line")
        .attr("x1", d => d.x1)
        .attr("y1", d => d.y1),
      update => update,
      exit => exit.remove()
    )
    .transition()
    .duration(500)
    .attr("x2", d => d.x2)
    .attr("y2", d => d.y2)
    .attr("stroke", d => d.healthy ? "green" : "red");
};
```

---

## Accessibility & Performance

### Performance Tips

- **Large graphs (>1000 nodes)**: Use WebGL rendering (Babylon.js) or pre-computed layouts instead of live simulation
- **Lazy load**: Only render visible nodes (use viewport clipping)
- **Debounce interactions**: Pan/zoom can fire 100s of times/sec — debounce updates to 16ms (60 FPS)
- **Worker threads**: Expensive calculations (layout, pathfinding) should run in Web Workers to avoid blocking UI

### Accessibility

- **Keyboard navigation**: Arrow keys to move between nodes, Enter to expand, Escape to deselect
- **Tooltips**: Always show on hover (not hover-only for mobile users)
- **Color + shape**: Use both (not color alone) to differentiate node types
- **Focus states**: Highlight focused node with thicker border + label display
- **Alt text**: For static export, always include `<img alt="Network showing X nodes, Y edges">`

---

## When to Use Interactive vs. Static

| Scenario | Use... | Why |
|---|---|---|
| 50+ nodes, user exploration expected | Interactive | Static becomes spaghetti |
| Executive slide, 10 minutes to understand | Static (Excalidraw) | Interactive distracts, interactive requires learning |
| Data lineage: user needs to drill by domain | Interactive | Domain filtering + drill-down essential |
| System architecture: "here's how it's built" | Static (D2 or C4) | Static is faster to consume |
| Real-time monitoring dashboard | Interactive | Must update live, users expect interactivity |
| Network topology: find the bottleneck | Interactive | Users need to explore, filter, highlight paths |
| Compliance audit trail: show lineage | Static | Auditors want a fixed, printable record |

---

## Common Gotchas

1. **Too many nodes, no filtering** — Force simulation becomes unresponsive. Add a search or filter UI to show only relevant nodes.

2. **Real-time updates without cleanup** — Old data points accumulate → memory leak. Always `.remove()` exited selections.

3. **Colors without labels** — Users can't distinguish node types if color-blind. Use shape + size + label.

4. **No zoom to fit** — Users get lost in large graphs. Add "Zoom to fit" button + double-click node to zoom in.

5. **Mobile-hostile** — Touch events aren't the same as mouse events. Use `d3.pointer()` instead of `d3.mouse()` (deprecated).

---

## Databricks Integration Examples

### Example 1: Live Ingestion Throughput

```javascript
// Real-time pipeline health dashboard
setInterval(async () => {
  const response = await fetch(
    "https://databricks.example.com/api/latest/pipelines/{pipeline_id}/updates"
  );
  const update = await response.json();
  
  // Update D3 bar chart with latest throughput
  d3.select("#throughput")
    .datum(update.bytes_processed)
    .transition()
    .duration(1000)
    .attr("width", d => scale(d));
}, 5000);  // Poll every 5 seconds
```

### Example 2: Click Table → Show Lineage

```javascript
// Unity Catalog lineage explorer
async function showLineage(tableName) {
  const response = await fetch(
    `https://databricks.example.com/api/lineage?table=${tableName}`
  );
  const lineage = await response.json();
  
  // Render interactive tree with D3
  // Click upstream table → fetch its lineage recursively
}
```

### Example 3: Quality Expectations as Nodes

```javascript
// Show data quality expectations in pipeline DAG
const stageNodes = pipeline.stages.map(stage => ({
  id: stage.id,
  label: stage.name,
  color: stage.status === "success" ? "green" : "red",
  expectations: stage.expectations.map(e => ({
    name: e.name,
    pass_rate: e.pass_rate  // e.g., 99.5%
  }))
}));

// On click, show expectations as nested nodes or sidebar list
```

---

## Output & Embedding

**React Artifact:**
```jsx
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function InteractiveLineage() {
  const svgRef = useRef();
  
  useEffect(() => {
    if (!svgRef.current) return;
    
    // Fetch lineage data
    // Render D3 diagram
    // Attach event handlers
  }, []);
  
  return <svg ref={svgRef}></svg>;
}
```

**HTML Artifact:**
```html
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
  <style>
    #network { border: 1px solid #ccc; }
  </style>
</head>
<body>
  <svg id="network"></svg>
  <script>
    // D3 code here
  </script>
</body>
</html>
```

---

## References & Resources

- **D3.js**: https://d3js.org/ (force-directed, tree, sunburst layouts)
- **Cytoscape.js**: https://js.cytoscape.org/ (biological networks, specialized layouts)
- **Vis.js**: https://visjs.org/ (timeline, network, Gantt)
- **Observable**: https://observablehq.com/ (live D3 examples, fork & modify)
- **D3 Gallery**: https://observablehq.com/@d3/gallery (500+ examples)

---

*"The most effective diagrams are interactive. Static diagrams work great for slides. Interactive diagrams work great for exploration."*

**See also:** diagram skill for static, presentation-ready architecture diagrams.
