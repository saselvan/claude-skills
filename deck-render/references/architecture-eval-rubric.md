# Architecture Diagram Visual Evaluation Rubric
# For use in the deck-render render→evaluate→fix loop
#
# PURPOSE: Claude Code's self-evaluation is broken. It checks "did things render"
# instead of "do they look right." This rubric converts visual quality into
# mechanical pass/fail checks that can be applied to a rendered thumbnail.
#
# WHEN TO USE: After every render of an architecture diagram slide.
# Read the rendered PNG, then run every check below. Any FAIL = fix and re-render.
#
# NOTE: Architecture diagrams should be generated using the diagram or arch-diagram
# skills and embedded as images. This rubric evaluates the rendered image regardless
# of how it was generated.

## How to evaluate

When you read the rendered PNG, do NOT just glance at it and say
"looks good." Instead, run every check below in order. Write out each check result
explicitly. If you catch yourself writing "PASS" without actually verifying the specific
thing described, you are cheating. Stop and look again.

---

## Check 0: Narrative Intent

Before evaluating any visual element, verify the diagram has a defined
narrative. Look for a comment block at the top of the rendering code or
the strategy notes with these three items:

1. **ARGUMENT:** What should the audience conclude from this diagram?
   One sentence. Must be a claim, not a description.
   - PASS: any statement that someone could disagree with
   - FAIL: "Shows the architecture of X" (that's a description)
   - FAIL: no argument defined

2. **STRUCTURE:** What spatial arrangement carries the argument?
   One sentence. Describes the layout logic, not the technology.
   - e.g., "Two zones side by side with opposing flows between them"
   - e.g., "Three columns showing redundancy across failure domains"
   - e.g., "Top-down tree showing ownership and isolation"
   - e.g., "Left-to-right pipeline showing transformation stages"
   - FAIL: no structure defined

3. **INVENTORY:** Every shape and every arrow on the diagram listed
   with what it represents and why it's on the slide. If you can't
   justify an element's presence in one sentence, remove it.
   - FAIL: an element on the rendered slide has no inventory entry
   - FAIL: an inventory entry has no corresponding rendered element

FAIL conditions:
- Any of the three items is missing
- Argument is descriptive rather than argumentative
- Rendered diagram contradicts the defined structure (e.g., structure
  says "opposing horizontal flows" but arrows route vertically)
- Orphan elements exist (rendered but not in inventory, or vice versa)

**This check gates all others.** If narrative intent is undefined or
the rendered diagram contradicts it, the diagram fails regardless
of how clean the layout is.

---

## Check 1: Containment

For EACH tier band or container (full-width rectangle, zone boundary, etc.):
- List every component that belongs to this container
- Is each component VISUALLY INSIDE the container? (component edges do not extend beyond container edges)
- Is the container label VISUALLY INSIDE the container and not overlapping any component?

FAIL conditions:
- Any component box/cylinder extends beyond its container boundary
- Any container label overlaps a component
- Any component appears to float between two containers

This is the most common failure. Components that overflow their container make the diagram
look broken even if the data is correct.

---

## Check 2: Label Placement Accuracy

For EACH flow label:
- What flow does this label describe?
- What two components does that flow connect?
- Is the label positioned ON or NEAR the arrow connecting those two components?
- Is the label NOT on or near a DIFFERENT component or flow?

FAIL conditions:
- A label is placed on or near a component it doesn't relate to
- A label is placed far from its arrow, near a different arrow
- Two labels overlap each other and are unreadable

This is the second most common failure. The routing math places labels at midpoints
that may not correspond to the visual location of the flow.

---

## Check 3: Overlap Detection

Scan the entire slide for ANY case where:
- Two text elements overlap (even partially)
- A text element overlaps a shape it doesn't belong to
- The legend overlaps any container or component
- An arrow overlaps a label it doesn't belong to
- Any element is clipped by the slide edge

FAIL conditions:
- Any overlap exists anywhere on the slide

The legend is the most common offender. It must be positioned in clear space,
not on top of the last tier.

---

## Check 4: Flow Correctness

For EACH flow arrow on the slide:
- What color is it?
- Trace it from start to end. What component does it start from? What component does it end at?
- Does that match the architecture being diagrammed? Do different flow types use distinct colors?
- Are any expected flows missing from the diagram?

FAIL conditions:
- An arrow connects two components that shouldn't be connected
- An arrow has the wrong color for its flow type
- An arrow is missing (a flow that should exist doesn't have a visible arrow)
- Different flow types use the same color (making them indistinguishable)

---

## Check 5: Corridor Separation

- Are different flow types visually separated?
- Do any flow arrows of different types cross each other?
- Zero crossings between different flow types is the target.

FAIL conditions:
- Flow arrows of different types cross each other unnecessarily
- Different flow types are interleaved rather than spatially grouped
- The diagram could be reorganized to eliminate crossings but wasn't

---

## Check 6: Visual Hierarchy

- Are boundary or tier labels visible and readable?
- Are they between every adjacent pair of zones/tiers?
- Are the container bands visually distinct from the slide background? (not the same shade)
- Is there a clear visual gap between each tier/zone?
- Is the title at the top of the slide, not overlapping any content?

FAIL conditions:
- Boundary labels are missing, invisible, or overlapping content
- Containers blend into the background (no contrast)
- Tiers/zones touch each other with no gap
- Title overlaps content

---

## Check 7: Readability at Presentation Size

Imagine this slide projected on a screen in a conference room:
- Can you read every component name?
- Can you read every flow label?
- Can you read every tier/zone label?
- Can you read the legend?
- Is any text smaller than ~9pt equivalent?

FAIL conditions:
- Any text is too small to read at projection size
- Any text is truncated (ends with "..." or is cut off by shape boundary)
- Any text uses a color that doesn't contrast with its background

---

## Check 8: Legend

- Does the legend exist?
- Is it in clear space (not overlapping any content)?
- Does it accurately represent the flow colors used in the diagram?
- Are the color swatches visually distinguishable from each other?

FAIL conditions:
- Legend missing
- Legend overlaps content
- Legend colors don't match actual arrow colors
- Legend is incomplete (missing a flow type that appears in the diagram)

---

## Scoring

Count PASS checks out of 9 total.

| Score | Verdict | Action |
|---|---|---|
| 9/9 | Ship it | Present to user |
| 7-8/9 | Close | Fix the failing checks, re-render, re-evaluate |
| 5-6/9 | Significant issues | Prioritize Check 0 (narrative) and Check 1 (containment) |
| 0-4/9 | Start over | Narrative or layout is fundamentally broken |

**Do not present to the user until you score 8/9 or higher.**

---

## Common Positioning Bugs and Fixes

### Legend overlaps last tier
The legend y-position is calculated relative to content height but doesn't account for
the last tier's actual bottom edge. Fix: calculate legend_y from the actual bottom of
the last tier band + padding, not from the content area height.

### Components overflow containers
Component y-position + component height > container y-position + container height.
Fix: clamp component dimensions to fit within container_y + container_h with padding.

### Labels on wrong components
Label x/y is calculated from flow midpoint, but the midpoint falls inside a different
component's bounding box. Fix: offset labels OUTSIDE all component bounding boxes.
Check every label position against every component bounding box — if it's inside
a box it doesn't belong to, shift it.

### Tier labels collide with flow labels
Both occupy the left side of the container band. Fix: reserve a label column on the far left
(inside the band, before the component zone) and ensure flow labels are placed in the
gutter or on the arrow, not in the label column.

### Middle tiers have no visible background
Only first and last tiers get background fills. Fix: ensure every tier gets a band background
shape, regardless of position.

---

## Integration with deck-render skill

After rendering any slide with an architecture diagram:
1. Read the rendered PNG
2. Run all 9 checks from this rubric (write out each result)
3. If any check FAILS: fix the issue, re-render, go to step 1
4. If 8/9+ PASS: include honest assessment in output, present to user

This rubric is NOT optional. Architecture diagrams are the highest-risk slide type
for visual quality issues. The default "looks reasonable" evaluation is insufficient.
