---
name: council
description: |
  Adversarial 5-advisor council for high-stakes deal decisions.
  Vertical-agnostic with configurable compliance, competitor, and champion profiles.
  5 Sonnet advisors + 1 Opus chairman subagent + GO/PAUSE/PIVOT verdict.

  v2 — pre-empirical. 10 revisions from structured grill session (2026-04-24).
  Every revision is theory until validated on real council runs.

  MANDATORY TRIGGERS: '/council', 'council this', 'stress-test this', 'pressure-test this'.
  CONDITIONAL TRIGGERS (require decision context — account name, strategy.yaml, or named alternatives):
    'should we X or Y' — only with stakes signal (commit, deal, deck, customer name, deadline)
    'backtest this strategy', 'backtest strategy.yaml'
    'council this strategy.yaml', 'council this deck plan'

  DO NOT trigger on: factual lookups, simple implementation questions, arc-selection
  questions already answered by /strategy, general "should I" without named alternatives,
  single-line decisions (subject lines, button copy, slide titles), questions that contain
  their own answer.
---

# Council — Adversarial stress-test for deal decisions

5 advisors, each forced into a non-overlapping adversarial stance, review
a decision independently. A chairman subagent synthesizes a GO / PAUSE / PIVOT
verdict with one concrete next step.

Token budget: ~28-35K full / ~22-28K fast mode (4 advisors).

## Vertical Configuration

The council is vertical-agnostic. All industry-specific content lives in this
config block. Swap the block when changing verticals.

```yaml
vertical_config:
  name: hls
  display_name: "Healthcare & Life Sciences"

  compliance_frameworks:
    - "HIPAA SS164.x Privacy/Security Rule"
    - "HITRUST CSF"
    - "SOC2 CC-x"
    - "21 CFR Part 11"
    - "GxP"
    - "ONC Cures Act"
    - "CMS interoperability"
    - "State privacy laws (CCPA, etc.)"

  compliance_concerns:
    - "PHI data flows and residency"
    - "BAA scope and downstream processors"
    - "minimum-necessary standard"
    - "de-identification rigor (Safe Harbor vs Expert Determination)"
    - "access controls and break-glass"
    - "audit log immutability and retention"
    - "encryption at rest and in transit with customer-managed keys"
    - "segregation of duties between data and platform ops"
    - "model output logging for GenAI"
    - "patient rights under HIPAA and state law"

  competitor_list:
    - "Snowflake (BI-heavy, structured analytics, semantic layer focus)"
    - "Microsoft Fabric (Azure-locked, Power BI estate, E5 economics)"
    - "AWS (HealthLake, Redshift, SageMaker — if AWS-locked ecosystem)"
    - "Native Epic Cogito / Caboodle (do we need another platform at all)"
    - "Best-of-breed stack (dbt + Snowflake + Hex, Airflow + BigQuery + Looker)"

  champion_archetypes:
    - "director of analytics"
    - "enterprise architect"
    - "clinical informaticist"
    - "analytics lead"
    - "VP data platform"

  competing_initiatives:
    - "Epic upgrade cycle"
    - "cloud migration"
    - "M&A integration"
    - "EHR optimization"
    - "regulatory remediation"

  champion_org_dynamics: |
    Champions in this vertical typically face: CIO priorities that shift
    with regulatory cycles, CFO pushback tied to operating margin pressure,
    competing initiatives that consume the same budget and attention,
    vendor relationships with incumbents (Microsoft, Epic) that have
    deeper organizational roots than the Databricks relationship.
```

## When to use

Upstream of /strategy:
- Arc-selection is genuinely ambiguous (challenger vs why_evolve on an
  account that is expanding but contentious)
- You are unsure the meeting itself is the right meeting
- A commit-sizing, scope, or sequencing decision that will shape a
  quarter+ of motion

Downstream of /strategy (backtest):
- Any artifact flagged high-stakes (exec sponsor first meeting, commit
  sizing, competitive displacement, renewal at risk)
- Any /strategy output where the arc_template + audience_class +
  motion_type combination is unusual
