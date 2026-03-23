# Enablement Card Patterns

> **Purpose:** Structural templates for dynamic section assembly. These are the *how* — the section menu and composition rules that the SKILL.md orchestrator uses to build role-calibrated cards. The *why* lives in `enablement-card-philosophy.md`.

**Architecture:** Option B — role_profile-driven dynamic section selection. This is NOT four hardcoded templates. It's a shared section menu where each section has selection rules driven by role_profile attributes. Adding a new role (CSM, Partner) requires only a new profile YAML — no changes to this file.

---

## Rendering Approach

Enablement cards are pure markdown → optional HTML → optional PDF. Unlike decks (Google Slides API) and one-pagers (HTML table → wkhtmltopdf), enablement cards optimize for:

1. **Editability** — the field will want to customize. Markdown is the master format.
2. **Readability on screen** — most reps read on laptop or phone, not print.
3. **Copy-paste** — reps copy talk track snippets into CRM notes, Slack, and email.

Output chain: **Markdown (master) → HTML (styled, optional) → PDF (distributable, optional)**

For HTML rendering, use the same table-based layout proven in one-pager-patterns.md. No CSS Grid, no Flexbox. Tables render identically everywhere.

---

## Formatting Conventions (All Roles)

### Headers = Situations
Every H2 and H3 is a *situation* the rep faces, not a topic about the product.

```markdown
## ✅ Good: "Prospect Asks About HIPAA"
## ❌ Bad: "Compliance Features"

## ✅ Good: "Cold Call — They Pick Up"
## ❌ Bad: "Messaging Framework"

## ✅ Good: "Customer Wants to Compare vs Aurora"
## ❌ Bad: "Competitive Positioning"
```

### Timing Badges
Every scripted element gets a timing badge:

```markdown
### Opening Hook ⏱️ 10s
### Voicemail ⏱️ 30s
### Elevator Pitch ⏱️ 15s
### Discovery Flow ⏱️ 5min
```

### Objection Pairs
Objection in bold, response immediately below as blockquote:

```markdown
**"We already have Aurora/RDS for our apps."**
> That's common — Aurora is great for existing apps. Where Lakebase
> differs is when you're building *new* AI-powered apps that need
> governed lakehouse data. Teams using Aurora for this end up building
> reverse-ETL pipelines that take weeks to maintain. Ensemble Health
> Partners eliminated those entirely.
```

### Proof Blocks
Named customer + metric + timeframe, always:

```markdown
> **Ensemble Health Partners** — Reduced data sync from 20+ hours to
> 4 minutes for Clinical Viewer. Daily Lakebase spend: $900-1,000.
> (Non-PHI deployment, expanding to PHI when BAA available.)
```

### Traffic Light Qualification
Green/yellow/red formatting for quick visual scanning:

```markdown
| Signal | Criteria |
|--------|----------|
| 🟢 | Existing Databricks customer with Unity Catalog |
| 🟢 | Building operational apps or AI agents |
| 🟡 | No Postgres experience (can learn, adds ramp time) |
| 🟡 | Data volumes >8TB (requires architecture discussion) |
| 🔴 | Non-Postgres migration required (not a fit today) |
| 🔴 | GCP requirement (not supported) |
```

### Collateral Links
Inline, with context for *when* to use each:

```markdown
> 📎 **Send after qualifying call:** [One-Pager (PDF)](#)
> 📎 **Send before first AE meeting:** [Customer Brief](#)
> 📎 **SA use during deep dive:** [Technical Architecture Deck](#)
```

---

## Section Menu

This is the core of Option B. Each section has:
- **Selection rule** — which `role_profile` attributes include/exclude it
- **Depth adaptation** — how content changes based on depth attributes
- **Priority tier** — P1 essential, P2 important, P3 nice-to-have (for cognitive budget enforcement)
- **Structural template** — the markdown skeleton
- **Content source** — which research atoms feed it

### Dual Depth Convention

Depth is split into two independent dimensions:
- `technical_depth` — architecture detail, specs, code examples (shallow | moderate | deep)
- `strategic_depth` — business framing, deal strategy, program coaching (shallow | moderate | deep)

**Selection rules reference the relevant dimension explicitly.** Most sections naturally key on one dimension:
- Technical sections (Demo, POC, Limitations, Compliance) → `technical_depth`
- Strategic sections (Deal Coaching, Deal Sizing) → `strategic_depth`
- When a section includes roles that differ on both dimensions (e.g., S02 includes SA for tech depth AND Manager for strategic depth), the rule uses OR logic annotated with `# OR`

**Depth adaptation tables key on the dimension that drives content format for that section.** The column header specifies which dimension.

---

### S01: Elevator Pitch / Positioning Statement

**Purpose:** Quick verbal summary of the product/solution.

**Selection rule:**
```yaml
include_when:
  technical_depth: [shallow, moderate]
  strategic_depth: [shallow, moderate]
  # Both dimensions must be ≤ moderate (AND logic)
exclude_when:
  technical_depth: [deep]     # OR
  strategic_depth: [deep]
  # Either dimension deep → use S02 Positioning Statement instead
```

**Depth adaptation (keyed on `technical_depth`):**
| technical_depth | Format | Word Limit | Timing |
|-----------------|--------|------------|--------|
| `shallow` | Single sentence, no jargon | 30 words | ⏱️ 10s |
| `moderate` | Two sentences, light context | 50 words | ⏱️ 15s |

**Priority tier:** P1 (essential)

**Content source:** `[!tldr]`, `[!value-prop]`

**Structural template:**
```markdown
## What You're Selling ⏱️ [TIME]

[Plain English summary. ≤[WORD_LIMIT] words.]

**The pitch:**
> "[Single/double sentence a rep can say verbatim]"
```

---

### S02: Positioning Statement (replaces Elevator Pitch when either depth is deep)

**Purpose:** Technical or strategic positioning for SA/Manager/CSM contexts.

**Selection rule:**
```yaml
include_when:
  technical_depth: [deep]     # OR
  strategic_depth: [deep]
  # At least one dimension deep → richer positioning needed
exclude_when:
  technical_depth: [shallow, moderate]
  strategic_depth: [shallow, moderate]
  # Both dimensions ≤ moderate → use S01 Elevator Pitch instead (AND logic)
```

**Depth adaptation (keyed on the deeper dimension):**
| Deeper dimension | Format | Word Limit |
|------------------|--------|------------|
| `technical_depth: deep` | Architecture-aware, outcome-focused | 80 words |
| `strategic_depth: deep` (tech ≤ moderate) | Business metrics, program context, renewal/expansion framing | 75 words |

**Priority tier:** P1 (essential)

**Content source:** `[!tldr]`, `[!architecture]`, `[!value-prop]`

**Structural template (SA):**
```markdown
## Architecture in 60 Seconds

[Technical summary. Key components, data flow. ≤80 words.]

**The SA pitch** ⏱️ 30s:
> "[Architecture-aware but outcome-focused value prop]"
```

**Structural template (Manager):**
```markdown
## Program Summary

[What the program is, why it matters, current status. ≤75 words.]

**Key numbers:**
| Metric | Value |
|--------|-------|
| Quota credit | [X]× |
| SPIF | [Amount] |
| Pipeline (current) | [Count] |
```

---

### S03: Target Titles / Persona Map

**Purpose:** Who to target (BDR/AE) or who's in the buying committee (all roles).

**Selection rule:**
```yaml
include_when: always  # Universal section
```

