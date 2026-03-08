# D2 Architecture Diagram Rules v2.0
## With Mandatory Pre-Flight Checklist and Edge Management

Created: 2026-02-28
Version: 2.0 (incorporates post-mortem from Lakebase diagram failure)

---

## ⛔ MANDATORY: Render-Review-Fix Loop (PROCESS GATE)

> **This section is not a reference. It is a gate. Do not present any diagram to the user until every checkbox passes. No exceptions.**

### Step 1: Pre-Render Source Audit

Before running `d2 --layout=elk`, audit the `.d2` source file:

| # | Check | Threshold | Action if Failed |
|---|---|---|---|
| 1a | Count total edges | ≤8 (single-column), ≤10 (single-row), ≤15 (multi-column grid), ≤20 (split corridor) | Consolidate parallel edges or split into multiple diagrams |
| 1b | Count parallel edges (same source type → same target type, same semantic) | If ≥3 parallel edges of same meaning | Consolidate into 1 edge with multiplicity label: `{label: "archive (3x)"}` |
| 1c | Check for layer-skipping edges | Any edge connecting non-adjacent layers | Add pass-through routing nodes in intermediate layers, or use bus notation |
| 1d | **Corridor assignment** (see below) | Every flow type has a dedicated spatial region | Restructure D2 source to enforce corridors |
| 1e | **Layout-argument alignment** | The D2 `direction` matches the architecture type (see design-thinking Phase 1 Decision Matrix). Layered/tiered architectures MUST use `direction: down` even when targeting slides. Pipeline architectures use `direction: right`. | If direction is `right` but architecture is layered → FAIL. Switch to wide-tier vertical. See design-thinking "Adapting for Slide Format" section. |

#### Step 1d: Corridor Assignment Verification (MANDATORY)

This is where most diagrams fail. Claude Code correctly consolidates edges but then lets ELK route all flows through the same visual column. You must **structurally enforce** corridor separation in the D2 source — ELK will not do it for you.

**Procedure:**

1. List every flow type in the diagram (e.g., writes, reads, storage ops)
2. Assign each flow to a corridor:

| Flow Priority | Corridor Assignment (Vertical Layout) | Corridor Assignment (Horizontal Layout) |
|---|---|---|
| Primary write path | LEFT side of each tier container | TOP of each tier container |
| Primary read path | RIGHT side of each tier container | BOTTOM of each tier container |
| Async/background (archive, sync) | FAR RIGHT edge, outside main containers | FAR BOTTOM, outside main containers |

3. **Enforce corridors structurally in D2 using zone containers:**

```d2
# MANDATORY PATTERN: Use invisible zone containers to pin flows to corridors

compute_tier: {
  direction: right

  # LEFT ZONE: write-path components
  write_zone: {
    label: ""
    style.fill: "transparent"
    style.stroke: "transparent"

    rw_compute: "R/W Compute"
  }

  # RIGHT ZONE: read-path components
  read_zone: {
    label: ""
    style.fill: "transparent"
    style.stroke: "transparent"

    replicas: "Read Replicas (3x)" {shape: cylinder}
  }
}

# Write edges connect from write_zone components
compute_tier.write_zone.rw_compute -> consensus_tier.safekeepers: "writes" {
  style.stroke: "#FF3621"
}

# Read edges connect from read_zone components
compute_tier.read_zone.replicas -> cache_tier.pageservers: "reads" {
  style.stroke: "#00CC66"
}
```

4. **Verify corridor separation in source code:**
   - Grep all edges with write color (`#FF3621`). Do they ALL originate from `write_zone` or left-side components? If any originate from `read_zone` → FAIL.
   - Grep all edges with read color (`#00CC66`). Do they ALL originate from `read_zone` or right-side components? If any originate from `write_zone` → FAIL.
   - Grep all async/dashed edges. Do they route to the far edge (right in vertical, bottom in horizontal)? If they cross through the center → FAIL.

5. **If a component receives BOTH writes and reads** (e.g., Pageservers receive WAL stream AND serve reads):
   - The component lives in CENTER, spanning both corridors
   - Write edges enter from the LEFT
   - Read edges enter from the RIGHT
   - This is architecturally accurate — shared infrastructure should be visually centered

**Why zone containers SHOULD work:** ELK respects container membership for node placement — in theory. In practice, transparent/invisible containers are unreliable. ELK may collapse, ignore, or reposition them unpredictably.

