mean# Demo Factory Skill Upgrade — Prompt for Claude Code

## Task

Modify `/Users/samuel.selvan/.claude/skills/demo-factory/SKILL.md` to add an **AE Self-Service Demo Gate** — a new mandatory quality gate that ensures every demo produced by the factory includes the route structure, persona scripts, recovery playbook, and conversion mechanics needed for an AE to run the demo without an SA in the room.

**Do NOT rewrite the entire skill.** Add the new gate and supporting sections surgically. The existing phase orchestration (Phases 0–5), board protocols, blackboard integration, adapter schemas, and supervision tree remain unchanged unless explicitly noted below.

---

## Context

We audited three live demos (`clinical_agent`, `referral-route`, `hls-pulse`) against AE self-service readiness and found all three were PARTIAL. The common gaps:

1. No discoverable in-app guide from the default route (`/`)
2. Persona-specific scripts fragmented across docs instead of routed in-app
3. No deep-linkable URLs for persona runbooks or key guide sections
4. Recovery playbooks buried in markdown, not in the guide flow
5. No explicit conversion close (next-step CTA, follow-up copy) at end of demo

These learnings must be baked into the demo-factory skill so every future demo is born with self-service DNA.

---

## Resolved Design Decisions (from grill-me session — do not re-litigate)

| Decision | Resolution |
|----------|------------|
| Gate strictness | Block Phase 4 build on `PARTIAL` or `NOT READY` by default |
| Override mechanism | Allow via explicit phrase ("override self-service gate") OR `allow_partial_self_service: true` in `context.yaml` |
| Override controls | Require explicit risk acknowledgment + auto-generate `SELF_SERVICE_REMEDIATION.yaml` with P0/P1/P2 tasks |
| Persona coverage | Personas confirmed during brainstorm phase — vertical defaults used if user doesn't override (see Persona Hierarchy) |
| Persona exceptions | Allowed with structured evidence: excluded persona + why irrelevant + replacement mitigation |
| Route contract | Enforce semantic contract (Primer, Persona, Runbook, Objections, Recovery, Next Steps); path patterns may vary by framework |
| Discoverability | Hard requirement: visible "Guide" entry in primary nav/header from `/` |
| Canonical source | In-app guide is canonical; docs sync from it, not the other way around |
| Deep-linking | Hard requirement for persona pages and key guide sections |
| Script depth | 15-minute script required for `READY`; 5/15/30 variants required for `GOLD` |
| Recovery + conversion | Both mandatory for `READY` |
| Scoring thresholds | READY = 25–30, GOLD = 26–30 with no dim < 2 AND timed variants, PARTIAL = 17–24, NOT READY = ≤16 (max 30, 10 dimensions × 0–3) |

---

## What to Add to SKILL.md

### 1. New section: "Self-Service Gate" (between Narrative and Build)

Insert this as a new phase between Phase 3.5 (Demo Narrative) and Phase 4 (Build). It runs after narrative is complete (or after spec if narrative is skipped). The phase is identified as `self-service-gate` in the `phase_completed` enum — do NOT use "Phase 3.7" numbering anywhere in SKILL.md to avoid collision with the integer phase scheme.

**Purpose:** Audit the demo spec + narrative against the self-service rubric. Produce `SELF_SERVICE_AUDIT.md` and optionally `SELF_SERVICE_REMEDIATION.yaml`. Gate the build phase on the verdict.

**Trigger:** Automatic — runs as part of the pipeline after Phase 3.5 completes (or after Phase 3 if narrative is skipped).

**Inputs:**
- `DEMO_SPEC.md` (from Phase 3) — **required**
- `board/narrative-output.yaml` (from Phase 3.5) — **optional** (narrative may be skipped)
- `board/brainstorm-output.yaml` (for persona and audience context) — **required**

**Narrative-absent behavior:** When narrative was skipped, dimensions 4 (Script Usability) and 6 (Objection Handling) are capped at score 1 — the spec alone cannot demonstrate timed scripts or persona-specific objection counters. The gate logs `narrative_skipped: true` and the audit notes which dimensions were capped and why. This means skipping narrative almost guarantees a `PARTIAL` verdict, which is correct — a demo without narrative is inherently less AE-ready.

**Process:**