**Depth adaptation:**
| Depth | Format |
|-------|--------|
| `shallow` | Title + Why They Care + Signal (3 columns, 3-4 rows) |
| `moderate` | Title + Role in Decision + Concern + Your Message (4 columns, 4-5 rows) |
| `deep` | Title + Technical Concerns + Your Message + Trap Questions |
| `strategic` | ICP criteria table with Green/Yellow/Red signals |

**Priority tier:** P1 (essential)

**Content source:** `[!buying-committee]`, `[!persona]`, `[!target-titles]`

**Structural template (shallow — BDR):**
```markdown
## Who To Call

| Title | Why They Care | Signal to Look For |
|-------|---------------|-------------------|
| [Real title 1] | [Their specific pain] | [LinkedIn/news trigger] |
| [Real title 2] | [Their specific pain] | [LinkedIn/news trigger] |

**LinkedIn Sales Navigator filters:**
- Title: [exact strings]
- Industry: [vertical filter]
```

**Structural template (moderate — AE):**
```markdown
## Buying Committee

| Title | Role in Decision | What They Care About | Your Message |
|-------|-----------------|---------------------|--------------|
| [Title 1] | Economic buyer | [Their concern] | [Your value prop] |
| [Title 2] | Technical evaluator | [Their concern] | [Your value prop] |
| [Title 3] | Champion/user | [Their concern] | [Your value prop] |
```

**Structural template (strategic — Manager):**
```markdown
## ICP — Who Should Your Team Target?

| Criteria | 🟢 Prioritize | 🟡 Qualify | 🔴 Deprioritize |
|----------|--------------|-----------|----------------|
| [Criteria 1] | [Good signal] | [Needs validation] | [Bad signal] |
| [Criteria 2] | [Good signal] | [Needs validation] | [Bad signal] |
```

---

### S04: Situation Router

**Purpose:** The core navigation structure — routes by situation, not topic.

**Selection rule:**
```yaml
include_when: always  # Universal section
```

**Frame adaptation (based on `help_router_frame`):**
| Frame | Routing Logic | Example Headers |
|-------|--------------|-----------------|
| `call_situation` | What the prospect says/does | "They Pick Up", "They Push Back", "They Ask About Pricing" |
| `deal_stage` | Where in the deal cycle | "First Discovery", "After Demo", "Procurement Stall" |
| `architecture` | Technical questions | "They Ask About Scale", "They Ask About Security" |
| `coaching` | Rep behaviors | "Deal is Stalling", "Champion is Weak" |

**Priority tier:** P1 (essential)

**Content source:** Context-specific — derived from `[!objection]`, `[!pain-business]`, `[!discovery-questions]`

**Structural template (call_situation — BDR):**
```markdown
## Cold Call — They Pick Up ⏱️ 10s opener

### Opening Hook
> "[Scripted opener — under 10 seconds]"

### If They Engage — Discovery Questions
1. [Question targeting pain #1]
2. [Question targeting pain #2]

### If They Push Back
[See Objection Scripts section]
```

**Structural template (coaching — Manager):**
```markdown
## Deal Coaching Prompts

### During Pipeline Review, Ask:
1. "[Question to validate qualification]"
2. "[Question to test champion strength]"
3. "[Question to pressure-test timeline]"

### If the Deal is Stalling:
- **Symptom:** [Observable behavior]
  → **Coach:** "[What to tell the rep]"
```

---

### S05: Objection Scripts

**Purpose:** Paired objection-response handling.

**Selection rule:**
```yaml
include_when: always  # Universal section
```

**Surface adaptation (based on `objection_surface`):**
| Surface | Objection Types | Example |
|---------|-----------------|---------|
| `surface` | First-call brush-offs | "We're not looking right now", "Send me an email" |
| `commercial` | Business/value objections | "Too expensive", "We already have a vendor" |
| `technical` | Architecture/capability objections | "Does it support X?", "What about Y limitation?" |
| `program` | Execution/team objections | "My team isn't trained", "We tried this before" |

**Depth adaptation:**
| Depth | Count | Response Length |
|-------|-------|-----------------|
| `shallow` | 3-5 objections | 2-3 sentences each |
| `moderate` | 5-8 objections | 3-4 sentences, may include proof |
| `deep` | 8-10 objections | Full technical response with caveats |
| `strategic` | 4-6 objections | Coaching frame, not talk tracks |

**Priority tier:** P1 (essential)

**Content source:** `[!objection]`

**Structural template:**
```markdown
## When They Push Back

**"[Objection statement verbatim]"**
> [Response — matches language_register. Include proof if available.]

**"[Objection 2]"**
> [Response]

[Repeat for all objections matching objection_surface]
```

---

### S06: Proof Points / Drop Stats

**Purpose:** Named customer evidence for credibility.

**Selection rule:**
```yaml
include_when: always  # Universal section
```

**Format adaptation (based on `proof_type`):**
| Proof Type | Format | Example |
|------------|--------|---------|
| `quotable` | Quote + name + outcome (for verbal use) | "As [Name] at [Company] said, '[quote]'" |
| `logos` | Logo + metric + use case (for slides/decks) | **Ensemble Health Partners** — 20h → 4min sync |
| `benchmarks` | Technical metric + methodology + source | "4ms p99 latency at 10K TPS (internal benchmark, 2024)" |
| `pipeline_metrics` | Deal stats for coaching | "Average deal size: $X, Win rate: Y%" |

**Priority tier:** P1 (essential)

**Content source:** `[!proof]`, `[!customer-quote]`, `[!benchmark]`

**Structural template (quotable — BDR):**
```markdown
## Proof Points to Drop

> "Teams like **[Customer]** went from [before] to [after] in [timeframe]."

> "[Quotable stat] — [Customer name]"
```

**Structural template (benchmarks — SA):**
```markdown
## Proof Points

> **[Customer]** — [Specific metric + methodology].
> [Timeframe]. [Caveat if any].
```

---

### S07: Qualification Quick-Check

**Purpose:** Green/yellow/red qualification signals.

**Selection rule:**
```yaml
include_when:
  role: [bdr, ae, manager]  # Mid-funnel roles
exclude_when:
  role: [sa]  # SA assumes already qualified
```

**Depth adaptation:**
| Depth | Format |
|-------|--------|
| `shallow` | Simple 🟢/🟡/🔴 table |
| `moderate` | 🟢/🟡/🔴 table + MEDDIC quick-check |
| `strategic` | Forecast signal table |

**Priority tier:** P2 (important)

**Content source:** `[!qualification]`, strategy.qualification_criteria

**Structural template (shallow — BDR):**
```markdown
## Qualification — Quick Check

| Signal | Criteria |
|--------|----------|
| 🟢 | [Green criteria — strong fit] |
| 🟢 | [Green criteria] |
| 🟡 | [Yellow — proceed with caveats] |
| 🔴 | [Red — disqualify] |
```

**Structural template (moderate — AE):**
```markdown
## Qualification Scorecard

| Signal | Criteria |
|--------|----------|
| 🟢 | [Green criteria] |
| 🟡 | [Yellow criteria] |
| 🔴 | [Red criteria] |

**MEDDIC Quick-Check:**
- **M**etrics: [What success looks like]
- **E**conomic buyer: [Who signs]
- **D**ecision criteria: [How they'll evaluate]
- **D**ecision process: [Timeline, stages]
- **I**dentify pain: [Confirmed?]
- **C**hampion: [Internal advocate?]
```