**⚠️ ELK ZONE CONTAINER RELIABILITY:**

Invisible zone containers (`style.fill: "transparent"; style.stroke: "transparent"`) fail approximately 50% of the time. ELK treats them as zero-size hints rather than layout constraints.

**Mandatory fallback order:**

1. **First attempt:** Use visible zone containers with subtle styling (not transparent). Give them a label, a faint fill, and a 1px stroke. ELK respects containers it considers "real."

```d2
write_zone: {
  label: "Write Path"
  style: {
    fill: "#0F1A20"       # Near-canvas color, barely visible but ELK sees it
    stroke: "#1A2A33"     # Faint border
    stroke-width: 1
    font-color: "#4A5A66" # Muted label
    font-size: 11
  }
}

read_zone: {
  label: "Read Path"
  style: {
    fill: "#0F1A20"
    stroke: "#1A2A33"
    stroke-width: 1
    font-color: "#4A5A66"
    font-size: 11
  }
}
```

2. **If zones still collapse:** Use explicit `width` and `height` on zone containers to prevent ELK from collapsing them. Set zone width to at least the sum of child component widths + padding.

```d2
write_zone: {
  label: "Write Path"
  width: 250    # Force minimum size
  height: 140
  style.fill: "#0F1A20"
  style.stroke: "#1A2A33"
}
```

3. **If ELK still won't cooperate:** Abandon zone containers entirely. Instead, use **two separate tier containers** side by side for each layer — one for write-path components, one for read-path components. Connect them with invisible edges to force horizontal alignment.

```d2
direction: down

# Instead of one compute_tier with zones, use two side-by-side containers
compute_write: {
  label: "Compute — Write Path"
  rw_compute: "R/W Compute\n\n• Auto-scale\n• Scale-to-zero"
}

compute_read: {
  label: "Compute — Read Path"
  direction: right
  replica1: "Replica 1" {shape: cylinder}
  replica2: "Replica 2" {shape: cylinder}
  replica3: "Replica 3" {shape: cylinder}
}

# Force horizontal alignment
compute_write -> compute_read: {style.opacity: 0}
```

4. **Nuclear option — post-render manual check:** If after 2 render attempts the corridors are not separated, STOP trying to fix it in D2. Instead:
   - Render the best version you have
   - In your assessment to the user, explicitly state: "ELK placed the read and write paths in the same corridor. D2/ELK cannot enforce spatial separation for this topology. Recommend manual adjustment in a vector editor, or switching to a simpler topology with fewer edge types."
   - Do NOT present a diagram with crossed critical paths and claim it passes the checklist.

### Step 2: Post-Render Visual Audit

After running `d2 --layout=elk --theme=200`, open the PNG and evaluate:

| # | Check | Threshold | Action if Failed |
|---|---|---|---|
| 2a | Count edge crossings | Max 5 total, **0 on critical paths** | Restructure layout. Add spatial separation. Consolidate edges. |
| 2b | **Corridor verification** | Write edges (red) are all on the LEFT half. Read edges (green) are all on the RIGHT half. Async edges (dashed) are on the FAR edge. | If any flow is in the wrong corridor → escalate through the fallback order in Step 1d: (1) visible zones, (2) explicit zone sizing, (3) split tier containers, (4) acknowledge ELK limitation to user. Max 2 re-render attempts before escalating to next fallback. |
| 2c | Critical path isolation | For EACH flow type: trace the path end-to-end. Does your eye cross a line of a different color at any point? | If YES → FAIL. The corridors are not separated. Revisit 1d. |
| 2d | Bottom-half independence | Cover top 40%. Is bottom 60% readable on its own? | If NO → FAIL. Redistribute or simplify. |
| 2e | Whitespace between layers | Visible gap between every layer container | If layers touch → FAIL. Add padding. |
| 2f | Label anchoring | Every flow label is attached to its edge, not floating in space | If any label floats → fix edge label placement |
| 2g | Figure-ground contrast | Layer backgrounds visibly distinct from canvas | If layers disappear → increase fill opacity by 20%+ |
| 2h | Visual star prominence | The diagram's key argument (e.g., scaling boundaries) is the most visually prominent element after components | If the argument is invisible or the smallest element → enlarge, increase contrast, or reposition |

### Step 3: Iterate or Ship

- **Any checkbox fails** → revise `.d2` source, re-render, re-audit. Do not present.
- **All checkboxes pass** → present to user.
- **Never trust the layout engine.** ELK optimizes topology (minimize edge length), not visual clarity (path isolation, crossing elimination). You must verify visually.

