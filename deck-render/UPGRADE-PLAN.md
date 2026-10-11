# Deck-Render Skill Upgrade Plan

**Created:** 2026-04-05 via /grill-me session (20 decisions resolved)
**Status:** Ready for execution
**Execution:** Phase-by-phase with user approval between each phase

---

## Resolved Decisions (from Grill-Me)

| # | Question | Decision |
|---|----------|----------|
| Q1 | S12-Space estimation method | Visual heuristic from PNG (consistent with S1-S11) |
| Q2 | Where new deck types live | Separate file: `references/deck-type-arcs.md` (on-demand loading) |
| Q3 | "Principles" section location | Stays in deck-philosophy.md (per-slide diagnostic aid) |
| Q4 | Eval override communication | Both: prose rationale in deck-type-arcs.md + compact matrix in eval-checklist.md |
| Q5 | intrigue_break implementation | Narrative role variant of power_statement (no new layout key) |
| Q6 | Forward bridge on last slide | Bridge to conversation ("The question I'd leave you with...") |
| Q7 | "If Challenged" scope | Claims/data/competitive slides only, max 1 per slide |
| Q8 | Slide Zero eval/numbering | Excluded from eval + per_slide_scores, included in slide_count |
| Q9 | Appendix eval | Same pptx, mechanical eval only (S7-Boundaries + S11-Overlap) |
| Q10 | deck-type-arcs.md load timing | Read at start when deck_type is one of the four new types |
| Q11 | S2 cognitive load distinction | Diagnostic only — verdict stays FAIL, guides fix (split vs simplify) |
| Q12 | Pause taxonomy migration | Clean replacement: [PAUSE]→[BEAT], [LET IT LAND]→[BREATHE], add [HOLD] |
| Q13 | Board validation behavior | Block: fix invalid YAML before writing |
| Q14 | Why Evolve register table location | deck-philosophy.md Section 4 (alongside Challenger) |
| Q15 | GSlides archive scope | All GSlides artifacts: 5 Python files + 2 test dirs → `_archive/gslides/` |
| Q16 | deck_type vs motion_type | deck_type subsumes motion_type. Backward compat: motion_type: expand → infer deck_type: expansion |
| Q17 | QBR GAPS honesty | Always on-slide, no sensitivity modifier |
| Q18 | Board fields for non-sales decks | Nullable with explanation (e.g., "N/A — educational deck") |
| Q19 | layout-reference.md palette scope | Full rewrite: light theme default in all code examples |
| Q20 | Execution approach | Plan file now, execute in fresh session |

---

## Phase 1: P0 Technical Fixes

### 1a. Fix palette in layout-reference.md (FULL REWRITE)

**Scope:** 14 occurrences of `bg1` + all dark-bg code examples.

**Changes:**
1. Rename palette key `bg1` → `bg` everywhere
2. Replace the Section 4 palette constant with LIGHT_PALETTE as default:
   ```javascript
   const C = {
     bg: "F9F7F4", bgCard: "FFFFFF", bgLight: "EEEDE9",
     lava: "FF3621", lavaText: "C42B1A",
     green: "00A972", blue: "2272B4", yellow: "FFAB00",
     maroon: "C4243E",
     navy: "1B3139", navyDark: "0B2026",
     t1: "333333", t2: "545454", t3: "595959",
     border: "B0B0B0"
   };
   ```
3. Rewrite all code examples to show light-bg rendering:
   - Content slides: `s.background = { color: C.bg };` with dark text (t1, t2)
   - Structural slides (title, section, closing): `s.background = { color: C.navy };` with white text
   - Architecture slides: `s.background = { color: C.navyDark };`
4. Add dark palette as clearly-marked opt-in section:
   ```javascript
   // DARK THEME (opt-in via strategy YAML: theme: dark)
   const C_DARK = {
     bg: "0B2026", bgCard: "1B3139", bgLight: "303F47",
     ...
   };
   ```
5. Fix line 29 strategy table note to remove `bg1` reference

### 1b. Archive ALL GSlides artifacts

