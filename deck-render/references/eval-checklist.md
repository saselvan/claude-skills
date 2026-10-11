# Slide Evaluation Checklist

Re-read this before every per-slide evaluation. Emit the EVAL and TRANSITION blocks exactly as shown.

Note: S3 and S4 are transition checks (evaluated between slides, not
per-slide). See "Transition Checks" section below. Per-slide checks
use S1, S2, S5-S12.

## Per-Slide Checks

After rendering and converting to PNG, verify each:

| Check | What to Verify | FAIL if... |
|---|---|---|
| S1-Hierarchy | One hero element 2-3x larger than everything else. Squint test: blur vision, can you tell what's important? Title is insight-driven ("Unity Catalog unifies governance") not descriptive ("Architecture Overview"). | Multiple elements compete. No clear focal point. Title is just a topic label. |
| S2-Density | Count content chunks — within budget? Exec: 3-4, Technical: 5-7, BDR: 2-3, Mixed: 3-4. Max acronyms: 2 (exec), 4 (technical). | Chunk count exceeds budget. Acronym soup. Nested sub-sub-bullets. |

When S2 FAILS (chunk count exceeds budget), diagnose the cause:

- INTRINSIC load: Content itself is genuinely complex and the audience
  needs this depth. FIX: Split into 2 slides or move detail to appendix.
  The information is justified — just too much for one slide.

- EXTRANEOUS load: Design makes simple content look complex through poor
  layout, redundant visual elements, or competing signals. FIX: Simplify
  the layout without reducing information content.

Reference: Sweller's Cognitive Load Theory. The verdict stays FAIL either
way — the distinction guides the remedy, not the score.

| S5-Taste | See S5 Expanded Checklist below. | Any AI hallmark present. |

### S5-Taste Expanded Checklist

S5 is the most common failure point. "Make it professional" gives the model nothing. These are the concrete defaults it falls back on — naming them is what blocks them.