---

### S08: Discovery Framework

**Purpose:** Structured discovery flow with timing.

**Selection rule:**
```yaml
include_when:
  technical_depth: [moderate, deep]
  # Roles that participate in discovery conversations
exclude_when:
  role: [bdr, manager]  # BDR has simpler questions in Situation Router; Manager coaches, doesn't discover
```

**Depth adaptation (keyed on `technical_depth`):**
| technical_depth | Format | Timing |
|-----------------|--------|--------|
| `moderate` | Business pain + light technical | ⏱️ 15-30min |
| `deep` | Technical discovery deepening AE's work | ⏱️ 15min |

**Priority tier:** P2 (important)

**Content source:** `[!discovery-questions]`, `[!pain-business]`, `[!pain-technical]`

**Structural template (moderate — AE):**
```markdown
## Discovery Framework ⏱️ 15-30min

### Opening — Situation Framing ⏱️ 2min
> "[Frame what you know about their world before asking questions]"

### Pain Discovery Questions
**Business pain:**
1. [Question] → *Listen for: [signal]*
2. [Question] → *Listen for: [signal]*

**Technical pain (light touch):**
3. [Question] → *Listen for: [signal]*

### Value Articulation ⏱️ 3min
> "[Connect discovered pain to solution with proof point]"
```

**Structural template (deep — SA):**
```markdown
## Technical Discovery — Deepening the AE's Work ⏱️ 15min

### Architecture Questions
1. [Question about data architecture]
   → *Map to: [what this tells you about fit]*
2. [Question about application architecture]
   → *Map to: [fit signal]*

### Data Questions
3. [Data volumes and patterns]
4. [Data freshness requirements]
5. [Governance/compliance]

### Environment Questions
6. [Cloud provider and services]
7. [Existing database usage]
```

---

### S09: Demo Quick-Reference

**Purpose:** Demo environment, do's/don'ts, flow guidance.

**Selection rule:**
```yaml
include_when:
  technical_depth: [deep]
  # Only roles who actually run demos
exclude_when:
  role: [bdr, ae, manager]
```

**Priority tier:** P2 (important)

**Content source:** `[!demo-environment]`, internal demo docs

**Structural template:**
```markdown
## Demo Quick-Reference

### Demo Environment
- **Live demo:** [URL, credentials, setup notes]
- **Backup (recorded):** [URL]
- **Reset procedure:** [How to reset between demos]

### Demo Do's (Cohan/Care validated)
- Start with Situation Slide (frame their world first)
- Do the Last Thing First (show outcome, then peel back)
- Check in every 3-4 minutes
- Map every feature to a discovery pain point

### Demo Don'ts (Care's Demo Crimes)
- Don't demo features not discussed in discovery
- Don't lead with architecture before establishing pain
- Don't show admin console unless they asked
- Don't fill dead air with feature narration
```

---

### S10: POC Scoping Guide

**Purpose:** Standard POC scope, anti-patterns, checklist.

**Selection rule:**
```yaml
include_when:
  technical_depth: [deep]
  # Only roles who scope and run POCs
exclude_when:
  role: [bdr, ae, manager]
```

**Priority tier:** P2 (important)

**Content source:** `[!poc-template]`, internal POC docs

**Structural template:**
```markdown
## POC Scoping Guide

### Standard POC Scope
- Duration: [Typical timeframe]
- Scope: [What to include]
- Success criteria: [Measurable outcomes]

### POC Anti-Patterns
- ❌ **Scope creep:** [Common expansion requests to push back on]
- ❌ **Wrong workload:** [Workloads that don't fit]
- ❌ **Production pretense:** [POC ≠ production]

### POC Checklist
- [ ] Customer provides: [What they bring]
- [ ] We provide: [What we set up]
- [ ] Success criteria documented
- [ ] Timeline with milestones
- [ ] Escalation path for blockers
```

---

### S11: Competitive Positioning

**Purpose:** How to handle competitive mentions.

**Selection rule:**
```yaml
include_when:
  technical_depth: [moderate, deep]
  # Roles that face competitive questions in conversations
exclude_when:
  role: [bdr, manager]  # BDR handles in objections; Manager in coaching
```

**Depth adaptation (keyed on `technical_depth`):**
| technical_depth | Format |
|-----------------|--------|
| `moderate` | What to say + key differentiators table + trap question |
| `deep` | Full technical comparison + trap questions + honest weaknesses |

**Priority tier:** P2 (important)

**Content source:** `[!competitive]`, competitive battle cards

**Structural template (moderate — AE):**
```markdown
## vs [Primary Competitor]

**When they bring it up:**
> "[What to say — concise, honest, differentiated]"

**Key differentiators:**
| Dimension | Us | Them | Why It Matters |
|-----------|----|----|----------------|
| [Dimension 1] | [Our position] | [Their position] | [Impact] |

**Trap question:**
> "[Question that exposes competitor limitation]"
```

**Structural template (deep — SA):**
```markdown
## Competitive Technical Comparison

### vs [Primary Competitor]

| Dimension | [Us] | [Them] | Proof/Source |
|-----------|------|--------|-------------|
| [Architecture] | [Our approach] | [Their approach] | [Benchmark] |
| [Performance] | [Our numbers] | [Their numbers] | [Source] |

**Trap questions:**
1. "[Question exposing limitation]"
2. "[Question highlighting differentiation]"

**Honest weaknesses (know before customer raises):**
- [Limitation 1] — [mitigation or timeline]
- [Limitation 2] — [mitigation or timeline]
```

---

### S12: Known Limitations & Gotchas

**Purpose:** Current limitations, workarounds, do-not-promise list.

**Selection rule:**
```yaml
include_when:
  technical_depth: [deep]
  # Only roles who need to know precise technical boundaries
exclude_when:
  role: [bdr, ae, manager]
```

**Priority tier:** P2 (important)

**Content source:** `[!warning]`, `[!limitation]`, product docs

**Structural template:**
```markdown
## Known Limitations & Gotchas

| Limitation | Status | Workaround | Timeline |
|-----------|--------|------------|----------|
| [Limitation 1] | [Current state] | [If any] | [When fixed] |
| [Limitation 2] | [Current state] | [If any] | [When fixed] |

**⚠️ Do not promise:**
- [Thing 1 — not committed]
- [Thing 2 — not committed]
```

---

### S13: Handoff Section

**Purpose:** When to hand off, what to pass, how to position.

**Selection rule:**
```yaml
include_when: always  # Universal section
adapt_by: strategy.handoff.to_role
```

**Handoff matrix:**
| From | To | Trigger |
|------|-----|---------|
| BDR | AE | Qualified meeting booked |
| AE | SA | Technical deep-dive needed |
| SA | AE (back) | POC success, move to procurement |
| Manager | — | Escalation to leadership |

**Priority tier:** P1 (essential)

**Content source:** strategy.handoff, `[!handoff-criteria]`

**Structural template:**
```markdown
## Handoff to [TO_ROLE]

**When to hand off:** [Specific criteria from strategy.handoff.criteria]

**What to include:**
- [ ] [Item from strategy.handoff.info_to_pass]
- [ ] [Item 2]
- [ ] [Item 3]

**Positioning to the prospect:**
> "[Script from strategy.handoff.suggested_language]"

📎 **Next role's card:** [Link to [TO_ROLE] enablement card]
```

---