**Move to `deck-render/_archive/gslides/`:**
- `references/gslides_scaffold.py` (125K)
- `references/gslides_scaffold.py.backup` (125K)
- `references/deck_tool.py` (15K)
- `references/icon_bootstrap.py` (6K)
- `PLAN-gslides-migration.md`
- `rendered/test-deck-v2/` (entire directory)
- `rendered/test-deck-v3/` (entire directory)

**Verify:** No remaining imports/references from active files after move.

### 1c. Fix eval checklist numbering note

Add to top of eval-checklist.md:
```
Note: S3 and S4 are transition checks (evaluated between slides, not
per-slide). See "Transition Checks" section below. Per-slide checks
use S1, S2, S5-S12.
```

---

## Phase 2: Eval Checklist Additions

### 2a. Add S12-Space (Negative Space Check)

Add to per-slide checks table in eval-checklist.md:

| Check | What to Verify | FAIL if... |
|-------|----------------|------------|
| S12-Space | For REFRAME/FEEL slides: >= 50% empty (visual estimate from PNG). For breather/section_break: >= 70% empty. Garr Reynolds's Presentation Zen — deliberate emptiness IS the design. | REFRAME or FEEL slide has < 40% empty space. N/A for SOLVE, PROVE, EQUIP, data-heavy slides. |

Add to EVAL block format:
```
S12-Space:     PASS|FAIL|N/A — [narrative_role], [estimated empty %]
```

**Design principle citation:** Garr Reynolds, Presentation Zen — inverse of S2-Density. S2 catches overcrowding; S12 catches slides that should be sparse but aren't.

### 2b. Refine S2-Density with cognitive load diagnostic

Add diagnostic note below S2 in eval-checklist.md:

```
When S2 FAILS (chunk count exceeds budget), diagnose the cause:

- INTRINSIC load: Content itself is genuinely complex and the audience
  needs this depth. FIX: Split into 2 slides or move detail to appendix.
  The information is justified — just too much for one slide.

- EXTRANEOUS load: Design makes simple content look complex through poor
  layout, redundant visual elements, or competing signals. FIX: Simplify
  the layout without reducing information content.

Reference: Sweller's Cognitive Load Theory. The verdict stays FAIL either
way — the distinction guides the remedy, not the score.
```

---

## Phase 3: SKILL.md Talk Track and Delivery Improvements

### 3a. Add forward bridge rule

In the "Talk Tracks to Speaker Notes" section, add:

```
**Forward Bridge Rule:** Every slide's talk track MUST end with a
Transition bullet that is a FORWARD BRIDGE — it sets up the next slide
before the click, not after. The audience should already be wondering
"how?" or "what happened?" when the next slide appears.

Bad:  "So that's the problem." [click] "Now let me show you..."
Good: "Every escaped referral costs $31K. What if you could catch them
  before they leave?" [click] [slide answers the question]

Last slide exception: The final substantive slide bridges to the
post-deck CONVERSATION, not another slide:
  "The question I'd leave you with: what would it mean for your team
   if every referral arrived at an active provider?"

Reference: Heath & Heath, Made to Stick — the "knowledge curse" means
audiences lose the thread between slides, not during them.
```

### 3b. Replace pause taxonomy

Replace the delivery cue mapping with three-level taxonomy:

| Cue | Duration | Purpose | When |
|-----|----------|---------|------|
| [BEAT] | 1-2 sec | Emphasis — "that was important" | After hero stat, key claim |
| [BREATHE] | 3-4 sec | Processing — let audience absorb | After dense data, emotional beat |
| [HOLD] | 5-7 sec | Tension — uncomfortable anticipation | Before REFRAME reveal, major narrative turn |

**Mapping from narrative_role:**
- WARM → [BEAT] after credibility statement
- REFRAME → [HOLD] before the reveal, [BREATHE] after
- DROWN → [BREATHE] after hero stat
- FEEL → [BREATHE] throughout, [HOLD] at emotional peak
- SOLVE → [BEAT] after key capability
- PROVE → [BEAT] after proof point
- EQUIP/ACTION → [BEAT] before specific ask

**Replace in all examples:** `[PAUSE]` → `[BEAT]`, `[LET IT LAND]` → `[BREATHE]`. Update scaffold-reference.md examples too.

### 3c. Add "If Challenged" bullets

Add to talk track rules:

