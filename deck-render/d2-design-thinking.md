# D2 Architecture Diagram Design Thinking
## How to Design Diagrams That Make Arguments, Not Just Show Topology

Created: 2026-02-28
Companion to: d2-architecture-rules-v2.md (mechanical checklist)

---

## ⛔ MANDATORY: Read This BEFORE Writing Any D2 Code

The mechanical rules (edge budgets, crossing limits, checklists) prevent bad diagrams.
This document produces *good* diagrams.

A good architecture diagram is not a graph visualization. It is a **visual argument**.
Before writing a single line of D2, you must answer three questions:

1. **What is the architectural insight?** (What makes this architecture worth diagramming?)
2. **Who is the audience?** (What do they already know? What do they need to learn?)
3. **What is the one thing they should remember?** (The takeaway after 5 seconds)

If you cannot answer all three, stop and ask the user.

---

## Phase 0: Discover the Argument

### The Architecture Insight Question

Every system architecture exists because of a set of design decisions. The diagram's job is to make those decisions visible and comprehensible.

**Before drawing, ask yourself:**

| Question | What It Determines |
|---|---|
| What scales independently? | Where to draw scaling boundaries |
| What is decoupled from what? | Where to draw tier separations |
| What is the failure domain? | How to group components |
| What is the data gravity? | Where to anchor the diagram (storage usually at bottom) |
| What is novel vs commodity? | What to emphasize vs minimize |

**Example — Lakebase:**
- Insight: Compute is fully decoupled from storage. Each tier scales independently.
- Audience: Healthcare CTOs evaluating database platforms.
- Takeaway: "Every layer scales independently — you pay only for what you use."
- Therefore: The diagram must make **scaling boundaries** the visual star, not data flow arrows.

**Example — FHIR Integration Pipeline:**
- Insight: Raw HL7/FHIR data lands in bronze, gets harmonized to OMOP in silver, serves analytics from gold.
- Audience: Health system data engineers.
- Takeaway: "Medallion architecture gives you auditability at every stage."
- Therefore: The diagram must make **the three stages** visually dominant, with data lineage flowing through them.

**Example — Multi-Cloud DR:**
- Insight: Active-active across two regions with RPO < 1 minute.
- Audience: CISO and compliance team.
- Takeaway: "No single region failure can cause data loss."
- Therefore: The diagram must make **the two regions** visually symmetric, with replication as the connecting element.

### Anti-Pattern: Topology-First Thinking

**WRONG process (what produces bad diagrams):**
1. List all components
2. List all connections
3. Draw boxes and arrows
4. Hope it communicates something

**RIGHT process (what produces good diagrams):**
1. Identify the architectural argument
2. Choose a layout that makes the argument visible
3. Determine which components support the argument
4. Draw only what serves the argument
5. Verify the argument is visible in 5 seconds

---

## Phase 1: Choose the Layout Pattern

The layout is not an aesthetic choice. It encodes meaning. Choose the layout that matches the argument.

### Pattern Library

#### Vertical Stack (Top-Down)
**Use when the argument is about:** layers, tiers, abstraction levels, durability gradients, trust boundaries

```
    ┌─────────────┐
    │  Clients    │  ← least durable, most ephemeral
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  Compute    │  ← stateless, scales horizontally
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  Consensus  │  ← stateful, fixed size
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  Storage    │  ← most durable, cheapest per GB
    └─────────────┘
```

**Mental model it invokes:** "The deeper you go, the more durable and persistent."
**Best for:** Database architectures, data platforms, security models.
**Lakebase uses this** because the argument is about decoupled tiers.

#### Horizontal Pipeline (Left-to-Right)
**Use when the argument is about:** data transformation, ETL stages, request lifecycle, time progression

```
    ┌─────┐    ┌─────────┐    ┌────────┐    ┌────────┐
    │Ingest│───►│Transform│───►│Enrich  │───►│ Serve  │
    └─────┘    └─────────┘    └────────┘    └────────┘
```

**Mental model it invokes:** "Data flows left to right, getting refined at each stage."
**Best for:** Medallion architecture, CI/CD pipelines, data processing.
**Lakebase should NOT use this** because it implies sequential processing, not independent tiers.

