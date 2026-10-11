# Prep — SA Intelligence Vault

Meeting preparation with full context from `~/obsidian/sa-intel/`, powered by vault_speaker for unified retrieval.

## Usage

```
/prep [account]           # Internal meeting prep (forecast, AE sync)
/prep [account] customer  # Customer meeting prep
/prep [account] quick     # Quick version (5 min)
/prep [account] deep      # Deep dive with full technical context
/prep [account] exec      # Executive meeting (includes strategic intel)
/prep --project [id]      # Project-scoped prep (e.g., /prep --project career-growth-2026)
```

## Vault Speaker Integration

**Step 1: Invoke vault_speaker as the primary context source.**

Before generating any prep output, call vault_speaker to gather all context:

```
/vault-speaker --intent prep --account {account_id}
```

Or for project-scoped prep:

```
/vault-speaker --intent prep --project {project_id}
```

This replaces manual vault queries (vault_summary, vault_signals, vault_search, vault_graph). The vault_speaker package contains:
- Account Context (use cases, stages, MRR, health)
- Stakeholder Context (attendees, roles, stance, relationships)
- Temporal Context (recent sessions, what changed, timeline)
- Contradictions (flagged for manual review)
- Fallback Interrogations (gaps the SA should investigate)
- Degradation Notes (data quality warnings)

**Step 2: Parse the vault_speaker package.**

Extract the frontmatter fields:
- `invocation_id` — needed for outcome feedback (Step 4)
- `min_confidence` — determines if data is trustworthy
- `cache_hit` — informational

**Step 3: Generate prep output using the package data.**

Map vault_speaker sections to prep output sections:
| Vault Speaker Section | Prep Section |
|---|---|
| Account Context | Account Summary, Use Cases to Discuss |
| Stakeholder Context | Attendees Expected (customer prep) |
| Temporal Context | "Last Time" / "Changed" fields, Recent Artifacts |
| Contradictions | Surface as warnings in prep output |
| Fallback Interrogations | Add to Pre-Call Checklist as investigation items |

**Confidence handling:**
- `high` — proceed normally
- `medium` — add note: "Some data may be stale — verify key facts"
- `low` — add warning: "Data quality is low — manual vault review recommended before meeting"

**Step 4: Log outcome feedback.**

After generating prep output, log the invocation using the shared helper:

```python
python3 -c "
import sys; sys.path.insert(0, '/Users/samuel.selvan/obsidian/sa-intel/_System/scripts')
from shared.invocation_logger import log_invocation
log_invocation(intent='prep', caller_skill='prep', scope={'account': '{account_id}'}, outcome_tag='usable')
"
```

Valid outcome_tag values: `usable`, `incomplete`, `abandoned`, `error`.

**Outcome feedback mechanism:**
- If user gives thumbs-down or says "this is wrong" → update to 'incomplete'
- If user abandons prep and re-runs → update prior invocation to 'abandoned'
- Default assumption: if user proceeds without complaint → 'usable'

---

## Fallback: Direct Vault Queries

If vault_speaker is unavailable (skill not loaded, or returns error), fall back to direct MCP tool queries:

1. `vault_schema()` — introspect valid accounts
2. `vault_summary(account="[name]")` — account overview
3. `vault_signals(account="[name]", status="open")` — open signals
4. `vault_graph(source_id="person:[slug]")` — stakeholder connections
5. `vault_search(query="...", account="[name]")` — topic search

Log a degradation warning in output: "vault_speaker unavailable — using direct vault queries (may miss cross-retriever synthesis)"

---

## Strategic Intel Integration

**BEFORE generating prep**, check for strategic research:
```
~/obsidian/sa-intel/Reference/strategic-intel/[account]-strategic.md
~/obsidian/sa-intel/Reference/strategic-intel/[account]-business-units.md
```

If strategic intel exists, integrate into prep:
- Surface relevant strategic priorities for the meeting context
- Note which business unit the use case aligns to
- Flag any financial metrics or KPIs relevant to the discussion

If strategic intel is missing and prep type is `exec` or `deep`:
- Warn: "Strategic intel not found. Run `/research [account] deep` first?"

---

## Internal Meeting Prep (Default)

For forecast calls, AE syncs, internal reviews.

### Process

1. **Invoke vault_speaker** with intent=prep, account={account_id}
2. **Parse package** — extract Account Context, Temporal Context, Contradictions
3. **Check Recent Artifacts:**
   - From vault_speaker's Artifact Context section (if available)
   - Or search `~/obsidian/sa-intel/Accounts/[account]/Artifacts/`
   - List recent artifacts (last 30 days) with age
   - Flag stale artifacts (>60 days) that may need refresh

4. **Build output sections from vault_speaker package:**

   **Account Overview:** (from Account Context)
   - Total MRR potential
   - Account health
   - Primary competitor

   **All Non-Live Use Cases:** (from Account Context + Temporal Context)
   - Stage, MRR, close date, status
   - What I said last time (from Temporal Context)
   - What changed since last forecast

   **Risks:** (from Account Context)
   - All `#risk/high` and `#risk/critical`
   - Sorted by severity

   **Overdue Follow-ups:** (from Temporal Context)
   - Anything past due

   **MEDPICC Gaps:** (from Account Context)
   - Lowest scores across use cases