1. Score the demo plan against the 10-dimension rubric (see rubric below)
2. For each dimension, cite specific evidence from the spec/narrative or note the gap
3. Determine verdict: `READY`, `GOLD`, `PARTIAL`, or `NOT READY`
4. Write `SELF_SERVICE_AUDIT.md` to `.pipeline/demo-factory/artifacts/`
5. If verdict is `PARTIAL` or `NOT READY`, also write `SELF_SERVICE_REMEDIATION.yaml`
6. Write board entry to `board/self-service-gate-output.yaml`

**Gate logic:**
- If `READY` or `GOLD` → proceed to Phase 4
- If `PARTIAL` or `NOT READY` → **BLOCK** build. Present audit summary. User must either:
  - Address gaps and re-run gate, OR
  - Override with explicit phrase or context flag (triggers remediation backlog generation)

**Re-run semantics:**
- Each re-run creates a versioned audit: `SELF_SERVICE_AUDIT_v{N}.md` (v1, v2, v3...)
- The board entry tracks `attempt_number: N` and `previous_verdicts: ["NOT_READY", "PARTIAL"]`
- Only the latest audit is used for the gate decision — previous versions are kept for traceability
- `SELF_SERVICE_REMEDIATION.yaml` is regenerated on each re-run (not appended) — reflects current state
- context.yaml stores only the latest verdict/score, not history

**Override behavior:**
- When overridden, auto-generate `SELF_SERVICE_REMEDIATION.yaml` with prioritized tasks (P0/P1/P2)
- Log override to `context.yaml`: `self_service_override: true`, `self_service_override_reason: "{user's rationale}"`
- Remediation tasks are written to TWO destinations:
  1. `SELF_SERVICE_REMEDIATION.yaml` in `.pipeline/demo-factory/artifacts/` (machine-readable, used by the pipeline)
  2. `TODO-SELF-SERVICE.md` in the demo project root (human-readable checklist, survives pipeline archival)
- If the demo project has a GitHub repo, also create a GitHub issue with label `self-service-gap` containing the P0 tasks (use `gh issue create` if available)
- Phase 5 (archive) must check: if override was applied, copy `TODO-SELF-SERVICE.md` to the archive AND log a warning in the archive summary

### 2. Rubric (embed in the skill as a reference table)

```
AE SELF-SERVICE READINESS RUBRIC
=================================
Score each 0–3. Max 30.

 #  Dimension                    0 (missing)              1 (partial)                    2 (solid)                         3 (best-in-class)
 1  Guide Discoverability        No guide route           Guide exists but hidden        Visible link from /               One-click from every entry point
 2  Primer Quality               No primer                Partial (missing why/who)       Complete what/why/who/value        Primer + 60s video script
 3  Persona Coverage             0–1 personas             2 personas                     3 personas                        4 personas with justified exceptions
 4  Script Usability             No scripts               Scripts exist, no timing       15-min timed script               5/15/30 variants with say/show/why
 5  Recovery Robustness          No recovery              Recovery in docs only          In-app recovery per critical step  Tested fallback paths with timing
 6  Objection Handling           None                     Generic objections             Persona-specific objections        Objections + escalation triggers
 7  Route Deep-Linkability       No defined routes        Routes exist, no deep links    Deep links for personas            Deep links for all guide sections
 8  Single Source of Truth       Fragmented docs          Docs + app, unclear canonical  In-app canonical, docs drift ok    In-app canonical, docs auto-synced
 9  AE Setup Simplicity          Requires SA/admin setup  Technical setup documented     One-click preflight check          Zero-setup (always-on environment)
10  Conversion Close             No close                 Generic "contact us"           Explicit next-ask per persona      Next-ask + follow-up copy + handoff template

VERDICT THRESHOLDS:
  GOLD:      26–30, no dimension below 2, all timed variants (5/15/30) present
  READY:     25–30, no critical dimension below 2
  PARTIAL:   17–24, OR any critical dimension below 2
  NOT READY: ≤16

CRITICAL DIMENSIONS (must score ≥2 for READY):
  1 (Guide Discoverability), 2 (Primer Quality), 3 (Persona Coverage),
  5 (Recovery Robustness), 10 (Conversion Close)
```

### 3. Route semantic contract (embed as a reference)

Add a section called "Self-Service Route Contract" that specifies the semantic sections every demo guide must include. Not exact URL paths — semantic equivalents are fine.