```
**If Challenged bullets:** For slides with claims, data, or competitive
positioning (typically REFRAME, DROWN, PROVE, SOLVE, and stat heroes):
add ONE "If Challenged" bullet. Max 1 per slide.

Distinct from "If Asked":
- If Asked = informational follow-up → provide info
- If Challenged = frame contest → acknowledge + redirect (never defensive)

Template:
  If challenged: "[likely pushback]"
  Response: "[acknowledge] — [redirect to your frame]"

Example:
  If challenged: "Your $2.4M number seems high."
  Response: "Fair pushback — that's from YOUR claims data using a
    conservative $31K average. Happy to walk through the methodology
    after. The directional point: even at half that, it's material."

Reference: Klaff, Pitch Anything — frame control. Acknowledge the
challenge without ceding the frame, then redirect.

**Canonical speaker note ordering:**
1. Body bullets (3-7, one idea each)
2. Transition / Forward Bridge (sets up the next slide)
3. If Asked (informational follow-up)
4. If Challenged (frame contest — claims slides only)
```

---

## Phase 4: deck-philosophy.md Narrative Additions

### 4a. Split into two files

**Create:** `references/deck-level-review.md`

**Move from deck-philosophy.md:** Section 7 ("Deck-Level Evaluation") and everything after it (EXCEPT "Principles to Keep in Your Head" which stays).

Content to move:
- Full Arc Check
- Attention Placement Check (Hammock Effect)
- Rhythm Check
- Time Budget Check
- Thumbnail Distinctiveness Test
- Register Variation Check
- CTA Context Check
- Repeated Message Check
- Image Quality Gate
- Image and Narrative Arc
- Template Icon & Illustration Checklist

**Update SKILL.md loading instructions:**
```
Read ON DEMAND:
  - deck-philosophy.md → when a slide fails evaluation and deeper diagnosis needed
  - architecture-eval-rubric.md → for architecture slides only

Read ONCE after all slides complete:
  - references/deck-level-review.md → deck-wide checks before final assembly

Read at start (if deck_type is account_plan/enablement_session/educational/qbr):
  - references/deck-type-arcs.md → arc definition, eval overrides, density budgets
```

### 4a-verify. Cross-reference audit before proceeding

Before modifying any other files after the split, run:
```bash
grep -r "deck-philosophy" ~/.claude/skills/deck-render/ --include="*.md" \
  | grep -v "deck-philosophy.md:" | grep -v "_archive/" | grep -v "UPGRADE-PLAN"
```
Verify that no other file (board-protocol.md, architecture-eval-rubric.md,
SKILL.md, eval-checklist.md) references Section 7+ content by name. If
any reference points to moved content, update the reference to point to
deck-level-review.md instead.

### 4b. Add Crocodile Brain Novelty

Add to deck-philosophy.md Section 3 (Rhythm):

```
### Crocodile Brain Novelty (Klaff)

Every message passes through the audience's amygdala before reaching
the neocortex. The amygdala looks for novelty, danger, and concrete
patterns while filtering out "more of the same."

When a new slide appears, the croc brain does a rapid threat/novelty
assessment in the first 3 seconds. If the slide looks like the previous
one (same layout, same density, same color), it classifies as "already
processed" and attention drops.

S3-Rhythm catches the symptom (consecutive identical layouts). The croc
brain principle explains WHY and gives deeper diagnostic guidance when
S3 fails:
- Is the visual novelty sufficient to trigger croc brain re-engagement?
- Would a reader scrolling through thumbnails pause at this transition?
- Consider: layout family shift, density shift, color temperature shift,
  or a "pattern interrupt" (full-bleed image, single sentence, question)
```

### 4c. Add Bookend Technique to Section 6

Add to deck-philosophy.md Section 6 ("The Data Isn't Convincing"):

```
### Bookend Technique (Duarte, DataStory)

Bookend the data with human context:

1. Speaker note opens with a concrete human moment:
   "Picture the nurse coordinator at 7am, printing referral faxes
    because the EHR can't tell her which providers are still active."
2. Slide shows the stat: "$2.4M annual leakage"
3. Speaker note closes by returning to the same moment, transformed:
   "That nurse? She's now getting real-time provider status.
    No more faxes. That's what rescued revenue looks like."

This is NOT the arc-level FEEL slide. The bookend operates within a
single slide's talk track. It gives every data slide the option to
carry emotional weight.
```

