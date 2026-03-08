# Architecture Diagram Quality Gate

**Purpose:** Objective rubric for evaluating technical architecture diagrams before delivery.

**Sources:**
- [Atlassian Architecture Diagram Best Practices](https://www.atlassian.com/work-management/project-management/architecture-diagram)
- [IBM Design Language – Technical Diagrams](https://www.ibm.com/design/language/infographics/technical-diagrams/design/)
- [The Art and Science of Architecture Diagrams | Catio](https://www.catio.tech/blog/the-art-and-science-of-architecture-diagrams)
- [Visual Hierarchy in Design - MasterClass](https://www.masterclass.com/articles/visual-hierarchy)
- [Creating Beautiful Diagrams for Presentations | SlideModel](https://slidemodel.com/how-to-create-beautiful-diagrams-for-presentations/)
- [Symmetry in Graphic Design | Canva](https://www.canva.com/learn/symmetry-graphic-design/)

---

## The 10-Point Quality Gate

### 1. **5-Second Clarity Test**
✅ Pass: Can someone unfamiliar with the system identify the main components and data flow in 5 seconds?
❌ Fail: Requires 30+ seconds to understand basic structure

**Why it matters:** "Architecture diagrams should be easy to digest, so keep things relatively simple and visually clean" (Atlassian). A cluttered diagram forces cognitive overload.

**Fix:** Simplify. Remove decorative elements. Group related components into labeled clusters.

---

### 2. **Visual Hierarchy (Primary → Secondary → Tertiary)**
✅ Pass: Clear focal point (largest/boldest), supporting elements (medium), details (small)
❌ Fail: All elements same size/weight, or random sizing

**Why it matters:** "Hierarchical relationships are crucial for organizing and understanding complex systems" (Catio). Visual hierarchy guides the viewer's eye through the narrative.

**Test:** Squint at the diagram. Can you still identify the most important component?

**Fix:**
- Primary components: Larger boxes, bolder borders, brighter colors
- Secondary: Medium size, standard borders
- Tertiary: Smaller, lighter colors, thinner lines

---

### 3. **Grid Alignment**
✅ Pass: All elements align to an invisible grid (edges, centers, baselines consistent)
❌ Fail: Elements positioned randomly with inconsistent spacing

**Why it matters:** "Poor spacing and inconsistent alignment break visual harmony... misaligned shapes imply a lack of attention" (UXPin). Audiences may not consciously notice alignment, but they sense disorganization.

**Test:** Draw imaginary vertical/horizontal lines through element edges. Do they align?

**Fix:** Use a grid system. Snap all elements to 0.25" or 0.5" increments.

---

### 4. **Strategic Whitespace**
✅ Pass: Consistent spacing between elements (e.g., 0.5" gaps), breathing room around clusters
❌ Fail: Cramped areas next to vast empty spaces, or uniform density everywhere

**Why it matters:** "Whitespace reduces cognitive load by approximately 25%" (vFunction). Whitespace isn't wasted space—it's structural.

**Test:** Measure gaps between adjacent elements. Are they consistent?

**Fix:** Define spacing rules (e.g., 0.3" between related elements, 0.8" between clusters).

---

### 5. **Symmetry & Balance**
✅ Pass: Visual weight evenly distributed (not all content on one side)
❌ Fail: Diagram feels "lopsided" or top-heavy

**Why it matters:** "Symmetry evens out the visual weight so our eyes are not drawn to one element in particular" (Canva). Balance creates calm; imbalance creates tension.

**Test:** Cover half the diagram. Is the other half proportionally similar?

**Fix:** Distribute components symmetrically, or use asymmetric balance (large element left = multiple small elements right).

---

### 6. **Color With Purpose**
✅ Pass: Colors indicate meaning (e.g., red=compute, blue=storage, green=data flow)
❌ Fail: Random colors, or color used only for decoration

**Why it matters:** "Color schemes should remain stable and predictable, with hues relating to the information being conveyed" (Atlassian). 92% of experts advocate for consistent symbol reuse.

**Test:** Remove color. Does the diagram still work? If yes, color adds meaning. If no, you're relying on color to convey structure (risky for colorblind viewers).

**Fix:** Use color to reinforce categories already clear from position/labels. Limit palette to 3-5 colors.

---

### 7. **Self-Explanatory Labels**
✅ Pass: Every component labeled clearly; arrows labeled with purpose; legend if needed
❌ Fail: Unlabeled boxes, ambiguous arrows ("connects to"), missing legend for color/icon meaning

**Why it matters:** "Make your diagrams self-explanatory with clear and concise text annotations" (IBM). "Everything should be clearly labeled so stakeholders know what they're looking at" (vFunction).

**Test:** Show diagram to someone unfamiliar. Can they explain it without your help?

**Fix:** Label every box, arrow, and cluster. Use a legend for color/line style meanings.

---

### 8. **Logical Flow (Left-to-Right or Top-to-Bottom)**
✅ Pass: Data/process flows in a consistent direction (LR or TB), minimal arrow crossings
❌ Fail: Arrows loop back, cross frequently, or flow in contradictory directions

**Why it matters:** "Use logical grouping and clear layers to show how components interact" (Catio). Crossed arrows force the viewer to trace paths mentally (cognitive load).

**Test:** Count arrow crossings. 0-2 = excellent, 3-5 = acceptable, 6+ = redesign needed.

**Fix:** Reorder components to minimize crossings. Use "through" edges sparingly.

---

### 9. **Minimal Complexity (Every Element Earns Its Place)**
✅ Pass: Removing any element would lose critical information
❌ Fail: Decorative icons, redundant labels, or over-detailed components for this audience

**Why it matters:** "Avoid over-complication and keep the diagram as simple as possible while conveying the necessary details" (vFunction). "Diagrams exist to reduce cognitive effort" (SlideModel).

**Test:** Remove one element. Did you lose essential information? If no, delete it.

**Fix:** Tailor detail to audience. Executives get high-level (3-5 boxes), architects get component-level (10-15 boxes).

---

### 10. **Professionalism Check (Would This Work in a Board Deck?)**
✅ Pass: Clean typography, professional color palette, consistent styling, no pixelated images
❌ Fail: Comic Sans, garish colors, mismatched fonts, low-res icons, "MS Paint feel"

**Why it matters:** "Visually compelling designs improve information retention by up to 65%" (Atlassian). Poor aesthetics signal carelessness, undermining technical credibility.

**Test:** Screenshot the diagram. Would you put this in a deck for your CEO?

**Fix:**
- Use system fonts (Arial, Helvetica, Segoe UI) or brand fonts
- Stick to muted professional colors (#0B2026, #FF6B35, #FFAB00)
- Use vector icons or high-DPI PNGs (200+ DPI)
- Ensure consistent line weights (1pt, 2pt, 3pt—no random thicknesses)

---

## Scoring System

**Pass = 8+/10 criteria met**
**Acceptable (with caveats) = 6-7/10**
**Reject = <6/10**

---

## Common Failure Modes & Fixes

| Failure Mode | Root Cause | Fix |
|--------------|------------|-----|
| "Looks like Graphviz auto-layout" | Uneven spacing, random positioning | Manually adjust node positions or use strict grid |
| "Too busy" | Too many components for one view | Split into multiple diagrams (L1 overview, L2 detail) |
| "Arrows everywhere" | Poor ordering or bidirectional dependencies | Reorder components to create linear flow |
| "Can't tell what's important" | All elements same size | Apply visual hierarchy (size, color, weight) |
| "Looks amateurish" | Inconsistent fonts, misaligned boxes, random colors | Apply grid alignment, standardize palette/typography |

---

## Application to Current Lakebase Diagram

**Iteration 2 Scorecard:**

1. 5-Second Clarity: ✅ PASS (Computes left, Storage right is clear)
2. Visual Hierarchy: ⚠️ PARTIAL (All components similar size—no clear focal point)
3. Grid Alignment: ❌ FAIL (Replicas/Safekeepers not aligned horizontally)
4. Strategic Whitespace: ⚠️ PARTIAL (Some areas cramped, others sparse)
5. Symmetry & Balance: ✅ PASS (Relatively balanced left-right)
6. Color With Purpose: ✅ PASS (Red=writes, Green=reads, Yellow=storage)
7. Self-Explanatory Labels: ✅ PASS (All components labeled)
8. Logical Flow: ⚠️ PARTIAL (Some arrow crossings on archive paths)
9. Minimal Complexity: ✅ PASS (Every element necessary)
10. Professionalism: ❌ FAIL (Graphviz auto-layout look, not presentation-ready)

**Score: 5.5/10 - REJECT** (needs iteration 3)

**Priority fixes:**
1. Manual positioning to fix alignment (#3)
2. Size variation to establish hierarchy (#2)
3. Cleaner arrow routing (#8)
4. Professional polish (#10)

---

## When to Accept "Good Enough"

**For internal technical docs:** 6/10 acceptable
**For customer-facing presentations:** 8/10 minimum
**For board/executive decks:** 9+/10 required

**Reality check:** Graphviz auto-layout diagrams typically max out at 6-7/10. To reach 8+, manual design in PowerPoint/Figma is usually required.

---

**Last Updated:** 2026-02-28
**Author:** Architecture Diagram Research (via WebSearch synthesis)