#### Hub and Spoke
**Use when the argument is about:** a central platform connecting many systems, integration, interoperability

```
              ┌───────┐
              │Epic   │
              └───┬───┘
                  │
    ┌─────┐   ┌──┴───┐   ┌──────┐
    │Lab  ├───┤ FHIR ├───┤Claims│
    └─────┘   │ Hub  │   └──────┘
              └──┬───┘
                  │
              ┌───┴───┐
              │Genomics│
              └───────┘
```

**Mental model it invokes:** "Everything connects through one platform."
**Best for:** Integration architectures, data mesh, platform pitch decks.

#### Symmetric Mirror
**Use when the argument is about:** redundancy, disaster recovery, active-active, before/after comparison

```
    ┌──── Region A ────┐     ┌──── Region B ────┐
    │  ┌────┐ ┌─────┐  │     │  ┌────┐ ┌─────┐  │
    │  │App │ │ DB  │  │◄───►│  │App │ │ DB  │  │
    │  └────┘ └─────┘  │     │  └────┘ └─────┘  │
    └──────────────────┘     └──────────────────┘
```

**Mental model it invokes:** "If one side fails, the other is identical."
**Best for:** DR architectures, compliance diagrams, A/B comparisons.

#### Nested Boundaries
**Use when the argument is about:** security zones, trust boundaries, network segmentation, compliance scope

```
    ┌─── Public Internet ──────────────────────┐
    │                                           │
    │  ┌─── DMZ ────────────────────────┐      │
    │  │                                 │      │
    │  │  ┌─── Private Subnet ───────┐  │      │
    │  │  │                           │  │      │
    │  │  │  ┌─── HIPAA Enclave ──┐  │  │      │
    │  │  │  │   PHI Data Store   │  │  │      │
    │  │  │  └────────────────────┘  │  │      │
    │  │  └───────────────────────────┘  │      │
    │  └─────────────────────────────────┘      │
    └───────────────────────────────────────────┘
```

**Mental model it invokes:** "Each boundary adds a layer of protection."
**Best for:** HIPAA compliance, zero-trust architectures, network diagrams.

### Decision Matrix

| Your Argument Is About... | Use Layout | Direction in D2 |
|---|---|---|
| Tiers / layers / durability | Vertical Stack | `direction: down` |
| Data transformation / pipeline | Horizontal Pipeline | `direction: right` |
| Central platform / integration | Hub and Spoke | Custom positioning |
| Redundancy / DR / comparison | Symmetric Mirror | `direction: right` with two containers |
| Security / compliance / trust | Nested Boundaries | Nested containers |
| Independent scaling | Vertical Stack + scaling boundary markers | `direction: down` |

### Adapting for Slide Format (16:9)

**Common request:** "Make it fit a slide." This does NOT mean "rotate the diagram to horizontal."

Rotating a vertical-stack architecture to horizontal changes its meaning — it reads as a pipeline instead of layers. The layout encodes the argument (Phase 1). Changing the layout to fit a slide destroys the argument.

**Instead, use a compressed vertical layout within a wide canvas:**

#### Strategy: Wide Tiers, Short Stack

Keep `direction: down` but make each tier wide and short instead of narrow and tall.

```
┌──────────────────── 16:9 SLIDE CANVAS ────────────────────┐
│                                                            │
│  ┌─ Compute (scales to zero) ──────────────────────────┐  │
│  │  R/W Compute    Replica 1   Replica 2   Replica 3   │  │
│  └─────────────────────────────────────────────────────┘  │
│                    ── scales independently ──               │
│  ┌─ WAL Consensus (fixed size) ────────────────────────┐  │
│  │         Safekeepers (Paxos 2/3, 3x AZ)              │  │
│  └─────────────────────────────────────────────────────┘  │
│                    ── scales independently ──               │
│  ┌─ Page Cache (scales with read load) ────────────────┐  │
│  │            Pageservers (Multi-AZ Cache)              │  │
│  └─────────────────────────────────────────────────────┘  │
│                    ── scales independently ──               │
│  ┌─ Persistent Storage (99.999999999% Durability) ─────┐  │
│  │            Object Storage (immutable pages)          │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Why this works:**
- Preserves the vertical layered argument (durability increases downward)
- Scaling boundaries remain horizontal separators between tiers (visual star intact)
- Wide tiers fill the 16:9 canvas without wasted horizontal space
- Corridors still work: write path on the left of each tier, read path on the right
- Components within each tier spread horizontally (using `direction: right` inside tier containers)

**D2 implementation for slide format:**

```d2
direction: down

