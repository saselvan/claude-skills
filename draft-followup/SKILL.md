---
name: draft-followup
description: "Draft post-meeting follow-up emails as proposals with written commitments. Generates external email (proposal for next steps) + internal email (deal health assessment). USE WHEN: user says 'draft followup' or auto-triggered by /post-meeting. Takes session file + optional coaching-flags input. Produces external + internal email pairs as HTML + MD."
allowed-tools: Read, Write, Bash, Task, Glob, Grep, mcp__glean__*
---

# Follow-Up Email Render (Redesigned: Proposal Framework)

Draft post-meeting follow-up emails as **proposals with written commitments**, not passive recaps.

## Core Philosophy

A follow-up email is **bilateral commitment documentation** — not recap, not feature list.

- **External email**: Proposal for next steps with mutual commitments, success criteria, and transparent assumptions
- **Internal email**: Deal health assessment (commitment reliability, vague language decoded, blockers, champion strength)

Both informed by psychology: Cialdini (written commitments stick), Kahneman/Tversky (specificity beats vagueness), Challenger Sale (confidence in execution).

---

## Usage

```bash
/draft-followup                                    # Uses most recent session
/draft-followup Sessions/nwm/customer/2026-04-18.md   # Specific session
/draft-followup --dry-run                          # Preview without writing
```

---

## Process (9 Steps)

### Step 0: Commitment Extraction & Classification

Parse the session for all commitments (spoken, implied, inferred). Classify into 8 categories with confidence scoring.

#### 8 Commitment Categories

| Category | Definition | Language Markers | Confidence |
|---|---|---|---|
| **OUR-COMMITMENT** | We explicitly committed to deliver/own | "We will...", "I'll...", "Let's..." | HIGH (explicit) / MEDIUM (affirmative + action) / LOW (implied) |
| **THEIR-COMMITMENT** | Customer explicitly committed | "We'll...", "We commit to...", "Count on us..." | HIGH / MEDIUM / LOW |
| **DECISION** | Someone committed to decide by date | "We'll decide by Q3", "Next week decision makers align" | HIGH (named + date) / MEDIUM (decision + soft date) / TENTATIVE (under discussion) |
| **OPEN-QUESTION** | Explicitly deferred, awaiting answer | "We need to validate that", "Revisit next meeting" | MEDIUM (deferred) / LOW (implied) |
| **DEFERRED** | Acknowledged but explicitly postponed | "Not in Phase 1", "That's Phase 2" | HIGH (explicit boundary) |
| **DEPENDENCY** | Our action depends on their action | "Once you provide access, we'll..." | HIGH (condition stated) / MEDIUM (implied) |
| **AT-RISK** | Commitment exists but low confidence | "We might...", "Depending on budget..." | TENTATIVE (explicitly uncertain) |
| **VAGUE-COMMITMENT** | Stated but lacks specificity | "We'll get you options", "We'll follow up soon" | LOW (no WHO/WHAT/WHEN) |

#### Extraction Process

1. **Scan transcript** for commitment language: "will", "commit", "agreed", "promised", "let's", "by [date]"
2. **Classify** into one of 8 categories
3. **Score confidence**: HIGH / MEDIUM / LOW / TENTATIVE
4. **Extract WHO/WHAT/WHEN** for each
5. **Output: Commitments Matrix**

---

### Step 0.5: Send/Skip Triage

**Not every meeting requires a follow-up email.** Decide whether to send using three factors:

| Factor | Score | How to Calculate |
|---|---|---|
| **Commitment Weight** | 0-3 | HIGH/MEDIUM = 3 pts each; TENTATIVE = 1 pt; cap at 3 |
| **Follow-Up Significance** | 0-3 | Research we own (3), Blockers to remove (3), Proof to deliver (2), Relationship advance (1-2) |
| **Relationship Advance Potential** | 0-3 | Build champion (3), Remove objections (3), Clarify path (2), Status quo (0) |

**Decision: SEND if total ≥ 4. Otherwise, skip.**

---

### Step 1: Answer-Now vs Research vs Deferred

Triage each open question into **ownership + timeline**.

| Classification | Definition | Our Responsibility | Timeline |
|---|---|---|---|
| **ANSWER-NOW** | We have the answer already | HIGH (include in email) | Full response in email |
| **RESEARCH (SA-OWNED)** | We need to validate/model | HIGH (we committed) | Propose deadline + deliverable |
| **RESEARCH (CUSTOMER-OWNED)** | They validate; we need result as blocker | MONITOR (watch momentum) | Flag as "blocker on their side" in internal email |
| **TOO-EARLY** | Can't answer until next phase | DEFER (state dependency) | Propose revisit date after dependency |
| **THEIR-DECISION** | They decide internally; we support | SUPPORT (offer options) | Flag in "Mutual Commitments" section |