### S14: Coaching Playbook

**Purpose:** Deal coaching prompts and common rep mistakes.

**Selection rule:**
```yaml
include_when:
  strategic_depth: [deep]
  # Roles that coach deals and evaluate pipeline health
exclude_when:
  role: [bdr, ae, sa]
```

**Priority tier:** P1 (essential for Manager)

**Content source:** Internal coaching frameworks, deal review patterns

**Structural template:**
```markdown
## Deal Coaching Prompts

### During Pipeline Review, Ask:
1. "[Validate deal qualification]"
2. "[Test champion strength]"
3. "[Pressure-test timeline]"
4. "[Identify blockers]"

### Common Rep Mistakes

| Mistake | What to Listen For | Coaching Response |
|---------|-------------------|-------------------|
| [Mistake 1] | "[What rep says/does]" | "[How to redirect]" |
| [Mistake 2] | "[What rep says/does]" | "[How to redirect]" |
```

---

### S15: Deal Sizing

**Purpose:** How to estimate deal value.

**Selection rule:**
```yaml
include_when:
  strategic_depth: [moderate, deep]
  # Roles that own or coach deal value estimation
exclude_when:
  role: [bdr, sa]
```

**Priority tier:** P3 (nice-to-have)

**Content source:** Pricing models, deal templates

**Structural template:**
```markdown
## Deal Sizing

| Component | Typical Range | How to Estimate |
|-----------|---------------|----------------|
| [Revenue component 1] | [Range] | [What to ask] |
| [Revenue component 2] | [Range] | [What to ask] |

**Back-of-napkin:** [Simple formula]
```

---

### S16: Collateral Index

**Purpose:** Links to supporting materials with usage context.

**Selection rule:**
```yaml
include_when: always  # Universal section
```

**Priority tier:** P2 (important)

**Content source:** strategy.collateral_links

**Structural template:**
```markdown
## Collateral & Resources

| Asset | When to Use | Link |
|-------|-------------|------|
| [Name] | [Usage context from strategy.collateral_links.when_to_use] | [URL] |
| [Name 2] | [Context] | [URL] |
```

---

### S17: Outreach Templates (BDR-specific)

**Purpose:** Voicemail, LinkedIn DM, email sequence templates.

**Selection rule:**
```yaml
include_when:
  role: [bdr]
  time_pressure: [seconds]
exclude_when:
  role: [ae, sa, manager]
```

**Priority tier:** P2 (important for BDR)

**Content source:** `[!email-template]`, `[!voicemail-script]`

**Structural template:**
```markdown
## Voicemail ⏱️ 30s

> "[Full voicemail script — name, company, pain, proof, CTA, email]"

---

## LinkedIn DM

> "[Under 300 chars. Pain observation → proof → soft ask]"

---

## Email Sequence

### Email 1: Cold Outreach
**Subject:** [Under 40 chars]
> [3-4 sentences. Pain → proof → ask.]

### Email 2: Follow-up (Day 3)
**Subject:** Re: [Original]
> [2-3 sentences. New angle.]

### Email 3: Break-up (Day 7)
**Subject:** [Subject]
> [2 sentences. Final value prop + permission to close.]
```

---

### S18: Compliance & Security Posture

**Purpose:** Current compliance status, approved response language.

**Selection rule:**
```yaml
include_when:
  technical_depth: [deep]
  # Also include when strategy.compliance_notes is non-empty (any role)
exclude_when:
  role: [bdr, manager]
  # AE only if compliance is a known concern for this product
```

**Priority tier:** P3 (nice-to-have, but P1 if compliance_notes exists)

**Content source:** `[!compliance]`, strategy.compliance_notes

**Structural template:**
```markdown
## Compliance & Security Posture

| Requirement | Status | Notes |
|-------------|--------|-------|
| [Req 1] | ✅ Available / 🔄 Roadmap / ❌ N/A | [Details] |
| [Req 2] | [Status] | [Details] |

**When asked about [topic]:**
> "[Pre-approved response language]"
```

---

## Output Mode: Hub-and-Spoke vs Self-Contained

The `output_mode` field in the role_profile determines whether the card renders as a single document or as a landing page with linked satellites.

### Self-Contained Mode (default)

All selected sections render inline in a single markdown document. An anchor-linked table of contents at the top enables fast jumping. This is the standard mode for planners (AE, SA, Manager).

Structure:
- Anchor TOC (situation-framed links, not section numbers)
- All sections rendered sequentially per composition algorithm
- No external document dependencies

TOC framing: Entries use situation labels, not section type names.
- Good: "Deal stuck at discovery", "Competitor came up", "Need to justify pricing"
- Bad: "Discovery Framework", "Objection Scripts", "Pricing"

### Hub-and-Spoke Mode

The card splits into a **landing page** (hub) and **satellite documents** (spokes). The landing page is the primary artifact; satellites are linked resources.

#### Landing Page Contains (max ~1 printed page / ~400 words):

1. **Stat Bar** — 4-6 key numbers in a scannable row. Source: `drop_stats` section, compressed to pipe-delimited inline format.
   Format: `**2× quota** | **$5K SPIF** | **<10ms latency** | **70-80% cost reduction**`

2. **Elevator Pitch** — One breath, ready to say aloud. Under 30 words. Source: `elevator_pitch` section, unmodified.

3. **Critical Read-Do Scripts** — Scripts that are literally read aloud mid-task. These MUST be on the landing page per Gawande's Read-Do principle. Selection criteria:
   - `time_pressure: seconds` (the role uses this mid-task)
   - Script is under 30 seconds spoken
   - Script is used on >50% of task instances (high frequency)

   Typical candidates:
   - Cold call opener (⏱️ 10s)
   - Voicemail script (⏱️ 30s)
   - #1 most common objection response (for HLS: HIPAA)

   Render as blockquote boxes with timing badges.

4. **Situation Router Grid** — Visual grid mapping situations to satellite docs. Each cell: emoji + situation label + link to satellite.

   Framing driven by `help_router_frame` from the role_profile. Example for `call_situation`:

   | | Situation | Resource |
   |---|---|---|
   | 📞 | Someone picked up | [Call Track →](call-track.md) |
   | 📬 | Got voicemail | [VM Script →](vm-script.md) |
   | 💬 | LinkedIn accepted | [LinkedIn DM →](linkedin-sequence.md) |
   | ✉️ | Need email sequence | [Email Sequence →](email-sequence.md) |
   | ❓ | Don't know the answer | [FAQ →](faq-sheet.md) |
   | 🚫 | They pushed back | [Objection Handling →](objection-handling.md) |
   | 🤝 | Ready to hand off | [AE Handoff →](ae-handoff.md) |
   | 🤖 | Ask the AI | [AI Queries →](ai-assistant.md) |

5. **Handoff Quick-Check** — 3-4 bullet criteria for "when to hand off". Compressed from full `handoff` section.

6. **Collateral Links** — Asset name + link, no descriptions. Compressed from `collateral_index`.

#### Landing Page Design Rules:

- No prose paragraphs. Every element is a number, a script, or a link.
- Scripts render as blockquote boxes with timing badges: `> ⏱️ 10s | "Hi [name], this is..."`
- Stat bar: pipe-separated bold numbers
- Router: table or grid format, not bullet lists

#### Satellite Documents (Spokes):

The landing page links to satellite documents. These may be:
- **Existing docs** — playbooks, FAQ sheets, one-pagers already created
- **Generated satellites** — standalone files created by the skill when docs don't exist (user must confirm)
- **Placeholder links** — left as `#` if user declines generation