# Make tier containers wide by giving components explicit widths
# and using direction: right to spread them horizontally

compute_tier: {
  label: "Compute Layer (Scales to Zero)"
  direction: right

  write_zone: {
    label: "Write Path"
    width: 250
    style: {
      fill: "#0F1A20"
      stroke: "#1A2A33"
      stroke-width: 1
      font-color: "#4A5A66"
      font-size: 11
    }

    rw_compute: "R/W Compute\n\n• Auto-scale\n• Scale-to-zero" {
      width: 220
      height: 100
    }
  }

  read_zone: {
    label: "Read Path"
    direction: right
    width: 500
    style: {
      fill: "#0F1A20"
      stroke: "#1A2A33"
      stroke-width: 1
      font-color: "#4A5A66"
      font-size: 11
    }

    replica1: "Replica 1" {shape: cylinder; width: 140; height: 80}
    replica2: "Replica 2" {shape: cylinder; width: 140; height: 80}
    replica3: "Replica 3" {shape: cylinder; width: 140; height: 80}
  }
}

# Scaling boundary (visual star)
sb1: "── scales independently ──" {shape: text; style.font-color: "#6B7B8D"}

consensus_tier: {
  label: "WAL Consensus Layer (Fixed Size)"
  safekeepers: "Safekeepers (Paxos 2/3, 3x AZ)" {width: 400; height: 80}
}

sb2: "── scales independently ──" {shape: text; style.font-color: "#6B7B8D"}

cache_tier: {
  label: "Page Cache Layer (Scales with Read Load)"
  pageservers: "Pageservers (Multi-AZ Cache)" {width: 400; height: 80}
}

sb3: "── scales independently ──" {shape: text; style.font-color: "#6B7B8D"}

storage_tier: {
  label: "Persistent Storage (99.999999999% Durability)"
  object_storage: "Object Storage\n• Immutable pages\n• 30-day retention" {
    shape: cylinder; width: 400; height: 100
  }
}
```

**Render command for slide-optimized output:**
```bash
# Render at 16:9 aspect ratio
d2 --layout=elk --theme=200 input.d2 output.png
# Then crop/resize to 1920x1080 or 3840x2160 for slide import
```

#### When Horizontal IS Appropriate

Use horizontal layout ONLY when the architecture's argument is sequential/pipeline:

| Architecture | Argument | Layout |
|---|---|---|
| Lakebase (decoupled tiers) | Independent scaling | **Vertical** (even on slides) |
| Medallion (bronze/silver/gold) | Data refinement stages | Horizontal ✓ |
| CI/CD pipeline | Sequential stages | Horizontal ✓ |
| Request lifecycle | Time progression | Horizontal ✓ |
| FHIR-to-OMOP harmonization | Transformation pipeline | Horizontal ✓ |

**Rule:** If the user asks to "make it fit a slide" or "make it horizontal," check the decision matrix first. If the architecture is a layered stack, use the wide-tier vertical strategy instead. If the architecture is genuinely a pipeline, horizontal is correct.

---

## Phase 2: Identify the Visual Star

Every diagram has one visual element that carries the argument. Everything else is supporting context.

### What Is the Visual Star?

| Architecture Type | Visual Star | How to Emphasize |
|---|---|---|
| Decoupled tiers (Lakebase) | **Scaling boundaries** between tiers | Dashed separator lines with labels like "scales independently" |
| Medallion architecture | **The three stages** (bronze/silver/gold) | Large containers with distinct colors per stage |
| Integration platform | **The central hub** | Largest element, thickest borders, all spokes point to it |
| DR architecture | **The replication link** | Bold bidirectional arrow between mirrored regions |
| Security architecture | **The innermost boundary** | Strongest border, most contrast, smallest area |

### Anti-Pattern: Everything Is Equally Important

If every box is the same size, same color, same border weight — nothing is important. The eye has nowhere to land. The viewer must read every label to understand the diagram.

**Rule:** One visual star per diagram. 2-3 supporting elements. Everything else is context.

### D2 Implementation: Scaling Boundaries as Visual Star

```d2
# Scaling boundary = the argument made visible
scaling_boundary_1: {
  label: "── scales independently ──"
  shape: text
  style: {
    font-size: 12
    font-color: "#6B7B8D"
    italic: true
  }
}

