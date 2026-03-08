---
name: cheatsheet-render
description: "Render a cheat sheet (cognitive prosthetic) as a single-file HTML with dark-mode card grid. USE WHEN: user says 'cheat sheet', 'quick reference', 'field reference', or needs a scannable mid-task lookup tool for any domain or role."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
---

# Cheat Sheet Render Skill

## Trigger
Invoke when the user requests a cheat sheet, quick-reference card, or field reference for any domain or role.

## Workflow

### Step 1: Read References
Before generating anything, read all reference files:
1. `references/cheatsheet-philosophy.md` — Evaluation rubric and judgment criteria
2. `references/cheatsheet-patterns.md` — Card templates and tactical formulas
3. `references/cheatsheet-design-rules.md` — Visual grammar and specifications
4. `references/design-rules.md` — Shared brand palette (if present — use org colors over defaults)
5. `_System/tailoring/hls-tailoring-map.yaml` (in vault root) — **HLS Audience Tailoring Engine** (if domain is HLS/healthcare/clinical). This is a shared file — not skill-local. Read from the vault path.

### Step 1.5: Board Read Protocol (Coordinated Mode)

Check the strategy contract (strategy YAML or strategy-contract.yaml) for a `_meta.board_dir` field.

**If `_meta.board_dir` is present** — you are running inside a coordinator pipeline:
1. Read `{board_dir}/invariants.yaml` if it exists. These are HARD constraints:
   - `hero_message` — must appear verbatim (or semantic equivalent) in the cheat sheet banner or first card
   - `proof_points[].assigned_to` — only use proof points assigned to "cheatsheet" or "all"
   - `competitive_frame` — use this positioning for any competitive counter cards
   - `call_to_action` — unified CTA in footer
2. Read `{board_dir}/board/deck-render-output.yaml` if it exists. This is the deck that was rendered BEFORE you:
   - `hero_message_as_rendered` — your hero must match or complement this
   - `proof_points_used` — if a proof point was used as a stat hero in the deck, use it as a supporting reference (not a hero) in the cheat sheet to avoid redundancy
   - `competitive_frame_as_rendered` — your competitive cards must align
   - `recommendations_for_downstream` — check if deck-render left notes for cheatsheet-render
3. Read any other board entries in `{board_dir}/board/` for context from other upstream skills.
4. `{board_dir}/strategy-contract.yaml` (at the coordinator root, NOT in `board/`) is the LIVING strategy. Use it instead of any stale copy. Check its `version` field — higher = more recent amendments.
5. If `strategy-contract.yaml` contains `deck_mode.framing_style`, use it as the default tone for trigger-response and metrics cards. Loss framing → frame evidence as active loss ("They're losing $X/month to..."). Ease framing → frame evidence as simpler-than-status-quo ("This is 3 questions instead of your current 12-field form"). Recognition framing → frame evidence as patterns they'll recognize ("You've seen this before when...").

**If `_meta.board_dir` is absent** — standalone mode. Ignore this section entirely. Zero cost.

**Standalone mode:** If a strategy contract is provided directly (not via board), also check for `deck_mode.framing_style`. If present, use it as the default tone for trigger-response and metrics cards (same behavior as coordinated mode).

### Step 2: Extract or Infer Strategy Contract
The user's prompt (or an upstream `/strategy` output) must provide these fields. If missing, infer from context or ask:

```yaml
required:
  audience.role: string            # Who is using this? (SA, AE, DBA, CSM, etc.)
  audience.experience_level: string # new_to_domain | familiar | expert
  context.domain: string           # What domain? (Healthcare RCM, Unity Catalog, etc.)
  context.moment: string           # apply | remember | solve | learn_new
  context.usage: string            # live_interaction | prep | onboarding
  content.card_topics: list        # What cards to include
  content.action_types: list       # talk_tracks | commands | discovery_questions | etc.
```

If the user provides raw content (e.g., meeting notes, a domain overview, a product doc), extract the strategy contract fields from the content before rendering.

### Step 2.3: Apply Tailoring Map (if HLS domain)

If `context.domain` contains "HLS", "healthcare", "clinical", or "health system":