---

### Step 2: Assess Deal Health

5 core dimensions + 2 mandatory sub-checks. Output: Score (0-15) + momentum flag.

#### 5 Core Dimensions (0-3 points each)

| Dimension | Score 3 | Score 2 | Score 1 | Score 0 |
|---|---|---|---|---|
| **Customer Commitment Level** | Multiple HIGH commitments | Mix MEDIUM + some HIGH | Mostly TENTATIVE | None or all vague |
| **Decision Authority Present** | Economic buyer + engaged | Director + engaged | Manager present | No decision-maker OR passive |
| **Buying vs. Shopping Signals** | Clear progression (scoping/POC/negotiation) | Evaluating vs. competitors | Still comparing | Shopping, no urgency |
| **Blocker Analysis** | No blockers OR owners/plans | 1-2 blockers, partial clarity | 3+ blockers unowned | Critical blocker, no path |
| **Champion Assessment** | Strong, actively selling internally | Likely, engaged, untested | Supporter, unclear influence | No champion OR skeptical |

#### 2 Mandatory Sub-Checks

**Sub-Check #1: Approval Gates**
- Beyond obvious blockers, who else needs sign-off? (legal, InfoSec, compliance, procurement, reorg)
- If missing, flag as blocker

**Sub-Check #2: Competitive Position**
- Are we #1 choice, evaluating alternatives, or fallback?
- Adjust "Buying vs. Shopping" score accordingly

#### Momentum Classification

- **GREEN**: Score 12-15. Email should be proposal-heavy.
- **YELLOW**: Score 9-11. Email should balance recap + proposal.
- **RED**: Score 0-8. Email should be recap-heavy, focus on removing blockers.

---

### Step 3: Detect Sentiment & Coach Gaps

Read from `_System/coaching/coaching-flags.yaml` (if exists) or do lightweight self-check:

- **Sentiment**: excited | engaged | neutral | hesitant | skeptical
- **Coach Gaps** (from coaching-flags or inferred from transcript):
  - Discovery fundamentals gap? (if discovery score ≤ 2)
  - Over-talking pattern? (if we talk > 55% of meeting)
  - Passive listening pattern? (if we talk < 20% of meeting)
  - Objection handling gap? (if key objections unresolved)

**Output**: Sentiment + detected gaps (if any)

---

### Step 4: Surface Vague Language

Scan external email draft for 15+ vague language patterns. For **internal email only**, provide translations:

#### Vague Language Inventory (15+ patterns)

| Vague Pattern | What It Means | Internal Translation |
|---|---|---|
| "We'll get you options" | No timeline, no specifics | Action: Draft 2-3 options by DATE; blockers: need PERSON input |
| "Pending [X] approval" | Approval authority unclear | Risk: Approval gate not yet owned; owner: [?] |
| "Maybe in Q3" | Conditional, uncertain timeline | At-risk: Budget / priority not confirmed; contingency: escalate to [X] |
| "It depends on..." | Dependency stated but soft | Dependency owner: [?]; blocker if not resolved by [DATE] |
| "We should/could" | No commitment, just suggestion | Non-commitment; reframe as "will" or "proposes" |
| "Soon" | Vague timeline | Missing: specific date. Implies urgency but no proof. |
| "Somewhere around X" | Uncertain estimate | At-risk: timeline slip likely; mitigation: weekly check-ins |
| "In theory" | Hedging statement | Credibility gap: missing proof or concern unstated |
| "Supports HIPAA-eligible" | Compliance hedging (healthcare specific) | Risk: Not HIPAA-compliant, only *eligible*; legal review needed |
| "Industry standard" | Vague claim without proof | Credibility gap: missing case study or standard reference |
| "We'll evaluate/assess" | Action is analysis, not decision | At-risk: Can become perpetual assessment; set decision gate |
| "Assuming..." | Unstated assumption | Flag assumption in internal email; ask customer to confirm |
| "Most companies..." | Vague peer claim | Credibility gap: missing named reference or data |
| "Low risk" | Risk assessment without detail | Risk: Understated; ask for risk categories + mitigation |
| "Quick pilot" | Timeline undefined | At-risk: "Quick" varies by org; clarify in proposal (e.g., "2-week pilot") |

For **external email**: Translate vague patterns into specific WHAT/WHO/WHEN before sending.

---

### Step 5: Determine Composition Strategy