# Place between tiers
compute_tier -> scaling_boundary_1: {style.opacity: 0}
scaling_boundary_1 -> consensus_tier: {style.opacity: 0}
```

---

## Phase 3: Spatial Separation of Flow Types

### The Corridor Rule

If a diagram has multiple flow types (write, read, sync, admin), each type must have its own **spatial corridor** — a region of the diagram that belongs exclusively to that flow.

**Why:** Human vision tracks motion along paths. If two paths cross, the eye loses tracking. Spatial separation prevents this.

**This is not optional.** If your architecture has ≥2 flow types, you MUST use zone containers to enforce corridors. See `d2-architecture-rules-v2.md → Step 1d` for the mechanical enforcement procedure.

### The Default: Write-Left, Read-Right

Unless you have a specific reason to do otherwise, use this corridor assignment:

| Corridor | Position (Vertical Layout) | Position (Horizontal Layout) | Assigned Flows |
|---|---|---|---|
| Write corridor | LEFT side of each tier | TOP of each tier | All write-path edges (red) |
| Read corridor | RIGHT side of each tier | BOTTOM of each tier | All read-path edges (green) |
| Async corridor | FAR RIGHT edge | FAR BOTTOM edge | Archive, sync, background ops (dashed) |
| Shared components | CENTER | CENTER | Components that participate in both paths |

### Why This Default Works

It mirrors how we read architecture:
- **Vertical layout:** Left = "input/write" (we read left-to-right, writes come first). Right = "output/read" (reads are the result).
- **Shared infrastructure** (Pageservers, Object Storage) sits in the center because it's architecturally shared — and visually, the center is where write and read paths converge.

### D2 Enforcement: Zone Containers

You enforce corridors by wrapping components in zone containers within each tier.

**CRITICAL: Do NOT use invisible/transparent zone containers.** ELK frequently ignores containers with `style.fill: "transparent"` and `style.stroke: "transparent"`. Instead, use near-canvas-colored zones that are barely visible to humans but structurally real to ELK. See `d2-architecture-rules-v2.md → Step 1d fallback order` for the full escalation path when ELK doesn't cooperate.

```d2
direction: down

# Every tier gets write_zone (left) and read_zone (right)
compute_tier: {
  direction: right

  write_zone: {
    label: "Write Path"
    width: 250
    style: {
      fill: "#0F1A20"
      stroke: "#1A2A33"
      stroke-width: 1
      font-color: "#4A5A66"
      font-size: 11
    }

    rw_compute: "R/W Compute\n\n• Auto-scale\n• Scale-to-zero" {
      style.stroke: "#FF6B35"
      style.stroke-width: 3
    }
  }

  read_zone: {
    label: "Read Path"
    direction: right
    width: 500
    style: {
      fill: "#0F1A20"
      stroke: "#1A2A33"
      stroke-width: 1
      font-color: "#4A5A66"
      font-size: 11
    }

    replica1: "Replica 1" {shape: cylinder}
    replica2: "Replica 2" {shape: cylinder}
    replica3: "Replica 3" {shape: cylinder}
  }
}

# Consensus tier: ONLY on write path (reads don't touch WAL)
consensus_tier: {
  # No read_zone needed — this tier is write-only
  safekeepers: "Safekeepers\n(Paxos 2/3, 3x AZ)"
}

# Cache tier: receives from BOTH paths, so it's centered
cache_tier: {
  pageservers: "Pageservers\n(Multi-AZ Cache)"
}

# Storage tier: receives from BOTH paths, centered
storage_tier: {
  object_storage: "Object Storage\n\n• Immutable pages\n• 30-day retention" {shape: cylinder}
}

# WRITE PATH: all red edges stay LEFT
compute_tier.write_zone.rw_compute -> consensus_tier.safekeepers: {
  label: "writes"
  style.stroke: "#FF3621"
  style.stroke-width: 3
}

