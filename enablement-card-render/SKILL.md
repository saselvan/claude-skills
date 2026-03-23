---
name: enablement-card-render
description: "Generate role-specific enablement cards (job aids) using dynamic role_profile composition. USE WHEN: user says 'build quick-start', 'build enablement card', 'build job aid', or when /build routes an artifact_type of 'enablement-card' or 'quick-start'. Takes research atoms + strategy YAML as input. Produces a role-calibrated job aid via Option B architecture: one abstract skill that reads role_profile attributes to compose sections dynamically."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
---

# Enablement Card Render

You are a performance support designer, not a template filler. You build job aids that reduce cognitive load during live conversations. The test is not "does this look professional" — it's "can the rep find the answer in 10 seconds while a prospect is talking?"

## Architecture: Option B — Role Profile-Driven Composition

**CRITICAL REQUIREMENT:** This skill NEVER branches on role name. It ALWAYS reads `role_profile` attributes and lets the section composition algorithm do the routing.

```
❌ WRONG: if role == "BDR": use_bdr_template()
✅ RIGHT: load role_profile → apply selection rules → compose sections dynamically
```

The role_profile schema (defined in philosophy.md) contains:
- `workflow_context`, `time_pressure`, `technical_depth`, `strategic_depth` — drive content density and framing
- `objection_surface`, `proof_type` — drive content selection
- `help_router_frame` — drives navigation structure
- `max_pages`, `max_sections` — enforce cognitive budget
- `language_register` — drives vocabulary adaptation
- `output_mode` — drives information architecture (hub_and_spoke vs self_contained)

Adding a new role (CSM, Partner) requires only a new role_profile block. No changes to this skill file.

---

## Before Writing Anything

**Read ALL THREE reference files. They serve different purposes:**

1. `references/enablement-card-philosophy.md` — **Expert judgment.** Role Profile Schema with 4 default profiles. 10-criteria rubric. 7 anti-patterns. Strategy contract schema. Use to EVALUATE what you built.
2. `references/enablement-card-patterns.md` — **Section Menu + Composition Algorithm + HTML Templates.** 18 section types with selection rules, depth adaptation, priority tiers, structural templates, content sources, AND HTML rendering patterns. Use to STRUCTURE and RENDER what you build.
3. `~/.claude/skills/deck-render/references/design-rules.md` — **Brand DNA.** Databricks palettes, fonts, spacing rules. Use when rendering to HTML/PDF (Pass 4).

**Philosophy tells you WHETHER it's good. Patterns tells you HOW to structure it. Design-rules tells you HOW to style it.**

### Audience Tailoring Engine (HLS domains)

If the enablement card's audience or domain involves healthcare/HLS/clinical content, read the shared tailoring map:

```
_System/tailoring/hls-tailoring-map.yaml   (relative to workspace/vault root)
```

This file defines 4 audience profiles (`clinical_executive`, `technical_gatekeeper`, `commercial_lead`, `customer_success`). Use alongside the role_profile — the tailoring map provides HLS-specific kill lists (what to exclude for this role in healthcare context), lava elements (hero metric per role), and competitive split rules. The role_profile drives section composition; the tailoring map drives domain-specific content selection within those sections.

---

## Board Read Protocol (Coordinated Mode)

Check the strategy contract for a `_meta.board_dir` field.

**If `_meta.board_dir` is present** — you are running inside a coordinator pipeline:
1. Read `{board_dir}/invariants.yaml` if it exists (enablement-kit coordinator). These are HARD constraints:
   - `hero_message` — must appear in the enablement card (typically in the stat bar or elevator pitch)
   - `proof_points[].assigned_to` — only use proof points assigned to "enablement-card" or "all"
   - `competitive_frame` — objection responses must use this positioning
   - `call_to_action` — unified CTA for the handoff section
2. Read `{board_dir}/board/` for ALL prior skill outputs:
   - If `deck-render-output.yaml` exists: read `hero_message_as_rendered` to ensure the enablement card's stat bar matches the deck's hero message.
   - If `cheatsheet-render-output.yaml` exists: read `proof_points_used` to avoid duplication. The enablement card should use role-specific proof points, not repeat the cheatsheet's.
   - If `one-pager-render-output.yaml` exists: read `competitive_frame_as_rendered` to maintain consistency in objection handling.
   - Read ALL `recommendations_for_downstream` entries where `target_skill` = "enablement-card-render".
3. `{board_dir}/strategy-contract.yaml` (at the coordinator root, NOT in `board/`) is the LIVING strategy. Use it instead of any stale copy.

**If `_meta.board_dir` is absent** — standalone mode. Skip this section entirely. Zero cost.

## Board Write Protocol (Coordinated Mode)

**Only when `_meta.board_dir` is present.** Execute this AFTER Pass 4 (Rendering) succeeds and BEFORE symlinking to the Customer folder. **If Pass 4 fails** (Chrome crash, PDF generation error), do NOT write the board entry — log the render failure to `failures.yaml` instead.