### 4d. Add Credibility Anchor to Section 6

```
### Credibility Anchor

The first technical claim sets the credibility anchor for all subsequent
claims. The audience evaluates the first data point with maximum
scrutiny. If it checks out, subsequent claims get a credibility
discount (trusted more easily).

Place your most verifiable, most conservative claim first — not your
most impressive one.

Good first claim: "Your FY24 claims data shows 23% of referrals went
  to inactive providers." (Their data. Easily verified. Conservative.)
Bad first claim: "Healthcare organizations lose $4.2M annually to
  referral leakage." (Industry average. Feels like marketing.)
```

### 4e. Add Peak-End Rule to deck-level-review.md

Add to the NEW deck-level-review.md:

```
### Peak-End Rule (Kahneman)

People judge experiences based on two moments — the emotional peak
and the ending. Everything in between is averaged.

The most emotionally intense slide (usually FEEL or HARD TRUTH) and
the final substantive slide together determine how the audience
remembers the entire presentation.

Peak-End Check:
- Identify the emotional peak slide (highest intensity in the arc)
- Identify the final substantive slide
- For both: Is this the highest quality slide in the deck? Would it
  stand alone as a single-slide summary of the presentation's impact?
- If either is mediocre, the audience remembers the entire deck as
  mediocre regardless of other slides.
```

### 4f. Add Why Evolve register table to Section 4

Add to deck-philosophy.md Section 4 (alongside Challenger register guidance):

```
### Why Evolve — Visual Register

| Phase | Register | Why |
|-------|----------|-----|
| CELEBRATE | Polished | Validates past decision — authoritative |
| DOCUMENT | Polished | Evidence — charts, metrics, clean data |
| PRESSURE | Sparse-trending | Shift signal — "something has changed" |
| HARD TRUTH | Sparse | Maximum contrast with CELEBRATE |
| RISK | Moderate | Loss framing needs data, not polish |
| UPSIDE | Building | Hope emerging — cleaner than RISK, not yet polished |
| QUANTIFY | Polished | Confidence and clarity — commitment slide |
```

### 4g. Add Choice Budget

Add to deck-philosophy.md (near Section 2 or as standalone subsection):

```
### Choice Budget (Schwartz, Paradox of Choice)

Presenting more than 3-4 options causes decision paralysis.

For SOLVE or capability slides:
- <= 3 items: audience can compare and choose (ideal)
- 4-5 items: audience scans but may not deeply evaluate
- 6+ items: choice overload — audience defers decision

When 6+ items need to appear:
- Group into 2-3 categories first, then detail within categories
- Or sequence across multiple slides (3 per slide)
- Never present a flat list of 6+ equal-weight items
```

---

## Phase 5: Intrigue Break (Simplified per Q5)

**No new layout key.** Add `intrigue_break` as a narrative_role variant.

Add to deck-philosophy.md (Challenger arc section) or SKILL.md delivery cues:

```
### Intrigue Break (Klaff)

narrative_role: intrigue_break
Layout: power_statement (reuses existing layout)
Visual: Dark background (structural treatment), single provocative
  incomplete sentence, 28-36pt, centered, white text, >= 70% empty
Delivery cue: [HOLD] (5-7 second tension pause)
Purpose: Break the audience's analyst frame with unresolved tension

Example: "The last health system that tried this spent 18 months
building something they never launched."

The talk track completes the story. The slide creates the gap.

Distinct from power_statement: its job is specifically to break an
analytical frame, not to make a declarative statement. Use when the
audience is about to go into analyst mode and you need to pull them
back into narrative.
```

---

## Phase 6: New Deck Types

**Target file:** NEW `references/deck-type-arcs.md`