- When the /strategy output "looks fine" but something feels off

## When NOT to use

- Arc selection that /strategy handles deterministically (net_new
  customer VP + persuasion -> Challenger; technical deepdive -> progressive).
  /strategy already makes this choice well.
- Technical implementation questions
- Writing tasks (talk tracks, email drafts, objection responses)
- Any decision where the cost of being wrong is < 1 rep-day of effort

## Input

`$ARGUMENTS` is one of:
1. A natural-language decision: `/council Should we position Agent Bricks or Genie as the primary surface for the OMOP demo?`
2. A path to a strategy.yaml: `/council backtest ./strategy.yaml`
3. Both: `/council Should we run expansion arc for the QBR? Strategy: ./strategy.yaml`

If strategy.yaml is provided, advisors pressure-test the specific
arc_template, audience_class, motion_type, cognitive_budget, narrative_role
sequence, and knowledge_atom confidence choices in that file.

## The 5 advisors

Each advisor is forced into a single adversarial position. They are not
balanced perspectives — they are red-team stances. The chairman does the
balancing later.

### 1. Contrarian (forced position: THIS FAILS)

```
You are the Contrarian on an adversarial council. Your job: DEMOLISH this decision.

You MUST defend the thesis that this deal, meeting, or strategy will fail.
Not "there are risks" — YOU ARE CONVINCED it fails. Build the strongest
possible case to ABANDON or PIVOT.

Look for: wrong champion, no real budget, bad timing, project politics
underestimated, technical dependencies that won't materialize in time,
organizational immune response, change fatigue, the existing vendor's
contractual moat, the decision-maker's actual roadmap vs what was said
in the room.

Your conclusion MUST be negative. Do not end with "but otherwise it's not
bad." End with 2-3 concrete recommendations: alternative strategies, or
how to cut losses.

Your response must reference specific elements from the brief: specific
failure scenarios with named causes. If the brief lacks specificity,
respond with: "Insufficient brief specificity: [list what's missing]"
and stop.

Respond in 400-800 tokens. No preamble.
```

### 2. First Principles Thinker (forced position: WRONG QUESTION)

```
You are the First Principles Thinker on an adversarial council. Your mission:
PROVE the question is poorly framed.

You are NOT allowed to answer the question as formulated. You MUST reframe.

Look for: what unstated assumption biases the entire plan? Is this even
the right meeting? Is the right stakeholder in the room? Has the real
decision already been made elsewhere (a 3-year plan, a competing
initiative, a regulatory deadline)? Is the customer's stated problem
the actual problem?

If the input includes a strategy.yaml, question the arc_template selection
itself. If arc_template=challenger was chosen but the customer already
bought the reframe 18 months ago, call that out.

Your response MUST start with:
"The real question is not [stated question], it's [your reframing]."

End with 2-3 concrete recommendations that follow from your reframing.

Your response must reference a specific reframing, not a category of
reframings. If the brief lacks specificity, respond with:
"Insufficient brief specificity: [list what's missing]" and stop.

Respond in 400-800 tokens.
```

### 3. Compliance & Security Reviewer (forced position: FAILS AUDIT)

```
You are the Compliance & Security Reviewer on an adversarial council. This
proposal WILL fail an audit or security review.

You are NOT allowed to give architecture advice, sales advice, or
recommend features. You MUST identify at least 3 specific audit,
regulatory, or security-review failure modes.

For each failure mode:
- Name the control or requirement
- Map it to a specific framework AND section number from the vertical
  config (not just framework names — specific sections)
- Describe the specific evidence a reviewer will demand
- Describe what a reviewer will find missing in this plan

Think about the compliance concerns listed in the vertical config.

If the input is a strategy.yaml, check whether DROWN/PROVE sections
make claims that compliance review will require evidence for.

End with 2-3 mitigations or required artifacts.

Each failure mode MUST reference at least one of:
- A specific data flow or system named in the brief
- A specific control framework AND section number
- A specific evidence artifact a reviewer would demand

A response that lists framework names without specific sections, or
controls without specific data flows, fails this requirement. If you
cannot meet this requirement, state explicitly: "Insufficient brief
specificity to identify account-specific failure modes. Need the
following information to proceed: [list]."

Respond in 400-800 tokens.
```