Write a board entry to `{board_dir}/board/enablement-card-render-{role}-output.yaml` (one per role variant):

```yaml
skill_name: "enablement-card-render"
invoked_at: "{ISO 8601 timestamp}"
invoked_by: "{coordinator name from _meta.coordinator}"

artifact_path: "{absolute path to final .md and .html/.pdf}"
artifact_type: "enablement-card"

# Role-specific metadata
role_variant: "{bdr|ae|sa|manager|csm}"
output_mode: "{hub_and_spoke|self_contained}"
section_count: N
max_sections_budget: N

# What the card contains (for downstream skills to read)
hero_message_as_rendered: "{the stat bar / hero metric as it appears}"
proof_points_used:
  - point: "{proof point text}"
    section: "{which section contains it}"
    treatment: "{quotable|logos|benchmarks|pipeline_metrics}"
competitive_frame_as_rendered: "{objection response positioning}"

# Render status (Pass 4)
render_status: "pdf_success"            # pdf_success | pdf_failed | html_only
render_format: "html+pdf"              # what was actually produced

# Quality from existing 10-criterion rubric (Pass 3)
quality_score: N                        # total from rubric (0-20)
quality_max: 20
quality_pass: true/false                # >= 15
quality_notes: ""
per_dimension_scores:
  situation_routing: N
  retrieval_speed: N
  title_specificity: N
  inverted_pyramid: N
  objection_pairing: N
  timing_discipline: N
  handoff_continuity: N
  proof_integration: N
  cognitive_load: N
  role_calibration: N

# Anti-patterns detected during generation
anti_patterns_detected: []              # list from Pass 1 Step 1.4 screen

# Amendments
strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []

recommendations_for_downstream: []
# enablement-card is typically the last render primitive in the pipeline.
# If you DO have downstream advice (e.g., for email-render), add an entry:
#   - target_skill: "email-render"
#     recommendation: "reference the {role} quick-start terminology in follow-up"
#     priority: "medium"
```

Use the Write tool to create this file. If the file already exists (retry scenario), overwrite it.

**If `_meta.board_dir` is absent** — skip board write entirely. Do not create any files.

### Strategy Contract Integration (when available)

If a strategy contract is provided (standalone or via board), read `deck_mode` fields:
- `deck_mode.framing_style` → Adapt objection response framing: `loss` = frame objections as active pain ("You're losing $X to..."), `ease` = frame as simpler alternative ("This replaces your 12-step process with 3 clicks"), `recognition` = frame as familiar pattern ("You've seen this before when...")
- `deck_mode.audience_class` → Cross-reference with `role_profile` for content depth calibration

## Input Modes

### Mode 1: From Strategy YAML + Research (preferred)
```
/enablement-card-render path/to/strategy.yaml --role=bdr
```
Strategy provides the `enablement_card_strategy` block. Research provides atoms (`[!tldr]`, `[!pain-business]`, `[!objection]`, `[!proof]`, `[!buying-committee]`, etc.). The `--role` flag identifies which `role_profile` to load.

### Mode 2: From Product + Vertical + Role Description
```
/enablement-card-render "Lakebase for HLS BDRs"
```
You MUST complete Pass 0 (Socratic phase) and produce a strategy contract before generating. Do not skip this.

### Mode 3: From Existing Content (rewrite/improve)
```
/enablement-card-render path/to/existing-card.md --rewrite --role=sa
```
Score against rubric, identify failures, rebuild using the pass workflow below. Emit BEFORE and AFTER scores.

---

## Workflow: 3-Pass Generation with Mandatory Gates

### Pass 0: Socratic Phase (MANDATORY — cannot be skipped)

Resolve all inputs before any content is generated. Ask the user up to 6 questions. Do not proceed until every required field in the strategy contract is populated.

**Questions to resolve:**

| # | Question | Maps To | Exit Criteria |
|---|----------|---------|---------------|
| 1 | What product/solution is this for? | `product` | Named product, not vague category |
| 2 | What vertical? (or "general" if horizontal) | `vertical` | Specific vertical or explicit "general" |
| 3 | Which role? | `role` | Valid role with defined role_profile |
| 4 | What are the top 3-5 target titles? | `target_titles` | Real titles searchable in LinkedIn |
| 5 | What are the top use cases and proof points? | `use_cases` | Named customers with metrics |
| 6 | What's the competitive context? | `competitive_context` | Primary competitor or "no direct competitor" |

**If research atoms are available**, pre-fill answers from:
- `[!buying-committee]` → target titles
- `[!use-case]` + `[!proof]` → use cases with proof
- `[!objection]` → objection list
- `[!competitive]` → competitive context
- `[!warning]` → known limitations
- `[!specs]` → qualification criteria