### File structure:
```markdown
# Deck Type Arc Definitions

Loaded at start when deck_type is one of these types.
For Challenger and Why Evolve arcs, see deck-philosophy.md Section 4.

## account_plan
[Full arc: LANDSCAPE → WHITESPACE → HYPOTHESIS → PLAY → ASK]
[Register: consistently moderate throughout]
[Density: 5-7 chunks]
[Eval overrides: S12 N/A, S4 optional, S5 "planning document test"]
[No loss framing. No emotional appeals. Data-forward, hypothesis-driven.]
[Key: reference-heavy, scannable, standalone without presenter]

## enablement_session
[Full arc: ORIENT → CONCEPT → DEMONSTRATE → PRACTICE → PATTERN]
[Register: consistent clarity throughout]
[Density: 7-9 chunks]
[Eval overrides: S1 hero=screenshot/code, S2 budget 7-9, S6 relaxed, S12 N/A]
[Training layouts: annotated screenshot, terminal/code, "your turn" prompt]
[PRACTICE slides: exercise prompt, time, expected output, common pitfalls]

## educational
[Full arc: PROVOKE → CONTEXT → DEEP DIVE → IMPLICATION → HORIZON]
[Register: high production value, magazine aesthetic]
[Density: varies — PROVOKE 2-3, DEEP DIVE 7-9, IMPLICATION 3-4, HORIZON 2-3]
[Eval overrides: S5 highest bar, CTA disabled, closing = thought not ask]
[Emotional engine: CURIOSITY not FEAR. No loss framing.]

## qbr
[Full arc: RESULTS → ADOPTION → GAPS → ROADMAP → NEXT QUARTER]
[Register: clinical and confident, consulting-firm aesthetic]
[Density: 7-9 throughout, tables with 5+ rows justified]
[Eval overrides: S2 higher ceiling, S5 Tufte data-ink, S10 smaller text OK, S1 charts as hero]
[GAPS: always on-slide, never hidden. Yellow accent for issues.]
[CTA: joint commitment ("we" not "you")]
[Loss framing: GAPS only, shared loss framing]
```

### Eval override matrix (append to eval-checklist.md)

```
## Deck-Type Eval Override Matrix

| Check | customer_pitch | expansion | int_persuasion | int_equipping | account_plan | enablement | educational | qbr |
|-------|---------------|-----------|----------------|---------------|-------------|------------|-------------|-----|
| S1-Hierarchy | standard | standard | standard | standard | standard | hero=screenshot OK | PROVOKE dramatic | charts as hero OK |
| S2-Density | 3-4/5-7 | 4-6 | 4-6 | SA 5-7, BDR 2-3 | 5-7 | 7-9 | varies by phase | 7-9 |
| S5-Taste | magazine | magazine | magazine | clarity | planning doc | clarity | HIGHEST bar | Tufte data-ink |
| S6-Proof | strict | strict | strict | relaxed | strict | relaxed (product docs) | strict | strict |
| S12-Space | applies | applies | applies | N/A | N/A | N/A | applies | N/A |
| S3-Rhythm | applies | applies | applies | applies | applies | applies | applies | applies |
| S4-Narrative | applies | applies | applies | applies | optional | applies | applies | applies |
| CTA required | yes (specific) | yes | yes (resource ask) | no | yes (resource ask) | no | no (end on idea) | joint commitment |
| Loss framing | yes | PRESSURE/RISK only | yes | no | no | no | no | GAPS only (shared) |
| Register shift | yes | yes | yes | no | no | no | no | no |

Note: int_persuasion uses Challenger arc (internal variant), int_equipping uses
Recognition→Pattern→Application or Proof→Script→Practice. Both defined in
deck-philosophy.md Section 4. Their eval overrides follow the same patterns as
their closest external equivalents (customer_pitch and enablement_session respectively).
```

---

## Phase 7: Strategy YAML Updates

### 7a. Add deck_type field to SKILL.md

Add to strategy YAML schema:

```yaml
deck_type: customer_pitch  # default if omitted
# Options: customer_pitch | expansion | internal_persuasion |
#          internal_equipping | account_plan | enablement_session |
#          educational | qbr
```

Add routing table and deprecation note:

```
**deck_type** selects arc, eval overrides, density budgets, CTA
enforcement, loss framing, and register shifting. See routing table
in eval-checklist.md override matrix.

**Backward compatibility:** `motion_type: expand` (without deck_type)
→ infer `deck_type: expansion`. `motion_type` is deprecated — use
`deck_type` going forward.
```

### 7b. Slide Zero and Appendix conventions