# READ PATH: all green edges stay RIGHT
compute_tier.read_zone.replica1 -> cache_tier.pageservers: {
  style.stroke: "#00CC66"
  style.stroke-width: 2
}
compute_tier.read_zone.replica2 -> cache_tier.pageservers: {
  label: "reads"
  style.stroke: "#00CC66"
  style.stroke-width: 2
}
compute_tier.read_zone.replica3 -> cache_tier.pageservers: {
  style.stroke: "#00CC66"
  style.stroke-width: 2
}

# STORAGE OPS: WAL stream enters cache from left, archive goes far right
consensus_tier.safekeepers -> cache_tier.pageservers: {
  label: "WAL stream (3x AZ)"
  style.stroke: "#FFAB00"
  style.stroke-width: 2
}
consensus_tier.safekeepers -> storage_tier.object_storage: {
  label: "archive (3x AZ)"
  style.stroke: "#FFAB00"
  style.stroke-width: 2
  style.stroke-dash: 5
}
cache_tier.pageservers -> storage_tier.object_storage: {
  label: "persist"
  style.stroke: "#FFAB00"
  style.stroke-width: 2
}
```

**Key insight:** The write path (red) flows down from `write_zone` on the LEFT through Safekeepers. The read path (green) flows down from `read_zone` on the RIGHT to Pageservers. They never cross because they originate from opposite sides of each tier. Storage ops (amber) flow down the center/right because they connect consensus → cache → storage.

### Self-Check After Writing D2 Source

Before rendering, verify in the source code:

1. Every edge with `stroke: "#FF3621"` (write) originates from a `write_zone` or left-positioned component
2. Every edge with `stroke: "#00CC66"` (read) originates from a `read_zone` or right-positioned component
3. Every dashed edge routes to/from far-edge components, not through the center corridor
4. Components that receive both writes and reads are NOT inside a zone — they're in the tier root (centered)

If any of these fail, fix the source before rendering. Do not hope ELK will route around the problem.

### Corridor Assignment Strategy (Custom)

For non-standard architectures, assign corridors by priority:

1. **Identify all flow types** in the architecture
2. **Rank by importance** to the argument
3. **Assign corridors:**
   - Most important flow: left corridor (vertical) or top corridor (horizontal) — this is where the eye starts
   - Second most important: right corridor (vertical) or bottom corridor (horizontal)
   - Background/async flows: outer edges of the diagram
   - Admin/control plane: separate diagram or muted overlay

### Example — Lakebase Corridor Result

With zone containers enforced:
- **Write path (red):** R/W Compute (left) → Safekeepers → WAL stream → Pageservers (enters from left) → Object Storage
- **Read path (green):** Read Replicas (right) → Pageservers (enters from right) → Object Storage
- **Archive (dashed amber):** Safekeepers → Object Storage (routes down center-right, no crossing)
- **Zero crossings** because write and read originate from opposite sides of the compute tier

### D2 Implementation

```d2
direction: down