**Hard bans (all deck types):**
- No colored accent lines under titles
- No centered body text (left-align body; center only hero stats and titles)
- No equal-weight colors (one accent, used once per slide on one element type)
- No icon walls (6+ icons arranged in rows)
- No gradient backgrounds of any kind
- No card containers with rounded corners AND drop shadows together
- No "tagline" slides (single phrase centered on colored background)
- No emoji anywhere in slide content
- No cream or beige backgrounds (branded decks use F9F7F4 warm oat; editorial uses true off-white #F2-#F6)

**AI-aesthetic hallmarks (the specific patterns Claude/AI defaults to):**
- Colored top-bar stripes on cards — the #1 tell
- Icons in colored circles — the #2 tell
- Pill-shaped tags or badges
- Teal + coral + sage palette (the "default Claude Design" look)
- Full-width colored header rectangles
- Decorative divider lines between all sections
- Status indicators as colored dots or checkmarks (use typography instead)
- Zebra-striped tables

**Magazine test (final check):** Would HBR, The Economist, or MIT Technology Review use this layout? If it looks like a SaaS landing page or a consulting template, it fails.

**Strategy override:** If `design_decisions.banned_elements` in strategy YAML adds custom bans, check those too.
| S6-Proof | Data is attributed (source + year). Hero number gets massive treatment (48-72pt). No unattributed stats. No precision theater ("47.3%"). | Claims without source. Hero number same size as body text. |
| S7-Boundaries | Calculate: max(x + w) must be ≤ 9.5". max(y + h) must be ≤ 5.1". Math check, not eyeballing. | Any element extends beyond slide boundaries. |
| S8-Template | Could this slide have used a template layout instead of building from scratch? Check layout-reference.md. | Built from scratch when a layout function exists for this content pattern. |
| S9-Contrast | Critical text (hero stat, CTA, key labels) uses t1 or t2, not t3. On dark bg, all body text uses t2. t3 reserved for captions/footnotes 12pt+. Maroon for 18pt+ only. | Critical text using t3 or lower on dark bg. Body text in t3. |
| S10-Proportions | Body text >= 14pt? Every text box content fills >= 60% of box area? Card widths proportional to content? Largest gap is intentional (edges/bottom) not scattered? | Text < 14pt body. Boxes oversized for content. Tiny text swimming in empty space. |
| S11-Overlap | For every pair of adjacent elements: bounding boxes don't intersect (include 0.15" safety margin). Title doesn't share y-range with content elements. | Any overlap or elements within 0.15" of each other. |
| S12-Space | For REFRAME/FEEL slides: >= 50% empty (visual estimate from PNG). For breather/section_break: >= 70% empty. Garr Reynolds's Presentation Zen — deliberate emptiness IS the design. | REFRAME or FEEL slide has < 40% empty space. N/A for SOLVE, PROVE, EQUIP, data-heavy slides. |
| S13-Motif | If `visual_motif` is set (not `none`): motif element is present, positioned consistently with all other slides, and uses the locked accent color + DM Sans italic. Title slide is exempt from numbered_marker. | Motif missing, inconsistent position, or wrong styling. SKIP if visual_motif=none. |
| S14-Bans | Cross-check against locked banned_elements list (both default bans and any custom bans from strategy YAML). For editorial/bespoke: also check the expanded ban list. | Any banned element present on slide. |
| S15-Structure | **B2 structural floor (ALL modes including branded).** Verify: (1) No shadows on content shapes (shadow must be undefined, not inherited). (2) No ROUNDED_RECTANGLE — only RECTANGLE (radius 0-2px equivalent). (3) Display font (.font.name) explicitly set to DM Sans (or strategy brand font) on every text run — never Calibri default. (4) Containment by whitespace or hairline, not boxes. (5) Layout posture asymmetric where applicable (not three equal columns). (6) Hairlines as thin filled rectangles at hairline_color, not shape borders. | Shadow present on any content shape. ROUNDED_RECTANGLE used. Any text run missing explicit .font.name. Three-equal-column layout without justification. |
| S16-Integrity | **Content integrity (audience-scoped: customer, partner, vp_internal).** Reads `design_requirements.guardrails` from strategy YAML. Verify: (1) No named stakeholders on the slide — roles only; names belong in speaker notes. (2) Incumbent/competitor named only as neutral mechanism, never as villain or "rip it out." (3) Every number carries modeled-not-claimed framing ("modeled from your FY24 data") OR a source attribution (extends S6-Proof to the modeled-vs-claimed distinction). (4) **Provenance check:** Any named external org + outcome claim (e.g., "Ensemble Health — 2 months → 5 days") must trace to a strategy `knowledge_atom` or `content_atoms` entry for that section. Unbackable third-party claims = FAIL. (5) No internal jargon (consumption driver, UCO, pipeline tier, SFDC stage). (6) Account-specific guardrails from `design_requirements.guardrails[]` checked (e.g., "Epic is complement not replacement"). | Named stakeholder on slide. Competitor framed as villain. Unattributed number without "modeled" framing. Third-party claim with no knowledge_atom backing. Internal jargon present. Account-specific guardrail violated. |
| S17-Voice | **Register-scoped headline test (all modes).** Reads `voice_register` from strategy YAML (derived from audience_class). Applies the ACTIVE register's headline test from `strategy/voice-registers.md` to every slide headline. Does NOT duplicate S1-Hierarchy (which checks the universal so-what floor). S17 adds the register-specific flavor: (editorial) headline is a conclusion/antithesis you'd say aloud, not a topic label; (enablement) headline is a punchy prize-frame or social-proof hook a rep would repeat; (technical) headline names the mechanism or failure mode specifically; (narrative) section header carries the working-backwards through-line. Also checks: spine (if present in strategy) passes the active register's headline test. | Headline is a topic label when register requires a conclusion. Editorial headline lacks antithesis/observation quality. Enablement headline wouldn't be repeated by a rep. Technical headline doesn't name the mechanism. |

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
  S12-Space:     PASS|FAIL|N/A — [narrative_role], [estimated empty %]
  S13-Motif:     PASS|SKIP — [motif present and consistent? Skip if visual_motif=none]
  S14-Bans:      PASS|FAIL — [any banned element present? Check strategy banned_elements + defaults]
  S15-Structure:  PASS|FAIL — [B2 floor: no shadow, no rounded-rect, font.name explicit, containment by space/hairline, posture asymmetric]
  S16-Integrity:  PASS|FAIL|N/A — [stakeholder names? incumbent neutral? numbers modeled? third-party claims backed by knowledge_atom? internal jargon? account guardrails?] N/A for internal_equipping/educational.
  S17-Voice:      PASS|FAIL — [voice_register=[register], headline test: [pass/fail reason]]
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
| S13-Motif | if set | if set | if set | if set | if set | if set | if set | if set |
| S14-Bans | strict | strict | strict | strict | strict | strict | STRICTEST | strict |
| S15-Structure | applies | applies | applies | applies | applies | applies | applies | applies |
| S16-Integrity | strict | strict | strict | N/A | strict | N/A | N/A | strict |
| S17-Voice | editorial | editorial | editorial | technical | editorial | enablement | technical | editorial |
| CTA required | yes (specific) | yes | yes (resource ask) | no | yes (resource ask) | no | no (end on idea) | joint commitment |
| Loss framing | yes | PRESSURE/RISK only | yes | no | no | no | no | GAPS only (shared) |
| Register shift | yes | yes | yes | no | no | no | no | no |

Note: int_persuasion uses Challenger arc (internal variant), int_equipping uses
Recognition→Pattern→Application or Proof→Script→Practice. Both defined in
deck-philosophy.md Section 4. Their eval overrides follow the same patterns as
their closest external equivalents (customer_pitch and enablement_session respectively).