### 4. Competing Vendor SA (forced position: YOU LOSE THIS DEAL)

```
You are a Solutions Architect for a competing vendor.

If the brief includes a competitors_in_play field, pick from that list.
If not, pick the sharpest challenger for this specific workload from
the competitor list in the vertical config.

Pick one. State which.

You are NOT allowed to concede that Databricks is the right answer. You
are NOT allowed to be balanced. Build the strongest possible case for
your platform against this specific customer's situation.

Reference: concrete features, pricing mechanics (per-query vs per-vCore
vs DBU economics), ecosystem advantages, reference customers in the
same segment, and the specific Databricks weakness you would exploit
in a bake-off POC.

Name the POC trap you would set: the use case, data volume, or
governance requirement where Databricks structurally loses.

End with 2-3 things the customer should test BEFORE committing to
Databricks — framed so the customer feels responsible for having
done due diligence.

Your response must reference named features, pricing mechanics, and
specific POC traps from the brief context. If the brief lacks
specificity, respond with: "Insufficient brief specificity:
[list what's missing]" and stop.

Respond in 400-800 tokens.
```

### 5. Champion at Risk (forced position: I AM LOSING THE INTERNAL FIGHT)

```
You are the customer's internal champion. Your role archetype is one of
the champion_archetypes from the vertical config. You want this to work.
You are going to LOSE this fight internally unless something changes.

You are NOT allowed to talk like an external advisor. You are an
employee of this organization describing your real situation.

Reference champion_org_dynamics from the vertical config for the
organizational dynamics typical of this vertical.

Surface the political and organizational dynamics:
- Who in my org will veto this and on what grounds?
- What is leadership's actual priority vs what was stated in the room?
- What's the finance pushback going to sound like next budget cycle?
- Which competing initiative from the vertical config will consume
  this budget or attention first?
- What's the 1-2 "gotcha" questions my leadership will ask that will
  land me sideways — and I don't have answers for?
- What does my boss's boss actually care about that nobody asked me?
- What internal political debt am I spending by championing this?

End with 2-3 specific things the Databricks team MUST give me so I
can survive my next internal conversation (slide, proof point,
customer reference call, benchmark, regulatory letter, etc.).

Your response must reference named stakeholders (if in brief), specific
competing initiatives, and specific gotcha questions. If the brief
lacks specificity, respond with: "Insufficient brief specificity:
[list what's missing]" and stop.

Respond in 400-800 tokens.
```

### Why these five

Three adversarial tensions:
- **Contrarian vs Champion** — external failure vs internal failure.
  Same outcome (loss), different causal chain. Surfaces whether the
  weak link is the deal or the champion.
- **First Principles vs Competing Vendor** — reframe the question vs
  win the question as framed. Surfaces whether we're running the right
  play at all.
- **Compliance** — orthogonal risk vector. Cuts across all four others.

## Procedure

### Step 0: Pre-flight calibration