### Output

```markdown
# Internal Prep: [Account]
**Date:** [Today]
**Prep Time:** ~10 min
**Data Source:** vault_speaker (invocation: {invocation_id})

---

## Account Summary

| Metric | Value |
|--------|-------|
| Total MRR (Active) | $X |
| Use Cases (Active) | X |
| Primary Competitor | Snowflake |
| Account Health | yellow |

---

## Use Cases to Discuss

### UC: [Name] — ON TRACK
- **Stage:** Evaluation | **MRR:** $25K | **Close:** Feb 28
- **Last Time:** "POC going well, security review in progress"
- **Changed:** Security review completed
- **This Week:** [Draft what to say]
- **MEDPICC Gap:** Decision Process (score: 2)

### UC: [Name] — SLIPPING
- **Stage:** Scoping | **MRR:** $15K | **Close:** Mar 15 (+14 days)
- **Last Time:** "Building proposal"
- **Changed:** Close date pushed, scope expanded
- **Slippage Reason:** Customer requested scope expansion
- **This Week:** [Draft what to say]
- **MEDPICC Gap:** Champion (score: 3)

---

## Risks to Raise

| Risk | Use Case | Severity | Mitigation Status |
|------|----------|----------|-------------------|
| Security concerns | DataLake | #risk/high | Addressed |
| Budget approval | MLPlatform | #risk/medium | Pending |

---

## Overdue Follow-ups

| Days | Use Case | What | To Whom |
|------|----------|------|---------|
| 3 | DataLake | Architecture doc | John |

---

## MEDPICC Gaps (Account-Wide)

| Component | Avg | Biggest Gap |
|-----------|-----|-------------|
| Decision Process | 2.5 | DataLake |
| Champion | 3.0 | MLPlatform |

---

## Talking Points

1. [Use Case 1] - [Key message]
2. [Use Case 2] - [Key message]
3. Risk callout: [If any]
4. Ask for help: [If needed]

---

## Contradictions (from vault_speaker)
{Any conflicting data surfaced by vault_speaker — review before meeting}

## Data Quality
{Degradation notes from vault_speaker — flag any low-confidence sections}
```

---

## Customer Meeting Prep

### Additional Data (from vault_speaker Stakeholder Context)

**Stakeholder Intel:**
- Who's expected on the call?
- Their role, stance, last interaction
- What they care about
- How to approach them

**Open Questions from Them:**
- Unanswered questions flagged with `#open-question`

**Our Commitments to Them:**
- What did we promise?

**Their Commitments to Us:**
- What are we waiting on?

**Reference Materials:**
- Relevant architectures from `Reference/`
- Similar case studies
- Demo links

**Competitive Context:**
- What competitors are they considering?
- Our positioning

### Output (Customer Prep)

```markdown
# Customer Prep: [Account]
**Meeting:** [Date/Time if known]
**Type:** Discovery | Technical | Executive | Check-in
**Data Source:** vault_speaker (invocation: {invocation_id})

---

## Attendees Expected

### [Name] — [Title]
- **Role:** Economic Buyer
- **Stance:** Supporter (moving toward Champion)
- **Last Contact:** Jan 5 — discussed security requirements
- **Cares About:** TCO, time to value
- **Approach:** Lead with ROI, avoid deep technical dive

### [Name] — [Title]
- **Role:** Technical Buyer
- **Stance:** Neutral
- **Last Contact:** Dec 20 — POC kickoff
- **Cares About:** Integration complexity
- **Approach:** Address Kafka concerns proactively

---

## Use Cases to Discuss

[Same as internal but customer-appropriate framing]

---

## Open Questions (Theirs)

| Question | Asked By | Urgency | Our Answer |
|----------|----------|---------|------------|
| How does Unity Catalog handle X? | CTO | High | [Prepare answer] |

---

## Our Commitments to Them

| What | To Whom | Due | Status |
|------|---------|-----|--------|
| Architecture doc | John | Jan 10 | Overdue |

---

## Their Commitments to Us

| What | From Whom | Due | Status |
|------|-----------|-----|--------|
| Test data access | IT Team | Jan 12 | Pending |

---

## Reference Materials

- [[Reference/architectures/lakehouse-healthcare.md]]
- [[Reference/case-studies/similar-payer.md]]
- Demo environment: [link]

---

## Competitive Context

- **Considering:** Snowflake
- **Their pitch:** Easier to manage
- **Our counter:** TCO, unified platform, ML capabilities

---

## Suggested Agenda

1. Follow up on [open item]
2. Address [their question]
3. Demo [specific capability]
4. Discuss next steps -> [propose specific next step]

---

## Pre-Call Checklist

- [ ] Review their pain points
- [ ] Prepare answer to open questions
- [ ] Know what I committed to last time
- [ ] Have demo ready
- [ ] Know the next step to propose
- [ ] Investigate fallback interrogations from vault_speaker
```

---