Map sentiment + momentum + gaps to section allocation. 

| Momentum | Sentiment | Recap % | Proof % | Proposal % | Rationale |
|---|---|---|---|---|---|
| GREEN | Excited | 20% | 30% | 50% | Momentum strong; spend energy on next steps |
| GREEN | Engaged | 30% | 40% | 30% | Solid foundation; confirm + move forward |
| YELLOW | Engaged | 40% | 35% | 25% | Balance recap confirmation with proposal |
| YELLOW | Hesitant | 50% | 40% | 10% | Reassurance + proof first; proposal is secondary |
| RED | Skeptical | 60% | 30% | 10% | Recap to show you heard concerns; minimal proposal until blockers cleared |
| RED | Hesitant | 70% | 25% | 5% | Heavy recap to rebuild trust; proposal deferred |

**Recap Section**: "Here's what we discussed" — recap with specificity, not generality.
**Proof Section**: "Here's why this matters" — case study, metric, or competitor context.
**Proposal Section**: "Here's what we propose next" — specific actions with WHO/WHAT/WHEN.

---

### Step 6: Generate External Email

Structure (universal):

```
Subject: [Proposal] {Topic from Meeting}

Greeting (1 para):
- "Thanks for taking the time..." + reaffirm one key point they said

Problem Statement (1-2 para):
- Restate their pain in their language (shows you heard)
- Why it matters to them (business impact or compliance)

Proposal (2-3 para):
- "Here's what we propose..." — specific next step(s)
- Include timeline and success criteria
- What we'll deliver; what you'll need to provide

Proof (1-2 para):
- Case study, metric, or competitive context
- Why this approach works (behavioral + technical)

Your Role (1 para):
- What our team commits to doing/owning
- Timeline + deliverable

Mutual Commitments (1 para):
- Our Commitment: WHO will do WHAT by WHEN
- Your Team's Role: WHO will do WHAT by WHEN (if applicable)
- Success Looks Like: Concrete success criteria

Questions We're Researching (1 para, if applicable):
- Anything we deferred or committed to validate
- Timeline for answer + how we'll share

Assumptions (1 para):
- Key assumptions we're making (e.g., "We assume you have Epic access by DATE")
- Flag if customer needs to validate any

Closing (1 para):
- Next step: "Let's schedule a [TYPE] call on [DATE] to..."
- Clear call-to-action

---

```

#### Prior Email Continuity Check

Before finalizing external email:
1. Find last 3 follow-ups to this customer (past 30 days)
2. Check for: repeated themes, unresolved issues, promise patterns
3. If repeating same proposal/promise → highlight what's different this time OR explain why re-emphasis matters

---

### Step 7: Generate Internal Email

Structure (for AE + manager):

```
Subject: [DEAL HEALTH: {MOMENTUM}] {Topic}

Executive Summary (1 para):
- Deal health badge (GREEN/YELLOW/RED)
- One-line momentum assessment
- What we need from AE in next 72 hours

Commitment Summary (table or bullets):
- Our Commitment: WHAT by WHEN (with confidence)
- Their Commitment: WHAT by WHEN (with confidence)
- At-Risk: Any commitments with LOW confidence or explicitly conditional

Decision-Readiness (1 para):
- Who can decide? (economic buyer, influencer, architect?)
- Are they present? Engaged?
- What's blocking their decision?

Vague Language Decoded (table, if any):
- Vague pattern from transcript | What it probably means | Action to de-vague
- Example: "We'll get you options" | They haven't decided on approach | Action: Draft 2-3 options by [DATE]; confirm with [PERSON]

Blockers & Risks (bullets):
- Blocker 1: [Description] | Owner: [?] | Timeline to resolve: [?]
- Risk 1: [Explicit concern from meeting or inferred]
- Competitive position: [Are we #1, evaluating alternatives, or fallback?]

Champion Assessment (1 para):
- Is there a strong champion? Who?
- Are they actively selling internally? (Ask AE)
- Red flag: No champion or champion skeptical

Strategic Insights (1-2 para, optional):
- Patterns we notice (e.g., "They keep deferring compliance questions")
- Opportunities (e.g., "Economic buyer mentioned Q3 budget — we should propose by Q2")
- Competitive intelligence (if discussed)

Next Moves (bullets):
- Step 1: [AE action] by [DATE]
- Step 2: [Our action] by [DATE]
- Step 3: [Customer action] by [DATE] (if applicable)
- Step 4: [Checkpoint/re-engagement date] by [DATE]

Coach Queue (if applicable):
- If discovery score ≤ 2: "Add to coach queue: discovery fundamentals gap"
- If talk ratio > 0.55: "Add to coach queue: over-talking pattern"
- If talk ratio < 0.20: "Add to coach queue: passive listening pattern"
```

