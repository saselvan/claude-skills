---
name: draft-followup (redesigned)
description: "Draft post-meeting follow-up emails as proposals, not recaps. USES WHEN: user says 'draft followup', 'draft-followup', or when auto-triggered by /process-transcript. Extracts commitments, surfaces vague language, separates OUR commitments from THEIR commitments, and generates external email as a proposal with clear next steps + checkpoint, internal email as a deal health assessment."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
---

# Follow-Up Email Redesign — Proposal-Based Framework

## Purpose (Redesigned)

A follow-up email is **NOT a recap document**. It's a **forward-looking proposal** that:

1. Confirms what each party committed to (written commitments are 2x more likely to be kept)
2. Clarifies what remains unclear (ambiguity kills deals)
3. Proposes the next step with specific dates and owners (specificity drives response)
4. Identifies blockers, risks, and assumptions (transparency builds trust)
5. Includes a checkpoint where you both decide if it's working (removes vagueness)

After the customer reads it and doesn't object, they've implicitly agreed to the plan.

**Psychological Principles Embedded:**
- **Cialdini's Commitment & Consistency** — Written commitments are stronger
- **Specificity drives response** — "Friday 2pm" gets responses; "soon" doesn't
- **Loss aversion** — Frame problems as losses, solutions as recoveries
- **Ambiguity effect** — Reduce uncertainty or deals stall
- **Progressive commitment** — Small commitments build to larger ones
- **Transparency paradox** — Naming risks increases credibility

---

## Inputs (Read from Vault)

Same as before, but with NEW extraction logic:

| Input | Source | Used For |
|-------|--------|----------|
| **Commitments** (OUR, THEIR, DECISION) | Session body + entities.jsonl signals | Classification, bilateral tracking |
| **Open questions** | Transcript markers ("I'll get back to you", "?") | Answer NOW / RESEARCH / DEFERRED categorization |
| **Vague language** | Transcript analysis | Internal flag: NOT A COMMITMENT |
| **Meeting type** | Session frontmatter + Step 1 detection | Communication style selection |
| **Attendees** (internal + customer) | Session frontmatter | Tone calibration, decision authority check |
| **Key risks & assumptions** | Session body + architecture signals | Transparency section in external email |
| **Proof points & quotes** | Transcript | Outcome-linking validation |
| **Action items** | Session body + entities.jsonl | Bilateral commitments mapping |

---

## Step 0: Commitment Extraction & Classification (NEW)

Before generating emails, extract and classify ALL commitments from the session.

### Extraction Categories

For each statement in the transcript/session that indicates an action, decision, or question:

1. **OUR-COMMITMENT** — We (SA/Databricks) promised something with timeline
   - Example: "I'll send the security architecture by Friday"
   - Email treatment: External says "I'm sending Friday"; Internal flags if at-risk

2. **THEIR-COMMITMENT** — Customer/prospect promised something with timeline
   - Example: "Your team will send sample FHIR data by next Tuesday"
   - Email treatment: External says "looking for your data next Tuesday"; Internal flags if unlikely

3. **DECISION** — Both agreed on something, attributed to person
   - Example: "As Dr. Chen confirmed, we'll proceed with FHIR streaming approach"
   - Email treatment: External states the agreement; Internal assesses if genuine or lip service

4. **OPEN-QUESTION** — Customer asked, we don't have answer in meeting
   - Example: "How much does it cost?" "Can it handle 100K messages/sec?"
   - Email treatment: Acknowledge + say when we'll answer + don't guess

5. **DEFERRED** — Customer has question, we know answer but it's premature
   - Example: "Will this replace your current EDW?" → "We'll refine in Phase 2"
   - Email treatment: External: "We'll clarify during architecture review"; Internal: not a risk

6. **DEPENDENCY** — Can't do X until Y happens
   - Example: "Can't estimate cost until we see your data volume"
   - Email treatment: Transparent in external; Internal flags if blocking progress

7. **AT-RISK** — We promised something unlikely or customer promised something they won't do
   - Example: We said "Friday" but we're missing their schema; Customer said "we'll send data" but IT hasn't approved
   - Email treatment: Internal flags as blocker; External softens language ("aiming to send Friday")

8. **VAGUE-COMMITMENT** — Customer said something non-committal
   - Example: "We'll think about it", "Interesting, let's explore", "We'll consider a pilot"
   - Email treatment: **NOT A COMMITMENT** — internal flags as risky, external asks for clarity

### Extraction Process