**Output mode override:** If user explicitly requests `--hub-and-spoke` or `--self-contained` (or equivalent phrasing), override the profile default. Otherwise, output_mode is loaded automatically from the role_profile.

**Load role_profile immediately after role is confirmed:**
```
ROLE PROFILE LOADED:
  role:                 [role]
  workflow_context:     [value]
  time_pressure:        [seconds|minutes|hours|days]
  technical_depth:      [shallow|moderate|deep]
  strategic_depth:      [shallow|moderate|deep]
  core_question:        [value]
  persona_orientation:  [value]
  objection_surface:    [surface|commercial|technical|program]
  proof_type:           [quotable|logos|benchmarks|pipeline_metrics]
  output_mode:          [hub_and_spoke|self_contained]
  help_router_frame:    [call_situation|deal_stage|architecture|coaching]
  max_pages:            [int]
  max_sections:         [int]
  language_register:    [description]
```

**Present the pre-filled strategy contract for user approval:**

```
STRATEGY CONTRACT:
  product:            [value] ✓|✗
  vertical:           [value] ✓|✗
  role:               [value] ✓|✗ → role_profile loaded
  target_titles:      [list]  ✓|✗ (must be real job titles)
  use_cases:          [count] ✓|✗ (3-5 required, each with proof)
  objections:         [count] ✓|✗ (count calibrated by objection_surface)
  qualification:      [G/Y/R] ✓|✗ (green, yellow, red signals)
  handoff:            [value] ✓|✗ (to_role, criteria, info_to_pass)
  collateral_links:   [count] ✓|✗ (linked assets for this stage)
  competitive_context:[value] ✓|✗
  compliance_notes:   [value] ✓|✗ (or "N/A")
  incentive_info:     [value] ✓|✗ (or "N/A")
  last_validated:     [date]  ✓|✗
CONTRACT: VALID | INVALID → [list what's missing]
```

**Gate:** Do not proceed to Pass 1 until the user confirms the strategy contract. If INVALID, request the missing fields.

---

### Pass 1: Strategy Skeleton

**Step 1.1: Run Section Composition Algorithm**

Load the section menu from `enablement-card-patterns.md` and apply selection rules against the loaded `role_profile`:

```python
# Pseudocode — do NOT hardcode role names
for section in SECTION_MENU:
    if section.selection_rule.matches(role_profile):
        selected_sections.append(section)

# Priority sort
selected_sections.sort(key=lambda s: s.priority_tier)

# Cognitive budget enforcement
if len(selected_sections) > role_profile.max_sections:
    keep P1 sections (never drop)
    fill remaining budget with P2, then P3
    drop lowest-priority sections first
```

**Step 1.2: Present Selected Sections**

```
SECTION COMPOSITION:
  Role profile:       [role] (loaded from philosophy.md)
  Output mode:        [hub_and_spoke|self_contained]
  Max sections:       [role_profile.max_sections]
  Selected sections:  [count]
  Budget status:      WITHIN BUDGET | OVER BY [N] → dropping [sections]

SECTIONS:
  [1] [Section name] (P[tier])
      Selection: [why this section was included]
      Depth adaptation: [how content adapts based on technical_depth/strategic_depth]
      Frame adaptation: [how structure adapts based on help_router_frame]
      Source atoms: [which research atoms feed this]
      Gap: [if any required atom missing]

  [2] [Section name] (P[tier])
      ...

# Additional block for hub_and_spoke only:
HUB-AND-SPOKE PLAN:
  Landing Page:
    - Stat Bar: [source metrics]
    - Elevator Pitch: [source]
    - Read-Do Scripts on Hub: [list with justification]
      - "[script name]" — stays on hub because: [read aloud mid-call, <30s, >50% frequency]
    - Situation Router: [N situations] → [N satellites]
    - Handoff Quick-Check: [compressed criteria]
    - Collateral Links: [N assets]

  Satellites ([N] files):
    1. [satellite-name].md — sections: [list]
    2. [satellite-name].md — sections: [list]
    ...

  Total files to generate: [N+1]
```

**Step 1.3: Specify Per-Section Details**

For each selected section:
```
SECTION [N]: [Header — must be a situation, not a topic]
  Template: [which structural template from patterns.md]
  Source atoms: [which research atoms feed this section]
  Content type: script | table | paired-objection | checklist | reference
  Priority: P1 | P2 | P3
  Tech depth: [role_profile.technical_depth] → [specific adaptation]
  Strategic depth: [role_profile.strategic_depth] → [specific adaptation]
  Register: [role_profile.language_register] → [vocabulary constraints]
  Gap: [if any required atom is missing, flag here]
```

**Step 1.4: Anti-Pattern Pre-Screen**

Run the 7 anti-patterns from philosophy.md:

```
ANTI-PATTERN SCREEN:
  "Training Deck Excerpt":  ✓ CLEAR | ⚠ AT RISK → [evidence]
  "Feature Catalog":        ✓ CLEAR | ⚠ AT RISK → [evidence]
  "Persona Fiction":        ✓ CLEAR | ⚠ AT RISK → [evidence]
  "Encyclopedia":           ✓ CLEAR | ⚠ AT RISK → [evidence]
  "Hedge Garden":           ✓ CLEAR | ⚠ AT RISK → [evidence]
  "Island":                 ✓ CLEAR | ⚠ AT RISK → [evidence]
  "Stale Reference":        ✓ CLEAR | ⚠ AT RISK → [evidence]
SCREEN: CLEAR | [N] RISKS → [mitigations]
```

**Gate:** Present skeleton to user for approval. User must confirm before Pass 2.

---

### Pass 2: Full Generation

Generate the complete enablement card in markdown, following the approved skeleton.

**5 Transformation Rules (apply during generation):**

#### Rule 1: Register Adaptation
Adjust language to match `role_profile.language_register`. Do NOT hardcode role names — read the register description and apply it.

```
role_profile.language_register: "Business only. Zero technical terms. Conversational."
→ Strip all technical jargon. Use short sentences. Write as spoken.

role_profile.language_register: "Full technical depth. Architecture terms expected."
→ Use precise technical terminology. Include specifications. Never hand-wave.
```

#### Rule 2: Timing Enforcement
Every scripted element gets a timing badge. Validate by read-aloud. Timing budgets are derived from `role_profile.time_pressure`:

| time_pressure | Implication |
|---------------|-------------|
| `seconds` | Openers ≤10s, voicemails ≤30s, pitches ≤15s |
| `minutes` | Discovery ≤5min, elevator pitch ≤30s |
| `hours` | Can include longer-form content, but still chunked |
| `days` | Strategic content, less timing-critical |

#### Rule 3: Situation Headers
Every H2/H3 must describe a situation the user faces, not a product topic. This is driven by `role_profile.help_router_frame`:

| help_router_frame | Header Pattern |
|-------------------|----------------|
| `call_situation` | "They Pick Up", "They Push Back", "They Ask About Pricing" |
| `deal_stage` | "First Discovery", "After Demo", "Procurement Stall" |
| `architecture` | "They Ask About Scale", "They Ask About Security" |
| `coaching` | "Deal is Stalling", "Champion is Weak" |

#### Rule 4: Proof Discipline
Every proof point must include: named customer + specific metric + timeframe. Format is driven by `role_profile.proof_type`:

| proof_type | Format |
|------------|--------|
| `quotable` | Quote + name + outcome (for verbal use) |
| `logos` | Logo + metric + use case (for slides) |
| `benchmarks` | Technical metric + methodology + source |
| `pipeline_metrics` | Deal stats for coaching |

No proof point with confidence below HIGH. If LOW confidence, flag: "⚠ Unverified — do not use in customer conversations until confirmed."

#### Rule 5: Objection Pairing
Every objection has an immediate response. No orphaned objections. Objection selection is driven by `role_profile.objection_surface`:

| objection_surface | Objection Types to Include |
|-------------------|---------------------------|
| `surface` | First-call brush-offs |
| `commercial` | Business/value objections |
| `technical` | Architecture/capability objections |
| `program` | Execution/team objections |

Format:
```markdown
**"[What the prospect says]"**
> [What you say back — specific, confident, proof-backed]
```

#### Rule 6: Output Mode Enforcement

If `hub_and_spoke`:
- Generate landing page first
- Landing page MUST fit under ~400 words / ~1 printed page
- Critical Read-Do scripts appear as blockquote boxes with timing badges
  - **Read-Do selection criteria** (from patterns.md): `time_pressure: seconds` AND script is under 30 seconds spoken AND script is used on >50% of task instances. Typical candidates: cold call opener, voicemail, #1 most common objection response.
- Situation router renders as table with emoji + label + relative link
- Every satellite has back-link to landing page
- Every satellite linked from router (no orphan files)
- Satellite filenames follow convention: `{product}-{vertical}-{role}-{satellite-name}.md`

**Satellite gap resolution (MANDATORY after landing page):**
After generating the landing page, check whether each satellite linked from the router exists:

```
SATELLITE STATUS:
  [satellite-name].md — ✓ EXISTS | ✗ MISSING
  [satellite-name].md — ✓ EXISTS | ✗ MISSING
  ...
  Missing: [N] of [total]
```

If ANY satellites are missing:
1. **Ask the user:** "N satellite docs are missing. Generate them now, or leave as placeholders?"
2. **If user confirms generation:** Generate each missing satellite as a standalone markdown file using the same Pass 2 transformation rules (register adaptation, timing, situation headers, proof discipline, objection pairing). Each satellite contains:
   - Back-link to landing page at top
   - The sections assigned to that satellite (from the hub-and-spoke plan in Step 1.2)
   - Adapted depth/register matching the role_profile