compute_tier: {
  direction: right
  
  write_zone: {
    label: "Write Path"
    width: 250
    style: {
      fill: "#0F1A20"
      stroke: "#1A2A33"
      stroke-width: 1
      font-color: "#4A5A66"
      font-size: 11
    }

    rw_compute: "R/W Compute\n\n• Auto-scale\n• Scale-to-zero" {
      style.fill: "#1B3139"
      style.stroke: "#FF6B35"
      style.stroke-width: 3
    }
  }

  read_zone: {
    label: "Read Path"
    direction: right
    width: 500
    style: {
      fill: "#0F1A20"
      stroke: "#1A2A33"
      stroke-width: 1
      font-color: "#4A5A66"
      font-size: 11
    }

    replica1: "Replica 1" {shape: cylinder}
    replica2: "Replica 2" {shape: cylinder}
    replica3: "Replica 3" {shape: cylinder}
  }
}
```

---

## Phase 4: Component Selection — What to Include

### The Argument Filter

For every component in the real architecture, ask:

1. **Does it support the argument?** If yes → include.
2. **Is it necessary context?** If yes → include but de-emphasize (smaller, muted color).
3. **Is it neither?** → Exclude. It belongs in a different diagram.

### Example — Lakebase

| Component | Supports Argument? | Include? | Visual Treatment |
|---|---|---|---|
| R/W Compute | Yes — shows compute tier | Yes | Primary size, accent border |
| Read Replicas | Yes — shows horizontal scaling | Yes | Primary size, peer of R/W |
| Safekeepers (3x AZ) | Yes — shows consensus tier | Yes | Medium size, consolidated |
| Pageservers | Yes — shows cache tier | Yes | Medium size |
| Object Storage | Yes — shows durable storage | Yes | Primary size (it's where data lives) |
| Monitoring/metrics | No | No | Separate observability diagram |
| Load balancer | Context only | Maybe | Small, muted, if audience cares |
| Network topology | No | No | Separate network diagram |
| Auth/IAM | No | No | Separate security diagram |

### Anti-Pattern: Kitchen Sink Diagram

Including everything guarantees nothing is clear. A diagram with 20+ components communicates one thing: "this system is complex." That is never the argument you want to make.

**Rule:** Max 8-10 components per diagram. If you need more, you need multiple diagrams at different abstraction levels (C4 model: Context → Container → Component → Code).

---

## Phase 5: Annotation Strategy

### Labels Should Explain WHY, Not Just WHAT

**Bad label:** "PostgreSQL"
**Good label:** "PostgreSQL\n(Source of Truth)"

**Bad label:** "Safekeepers"
**Good label:** "Safekeepers\n(Paxos 2/3, 3x AZ)"

**Bad label:** "writes"
**Good label (on a scaling-focused diagram):** "writes\n(scales with compute)"

The label should reinforce the argument. If the argument is about scaling, labels mention scaling. If the argument is about durability, labels mention replication factors. If the argument is about compliance, labels mention data classification.

### Annotation Placement Rules

| Annotation Type | Placement | D2 Implementation |
|---|---|---|
| Component purpose | Inside the box, below name | Multi-line label: `"Name\n\n• Detail 1\n• Detail 2"` |
| Flow description | On the edge | Edge label: `a -> b: {label: "writes (SQL)"}` |
| Architectural insight | Between tiers | Text shape: `{shape: text; label: "scales independently"}` |
| Scaling info | Inside tier container label | Container label: `"Compute Tier (scales to zero)"` |
| Quantity/multiplicity | On consolidated edge or in component | `"Safekeepers (3x AZ)"` or `{label: "archive (3x)"}` |

---

## Phase 6: Audience-Specific Adaptation

### The Same Architecture, Different Arguments

The same system may need different diagrams for different audiences. The architecture doesn't change — the argument does.

#### For a CTO / VP Engineering
**Argument:** "This architecture reduces operational burden and cost."
**Emphasize:** Scale-to-zero, managed services, independent scaling
**De-emphasize:** Internal component details, replication mechanics
**Layout:** High-level vertical stack, scaling boundaries prominent

#### For a Data Engineer
**Argument:** "Here's how data flows through the system and where to find it."
**Emphasize:** Data flow paths, storage formats, access patterns
**De-emphasize:** Infrastructure scaling, AZ distribution
**Layout:** Horizontal pipeline or detailed vertical with flow annotations

#### For a Security/Compliance Officer
**Argument:** "PHI is protected at every layer with encryption and access controls."
**Emphasize:** Encryption boundaries, access control points, audit logging
**De-emphasize:** Performance characteristics, scaling mechanics
**Layout:** Nested boundaries with trust zones

#### For a Solutions Architect (Peer)
**Argument:** "Here are the interesting design decisions and tradeoffs."
**Emphasize:** Consensus protocol choice, cache invalidation strategy, durability guarantees
**De-emphasize:** Basic components (they know what a load balancer is)
**Layout:** Detailed vertical stack with technical annotations

### D2 Adaptation Pattern

```d2
# CTO version: high-level, scaling-focused
compute: "Compute\n(scales to zero)" { width: 300; height: 120 }
storage: "Durable Storage\n(99.999999999% durability)" { width: 300; height: 120 }

