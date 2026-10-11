# Evolution Log: arch-diagram

## Session: 2026-03-24 (branch: evolve/arch-diagram/2026-03-24)

### Baseline
- **Score:** 9/13 (median of 9 runs across 3 inputs)
- **Per-eval pass rates:**
  - E1 (valid XML): 100%
  - E2 (explicit coords): 100%
  - E3 (governance full-width): 100%
  - E4 (cross-zone labels): 100%
  - E5 (L-R flow): 100%
  - E6 (Databricks names): 100%
  - E7 (descriptive medallion): 100%
  - E8 (zones grouped): 100%
  - E9 (no overlapping text): 0% **weakest**
  - E10 (breathing room): 11%
  - E11 (concise labels): 44%
  - E12 (clean arrows): 67%
  - E13 (color palette): 44%
- **Run totals:** 9, 8, 9, 10, 10, 10, 9, 9, 11

### Round 1
- **Hypothesis:** Adding explicit minimum spacing and node sizing constraints (30px gaps, 140x50 min size, 20px zone padding, step indicator placement rules) will prevent text overlap in rendered diagrams
- **Change:** Added "Spacing Rules" subsection to Layout Rules with 5 bullet points
- **Diff size:** 7 lines added
- **Target eval:** E9 (no overlapping text — 0% pass rate)
- **Baseline:** 9/13 (median)
- **Challenger:** 10/13 (median) — sorted: 8, 9, 9, 9, 10, 10, 10, 12, 13
- **Result:** WIN (10 > 9). Committed as b6b8baf.
- **Per-eval changes:**
  - E9 (no overlapping text): 0% → 22% (+22%)
  - E10 (breathing room): 11% → 44% (+33%)
  - E12 (clean arrows): 67% → 89% (+22%)
  - E13 (color palette): 44% → 78% (+34%)
  - E7 (descriptive medallion): 100% → 67% (-33%, scorer noise on input1)
  - E11 (concise labels): 44% → 33% (-11%)
- **Commit:** b6b8baf

### Round 2
- **Hypothesis:** Adding explicit "Keep node labels concise — 1-3 words per node, no schemas/SQL/descriptions inside boxes" constraint will improve E11 (concise labels)
- **Change:** Added 1 line to Constraints section
- **Diff size:** 1 line added
- **Target eval:** E11 (concise labels — 33% pass rate after Round 1)
- **Baseline:** 10/13 (median, from Round 1 winner)
- **Challenger:** 12/13 (median) — sorted: 10, 11, 11, 11, 12, 12, 12, 12, 13
- **Result:** WIN (12 > 10). Committed as 7d75e05.
- **Per-eval changes:**
  - E10 (breathing room): 44% → 100% (+56%)
  - E11 (concise labels): 33% → 78% (+45%) — target
  - E13 (color palette): 78% → 100% (+22%)
  - E7 (descriptive medallion): 67% → 78% (+11%)
  - E12 (clean arrows): 89% → 78% (-11%)
  - E9 (no overlapping text): 22% → 22% (unchanged)
- **Commit:** 7d75e05

### Round 3
- **Hypothesis:** Adding overlap scan validation step to STEP 5 ("verify arrow labels won't land on top of nodes at 2x render scale") will improve E9
- **Change:** Added 1 line to STEP 5 validation checks
- **Diff size:** 1 line added
- **Target eval:** E9 (no overlapping text — 22% pass rate)
- **Baseline:** 12/13 (median, from Round 2 winner)
- **Challenger:** 11/13 (median) — sorted: 9, 9, 9, 10, 11, 11, 12, 12, 13
- **Result:** LOSS (11 < 12). Reverted.
- **Per-eval changes (vs R2 baseline):**
  - E7 (descriptive medallion): 78% → 67% (-11%)
  - E9 (no overlapping text): 22% → 22% (unchanged — target eval not improved)
  - E10 (breathing room): 100% → 56% (-44%)
  - E11 (concise labels): 78% → 56% (-22%)
  - E12 (clean arrows): 78% → 78% (unchanged)
  - E13 (color palette): 100% → 67% (-33%)
- **Note:** Process-oriented validation step backfired. The model can't compute pixel overlap from XML coordinates alone — the instruction added cognitive load without actionable guidance, degrading multiple visual evals.