3. **If user declines:** Leave placeholder links (`#`) and emit gap flags in the output summary
4. Satellite generation does NOT re-run Pass 0 or Pass 1 — the skeleton is already approved. It generates content for the assigned sections only.

If `self_contained`:
- Single document with anchor TOC at top
- TOC entries use situation-framed labels (not section type names)
- Every H2 has matching anchor slug

#### Rule 7: First-Line-Actionable (Cohan's "Do the Last Thing First")

The first line of every section must tell the rep what to **do** or **say** — not provide background context. This is the micro-level application of Cohan's Inverted Pyramid (P4 in philosophy.md).

**Test during generation:** Read only the first line of each section you've written. If it provides context, background, or explanation before the actionable content, rewrite it. The hook, proof point, or scripted response comes first. Supporting context follows.

```
❌ "Lakebase is a Postgres-compatible database built on the lakehouse..."
✅ "Tell them: 'Teams like Ensemble Health went from 20-hour syncs to 4 minutes.'"

❌ "HIPAA compliance is a common concern in healthcare..."
✅ "Say: 'We run on Databricks' secure infrastructure — encrypted, private networking, access controls.'"
```

---

### Pass 3: Evaluation

Run the 10-criteria rubric from `enablement-card-philosophy.md`:

```
RUBRIC:
  #1  Situation Routing:     [0|1|2] — [reason]
  #2  Retrieval Speed:       [0|1|2] — [reason]
  #3  Title Specificity:     [0|1|2] — [reason]
  #4  Inverted Pyramid:      [0|1|2] — [reason]
  #5  Objection Pairing:     [0|1|2] — [reason]
  #6  Timing Discipline:     [0|1|2] — [reason]
  #7  Handoff Continuity:    [0|1|2] — [reason]
  #8  Proof Integration:     [0|1|2] — [reason]
  #9  Cognitive Load:        [0|1|2] — [reason]
  #10 Role Calibration:      [0|1|2] — [reason]
  ─────────────────────────────────────
  TOTAL: [X]/20
  THRESHOLD: 15/20 (75%) = PASS | 18/20 (90%) = GREAT
  RESULT: PASS | FAIL → [list criteria scoring 0]
```

**If FAIL (<15/20):** Fix all criteria scoring 0. These are structural failures. Re-evaluate after fixes. Maximum 2 fix cycles.

**If PASS but not GREAT (15-17/20):** Fix criteria scoring 1 where effort is reasonable. One fix cycle maximum.

**Per-principle micro-tests (from philosophy.md):** For each criterion scoring 1, run the corresponding principle's specific test to determine if it's fixable:
- **#2 (Retrieval Speed):** Hand-the-card-to-stranger test — can they find the answer in 10 seconds?
- **#3 (Title Specificity):** LinkedIn Sales Navigator paste test — do the titles return results?
- **#5 (Objection Pairing):** Count objections, count responses — 1:1 ratio? Visually paired?
- **#6 (Timing Discipline):** Read each script aloud and time it — within budget?
- **#7 (Handoff Continuity):** Remove the handoff section — does the rep know what to do next? If not, it's incomplete.

**10-Second Retrieval Meta-Test (run last):**
```
10-SECOND TEST:
  Scenario: "[Specific situation matching role_profile.core_question]"
  Can an unfamiliar user find the answer in 10 seconds?
  ANSWER: YES | NO → [what to restructure for faster retrieval]
```

**Architecture Validation (hub_and_spoke only):**
```
ARCHITECTURE CHECK:
  ✓ Landing page under 400 words? [YES|NO]
  ✓ Read-Do scripts on hub (no click required)? [YES|NO]
  ✓ All satellites linked from router? [YES|NO]
  ✓ All satellites have back-link? [YES|NO]
  ✓ Router covers all generated satellites? [YES|NO]
```

**Architecture Validation (self_contained only):**
```
ARCHITECTURE CHECK:
  ✓ Anchor TOC present? [YES|NO]
  ✓ TOC entries situation-framed? [YES|NO]
  ✓ All H2s have matching anchors? [YES|NO]
```

---

## Output

### Primary Output: Markdown

**For self_contained mode:**
```
✓ Enablement card rendered: {product}-{vertical}-{role}-enablement.md
✓ Role: [role] | Profile: [role_profile loaded]
✓ Output mode: self_contained
✓ Product: [product] | Vertical: [vertical]
✓ Sections: [count] / [role_profile.max_sections] budget
✓ Anchor TOC entries: [N]
✓ Rubric score: [X]/20 ([PASS|GREAT])
✓ Content provenance: [N] atoms from research, [N] HIGH confidence
✓ Anti-patterns: [N] screened, [N] clear, [N] mitigated
✓ Timing validated: [N] scripts, all within budget
✓ Total files: 1
```