```
SELF-SERVICE ROUTE CONTRACT (Semantic)
=======================================
Every demo must include routable, deep-linkable equivalents of:

  SECTION              PURPOSE                                         CRITICAL?
  Primer               What is this demo, why now, who it's for        Yes
  Persona Picker       Select audience → get tailored script           Yes
  Persona Runbook      Say/show/why blocks per persona (15 min min)    Yes
  Objections           Persona-specific objections + counters          No
  Recovery             If step X fails, do Y in <30 seconds            Yes
  Next Steps / Close   Explicit ask + follow-up copy + handoff         Yes

DISCOVERABILITY RULE:
  The default app route (/) MUST include a visible, labeled link to the guide.
  Hidden URLs (/guide only known via README) fail dimension 1.

CANONICAL SOURCE RULE:
  In-app guide content is the source of truth.
  External docs (README, DEMO_RUNBOOK.md) should reference the guide URL, not duplicate content.

DEEP-LINK RULE:
  Each section above must have a stable, shareable URL.
  useState-only navigation (no URL change) fails dimension 7.
```

### 4. Persona Hierarchy + Brainstorm Integration

**Add a new reference section "Persona Hierarchy" to SKILL.md:**

```
PERSONA HIERARCHY
==================
Personas are NOT hardcoded. They are selected during brainstorm (Phase 1) based on
the demo's vertical and use case. The hierarchy provides defaults — the user confirms
or overrides during brainstorm.

VERTICAL DEFAULTS:
  Platform / Lakebase:
    - IT Leader
    - DBA
    - App Developer
    - Clinical Ops (only if HLS context)

  HLS (Healthcare & Life Sciences):
    - Clinical Executive (CMO/CMIO/CNO)
    - Technical Gatekeeper (IT/Security/Compliance)
    - Clinical Ops (Care Managers, Quality, Population Health)
    - Data & Analytics Lead (CDO, Analytics Director)

  FinServ:
    - Risk & Compliance Officer
    - Data Engineering Lead
    - Business Analyst / Quant
    - IT / Platform Owner

  Retail / CPG:
    - VP Merchandising / Supply Chain
    - Data Engineering Lead
    - Marketing Analytics Lead
    - IT / Platform Owner

  Cross-Industry / Generic:
    - Executive Sponsor (budget holder)
    - Technical Evaluator (architect / platform)
    - Line-of-Business User (daily operator)
    - Data Team Lead (engineering / analytics)

RESOLUTION ORDER:
  1. If context.yaml has `personas: [...]` → use those (user explicitly set them)
  2. If context.yaml has `vertical: "..."` → load vertical defaults, present to user
     during brainstorm for confirmation/override
  3. If neither → ask during brainstorm: "Which vertical is this demo for?" then
     present the matching defaults

MINIMUM COVERAGE:
  - 3 personas required for READY (dimension 3 score ≥ 2)
  - 4 personas required for GOLD (dimension 3 score = 3)
  - Fewer than 3 → PARTIAL at best, regardless of other scores
```

**Update brainstorm phase (Phase 1) to include persona selection:**

Add to the brainstorm phase's question set (the existing Socratic questions):

```
BRAINSTORM PERSONA SELECTION (add after existing audience/vertical questions):
  1. Detect vertical from user's description or context.yaml
  2. Present the matching default persona set from the hierarchy
  3. Ask: "These are the default personas for [vertical] demos.
     Confirm, swap, or add personas for this demo."
  4. Write confirmed personas to context.yaml: `personas: [...]`
  5. Write to board/brainstorm-output.yaml: `confirmed_personas: [...]`

If user says "just the defaults" → accept without further questions.
If user modifies → record the delta and reasoning in brainstorm output.
```

**Persona runbook contract (applies to whichever personas are selected):**

```
PERSONA RUNBOOK CONTRACT
=========================
Personas are confirmed during brainstorm — see Persona Hierarchy for defaults.
The self-service gate scores against the CONFIRMED persona list, not a hardcoded set.

Each persona page must include:
  - "What this persona cares about" (2-3 bullets)
  - 3 discovery questions to ask before showing features
  - 3 proof points relevant to this persona
  - 3 likely objections + approved counters
  - Persona-specific close line (the explicit ask)
  - Recovery: if the critical wow moment for this persona fails, what to do

EXCEPTION POLICY:
  If a demo excludes a persona from the vertical defaults, the audit must include:
    excluded_persona: "{name}"
    reason: "{why this persona is irrelevant to this demo's use case}"
    mitigation: "{how the demo still covers the audience gap}"
  Exceptions are valid only if recorded during brainstorm — not invented at gate time.
```