```
For each action item / signal in session:
1. Classify into one of 8 categories above
2. Extract: SUBJECT (what), OWNER (who), TIMELINE (when), CONFIDENCE (likely/unlikely)
3. Note: any dependencies or conditions
4. Flag: VAGUE-COMMITMENT categories require AE follow-up

Output: Commitments Matrix
| Category | What | Owner | When | Confidence | Blockers | Internal Flag |
|----------|------|-------|------|------------|----------|---------------|
| OUR-COMMITMENT | Send architecture | SA | Fri 5pm | HIGH | Waiting for their data schema | ⚠️ At-risk if no schema |
| THEIR-COMMITMENT | Provide sample FHIR data | IT Dir | Tue | MEDIUM | Needs manager approval | ⚠️ Likely to slip |
| DECISION | Proceed with POC in Q3 | VP Ops | Q3 (TBD) | MEDIUM | Budget cycle timing | ⚠️ Vague: "Q3" not "Q3 Week 2" |
| OPEN-QUESTION | Cost for pilot | SA | (commit to answer by Fri) | UNKNOWN | Need data volume first | — |
| VAGUE-COMMITMENT | "We'll think about a pilot" | Dir Ops | (undefined) | LOW | No decision pressure | 🚨 NOT A COMMITMENT |
```

---

## Step 1: Identify What's Answerable NOW vs RESEARCH vs DEFERRED

For each OPEN-QUESTION from Step 0:

### Categorization Logic

**NOW (include answer in email):**
- We prepared for this question
- Answer doesn't require customer input
- Example: "How does Lakebase handle FHIR ingestion?" → We have this answer
- **Action:** Include answer in email + proof points

**RESEARCH (promise to answer with date):**
- We didn't prepare; customer asked something we should have known
- Requires 1-2 hours research + validation
- Example: "What's the exact throughput at 100K messages/sec with your config?"
- **Action:** Acknowledge in email → "I'll validate exact throughput and send by [date]"

**TOO-EARLY (defer to next phase):**
- Answer depends on later decisions
- Example: "Will this replace your EDW?" → Depends on Phase 2 architecture
- **Action:** "We'll clarify during [next phase], which assumes we start [date]"