## Executive Meeting Prep (`exec`)

For meetings with economic buyers, C-suite, or senior stakeholders.

### Additional Data Required

Pull from vault_speaker package + `Reference/strategic-intel/[account]-strategic.md`:

**Strategic Context:**
- Their top 3 strategic priorities
- Key financial metrics they're targeting
- Business unit this use case maps to

**Executive Framing:**
- How our use case connects to their strategic priorities
- Business impact in their language (not technical)
- ROI/value story tailored to their KPIs

### Output (Exec Prep)

```markdown
# Exec Prep: [Account]
**Meeting:** [Date/Time]
**Attendees:** [Names and titles]
**Type:** Executive
**Data Source:** vault_speaker (invocation: {invocation_id})

---

## Strategic Context

### Their Priorities (from strategic intel)
| Priority | Our Alignment | Talking Point |
|----------|---------------|---------------|
| [Priority 1] | [How we help] | [Sound bite] |
| [Priority 2] | ... | ... |

### Key Metrics They Care About
| Metric | Current | Target | Our Impact |
|--------|---------|--------|------------|
| [Metric 1] | $X | $Y | [How we move the needle] |

### Business Unit Context
- **Unit:** [Which BU owns this]
- **Unit Priority:** [What that BU is focused on]

---

## Attendee Intel

### [Name] — [Title]
- **Cares About:** [From stakeholder context + strategic intel]
- **Communication Style:** [Executive summary only / wants details / etc.]
- **Last Interaction:** [Date] — [Key takeaway]
- **Approach:** [How to frame for this person]

---

## Value Story (Exec Version)

**The Problem (in their words):**
[Reframe technical pain as business pain using their strategic language]

**The Opportunity:**
[Connect to their stated priorities and metrics]

**Our Ask:**
[Clear next step framed as business decision, not technical milestone]

---

## Talk Track (30-second version)

"[Account] is focused on [Priority 1]. Our work on [Use Case] directly supports that by [impact]. We're at [stage] and need [specific ask] to [business outcome]."

---

## Pre-Call Checklist (Exec)

- [ ] Know their top 3 strategic priorities
- [ ] Can articulate business impact in <30 seconds
- [ ] Know the specific ask and why it matters to them
- [ ] Have exec-level objection handling ready
- [ ] Prepared for "why Databricks vs [competitor]" question
```

---

## Migration Meeting Prep (`migration`)

For accounts with EDW migration opportunities (Snowflake, legacy DW, cloud-native).

### Process

1. **Business Drivers Analysis** — from vault_speaker Account Context + strategic intel
2. **Technical Requirements Mapping** — from vault_speaker Pattern Context
3. **Competitive Positioning** — from vault_speaker Account Context

### Output (Migration Prep)

```markdown
# Migration Prep: [Account]
**Current Platform:** [Snowflake / Teradata / etc.]
**Migration Driver:** [Cost / Performance / AI / Consolidation]
**Data Source:** vault_speaker (invocation: {invocation_id})

---

## Business Case for Migration

### Strategic Drivers
| Driver | Current Pain | Migration Benefit |
|--------|--------------|-------------------|
| [Driver 1] | [What's broken] | [What migration fixes] |

### Industry Pressure Points
- [Trend 1]: [How it creates urgency]

---

## Mission-Critical Requirements

| Requirement | Why Mission-Critical | Current Gap | Databricks Advantage |
|-------------|---------------------|-------------|---------------------|
| [Req 1] | [Business reason] | [What's missing] | [How we solve] |

---

## Competitive Context

### Competitor: [Name]
**Their Pitch:** [What they're saying]
**Their Weakness:** [Where they fall short]

### Our Counter-Positioning
| Their Claim | Reality | Our Message |
|-------------|---------|-------------|
| [Claim 1] | [Truth] | [What to say] |

---

## Trap-Setting Questions

1. **[Question]**
   - Expected answer: [What they'll say]
   - Follow-up: [How to probe]
   - Sets up: [Databricks advantage]

---

## Talk Track (30-second version)

"[Account] is facing [pressure]. Your current [platform] is limiting [capability]. We've helped [similar customer] migrate and achieve [outcome]."

---

## Pre-Call Checklist (Migration)

- [ ] Know their current platform and pain points
- [ ] Can articulate 3 mission-critical requirements
- [ ] Have trap-setting questions ready
- [ ] Know competitor's pitch and our counter
- [ ] Have similar customer reference ready
```

---

## Output Convention

**Write path:** `Artifacts/{account-slug}/prep_docs/{YYYY-MM-DD}-prep-{meeting-type-slug}.md`
**artifact_type:** `prep_doc`
**Frontmatter required:**
```yaml
artifact_id: "{account-slug}-prep_doc-{date}-prep-{meeting-type-slug}"
account: "{account-slug}"
artifact_type: "prep_doc"
title: "{Internal|Customer|Exec|Migration} Prep: {Account}"
created: "{YYYY-MM-DD}"
source_skill: "prep"
related_session: "{session-id or null}"
```
**After saving:** `vault_reindex(full=false, embed=false)`

$ARGUMENTS