After generating the landing page, the skill checks which satellites exist. Missing satellites are offered for generation using the same Pass 2 transformation rules (register, timing, proofs, objections). Each generated satellite includes a back-link to the landing page and contains only the sections assigned to it in the hub-and-spoke plan.

Router grid format:
```markdown
| | Situation | Resource |
|---|---|---|
| 📞 | Someone picked up | [Call Tracks →](#) |
| 📬 | Got voicemail | [VM Scripts →](#) |
```

User replaces `#` with actual Google Drive or internal wiki links.

---

## Section Composition Algorithm

The skill reads the `role_profile` and assembles the card using this logic:

```python
def compose_card(role_profile, strategy, research_atoms):
    selected_sections = []

    # Phase 1: Selection
    for section in SECTION_MENU:
        if section.selection_rule.matches(role_profile):
            selected_sections.append(section)

    # Phase 2: Priority sorting
    selected_sections.sort(key=lambda s: s.priority_tier)  # P1 first, then P2, then P3

    # Phase 3: Cognitive budget enforcement
    if len(selected_sections) > role_profile.max_sections:
        # Keep all P1 sections
        p1_sections = [s for s in selected_sections if s.priority_tier == 'P1']
        remaining_budget = role_profile.max_sections - len(p1_sections)

        # Fill remaining budget with P2, then P3
        p2_sections = [s for s in selected_sections if s.priority_tier == 'P2'][:remaining_budget]
        remaining_budget -= len(p2_sections)

        p3_sections = [s for s in selected_sections if s.priority_tier == 'P3'][:remaining_budget]

        selected_sections = p1_sections + p2_sections + p3_sections

    # Phase 4: Depth/register adaptation
    card_sections = []
    for section in selected_sections:
        adapted = section.adapt(
            technical_depth=role_profile.technical_depth,
            strategic_depth=role_profile.strategic_depth,
            language_register=role_profile.language_register,
            help_router_frame=role_profile.help_router_frame,
            objection_surface=role_profile.objection_surface,
            proof_type=role_profile.proof_type
        )

        # Phase 5: Content population
        populated = adapted.populate(
            strategy=strategy,
            atoms=research_atoms.filter_by(section.content_source)
        )

        card_sections.append(populated)

    # Phase 6: Check output_mode
    if role_profile.output_mode == 'self_contained':
        # Phase 6a: Self-contained rendering
        # Render all sections into single document in workflow order
        # Generate anchor TOC with situation-framed labels at top
        # Each H2 gets a slug anchor matching the TOC entry
        return assemble_self_contained(
            title=f"{strategy.product} Quick-Start: {role_profile.role.upper()}",
            last_validated=strategy.last_validated,
            sections=card_sections,
            generate_anchor_toc=True
        )

    elif role_profile.output_mode == 'hub_and_spoke':
        # Phase 6b: Hub-and-spoke rendering
        # NOTE: Only generates the LANDING PAGE. Satellites are EXISTING docs.

        landing_page = {
            'stat_bar': compress_drop_stats(strategy),
            'elevator_pitch': find_section('elevator_pitch', card_sections),
            'critical_read_do_scripts': filter_read_do_scripts(card_sections),  # <30s AND >50% frequency
            'personas': compress_personas(card_sections),
            'situation_router': build_router_grid(strategy.satellite_links),  # Links to EXISTING docs
            'handoff_quick_check': compress_handoff(card_sections),
            'collateral_links': compress_collateral_index(strategy.collateral_links)
        }

        # Phase 7: Satellite gap resolution
        missing_satellites = []
        for link in strategy.satellite_links:
            if not file_exists(link.doc):
                missing_satellites.append(link)

        # Generate the landing page
        landing = assemble_landing_page(
            title=f"{strategy.product} Quick-Start: {role_profile.role.upper()}",
            last_validated=strategy.last_validated,
            landing_page=landing_page
        )

        # If satellites are missing, offer to generate them
        if missing_satellites:
            # Ask user: "N satellite docs are missing. Generate now?"
            if user_confirms_generation:
                for sat in missing_satellites:
                    # Generate satellite using same Pass 2 rules
                    sat_sections = [s for s in card_sections if s.name in sat.section_list]
                    sat_doc = assemble_satellite(
                        title=sat.name,
                        back_link=landing.filename,
                        sections=sat_sections,
                        technical_depth=role_profile.technical_depth,
                        strategic_depth=role_profile.strategic_depth,
                        language_register=role_profile.language_register
                    )
                    write_file(sat.doc, sat_doc)

        # Output: 1 landing page + K generated satellites
```

---

## Priority Tier Reference

| Tier | Meaning | Drop Policy |
|------|---------|-------------|
| **P1** | Essential — card fails without it | Never drop |
| **P2** | Important — significantly improves card | Drop only if over budget after P3 exhausted |
| **P3** | Nice-to-have — adds polish | Drop first when over budget |

**Hub-and-spoke mode priority note:** In hub-and-spoke mode, P1 sections that are Read-Do scripts render on the landing page. P1 sections that are reference content (full objection_script, qualification_check) render as the highest-priority satellites — they appear first in the router grid. P2/P3 sections render as lower-priority satellites.

### Section Priority Matrix

| Section | BDR | AE | SA | Manager |
|---------|-----|----|----|---------|
| S01/S02: Pitch/Positioning | P1 | P1 | P1 | P1 |
| S03: Target Titles | P1 | P1 | P2 | P1 |
| S04: Situation Router | P1 | P1 | P1 | P1 |
| S05: Objection Scripts | P1 | P1 | P1 | P2 |
| S06: Proof Points | P1 | P1 | P1 | P2 |
| S07: Qualification | P2 | P2 | — | P2 |
| S08: Discovery Framework | — | P2 | P2 | — |
| S09: Demo Quick-Reference | — | — | P2 | — |
| S10: POC Scoping Guide | — | — | P2 | — |
| S11: Competitive Positioning | — | P2 | P2 | — |
| S12: Known Limitations | — | — | P2 | — |
| S13: Handoff Section | P1 | P1 | P1 | P2 |
| S14: Coaching Playbook | — | — | — | P1 |
| S15: Deal Sizing | — | P3 | — | P3 |
| S16: Collateral Index | P2 | P2 | P2 | P2 |
| S17: Outreach Templates | P2 | — | — | — |
| S18: Compliance Posture | — | P3 | P2 | — |

`—` = Not included for this role

---

## Default Section Composition by Role

### BDR (max 8 sections)
1. S01: Elevator Pitch (P1)
2. S03: Target Titles (P1)
3. S04: Situation Router — call_situation frame (P1)
4. S05: Objection Scripts — surface (P1)
5. S06: Proof Points — quotable (P1)
6. S13: Handoff to AE (P1)
7. S07: Qualification Quick-Check (P2)
8. S17: Outreach Templates (P2)

### AE (max 12 sections)
1. S01: Elevator Pitch (P1)
2. S03: Target Titles / Buying Committee (P1)
3. S04: Situation Router — deal_stage frame (P1)
4. S05: Objection Scripts — commercial (P1)
5. S06: Proof Points — logos (P1)
6. S13: Handoff to SA (P1)
7. S08: Discovery Framework (P2)
8. S11: Competitive Positioning — moderate (P2)
9. S07: Qualification Scorecard + MEDDIC (P2)
10. S16: Collateral Index (P2)
11. S15: Deal Sizing (P3)
12. S18: Compliance Posture (P3) — if compliance_notes exists