1. Read `_System/tailoring/hls-tailoring-map.yaml` from the vault root (shared location, not skill-local)
2. Match `audience.role` to the closest profile:
   - Executive / CMIO / CNO / CQO → `clinical_executive`
   - SA / Security / Compliance / Engineer → `technical_gatekeeper`
   - AE / CFO / Revenue → `commercial_lead`
   - CSM / Account Manager → `customer_success`
3. Override the strategy contract with the profile's values:
   - `f_pattern_priority` → sets card order (Card 1 = top-left)
   - `kill_list` → pre-populates Gate 3 (add more, don't subtract)
   - `red_alert` → determines Gate 5 outcome
   - `lava_element` → identifies the single hero metric in `#FF3621`
   - `card_types.include` → starting card selection (gates can still cut)
   - `card_types.exclude` → hard exclusions (gates cannot override)
   - `competitive_split` → determines if counter cards split or unify
4. Apply `cross_profile_rules` for any remaining ambiguity

The tailoring map provides **starting positions, not final answers.** The Pre-Render Gates (Step 2.5) still apply and can cut cards from the tailoring map's `include` list. But they CANNOT add items from the `exclude` list.

### Step 2.5: Pre-Render Gates (MANDATORY)

Before selecting cards or writing HTML, complete ALL of the following gates. Skipping these gates is how "template-filling" overrides "performance design."

#### Gate 1: Moment Diagnosis

Declare the primary moment for this role. This determines F-pattern card priority (top-left = highest frequency need for THAT moment).

| Role | Primary Moment | Card 1 (Top-Left) Should Be |
|---|---|---|
| BDR | **Apply** (mid-call) | Persona targeting or competitive counter — what they need in the first 30 seconds |
| AE | **Apply** (mid-deal) | Objection handling or qualification — the live negotiation tool |
| SA | **Prep + Apply** (pre-demo AND mid-call) | Pre-demo checklist or architecture gate — what they verify before walking in |
| DBA/Engineer | **Solve** (mid-incident) | Troubleshooting tree or error lookup — the diagnostic entry point |
| CSM | **Remember** (mid-review) | Health signals or expansion triggers — what to watch for |

If the role's primary moment is **Prep**, checklists and architecture cards go to Row 1. If **Apply**, trigger-response and competitive cards go to Row 1. Do NOT default everything to Apply.

**Moment reconciliation:** If `context.moment` from the strategy contract differs from Gate 1's diagnosed moment, flag the conflict and use Gate 1's diagnosis. The strategy command may have set a generic moment; the cheatsheet's role-specific moment diagnosis is more precise.

#### Gate 2: Viewport Budget

Calculate max cards BEFORE drafting content. Do not start with topics and hope they fit.

```
Landscape letter: ~11" × 8.5" usable
Banner + footer: ~1.2" consumed
Remaining: ~7.3" for cards
3 rows × ~2.4" each = 9 cards MAX at 0.7rem body font
2 rows × ~3.5" each = 6 cards at 0.75rem body font
```

**Rule:** If role density is HIGH (SA, DBA) and card count is 9, font must be ≤0.7rem body with ≤0.25rem cell padding. Verify AFTER rendering — if it spills to page 2, cut cards until it fits. Never add a second page.

**Cognitive budget override:** If the strategy contract contains `deck_mode.cognitive_budget` (or `cognitive_budget`), use it as a ceiling on card count regardless of viewport fit:
- `executive` → max 6 cards
- `technical` → max 9 cards
- `bdr_field` → max 4 cards
- `clinical` → max 5 cards

#### Gate 3: Kill List (write BEFORE rendering)

List ≥3 items you are intentionally EXCLUDING to stay within the viewport envelope. This is not optional. If you cannot name what you cut, you haven't made hard enough choices.

Format:
```
KILL LIST:
- [Topic cut] — reason: [training content / SA territory / edge case / lookup-not-apply]
- [Topic cut] — reason: [...]
- [Topic cut] — reason: [...]
```

#### Gate 4: Training vs. Performance Audit

For each proposed card, ask: **"Does this audience already know this, or is this teaching them something new?"**

- If teaching → it's **training content** (onboarding layer, not cheat sheet). CUT IT.
- If reminding → it's **performance support**. KEEP IT.

Examples:
- "CMIO = Chief Medical Information Officer" → Training for BDR (they should know already). Cut.
- "CMIO: Lead with Research Agent for 'why did readmissions spike?'" → Performance for SA. Keep.
- "Genie uses a compound AI system" → Training. Cut.
- "25 tables max per space, best practice ≤5" → Performance. Keep.

#### Gate 5: Red Alert Placement

If ANY card topic involves compliance liability, beta features, or PHI/security constraints:
- The Red Alert banner MUST be the **first rendered element** (above the grid, not inside a card)
- It must include: constraint + consequence + safe path
- Do NOT bury compliance warnings in row 3

Only proceed to Step 3 after all five gates pass.

### Step 2.7: Battle-Tested Rules (Learned from Genie HLS exercise, 2026-02)

These rules were earned through iterative failure and head-to-head comparison. They are NOT optional.

#### Rule 1: Competitive Card Splitting

If the domain has competitors from **different conversation triggers** (e.g., EHR-native tools vs. BI tools), split into separate counter cards. Mixing them in one card blurs the "When you hear X" trigger pattern — the SA hears "SlicerDicer" from a CMIO and "Power BI" from a VP Analytics. Different persona, different card.

**Test:** Would the same person say both objections in the same sentence? If no → split.

#### Rule 2: "Drop When" on PROVE Cards

Every metric MUST have a `→ When:` trigger line that tells the user WHEN to deploy that number in conversation. A stat without a trigger is training content (memorize this number). A stat WITH a trigger is performance support (use this number when X happens).

**Format:**
```
[METRIC]  [Source]
→ When: [conversation trigger or persona signal]
```

**Anti-pattern:** "10x faster — Premier Inc." (stat dump, no context on when to say it)
**Correct:** "10x faster — Premier Inc. → When: 'Does this actually work in healthcare?'"

#### Rule 3: Row Labeling

Label each row of the grid with its F-pattern intent. This serves TWO purposes:
1. **For the designer:** Forces you to defend why each card is in that row
2. **For the user:** Provides a visual wayfinding layer above the card grid

**Standard row labels by role:**

| Role | Row 1 | Row 2 | Row 3 |
|---|---|---|---|
| SA | Prep — verify before you walk in | Apply — mid-call weapons | Depth — technical credibility |
| BDR | Target — who and why | Respond — what to say/ask | Prove — close the loop |
| AE | Qualify — is this real | Position — win the deal | Close — terms and urgency |
| DBA | Diagnose — what's broken | Fix — commands and config | Prevent — monitoring and checks |

Row labels use muted text, uppercase, small font (0.5-0.55rem), positioned above each grid section.

#### Rule 4: DECODE Card Overlap Trap

Jargon Decoder cards are the most common source of content overlap. Before including a DECODE card, audit every term against all other cards:

- If the term appears in a Counter card → cut from DECODE
- If the term appears in a Security card → cut from DECODE
- If the term appears in an Architecture card → cut from DECODE

**If >50% of DECODE terms overlap with other cards, replace DECODE entirely.** The best replacement is usually a Persona card (Rule 5) which adds net-new value instead of duplicating content.

#### Rule 5: Persona Card for SA/AE Roles

For SA and AE roles, a persona-to-feature routing card is **performance support, not training**, because it answers: "I'm sitting across from a [CMIO/CNIO/CISO] — what feature do I lead with?"

**Format:**
```
| Persona | → Lead With |
| CMIO    | → [Feature]: "[Example question that feature answers]" |
| CNIO    | → [Feature]: [Metric/use case that resonates] |
```

This card goes in Row 3 (Depth) — it's used during prep or early in the call, not mid-objection.

**Do NOT include persona cards for BDR/CSM roles** — BDRs need trigger-response cards (they don't choose features), CSMs need health signal cards (they don't pitch features).

#### Rule 6: Source Hygiene

Before rendering ANY content from knowledge base files or LLM-generated source material:

1. **Strip citation artifacts:** Remove `[cite_start]`, `[cite: NNN]`, `[source: X]`, and any similar metadata markers
2. **Strip KIQ annotations:** Remove `<!-- KIQ: ... -->` metadata comments
3. **Strip confidence tags:** Remove `**Confidence:** HIGH` inline markers
4. **Verify no metadata leaked into card content:** Search the final HTML for `cite`, `KIQ`, `Confidence:` before saving

**Why:** Citation artifacts from upstream LLMs (Gemini, Claude) render as visible text in HTML/PDF. This was a showstopper production bug in head-to-head testing.

#### Rule 7: Print CSS is Mandatory

Every cheat sheet HTML MUST include a `@media print` block. Without it, Chrome headless renders portrait (not landscape) and cards stack vertically, breaking the single-viewport constraint.

**Required print CSS:**
```css
@media print {
  @page { size: landscape; margin: 0.15cm; }
  body { background: var(--bg) !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .grid { display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 0.3rem !important; }
  .card { break-inside: avoid; page-break-inside: avoid; }
}
```

**`!important` on grid properties is required** — Chrome's print renderer overrides CSS grid unless forced. This was verified empirically.

#### Rule 8: Hero Message Placement

In coordinated mode, the hero message must appear in the **subtitle hero area** (the one-line subtitle under the sheet title, from cheatsheet-design-rules.md). Do NOT make it a card — that wastes one of 9 card slots on a message that belongs in the banner. Do NOT put it in the footer — it won't be seen. The subtitle hero area was designed for exactly this purpose.

### Step 3: Select Card Types
Use the card-type decision framework to map each topic to the right template:

| Content Type | Card Template | When to Use |
|---|---|---|
| Domain vocabulary the user doesn't know yet | **Jargon Decoder (2B)** | User is new to domain; terms will come up in conversation |
| Phrases the user will hear and needs to respond to | **Trigger-Response (2A)** | Live interaction moments; the signature cheat sheet card |
| People/roles the user will interact with | **Persona Card (2C)** | Customer-facing roles who need to tailor by audience |
| Questions the user should ask | **Discovery Questions (2D)** | Pre-call prep; early-stage engagements |
| Statistics or proof points to cite | **Metrics Card (2E)** | Credibility-building; mid-conversation evidence drops |
| Branching decisions ("if X then Y") | **Decision Tree (2F)** | Troubleshooting; triage; qualification logic |
| Sequential steps that must not be skipped | **Checklist (2G)** | Post-call verification; pre-deployment gates; safety-critical steps |
| Competitive positioning or objection handling | **Trigger-Response (2A)** variant | Objections are triggers; use the same hear->think->do pattern |
| Source systems, tools, or architecture components | **Jargon Decoder (2B)** variant | Three-column: System -> What It Does -> Your Angle |
| Use cases or solution patterns | **Decision Tree (2F)** or **Trigger-Response (2A)** | If mapping pain->solution: trigger-response. If mapping conditions->actions: decision tree. |

**Default card selection for common roles:**

| Role | Recommended Cards (in grid order) |
|---|---|
| SA (customer-facing technical) | Checklist (pre-demo gate), Architecture Patterns, Technical Limits, Competitive Counter A (EHR/incumbent), Competitive Counter B (BI tools), Security/Compliance, Metrics (with "→ When" triggers), Discovery Questions, Persona-to-Feature Routing |
| AE (customer-facing commercial) | Trigger-Response, Objection Handling, Discovery Questions, Personas, Metrics, Competitive Intel, Qualification Checklist, Use Cases, Key Dates |
| DBA/Engineer (hands-on-keyboard) | Commands/Syntax, Error Codes, Troubleshooting Tree, Architecture, Checklist (pre/post), Config Reference, Decision Tree, Metrics, Version Notes |
| CSM (relationship management) | Health Signals, Expansion Triggers, Personas, Renewal Checklist, Metrics, Discovery Questions, Escalation Tree, Key Dates, Account Context |

These are starting points. Always let the strategy contract override defaults.

### Step 4: Render

**Output format: HTML (single file)**

Generate a single self-contained HTML file with inline CSS. The HTML structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Sheet Title]</title>
  <style>
    /* Apply design-rules.md specifications here */
    /* Dark mode default unless strategy contract specifies light */
  </style>