### 5. Anti-patterns section (append to existing anti-patterns)

Add these to the existing anti-patterns table:

```
| Don't | Do Instead |
|-------|-----------|
| Hide guide URL behind README-only discovery | Make guide visible from app default route |
| Put persona scripts only in markdown docs | Route persona scripts in-app with deep links |
| Use useState-only navigation for guide sections | Use URL params or subroutes for deep-linkability |
| Skip recovery playbook ("demo never fails") | Include tested fallback per critical wow moment |
| End demo without explicit next-step ask | Close every persona flow with conversion CTA |
| Duplicate guide content in README and in-app | In-app is canonical; docs link to it |
| Require SA-level setup for AE baseline flow | Preflight check should be one click, not terminal commands |
```

### 6. Board entry schema for the new gate

```yaml
# board/self-service-gate-output.yaml
skill_name: "self-service-gate"
phase: "self-service-gate"
invoked_at: "{ISO timestamp}"
invoked_by: "demo-factory"

artifact_paths:
  audit: ".pipeline/demo-factory/artifacts/SELF_SERVICE_AUDIT_v{N}.md"
  remediation: ".pipeline/demo-factory/artifacts/SELF_SERVICE_REMEDIATION.yaml"  # only if PARTIAL/NOT READY
  todo: "{project_root}/TODO-SELF-SERVICE.md"  # only if override applied

# Re-run tracking
attempt_number: 1
previous_verdicts: []  # e.g. ["NOT_READY", "PARTIAL"] on attempt 3

# Persona context
confirmed_personas: []  # from brainstorm, e.g. ["IT Leader", "DBA", "App Developer", "Clinical Ops"]
vertical: ""  # e.g. "Platform / Lakebase", "HLS"
narrative_skipped: false  # if true, dims 4 and 6 are capped at 1

rubric_scores:
  guide_discoverability: N
  primer_quality: N
  persona_coverage: N
  script_usability: N
  recovery_robustness: N
  objection_handling: N
  route_deep_linkability: N
  single_source_of_truth: N
  ae_setup_simplicity: N
  conversion_close: N

total_score: N
max_score: 30
verdict: "{GOLD|READY|PARTIAL|NOT_READY}"
critical_failures: []  # dimensions 1,2,3,5,10 that scored below 2
persona_exceptions: []  # structured evidence for excluded personas

override_applied: false
override_reason: ""

quality_pass: true/false
quality_notes: ""
```

### 7. SELF_SERVICE_AUDIT.md template

```markdown
# AE Self-Service Readiness Audit

## Demo: {name}
## Date: {date}
## Verdict: {GOLD|READY|PARTIAL|NOT_READY}
## Score: {N}/30

## Rubric Scores

| # | Dimension | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Guide Discoverability | N | {specific evidence or gap} |
| 2 | Primer Quality | N | {evidence} |
| 3 | Persona Coverage | N | {evidence} |
| 4 | Script Usability | N | {evidence} |
| 5 | Recovery Robustness | N | {evidence} |
| 6 | Objection Handling | N | {evidence} |
| 7 | Route Deep-Linkability | N | {evidence} |
| 8 | Single Source of Truth | N | {evidence} |
| 9 | AE Setup Simplicity | N | {evidence} |
| 10 | Conversion Close | N | {evidence} |

## Critical Dimension Analysis

{For each critical dimension (1, 2, 3, 5, 10), detailed assessment}

## Persona Coverage Detail

{For each of the 4 personas: covered/excluded + evidence}
{If excluded: structured exception with reason + mitigation}

## Recommendations

{Prioritized list of improvements needed to reach READY/GOLD}
```

### 8. SELF_SERVICE_REMEDIATION.yaml template