### SA (max 16 sections)
1. S02: Positioning Statement / Architecture (P1)
2. S04: Situation Router — architecture frame (P1)
3. S05: Objection Scripts — technical (P1)
4. S06: Proof Points — benchmarks (P1)
5. S13: Handoff (POC → Production) (P1)
6. S03: Buying Committee — technical focus (P2)
7. S08: Technical Discovery (P2)
8. S09: Demo Quick-Reference (P2)
9. S10: POC Scoping Guide (P2)
10. S11: Competitive Technical Comparison (P2)
11. S12: Known Limitations & Gotchas (P2)
12. S18: Compliance & Security Posture (P2)
13. S16: Collateral & Reference (P2)
14-16. [Buffer for product-specific sections]

### Manager (max 8 sections)
1. S02: Program Summary (P1)
2. S03: ICP — Team Targeting (P1)
3. S04: Situation Router — coaching frame (P1)
4. S14: Coaching Playbook (P1)
5. S06: Proof Points — pipeline_metrics (P2)
6. S07: Forecast Signals (P2)
7. S16: Collateral Index (P2)
8. S13: Escalation & Resources (P2)

---

## Adding New Roles

To add a new role (e.g., CSM), define the `role_profile` in philosophy.md:

```yaml
role_profile:
  role: csm
  workflow_context: "QBR prep or reactive customer call"
  time_pressure: hours
  technical_depth: moderate       # Understands product/adoption, not architecture
  strategic_depth: deep           # Deep on renewal strategy, expansion plays
  core_question: "How do I demonstrate value and secure renewal?"
  persona_orientation: "Economic buyers, exec sponsors"
  objection_surface: program
  proof_type: benchmarks
  help_router_frame: deal_stage  # Adapted for renewal stages
  max_pages: 3
  max_sections: 10
  language_register: "Business outcomes, adoption metrics"
```

The section composition algorithm will:
1. Select sections where `include_when` matches (using `technical_depth` and/or `strategic_depth`)
2. Exclude sections where `exclude_when` matches
3. Adapt depth/format per the profile's dual depth dimensions
4. Enforce max_sections budget

**No changes to this patterns file required.**

---

*These patterns define the section menu and composition rules. Fill sections with research atoms via the SKILL.md orchestrator. Evaluate output against the rubric in `enablement-card-philosophy.md`.*

---

## HTML Rendering Patterns

When rendering to HTML/PDF, use these patterns. The approach mirrors one-pager-render: **HTML table layout, inline CSS, wkhtmltopdf for PDF**.

### Technical Constraints (same as one-pager)