# Engineer version: detailed, flow-focused
compute: {
  direction: right
  rw: "R/W Compute" { width: 150 }
  r1: "Replica 1" { width: 120; shape: cylinder }
  r2: "Replica 2" { width: 120; shape: cylinder }
  r3: "Replica 3" { width: 120; shape: cylinder }
}
```

---

## Decision Flowchart: From Request to Diagram

```
User says "draw me an architecture diagram"
           │
           ▼
   ┌───────────────────────┐
   │ What is the system?   │
   │ What is the argument? │
   │ Who is the audience?  │
   └───────────┬───────────┘
               │
         Can you answer all 3?
        ┌──────┴──────┐
        │ NO          │ YES
        ▼             ▼
   Ask the user    Choose layout pattern
                   (Phase 1 Decision Matrix)
                       │
                       ▼
                  Identify visual star
                  (Phase 2)
                       │
                       ▼
                  Assign flow corridors
                  (Phase 3)
                       │
                       ▼
                  Filter components
                  (Phase 4: max 8-10)
                       │
                       ▼
                  Write D2 source
                       │
                       ▼
               ┌───────────────────┐
               │ Run Pre-Render    │
               │ Audit (Rules v2)  │
               │ Edge budget?      │
               │ Parallel edges?   │
               │ Layer skips?      │
               └───────┬───────────┘
                       │
                  Render with ELK
                       │
                       ▼
               ┌───────────────────┐
               │ Run Post-Render   │
               │ Audit (Rules v2)  │
               │ Crossings?        │
               │ Path isolation?   │
               │ Bottom-half test? │
               └───────┬───────────┘
                       │
                  All pass?
               ┌───────┴───────┐
               │ NO            │ YES
               ▼               ▼
          Revise D2       Present to user
          Re-render       with honest assessment
```

---

## Common Healthcare Architecture Patterns

These are patterns you will encounter repeatedly in HLS contexts.

### Epic Integration Architecture
**Argument:** "Databricks connects to Epic data without disrupting clinical workflows."
**Layout:** Horizontal pipeline (Epic Clarity/Caboodle → Bronze → Silver → Gold)
**Visual Star:** The medallion stages
**Key Components:** Epic source systems, FHIR API, landing zone, harmonization layer, analytics layer
**Audience-Specific:** For Epic analysts, show Clarity vs Caboodle. For executives, show "Epic" as one box.

### FHIR-to-OMOP Harmonization
**Argument:** "Raw clinical data becomes research-ready through automated harmonization."
**Layout:** Horizontal pipeline with validation checkpoints
**Visual Star:** The transformation step (FHIR → OMOP mapping)
**Key Components:** FHIR server, raw FHIR store, mapping engine, OMOP CDM tables, quality checks

### Clinical Data Platform (Multi-Source)
**Argument:** "One platform unifies all clinical data sources."
**Layout:** Hub and spoke (Databricks lakehouse as hub)
**Visual Star:** The central lakehouse
**Key Components:** Epic, claims, labs, imaging, genomics all feeding into one platform

### Real-Time Hospital Operations
**Argument:** "Streaming data enables real-time operational decisions."
**Layout:** Horizontal pipeline with a streaming backbone
**Visual Star:** The streaming layer (Kafka/Event Hub) as a horizontal bus
**Key Components:** ADT feeds, bed sensors, staffing system, command center dashboard

---

## Failure Mode Reference

These are the specific ways architecture diagrams fail. Check each one.

| Failure Mode | Symptom | Root Cause | Fix |
|---|---|---|---|
| Spaghetti | Lines cross everywhere | Too many edges, no spatial separation | Consolidate edges, assign corridors |
| Topology dump | Correct but meaningless | No argument, just components and connections | Start over with Phase 0 |
| Kitchen sink | 20+ components, nothing stands out | No component filtering | Apply Phase 4 argument filter |
| Wrong layout | Pipeline for a layered system | Layout doesn't match argument | Revisit Phase 1 decision matrix |
| Everything equal | All boxes same size/color | No visual hierarchy | Apply Phase 2 visual star |
| Floating labels | Labels near but not on elements | D2 edge labels not used properly | Attach labels to edges and components |
| Trust the engine | Rendered without reviewing | Skipped post-render audit | Always run the checklist |

---

**Version**: 1.0
**Last Updated**: 2026-02-28
**Companion**: d2-architecture-rules-v2.md (mechanical checklist)
**Usage**: Read Phase 0-2 before writing any D2. Reference Phase 3-6 during design. Run mechanical checklist during render.
