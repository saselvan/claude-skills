# Slide Evaluation Checklist

Re-read this before every per-slide evaluation. Emit the EVAL and TRANSITION blocks exactly as shown.

## Per-Slide Checks

After rendering and converting to PNG, verify each:

| Check | What to Verify | FAIL if... |
|---|---|---|
| S1-Hierarchy | One hero element 2-3x larger than everything else. Squint test: blur vision, can you tell what's important? Title is insight-driven ("Unity Catalog unifies governance") not descriptive ("Architecture Overview"). | Multiple elements compete. No clear focal point. Title is just a topic label. |
| S2-Density | Count content chunks — within budget? Exec: 3-4, Technical: 5-7, BDR: 2-3, Mixed: 3-4. Max acronyms: 2 (exec), 4 (technical). | Chunk count exceeds budget. Acronym soup. Nested sub-sub-bullets. |
| S5-Taste | No accent line under titles. No centered body text. No equal-weight colors. No icon walls (6 icons in 2 rows). No gradient backgrounds. Magazine test: would HBR use this? | Any AI hallmark present. |
| S6-Proof | Data is attributed (source + year). Hero number gets massive treatment (48-72pt). No unattributed stats. No precision theater ("47.3%"). | Claims without source. Hero number same size as body text. |
| S7-Boundaries | Calculate: max(x + w) must be ≤ 9.5". max(y + h) must be ≤ 5.1". Math check, not eyeballing. | Any element extends beyond slide boundaries. |
| S8-Template | Could this slide have used a template layout instead of building from scratch? Check layout-reference.md. | Built from scratch when a layout function exists for this content pattern. |
| S9-Contrast | Critical text (hero stat, CTA, key labels) uses t1 or t2, not t3. On dark bg, all body text uses t2. t3 reserved for captions/footnotes 12pt+. Maroon for 18pt+ only. | Critical text using t3 or lower on dark bg. Body text in t3. |
| S10-Proportions | Body text >= 14pt? Every text box content fills >= 60% of box area? Card widths proportional to content? Largest gap is intentional (edges/bottom) not scattered? | Text < 14pt body. Boxes oversized for content. Tiny text swimming in empty space. |
| S11-Overlap | For every pair of adjacent elements: bounding boxes don't intersect (include 0.15" safety margin). Title doesn't share y-range with content elements. | Any overlap or elements within 0.15" of each other. |

## EVAL Block Format

Emit after every slide evaluation:

```
EVAL Slide N: [slide title]
  S1-Hierarchy:   PASS|FAIL — [reason. Is title insight-driven?]
  S2-Density:     PASS|FAIL — [chunk count] chunks, budget [X] for [audience]. Acronyms: [N]
  S5-Taste:       PASS|FAIL — [specific AI hallmark found, or clean]
  S6-Proof:       PASS|FAIL — [attribution check or N/A]
  S7-Boundaries:  PASS|FAIL — right max: [X]" ≤ 9.5", bottom max: [Y]" ≤ 5.1"
  S8-Template:    PASS|FAIL|N/A — [layout used vs available]
  S9-Contrast:    PASS|FAIL — [any t3 on critical text?]
  S10-Proportions: PASS|FAIL — body [N]pt, box fill [N]%, gap distribution [ok|scattered]
  S11-Overlap:    PASS|FAIL — [nearest pair distance]
  VERDICT:        CLEAN | FIX REQUIRED → [what to fix]
```

After self-eval VERDICT = CLEAN, dispatch deck-qa agent with the PNG for independent visual QA (mandatory gate).

## Transition Checks (after each slide, comparing to predecessor)

| Check | What to Verify | FAIL if... |
|---|---|---|
| S3-Rhythm | This slide's layout differs from the previous 2 slides. 3 consecutive identical layouts = HARD STOP. | Same layout type as both predecessors. |
| S4-Narrative | Visual register matches the emotional shift specified in strategy (register field). Bridging sentence exists between talk tracks. | Dense slide after a breather with no shift. No natural bridge between talk tracks. |

## TRANSITION Block Format

```
TRANSITION Slide N-1 → Slide N:
  S3-Rhythm:    PASS|FAIL — layouts: [prev2], [prev1], [current]
  S4-Narrative:  PASS|FAIL — register shift: [from] → [to]
  VERDICT:      CLEAN | FIX REQUIRED → [what to fix]
```

## Circuit Breaker

- 2 consecutive deck-qa failures on SAME issue → stop, propose different layout to user
- 3 total deck-qa failures on one slide (any issues) → present best version with remaining issues list
- Hard max 5 render attempts per slide → ship with honest quality notes

## Architecture Slides

For any slide with architecture diagrams, ALSO read and apply `references/architecture-eval-rubric.md` after the standard checks above.
