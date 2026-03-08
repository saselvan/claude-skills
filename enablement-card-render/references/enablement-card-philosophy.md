# Enablement Card Philosophy

> **Thesis:** An enablement card is not a one-pager. A one-pager persuades someone in 30 seconds. An enablement card helps someone perform in the moment. The design problem is not "how do I communicate value" — it's "how do I reduce cognitive load during a high-stakes conversation so the rep can focus on listening."

---

## What This Artifact IS vs ISN'T

| Enablement Card IS | Enablement Card IS NOT |
|---|---|
| A **job aid** — used *during* the work | A **one-pager** — used to *sell* the idea |
| **Non-linear** — user jumps to what they need | **Sequential** — reader follows top-to-bottom |
| **Internal** — never sent to customers | **External** — designed for forwarding |
| **Interrupt-driven** — "prospect just said X, what do I say?" | **Narrative** — tells a story with arc |
| **Performance support** (Gottfredson Moment 3: Apply) | **Training** (Gottfredson Moment 1: Learn New) |

This distinction drives every design decision. When you optimize for persuasion (one-pager), you maximize hero clarity and scan path. When you optimize for performance support (enablement card), you maximize **retrieval speed** and **situational routing**.

---

## Expert Foundations

Every principle in this document traces to a named expert with verifiable credentials.

### 1. Gottfredson & Mosher — 5 Moments of Need (2011)

Conrad Gottfredson (Ph.D. Instructional Science, 1984) and Bob Mosher identified five moments when workers need support: learning something New, learning More, Applying knowledge to work, Solving problems, and adapting to Change. Their central thesis is that performance support should be designed from the "moment of Apply" backward — not from training forward.

**What this means for enablement cards:**
- **Design for Moment 3 (Apply) and Moment 4 (Solve).** The BDR is mid-call. The AE is in discovery. The SA is in a technical deep dive. They don't need to *learn* — they need to *perform*.
- **Workflow learning, not course content.** Gottfredson explicitly warns against "micro-learning pushed into the workflow" — that's not performance support, that's interrupted training. A job aid must be *native to the workflow*, not an excerpt from a training deck.
- **Rapid Task Analysis (RTA).** Design for processes → steps → concepts. The card maps to the *sequence of decisions* the rep makes, not the *taxonomy of the product*.

### 2. Peter Cohan — Great Demo! & Doing Discovery (2003, 2022)

Peter Cohan founded the Great Demo! methodology, validated by Gong.io analysis of 3+ million demos. He is credited with creating the "First Law of Discovery" and the original Demo Crime Files (1995).