**THEIR-DECISION (offer support, don't speculate):**
- They need to decide internally
- Example: "Will our IT team approve this architecture?" → Their decision
- **Action:** "Your IT team should review [specific requirements]. I'm looping in [security contact]."

### Output: Question Inventory

```
| Question | Category | Answer Approach | Commitment Date | Owner |
|----------|----------|-----------------|-----------------|-------|
| "Cost for pilot?" | RESEARCH | Validate against their data volume; send pricing by Fri | Fri 5pm | SA |
| "How's throughput?" | NOW | 100K/sec confirmed in benchmark; show comparison | (today in email) | SA |
| "Will it replace EDW?" | TOO-EARLY | Depends on architecture decisions in Week 2 review | (revisit Week 2) | Both |
| "IT approval path?" | THEIR-DECISION | Your IT team reviews [security doc]; I'm looping in [contact] | (their timeline) | Customer IT |
```

---

## Step 2: Assess Deal Health (INTERNAL ONLY)

Before writing emails, diagnose deal health. This informs how you write both emails.

### Quick Assessment (5 dimensions)

**1. Customer Commitment Level**
- **YES** — Stated commitment to move forward with timeline
  - Example: "We're proceeding with POC in Q3"
  - Email impact: Proposal framing strong; assume they're ready
  
- **MAYBE** — Soft language, non-committal
  - Example: "We'll think about it", "Let's explore further"
  - Email impact: Proposal should ask clarifying questions; internal email flags as risky
  
- **NO** — No interest or stated blocker
  - Example: "This isn't a fit for us right now"
  - Email impact: Don't force proposal; focus on relationship for future

**2. Decision Authority Present**
- **HIGH** — Economic buyer or decision-maker in room
  - Email impact: Can ask for next commitment directly
  
- **MEDIUM** — Influencer/champion present, but buyer offline
  - Email impact: Email arms the champion with clarity to take to buyer
  
- **LOW** — Technical evaluator only, no commercial decision-maker
  - Email impact: Internal email flags as risky; external email helps champion present to buyer later

**3. Buying Signals vs. Shopping Signals**
- **Buying signals** (asking about implementation, timeline, team readiness, cost, support)
  - Email impact: They're serious; move to proposal
  
- **Shopping signals** (asking about capabilities, comparing to competitors, no questions about their own process)
  - Email impact: They're evaluating; proposal is lighter; assume longer sales cycle

**4. What's Blocking Next Step?**
- **Information** — They need data/clarity before committing
  - Example: "Can't commit to timeline until we see performance benchmarks"
  - Email action: Commit to providing that info with date
  
- **Budget** — They haven't secured funding
  - Example: "This needs Q3 budget approval"
  - Email action: Propose timeline around budget cycle
  
- **Org alignment** — Need to align internally
  - Example: "Our IT and Finance teams need to align on approach"
  - Email action: Offer to help with joint session
  
- **Competing priorities** — Other initiatives taking precedence
  - Example: "We're focused on migration first"
  - Email action: Propose timeline after migration; don't force urgency

- **Skepticism** — Doubts about fit or value
  - Example: "We're not sure this solves our problem" or skeptic was silent
  - Email action: Address skeptic directly (John Care transparency principle)

**5. Champion Assessment**
- **Strong mobilizer** — Has budget authority, willing to fight for it internally
  - Email impact: Champion can move deal; proposal directly asks for their commitment
  
- **Talker** — Shares information but won't spend political capital
  - Email impact: Email is leverage for them to use with boss; don't ask them to push
  
- **Weak** — No internal influence
  - Email impact: Internal email flags as risk; you may need to find real champion

### Output: Deal Health Summary (INTERNAL REFERENCE)

```
Deal Health: YELLOW (has potential but not ready to move yet)

TL;DR: Met VP Ops (decision-maker) + Dir IT (champion, moderate strength).
Customer interested in POC ("we'll think about it") but no timeline commitment.
Blocker: Need to see performance benchmarks + Budget cycle is Q4, not Q3.
Next step: Send performance data by Fri, propose Sept architecture review (before Q4 budget).
Risk: Vague timeline language suggests they're not urgent; competitor may move faster.
```

---

## Step 3: Detect Meeting Type & Communication Style (REFINED)

Use both Session type (from process-transcript) and deal health to choose communication style.

### Meeting Type → Communication Style Matrix

| Meeting Type | Deal Health | External Email Style | Internal Email Focus |
|---|---|---|---|
| **Discovery** | (any) | 80% "I heard you", 10% proof, 10% proposal to architecture | Buying signals found? Champion identified? |
| **Demo** | YES/MAYBE | 30% "you asked for X", 50% "here's how we deliver", 20% proposal to architecture | Did they say yes? What's blocking? |
| **Demo** | NO | 30% proof, 20% "here's why it matters", 50% nurture (no hard proposal) | Are they evaluating us fairly? Dead or dormant? |
| **Architecture review** | YES | 20% "here's what we agreed", 70% proposal for POC, 10% risks | Ready to commit to POC scope? |
| **Architecture review** | MAYBE | 30% "here's what we explored", 50% proposal for POC, 20% "open questions" | What's the real blocker? |
| **POC scoping** | YES | 5% recap, 95% proposal for execution (scope, dates, criteria, go/no-go gate) | Can we deliver in timeframe? |
| **POC checkpoint** | (any) | 40% progress vs criteria, 30% learnings, 30% next phase proposal | On track or slipping? What needs adjustment? |
| **Working session** | (any) | 90% "here's what we accomplished + blockers", 10% next block proposal | Productive? Making progress on blocker? |
| **Status update** | (any) | 70% progress, 20% risks, 10% next step | Momentum maintained? Anything changing? |
| **Executive briefing** | (any) | 100% strategic value (no product, no technical detail) | Do they see fit? What's their ask? |
| **Security review** | (any) | 80% "requirements confirmed", 20% next phase proposal | Ready to sign BAA? Any legal surprises? |

---

## Step 4: Surface Unclear Language (NEW MANDATORY STEP)

After all extractions, scan the commitments matrix for VAGUE-COMMITMENT entries.

### Vague Language Patterns (Flag These)

| Vague Pattern | Translation | Internal Action |
|---|---|---|
| "We'll think about it" | No decision pressure. They're evaluating options. | Flag: Not urgent. What's timeline? Who decides? |
| "Interesting" or "That makes sense" | They don't object, but no commitment. | Flag: Polite, not excited. Are they really buying? |
| "Let's explore further" | They're curious but not committed. | Flag: More research needed before proposal. |
| "Maybe in Q3" | Conditional, not confirmed. | Flag: Why Q3? Is it automatic or conditional? What triggers it? |
| "We'll consider a pilot" | Pilot is optional, not decided. | Flag: What would change "consider" to "commit"? |
| "We need to align internally" | They're not ready to commit yet. | Flag: When will they have alignment? What's blocking? |
| "This isn't a fit right now" | Not a "no," but low priority. | Flag: When might it fit? What needs to change? |

### Output: Vague Language Inventory (INTERNAL ONLY)

```
VAGUE LANGUAGE DETECTED:

Customer said: "We'll think about it" → Means: No decision pressure, evaluating us
SA follow-up action: Ask (via email or next call): "What would change your mind from 'maybe' to 'yes' by [date]?"

Customer said: "We'll consider a pilot" → Means: Pilot is optional, not approved
SA follow-up action: Propose: "If you decide to move forward, here's what the pilot would look like and timeline. Can we target [date] for a decision?"

Customer said: "Maybe in Q3" → Means: Conditional, not confirmed
SA follow-up action: Externally: "Let's target a specific date in Q3 [propose Week X]. Internally confirm Q3 is locked in or if budget cycle might delay."
```

---

## Step 5: Generate External Email (PROPOSAL FRAMEWORK)

Use the meeting type + deal health to choose structure.

### Universal Proposal Structure (All Meeting Types)

```
Subject: [Key Outcome] — [Account] / Databricks [Date]

[GREETING — 1 sentence, acknowledge the meeting]

[SECTION 1: Problem Statement OR Recap]
(Adapted to meeting type — see variants below)

[SECTION 2: Our Proposal / Next Steps]
(Concrete: what we're doing, by when, why)

[SECTION 3: Your Role / What We Need]
(What they need to do, by when, why it matters)

[SECTION 4: Success Criteria & Checkpoint]
(How we measure success, when we decide, what "yes" looks like)

[SECTION 5: Assumptions & Dependencies]
(Transparency: what might change the timeline, what we're waiting on)

[SECTION 6: Questions We're Researching]
(For each RESEARCH-category question: what we're looking into, when answer comes)

[CLOSING — Forward-looking, validation query if appropriate]
```

### Meeting-Type Variants

#### Discovery Recap (80% I Heard, 10% Proof, 10% Proposal)

```
Subject: Understanding [Their Problem] — [Account] Databricks

Hi [Name],

Thank you for the conversation. Here's my understanding of where things stand:

SITUATION:
[Objective facts about their current state — systems, team structure, recent events.
 Pull from transcript, not assumptions. Use their exact vocabulary.]

PAIN:
[Their subjective problem, in their exact words.
 "You described [X] as..." — attribute to specific people.
 Include impact: "$X in rework" or "Y hours/week" or "creating [frustration/risk]"]

GOAL:
[Their stated objective, in their words.
 "Your goal is to reduce [X] to [target] by [timeframe]."]

IMPLICATIONS:
[If they don't solve this: cost of inaction. Use loss-aversion framing.]
"As you noted, continuing with [current process] means [consequence]."

NEXT STEP:
Here's what makes sense: Let's schedule a 45-minute architecture review where we:
1. Deep-dive into how the problem manifests across your systems
2. Walk through an approach that addresses the cost + timeline concerns you raised
3. Identify what data we'd need to propose a pilot

When would Week of [specific dates] work? [I'm flexible — let me know what works.]

WHAT I'LL PREPARE:
- High-level architecture diagram showing the [capability] applied to your [specific context]
- 2-3 proof points from similar [industry/scale] deployments

WHAT WE'LL NEED FROM YOU:
- 15 min pre-call (week of [date]): technical lead to describe your current data pipeline
- During architecture review: bring the same people as today + optionally someone from your IT team

Please let me know if I've captured this accurately or if I missed any nuance.

Best,
[Your name]
```

---

#### Demo Follow-Up (30% "You Asked For", 50% "Here's How We Deliver", 20% Proposal)

```
Subject: [Capability] for [Their Use Case] — [Account] Databricks

Hi [Name],

Today we confirmed that [capability] can solve the [specific pain point] you're facing.

WHAT YOU ASKED FOR:
[2-3 specific requirements from transcript]
"You need to reduce manual reconciliation + maintain data quality"
"You want real-time visibility across [systems]"

HOW WE DELIVER:
[Proof — not features, but outcomes mapped to their requirements]

| What You Need | How We Address It | What You Saw | Proof |
|---|---|---|---|
| Reduce manual reconciliation | FHIR-to-Lakehouse automation | Live ingestion → Bronze layer | Processes 10K bundles/hour, zero manual steps |
| Real-time visibility | Streaming into analytics layer | [Dashboard demo] | [Benchmark or quote from demo] |
| Maintain data quality | Built-in validation rules + Unity Catalog | [Rule editor + audit logs shown] | [Validation accuracy %, support detail] |

WHAT THIS MEANS FOR YOUR TEAM:
- 15 FTE hours/week freed up (currently spent on reconciliation)
- Single source of truth for clinical data (eliminates [current problems])
- Audit trail for compliance (required for your [initiative])

WHAT'S NEXT:
For this to move from "proven in demo" to "running in your environment," we need to:

1. **Architecture Design** (Week of [date], 1 hour)
   - Confirm approach aligns with your IT infrastructure
   - Identify any prerequisites (VPN bandwidth, schema review, etc.)
   - Align on timeline for [next phase]

2. **Security & Compliance Review** (After architecture, 1-2 weeks)
   - Your InfoSec reviews our architecture + data residency approach
   - Legal reviews BAA (we provide template)
   - Your IT confirms infrastructure readiness

3. **Pilot Scope** (After reviews, specific)
   - 2-4 weeks of hands-on validation with your data
   - Success criteria: [benchmark throughput, validation accuracy, timeline]
   - Go/no-go decision: [date]

YOUR ROLE:
- **By [date]:** Confirm architecture review attendees (IT lead + ideally InfoSec/compliance)
- **Week of [date]:** Attend architecture review (1 hour, we'll send prep docs)
- **If you move forward:** Assign 1 technical lead for pilot (est. 5 hours/week for 4 weeks)

WHAT WE'RE COMMITTING:
- Send architecture diagram + security whitepaper by [date]
- Lead architecture review, identify blockers, propose timeline
- Provide pilot environment + monitoring (turn-key)
- 2x weekly check-ins during pilot

OPEN QUESTIONS:
We're researching a couple of items and will send answers by [date]:
- **Licensing model for your data volume:** You described ~[X] GB/day. I'll confirm cost estimate.
- **Migration from your current system:** Will take [time estimate] based on your data size. I'll refine once we see your schema.

ASSUMPTIONS:
- This assumes IT can provision network access by [date]. If that timeline shifts, everything downstream moves.
- Success criteria assume [specific data quality threshold]. If your actual data is messier, we may need to refine validation rules — doesn't block pilot, just changes scope.

THE CHECKPOINT:
If everything aligns in the architecture review + security review, we'll propose a 4-week pilot starting [date]. At the end, you'll have proof that this works in YOUR environment, against YOUR data, at YOUR scale. That's when you decide: proceed to production or revisit approach.

Looking forward to [next specific interaction].

[Your name]
```

---

#### Architecture Review Proposal (20% "What We Agreed", 70% Proposal for POC, 10% Risks)

```
Subject: Architecture Review: [Deployment Model] for [Project] — [Account] Databricks

Hi [Name],

Here's what we aligned on during today's architecture review:

AGREED ARCHITECTURE:
[Decision 1 — attributed to who confirmed it]
"As [Name] confirmed, we're proceeding with [approach] to accommodate [their stated requirement]."

[Decision 2 — same pattern]
"Your team validated that FHIR resources ingested via streaming into Bronze, normalized in Silver, meets your operational SLA of [metric]."

ASSUMPTIONS UNDERLYING THIS DESIGN:
(This is critical — flag now if any need adjustment)

| # | Assumption | Status | Verification Owner | Deadline |
|---|-----------|--------|-------------------|----------|
| 1 | Epic Clarity extract available nightly by 2am | To Confirm | Your IT Lead | Week of [date] |
| 2 | VPN bandwidth can support [Mbps] streaming | To Confirm | Your IT/Networking | Week of [date] |
| 3 | Your data schema matches [FHIR standard] (we saw draft) | Tentative | Your Data Owner | Before POC start |
| 4 | Unity Catalog can inherit your current LDAP group structure | Confirmed ✓ | Databricks (us) | — |

**If any of these assumptions change, timeline changes. Let's surface that now.**

PROPOSED PILOT (POC)
Now that we've agreed on the architecture, here's how we validate it works:

**Scope:**
- Ingest [specific FHIR resources] from your [source] into our demo Lakebase instance
- Validate data quality rules execute correctly
- Measure throughput + latency against your SLAs
- Confirm your security team's concerns are addressed

**Success Criteria (measurable, binary):**
1. FHIR bundle ingestion at [X] bundles/hour with <2% error rate
2. PII detection accuracy >99% on sample dataset
3. Clinical dashboard loads in <3 seconds with 6 months historical data
4. Security audit logs show [required compliance data] and are accessible to your team

**Timeline:**
- Week 1 (Week of [date]): Environment setup, data onboarding
- Week 2-3 (Week of [date]): Core use case validation
- Week 3: Go/no-go checkpoint — are we hitting criteria?
- Week 4: Final readout + recommendation

**YOUR TEAM'S COMMITMENT:**
- Assign 1 technical lead (est. 5 hours/week for 4 weeks) to work with us
- Provide sample data by [date] (we'll handle de-identification)
- Attend weekly check-ins (Tue 2pm, 30 min)

**OUR COMMITMENT:**
- Provide Databricks engineer + SA for hands-on support (daily availability)
- Environment + monitoring (all set up, turn-key)
- Weekly readouts showing progress vs. criteria

**GO/NO-GO GATE:**
At the end of Week 3, we measure all 4 criteria. If 4/4 pass: recommend production POC. If 3/4 pass: discuss what needs refinement. If <3/4: revisit approach.

**RISKS & OPEN ITEMS:**
- **Risk:** Legacy system latency may impact ingestion speed during peak hours. *Mitigation:* We'll test during your peak window (Week 2) + propose caching strategy if needed.
- **Question:** Will your InfoSec team need to review the architecture separately? *Action:* Let's confirm their review timeline + loop them in.

NEXT STEPS:
1. **This week:** You confirm the 3 "To Confirm" assumptions with your IT team. Reply with status + owners.
2. **By [date]:** Send your sample data (we handle everything from there).
3. **Week of [date]:** Kick off POC with environment handover + orientation.

Questions on anything above? Let me know.

Best,
[Your name]
```

---

#### POC Scoping (5% Recap, 95% Proposal for Execution)

```
Subject: [Use Case] Pilot Scope & Success Criteria — [Account] Databricks Confirmation

Hi [Name],

Here's the pilot we discussed, confirmed and ready to start:

OBJECTIVE:
To validate that [capability] meets [their stated requirement] within a [timeframe] evaluation period.

SUCCESS CRITERIA (measurable, binary — you'll see proof of each):
1. FHIR bundle ingestion processing [X] bundles/hour with <[Y]% error rate
2. PII detection accuracy >[Z]% on de-identified sample dataset
3. Clinical dashboard loads in <[T] seconds with [N] months historical data
4. Your team can access [required compliance logs] + audit trail is functional

If all 4 pass: proceed to production. If 3/4: discuss refinements. If <3/4: revisit approach.

SCOPE:
**Explicitly IN:**
- [Item 1 with specificity]
- [Item 2 with specificity]

**Explicitly OUT (to address in Phase 2):**
- Custom API development
- Production data migration (pilot uses sample data only)
- Training for end-users (handled in Phase 2 rollout)

**TIMELINE & MILESTONES:**

| Week | Milestone | Owner |
|------|-----------|-------|
| Week 1 | Environment setup, data onboarding, access provisioning | Databricks + Your IT |
| Week 2-3 | Core use case validation + weekly readouts | Databricks engineer + Your tech lead |
| Week 3 (mid) | Go/no-go checkpoint — all criteria measured | Both teams |
| Week 4 | Final readout + recommendation | Databricks + Your leadership |

**Decision Date: [specific date, Week 4]**
By this date, you'll make the go/no-go decision for production rollout.

BILATERAL COMMITMENTS:

**From Your Team:**
- Assign 1 technical lead (5 hrs/week for 4 weeks) for hands-on collab
- Provide sample data by [date] (we handle de-identification + security review)
- Attend weekly check-ins (Tue 2pm, 30 min)
- Your InfoSec reviews + approves architecture (timeline: [date])

**From Databricks:**
- Provision pilot environment (fully configured, monitoring included)
- Assign engineer + SA (daily availability, pro-active support)
- Weekly readouts (progress vs. each success criterion)
- Post-pilot recommendation (data-driven: proceed or revisit)

ASSUMPTIONS & DEPENDENCIES:
- **Your IT:** VPN bandwidth of [Mbps] available by [date]
- **Your data:** Approximately [size] of sample data provided by [date]
- **Our timeline:** Assumes no blockers on your IT side. Any delays push the decision date back.

WHAT HAPPENS AFTER THE PILOT:
- **If successful (4/4 criteria met):** We propose production timeline + your CFO engages for license agreement
- **If partially successful (3/4):** We recommend small scope refinements + extended pilot (2 weeks)
- **If unsuccessful (<3/4):** We discuss whether a different approach makes more sense OR if this isn't the right time

NEXT STEPS:
1. **This week:** You confirm the Bilateral Commitments — especially tech lead assignment + sample data timeline
2. **By [date]:** Share sample data + any pre-existing compliance concerns your InfoSec has
3. **Week of [date]:** Pilot kickoff — environment handover + first check-in

This is the plan if we move forward. Any questions before we lock it in?

Best,
[Your name]
```

---

## Step 6: Generate Internal Email (DEAL HEALTH FRAMEWORK)

Now create the internal email (for AE, manager, SE leadership). This is where you translate "what they said" into "what it means."

### Structure

```
Subject: [Account] — [Meeting Type] Debrief [Date] — [DEAL_HEALTH]

DEAL HEALTH: [GREEN | YELLOW | RED]

TL;DR (2-3 sentences, must include):
- Who we met + decision authority assessment (do they decide or are they influencers?)
- Customer commitment level (YES / MAYBE / NO) with one-sentence proof
- Blocker or risk (#1 thing that could kill this)
- What happens next (action + timeline)

---

VAGUE LANGUAGE TRANSLATION:
(What they said vs. what it means)

Customer said: "We'll think about it" 
→ Means: No decision pressure. They're in evaluation mode. 
→ Risk: Competitor may move faster. 
→ Our action: AE follow-up this week: "What would accelerate your decision?"

Customer said: "Maybe in Q3"
→ Means: Conditional, not confirmed. Budget cycle likely trigger.
→ Risk: If their budget gets reallocated, they'll delay.
→ Our action: Propose architecture review for Sept (before Q4 budget cuts).

Customer said: "Interesting"
→ Means: Polite, not excited. Not a buying signal.
→ Risk: They're evaluating us against competitors.
→ Our action: Send proof points that differentiate us vs. [likely competitor].

---

COMMITMENTS AT-RISK:
(Which promises might we struggle to keep?)

OUR COMMITMENTS:
- [ ] Send architecture Friday 5pm
  - Risk level: MEDIUM (waiting for their data schema; if not sent, we slip)
  - Mitigation: Email commitment says "aiming to Friday pending receipt of schema"
  
- [ ] Answer throughput question by Friday
  - Risk level: LOW (we can validate from benchmark data)

THEIR COMMITMENTS:
- [ ] Send sample FHIR data by Tuesday
  - Risk level: MEDIUM (IT approval needed; likely to slip)
  - Mitigation: Follow up Wed if not received; propose Thu as backup

---

CUSTOMER DECISION-READINESS:
(Are they actually ready to move, or just exploring?)

Buying signals detected:
✓ Asked about timeline ("when would we start?")
✓ Asked about team readiness ("how much support do you provide?")
✓ Asked about implementation ("what does go-live look like?")

Shopping signals detected:
✗ Asked about cost (but not urgently; haven't done budget review)
✗ Compared features to [competitor] (suggests still evaluating)
✗ No commitment on next step timeline

Assessment: **Moderate buying intent** (asking about implementation, but cost + timeline uncertain)

---

CHAMPION ASSESSMENT:
(Can they move the deal forward internally?)

Name: [Title]
Role in buying: [Economic buyer | Influencer | Technical evaluator | Champion]
Strength: [Strong mobilizer | Talker | Weak advocate]
Assessment: [1-2 sentences on whether they can drive decision]

Example:
"Dr. Chen (VP Ops, economic buyer, strong mobilizer) is willing to push for this internally but is waiting for IT (budget-constrained) to confirm feasibility. She'll carry the message, but IT is the real gatekeeper."

---

BLOCKERS & RISKS:
(What's preventing next step?)

1. **Budget** — They don't have Q3 budget allocated (they said "maybe in Q3")
   - What to do: Propose timeline around Q4 budget cycle instead (propose Oct review)
   - Follow-up: AE check: when is Q4 budget finalized?

2. **IT Alignment** — IT Director was quiet during demo; no IT commitment yet
   - What to do: Propose dedicated IT architecture review (don't assume it carries forward)
   - Follow-up: AE loop in IT Director separately; don't let SA do it

3. **Missing Skeptic** — CFO not in meeting; likely to be cost-conscious
   - What to do: Prepare ROI story (FTE hours saved + speed to value)
   - Follow-up: AE previews ROI before formal proposal to CFO

---

STRATEGIC INSIGHTS:
(What does this MEAN, not what happened?)

Title: [E.g., "Budget is the real blocker, not technology"]

[1-2 paragraphs analyzing the deeper truth]

Example:
"They're technically ready to move (asked good implementation questions, champion is strong). But budget is the constraint — they said 'maybe in Q3' which likely means 'if we get budget.' Our timeline assumption (POC starts Q3) doesn't align with their budget cycle (Q4 finalization). Recommend we propose Sept architecture review + Oct POC start (after budget is locked). This shows we're not pushing; we're being realistic about their constraints."

---

NEXT MOVES (AE priorities this week):
1. [Owner] — [Action] ([deadline])
2. [Owner] — [Action] ([deadline])
3. [Owner] — [Action] ([deadline])

Example:
1. **AE Kim** — Call Dr. Chen's IT director (separately from SA) to gauge IT buy-in on architecture. Assess: is IT a champion or a blocker? ([Tue EOD])
2. **AE Kim** — Ask CFO office: when is Q4 budget cycle finalized? ([Wed])
3. **SA** — Send architecture diagram + security whitepaper ([Fri 5pm], pending their schema)
4. **AE Kim** — If architecture arrives Fri, preview it with Dr. Chen over weekend ([Fri evening check-in])
5. **AE Kim** — Schedule Sept architecture review (contingent on budget confirmation) ([next Mon])

---

[Metadata: date, type, duration, attendees, "internal only"]
```

---

## Step 7: Quality Gates & Anti-Patterns (Refined)

After both emails draft, run this checklist. Any CRITICAL issue blocks output.

### Checklist

```
EXTERNAL EMAIL QUALITY:

1. COMMITMENT CLARITY
   [ ] Each next step has: WHAT (specific action) | WHO (name, not "team") | WHEN (date, not "soon")
   [ ] Every promise is either: (a) specific commitment or (b) soft ("aiming to" / "assuming...")
   [ ] No vague language accepted (no "we'll discuss," "let's explore," "we'll be in touch")
   ✓ PASS / ✗ FAIL

2. OUTCOME-LINKING
   [ ] Every technical statement has a "so what?" — connects to their business outcome
   [ ] Count: [N] technical statements, [N] outcome-linked. Ratio: [%]
   [ ] Minimum 90% linked. Below 90% = FAIL
   ✓ PASS / ✗ FAIL

3. BILATERAL CLARITY
   [ ] "What we're doing" and "what you're doing" are visually separated
   [ ] Dates + owners are specific for both our commitment and theirs
   [ ] No confusion about who's responsible for what
   ✓ PASS / ✗ FAIL

4. INTERNAL LEAK CHECK
   [ ] Zero deal health, champion assessment, competitive strategy in external email
   [ ] Zero "they actually mean..." language
   [ ] Zero pricing or internal resource references
   ✓ PASS (clean) / ✗ FAIL (remove immediately)

5. LOSS-AVERSION FRAMING
   [ ] Problem is framed with cost of inaction (what they lose if they don't move)
   [ ] Not just: "here's the solution" but "here's the problem you're facing + cost + solution"
   ✓ PASS / ✗ FAIL (optional but strong if present)

---

INTERNAL EMAIL QUALITY:

6. TRANSLATION ACCURACY
   [ ] Vague language is translated with specificity ("maybe" vs. "no clear timeline")
   [ ] TL;DR has commitment level (YES/MAYBE/NO) with evidence
   [ ] No assumptions left unsaid (if you think they mean X, say so in internal email)
   ✓ PASS / ✗ FAIL

7. ACTIONABILITY
   [ ] Every "Next Move" has an owner + deadline
   [ ] No observations without actions ("no compelling event" becomes "AE: find the deadline")
   [ ] 3-5 next moves max (if more, top ones are email, rest go to vault)
   ✓ PASS / ✗ FAIL

8. RISK FLAGGING
   [ ] At-risk commitments identified (which promises might slip?)
   [ ] Blockers named + owner assigned to resolve
   [ ] No surprises left unspoken
   ✓ PASS / ✗ FAIL

---

HLS-SPECIFIC (healthcare accounts only):

9. PHI DETECTION
   [ ] Zero patient names with clinical context
   [ ] Zero specific diagnoses linked to people
   [ ] Zero MRN/SSN/DOB patterns
   [ ] Zero HIPAA-specific patient information
   ✓ PASS (clean) / ✗ FAIL (delete immediately)

10. COMPLIANCE LANGUAGE
    [ ] No "we are HIPAA compliant" (should be "supports HIPAA-eligible configurations")
    [ ] No "we are HITRUST certified" without scope
    [ ] No "we agreed" in security context (use "as discussed")
    ✓ PASS / ✗ FAIL (rewrite)

---

OVERALL GATE:
[ ] PASS — ready to send
[ ] PASS WITH NOTES — [list what to watch]
[ ] BLOCKED — [critical issue, fix before sending]
```

---

## Step 8: Generate & Persist Output Files

Save external + internal emails as HTML + markdown to vault.

**Locations:**
```
Artifacts/{account}/{type}/emails/[YYYY-MM-DD]_external.html
Artifacts/{account}/{type}/emails/[YYYY-MM-DD]_external.md
Artifacts/{account}/{type}/emails/[YYYY-MM-DD]_internal.html
Artifacts/{account}/{type}/emails/[YYYY-MM-DD]_internal.md
```

**Sidecar metadata** (embedded in .md frontmatter):
```yaml
artifact_id: "{account}-followup-{YYYY-MM-DD}"
artifact_type: "email_draft"
email_type: "external|internal"
related_session: "Sessions/{account}/{type}/{date}.md"
deal_health: "GREEN|YELLOW|RED"
vague_language_detected: true|false
commitments_count: N
questions_researched: N
checkpoint_date: "YYYY-MM-DD"
```

---

## Summary of Psychology & Design Principles Applied

1. **Written commitments** (Cialdini) → Both OUR and THEIR commitments in email, clear dates/owners
2. **Specificity drives response** → Every next step has WHO | WHAT | WHEN, never "soon"
3. **Ambiguity kills deals** → Surface vague language, flag internally, ask clarifying questions
4. **Loss aversion** → Frame problems as losses, solutions as recovery
5. **Progressive commitment** → Small commitments (architecture review) → bigger (POC) → largest (production)
6. **Transparency builds trust** → Name assumptions, risks, dependencies upfront
7. **Decision frameworks reduce stalling** → Include success criteria + go/no-go checkpoint
8. **Champion the proposal as shared document** → "Here's what we both agree to" not "here's my recap"
9. **Implication + need-payoff questions** → Probe vague language ("what would change your mind?")
10. **Meeting type shapes communication** → Discovery is 80% listening; POC scoping is 95% proposal

---

## What Changed from Original Skill

| Original | Redesigned | Why |
|----------|-----------|-----|
| Focus: Recap of what happened | Focus: Proposal for what's next | Proposal drives commitment; recap is passive |
| Vague language tolerated | Vague language flagged + translated | Ambiguity kills deals; clarity moves them |
| Single email for all | Contextual style per meeting type | Discovery ≠ POC scoping; different strategies |
| Deal health buried in internal email | Deal health diagnostic (separate step) | Shapes how you write both emails |
| Commitments mixed in prose | Commitments extracted + classified | Written commitments are 2x more likely to be kept |
| No risk flagging | At-risk commitments identified | Which promises might slip? Flag proactively |
| Generic next steps | Specific next steps with owners + dates + purpose | Specificity drives response 2-3x |
| Trust by approval | Trust by transparency | Name risks + assumptions = more credible |

---

END OF REDESIGNED SKILL