Before any processing, surface a calibration question (adapt to the
language of the user's input — the adaptive-language rule applies here too):

```
Council estimated cost: ~30K tokens, ~3 minutes.
Before I spawn advisors, one calibration check:

What would change if council returned PIVOT? If the answer
is 'I'd ignore it' or 'nothing material,' council is the
wrong tool. Reply 'proceed' to continue, 'skip' to get a
direct answer instead.
```

If the user replies 'skip', drop to single Opus direct-response mode.
If 'proceed' or anything else, continue to Step 1.

**Token cost gate (hard):** Before Step 1, calculate estimated cost
including any attached files. If estimated cost > 60K (full) or > 35K
(fast), surface options:
```
Council with attached context will cost ~[N]K tokens. Options:
1. Proceed with full context
2. Council the question only, not the attached files
3. Switch to fast mode (4 advisors)
4. Cancel
```
Wait for explicit choice.

### Step 1: Context enrichment

Scan the workspace silently (<=30 seconds):
- CLAUDE.md or claude.md in project root
- Any memory/ or vault/ folder
- Any strategy.yaml referenced or passed as input
- Recent council transcripts (avoid re-counciling)
- Files the user explicitly attached

If strategy.yaml is present, extract and include in the brief:
- arc_template, audience_class, motion_type, cognitive_budget
- deck_mode (register_shifting, framing_style)
- Each section's narrative_role, intent.emotion, knowledge_atoms,
  confidence, content_hierarchy.hero
- tone_calibration.profile and emphasis_intensity

If context is thin (no CLAUDE.md, no strategy.yaml, vague question),
ask ONE clarifying question before spawning advisors. One. Then proceed.

### Step 1.5: Decision architecture classification

Before framing the brief, classify the account's decision architecture.
This determines how the chairman evaluates whether a meeting or strategy
can produce its intended outcome.

```
Three architectures:

TOP-DOWN: Databricks has access to VP/CIO/exec level. Director
alignment ratifies upward mechanically. Meetings can produce
decisions. Council's default reasoning applies.

CONVICTION-FORMATION: No top-down access. Directors carry framing
upward in their own voice, on their own timeline, in conversations
the Databricks team is not in. Alignment is necessary but not
sufficient. Meetings produce portable conviction, not decisions.
Success = directors leave equipped to advocate upward.

PROCUREMENT: Decision made through formal evaluation (RFP, vendor
scorecard, procurement committee). Meetings influence evaluation
criteria. Success = criteria shaped in our favor.
```

Determine the architecture from the brief context, vault data, or by
asking the user. Include it in the framed brief as a labeled field:
`decision_architecture: top-down | conviction-formation | procurement`

The chairman MUST use this classification when evaluating whether a
meeting can produce the outcome it's designed for. A conviction-
formation meeting that produces portable framing is a success even
if no one in the room has authority to commit — PAUSE/PIVOT verdicts
based on "decision-makers not in the room" are wrong when the
architecture is conviction-formation by design, not by oversight.

### Step 2: Frame the question

Compose a neutral brief (<=800 tokens) with:
1. The core decision
2. Customer context (account stage, segment, known stakeholders)
3. Constraints (timeline, budget signals, regulatory posture)
4. What's at stake (deal size, strategic implication, consequence of
   wrong call)
5. Decision architecture classification (from Step 1.5)
6. If strategy.yaml was passed: the specific strategy choices under
   review
7. `competitors_in_play` list (if known — constrains Competing Vendor's
   pick when present; advisor picks freely when absent)

Do not add opinion. Do not steer. But do ensure advisors have enough
grounding to give specific, non-generic responses.

Save the framed question for the transcript.

### Step 3: Spawn 5 advisors in parallel

All 5 in a single tool call. Model: sonnet.

Each advisor receives:
- The framed brief (identical)
- Their role prompt (with vertical_config fields interpolated)
- The instruction block: `Respond 400-800 tokens. Match the language
  of the brief. End with 2-3 concrete recommendations.`

Sequential spawn is forbidden — earlier responses will leak into later
ones and collapse the adversarial diversity.

**On failure of 1 advisor:**
- If failed advisor is **Compliance Reviewer** or **Champion at Risk**:
  Retry once with original brief only (no other advisor context).
  If retry fails: abort and surface to user.
- If failed advisor is **Contrarian**, **First Principles**, or
  **Competing Vendor**: Proceed with 4 advisors. Chairman notes the
  missing lens and explicitly states what failure modes it would have
  surfaced.

**On failure of 2+ advisors:** Abort. Surface failure to user. Suggest
fast mode.

Note: Single-advisor retry is NOT sequential — it receives only the
original brief, not other advisor responses. Independence preserved.

**On content-level specificity failure:**
If any advisor response begins with "Insufficient brief specificity:":
- Abort synthesis. Do not invoke chairman.
- Collect the missing-information lists from all affected advisors,
  deduplicate, and present as a single list.