---

### Step 8: Quality Gates

**4 Blocking Gates** (email doesn't go out if any fail):

1. ✓ **Commitment Clarity**: All OUR-COMMITMENT and THEIR-COMMITMENT have WHO/WHAT/WHEN. No "we'll follow up" without specifics.
2. ✓ **Outcome-Linking (90%+ threshold)**: At major section level (not sentence level), ask "So What?" — why does this matter to the customer? 90%+ of external email sections link to customer business outcome or next decision.
3. ✓ **Bilateral Clarity**: External email makes clear WHO is doing WHAT on both sides. Language: "Our Team / Your Team / Success Looks Like" format.
4. ✓ **PHI/Leak Check** (healthcare only): No PHI in external email. No internal financial numbers in external. Internal email free of customer secrets.

**1 Flag Gate** (warning, not blocking):

5. 🚩 **Loss-Aversion Framing (optional)**: Does external email invoke loss (fear of missing out, competitive threat, momentum loss) in addition to gain (opportunity)? Cialdini research shows loss frames drive commitment. If NOT present, flag for consideration (may be unnecessary for GREEN deals, valuable for RED/YELLOW).

---

### Step 9: Generate & Persist Output Files

#### File Paths (Vault Convention)

```
Artifacts/{account}/emails/{YYYY-MM-DD}-{email-slug}_external.html
Artifacts/{account}/emails/{YYYY-MM-DD}-{email-slug}_internal.md
```

Example:
```
Artifacts/nwm/emails/2026-04-18-operational-governance-endorsement_external.html
Artifacts/nwm/emails/2026-04-18-operational-governance-endorsement_internal.md
```

#### Sidecar Metadata (in HTML `<head>` or markdown frontmatter)

```yaml
---
artifact_id: "{account}-email-{YYYY-MM-DD}-{slug}"
artifact_type: "email"
email_type: "external|internal"
title: "[Proposal] Architecture Review Follow-Up — NWM"
created: "YYYY-MM-DD"
source_skill: "draft-followup"
related_session: "SESSION-ID"

draft_followup_metadata:
  meeting_type: "architecture_review|governance|commercial_discussion|etc"
  deal_health_score: 0-15
  deal_momentum: "GREEN|YELLOW|RED"
  
  composition_strategy:
    recap: "X%"
    proof: "Y%"
    proposal: "Z%"
  
  commitments:
    count_high_confidence: N
    count_medium_confidence: N
    count_low_confidence: N
    count_at_risk: N
  
  vague_language_detected: true|false
  vague_patterns:
    - "pattern 1"
    - "pattern 2"
  
  questions_researched: N
  
  quality_gates:
    commitment_clarity: "PASS|FAIL"
    outcome_linking: "PASS|FAIL"
    bilateral_clarity: "PASS|FAIL"
    internal_leak_check: "PASS|FAIL"
    loss_aversion: "PRESENT|FLAG"
  
  coaching_flags:
    - "discovery fundamentals gap" (if applicable)
    - "over-talking pattern" (if applicable)
---
```

#### Post-Persist Actions

1. Call `vault_reindex(full=false, embed=false)` to sync vault metadata
2. If `coaching_flags` are set, append to `_System/coaching/coach-queue.md` for `/coach` skill
3. Provide user with:
   - File paths for both emails
   - Deal health summary table
   - Quality gates result (all PASS, or which gates failed)
   - Coaching flags (if any)

---

## Success Criteria

You've drafted a good follow-up when:

✓ Customer (if shown) says "This captures what we discussed and makes it clear what comes next"
✓ AE (reading internal email) immediately understands deal momentum + blockers + next moves
✓ No vague language goes untranslated in internal email
✓ Both sides' commitments are explicit with WHO/WHAT/WHEN
✓ Outcome-linking passes 90% threshold at section level
✓ Champion can forward external email without editing (or with minimal edits)
✓ All 4 blocking quality gates pass

You've drafted a weak follow-up when:

✗ Email reads like a recap, not a proposal
✗ 20+ sentences of features with no outcome linkage
✗ Commitments are vague ("we'll follow up", "pending approval")
✗ Decision authority can't act on it
✗ AE finishes internal email confused about what to do next
✗ Quality gates fail on commitment clarity or bilateral clarity

---

## Psychology & Design

### Why Written Commitments?

Cialdini (Influence): Written commitments are self-reinforcing. When someone sees their own commitment in writing, they're more likely to follow through. The follow-up email is the *record* they'll point to later.

### Why Specificity Over Vagueness?

Kahneman/Tversky (Prospect Theory): People act on specific outcomes, not vague ones. "We'll increase throughput 20%" is actionable. "We'll make it better" is not.

### Why Bilateral Language?

Challenger Sale: Don't position ourselves as the expert solving THEIR problem. Position as the partner helping THEM solve it. "Our Team / Your Team" language builds accountability on both sides.

### Why Outcome-Linking?

Behavioral Economics: Every section must answer "Why does this matter to YOU?" Generic feature descriptions don't move people. Customer-specific impact does.

---

## vault_speaker Integration (Production — W5 Cutover)

**Status:** PRIMARY (graduated from shadow mode)

vault_speaker is the primary context source for follow-up email generation. Existing retrieval logic (session file parsing, vault_signals, stakeholder lookups) serves as fallback.

### At generation start:

1. Call vault_speaker: `/vault-speaker --intent email --account {account_id}`
2. If vault_speaker succeeds (returns confidence != low): use its package as primary context
   - Session context, commitments, and stakeholder profiles come from vault_speaker
   - Still parse the session file directly for commitment extraction (Step 0) and deal health assessment (Step 2)
3. If vault_speaker fails or returns confidence=low: fall back to existing retrieval logic (session file + vault_signals + stakeholder lookups)
4. Log outcome_tag to vault_speaker_invocations after generation completes

### Fallback behavior:

- vault_speaker timeout (>15s): use existing retrieval logic, log outcome_tag='timeout'
- vault_speaker error: use existing retrieval logic, log outcome_tag='error'
- vault_speaker confidence=low for all retrievers: use existing retrieval logic, log outcome_tag='low_confidence_fallback'

### What vault_speaker provides (when successful):

- **Session context**: recent meeting summaries and discussion themes
- **Commitments**: ours-to-them and theirs-to-us with confidence levels
- **Stakeholder profiles**: roles, decision authority, communication preferences

### What existing logic still owns (always):

- Commitment extraction and classification (Step 0 — 8 categories)
- Send/Skip triage (Step 0.5)
- Deal health assessment (Step 2 — 5 dimensions)
- Vague language detection (Step 4)
- Quality gates (Step 8 — 4 blocking gates)
- Session file parsing for verbatim quotes

### Logging:

After follow-up generation completes, log the invocation to brain.db:
```python
import sqlite3, json, secrets
db = sqlite3.connect("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")
db.execute("""
    INSERT INTO vault_speaker_invocations
    (invocation_id, run_id, intent, scope, outcome_tag, latency_ms)
    VALUES (?, ?, 'email', ?, ?, ?)
""", (
    secrets.token_hex(16), secrets.token_hex(16),
    json.dumps({"account_id": account_id, "skill": "draft-followup"}),
    outcome_tag,  # 'success' | 'timeout' | 'error' | 'low_confidence_fallback'
    latency_ms,
))
db.commit()
db.close()
```

---

## Integration with Other Skills

### From `/process-transcript`

- **Input**: Structured session file with commitments, action items, risks, MEDPICC signals
- **Flow**: `/process-transcript` → outputs session + coaching-flags.yaml → `/draft-followup` reads both

### Into `/post-meeting` Coordinator

- **Input**: Session from `/process-transcript`
- **Output**: External + internal emails
- **Next**: Post-meeting coordinator may call `/tone-check` on external email, `/iterate` for refinement

### From `/coach` Skill

- **Input**: Coaching flags from `/draft-followup` (written to coach-queue.md)
- **Output**: One-at-a-time coaching questions for AE or SA
- **Loop**: Coach flags fed back into next follow-up design

---

## Common Failure Modes

1. **Recap without proposal** — Email reads like meeting notes, not a next step. Check Step 5 allocation; proposal section should be non-zero.
2. **Vague commitments slip through** — "We'll follow up" without date. Check Step 4 vague language inventory before finalizing.
3. **Internal leak in external email** — Financial numbers, competitive positioning, or manager notes visible to customer. Check Step 8 PHI/leak gate.
4. **No champion identified** — Internal email doesn't flag who's selling internally. Check Step 2 champion assessment + Step 7 internal email.
5. **Success criteria deferred** — "We'll define success in the pilot" instead of now. Check Step 6 "Success Looks Like" — must be explicit in email.

---

## Testing

See `/draft-followup` test cases in `.testing/draft-followup-tests.md` for real examples from NWM, CHN, CHLA accounts.