---

## Edge Management Rules

### Rule 21: Edge Budget by Layout Type

| Layout | Max Edges | Rationale |
|---|---|---|
| Vertical single-column | 8 | All flows compete for one narrow corridor |
| Horizontal single-row | 10 | Slightly more routing room |
| Multi-column grid (2+ columns) | 15 | Flows can route through separate channels |
| Split corridor (write-left, read-right) | 20 | Dedicated corridors per flow type |

**Enforcement:** Count edges in `.d2` source before rendering. If over budget, apply Rule 22 or switch to split corridor layout.

**Default recommendation:** If the architecture has ≥2 distinct flow types (e.g., writes + reads), start with split corridor layout. Do not attempt single-column.

### Rule 22: Parallel Edge Consolidation (3+ Rule)

If ≥3 edges share the same:
- Source type (e.g., all Safekeepers)
- Target type (e.g., all → Object Storage)
- Semantic meaning (e.g., all are "archive")

Then consolidate into ONE edge with a multiplicity label.

```d2
# BAD: 3 individual lines
safekeeper_1 -> object_storage: {label: "archive"; style.stroke-dash: 5}
safekeeper_2 -> object_storage: {label: "archive"; style.stroke-dash: 5}
safekeeper_3 -> object_storage: {label: "archive"; style.stroke-dash: 5}

# GOOD: 1 consolidated edge from tier container
safekeeper_tier -> object_storage: {
  label: "archive (3x AZ)"
  style: {
    stroke: "#FFAB00"
    stroke-width: 2
    stroke-dash: 5
  }
}
```

**Alternative — Bus notation** for when the source tier needs to fan out to multiple targets:

```d2
# BUS PATTERN: Single visual element represents multiplexed flow
wal_bus: {
  label: "WAL Stream (3x AZ replication)"
  shape: rectangle
  width: 400
  height: 30
  style: {
    fill: "transparent"
    stroke: "#FFAB00"
    stroke-width: 2
    stroke-dash: 5
  }
}

safekeeper_tier -> wal_bus
wal_bus -> pageserver_tier: {label: "replay"}
wal_bus -> object_storage: {label: "archive"}
```

### Rule 23: Edge Crossing Hard Limit

- **Max 5 crossings** per diagram total
- **Zero crossings** on critical data paths (write path, read path)
- **Enforcement:** After first render, count crossings. If >5, redesign — don't adjust cosmetics.

### Rule 24: Critical Path Isolation Test

For each semantic flow type in the diagram:

1. Mentally (or physically) trace the path from source to destination
2. Does your eye cross a line of a **different color or style**?
3. If YES → the paths are not isolated → FAIL

**Resolution options:**
- Spatially separate flow types (write-left, read-right)
- Use bus notation to reduce individual line count
- Split into separate diagrams per flow type

### Rule 25: Layer-Skip Routing

Edges between non-adjacent layers (e.g., Compute → Storage, skipping Consensus and Cache) create long lines that cross through intermediate layers.

**Options:**
- Add pass-through nodes in intermediate layers (even if logically unnecessary)
- Route edge labels around containers, not through them
- If the skip represents a real architectural concern (e.g., reads bypass WAL), call it out visually with a dedicated corridor on the diagram's edge

```d2
# BAD: Long line from top to bottom, crossing through intermediate layers
rw_compute -> object_storage: "reads"

# GOOD: Explicit routing through intermediary
rw_compute -> pageserver_cache: "page request"
pageserver_cache -> object_storage: "cache miss → fetch"
```

### Rule 26: Bottom-Half Independence Test

Cover the top 40% of the rendered diagram. Evaluate the bottom 60% alone:

- Can you identify every component?
- Can you trace every flow?
- Is there visible whitespace between elements?

If NO to any → the diagram fails. Bottom-heavy diagrams lose executives who stop scanning halfway down.

---

## Spatial Separation Patterns

### Pattern A: Write-Left, Read-Right

Use when a system has distinct write and read paths that share storage.