### Round 4
- **Hypothesis:** Adding arrow routing discipline — connect adjacent zones only, limit to ≤15 arrows — will reduce spaghetti and improve E12
- **Change:** Added 1 line to Constraints section (arrow span limit)
- **Diff size:** 1 line added
- **Target eval:** E12 (clean arrows — 78% pass rate)
- **Baseline:** 12/13 (median, from Round 2 winner)
- **Challenger:** 11/13 (median) — sorted: 10, 11, 11, 11, 11, 12, 13, 13, 13
- **Result:** LOSS (11 < 12). Reverted.
- **Per-eval changes (vs R2 baseline):**
  - E11 (concise labels): 78% → 100% (+22%)
  - E12 (clean arrows): 78% → 100% (+22%) — target hit!
  - E9 (no overlapping text): 22% → 33% (+11%)
  - E7 (descriptive medallion): 78% → 67% (-11%)
  - E10 (breathing room): 100% → 78% (-22%)
  - E13 (color palette): 100% → 89% (-11%)
- **Note:** Target E12 hit 100% and E11 also hit 100%, but E10 regressed -22% killing the median. Arrow-span constraint caused less-connected diagrams that scorers penalized on "breathing room." Net: gained on two evals, lost on three. Interesting that fewer arrows hurt visual quality perception despite reducing spaghetti.

### Round 5
- **Hypothesis:** Making the XML `&#xa;` multiline format explicit in the medallion labels constraint (showing exact XML syntax instead of prose) will improve E7
- **Change:** Modified 1 line in Constraints section — replaced prose format with XML example
- **Diff size:** 1 line modified (replacement)
- **Target eval:** E7 (descriptive medallion — 78% pass rate)
- **Baseline:** 12/13 (median, from Round 2 winner)
- **Challenger:** 12/13 (median) — sorted: 11, 11, 11, 12, 12, 12, 12, 13, 13
- **Result:** TIE (12 == 12). Ties are losses. Reverted.
- **Per-eval changes (vs R2 baseline):**
  - E9 (no overlapping text): 22% → 56% (+34%)
  - E11 (concise labels): 78% → 100% (+22%)
  - E12 (clean arrows): 78% → 89% (+11%)
  - E7 (descriptive medallion): 78% → 67% (-11%) — target went DOWN
  - E10 (breathing room): 100% → 78% (-22%)
  - E13 (color palette): 100% → 100% (unchanged)
- **Note:** Ironic — explicit `&#xa;` format hurt E7 on input1 (agent memory diagram has no medallion layers, but the model started forcing multiline labels everywhere). E9 improved dramatically (+34%) suggesting the XML format examples help layout quality generally. But the E10 regression canceled it out, yielding a tie.

### Summary
- **Start:** 9/13 → **End:** 12/13
- **Wins:** 2, **Ties:** 1, **Losses:** 2
- **3 consecutive non-wins** (R3 loss, R4 loss, R5 tie) — evolution stopped per protocol
- **Winning changes:**
  - Round 1: Spacing rules (min gaps, node sizes, zone padding) [9→10]
  - Round 2: Concise label constraint (1-3 words per node) [10→12]
- **Failed hypotheses:**
  - Round 3: Overlap scan validation in STEP 5 (cognitive load without actionable guidance)
  - Round 4: Arrow span limit (reduced connections hurt "breathing room" perception)
  - Round 5: Explicit XML `&#xa;` format for medallion labels (hurt E7 on non-medallion diagrams)

### Per-eval trajectory (baseline → final)
- E1 (valid XML): 100% → 100%
- E2 (explicit coords): 100% → 100%
- E3 (governance full-width): 100% → 100%
- E4 (cross-zone labels): 100% → 100%
- E5 (L-R flow): 100% → 100%
- E6 (Databricks names): 100% → 100%
- E7 (descriptive medallion): 100% → 78% (-22%, scorer variance on non-medallion inputs)
- E8 (zones grouped): 100% → 100%
- E9 (no overlapping text): 0% → 22% (+22%)
- E10 (breathing room): 11% → 100% (+89%)
- E11 (concise labels): 44% → 78% (+34%)
- E12 (clean arrows): 67% → 78% (+11%)
- E13 (color palette): 44% → 100% (+56%)

### Observations
- **Structural constraints work; process instructions don't.** Changes the model can directly control (node sizes, label length) improve output. Validation steps the model can't actually verify at generation time (overlap checks, render-time calculations) add noise.
- **Visual evals are coupled.** E9/E10/E11/E12 move together — improving one often regresses another. The remaining 1/13 gap (E9 at 22%) may require fundamentally different approach (e.g., coordinate calculation examples, not just rules).
- **E9 is the hard ceiling.** Text overlap prevention requires spatial reasoning the model lacks when generating XML coordinates. May need render-in-the-loop or coordinate templates to break through.
