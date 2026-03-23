---
name: draft-followup
description: "Draft post-meeting follow-up emails (external recap + internal debrief) from structured process-transcript output. USE WHEN: user says 'draft followup', 'draft-followup', or when auto-triggered by /process-transcript. Takes a session file as input. Produces external + internal email pairs as HTML + MD."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
---

# Follow-Up Email Render — SA Intelligence Vault

Draft post-meeting follow-up emails from structured `process-transcript` output.

## Purpose

After `/process-transcript` completes, this skill generates:

1. **External email** (customer-facing) — The recap they'll forward to their VP/CMIO
2. **Internal email** (AE + manager) — The real deal assessment

Both saved as `.html` files you can open in browser and copy-paste into Gmail.

## Usage

```
/draft-followup                        # Uses most recent session in vault
/draft-followup Sessions/CHLA/customer/2026-01-21.md   # Specific session
```

### Audience Tailoring Engine (HLS domains)

If the session account involves healthcare/HLS/clinical context, read the shared tailoring map:

```
_System/tailoring/hls-tailoring-map.yaml   (relative to workspace/vault root)
```

Match the primary recipient's role to the closest profile (`clinical_executive`, `technical_gatekeeper`, `commercial_lead`, `customer_success`). Use the profile's `kill_list` to avoid irrelevant depth in the follow-up (e.g., don't include architecture details for executives), its `lava_element` for the hero proof point to reinforce, and its `mental_model` for framing language.

## Inputs (Read from Vault)

The skill reads structured data that `/process-transcript` already extracted:

| Input | Source | Used For |
|-------|--------|----------|
| Attendees (internal + customer) | Session frontmatter | To/CC fields, tone calibration |
| Action items | Session body + entities.jsonl | "Next Steps" section |
| Commitments (ours→them, theirs→us) | Session body | Accountability sections |
| Risks | Session body + entities.jsonl | Internal email risk flags |
| MEDPICC signals | entities.jsonl | Internal email deal assessment |
| Key quotes | Session body + entities.jsonl | External email validation points |
| Meeting type | Session frontmatter `type` field | Template selection |
| Account context | Accounts/[name].md | Industry language, deal stage |
| Stakeholder profiles | People/clients/[name].md | Seniority detection, role context |
| Use case stage | UseCases/[account]/[name].md | Deal stage calibration |

## Board Read Protocol (Coordinated Mode)

Check for a `_meta.board_dir` field passed by the invoking coordinator.

**If `_meta.board_dir` is present** — you are running inside the post-meeting coordinator pipeline:
1. Read `{board_dir}/context.yaml` if it exists. The post-meeting coordinator may have already extracted:
   - Session metadata (account, type, date, attendees)
   - Pre-parsed entities from the transcript
   Use this to skip redundant parsing. If context.yaml provides attendees, don't re-detect them.
2. Read `{board_dir}/board/` for any prior skill outputs (draft-followup is typically the FIRST skill in the post-meeting pipeline, so the board may be empty).

**If `_meta.board_dir` is absent** — standalone mode. Skip this section entirely. Zero cost.

## Step 1: Detect Meeting Type

Read session frontmatter and body to classify:

| Meeting Type | Detection Signals | Template |
|---|---|---|
| `discovery` | First meeting, "learning about", L100-L200, no prior sessions for this use case | Discovery Recap |
| `demo` | "showed", "demonstrated", demo environment mentioned, L200-L300 | Demo Follow-Up |
| `architecture_review` | "design", "whiteboard", architecture discussion, L300-L400 | Architecture Recap |
| `poc_scoping` | "POC", "pilot", success criteria discussed, L300 | POC Scope Confirmation |
| `poc_execution` | Active POC, checkpoint, progress against criteria, L300-L400 | POC Checkpoint |
| `office_hours` | "office hours", "working session", tactical troubleshooting, L100-L200 | Working Session Recap |
| `ebc` | Executive briefing, C-suite attendees, strategic discussion | Executive Briefing Recap |
| `qbr` | Quarterly review, metrics review, expansion discussion | QBR Follow-Up |
| `kickoff` | Post-sale, onboarding, "kick-off", L200-L300 | Kickoff Recap |
| `security_review` | Compliance, HITRUST, SOC2, BAA, security questionnaire | Security Review Recap |

**Fallback:** If type unclear, use `general_recap` template.

## Step 2: Detect Audience Seniority

Scan attendees_customer for highest-seniority person present:

| Seniority Tier | Title Patterns | Mental Model | Key Vocabulary | Tone Effect |
|---|---|---|---|---|
| `executive` | C-suite, SVP, VP, Chief, President, Dean | Risk, ROI, Strategic Advantage, Time-to-Value | *Governance, Compliance, Consolidation, Efficiency, Revenue Leakage, Competitive Parity* | BLUF first. No "how," only "what" and "why." No product names — use "the platform." Concise. |
| `director` | Director, Head of, Sr. Director | Execution, Capacity, Cross-Dept Friction | *Interoperability, Roadmap, Resource Lift, Adoption Curve, Training Burden, Workflow Impact* | Pragmatic, assuring. "We have a plan." Highlight implementation plan and resource requirements. |
| `manager` | Manager, Lead, Principal, Team Lead | Feasibility, Specific Features, Vendor Support | *User Management, Reporting, API Docs, Latency, Uptime, UAT, Shift Coverage* | Collaborative, detail-oriented. Include action items table with owners and dates. Link to docs. |
| `individual` | Engineer, Analyst, Developer, Scientist, Architect | "My Daily Life," Technical Correctness | *JSON, Python SDK, DICOM Tags, SSO Config, Error Handling, Logs, REST endpoints* | Technical, precise, "no fluff." Include code snippets, direct links to API references, screenshots. |

**Rule:** Calibrate to the HIGHEST seniority person on the email. If CMIO and engineer both attended, write for the CMIO. Technical details go in attachments or "happy to dive deeper" offers.

**HLS-specific vocabulary substitutions (always apply for healthcare accounts):**

| Generic Term | HLS Term |
|---|---|
| User | Provider / Clinician |
| Session | Encounter |
| Company | Health System |
| Customer | Organization |
| Dashboard | Clinical/Operational Dashboard |
| Data pipeline | Clinical data flow |

## Step 2b: Extract Dynamic Lexicon Table (MANDATORY)

Before generating either email, scan the transcript/session for the customer's **exact vocabulary**. This produces a lookup table that overrides the static HLS substitution table (Step 2) when conflicts occur.

**Extraction process:**

1. **Scan for problem descriptions:** Find every sentence where a customer attendee describes a pain, challenge, or frustration. Extract their exact phrasing.
2. **Scan for initiative names:** Find proper nouns for their internal projects, systems, or programs (e.g., "Digital Front Door," "Project Nightingale," "Epic Clarity extract").
3. **Scan for system names:** Their names for tools, databases, and processes (e.g., "the cube" for their analytics warehouse, "morning huddle" for shift handoff).
4. **Scan for metric language:** How they quantify problems — "FTE hours," "turnaround time," "days to discharge," etc.

**Output format (embed in email metadata as HTML comment):**

```html
<!-- LEXICON TABLE (extracted from transcript)
| Their Phrase | Generic Equivalent | Used By | Context |
|---|---|---|---|
| "physician burnout" | clinician fatigue | Dr. Chen | describing alert fatigue impact |
| "the cube" | analytics warehouse | IT Director | referring to existing reporting system |
| "morning huddle" | shift handoff meeting | Nurse Manager | describing real-time data needs |
| "Project Lighthouse" | data platform initiative | VP CIO | internal program name |
-->
```

**Override rule:** When the static HLS substitution table (Step 2) would produce a term that differs from the customer's actual words, the customer's words win. Example:
- Static table says: `Dashboard → Clinical Dashboard`
- Customer said: "the morning scorecard"
- Use: "the morning scorecard" (their words), not "Clinical Dashboard" (your substitution)

**Minimum extraction:** At least 3 entries. If the transcript yields fewer than 3, flag: `<!-- LEXICON: thin transcript — only [N] customer-specific terms extracted. Review for vocabulary accuracy. -->`

---

## Step 2c: Missing Skeptic Inference (MANDATORY for HLS)

After detecting meeting type (Step 1) and attendees (Step 2), compare the attendee list against the **Expected Roles** for that meeting type. If a predictably critical role is absent, the system must proactively address the gap.

### Expected Roles by Meeting Type

| Meeting Type | Expected Roles | If Missing → External Email Action | If Missing → Internal Email Flag |
|---|---|---|---|
| `discovery` | Business sponsor, technical lead | Add "Who else should be involved?" section | "⚠ Missing: [role] — AE should confirm decision process includes [role]" |
| `demo` | Champion, technical evaluator, business stakeholder | Include multi-value translation (IT/Clinical/Finance) to cover absent perspectives | "⚠ Missing: [role] — schedule dedicated session or provide written summary" |
| `architecture_review` | Architect, InfoSec/Security, Infrastructure/Ops | Add "Security & Data Residency" section if InfoSec absent; add "Operational Readiness" if Ops absent | "⚠ InfoSec not represented — champion needs to address data residency and compliance internally before next gate" |
| `poc_scoping` | Technical lead, business sponsor, data owner | Add explicit data ownership section if data owner absent | "⚠ Data owner not in room — risk of scope change when they engage" |
| `security_review` | CISO/InfoSec lead, compliance officer, legal | Add "Legal & Contractual" section if legal absent | "⚠ Legal not represented — BAA/DPA review may introduce new timeline" |
| `ebc` | C-suite sponsor, line-of-business VP | Add strategic initiative alignment if LOB VP absent | "⚠ LOB VP absent — executive alignment may not translate to operational prioritization" |
| `kickoff` | Project manager, technical lead, exec sponsor | Add "Executive Visibility" section if exec sponsor absent | "⚠ Exec sponsor not in kickoff — risk of deprioritization if competing initiatives arise" |

### Inference Logic

```
1. Map each attendee to a role category using:
   - Stakeholder profiles (People/clients/[name].md → title, role)
   - Title pattern matching from Step 2 seniority table
   - Transcript signals ("I'm from the security team", "I handle compliance")

2. Compare attendee roles against Expected Roles for the detected meeting type

3. For each MISSING expected role:
   a. External email: Add the corresponding section header + 2-3 sentences
      addressing that role's likely concerns. Frame as proactive helpfulness:
      "For your colleagues in [domain], here's a summary of how [topic]
      was addressed..."  — NOT "We noticed InfoSec wasn't present."
   b. Internal email: Add to a "Missing Stakeholder Gaps" section with
      the specific flag from the table above.

4. If ALL expected roles are represented: emit nothing (no false alarms).
```

**Critical rule:** The external email NEVER names the absent role or implies someone should have attended. It frames the additional section as helpful context for the champion to share internally. Only the internal email is explicit about the gap.

---

## Step 3: Generate External Email

### Universal Structure (All Meeting Types)

```
Subject: [Key Outcome] — [Account] / Databricks [Date]

[Greeting — 1 sentence, name the senior-most person first]

[BLUF — 1-2 sentences: What we accomplished and what happens next]

[What We Heard — 2-3 sentences reflecting THEIR priorities back to them.
 This is NOT what you presented. This is what THEY care about.
 Pull from key quotes and pain points detected in transcript.]

[What We Discussed — 3-5 sentences or short paragraphs.
 Organized by THEIR agenda items, not yours.
 Connect each topic to a business outcome, not a feature.]

[Decisions & Agreements — Only if decisions were made.
 Attributed to the decision-maker by name.
 "As Dr. Chen confirmed, the team will proceed with..." ]

[Next Steps — Numbered list, each with:
  - What (specific action)
  - Who (owner — name, not "your team")  
  - When (date or timeframe)
  Separate OUR commitments from THEIR commitments.]

[Collateral — If we promised to send materials:
  "As discussed, I'm attaching [X]. For [specific topic],
   I'll send [Y] separately by [date]."
  If nothing promised, omit this section entirely.]

[Close — 1 sentence. Forward-looking, not backward-looking.
 "Looking forward to [next specific interaction]."
 NOT "Thanks again for your time."

 For Discovery and Demo recaps, add a VALIDATION QUERY
 (Chris White, Six Habits of Highly Effective SEs):
 "Please let me know if I've captured this accurately
  or if I missed any nuance."
 This invites correction — if they reply to fix a minor
 detail, they've psychologically committed to the accuracy
 of everything else. The email becomes a shared document,
 not a vendor document.]

[Signature]
```

### Transformation Rule: So What? Outcome-Linking (MANDATORY)

Before finalizing any section of the external email, run the So What? recursive loop on every technical or capability statement:

```
FOR each sentence that mentions a product capability, feature, or technical action:
  1. Ask "So what?" → Does it connect to a STATED business outcome from the transcript?
  2. If YES → Append outcome-link: "[capability] — [so] your team can [outcome they described]"
  3. If NO stated outcome exists → Ask "So what?" again until you reach a plausible business impact
  4. If still no connection after 2 hops → Insert: <!-- SO-WHAT: [statement] — needs outcome link -->
     This flags the line for human review rather than publishing an orphaned feature reference.

EXAMPLES:
  ❌ "We demonstrated FHIR streaming into the lakehouse."
  ✓  "We demonstrated FHIR streaming into the lakehouse — addressing the manual
      reconciliation burden your team described, which currently consumes ~15 FTE hours/week."

  ❌ "The platform supports Unity Catalog for fine-grained access control."
  ✓  "Unity Catalog provides the row-level access controls Dr. Chen asked about,
      ensuring each department sees only their authorized patient cohorts."

VALIDATION: After drafting the full external email, count technical statements vs.
outcome-linked statements. Ratio must be ≥ 90% linked. If below, fix before proceeding.
```

This is the procedural enforcement of Design Principle #7. The principle says *why*; this rule says *how*.

---

### Design Principles (Apply to ALL Templates)

**1. Champion-Forwardable**
The email must read well to someone who WASN'T in the meeting. Your champion will forward this to their VP with "see below." If the email only makes sense with meeting context, it fails. Every section should be self-contained.

**2. Mirror Their Language**
Use the exact words they used to describe their problems, not your product vocabulary. If they said "we're drowning in manual chart reviews," don't translate that to "clinical workflow inefficiency." Their words resonate with their colleagues who also use those words.

**3. Decisions > Discussions**
"We discussed X" is weak. "We agreed to X" is strong. "Dr. Chen confirmed X" is strongest. Attribute decisions to specific people — it creates gentle accountability and makes the email feel like a record, not a diary.

**4. Asymmetric Next Steps**
Your commitments should be specific and dated. Their commitments should be softer — "your team mentioned providing..." not "you committed to delivering." You're holding yourself accountable while giving them room.

**5. No Selling in the Recap**
The meeting is over. The recap is not a chance to re-pitch. No feature lists, no ROI calculations, no competitive positioning. If you discussed those topics, reference them naturally: "We walked through how Lakebase handles the FHIR ingestion challenge you described." Don't re-argue the case.

**6. One Email, One CTA**
The email may have 5 next steps, but highlight ONE that matters most. "The most important next step is [X] by [date]." Everything else is supporting detail.

**7. The "So What?" Filter (John Care, Mastering Technical Sales)**
Never list features or capabilities in isolation. Every technical reference must pass the "So What?" test — keep asking "so what?" until you reach a business outcome. "We demonstrated the FHIR API" fails. "To address your integration cost concern, we demonstrated how the FHIR API automates patient data ingestion — reducing manual entry by an estimated 80%" passes. The email should read like a consulting report, not a feature list.

**8. Risk Transparency Builds Trust (John Care, Trusted Advisor SE)**
Counterintuitively, documenting a limitation increases the credibility of the positive claims. If every statement is positive, the buying committee's skepticism increases. Include an "Implementation Prerequisites" or "Open Items" section for architecture reviews and technical demos. Frame limitations as prerequisites, not defects: "This configuration requires [X] — we'll confirm availability during the security review." A document that reads "5 strengths and 1 specific prerequisite" is trusted more than one that reads "6 strengths."

**9. Write in the Buyer's Voice (Nate Nasralla, Fluint / DEEP-C)**
The follow-up email is not YOUR recap — it's the champion's draft internal memo. Write it so the champion can forward it without editing, or copy-paste sections into their own internal communication. This means: use neutral business voice, not vendor voice. Lead with the problem statement, not the solution. Focus on "the problem we are solving" before "how we solve it." Executives fund problems, not solutions. When a champion forwards your email with "see below — this captures it well," you've won.

**10. Pre-Empt the Skeptic (Gartner/CEB Consensus Research)**
If the meeting revealed a specific blocker or skeptic (e.g., "the CISO is concerned about data residency"), include a section that directly addresses that concern — even if the skeptic wasn't in the meeting. This arms the champion to say "I know you're worried about X; see the section below." The section header should name the concern domain, not the person: "Security & Data Residency Architecture" not "Addressing CISO Concerns."

**11. Cost of Inaction (Challenger Sale — Adamson & Dixon)**
For discovery and demo recaps, include a single sentence that reasserts why the status quo is untenable. This is not selling — it's reflecting back what THEY said. "As your team noted, maintaining the current manual reconciliation process continues to consume [X] FTE hours per month." This reminds the champion why they need to fight the internal battle for budget and priority.

### Meeting-Type Template Variations

#### Discovery Recap

**What changes:** Heavy on "What We Heard" (proving you listened). Light on "What We Discussed" (you didn't pitch yet). No "Decisions" section (too early). Next steps focus on scheduling the deeper dive. **Do not pitch the solution yet** — pitching too early signals you stopped listening.

**Primary framework:** SPICED (Jacco van der Kooij, Winning by Design)

**Subject pattern:** `Understanding [Their Initiative] — [Account] / Databricks Follow-Up`

**Key section — The SPICED Diagnosis (replaces generic "What We Heard"):**
```
Based on our conversation, here's my understanding of where things stand:

SITUATION: [Objective facts about their current state — systems,
  team structure, recent events like acquisitions or audits.
  Pull from transcript, not assumptions.]

PAIN: [Their subjective problem, in their exact words.
  "Your team described [X] as..." — attribute to specific people.]

IMPACT: [The rational AND emotional consequence.
  Quantify if they gave numbers: "$X in rework" or "Y hours/week."
  If they described frustration or risk, capture that too:
  "creating clinician fatigue" or "exposing the organization to
  audit findings."]

CRITICAL EVENT: [The deadline or forcing function, if one emerged.
  "Must be resolved before the Q3 EMR upgrade" or
  "Budget cycle closes in March."
  If no critical event surfaced, FLAG this in the internal email
  as "Missing Sales Signal — no compelling event identified."]

GOAL: [Their stated objective, in their words.
  "Your goal is to reduce [X] to [target] by [timeframe]."]

Please let me know if I've captured this accurately
or if I missed any nuance.
```

**Cost of Inaction line (include after IMPACT):**
```
As your team noted, maintaining the current [process/system]
continues to [consequence they described].
```

**Why SPICED works here:** The champion forwards this to their boss with "they actually understood our problem — this is exactly what we're dealing with." The boss reads a structured diagnosis, not a sales pitch. The missing SPICED bucket (if any) becomes an action item for the next meeting, not a gap in your credibility.

#### Demo Follow-Up

**What changes:** "What We Discussed" becomes "What We Showed & Why It Matters." Each demo topic ties back to a pain point from discovery. Include the "aha moment" if one was visible in the transcript. Structure is "Upside Down" (Cohan) — lead with the conclusion of value, not a chronological walkthrough.

**Primary framework:** Great Demo! (Peter Cohan) + Trusted Advisor (John Care)

**Subject pattern:** `[Capability] for [Their Use Case] — [Account] / Databricks Demo Recap`

**Key section — Executive Summary (The "Wow" — Cohan's Upside Down):**
```
Today we confirmed that [capability] can [outcome],
potentially [quantified impact if available].
```

**Key section — Capabilities Mapped to Challenges (The Table):**

Use a table format that the champion can scan in 10 seconds. Each row connects THEIR challenge (left) to what they SAW (middle) to proof (right). This is Cohan's "chunking" — organized by their mental model, not your demo script.

```
| Challenge You Described | What We Showed | Proof / Quote |
|---|---|---|
| [Pain point from discovery — in their words] | [Capability — framed as outcome, not feature] | [Key quote or metric from demo] |
| [Pain point 2] | [Capability 2 — "So What?" filtered] | [Quote or "Demonstrated live"] |
```

**Multi-Value Translation (Challenger — for forwardability):**

When the email will reach multiple stakeholder types (IT + Clinical + Finance), translate capabilities into value dialects:

```
[Capability] addresses three priorities your team raised:
- For clinical operations: [Clinical benefit — workflow, patient safety, time savings]
- For IT: [IT benefit — maintenance, security, integration simplicity]
- For finance: [Financial benefit — cost reduction, consolidation, efficiency]
```

**Implementation Prerequisites (John Care — risk transparency):**

If any limitations or prerequisites were discussed, surface them honestly. This section is OPTIONAL — only include if something came up.

```
Implementation Prerequisites:
- [Prerequisite 1 — framed as prerequisite, not defect.
  "This configuration requires [X] — we'll confirm
  availability during the architecture review."]
- [Prerequisite 2 — with next step to resolve]
```

**Parking Lot:**
```
We agreed to cover [topic] in the [next meeting type].
```

**Cost of Inaction line (before Next Steps):**
```
As [champion name] noted, continuing with [current state]
means [consequence they described in discovery].
```

**Collateral section (always include after demo):**
```
For reference, I'm attaching:
- [One-pager specific to their use case, if exists]
- [Architecture diagram discussed, if whiteboarded]

If any of your colleagues would like a walkthrough of what we
covered today, I'm happy to schedule a separate session.
```

**Why the last line matters:** You're explicitly enabling the champion to bring more stakeholders into the conversation without them having to ask.

#### Architecture Review Recap

**What changes:** Decisions section is CRITICAL — document what was agreed technically with attribution. Assumptions surfaced in structured table. Risk register for identified concerns. Diagrams referenced or attached. Open questions listed clearly.

**Primary framework:** Trusted Advisor (John Care) — Risk Transparency

**Subject pattern:** `Architecture Review: [Deployment Model / Component] for [Project] — [Account] / Databricks`

**Key section — Agreed Design (from process-notes 7d decisions):**
```
Based on today's discussion, we aligned on the following
architecture approach:

[Decision 1 — attributed to who confirmed it.
 "As [Name] confirmed, the team will proceed with [approach]
  to accommodate [their stated requirement]."]

[Decision 2 — same pattern.
 e.g., "FHIR resources ingested via structured streaming into
 Bronze layer, normalized to Delta in Silver — [Architect Name]
 validated this aligns with the existing data flow."]
```

**Key section — Assumptions & Dependencies (from process-notes 7e):**

Pull directly from `signal_type: assumption` entities. This is the highest-value section for architecture recaps.

```
This design is based on the following working assumptions.
Please flag any that don't match your environment:

| # | Assumption | Status | Verification Owner |
|---|-----------|--------|-------------------|
| 1 | Epic Clarity extract available as nightly batch | To Confirm | Customer IT |
| 2 | VPN access for Databricks workspace by Week 1 | To Confirm | Customer InfoSec |
| 3 | Unity Catalog supports existing LDAP group mapping | Confirmed ✓ | SA (Databricks) |
```

**Key section — Implementation Prerequisites / Risk Register (John Care):**

Include ONLY if limitations, prerequisites, or risks surfaced. Frame as engineering precision, not weakness. A document that reads "5 strengths and 1 prerequisite" is trusted more than "6 strengths."

```
Implementation Prerequisites:
- [Prerequisite]: [What's needed + next step.
  "VPN bandwidth to support real-time streaming — [Name]
  to confirm with network team by [date]."]
- [Risk identified]: [Mitigation.
  "Legacy system latency may impact batch window — fallback
  is [Y], which we'll validate in POC Week 1."]
```

**Key section — Open Questions:**
```
Items requiring follow-up before we finalize the design:
1. [Question — who owns the answer, by when]
2. [Question — who owns, by when]
```

**Close:** Validation query (White): "Please review the assumptions table above and let me know if any need correction — better to surface these now than during implementation."

**Why this template matters:** Architecture review recaps are the most commonly referenced emails in the deal cycle. They get forwarded to InfoSec, to infrastructure teams, to procurement. They become quasi-contractual. Precision here prevents scope creep and finger-pointing later.

#### POC Scope Confirmation

**What changes:** This is practically a contract — the most "legally adjacent" email the SA writes. Success criteria are numbered, measurable, and binary. Timeline has milestones. Data requirements are explicit with owners. This email often gets attached to an internal approval request or forwarded to procurement.

**Primary framework:** MEDDPICC (Decision Criteria) + Scientific Protocol

**Subject pattern:** `[Use Case] Pilot Scope & Success Criteria — [Account] / Databricks Confirmation`

**Key section — Objective:**
```
Objective: To validate that [capability] meets [their stated
requirement] within a [timeframe] evaluation period.
```

**Key section — Success Criteria (The "Exam Questions"):**

Criteria must be binary (pass/fail) or measurable (with thresholds). Vague criteria like "system performs well" will be rejected during review.

```
Based on our discussion, here are the proposed success
criteria for the [timeframe] pilot:

1. [Criterion 1 — measurable, binary.
   e.g., "FHIR bundle ingestion processing 10K bundles/hour
   with < 2% error rate"]
2. [Criterion 2 — specific.
   e.g., "PII detection accuracy > 99% on de-identified
   sample dataset"]
3. [Criterion 3 — business-meaningful.
   e.g., "Clinical dashboard loads in < 3 seconds with
   6 months of historical data"]
```

**Key section — Scope Boundaries (In vs. Out):**
```
Explicitly IN scope:
- [Item 1]
- [Item 2]

Explicitly OUT of scope:
- [Item 1 — e.g., "Custom API development"]
- [Item 2 — e.g., "Production data migration"]
```

**Key section — Timeline & Milestones:**
```
Proposed Timeline:
- Week 1: [Milestone — environment setup, data onboarding]
- Week 2: [Milestone — core use case validation]
- Week 3: [Milestone — includes go/no-go checkpoint]
- Week 4: [Milestone — readout and recommendation]

Decision Date: [Date — when the team will make go/no-go call]
```

**Key section — Requirements (bilateral):**
```
From your team:
- [Data artifact 1 — owner, deadline]
- [Access/credential 1 — owner, deadline]

From Databricks:
- [Environment detail — owner (SA), deadline]
- [Documentation — owner, deadline]
```

**Close:** "Please review these criteria and let me know if they accurately reflect what success looks like for your team. Once confirmed, I'll set up the environment and we can begin [start date]."

**Why "out of scope" matters:** Without explicit boundaries, POCs expand until they fail. The champion needs this list to defend the scope internally when colleagues add "just one more thing."

#### POC Checkpoint

**What changes:** Status against agreed criteria. Green/yellow/red on each criterion. Blockers surfaced with specific asks. Next session agenda pre-set.

**Subject pattern:** `[Use Case] Pilot — Week [N] Update — [Account] / Databricks`

#### Executive Briefing Recap

**What changes:** Shortest email. Business language ONLY — no product names, no technical details, no architecture. Strategic alignment emphasized. Forward-looking, focused on "why this matters for your organization's [initiative]."

**Primary framework:** Challenger Sale (Economic Buyer) + BLUF

**Subject pattern:** `Executive Summary: Strategic Alignment on [Initiative Name] — [Account] / Databricks`

**Key structure:**
```
[BLUF — 1-2 sentences connecting the discussion to their
strategic initiative. Use their initiative name, not your
product name.]

"Today's discussion confirmed alignment between [Vendor
capability — abstract, no product names] and [Client]'s
[year] [initiative name] initiative."

Strategic Context:
[1-2 sentences on what was discussed at the strategic level.
 "The conversation focused on how [abstract capability] can
 support [their stated goal], specifically around
 [business area they emphasized]."]

Value Realization:
[If quantification was discussed, state it.
 "Projected impact: $XM in [revenue recovery / cost reduction
 / time savings] within [timeframe]."
 If no numbers, state the qualitative value.
 "Enabling [their goal] while reducing [their stated risk]."]

Executive Asks:
[1-2 next steps, framed as peer-to-peer commitments.
 "[Their exec] to [action] by [timeframe]."
 "[Our exec sponsor] to [action] by [timeframe]."]
```

**Tone rules for EBC emails:**
- No product names — use "the platform" or "the proposed solution"
- No technical terms — no APIs, no SDKs, no architecture references
- No "we showed" or "we demonstrated" — this is a strategic conversation, not a demo
- Frame everything as organizational capability, not software features
- Peer-level tone — you're a strategic advisor, not a vendor reporting back
- Reference their strategic language — if they said "Digital Front Door," use that exact phrase

#### Security Review Recap

**What changes:** Compliance items documented with forensic precision. No casual language around regulatory topics. "As discussed" not "we agreed" (avoid creating contractual implications). Reference official documentation by name and version. Separate what's confirmed from what needs further investigation.

**Primary framework:** Trusted Advisor (Care) — applied to compliance domain

**Subject pattern:** `[Compliance Framework] Review Summary — [Account] / Databricks`

**Key structure:**
```
[BLUF — what was reviewed and overall outcome]

"Today we reviewed [Account]'s [compliance/security]
requirements against Databricks' current capabilities
and certifications."

Items Confirmed:
- [Compliance item 1 — reference official doc.
  "SOC 2 Type II report available — I'll send the
  current report under NDA via [secure method]."]
- [Compliance item 2 — precise language.
  "BAA execution supported for qualifying workloads
  on Databricks. Configuration details in
  [official doc name]."]

Items Requiring Follow-Up:
- [Open item 1 — who owns the answer, by when.
  "[Name] to confirm [specific configuration] with
  Databricks security team — target response by [date]."]
- [Open item 2 — same pattern]

Documentation to Be Provided:
- [Doc 1 — e.g., "Current SOC 2 Type II report (under NDA)"]
- [Doc 2 — e.g., "HITRUST inheritance matrix"]
- [Doc 3 — e.g., "Architecture security whitepaper"]
```

**Critical compliance language rules:**
- Never say "we are HIPAA compliant" → say "Databricks supports HIPAA-eligible configurations"
- Never say "we are HITRUST certified" without specifying scope → say "HITRUST CSF certification for [specific scope] — I'll confirm coverage for your use case"
- Never say "we agreed" → say "as discussed" (avoids contractual implications)
- Never reference PHI, patient data, or specific clinical information in email
- Always reference the official document/certification by name, not by paraphrase
- Frame limitations as investigation items: "I'll confirm whether [X] is supported in your specific deployment model" not "we don't support [X]"

**HLS-specific:** If the meeting involved HIPAA, BAA, or clinical data governance, include a Trust Signaling footer:

```
For reference, Databricks security and compliance
documentation is available at [official URL].
Our team is available to support your security
review process — please let me know if additional
documentation would be helpful.
```

#### Working Session / Office Hours Recap

**What changes:** Shortest, most tactical email. What was accomplished, what's left, what to prepare for next session. No strategic framing — these people are in the weeds and want efficiency.

**Subject pattern:** `[Topic] Working Session Notes — [Account] [Date]`

---

## Step 4: Generate Internal Email

The internal email goes to your AE, your manager, and optionally SE leadership. It is NEVER forwarded to the customer. This is where **Radical Candor** lives (Kim Scott). The external email requires diplomacy; the internal email requires truth.

### Sentiment Routing (from Gemini research)

The system should use transcript signals to route content:
- **High agreement / consensus markers** → External email (amplify alignment)
- **High conflict / objection / skepticism** → Internal email (flag for strategy)
- **Ambiguous consensus** ("we'll think about it", "interesting") → Internal email with "Ambiguous Consensus" flag for human review

### Structure

```
Subject: [Account] — [Meeting Type] Debrief [Date]

Deal Health: [GREEN / YELLOW / RED]

TL;DR: [2-3 sentences — what happened, what it means for the deal]

What Went Well:
- [Positive signal 1 — attributed]
- [Positive signal 2]

Concerns:
- [Risk 1 — severity, what it means]
- [Risk 2]
- [Competitive mention if any — what was said, by whom]

MEDPICC Update:
  M: [Metrics — any new quantification of business impact?]
  E: [Economic Buyer — identified? Engaged? Absent?]
  D: [Decision Criteria — what are they evaluating on?]
  D: [Decision Process — what's their internal process? Timeline?]
  I: [Identify Pain — what hurts? How much?]
  P: [Paper Process — procurement, legal, security review status]
  C: [Champion — who? How strong? Can they mobilize?]
  C: [Competition — who else? Where are they in eval?]
  [Only update fields with new information from THIS meeting.
   Mark unchanged fields with "—" not "no update"]

  ⚠️ Missing Signals:
  [Flag any MEDPICC field AND any SPICED bucket that remains
   empty after this meeting. For discovery calls especially,
   flag missing Critical Event ("No compelling event identified
   — AE needs to create urgency") or missing Economic Buyer
   ("We have not reached the budget holder — blocked at
   Director level"). These are strategic gaps, not form fields.]

Political Dynamics Observed:
- [Who deferred to whom? Who had final say?]
- [Who was engaged vs checked out?]
- [Any new stakeholders mentioned but not present?
  "Dr. Chen referenced 'our VP of Clinical Informatics'
  twice — we need to understand this person's role."]
- [Body language / tone / energy shifts during specific topics]
- [Internal misalignment observed?
  "The Director of Infrastructure and Clinical Lead appear
  to have different priorities — Infrastructure is focused
  on maintenance burden while Clinical wants speed."]

Champion Assessment (Honest):
- Champion: [Name]
- Strength: [STRONG / ADEQUATE / WEAK / ABSENT]
- Evidence: [What they did or didn't do that reveals strength.
  "Forwarded our last recap to their VP within 2 hours" = STRONG.
  "Agreed with everything but offered no internal path forward" = WEAK.
  "Talker, not a Mobilizer" = flag for AE to find real champion.]
- [If champion is a "Talker" not a "Mobilizer" (Challenger Sale),
  say so explicitly. Talkers share information freely but lack
  influence. Mobilizers spend political capital.]

Recommended Next Moves:
1. [Action for AE — e.g., "Get exec sponsor meeting scheduled before
   their budget cycle closes in March"]
2. [Action for SA — e.g., "Build POC environment by Friday,
   need customer data by Wednesday"]
3. [Escalation if needed — e.g., "Need RVP air cover for the
   procurement timeline push"]

Collateral Sent to Customer:
- [List what was sent in the external email]
- [Note anything we promised but haven't sent yet — with deadlines]
```

### What Goes Here That NEVER Goes in the External Email

- Deal health assessment (RED/YELLOW/GREEN)
- Political dynamics and stakeholder reading
- Competitive intelligence and positioning strategy
- Internal resource requests or escalations
- Honest assessment of champion strength
- Pricing/packaging strategy considerations
- "They said X but I think they actually mean Y"

---

## Step 4b: Post-Generation Anti-Pattern Scan (MANDATORY)

After both emails are drafted (Steps 3 + 4) but BEFORE saving output files, run this structured scan. Every check is pass/fail. Any FAIL triggers an auto-fix cycle (max 2 attempts; if still failing, save with `<!-- WARNING: [pattern] detected — human review required -->`).

### Scan Checklist

```
ANTI-PATTERN SCAN:

  1. HAPPY TALK:
     Count instances of: excited, great, amazing, thrilled, fantastic, wonderful
     PASS: ≤ 2 instances across both emails
     FAIL: > 2 → Replace with: productive, confirmed, validated, aligned
     Result: [PASS | FAIL → fixed | FAIL → flagged]

  2. FEATURE DUMP:
     Count technical statements without outcome-links (from So What? rule)
     PASS: ≥ 90% of technical statements have outcome-links
     FAIL: < 90% → Apply So What? loop to unlinked statements
     Result: [PASS | FAIL → fixed | FAIL → flagged]

  3. VENDOR VOICE:
     Scan for: "Our platform", "We provide", "We offer", "Our solution delivers",
     "Databricks enables" (without customer framing)
     PASS: 0 instances in external email
     FAIL: > 0 → Rewrite in buyer voice: "Your team would be able to..."
     Result: [PASS | FAIL → fixed | FAIL → flagged]

  4. WALL OF TEXT:
     Check each section for > 150 words without a visual break
     (bold text, table, bullet list, or blockquote)
     PASS: All sections have visual breaks within 150-word spans
     FAIL: > 150 words without break → Add formatting
     Result: [PASS | FAIL → fixed | FAIL → flagged]

  5. LEXICON DRIFT:
     Compare draft vocabulary against the Lexicon Table (Step 2b)
     PASS: All customer-specific terms from lexicon used correctly
     FAIL: Generic term used where customer's exact phrase exists → Swap
     Result: [PASS | FAIL → fixed | FAIL → flagged]

  6. ORPHANED COMMITMENTS:
     Cross-check: every action item from session appears in Next Steps
     PASS: All action items accounted for (external or internal)
     FAIL: Missing action item → Add to appropriate email
     Result: [PASS | FAIL → fixed | FAIL → flagged]

  7. INTERNAL LEAK:
     Scan external email for: deal health, champion assessment, competitive
     strategy, pricing, "they actually mean", political dynamics language
     PASS: 0 internal-only content in external email
     FAIL: > 0 → Remove immediately (CRITICAL — no auto-fix, must delete)
     Result: [PASS | FAIL → removed]
```

### HLS-Specific Scans (run ONLY for healthcare accounts)

```
  8. PHI DETECTION:
     Regex scan for:
       - MRN patterns: /\b(MRN|mrn)[:\s#]*\d{4,}/
       - SSN patterns: /\b\d{3}-\d{2}-\d{4}\b/
       - DOB patterns: /\b(DOB|dob|Date of Birth)[:\s]*\d/
       - Patient names with clinical context: /\b(patient|pt)\s+[A-Z][a-z]+/
       - Specific diagnosis + person: /\b(diagnosed|diagnosis|dx)\b.*\b[A-Z][a-z]+\b/
       - Any of the 18 HIPAA identifiers referenced with specific values
     PASS: 0 matches
     FAIL: ANY match → Remove immediately (CRITICAL — non-negotiable)
     Result: [PASS | FAIL → removed]

  9. COMPLIANCE LANGUAGE:
     Scan for promissory compliance statements:
       - "we are HIPAA compliant" (should be "supports HIPAA-eligible configurations")
       - "we are HITRUST certified" without scope (should specify scope)
       - "we guarantee" + security/compliance term
       - "we agreed" in security context (should be "as discussed")
     PASS: 0 promissory statements
     FAIL: > 0 → Rewrite to capability language with official doc reference
     Result: [PASS | FAIL → fixed | FAIL → flagged]

  10. PREMATURE COMMERCIAL:
      Scan external email for: pricing, discount, contract terms, licensing,
      "per DBU", "$", cost estimate, quote
      PASS: 0 commercial references in technical recap
      FAIL: > 0 → Remove (SA swim lane violation)
      Result: [PASS | FAIL → removed]
```

### Scan Output

```
ANTI-PATTERN SCAN RESULTS:
  Total checks:     [7 standard + 3 HLS if applicable]
  Passed:           [N]
  Auto-fixed:       [N] → [list which patterns were fixed]
  Flagged (review): [N] → [list which patterns need human review]
  Critical removed: [N] → [list what was removed]

  GATE: [PASS — clean draft | PASS WITH FLAGS — review items noted | BLOCKED — critical issue]
```

If BLOCKED (critical issue in checks 7, 8, or 10), do NOT save the output. Fix and re-scan.

---

## Step 4c: Leave-Behind Assessment (CONDITIONAL)

After both emails pass the anti-pattern scan, assess whether this meeting warrants a **one-pager leave-behind** — a forwarding-optimized document the champion can share with stakeholders who weren't in the room.

### Trigger Matrix

| Meeting Type | Trigger Condition | One-Pager Variant | Priority |
|---|---|---|---|
| `discovery` | ≥3 distinct pain points surfaced in transcript | `consideration` | medium |
| `demo` | "Aha moment" detected (explicit positive reaction to capability) | `validation` | high |
| `architecture_review` | ≥2 architectural decisions made or confirmed | `validation` | high |
| `ebc` | Executive attendee present (VP+ from seniority detection) | `champion` | critical |
| `security_review` | Compliance requirements discussed (HIPAA, BAA, ZDR) | `validation` | medium |
| `poc_scoping` | POC scope, timeline, or success criteria agreed | `validation` | high |
| `kickoff` | Roles and milestones agreed | `awareness` | low |

### Assessment Logic

```
1. Check meeting_type (from Step 1) against Trigger Matrix
2. If meeting_type matches:
   a. Evaluate trigger condition against transcript/session content
   b. If condition MET:
      - Set leave_behind_recommended = true
      - Record: variant_type, priority, hero_message_seed (from transcript's strongest outcome)
   c. If condition NOT MET:
      - Set leave_behind_recommended = false
      - No action

3. If leave_behind_recommended:
   a. Add to EXTERNAL email's closing section (BEFORE the sign-off):
      "I'm preparing a summary document covering [key topic] from our discussion.
       I'll send it separately — feel free to share with [missing stakeholder roles]."
   b. Add to INTERNAL email's "Recommended Actions" section:
      "📄 Leave-behind recommended: [variant_type] one-pager
       Hero message seed: '[strongest outcome from transcript]'
       Target audience: [missing stakeholder roles from Step 2c]
       Priority: [priority]"

4. If running inside /orchestrate pipeline:
   Queue a leave_behind sub-item to _System/queue/pending/:
   {
     "schema_version": "1.0",
     "source_channel": "transcript_sub_item",
     "source_id": "sub:{parent_filename}:leave_behind",
     "parent_item_id": "{parent_queue_item_id}",
     "timestamp": "{session_timestamp}",
     "account": "{account}",
     "priority": "{priority from matrix}",
     "content": {
       "summary": "Generate {variant_type} one-pager: {hero_message_seed}",
       "body_ref": null,
       "raw_text": null
     },
     "metadata": {
       "parent_session": "Sessions/{account}/{type}/{date}.md",
       "pre_classified": true,
       "category": "deliverable_request",
       "artifact_type": "one-pager",
       "one_pager_variant": "{variant_type}",
       "hero_message_seed": "{hero_message_seed}",
       "target_stakeholders": ["{missing roles}"],
       "extraction_source": "draft-followup-leave-behind-assessment"
     }
   }

5. If NOT running inside /orchestrate (manual invocation):
   Suggest to user: "This meeting warrants a [variant_type] one-pager.
   Run: /build one-pager (or let /orchestrate pick it up on next cycle)"
```

### Skip Conditions (do NOT recommend leave-behind)

- `general_update` or `kickoff` with no decisions made
- Meeting was entirely internal (no external attendees)
- Session already has an artifact linked in frontmatter (`artifact:` field populated)
- Same variant already generated for this account in the last 14 days (check `Artifacts/` for existing one-pagers)

**Queue routing (Phase D):**
- If `_meta.board_dir` is present: leave-behind items are captured in `board/draft-followup-output.yaml` under `leave_behind_details`. The post-meeting coordinator reads this and decides whether to invoke one-pager-render. Do NOT write to `_System/queue/pending/`.
- If `_meta.board_dir` is absent: write to `_System/queue/pending/` as before (standalone mode).

---

## Step 5: Generate Output Files

### File Naming

```
~/obsidian/sa-intel/Sessions/[Account]/[type]/emails/
  [YYYY-MM-DD]_external.html
  [YYYY-MM-DD]_external.md
  [YYYY-MM-DD]_internal.html
  [YYYY-MM-DD]_internal.md
```

### HTML Format (Gmail-Ready)

Generate clean HTML that renders properly when pasted into Gmail compose:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
        Roboto, 'Helvetica Neue', Arial, sans-serif;
      font-size: 14px;
      line-height: 1.6;
      color: #202124;
      max-width: 680px;
      margin: 0 auto;
      padding: 20px;
    }
    .subject-line {
      background: #f8f9fa;
      border-left: 4px solid #1a73e8;
      padding: 12px 16px;
      margin-bottom: 24px;
      font-weight: 600;
      font-size: 15px;
    }
    .section-label {
      font-weight: 600;
      color: #444746;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-top: 20px;
      margin-bottom: 4px;
    }
    .next-steps ol {
      padding-left: 20px;
    }
    .next-steps li {
      margin-bottom: 8px;
    }
    .owner {
      font-weight: 600;
    }
    .date {
      color: #0b57a4;
      font-weight: 500;
    }
    .collateral {
      background: #f1f3f4;
      border-radius: 8px;
      padding: 12px 16px;
      margin-top: 16px;
    }
    .metadata {
      color: #444746;
      font-size: 12px;
      border-top: 1px solid #e8eaed;
      margin-top: 24px;
      padding-top: 12px;
    }
    /* Internal email specific */
    .deal-health {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 4px;
      font-weight: 700;
      font-size: 13px;
    }
    .deal-health.green { background: #e6f4ea; color: #0d5626; }
    .deal-health.yellow { background: #fef7e0; color: #7a4100; }
    .deal-health.red { background: #fce8e6; color: #9c1b18; }
    .medpicc-grid {
      display: grid;
      grid-template-columns: 40px 1fr;
      gap: 4px 12px;
      margin: 12px 0;
    }
    .medpicc-label {
      font-weight: 700;
      color: #444746;
    }
  </style>
</head>
<body>

  <div class="subject-line">
    Subject: {{subject}}
  </div>

  <!-- EMAIL BODY HERE -->
  <!-- Rendered per template type -->

  <div class="metadata">
    <em>Generated from session: {{session_path}}</em><br>
    <em>Meeting date: {{date}} | Type: {{meeting_type}}</em><br>
    <em>Draft — review before sending</em>
  </div>

</body>
</html>
```

### Markdown Format (Vault Reference)

Standard markdown with YAML frontmatter:

```yaml
---
type: follow_up_email
variant: external | internal
session: Sessions/[Account]/[type]/[date].md
account: "[Account]"
meeting_type: "[type]"
audience_tier: "[executive|director|manager|individual]"
generated: [YYYY-MM-DD]
status: draft
---
```

### Email Index File

After generating, append to an index for quick visual scanning:

```
~/obsidian/sa-intel/_System/email-queue.md
```

```markdown
## Email Queue

| Date | Account | Type | External | Internal | Status |
|------|---------|------|----------|----------|--------|
| 2026-01-21 | CHLA | architecture_review | [ext](../Sessions/CHLA/customer/emails/2026-01-21_external.html) | [int](../Sessions/CHLA/customer/emails/2026-01-21_internal.html) | ⏳ Draft |
| 2026-01-20 | Providence | discovery | [ext](...) | [int](...) | ✅ Sent |
```

---

## Step 5a: Board Write Protocol (Coordinated Mode)

**Only when `_meta.board_dir` is present.** Execute this AFTER generating output files (Step 5) and BEFORE symlinking (Step 5b).

Write a board entry to `{board_dir}/board/draft-followup-output.yaml`:

```yaml
skill_name: "draft-followup"
invoked_at: "{ISO 8601 timestamp}"
invoked_by: "{coordinator name from _meta.coordinator}"

artifact_path: "{absolute path to Sessions/[Account]/[type]/emails/ directory}"
artifact_type: "email"

# What the skill produced
external_emails_drafted:
  - recipient_group: "{attendees_customer names}"
    subject: "{subject line}"
    meeting_type: "{discovery|demo|architecture_review|poc_scoping|etc.}"
    audience_tier: "{executive|director|manager|individual}"
    word_count: N
    file_path: "{absolute path to external .html}"
internal_emails_drafted:
  - recipient_group: "{AE + manager names}"
    subject: "{subject line}"
    deal_health: "{GREEN|YELLOW|RED}"
    file_path: "{absolute path to internal .html}"

# Leave-behind assessment (from Step 4c)
leave_behind_recommended: true/false
leave_behind_details:
  variant_type: "{consideration|validation|champion|etc.}"
  hero_message_seed: "{strongest outcome from transcript}"
  target_stakeholders: []
  priority: "{critical|high|medium|low}"

# Extracted intelligence (for downstream skills to consume)
action_items_from_session:
  - action: "{action item text}"
    owner: "{name or 'us'/'them'}"
    due: "{date or 'TBD'}"
    covered_in_email: true/false
open_questions_from_session:
  - question: "{question text}"
    asked_by: "{name}"
    needs_research: true/false
commitments_from_session:
  - commitment: "{text}"
    direction: "{ours_to_them|theirs_to_us}"
    owner: "{name}"

# Quality from existing 12-criterion Forward Test
quality_score: N                        # total from rubric (0-24)
quality_max: 24
quality_pass: true/false                # >= 18
quality_notes: ""

# Anti-patterns detected (from Step 4b scan)
anti_patterns_detected: []              # list from scan results

# Amendments
strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []

recommendations_for_downstream:
  - target_skill: "email-render"
    recommendation: "{e.g., 'action item X needs a dedicated deliverable email — not covered in recap'}"
    priority: "high"
```

Use the Write tool to create this file. If the file already exists (retry scenario), overwrite it.

**Board entry is canonical.** When `_meta.board_dir` is present, write ONLY the board entry. Do NOT write to `_System/queue/pending/` or `_System/email-queue.md` — these legacy paths are deprecated.

The `/orchestrate` pipeline reads from the board directory (`.pipeline/post-meeting/board/draft-followup-output.yaml`) instead of `_System/queue/pending/`.

**If `_meta.board_dir` is absent** — standalone mode. Write to `_System/queue/pending/` and `_System/email-queue.md` as before. Standalone behavior is unchanged.

---

## Step 5b: Symlink to Customer Folder

After saving email files, symlink the external email (HTML + MD) into `~/Customer/[account]/01-Emails/` so it's accessible from Finder organized by account. The vault file remains the source of truth.

**Account name mapping:** spaces → underscores (e.g., "Mayo Clinic" → "Mayo_Clinic").

```bash
# Create account folder structure if it doesn't exist
for sub in 01-Emails 02-Decks 03-Reference_Docs 04-Notebooks 05-Proposals 06-Meeting_Prep 07-Contracts_Legal 08-Screenshots; do
  mkdir -p ~/Customer/[account_folder]/$sub
done

# Symlink both external email formats
ln -sf ~/obsidian/sa-intel/Sessions/[Account]/[type]/emails/[YYYY-MM-DD]_external.html ~/Customer/[account_folder]/01-Emails/[YYYY-MM-DD]_external.html
ln -sf ~/obsidian/sa-intel/Sessions/[Account]/[type]/emails/[YYYY-MM-DD]_external.md ~/Customer/[account_folder]/01-Emails/[YYYY-MM-DD]_external.md
```

- Use `-sf` (force) to overwrite stale symlinks if re-generating
- Always use full absolute paths in the symlink target
- Only symlink external emails — internal emails stay vault-only

---

## Step 6: Integration with process-transcript

### Automatic Invocation

After `/process-transcript` completes Step 6 (Output Report), it should automatically invoke this skill:

```
## Post-Meeting Queue

### 🔴 Follow-Up Emails (DRAFTED)

**External email:** [Open in browser →](file:///path/to/external.html)
  To: [attendees_customer emails]
  CC: [AE]
  Subject: {{subject}}
  Status: ⏳ Ready for review

**Internal email:** [Open in browser →](file:///path/to/internal.html)
  To: [AE email]
  CC: [Manager email]
  Subject: {{subject}}  
  Status: ⏳ Ready for review

➡ Review → Copy to Gmail → Send
```

### No Approval Gate

The emails are DRAFTED, not SENT. The human reviews them in the browser (or in the vault), copies to Gmail, and sends. There is no "approve to generate" step — the generation happens automatically because:

1. Every meeting needs a follow-up email (100% frequency)
2. The structured data is already extracted (zero additional input needed)
3. A draft that needs editing is faster than writing from scratch
4. The worst case is you delete the draft (no harm done)

---

## Quality Rules

### Core Rules

1. **Never invent information.** Every claim in the email must trace to transcript data. If something is ambiguous, omit it or flag it with `<!-- VERIFY: [what needs checking] -->` in the HTML.

2. **Never state compliance as fact.** Use "Databricks supports X — I'll confirm the specific configuration" not "we are X certified."

3. **Mirror their language.** If they said "patient journey," don't write "clinical pathway." Check key quotes for their exact vocabulary.

4. **Attribute decisions to people.** "As Dr. Chen noted..." creates accountability. "We discussed..." creates ambiguity.

5. **Your commitments: specific dates. Their commitments: softer framing.** You hold yourself accountable; you give them graceful room.

6. **No selling in the recap.** No feature lists. No ROI calculations. No competitive positioning. The meeting is over.

7. **Executive > tactical.** When in doubt, write for the most senior person who will read this email (including forwards).

8. **Internal email: be honest.** The internal email is where you say "the champion is weak" or "they're also talking to Snowflake." Never sugarcoat for your AE.

### HLS Compliance Rules (Healthcare Accounts)

9. **Zero PHI.** Never include Protected Health Information — no patient names, MRNs, SSNs, DOBs, specific diagnosis details, or any of the 18 HIPAA identifiers. "We discussed the imaging workflow for the patient cohort" not "We discussed the MRI results for patient John Doe." Scan for PHI patterns before generating output.

10. **Compliance references: factual, not promissory.** Reference SOC2, HITRUST, BAA readiness as capabilities available, not as contractual guarantees. "Databricks supports BAA execution for qualifying workloads — I'll confirm the specific configuration for your environment" not "We're HIPAA compliant for this use case."

11. **No premature commercial language.** Never reference pricing, discounts, contract terms, or licensing in a technical recap. Strict swim lanes: SA handles technical/business fit, AE handles commercials. Mixing them dilutes Trusted Advisor status (John Care).

### Anti-Pattern Detection

The system must scan generated drafts for these patterns and auto-fix:

| Anti-Pattern | Detection Signal | Fix |
|---|---|---|
| **"Just Checking In"** | Opening with "checking in", "following up", "touching base" with no new content | Every email must provide new value — a structured recap IS the value |
| **"Attachment Grenade"** | Multiple attachments without per-attachment context | Each attachment must have a sentence explaining why it's relevant to THIS conversation: "I've attached the architecture diagram specifically to address [Name]'s question about [topic]" |
| **"Happy Talk Overload"** | >2 instances of "excited", "great", "amazing", "thrilled" | Replace with neutral professional language: "productive", "insightful", "confirmed", "validated" |
| **"Feature Dump"** | Capabilities listed without connecting to customer pain | Apply "So What?" filter — every capability must link to a stated business outcome |
| **"Wall of Text"** | Any section >150 words without a visual break | Add formatting: bold key metrics, use the table format for multi-item comparisons, add whitespace |
| **Vendor Voice** | "Our platform delivers..." / "We provide..." / product marketing language | Rewrite in neutral business voice: "The platform enables..." or better, frame from their perspective: "Your team would be able to..." |

---

## Evaluation — The "Forward Test"

Score each generated email 0-2 on these criteria:

| # | Criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | **Champion-Forwardable** | Only makes sense if you were in the meeting | Mostly self-contained | A stranger on the buying committee could read this and understand the situation, the value, and the next step. Missing Skeptic sections (Step 2c) arm champion for absent stakeholders. |
| 2 | **Their Language** | Uses vendor vocabulary ("our platform delivers") | Mixes vendor and customer terms | Mirrors exact words from Lexicon Table (Step 2b), written in neutral business voice (Nasralla buyer-voice principle). Scan #5 (Lexicon Drift) passes. |
| 3 | **Decisions Attributed** | "We discussed" | Some attribution | Every decision tied to a named person: "As Dr. Chen confirmed..." |
| 4 | **Next Steps Actionable** | Vague ("follow up soon") | Has actions but missing owners or dates | Every step has what + who + when, with ONE highlighted as most important |
| 5 | **Tone Match** | Too casual or too formal for the audience | Mostly right | Perfect register for the seniority tier — vocabulary matches mental model (Domain 4) |
| 6 | **No Selling** | Re-pitches in the recap, feature lists | Subtle product promotion or vendor voice | Zero selling — pure service. Reads like consulting, not marketing |
| 7 | **Length Appropriate** | Too long to read on mobile (>400 words for discovery/EBC) | Reasonable but could be tighter | Scannable in 60 seconds. Key metrics bolded. Whitespace between sections |
| 8 | **Internal Email Honest** | Sugarcoated or missing political intel | Partially candid — flags risks but hedges | Brutally honest: champion strength assessed, missing MEDPICC fields flagged, competitive intel included |
| 9 | **"So What?" Filtered (Care)** | Features listed without business connection | Some features connected to outcomes | Every technical reference has outcome-link (Step 3 transformation rule). Scan #2 (Feature Dump) passes at ≥90%. |
| 10 | **Risk Transparency (Care)** | Limitations buried or omitted | Limitations acknowledged vaguely | Prerequisites/limitations in dedicated section, framed constructively, with next step to resolve |
| 11 | **Zero PHI (HLS only)** | Contains identifiable patient information | Contains borderline references (specific department + condition) | No PHI, no identifying clinical details. Scan #8 (PHI Detection) passes. Scan #9 (Compliance Language) passes. |
| 12 | **Anti-Pattern Free** | Contains 2+ anti-patterns (happy talk, feature dump, wall of text, vendor voice) | Contains 1 minor anti-pattern | Step 4b scan passes all checks. Zero flags, zero critical removals. |

**Pass: 18/24.** Below 18 → revise before sending. For HLS accounts, criterion #11 must score 2 (non-negotiable).

---

## Research Foundations

This skill's design principles are grounded in the following expert frameworks, synthesized from Gemini Deep Research (Feb 2026):

| Principle | Source | Key Concept |
|---|---|---|
| "So What?" filter — features → outcomes | John Care, *Mastering Technical Sales* | Trusted Advisor paradigm |
| Risk transparency builds trust | John Care, *Trusted Advisor SE* | Document limitations to increase credibility |
| Upside-down structure — lead with conclusion | Peter Cohan, *Great Demo!* | Start with the "Wow," not the walkthrough |
| Use Case 5 — arm the champion | Peter Cohan, *Great Demo!* | Demo designed for internal selling |
| Validation query close — invite correction | Chris White, *Six Habits of Highly Effective SEs* | Co-authorship effect |
| SPICED diagnosis for discovery | Jacco van der Kooij, *Winning by Design* | Situation → Pain → Impact → Critical Event → Decision |
| Buyer-voice narrative memo | Nate Nasralla, *Fluint / DEEP-C* | Write so champion can forward without editing |
| Mobilizer vs. Talker distinction | Brent Adamson & Matt Dixon, *Challenger Sale* | Mobilizers spend political capital; Talkers don't |
| Multi-value translation (Finance/IT/Clinical) | Challenger Sale | Same capability → multiple value dialects |
| Cost of Inaction reassertion | Challenger Sale | Remind champion why status quo is untenable |
| Pre-empt the skeptic's objections | Gartner/CEB consensus research | Arm champion to address blocker before asked |
| Audience seniority vocabulary ladder | Domain 4 synthesis (multiple sources) | C-suite: ROI/governance. IC: APIs/configs. |
| Zero PHI, compliance-as-capability | HIPAA Journal, HLS sales literature | Never promissory; always reference official docs |
| Anti-patterns: 5 email killers | Nasralla (Fluint), GTMnow, CEB | Just Checking In, Attachment Grenade, Happy Talk, Feature Dump, Premature Commercial |

---

## Relationship to email-render and Philosophy

This skill is the **post-meeting rendering specialist**. It sits within a broader email generation system:

```
_System/prompts/email-drafting-philosophy.md  ← Operating system (principles, tone, quality gates)
    │
    ├── email-render skill                    ← Action-thread emails (Types 1-9)
    │   Short markdown drafts → Artifacts/Emails/
    │   Deliverables, research answers, intros, nudges, scheduling, etc.
    │
    └── draft-followup skill (THIS)           ← Session recap emails
        External + internal HTML → Sessions/[account]/[type]/emails/
        Meeting-type templates, MEDPICC, champion assessment, seniority ladder
```

### What This Skill Owns (draft-followup only)
- Meeting-type detection and template selection (10 types)
- External recap emails with deep structural guidance per meeting type
- Internal debrief emails with MEDPICC, political dynamics, champion assessment
- 4-tier seniority vocabulary ladder with HLS substitutions
- HTML rendering for Gmail copy-paste
- 12-criterion Forward Test scoring rubric
- HLS compliance language rules

### What the Philosophy Governs (shared)
- Core principles (BLUF, Draft Don't Send, One Email per Thread, etc.)
- Tone calibration by relationship depth and recipient type
- Signature ("Samuel"), opening format (first name + em dash)
- Quality gates (no internal leaks, no wiki-links, forwardable)
- Anti-patterns (no "just checking in", no feature dumps, etc.)

### What email-render Handles (not this skill)
- Action-thread emails between meetings (Types 2-9)
- Nudge/check-in with account-configurable thresholds
- Insight shares, reactive responses, decline/redirect
- Automation pipeline integration with `/today` and `/follow-ups`
- Prep notes schema with 8 standardized sections

---

## Dependencies

| Tool | Purpose | Required? |
|------|---------|-----------|
| Obsidian vault access | Read session, stakeholder, account files | Yes |
| entities.jsonl | Read MEDPICC signals, action items | Yes |
| Speaker alias files | Map speakers to names | Yes (via process-transcript) |
| HTML rendering | Gmail-ready output | Yes |

$ARGUMENTS