```yaml
demo_name: "{name}"
current_verdict: "{PARTIAL|NOT_READY}"
target_verdict: "READY"
generated_at: "{ISO timestamp}"

tasks:
  - id: "ss-001"
    priority: "P0"
    dimension: "guide_discoverability"
    current_score: N
    target_score: 2
    gap: "{specific evidence string from the audit — what's missing or broken}"
    task: "{specific action to take}"
    effort_estimate: "{hours}"

  - id: "ss-002"
    priority: "P0"
    dimension: "persona_coverage"
    current_score: N
    target_score: 2
    gap: "{evidence from audit}"
    task: "{specific action}"
    effort_estimate: "{hours}"

  # ... more tasks ordered by priority
```

### 9. Update context.yaml schema

Add these fields to the context.yaml schema definition:

```yaml
# After existing fields like spec_prp_status
vertical: ""                      # Platform / Lakebase, HLS, FinServ, Retail / CPG, Cross-Industry
personas: []                      # confirmed during brainstorm, e.g. ["IT Leader", "DBA", "App Developer"]
self_service_verdict: null         # GOLD|READY|PARTIAL|NOT_READY
self_service_score: null           # 0-30
self_service_override: false
self_service_override_reason: ""
```

### 10. Update phase_completed enum

Update the `phase_completed` comment to include the new phase:

```yaml
phase_completed: null  # null → brainstorm → research → spec → narrative → self-service-gate → build-infra → build-app → verification → complete
```

### 11. Update mandatory stop after Phase 3.5

The existing mandatory stop after Phase 3.5 (narrative) should be updated to mention the self-service gate:

```
Next: Self-Service Gate
  This runs automatically to verify the demo plan includes
  self-service route structure, persona scripts, recovery playbook,
  and conversion mechanics for AE-led delivery.
  Personas scored against: {confirmed_personas from brainstorm}
```

### 12. Update Phase 4 entry verification

Phase 4's entry check currently verifies `phase_completed == "spec"` or `"narrative"`. **Replace** this with mandatory self-service-gate verification — the gate is NOT optional:

```
1. Read context.yaml → verify phase_completed is "self-service-gate"
   - If phase_completed is "spec" or "narrative" → BLOCK: "Self-service gate has not been run. Run it first."
     (This closes the loophole where skipping the gate entirely would allow build to proceed.)
2. If self_service_verdict is PARTIAL or NOT_READY:
   - Check self_service_override == true
   - If not overridden → BLOCK: "Self-service gate not passed. Override or fix gaps first."
3. If self_service_verdict is READY or GOLD → proceed
```

### 13. Update supervision tree

Add a row for the new gate:

```
| self-service-gate | Rubric score ≥ 25, no critical < 2 | 1 retry after spec/narrative update | Accept PARTIAL with remediation backlog | BLOCK on NOT_READY without override |
```

### 14. Update routing logic summary table

Add a row:

```
| Post-narrative: self-service ready? | N/A (no self-service gate) | Score rubric, block if PARTIAL/NOT_READY unless overridden |
```

---

## What NOT to Change

- Phases 0–2 (research, spec core logic) — unchanged
- Phase 1 (brainstorm) — add persona selection questions only, do not change existing Socratic flow
- Phase 3.5 (narrative) — unchanged except mandatory stop message
- Phase 4 build steps (4a–4e) — unchanged except entry verification
- Phase 4.5 verification gates — unchanged
- Phase 5 archive — unchanged
- Blackboard integration — unchanged
- All adapter schemas — unchanged
- All existing anti-patterns — keep, only append new ones

---

## Validation

After modifying SKILL.md, verify:

1. The new self-service-gate section is placed between Phase 3.5 and Phase 4 (no "3.7" numbering anywhere)
2. The rubric table renders correctly in markdown
3. The persona hierarchy, route contract, persona contract, and anti-patterns are in their own subsections
4. The board entry schema includes attempt_number, previous_verdicts, confirmed_personas, vertical, narrative_skipped
5. context.yaml schema updates are reflected in the Phase 0 section (including `personas: []` and `vertical: ""`)
6. Phase 1 (brainstorm) includes persona selection questions using the vertical hierarchy
7. Phase 4 entry verification REQUIRES `phase_completed == "self-service-gate"` — no fallback to "spec"/"narrative"
8. The supervision tree has the new row
9. The routing logic summary has the new row
10. The mandatory stop message after Phase 3.5 mentions the self-service gate
11. No existing content was accidentally deleted or reordered
12. Remediation destination is specified (YAML in pipeline + TODO.md in project root + optional GH issue)