**For hub_and_spoke mode:**
```
✓ Landing page rendered: {product}-{vertical}-{role}-quick-start.md
✓ Role: [role] | Profile: [role_profile loaded]
✓ Output mode: hub_and_spoke
✓ Product: [product] | Vertical: [vertical]
✓ Landing page size: [word count] (target: <400)
✓ Read-Do scripts on hub: [list]
✓ Satellites: [N] total ([M] pre-existing, [K] generated, [J] placeholder)
✓ Generated satellites: [list filenames]  ← only if K > 0
✓ Placeholder gaps: [list filenames]      ← only if J > 0
✓ Rubric score: [X]/20 ([PASS|GREAT])
✓ Content provenance: [N] atoms from research, [N] HIGH confidence
✓ Anti-patterns: [N] screened, [N] clear, [N] mitigated
✓ Timing validated: [N] scripts, all within budget
✓ Total files generated: [1 + K]
```

Strategy Contract:
  Role profile: [role] → tech:[value] strategic:[value] register:[summary]
  Target titles: [list]
  Use cases: [count] with proof
  Objections: [count] paired (surface: [objection_surface])
  Handoff: → [strategy.handoff.to_role]

Section Composition:
  [List of sections with priority tiers]
```

---

### Symlink to Customer Folder

After saving the enablement card, symlink it into `~/Customer/[account]/03-Reference_Docs/` so it's accessible from Finder organized by account. The source file remains the source of truth.

**Account name mapping:** spaces → underscores (e.g., "Mayo Clinic" → "Mayo_Clinic").

```bash
# Create account folder structure if it doesn't exist
for sub in 01-Emails 02-Decks 03-Reference_Docs 04-Notebooks 05-Proposals 06-Meeting_Prep 07-Contracts_Legal 08-Screenshots; do
  mkdir -p ~/Customer/[account_folder]/$sub
done

# Symlink the enablement card (and PDF if rendered)
ln -sf /absolute/path/to/[filename].md ~/Customer/[account_folder]/03-Reference_Docs/[filename].md
# If Pass 4 renders PDF:
ln -sf /absolute/path/to/[filename].pdf ~/Customer/[account_folder]/03-Reference_Docs/[filename].pdf
```

- Use `-sf` (force) to overwrite stale symlinks if re-generating
- Always use full absolute paths in the symlink target
- If the card is generic (no specific account), skip this step

---

### Pass 4: Rendering (HTML → PDF)

This pass converts the markdown to styled HTML and PDF. **Always run** — PDF is mandatory (Google Drive opens HTML as source code).

**Step 4.1: Prepare Output Directory**

```bash
mkdir -p output/rendered
```

**Step 4.2: Generate HTML**

Read the HTML template from `enablement-card-patterns.md` and populate with generated content:

1. Load the appropriate template:
   - `hub_and_spoke` → Landing Page HTML template
   - `self_contained` → Self-Contained HTML template

2. Apply brand colors from `~/.claude/skills/deck-render/references/design-rules.md`, using WCAG AA accessible variants:

   **On light/white backgrounds:**
   - Links/info: #1A5A8F (7.2:1 contrast on white)
   - Success/scripts (text): #006644 (7.3:1 on white). Keep #00A972 for borders/decorative only.
   - Discovery/warnings (text): #705510 (7.1:1 on white). Keep #FFAB00 for borders/decorative only.
   - Timing labels/metadata: #3D5A66 (7.1:1 on white)
   - Footer text: #3D5A66 (7.1:1 on white)

   **On dark backgrounds (#0B2026, #0D1F2D):**
   - Stat bar accent numbers: #FF8A7A (8.1:1 on #0B2026)
   - AI card examples text: #B8CCD6 (9.3:1 on #0B2026)
   - AI card links: #5CEBA0 (9.1:1 on #0B2026)
   - Proof block customer name: #6EB5E5 (7.8:1 on #0D1F2D)

   **Always (context-independent):**
   - Dark bg: #0B2026
   - White text on dark: #FFFFFF
   - Accent: #FF3621 (Databricks red — use sparingly, decorative/borders only)

3. Populate sections from markdown content:
   - Convert markdown tables → HTML `<table>` with proper styling
   - Convert blockquotes → styled `.script-box` or `.objection-response` divs
   - Convert headers → styled `<h2>`, `<h3>` with timing badges
   - Convert emoji signals → colored text spans

4. Write HTML file:
   ```
   output/{product}-{vertical}-{role}-{type}.html
   ```

**Step 4.3: Render to PDF**

Always generate PDF alongside HTML (Google Drive opens HTML as source code):

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu \
  --print-to-pdf="output/{name}.pdf" --no-margins --print-background \
  "output/{name}.html"
```

**Step 4.4: Visual QA (for hub_and_spoke only)**

Convert PDF to PNG for visual inspection:

```bash
pdftoppm -png -r 200 -singlefile output/{name}.pdf output/rendered/{name}
```