</head>
<body>
  <div class="container">
    <h1>[Sheet Title]</h1>
    <div class="grid">
      <!-- Cards rendered here, following patterns.md templates -->
      <div class="card">
        <div class="card-title">[Icon] [Title]</div>
        <div class="card-body">
          <!-- Card content per template type -->
        </div>
      </div>
      <!-- ... repeat for each card ... -->
    </div>
    <footer>
      [Sheet Title] — v[X.Y] — [Owner] — Updated: [Date] — Next review: [Trigger]
    </footer>
  </div>
</body>
</html>
```

**Rendering rules:**
1. Single file. All CSS inline in `<style>`. No external dependencies.
2. Grid layout per design-rules.md (3-column default, responsive breakpoints included).
3. Each card uses the appropriate template from patterns.md.
4. Card placement follows F-pattern priority (highest-frequency -> top-left).
5. Colors from shared design-rules.md palette. Fall back to cheatsheet-design-rules.md defaults only if no shared palette exists.
6. Typography scale from cheatsheet-design-rules.md.
7. Footer with version, owner, date, and update trigger.
8. Total word count must stay within density targets (400-700 words, 1000 max).

### Step 5: Self-Evaluate

After rendering, run the philosophy rubric against your output. Score each of the 10 criteria (0-2). The sheet must score >=15/20 to ship.

**Evaluation block (internal — do not show to user unless asked):**

```
EVAL: Cheat Sheet Self-Assessment
---------------------------------
PRE-RENDER GATES (must be completed BEFORE rendering):
  MOMENT: [role] = [prep|apply|solve|remember] → Card 1 = [what]
  VIEWPORT BUDGET: [N] cards at [font size] = [fits|overflows]
  KILL LIST (≥3 items):
    - [cut item 1] — reason: [...]
    - [cut item 2] — reason: [...]
    - [cut item 3] — reason: [...]
  TRAINING AUDIT: [N] cards proposed → [N] passed (performance) / [N] cut (training)
  RED ALERT: [YES → banner text | NO → N/A]