Add to SKILL.md:

```
**Slide Zero (optional pre-title atmospheric):**
- Rendered before slide 1 if strategy specifies slide_zero
- Excluded from all eval checks (S1-S12, S3-S4)
- Excluded from per_slide_scores in board output
- Included in slide_count (physically in pptx)
- S3-Rhythm comparison starts from slide 1, not slide 0

Strategy YAML:
  slide_zero:
    type: atmospheric | question | logo
    content: "What if every referral arrived at an active provider?"

**Appendix slides (optional, after closing):**
- Section divider: "APPENDIX" on dark background
- Use content_basic layout, no narrative_role
- Speaker notes: "Reference slide — do not present unless asked"
- Eval: S7-Boundaries + S11-Overlap only (mechanical safety)
- S3-Rhythm, S4-Narrative, S1-S2, S5-S6, S8-S12 do NOT apply

Strategy YAML:
  appendix:
    - title: "Detailed Benchmark Methodology"
      layout: content_basic
    - title: "Full Architecture Diagram"
      layout: blank
```

---

## Phase 8: Board Protocol Validation

### 8a. Add validation step to board-protocol.md

After the board write section, add:

```
### Board Output Validation (BLOCKING)

After writing deck-render-output.yaml, validate before completing.
If validation fails, FIX the output YAML before writing. Do not write
an invalid board signal — downstream skills trust it unconditionally.

Required field checks:
- artifact_path: present, file exists on disk
- hero_message_as_rendered: present, non-empty string
- proof_points_used: present, array
- slide_count: present, matches actual slide count in pptx
- quality_score: present, <= quality_max
- quality_max: present, integer
- quality_pass: true only if quality_score == quality_max
- per_slide_scores: present, has exactly slide_count entries
  (minus 1 if slide_zero exists, minus appendix slide count)

Nullable fields (for non-sales deck types):
- competitive_frame_as_rendered: null or "N/A — [deck_type]" when
  deck_type is educational, enablement_session, or account_plan
```

---

## Additional Housekeeping (discovered during grill-me)

1. **Deprecate motion_type reference in deck-philosophy.md line ~276:**
   Replace mention of `motion_type: expand` with `deck_type: expansion`

2. **Update scaffold-reference.md examples:** Replace `[PAUSE]` → `[BEAT]`,
   `[LET IT LAND]` → `[BREATHE]` in any speaker note examples

3. **Record grill-me decisions:** Save to `deck-render/.wall/grill-me-upgrade-2026-04-05.md`

---

## Execution Checklist

Run phases in order. After each phase, show user what changed and wait
for approval before proceeding.

- [ ] Phase 1a: layout-reference.md full palette rewrite (bg1→bg + light default)
- [ ] Phase 1b: Archive all GSlides artifacts to _archive/gslides/
- [ ] Phase 1c: Add S3/S4 numbering note to eval-checklist.md
- [ ] Phase 2a: Add S12-Space check
- [ ] Phase 2b: Add S2 cognitive load diagnostic
- [ ] Phase 3a: Add forward bridge rule to SKILL.md
- [ ] Phase 3b: Replace pause taxonomy in SKILL.md + scaffold-reference.md
- [ ] Phase 3c: Add "If Challenged" bullets to SKILL.md
- [ ] Phase 4a: Split deck-philosophy.md → create deck-level-review.md
- [ ] Phase 4b: Add Crocodile Brain to Section 3
- [ ] Phase 4c: Add Bookend Technique to Section 6
- [ ] Phase 4d: Add Credibility Anchor to Section 6
- [ ] Phase 4e: Add Peak-End Rule to deck-level-review.md
- [ ] Phase 4f: Add Why Evolve register table to Section 4
- [ ] Phase 4g: Add Choice Budget
- [ ] Phase 5: Add intrigue_break narrative role (no new layout)
- [ ] Phase 6: Create deck-type-arcs.md + eval override matrix
- [ ] Phase 7a: Add deck_type field + routing table to SKILL.md
- [ ] Phase 7b: Add Slide Zero + Appendix conventions to SKILL.md
- [ ] Phase 8: Add board validation to board-protocol.md
- [ ] Housekeeping: deprecate motion_type, update pause cues, record decisions