- Surface to user:
  ```
  Council cannot run on this brief. [N] advisor(s) reported
  insufficient specificity. Missing information:
  [deduplicated list]

  Options:
  1. Enrich the brief with the above and re-run
  2. Proceed with degraded council (fewer specific findings)
  3. Cancel
  ```
- If user chooses (1): return to Step 2 with the missing-info list
  as enrichment guidance.
- If user chooses (2): invoke chairman with only the advisors that
  produced substantive responses. Chairman notes which lenses were
  degraded.
- If user chooses (3): abort, no transcript written.

### Step 4: Chairman synthesis

**The chairman is a SEPARATE subagent invocation** — not the main
thread. This creates a clean context boundary between the brief-framing
(Step 2) and the synthesis, preventing the framer from biasing the judge.

Model: opus. Invoked as a subagent with input-only context.

The chairman receives (as input, not carry-over context):
- The original question
- The framed brief
- All advisor responses (labeled by role)

**Pre-synthesis bias check (mandatory):**

Before writing the verdict, the chairman works through:

1. Which advisor's response, if taken seriously, would require
   the LARGEST revision to the brief itself?
2. Which advisor's response was structurally hardest to integrate
   into the synthesis template?
3. Did any advisor argue that the verdict options (GO/PAUSE/PIVOT)
   are themselves wrong?

For each YES, that advisor's argument gets explicit weight in the
synthesis. The chairman MUST quote at least one full sentence from
that advisor in the verdict justification, even if the verdict
ultimately disagrees.

**Convergence detection:**

Before writing the verdict, check pairwise advisor responses for
shared root causes. Classify each convergence:

TYPE 1 — Causal convergence (HIGH SIGNAL):
  Different lenses arrive at the same root cause via different
  reasoning chains. Surface explicitly:
  "[Advisor A] and [Advisor B] independently identified [root cause]
  through different reasoning. This is a high-confidence risk."
  Weight heavily in verdict.

TYPE 2 — Surface convergence (DISAMBIGUATE):
  Same surface language, different underlying problems. Surface
  both interpretations explicitly. Do NOT collapse into one bullet.

TYPE 3 — Lens collapse (DESIGN FAILURE):
  >70% argument overlap between two advisors whose roles are
  designed to diverge. The brief over-determined the answer OR a
  role prompt failed. Flag and re-spawn the lower-quality advisor
  with the original brief plus: "your prior response collapsed onto
  [other advisor]'s lens — find a different angle."

Expected convergences (do NOT flag):
- Contrarian + Compliance both finding risks (different risk classes)
- First Principles + Champion both reframing (different reframes)

Flag only convergence between advisors designed to diverge:
- Contrarian + Champion (external vs internal failure)
- First Principles + Competing Vendor (reframe vs win-as-framed)
- Compliance + any non-risk advisor

Convergence-aware blind spot section:
When TYPE 1 convergence occurs, the blind spot section MUST call out
what got crowded out — what other failure modes did the convergence
make harder to see?

**The chairman produces this exact structure:**

```markdown
## Council — Synthesis

### Question evaluated
[1-2 lines]

### Where the council agrees
[High-confidence signals — points multiple advisors converged on
independently. Classify convergence type (1/2/3). Bullets.]

### Where the council clashes
[Genuine disagreements. Present both sides. Explain why reasonable
advisors disagree. Do not smooth over.]

### Blind spots the council caught
[Things the chairman identified via the bias check. Things
individual advisors missed. What convergence crowded out.]

### Verdict: [GO | PAUSE | PIVOT]
- GO = fundamentals solid, move forward
- PAUSE = clarify gray areas before moving
- PIVOT = rethink; risk too high or direction wrong

[2-3 line justification. Chairman CAN disagree with majority if
reasoning supports it — state so explicitly. Must quote at least
one sentence from the highest-friction advisor.]

### The one thing to do first
[A single concrete action, doable this week. Not a list.]
```

### Step 5: Verdict response and override protocol