```
┌─────────────────────────────────────────────┐
│              WRITE PATH (left)    READ PATH (right)     │
│                                                          │
│   ┌─────────┐                    ┌──────────┐           │
│   │ R/W     │                    │ Replicas │           │
│   │ Compute │                    │ (1,2,3)  │           │
│   └────┬────┘                    └────┬─────┘           │
│        │ writes                       │ reads            │
│        ▼                              │                  │
│   ┌─────────┐                         │                  │
│   │ WAL     │ ──── WAL stream ───►    │                  │
│   │ Consens.│                         │                  │
│   └────┬────┘                         │                  │
│        │ archive                      ▼                  │
│        │                         ┌──────────┐           │
│        │                         │Pageserver│           │
│        │                         │ (Cache)  │           │
│        │                         └────┬─────┘           │
│        │ persist                      │ persist          │
│        ▼                              ▼                  │
│   ┌─────────────────────────────────────────┐           │
│   │           Object Storage                 │           │
│   └─────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

D2 implementation:

```d2
direction: down

compute_layer: {
  direction: right
  write_side: {
    rw_compute: "R/W Compute\n\n• Auto-scale\n• Scale-to-zero"
  }
  read_side: {
    direction: right
    replica1: "Replica 1" {shape: cylinder}
    replica2: "Replica 2" {shape: cylinder}
    replica3: "Replica 3" {shape: cylinder}
  }
}

consensus_layer: {
  # Only on the write side — reads don't touch WAL
  direction: right
  safekeeper1: "Safekeeper AZ-1"
  safekeeper2: "Safekeeper AZ-2"
  safekeeper3: "Safekeeper AZ-3"
}

cache_layer: {
  # Only on the read side — writes don't touch page cache
  pageserver: "Pageservers\n(Page Cache)"
}

storage_layer: {
  object_storage: "Object Storage\n\n• Immutable pages\n• 30-day retention" {
    shape: cylinder
  }
}

# WRITE PATH (left side, red)
compute_layer.write_side.rw_compute -> consensus_layer.safekeeper2: {
  label: "writes"
  style.stroke: "#FF3621"
  style.stroke-width: 3
}

# WAL consensus (orange, within layer)
consensus_layer.safekeeper2 -> consensus_layer.safekeeper1: {
  label: "Paxos 2/3"
  style.stroke: "#FFAB00"
  style.stroke-width: 2
}
consensus_layer.safekeeper2 -> consensus_layer.safekeeper3: {
  style.stroke: "#FFAB00"
  style.stroke-width: 2
}

# WAL stream + archive (consolidated, orange)
consensus_layer -> cache_layer.pageserver: {
  label: "WAL stream (3x)"
  style.stroke: "#FFAB00"
  style.stroke-width: 2
  style.stroke-dash: 5
}
consensus_layer -> storage_layer.object_storage: {
  label: "archive (3x)"
  style.stroke: "#FFAB00"
  style.stroke-width: 2
  style.stroke-dash: 5
}

# READ PATH (right side, green)
compute_layer.read_side.replica1 -> cache_layer.pageserver: {
  style.stroke: "#00CC66"
  style.stroke-width: 2
}
compute_layer.read_side.replica2 -> cache_layer.pageserver: {
  label: "reads"
  style.stroke: "#00CC66"
  style.stroke-width: 2
}
compute_layer.read_side.replica3 -> cache_layer.pageserver: {
  style.stroke: "#00CC66"
  style.stroke-width: 2
}

# Storage persist (orange)
cache_layer.pageserver -> storage_layer.object_storage: {
  label: "persist"
  style.stroke: "#FFAB00"
  style.stroke-width: 2
}
```

**Edge count: 10** (within budget for a layout with spatial separation)
**Crossings: 0** (write path and read path don't share a corridor)

### Pattern B: Bus Backbone

Use when a single tier fans out to multiple downstream targets.

```d2
# Instead of 6 individual lines from 3 safekeepers to 2 targets:
wal_distribution: {
  label: "WAL Distribution Bus"
  shape: rectangle
  height: 30
  style.fill: "transparent"
  style.stroke: "#FFAB00"
  style.stroke-dash: 5
}