| Rule | Details |
|------|---------|
| Layout | **HTML `<table>` elements** for all structure. No CSS Grid, no Flexbox. |
| Page size | Letter (8.5 × 11") for PDF. For multi-page, use page breaks. |
| Fonts | System fonts. Brand fonts via system install. Use `pt` units for sizing. |
| Colors | Brand palette from design-rules.md. WCAG AA contrast (4.5:1). Hex `#RRGGBB` only — no `rgba()`. |
| Shadows | **No `box-shadow`** — use `border` for visual separation. |
| Images | Base64 in `<img>` tags only. No base64 in CSS `background-image`. |
| Print | `@page { size: letter; margin: 0.5in; }` + `-webkit-print-color-adjust: exact`. |

### Hub-and-Spoke Landing Page HTML

The landing page is a single-page visual router. Target: 1 printed page, ~400 words.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    @page { size: letter; margin: 0.5in; }
    @media print { * { -webkit-print-color-adjust: exact; } }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 11pt;
      line-height: 1.4;
      color: #1B3139;
      margin: 0;
      padding: 0;
    }

    .page { width: 7.5in; margin: 0 auto; }

    /* Stat Bar */
    .stat-bar {
      background: #0B2026;
      color: #FFFFFF;
      padding: 12pt 16pt;
      font-size: 12pt;
      font-weight: bold;
      border-radius: 4pt;
      margin-bottom: 16pt;
    }
    .stat-bar span { margin-right: 20pt; }
    .stat-bar .accent { color: #FF8A7A; } /* 8.1:1 on #0B2026 dark bg */

    /* Section Header */
    h1 {
      font-size: 22pt;
      color: #0B2026;
      margin: 0 0 8pt 0;
      border-bottom: 2pt solid #FF3621;
      padding-bottom: 6pt;
    }

    h2 {
      font-size: 13pt;
      color: #1B3139;
      margin: 16pt 0 8pt 0;
      text-transform: uppercase;
      letter-spacing: 1pt;
    }

    /* Elevator Pitch */
    .pitch {
      font-size: 13pt;
      color: #1B3139;
      margin: 8pt 0 16pt 0;
    }

    /* Read-Do Script Box */
    .script-box {
      background: #F5F7F8;
      border-left: 4pt solid #00A972;
      padding: 10pt 14pt;
      margin: 10pt 0;
    }
    .script-box .timing {
      font-size: 9pt;
      color: #3D5A66; /* 7.1:1 on light bg */
      text-transform: uppercase;
    }
    .script-box .script {
      font-size: 11pt;
      font-style: italic;
      margin-top: 6pt;
    }

    /* Situation Router Grid */
    .router-table {
      width: 100%;
      border-collapse: collapse;
      margin: 12pt 0;
    }
    .router-table td {
      padding: 8pt 10pt;
      border-bottom: 1pt solid #E5E9EC;
      vertical-align: middle;
    }
    .router-table .icon { width: 24pt; text-align: center; font-size: 14pt; }
    .router-table .situation { font-size: 11pt; color: #1B3139; }
    .router-table .link { text-align: right; }
    .router-table a {
      color: #1A5A8F; /* 7.2:1 on white bg */
      text-decoration: none;
      font-weight: 500;
    }

    /* AI Assistant Card */
    .ai-card {
      background: #0B2026;
      color: #FFFFFF;
      padding: 12pt 16pt;
      border-radius: 4pt;
      margin: 16pt 0;
    }
    .ai-card h3 { margin: 0 0 6pt 0; font-size: 12pt; }
    .ai-card .examples {
      font-size: 9pt;
      color: #B8CCD6; /* 9.3:1 on #0B2026 dark bg */
      font-family: monospace;
    }

    /* Handoff Checklist */
    .handoff-list {
      padding-left: 20pt;
      margin: 8pt 0;
    }
    .handoff-list li {
      margin: 4pt 0;
      font-size: 10pt;
    }

    /* Footer */
    .footer {
      font-size: 8pt;
      color: #3D5A66; /* 7.1:1 on white bg */
      border-top: 1pt solid #E5E9EC;
      padding-top: 8pt;
      margin-top: 16pt;
    }
  </style>
</head>
<body>
<div class="page">

  <h1>[Product] [Vertical] — Your Quick Start</h1>

  <div class="stat-bar">
    <span class="accent">2×</span> quota |
    <span class="accent">$5K</span> SPIF/acct |
    <span class="accent"><10ms</span> response |
    <span class="accent">70-80%</span> cost savings
  </div>

  <p class="pitch">[Elevator pitch — one sentence, under 30 words]</p>

  <h2>🤖 Got a Question? Ask the AI</h2>
  <div class="ai-card">
    <h3><a href="#" style="color:#5CEBA0;">Open AI Assistant →</a></h3>
    <p class="examples">Try: "HIPAA script" · "DBA voicemail" · "Aurora vs us" · "pricing objection"</p>
  </div>

  <h2>Cold Call Opener ⏱️ 10s</h2>
  <div class="script-box">
    <div class="timing">⏱️ 10 seconds</div>
    <div class="script">"Hi [Name], this is [You] from [Company]. I work with healthcare teams building patient apps. Do you have 2 minutes?"</div>
  </div>

  <h2>HIPAA — You'll Get Asked ⏱️ 15s</h2>
  <div class="script-box">
    <div class="timing">⏱️ 15 seconds</div>
    <div class="script">"[Product] runs on [Platform]'s secure infrastructure — encrypted data, private networking, access controls. HIPAA certification is on the roadmap. Many health systems start with a non-patient-data pilot to prove the fit."</div>
  </div>

  <h2>I Need Help Right Now</h2>
  <table class="router-table">
    <tr>
      <td class="icon">📞</td>
      <td class="situation">Someone picked up</td>
      <td class="link"><a href="#">Call Tracks →</a></td>
    </tr>
    <tr>
      <td class="icon">📬</td>
      <td class="situation">Got voicemail</td>
      <td class="link"><a href="#">VM Scripts →</a></td>
    </tr>
    <tr>
      <td class="icon">✉️</td>
      <td class="situation">Need email sequence</td>
      <td class="link"><a href="#">5-Touch Sequence →</a></td>
    </tr>
    <tr>
      <td class="icon">❓</td>
      <td class="situation">Don't know the answer</td>
      <td class="link"><a href="#">FAQ Sheet →</a></td>
    </tr>
    <tr>
      <td class="icon">⚔️</td>
      <td class="situation">Mentioned competitor</td>
      <td class="link"><a href="#">Competitive FAQ →</a></td>
    </tr>
    <tr>
      <td class="icon">✅</td>
      <td class="situation">Need to qualify</td>
      <td class="link"><a href="#">ICP & Qualification →</a></td>
    </tr>
    <tr>
      <td class="icon">🤝</td>
      <td class="situation">Ready to hand off</td>
      <td class="link"><a href="#">AE Handoff →</a></td>
    </tr>
  </table>

  <h2>Handoff Quick-Check</h2>
  <ul class="handoff-list">
    <li>✓ Persona confirmed (DBA, Engineer, or VP)</li>
    <li>✓ Operational use case identified</li>
    <li>✓ Timeline <6 months</li>
    <li>✓ Budget pathway identified</li>
  </ul>

  <div class="footer">
    Internal Use Only • v2.0 • [Date] • <a href="#">Full Enablement Kit →</a>
  </div>

</div>
</body>
</html>
```

### Self-Contained HTML Template

For AE/SA/Manager cards rendered as single multi-page documents.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    @page { size: letter; margin: 0.5in 0.75in; }
    @media print { * { -webkit-print-color-adjust: exact; } }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 10.5pt;
      line-height: 1.45;
      color: #1B3139;
      margin: 0;
      padding: 0;
    }

    .page { max-width: 7in; margin: 0 auto; }

    /* Title Block */
    .title-block {
      border-bottom: 3pt solid #FF3621;
      padding-bottom: 12pt;
      margin-bottom: 16pt;
    }
    h1 {
      font-size: 24pt;
      color: #0B2026;
      margin: 0 0 6pt 0;
    }
    .metadata {
      font-size: 9pt;
      color: #3D5A66; /* 7.1:1 on white bg */
    }

    /* TOC */
    .toc {
      background: #F5F7F8;
      padding: 12pt 16pt;
      margin: 16pt 0;
      column-count: 2;
      column-gap: 24pt;
    }
    .toc-title {
      font-size: 10pt;
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: 1pt;
      color: #3D5A66; /* 7.1:1 on light bg */
      margin-bottom: 8pt;
    }
    .toc ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .toc li {
      margin: 4pt 0;
      font-size: 10pt;
    }
    .toc a {
      color: #1A5A8F; /* 7.2:1 on light bg */
      text-decoration: none;
    }

    /* Section Headers */
    h2 {
      font-size: 14pt;
      color: #0B2026;
      margin: 20pt 0 10pt 0;
      padding-bottom: 4pt;
      border-bottom: 1pt solid #E5E9EC;
    }
    h3 {
      font-size: 11pt;
      color: #1B3139;
      margin: 14pt 0 6pt 0;
    }

    /* Timing Badge */
    .timing-badge {
      display: inline-block;
      background: #0B2026;
      color: #FFFFFF;
      font-size: 8pt;
      padding: 2pt 6pt;
      border-radius: 2pt;
      margin-left: 8pt;
      vertical-align: middle;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 10pt 0;
      font-size: 10pt;
    }
    th {
      background: #1B3139;
      color: #FFFFFF;
      text-align: left;
      padding: 8pt 10pt;
      font-weight: 500;
    }
    td {
      padding: 8pt 10pt;
      border-bottom: 1pt solid #E5E9EC;
      vertical-align: top;
    }
    tr:nth-child(even) td { background: #F9FAFB; }

    /* Objection Block */
    .objection {
      margin: 12pt 0;
    }
    .objection-text {
      font-weight: bold;
      color: #0B2026;
      margin-bottom: 4pt;
    }
    .objection-response {
      background: #F5F7F8;
      border-left: 3pt solid #00A972;
      padding: 8pt 12pt;
      font-style: italic;
    }

    /* Proof Block */
    .proof-block {
      background: #0D1F2D;
      border-left: 3pt solid #2272B4;
      padding: 10pt 14pt;
      margin: 10pt 0;
    }
    .proof-block .customer {
      font-weight: bold;
      color: #6EB5E5; /* 7.8:1 on #0D1F2D dark bg */
    }
    .proof-block .metric {
      color: #FFFFFF;
    }

    /* Qualification Signals */
    .signal-green { color: #006644; font-weight: bold; } /* 7.3:1 on white bg */
    .signal-yellow { color: #705510; font-weight: bold; } /* 7.1:1 on white bg */
    .signal-red { color: #FF3621; font-weight: bold; }

    /* Discovery Script */
    .script-block {
      background: #F5F7F8;
      border-left: 3pt solid #FFAB00;
      padding: 8pt 12pt;
      margin: 8pt 0;
      font-style: italic;
    }

    /* Collateral Links */
    .collateral-table a {
      color: #1A5A8F; /* 7.2:1 on white bg */
      text-decoration: none;
    }

    /* Footer */
    .footer {
      font-size: 8pt;
      color: #3D5A66; /* 7.1:1 on white bg */
      border-top: 1pt solid #E5E9EC;
      padding-top: 10pt;
      margin-top: 24pt;
      text-align: center;
    }

    /* Page Break */
    .page-break { page-break-before: always; }
  </style>
</head>
<body>
<div class="page">

  <div class="title-block">
    <h1>[Product] [Vertical] — [Role] Enablement Card</h1>
    <div class="metadata">
      <strong>Last validated:</strong> [Date] |
      <strong>Quota credit:</strong> 2× |
      <strong>Avg deal size:</strong> $150-300K ARR
    </div>
  </div>

  <div class="toc">
    <div class="toc-title">Quick Navigation</div>
    <ul>
      <li><a href="#the-pitch">The Pitch</a></li>
      <li><a href="#buying-committee">Buying Committee</a></li>
      <li><a href="#first-discovery">First Discovery</a></li>
      <li><a href="#commercial-objections">Commercial Objections</a></li>
      <li><a href="#proof-points">Proof Points</a></li>
      <li><a href="#competitive">vs [Competitor]</a></li>
      <li><a href="#qualification">Qualification Scorecard</a></li>
      <li><a href="#sa-handoff">When to Bring in SA</a></li>
      <li><a href="#deal-sizing">Deal Sizing</a></li>
      <li><a href="#collateral">Collateral by Stage</a></li>
    </ul>
  </div>

  <h2 id="the-pitch">The Pitch</h2>
  <p>[Elevator pitch paragraph]</p>
  <p><strong>For the business buyer:</strong> "[Business message]"</p>
  <p><strong>For the technical stakeholder:</strong> "[Technical message]"</p>

  <h2 id="buying-committee">Buying Committee</h2>
  <table>
    <tr>
      <th>Title</th>
      <th>Role in Decision</th>
      <th>What They Care About</th>
      <th>Your Message</th>
    </tr>
    <tr>
      <td><strong>[Title 1]</strong></td>
      <td>[Role]</td>
      <td>[Concern]</td>
      <td>"[Message]"</td>
    </tr>
    <!-- Repeat rows -->
  </table>

  <h2 id="first-discovery">First Discovery <span class="timing-badge">15-30min</span></h2>
  <h3>Opening — Situation Framing <span class="timing-badge">2min</span></h3>
  <div class="script-block">
    "[Opening script]"
  </div>

  <h3>Pain Discovery Questions</h3>
  <ol>
    <li>"[Question 1]" → <em>Listen for: [signal]</em></li>
    <li>"[Question 2]" → <em>Listen for: [signal]</em></li>
  </ol>

  <h2 id="commercial-objections">Commercial Objections</h2>
  <div class="objection">
    <div class="objection-text">"[Objection statement]"</div>
    <div class="objection-response">[Response with proof]</div>
  </div>

  <h2 id="proof-points">Proof Points</h2>
  <div class="proof-block">
    <span class="customer">[Customer Name]</span> —
    <span class="metric">[Specific metric with timeframe]</span>
  </div>

  <h2 id="competitive">vs [Primary Competitor]</h2>
  <table>
    <tr>
      <th>Dimension</th>
      <th>[Us]</th>
      <th>[Them]</th>
      <th>Why It Matters</th>
    </tr>
    <tr>
      <td>[Dimension]</td>
      <td>[Our position]</td>
      <td>[Their position]</td>
      <td>[Impact]</td>
    </tr>
  </table>

  <p><strong>Trap question:</strong></p>
  <div class="script-block">"[Question that exposes competitor weakness]"</div>

  <h2 id="qualification">Qualification Scorecard</h2>
  <table>
    <tr>
      <th>Signal</th>
      <th class="signal-green">🟢 Strong</th>
      <th class="signal-yellow">🟡 Needs Work</th>
      <th class="signal-red">🔴 Walk Away</th>
    </tr>
    <tr>
      <td><strong>Use case</strong></td>
      <td>[Good signal]</td>
      <td>[Okay signal]</td>
      <td>[Bad signal]</td>
    </tr>
  </table>

  <h2 id="sa-handoff">When to Bring in SA</h2>
  <p><strong>Bring in SA when:</strong></p>
  <ul>
    <li>✓ [Criterion 1]</li>
    <li>✓ [Criterion 2]</li>
  </ul>

  <h2 id="deal-sizing">Deal Sizing</h2>
  <table>
    <tr>
      <th>Component</th>
      <th>Typical Range</th>
      <th>Sizing Question</th>
    </tr>
    <tr>
      <td>[Component]</td>
      <td>[Range]</td>
      <td>"[Question]"</td>
    </tr>
  </table>

  <h2 id="collateral">Collateral by Stage</h2>
  <table class="collateral-table">
    <tr>
      <th>Stage</th>
      <th>Asset</th>
      <th>When to Send</th>
    </tr>
    <tr>
      <td>[Stage]</td>
      <td><a href="#">[Asset Name]</a></td>
      <td>[Usage context]</td>
    </tr>
  </table>

  <div class="footer">
    Generated via enablement-card-render | Role: [role] | Output: self_contained | Sections: [N]/[max]
  </div>

</div>
</body>
</html>
```

### Rendering Commands

```bash
# Setup
mkdir -p output/rendered

# Render Hub-and-Spoke landing page to PDF
wkhtmltopdf --enable-local-file-access \
  --page-size Letter \
  --margin-top 0.5in --margin-bottom 0.5in \
  --margin-left 0.5in --margin-right 0.5in \
  --dpi 150 \
  output/landing-page.html output/landing-page.pdf 2>/dev/null

# Render Self-Contained card to PDF
wkhtmltopdf --enable-local-file-access \
  --page-size Letter \
  --margin-top 0.5in --margin-bottom 0.75in \
  --margin-left 0.75in --margin-right 0.75in \
  --dpi 150 \
  --footer-center "[page] of [topage]" \
  --footer-font-size 8 \
  output/enablement-card.html output/enablement-card.pdf 2>/dev/null

# Convert to PNG for visual QA
pdftoppm -png -r 200 -singlefile output/landing-page.pdf output/rendered/landing-page
```

### Design Rules Reference

<!-- Note: HTML enablement cards use WCAG AA accessible color variants that differ by background context. Light-bg text colors are darker than the raw brand palette; dark-bg text colors are lighter. All text colors achieve 7:1+ contrast ratio (WCAG AAA). -->

For colors, fonts, and brand styling, use `~/.claude/skills/deck-render/references/design-rules.md` as the source palette, then apply these accessible variants:

**On light/white backgrounds:**

| Element | Value | Contrast | Use |
|---------|-------|----------|-----|
| blue (text) | #1A5A8F | 7.2:1 | Links, TOC links, collateral links |
| green (text) | #006644 | 7.3:1 | Signal green text, positive indicators |
| yellow (text) | #705510 | 7.1:1 | Signal yellow text, caution indicators |
| metadata/timing | #3D5A66 | 7.1:1 | Timing labels, metadata, TOC titles, footer |
| green (border) | #00A972 | — | Script box left borders, objection response borders (decorative) |
| yellow (border) | #FFAB00 | — | Discovery script left borders (decorative) |

**On dark backgrounds (#0B2026, #0D1F2D):**

| Element | Value | Contrast | Use |
|---------|-------|----------|-----|
| stat accent | #FF8A7A | 8.1:1 | Stat bar numbers on #0B2026 |
| AI examples | #B8CCD6 | 9.3:1 | AI card example text on #0B2026 |
| AI links | #5CEBA0 | 9.1:1 | AI card link text on #0B2026 |
| proof customer | #6EB5E5 | 7.8:1 | Customer name in proof blocks on #0D1F2D |
| t1 | #FFFFFF | — | Primary text on dark |
| t2 | #C4CCD6 | — | Secondary text on dark |

**Context-independent (structural):**

| Element | Value | Use |
|---------|-------|-----|
| bg | #0B2026 | Dark backgrounds (stat bar, AI card) |
| bgCard | #1B3139 | Card backgrounds |
| primary | #FF3621 | Databricks red (borders, title accents — never as text on white) |
| light bg | #F5F7F8 | Script boxes, TOC |
| border | #E5E9EC | Table borders |