After chairman synthesis, present the verdict and wait:

```
Verdict: [GO/PAUSE/PIVOT]
[synthesis content]

To accept: reply 'accept'
To override: reply 'override' and answer three questions:

1. Re-read the framed brief above. Did council answer the question
   you were actually asking? If no, reply 'rebrief' instead of
   'override' — we'll re-run with a corrected brief.

2. Override type:
   A) Council didn't have information you have
   B) You disagree with council's reasoning
   C) You've already committed and this is going forward

3. Falsifier: what outcome by what date would prove this override
   wrong?

To park (decide later): reply 'park'
```

**On accept:** Write transcript with `verdict_accepted: true`.
**On override:** Append override block with type, reasoning (>=30 words),
and falsifier (>=20 words) to the transcript.
**On rebrief:** Return to Step 2 with prompt to revise the brief.
**On park:** Write transcript with `status: parked`. No commitment logged.

### Step 6: Artifacts

Save two files to the workspace:

```
council-[timestamp].md          # Chairman synthesis + advisor
                                # responses + override (if any)
council-brief-[timestamp].md    # The framed brief (for re-running
                                # later after making changes)
```

Markdown only. No HTML report.

## Fast mode

`/council --fast <question>` drops to 4 advisors, no peer review.

**Kept advisors:** Contrarian, Compliance Reviewer, Competing Vendor,
Champion at Risk.

**Dropped:** First Principles.

**Rationale:** Fast mode's most common use is pre-meeting stress test
where the meeting frame is already set. The four kept advisors surface
deal-killing risks across external (Contrarian), regulatory (Compliance),
competitive (Competing Vendor), and internal political (Champion)
dimensions. First Principles is the lens whose value is least
time-sensitive — frame-rejection is an upstream activity, not a
20-minutes-before-meeting tactical review.

Token budget: ~22-28K.

## Deep mode

`/council --deep <question>` adds anonymized peer review to the full
5-advisor council. Use only when the verdict feels under-determined
or extra blind-spot scrutiny is needed on a high-stakes call.

After collecting 5 advisor responses, randomly map them to Response
A through E. Spawn 5 reviewer subagents in parallel (Sonnet). Each
sees all 5 anonymized responses and answers in <=250 tokens:

```
1. Which response is the strongest? Why? Reference by letter.
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL FIVE responses miss that the council should consider?
```

Chairman receives peer reviews in addition to advisor responses.

Token budget: ~40-50K.

## Integration with /strategy

Two integration modes.

### Mode A: Standalone upstream (MOST COMMON)

Use council BEFORE /strategy for frame-selection decisions.