consensus_tier -> wal_distribution: {label: "WAL (3x AZ)"}
wal_distribution -> cache_tier: {label: "replay"}
wal_distribution -> storage_tier: {label: "archive"}
```

---

## Core Design Principles (Reference)

### 1. Clarity Over Completeness
- Goal: Immediate comprehension, not exhaustive detail
- Remove unnecessary elements that don't serve the diagram's purpose
- If something can be implied by a label or multiplicity notation, don't draw it individually

### 2. Consistency Is Critical
- Use commonly accepted symbols: cylinder = data, rectangle = service, circle = external
- Maintain uniform shapes, colors, and line styles throughout
- Define classes at the top of the `.d2` file and apply consistently

### 3. Layered Architecture Pattern
- **Top-down vertical flow**: User-facing → Logic → Data
- **Horizontal within layers**: Components at same abstraction level
- **Clear separation**: Each layer has distinct responsibility
- **Direction hints**: `direction: down` global, `direction: right` within layers

### 4. Size Indicates Importance
- Primary components: 20-30% larger than secondary
- Same-role components: identical size (signals equivalence)
- Different-role components: different sizes (signals hierarchy)

### 5. Strategic Whitespace
- Macro whitespace: generous space between layers
- Micro whitespace: minimal space between same-group elements
- Use container `padding` and explicit `width`/`height` to control

### 6. Color With Purpose
- Assign distinct colors to data flow types (write, read, sync, archive)
- Use color to differentiate layers (compute, consensus, storage)
- Consistent palette across all diagrams

```d2
vars: {
  write_flow: "#FF3621"    # RED
  read_flow: "#00CC66"     # GREEN
  sync_flow: "#FFAB00"     # AMBER
  admin_flow: "#4A90E2"    # BLUE
}
```

### 7. Line Weight Indicates Importance
- Critical path: 3-4px stroke width
- Standard flow: 2px stroke width
- Background/optional: 1-2px, dashed

### 8. Figure-Ground Separation
- Layer backgrounds must be 20%+ more opaque than canvas
- Calculate: convert hex → RGB, multiply each channel by 1.2, convert back

### 9. Every Diagram Needs
- Title (plain text, no decorative box)
- Legend (edge-aligned, not floating)
- Clear component labels
- Flow labels on every edge

### 10. Minimize Visual Clutter
- Layer labels: muted gray, not bright accent colors
- Maximize data-ink ratio: if removing an element doesn't reduce understanding, remove it
- No decorative borders around titles

---

## D2 Technical Patterns

### Direction Control
```d2
direction: down          # Global: vertical layers
layer: {
  direction: right       # Local: horizontal within layer
}
```

### Shape Vocabulary
| Shape | Use For |
|---|---|
| `cylinder` | Databases, storage, data repositories |
| `rectangle` | Services, applications, processes |
| `circle` | External systems, endpoints, actors |
| `cloud` | External cloud services |
| `text` | Legend items, annotations |

### Stroke Patterns
| Pattern | Meaning |
|---|---|
| Solid | Active, primary path |
| Dashed (`stroke-dash: 5`) | Background, async, eventual |
| Dotted (`stroke-dash: 2`) | Future/planned |

### ELK Layout Engine
Always use ELK for architecture diagrams:
```bash
d2 --layout=elk --theme=200 input.d2 output.png
```

ELK provides better layer separation and orthogonal routing than dagre, but **does not guarantee zero crossings**. You must verify visually.

---

## Quality Checklist (Final Gate)

Before presenting any diagram:

- [ ] Edge count within budget (Rule 21)
- [ ] Parallel edges consolidated (Rule 22)
- [ ] Edge crossings ≤5, zero on critical paths (Rule 23)
- [ ] Each flow type traceable without visual interference (Rule 24)
- [ ] No layer-skipping edges without routing (Rule 25)
- [ ] Bottom half independently readable (Rule 26)
- [ ] Render-review-fix loop completed (Step 1-3 above)
- [ ] Title present (plain text)
- [ ] Legend present (edge-aligned)
- [ ] All labels anchored (not floating)
- [ ] Consistent shape vocabulary
- [ ] Figure-ground contrast sufficient
- [ ] Whitespace between all layers

---

## Post-Mortem Reference: Lakebase v1 Failure Analysis

The original Lakebase diagram scored 4/10 due to:
- 17 edges in a single-column layout (budget: 8)
- 17 edge crossings (limit: 5)
- Zero critical path isolation (writes, reads, and storage ops all shared one corridor)
- Bottom 60% unreadable
- No render-review loop executed

Root cause: **Process failure.** The rules existed but were not applied as a checklist. The layout engine was trusted to solve visual problems it cannot solve. The diagram was shipped without visual audit.

This v2 document places the mandatory process gate at the top to prevent recurrence.

---

**Version**: 2.0
**Last Updated**: 2026-02-28
**Tool**: D2 with ELK layout engine
**Render command**: `d2 --layout=elk --theme=200 input.d2 output.png`