Check the PNG for:
- [ ] Stat bar renders correctly (dark bg, white text, red accents)
- [ ] Scripts visible and legible (green left border)
- [ ] Router table is aligned and links are styled
- [ ] AI Assistant card is prominent
- [ ] No text overflow or clipping
- [ ] Page fits on single Letter sheet

**Step 4.5: Output Summary**

```
✓ HTML rendered: output/{product}-{vertical}-{role}-{type}.html
✓ PDF rendered: output/{product}-{vertical}-{role}-{type}.pdf
✓ Visual QA: output/rendered/{name}.png (if hub_and_spoke)
✓ Page count: [N] pages
✓ File size: [X] KB
```

---

## Output Formats

| Format | When | Command | Notes |
|--------|------|---------|-------|
| **Markdown** | Always (master format) | — | Editable, copy-paste friendly |
| **HTML** | User requests, or for browser viewing | Pass 4 | Styled with brand colors |
| **PDF** | Always (mandatory alongside HTML) | Pass 4 | Via Chrome headless |
| **DOCX** | User requests (rare) | `pandoc input.md -o output.docx` | For teams that edit in Word |

**Default behavior:** Generate markdown + HTML + PDF. Pass 4 always runs to ensure PDF is available for Google Drive distribution.

---

## Multi-Role Generation

When the user requests cards for multiple roles in one pass:

```
/enablement-card-render "Lakebase for HLS" --roles=bdr,ae,sa,manager
```

**Workflow:**

1. **Pass 0 runs ONCE** — the strategy contract is shared across roles (product, vertical, use cases, proof, competitive context are common).

2. **For each role:**
   - Load that role's `role_profile` from philosophy.md
   - Run Pass 1: section composition using that profile's attributes
   - Present skeleton for approval

3. **After all skeletons approved:**
   - Run Pass 2 per role — generate each card
   - Run Pass 3 per role — evaluate each independently

4. **Cross-card validation (after all cards generated):**

```
CROSS-CARD CHECK:
  Role profiles loaded: [list of roles]
  Output modes: [role: mode, role: mode, ...]

  Handoff continuity:
    [role_1] → [role_1.handoff.to_role]: ✓|✗
    [role_2] → [role_2.handoff.to_role]: ✓|✗
    ...

  Messaging consistency:
    Core pitch consistent across depth levels? ✓|✗
    Proof points used with appropriate proof_type per role? ✓|✗

  Collateral coverage:
    Every role links to stage-appropriate assets? ✓|✗

  Title consistency:
    No persona abstractions in any card? ✓|✗
    Buying committee titles consistent across cards? ✓|✗

  Cross-mode validation (when BDR=hub_and_spoke, others=self_contained):
    BDR's handoff satellite references AE card filename? ✓|✗
    Handoff criteria consistent across BDR handoff section and AE expected inputs? ✓|✗
```

---

## Refresh Workflow

When research changes and existing cards need updating:

```
/enablement-card-render path/to/existing-card.md --refresh --research=path/to/new-research.md
```

**Workflow:**

1. **Load existing card** — extract the role from metadata, load corresponding `role_profile`

2. **Diff research** — compare new atoms against atoms used in existing card:
   - New proof points
   - Changed objections
   - Updated compliance status
   - New use cases
   - Stale facts (>90 days since validation)

3. **Generate patch report:**
```
REFRESH ANALYSIS:
  Card: [filename]
  Role profile: [role]
  Last validated: [date] → STALE (>[N] days) | CURRENT

  NEW ATOMS:
    [!proof] "Customer X" — ADD to section [N]
    [!objection] "New objection" — ADD to objection pairs

  CHANGED ATOMS:
    [!compliance] HIPAA status: [old] → [new] — UPDATE section [N]

  STALE CONTENT:
    Proof point "[old proof]" — last validated [date] — FLAG for review

  RECOMMENDED PATCHES: [count]
```

4. **Apply patches surgically** — preserve human edits, update only research-sourced content

5. **Re-validate** — run Pass 3 evaluation, update `last_validated` date

---

## Dependencies