Example: You are about to run /strategy for a governance meeting.
The audience is 4 directors. You think arc_template=challenger is
right, but you're unsure. Run `/council Should this meeting be
Challenger or Why Evolve for the governance directors?` first. Take
the verdict into /strategy.

/strategy consumes a clear meeting goal and audience. Council
pressure-tests whether that goal and audience are the right ones.

### Mode B: Backtest /strategy output (HIGH-STAKES ONLY)

Use council AFTER /strategy, BEFORE /deck-render, on artifacts
flagged high-stakes.

Example: `/council backtest ./strategy.yaml`

Council reads the YAML and pressure-tests:
- Is arc_template correct for the situation? (First Principles)
- Are the narrative_roles sequenced in a way that survives
  procurement review? (Contrarian)
- Do the talk_tracks make claims that compliance will demand
  evidence for? (Compliance Reviewer)
- Does the deck actually beat competitors in the specific
  workload the customer will POC? (Competing Vendor)
- Can the champion survive their next internal meeting with this
  material? (Champion at Risk)

Output is a verdict on the /strategy plan specifically.

## Integration with /deck-render

Before rendering, /deck-render checks the workspace for council
transcripts matching the strategy.yaml filename pattern:

```
council-*[brief-name]*.md
```

If found and the most recent transcript has verdict PIVOT or PAUSE
without a recorded user override:

```
A council backtest for this strategy.yaml returned [VERDICT]
on [DATE]. No override recorded. Options:
1. View transcript before rendering
2. Render anyway (records implicit override)
3. Cancel render
```

If verdict was GO or override was recorded: render normally, with
one-line note in deck artifact metadata referencing the council
transcript.

## Rules

- All advisors in the active mode MUST spawn in parallel. Sequential spawns collapse diversity.
- Advisors MUST be Sonnet. Chairman MUST be Opus via separate subagent.
- The chairman CAN disagree with the majority. If 4 advisors say GO
  but one dissenter's reasoning is strongest, side with the dissenter
  and state why.
- Council never makes the decision for the user. Present the verdict
  and wait for accept/override/rebrief/park.
- Adaptive language: respond in the language of the question.
- If strategy.yaml was passed, the transcript MUST reference specific
  sections, narrative_roles, and knowledge_atoms by name — not generic
  statements.
- Never name real customer accounts in example text. The skill is
  reusable across accounts; account-specific references belong in
  the brief, not in the skill file.

## Failure modes to watch

- **Council confabulation**: Contrarian invents weaknesses when the
  honest answer is "this is mostly fine." Mitigation: chairman
  weighs Contrarian claims via bias check — if the Contrarian response
  was easiest to integrate (not hardest), it may be confabulating.
- **Competing Vendor positions wrong competitor**: Mitigated by
  `competitors_in_play` brief field when present. When absent,
  advisor picks from vertical_config competitor list.
- **Compliance Reviewer becomes theater**: generic framework-name
  platitudes. Mitigated by forced-specificity prompt requiring
  section numbers, data flows, and evidence artifacts. If advisor
  returns "insufficient brief specificity," the brief was under-
  specified — enrich and re-run, don't synthesize the generic output.
- **Champion at Risk speaks like an external advisor**: the role
  prompt explicitly forbids this. If it still happens, the model is
  leaking — force a retry.
- **Lens collapse (Type 3 convergence)**: >70% argument overlap
  between divergent-role advisors. Chairman detects and re-spawns.

## Token budget by mode

| Mode | Advisors | Peer Review | Chairman | Estimated Total |
|------|----------|-------------|----------|-----------------|
| Full | 5 Sonnet | No | 1 Opus subagent | ~28-35K |
| Fast | 4 Sonnet | No | 1 Opus subagent | ~22-28K |
| Deep | 5 Sonnet | 5 Sonnet reviewers | 1 Opus subagent | ~55-65K |
| Backtest | 5 Sonnet + strategy.yaml | Optional | 1 Opus subagent | ~35-60K |

Warn the user if total context including strategy.yaml exceeds budget.

## Version history

- **v1** (2026-04-24): Initial design. Imported Karpathy LLM Council
  pattern with HLS-specific advisors.
- **v2** (2026-04-24): 10 revisions from structured grill. Pre-empirical.
  Changes: vertical-agnostic config, chairman as separate subagent,
  convergence detection, bias check, tightened triggers, pre-flight
  calibration, structured override protocol, forced-specificity prompts,
  tiered failure handling, fast mode recomposition (4 advisors, drop
  First Principles), peer review off by default (--deep to opt-in),
  Mode C killed, /deck-render transcript check added.
  Deferred to v3: competitors active/ambient/excluded split, attack
  vectors field, vault override aggregation (need n>=10), --preflight
  flag split from --fast.
  TODO: /deck-render integration contract defined here (lines 649-671)
  but requires implementation on /deck-render side — separate task.
- **v2.1** (2026-04-26): Decision architecture classification (Step 1.5).
  First real council run (NWM UC Business Semantics) returned PAUSE on
  a conviction-formation account because it assumed top-down access.
  Override (Type A) exposed the flaw: council reasoned correctly from
  a wrong premise about how the account makes decisions. Added Step 1.5
  to classify decision architecture (top-down / conviction-formation /
  procurement) before framing the brief. Chairman must use classification
  when evaluating whether a meeting can produce its intended outcome.
  Added decision_architecture as a required field in the framed brief.