---------------------------------
POST-RENDER RUBRIC:
 1. <5s Retrieval:       [0|1|2] — [note]
 2. Scent Quality:       [0|1|2] — [note]
 3. Extraneous Load:     [0|1|2] — [note]
 4. Chunking:            [0|1|2] — [note]
 5. Card Count:          [0|1|2] — [note]
 6. Actionability:       [0|1|2] — [note]
 7. Self-Containment:    [0|1|2] — [note]
 8. Visual Hierarchy:    [0|1|2] — [note]
 9. Color Semantics:     [0|1|2] — [note]
10. Audience Fit:        [0|1|2] — [note]
---------------------------------
TOTAL: [X]/20
VERDICT: [CLEAN — ship as-is | FIX REQUIRED — list fixes]
SINGLE-VIEWPORT CHECK: [PDF page count = 1 | FAIL → cut cards until 1 page]
---------------------------------
POST-RENDER INTEGRITY (binary pass/fail):
  OVERLAP AUDIT: [list any terms that appear in >1 card → merge or cut]
  SOURCE HYGIENE: [searched HTML for cite/KIQ/Confidence artifacts → CLEAN or list findings]
  PRINT CSS: [@media print block present with landscape + grid !important → YES/NO]
  ROW LABELS: [present and match role's moment hierarchy → YES/NO]
  PROVE TRIGGERS: [every metric has "→ When:" line → YES/NO]
  COMPETITIVE SPLIT: [competitors with different conversation triggers in separate cards → YES/NO or N/A]
```

If VERDICT is FIX REQUIRED:
1. List the specific fixes needed
2. Apply fixes
3. Re-evaluate
4. Repeat until CLEAN or user accepts

### Step 5.5: Board Write Protocol (Coordinated Mode)

**Only when `_meta.board_dir` is present.**

After completing self-evaluation (Step 5), write a board entry to `{board_dir}/board/cheatsheet-render-output.yaml`:

```yaml
skill_name: "cheatsheet-render"
invoked_at: "{ISO 8601 timestamp}"
invoked_by: "{coordinator name from _meta.coordinator}"

artifact_path: "{absolute path to final .html and .pdf}"
artifact_type: "cheatsheet"

# What the cheat sheet actually contains (for downstream skills to read)
hero_message_as_rendered: "{exact hero text from the cheat sheet}"
cards_rendered:
  - card_title: "{title}"
    card_type: "{trigger-response | jargon-decoder | persona | etc.}"
    row: N
    column: N
    key_terms: ["{term1}", "{term2}"]
proof_points_used:
  - point: "{proof point text}"
    card_title: "{which card}"
    treatment: "{hero metric | supporting evidence | When trigger}"
competitive_frame_as_rendered: "{how competitive positioning was handled}"
card_count: N
word_count: N

# Quality from Step 5 evaluation
quality_score: N                        # from rubric
quality_max: 20
quality_pass: true/false                # >= 15?
quality_notes: "{summary}"

# Amendments the cheat sheet discovered
strategy_contract_amendments:
  - field: "{e.g., content.card_topics}"
    current_value: "{what strategy said}"
    recommended_value: "{what actually worked}"
    reason: "{why}"
discovered_entities: []
coverage_gaps: []

recommendations_for_downstream:
  - target_skill: "one-pager-render"
    recommendation: "{e.g., 'one-pager should use the same competitive framing from cards X and Y'}"
    priority: "medium"
```

Use the Write tool to create this file. If the file already exists (retry scenario), overwrite it.

**If `_meta.board_dir` is absent** — skip board write entirely. Do not create any files.

### Step 6: Deliver

1. Save the HTML file to the output directory
2. **Always generate PDF alongside HTML** (Google Drive opens HTML as source code):
```bash
TMPDIR=$(mktemp -d) && \
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="${OUTPUT_DIR}/${FILENAME}.pdf" \
  --no-margins --print-background --user-data-dir="$TMPDIR" \
  "file://${OUTPUT_DIR}/${FILENAME}.html" 2>&1 | head -2 && \
rm -rf "$TMPDIR"
```
**Critical:** Use `--headless=new` with a temp `--user-data-dir` to avoid Chrome rendering cached pages from previous sessions. The `file://` prefix is required for local paths.
3. Symlink both HTML and PDF to Customer folder (if account-specific):
```bash
for sub in 01-Emails 02-Decks 03-Reference_Docs 04-Notebooks 05-Proposals 06-Meeting_Prep 07-Contracts_Legal 08-Screenshots; do
  mkdir -p ~/Customer/[account_folder]/$sub
done
ln -sf /absolute/path/to/${FILENAME}.html ~/Customer/[account_folder]/03-Reference_Docs/${FILENAME}.html
ln -sf /absolute/path/to/${FILENAME}.pdf ~/Customer/[account_folder]/03-Reference_Docs/${FILENAME}.pdf
```
4. Present to the user with a brief summary:
   - What the sheet covers
   - How many cards / which card types
   - Who it's designed for (role + moment)
   - Any trade-offs made (what was cut to stay within density limits)

**Do not** write a lengthy explanation of each card. The user can look at the sheet themselves.

---

## Examples

**Example invocation (explicit strategy):**
> "Create a cheat sheet for SAs covering Healthcare Revenue Cycle Management. I'll be using it during live customer calls. I'm new to healthcare."

Inferred contract:
```yaml
audience.role: SA
audience.experience_level: new_to_domain
context.domain: Healthcare RCM
context.moment: apply
context.usage: live_interaction
content.action_types: [talk_tracks, discovery_questions, jargon_decoder]
```

**Example invocation (raw content):**
> "Here are my notes from a customer meeting about their data platform migration. Can you turn this into a cheat sheet I can use for the next call?"

Action: Extract domain, key terms, personas, triggers, and action items from the notes. Infer the strategy contract. Render.

**Example invocation (minimal):**
> "Cheat sheet for Unity Catalog governance"

Action: Ask for role and usage context, or infer SA + apply as defaults. Render with jargon decoder, decision tree (when to use what), commands, and checklist card types.