| Dependency | Type | Required? | Purpose |
|---|---|---|---|
| `enablement-card-philosophy.md` | Reference | **Yes** | Role profiles, rubric, anti-patterns, strategy schema |
| `enablement-card-patterns.md` | Reference | **Yes** | Section menu, composition algorithm, templates |
| Research file (`research/products/*.md`) | Knowledge | **Yes** | Source atoms |
| Vertical context (`research/verticals/*.md`) | Knowledge | Recommended | Vertical-specific context |
| `[!buying-committee]` atom | Content | Required | Title specificity (criterion #3) |
| `[!objection]` atom | Content | Required | Objection pairing (criterion #5) |
| `[!proof]` atom | Content | Required | Proof integration (criterion #8) |
| `[!use-case]` atom | Content | Required | Use case sections |
| `[!warning]` atom | Content | Required for deep | SA limitations section |
| `[!discovery-questions]` atom | Content | Required for moderate/deep | Discovery framework |
| `~/.claude/skills/deck-render/references/design-rules.md` | Reference | Only for HTML/PDF | Brand styling (Databricks palette) |
| Playwright (MCP) | Tool | Only for PDF | HTML → PDF via `browser_run_code` + `page.pdf()` |
| `wkhtmltopdf` | CLI tool | Alternative | HTML → PDF conversion (if installed) |
| `pdftoppm` | CLI tool | Only for visual QA | PDF → PNG for Pass 4 visual inspection |
| `pandoc` | CLI tool | Only for DOCX | Word conversion (rare) |

---

## Test Cases

### Test Case 1: Single Role — BDR (hub_and_spoke)
**Input:** Full product research with all atom types. `--role=bdr`
**Expected:**
- role_profile loaded: `technical_depth=shallow`, `strategic_depth=shallow`, `time_pressure=seconds`, `objection_surface=surface`, `output_mode=hub_and_spoke`
- Landing page under 400 words
- Cold call opener and HIPAA script on landing page (Read-Do principle: `time_pressure=seconds` + script <30s + >50% frequency)
- Router grid links to 6-8 satellite docs (call-track, vm-scripts, faq, objections, qualification, handoff)
- Missing satellites offered for generation; if accepted, generated as standalone files with back-links
- All scripts under timing budgets (opener ≤10s, voicemail ≤30s)
- Titles are real LinkedIn-searchable titles
- Total files generated: **1 + K** (landing page + K generated satellites)
**Validation:** Rubric ≥15/20. 10-second retrieval passes. Architecture validation passes. No role-name branching.

### Test Case 2: Single Role — SA
**Input:** Same research. `--role=sa`
**Expected:**
- role_profile loaded: `technical_depth=deep`, `strategic_depth=moderate`, `time_pressure=minutes`, `objection_surface=technical`
- Section composition: 16 sections max, includes Demo Quick-Reference, POC Scoping, Known Limitations
- Language register: full technical depth
- Proof format: benchmarks with methodology
**Validation:** No BDR-level simplification. Technical terms present. Handoff to production.

### Test Case 3: Multi-Role Generation
**Input:** Product research. `--roles=bdr,ae,sa,manager`
**Expected:**
- Pass 0 runs once (shared strategy)
- 4 different role_profiles loaded
- 4 cards generated with different section compositions
- Cross-card validation passes: handoff chain continuous, messaging consistent, proof aligned
**Validation:** Each card matches its role_profile constraints.

### Test Case 4: New Role (Extensibility Test)
**Input:** Research. `--role=csm` (with csm profile defined in philosophy.md)
**Expected:**
- role_profile for CSM loaded
- Section composition algorithm selects sections based on CSM profile attributes
- No code changes required — profile drives everything
**Validation:** Card generated successfully with no hardcoded CSM logic.

### Test Case 5: Gap Handling
**Input:** Minimal research (only `[!tldr]` and `[!pain-business]` atoms exist). `--role=ae`
**Expected:**
- Skeleton with gaps clearly flagged for P1 sections
- No fabricated proof points
- Socratic phase identifies missing atoms and asks user to provide or skip
- Reduced section count if required atoms unavailable
**Validation:** Gaps explicitly shown. No hallucinated content.

### Test Case 6: Output Mode Override
**Input:** Full product research. `--role=bdr --output-mode=self_contained`
**Expected:**
- role_profile loaded with `output_mode` overridden from `hub_and_spoke` to `self_contained`
- Single document generated (not landing page + satellites)
- Anchor TOC at top with situation-framed labels
- All H2s have matching anchors
- No satellite files generated
**Validation:** Override applied correctly. Architecture validation for self_contained mode passes.

---

## Architectural Invariants

These invariants must hold for every generation:

1. **No role-name branching** — The skill never uses `if role == "X"`. All behavior derived from role_profile attributes.

2. **Profile-driven composition** — Section selection is determined by selection rules matching role_profile, not hardcoded lists.

3. **Depth adaptation is parametric** — Content length, vocabulary, and detail level derived from `role_profile.technical_depth` and `role_profile.strategic_depth`, not role name. Technical sections key on `technical_depth`; strategic sections key on `strategic_depth`.

4. **Register adaptation is descriptive** — Language calibration uses `role_profile.language_register` description, not role-specific rules.

5. **Extensibility without modification** — Adding a new role requires only a new role_profile in philosophy.md. No changes to patterns.md or SKILL.md.

---

*This is the orchestration layer. The expert judgment lives in `enablement-card-philosophy.md`. The section menu and composition algorithm live in `enablement-card-patterns.md`. This file tells the system how to use both without hardcoding role-specific logic.*

---

## $ARGUMENTS

Accept the user's input and begin at the appropriate pass. If arguments include a path to a strategy YAML, load it and skip to Pass 1. If arguments are a free-text description, begin at Pass 0.