**Key principles for enablement cards:**
- **"Do the Last Thing First."** The most successful demos start with the end result, then peel back layers. Enablement cards should front-load the hook and proof point, not the architecture.
- **Situation Slides over Corporate Overviews.** Gong data showed the most successful demos began with a 1-2 minute customer-situation summary, not logo slides. Enablement cards should help reps *frame the customer's situation*, not recite product features.
- **Discovery ≠ Qualification.** Cohan distinguishes real discovery (understanding the customer's world) from BANT-style qualification. The enablement card should equip reps for discovery conversations, not just checkbox qualification.
- **Inverted Pyramid.** Most important information first, then supporting detail. If the call ends abruptly, the rep has delivered the highest-value content.

### 3. John Care — Mastering Technical Sales (2003, 4th ed. 2022)

John Care built SE organizations at Oracle, Sybase, Business Objects, Nortel, CA Technologies, and HP. His "3+1 Rules" framework (Develop Your People, Run Pre-Sales as a Business, Serve Your Customers, + Manage Yourself) is now integral to new hire development at many technology companies. Over 45,000 students trained.

**Key principles for enablement cards:**
- **The SE's job is to communicate technical value to both technical and non-technical stakeholders.** The SA enablement card must bridge both registers — architect-grade depth with business-outcome framing.
- **Demo Crimes.** Care cataloged the most common demo failures. The SA card should include anti-patterns: don't demo features that weren't discussed in discovery, don't lead with architecture before establishing pain.
- **"The MasterMap."** Care's framework for mapping a deal's technical landscape. The SA card should include a lightweight version — key questions to map before any technical conversation.

### 4. Sweller — Cognitive Load Theory (1988, revised)

John Sweller's CLT distinguishes intrinsic load (inherent complexity), extraneous load (caused by poor design), and germane load (productive learning effort). For enablement cards specifically:

- **Minimize extraneous load.** No decorative elements. No marketing chrome. Every pixel is information or structure.
- **Chunk by situation, not by topic.** Grouping by "prospect says X → you say Y" is lower-load than grouping by "feature 1, feature 2, feature 3."
- **Signal-to-noise ratio.** The card is used under stress (mid-call, pre-meeting). High cognitive load from the conversation itself means the card must be *extremely* low-load.

### 5. Nielsen/Norman Group — F-Pattern, Layer-Cake, and Scanning (validated)

Jakob Nielsen's eye-tracking research shows 79% of web readers scan rather than read. For enablement cards:

- **Layer-cake pattern.** Bold headers + lighter body text. The rep scans headers to find their situation, then reads the response.
- **Front-loaded lines.** First 2 words of each item carry the information scent. "Eliminate ETL" is scannable. "Our product can help" is not.
- **Contrast, not color.** Use typographic weight (bold/regular) and size (header/body) to create hierarchy, not colored backgrounds that waste ink and reduce readability.

### 6. Rossett & Schafer — Planners and Sidekicks (2007)

Allison Rossett (Professor of Educational Technology, San Diego State University) and Lisa Schafer identified two categories of performance support: **planners** (used before and after a task) and **sidekicks** (used during the task). Their GPS analogy clarifies the distinction: a roadmap is a planner, Google Maps directions are a better planner, but a GPS with the address entered is a sidekick — it operates in real-time alongside the task.

**What this means for enablement cards:**
- **Classify the card by usage moment.** A BDR mid-call needs a sidekick. An AE prepping before a meeting needs a planner. The information architecture must differ accordingly.
- **Sidekicks optimize for retrieval speed.** The user is performing the task simultaneously. Every second spent navigating the card is stolen from the conversation.
- **Planners optimize for completeness.** The user is building a mental model before the task. They want the full picture in one pass.
- **The same content can serve both modes** — but the structure changes. Sidekick = hub-and-spoke (visual router + linked depth). Planner = self-contained (all content inline with anchor navigation).

---

## Role Profile Schema (Option B Architecture)

This is the core abstraction that makes enablement cards extensible. Instead of hardcoding templates per role, we define a `role_profile` schema that drives section selection dynamically. The skill ships with 4 default profiles (BDR, AE, SA, Manager), but adding CSM, Partner, or any new role requires only a new profile YAML block — no template changes.

### Schema Definition

```yaml
role_profile:
  role: string                    # bdr | ae | sa | manager (extensible)
  workflow_context: string        # When they reach for this card
  time_pressure: enum             # seconds | minutes | hours | days
  technical_depth: enum           # shallow | moderate | deep — controls architecture detail, specs, code
  strategic_depth: enum           # shallow | moderate | deep — controls business framing, deal strategy, program context
  core_question: string           # What they're trying to answer
  persona_orientation: string     # Who THEY talk to
  objection_surface: enum         # surface | commercial | technical | program
  proof_type: enum                # quotable | logos | benchmarks | pipeline_metrics
  help_router_frame: enum         # call_situation | deal_stage | architecture | coaching
  max_pages: int                  # Cognitive budget — hard limit
  max_sections: int               # Cognitive budget — hard limit
  language_register: string       # Description of vocabulary constraints
  output_mode: enum               # hub_and_spoke | self_contained
```

### Field Semantics

| Field | Purpose | How It Drives Generation |
|-------|---------|--------------------------|
| `role` | Identity key | Selects which profile to load |
| `workflow_context` | When the card is used | Determines what situations to prioritize |
| `time_pressure` | How fast they need answers | `seconds` = extreme brevity, `days` = can include depth |
| `technical_depth` | Architecture/spec detail level | `shallow` = no technical terms, `moderate` = light technical, `deep` = full architecture/specs |
| `strategic_depth` | Business/program framing level | `shallow` = no strategy, `moderate` = connects to value, `deep` = full deal/program coaching |
| `core_question` | The job-to-be-done | Shapes section headers and content focus |
| `persona_orientation` | Who they're talking to | Calibrates language register to audience |
| `objection_surface` | What objection types they face | Determines which objections to include |
| `proof_type` | What evidence resonates | Shapes proof point format and selection |
| `help_router_frame` | How to organize the card | Determines primary navigation structure |
| `max_pages` | Cognitive budget | Hard constraint on output length |
| `max_sections` | Cognitive budget | Hard constraint on section count |
| `language_register` | Vocabulary rules | Controls technical terminology |
| `output_mode` | Information architecture | `hub_and_spoke` = visual router landing page + linked satellite docs. `self_contained` = all sections inline with anchor TOC. Driven by Rossett's planner/sidekick distinction. |

### Default Profiles

#### BDR Profile

```yaml
role_profile:
  role: bdr
  workflow_context: "Mid-call with prospect on phone, or composing LinkedIn outreach. Second monitor open. CRM in another tab. 10 seconds to find the answer."
  time_pressure: seconds
  technical_depth: shallow       # Zero technical terms — business language only
  strategic_depth: shallow       # No deal strategy — just keep the conversation alive
  core_question: "What do I say right now to keep this conversation alive?"
  persona_orientation: "First-line contacts: individual contributors, managers, occasionally directors. Rarely VP+."
  objection_surface: surface
  proof_type: quotable
  help_router_frame: call_situation
  max_pages: 2
  max_sections: 8
  language_register: "Business only. Zero technical terms. Conversational. If a 22-year-old BDR wouldn't say it naturally, rewrite it."
  output_mode: hub_and_spoke  # Sidekick mode. BDR is mid-call. Visual router surfaces situation → response instantly. Critical scripts (cold call opener, voicemail, HIPAA) stay on landing page per Gawande's Read-Do principle. Everything else links to satellite docs.
```

**Section types enabled:** Opening hooks, voicemail scripts, email templates, qualification signals, surface objection handling, handoff criteria to AE.

**Section types disabled:** Architecture diagrams, technical deep dives, POC scoping, competitive feature matrices.

#### AE Profile

```yaml
role_profile:
  role: ae
  workflow_context: "Pre-meeting prep (5-10 min before call) or mid-discovery when prospect raises unexpected topic. Laptop open, may be screen-sharing."
  time_pressure: minutes
  technical_depth: moderate       # 'Architecture' is OK. 'Pageserver' is not.
  strategic_depth: moderate       # Positions next step, doesn't own full deal strategy
  core_question: "How do I run this discovery and position the next step?"
  persona_orientation: "Directors, VPs, occasional C-level. Mix of business and technical stakeholders in same meeting."
  objection_surface: commercial
  proof_type: logos
  help_router_frame: deal_stage
  max_pages: 3
  max_sections: 12
  language_register: "Business-first, light technical. 'Architecture' is OK. 'Pageserver' is not. Acronyms must be ones the prospect uses."
  output_mode: self_contained  # Planner mode. AE preps 5-10 min before meeting. Anchor-linked TOC at top for mid-meeting retrieval.
```

**Section types enabled:** Discovery question flows, value propositions by persona, commercial objection handling, proof points with ROI, qualification deepening, SA engagement criteria.

**Section types disabled:** Implementation details, code samples, detailed architecture, CLI commands.

#### SA Profile

```yaml
role_profile:
  role: sa
  workflow_context: "Pre-meeting deep prep (30+ min for complex technical calls) or live technical Q&A where they need the precise answer."
  time_pressure: minutes
  technical_depth: deep           # Full architecture, specs, limits, caveats
  strategic_depth: moderate       # Connects technical answers to business value, doesn't own deal strategy
  core_question: "What's the technical answer, and how do I connect it to business value?"
  persona_orientation: "Architects, principal engineers, data platform leads, CTOs. Expect technical precision."
  objection_surface: technical
  proof_type: benchmarks
  help_router_frame: architecture
  max_pages: 4
  max_sections: 16
  language_register: "Full technical depth. Architecture terms expected. Include specific metrics, limits, and caveats. Never hand-wave."
  output_mode: self_contained  # Planner mode. SA preps 30+ min. Will read depth sequentially.
```

**Section types enabled:** Architecture positioning, technical objection handling, competitive technical differentiation, POC scoping, demo crime prevention, integration patterns, known limitations.

**Section types disabled:** Cold call scripts, basic qualification, pricing discussion.

#### Manager Profile

```yaml
role_profile:
  role: manager
  workflow_context: "Pipeline review, deal coaching session, or forecast call. Looking at CRM while coaching reps or explaining deal status to leadership."
  time_pressure: hours
  technical_depth: shallow        # No technical detail — focus on deal qualification
  strategic_depth: deep           # Full deal/program coaching, forecast signals, escalation
  core_question: "Is this deal real, and what should my rep do next?"
  persona_orientation: "Internal: reps, leadership, cross-functional partners. External: executive sponsors when escalating."
  objection_surface: program
  proof_type: pipeline_metrics
  help_router_frame: coaching
  max_pages: 2
  max_sections: 8
  language_register: "Business metrics, pipeline language, coaching prompts. No technical depth. Focus on deal qualification and next actions."
  output_mode: self_contained  # Planner mode. Reviews at desk, no time pressure.
```

**Section types enabled:** Deal qualification checklist, coaching prompts, escalation criteria, forecast signals, exec sponsor engagement, competitive deal patterns.

**Section types disabled:** Technical details, product features, demo flows, implementation specifics.

### Adding New Roles

To add a new role (e.g., CSM, Partner, SE Manager), create a new profile block:

```yaml
role_profile:
  role: csm
  workflow_context: "Quarterly business review prep or reactive customer call when adoption/renewal is at risk."
  time_pressure: hours
  technical_depth: moderate       # Understands product usage, adoption blockers, feature gaps
  strategic_depth: deep           # Deep on renewal strategy, expansion plays, value realization
  core_question: "How do I demonstrate value and secure renewal/expansion?"
  persona_orientation: "Economic buyers, executive sponsors, program leads. Post-sale stakeholders."
  objection_surface: program
  proof_type: benchmarks
  help_router_frame: deal_stage  # Adapted: "renewal stage" rather than "sales stage"
  max_pages: 3
  max_sections: 10
  language_register: "Business outcomes, adoption metrics, success stories. Technical only when discussing implementation blockers."
  output_mode: self_contained  # Planner mode. QBR prep is done ahead of time.
```

#### Selecting output_mode for custom profiles

Heuristic:
- If `time_pressure: seconds` AND the role has 4+ distinct task types that are never needed simultaneously → default `hub_and_spoke`
- Otherwise → default `self_contained`
- User can always override via Pass 0 or CLI flag (`--hub-and-spoke` or `--self-contained`)

The generation logic reads the profile and:
1. Applies `max_pages` and `max_sections` as hard constraints
2. Filters section types by what's enabled for that role
3. Calibrates language to `language_register`
4. Selects objections matching `objection_surface`
5. Formats proof points per `proof_type`
6. Organizes navigation per `help_router_frame`

No template changes required. The profile IS the template.

---

## The 7 Design Principles

### P1: Situation-First Architecture

**Route by what happens, not what the product does.**

The card is organized around *situations the rep encounters*, not product features or messaging pillars. The BDR card routes by "prospect says they're building AI apps" → here's what to say. The SA card routes by "customer asks about HIPAA" → here's the current answer.

**Expert basis:** Gottfredson's Rapid Task Analysis designs for processes → steps → concepts. Cohan's discovery methodology maps demo content to discovery findings, not feature lists.

**Test:** Read only the section headers. Do they describe *situations the rep faces*, or *topics about the product*? If the latter, restructure.

### P2: 10-Second Retrieval

**Any answer must be findable within 10 seconds of opening the card.**

The card is used mid-conversation. If the rep can't find what they need in 10 seconds, they've lost the moment. This constrains everything: total length, section count, header specificity, and visual density.

**Expert basis:** Gottfredson's performance support principle — "intuitive, tailored aid at the moment of need." Sweller's extraneous cognitive load — every second spent searching the card is cognitive budget stolen from the conversation.

**Test:** Hand the card to someone unfamiliar with it. Give them a scenario ("prospect just asked about HIPAA compliance"). Time how long it takes to find the answer. Target: under 10 seconds.

### P3: Title Specificity Over Persona Abstraction

**Index by real job titles, not personas.**

"Technical buyer" is useless for LinkedIn Sales Navigator. "VP Clinical Informatics" is actionable. The card maps messaging to concrete titles the rep can target, with the persona logic (why they care) embedded in the messaging itself.

**Expert basis:** Care's emphasis on communicating to specific stakeholder types. Cohan's discovery methodology requires understanding each stakeholder's specific concerns and language.

**Test:** Could a BDR paste the card's targeting into LinkedIn Sales Navigator and get results? If the titles are too abstract ("data platform leader"), they fail.

### P4: Inverted Pyramid Per Section

**Most actionable content first within every section.**

Each section follows Cohan's "Do the Last Thing First" principle — the hook, the proof point, and the response come before the supporting context. If the rep gets interrupted, they've already delivered the highest-value content.

**Expert basis:** Cohan's Inverted Pyramid (validated by Gong across 3M+ demos). Minto's Pyramid Principle applied at the micro level.

**Test:** Read only the first line of each section. Does it tell the rep what to *do* or *say*? Or does it provide background context first?

### P5: Paired Objection-Response Architecture

**Every anticipated objection has a pre-written response on the same visual line.**

The rep should never have to search for an objection response. Objection and response live together, formatted as a scannable pair (objection in bold, response immediately below).

**Expert basis:** Care's Demo Crime prevention — the worst SE behavior is being surprised by an objection and improvising badly. Cohan's preparation principle: map every anticipated question to a prepared response.

**Test:** Count the objections. Count the responses. 1:1 ratio? Are they visually paired (not on separate pages or sections)?

### P6: Timing Discipline

**Every scripted element has an explicit time budget.**

Cold call openers: 10 seconds. Voicemails: 30 seconds. Elevator pitch: 15 seconds. Discovery question flow: 5 minutes. If the script is too long for its time slot, it fails regardless of content quality.

**Expert basis:** Cohan's Situation Slide principle — the most successful demos began with a contextual overview running no longer than two minutes. Gong data validates that brevity correlates with conversion.

**Test:** Read the BDR cold call opener aloud. Time it. Over 10 seconds? Cut.

### P7: Handoff Continuity

**Every role's card includes explicit handoff language and criteria.**

The BDR card specifies exactly when to hand off to AE and what information to include. The AE card specifies when to bring in SA and what discovery outputs to share. The SA card specifies what the POC proposal needs to contain.

**Expert basis:** Care's emphasis on the team sales concept — the SE doesn't operate in isolation, and the deal's technical narrative must be consistent across handoffs. Gottfredson's process-focused design — the card maps the workflow, not just the individual task.

**Test:** Remove the handoff section. Does the rep know what to do when they've done their part? If not, the card fails its workflow purpose.

### P8: Progressive Disclosure by Time Pressure

**Surface routing first, defer depth — calibrated to the user's time pressure.**

When `time_pressure: seconds`, the card uses progressive disclosure (Nielsen, 1995): a visual router on the landing page with linked satellite documents for depth. When `time_pressure: minutes` or longer, the card is self-contained with anchor navigation, because the user intends to consume most content in one pass.

**Critical exception (Gawande Read-Do principle):** Scripts that are literally read aloud mid-task (cold call opener, voicemail, HIPAA response) must appear on the landing page even in hub-and-spoke mode. A Read-Do checklist should never require a click.

**Expert basis:** Rossett & Schafer's planner/sidekick distinction determines the architecture. Nielsen's progressive disclosure provides the mechanism. Gawande's Read-Do vs Do-Confirm distinction identifies the exception.

**Test:** For hub-and-spoke cards: can the rep identify their situation AND access the 3 most critical scripts without clicking away from the landing page? For self-contained cards: does the anchor TOC let the rep jump to any section in under 5 seconds?

---

## Evaluation Rubric: 10 Criteria

Score each criterion 0 (fail), 1 (adequate), or 2 (excellent). Pass threshold: 15/20 (75%). Great threshold: 18/20 (90%).

| # | Criterion | 0 (Fail) | 1 (Adequate) | 2 (Excellent) |
|---|-----------|----------|--------------|---------------|
| 1 | **Situation Routing** | Organized by product features or messaging pillars | Organized by situations but headers are vague | Headers name specific situations ("Prospect asks about HIPAA," "Cold call opener") |
| 2 | **Retrieval Speed** | Unfamiliar user takes >15s to find answer. Hub-and-spoke cards require >2 clicks to reach critical scripts. | 10-15s retrieval time. Hub-and-spoke cards have clear router but some scripts require clicking. | Under 10s. Hub-and-spoke: visual router + critical Read-Do scripts on landing page. Self-contained: anchor TOC enables instant jumps. |
| 3 | **Title Specificity** | Uses persona abstractions ("technical buyer") | Mix of personas and titles | All targeting uses real job titles searchable in LinkedIn |
| 4 | **Inverted Pyramid** | Background context before actionable content | Mixed — some sections lead with action | Every section's first line tells the rep what to do/say |
| 5 | **Objection Pairing** | Objections listed without responses, or responses on separate page | Objections and responses in same section but not visually paired | Objection (bold) immediately followed by response, scannable as pairs |
| 6 | **Timing Discipline** | No time budgets on scripts | Some scripts have timing | Every scripted element has explicit timing, validated by read-aloud |
| 7 | **Handoff Continuity** | No handoff guidance | Handoff mentioned but vague | Explicit handoff criteria, info to pass, and suggested language |
| 8 | **Proof Integration** | No proof points, or generic "customers love us" | Named customers but no metrics | Named customer + specific metric + timeframe in each proof reference |
| 9 | **Cognitive Load** | Dense text, >2 pages for BDR, marketing chrome | Lean but some sections overloaded | Every section serves one purpose. Nothing decorative. Nothing redundant. |
| 10 | **Role Calibration** | Same depth/register for all roles | Partially adjusted for role | Language register, technical depth, and content scope precisely match role's actual workflow |

---

## 7 Anti-Patterns

### "The Training Deck Excerpt"
**Symptom:** Card reads like slides copied from an enablement deck. Full sentences, transitions, context-setting paragraphs.
**Fix:** Strip to decision-support format. Situation → response pairs. No narrative flow needed.
**Principle:** Gottfredson — "Performance support is not micro-learning pushed into the workflow."

### "The Feature Catalog"
**Symptom:** Organized by product capabilities rather than customer situations. Sections labeled "Autoscaling," "Branching," "Unity Catalog Integration."
**Fix:** Reorganize by what the rep encounters. "Prospect has latency concerns" → mention autoscaling. "Prospect asks about dev/test" → mention branching.
**Principle:** Gottfredson's Rapid Task Analysis — design for processes, not taxonomy.

### "The Persona Fiction"
**Symptom:** Targeting sections use invented persona names ("Data-Driven Dave") or abstract archetypes ("the technical evaluator") instead of searchable job titles.
**Fix:** Replace with real titles from actual deals. "VP Clinical Informatics," "Director of Enterprise Data Architecture," "Chief Data Officer."
**Principle:** Care — communicate to specific stakeholder types. BDRs prospect by title, not persona.

### "The Encyclopedia"
**Symptom:** Card exceeds 2 pages (BDR) or 4 pages (SA). Contains information the rep will never need mid-conversation. Includes "nice to know" sections.
**Fix:** Apply the "Would I look this up mid-call?" test. If no, move it to a linked reference document.
**Principle:** Sweller — extraneous cognitive load. Every item that doesn't serve the moment of Apply makes the useful items harder to find.

### "The Hedge Garden"
**Symptom:** Responses full of qualifiers. "Lakebase may be able to..." "In some cases, customers have seen..." "Depending on the configuration, it's possible that..."
**Fix:** State the fact clearly. Add caveats as footnotes or a separate "Known Limitations" section, not inline hedges that destroy confidence.
**Principle:** Cohan — successful demos communicate tangible business value with confidence.

### "The Island"
**Symptom:** Card exists in isolation with no connection to other collateral. Rep finishes their stage and has no guidance on what happens next.
**Fix:** Every card includes: handoff criteria, information to pass forward, link to the next role's card, and link to supporting collateral (deck, one-pager, scorecard).
**Principle:** Care's team sales concept. Gottfredson's process-level design.

### "The Stale Reference"
**Symptom:** Proof points reference deals from 2+ years ago. Competitive positioning uses outdated product versions. Compliance status is wrong.
**Fix:** Every fact has a freshness date. Card includes a "Last validated" timestamp and flags items over 90 days old.
**Principle:** Tufte's data integrity — presenting stale data as current is a form of dishonesty that destroys credibility when the prospect knows more than the rep.

---

## Role-Specific Cognitive Budgets (Quick Reference)

Derived from the role profiles above. See "Role Profile Schema" section for full profile definitions including `workflow_context`, `objection_surface`, `proof_type`, and `help_router_frame`.

| Role | Max Pages | Max Sections | Time Pressure | Tech Depth | Strategic Depth | Language Register |
|---|---|---|---|---|---|---|
| **BDR** | 2 | 8 | seconds | shallow | shallow | Business only. Zero technical terms. |
| **AE** | 3 | 12 | minutes | moderate | moderate | Business-first, light technical. |
| **SA** | 4 | 16 | minutes | deep | moderate | Full technical depth. |
| **Manager** | 2 | 8 | hours | shallow | deep | Business metrics, coaching prompts. |
| **CSM** | 3 | 10 | hours | moderate | deep | Business outcomes, adoption metrics. |

---

## Strategy Contract Fields

Every enablement card requires these fields resolved before generation:

```yaml
enablement_card_strategy:
  # Required
  product: string              # What product/solution
  vertical: string             # What vertical (HLS, FSI, etc.) or "general"
  role: string                 # BDR | AE | SA | Manager
  target_titles:               # Real job titles, not personas
    - string
  
  # Required — from research
  use_cases:                   # Top 3-5 use cases for this product × vertical
    - name: string
      hook: string             # 10-second positioning
      proof: string            # Named customer + metric
  
  objections:                  # Top 5-8 objections for this role
    - statement: string        # What the prospect says
      response: string         # What the rep says back
      proof: string            # Optional supporting evidence
  
  qualification_criteria:      # Green/yellow/red signals
    green: [string]
    yellow: [string]
    red: [string]
  
  handoff:
    to_role: string            # Next role in the process
    criteria: [string]         # When to hand off
    info_to_pass: [string]     # What information to include
    suggested_language: string # How to position the handoff to the prospect
  
  # Required — metadata
  collateral_links:            # What to send/reference at each stage
    - name: string
      url: string
      when_to_use: string
  
  last_validated: date         # Freshness check
  
  # Optional
  competitive_context: string  # Primary competitor to position against
  compliance_notes: string     # Current compliance posture (e.g., "HIPAA BAA: roadmap H2")
  incentive_info: string       # Current SPIFs or quota credit
```

---

*This philosophy document is the evaluation layer. The structural templates live in `enablement-card-patterns.md`. The orchestration logic lives in `SKILL.md`. Read all three before generating any enablement card.*
