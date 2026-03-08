# Email Patterns — Quick Reference

Tactical patterns for the email-render skill. Use alongside `email-philosophy.md` for the full rules.

---

## BLUF Templates by Type

Every email starts with a BLUF sentence. These are starter patterns — adapt to the specific situation.

### Type 1: Follow-Up
```
We're sending over [deliverable] by [date] and scheduling [next meeting] for [timeframe].
```

### Type 1b: Group Follow-Up
```
We aligned on [N] next steps with [timeline] — here's the breakdown.
```

### Type 2: Deliverable
```
Here's the [artifact] addressing [their specific problem] we discussed on [date].
```

### Type 3: Research/Answers
```
We dug into your [N] questions from [date] — the short answer on [most impactful]: [answer].
```

### Type 4: Introduction
```
Connecting you two — [Person B] is working on [relevant thing] that maps to [Person A's challenge].
```

### Type 5: Check-In
```
Circling back on [topic] — wanted to share [new data point] that's relevant.
```

### Type 6: Scheduling
```
Want to get [meeting purpose] on the calendar — would [timeframe] work?
```

### Type 7: Decline/Redirect
```
After reviewing [their request], I think [alternative] would serve you better — here's why.
```

### Type 8: Insight Share
```
[Reframing insight] — this maps directly to [specific thing they mentioned on date].
```

### Type 9: Reactive Response
```
[Direct answer to what they asked/sent] — and here's what stood out about [specific element].
```

---

## Subject Line Formulas

Write subject lines LAST, after the body. Under 50 characters when possible.

| Type | Formula | Example |
|------|---------|---------|
| Follow-Up | `[Topic] — next steps` | PICU pipeline — next steps |
| Group Follow-Up | `[Meeting topic] — recap + next steps` | PDC architecture review — recap + next steps |
| Deliverable | `[Artifact] for [their goal]` | Architecture guide for PICU data flows |
| Research | `Answers on [topic]` | Answers on HIPAA timeline + Delta Sync |
| Introduction | `Connecting you — [reason]` | Connecting you — clinical AI on Databricks |
| Check-In | `[Topic] — quick update` | PDC pilot scoping — quick update |
| Scheduling | `[Meeting type] — [timeframe]?` | Technical deep dive — week of 2/17? |
| Decline | `[Topic] — honest take` | Oracle migration — honest take |
| Insight | `[Reframe statement]` | Your EHR pipeline bottleneck might not be where you think |
| Reactive | `Re: [their subject] — [what you're adding]` | Re: Architecture diagram — feedback + recommendations |

---

## Word Count Targets

**Default targets (most recipients — keep it short):**

| Type | Target | Hard Max |
|------|--------|----------|
| Follow-Up (1:1) | ≤ 100 | 120 |
| Follow-Up (Group) | ≤ 150 | 180 |
| Deliverable | ≤ 80 | 100 |
| Research/Answers | ≤ 200 | 300 |
| Introduction | ≤ 60 | 75 |
| Check-In | ≤ 50 | 60 |
| Scheduling | ≤ 60 | 75 |
| Decline/Redirect | ≤ 100 | 120 |
| Insight Share | ≤ 120 | 150 |
| Reactive Response | ≤ 150 | 200 |

**Technical depth escalation** (`to_type = technical` + 3+ distinct questions):

| Questions | Multiplier | Hard Max |
|-----------|------------|----------|
| 3-4 | 2× target | 2× hard max |
| 5+ | 3× target | 800 |

Escalation ONLY applies to technical recipients. Managers, execs, sales — standard targets always.

---

## Challenger Tailoring Matrix

Same content, different framing depending on recipient's buying role:

| Recipient Role | Lead With | Frame As | Example |
|---------------|-----------|----------|---------|
| Economic Buyer (CFO/VP Finance) | Dollars | Cost reduction or revenue protection | "This reduces reconciliation cost by ~40%." |
| Technical Buyer (CTO/VP Eng) | Architecture fit | Integration simplicity | "This plugs into your existing Spark pipelines without rearchitecting." |
| Champion (Data Eng/ML Eng) | Their visibility | Career win | "This positions your team as the ones who solved multi-site access." |
| Blocker (Security/Compliance) | Compliance status | Risk mitigation | "HIPAA eligible out of the box — here's the BAA process." |
| Clinical / Domain Expert | Patient/workflow impact | Operational improvement | "Reduces chart review time from 45 min to 8 min per case." |

---

## Relationship Depth Signals

How to detect depth from vault data:

| Vault Signal | Depth | Tone |
|-------------|-------|------|
| `vault_graph` shows 0-1 session edges | `new` | Formal. Full sentences. Title context. |
| `vault_graph` shows 2-5 session edges | `working` | Warm professional. First names. |
| `vault_graph` shows 5+ session edges OR stakeholder file has `stance: champion` | `champion` | Direct. Terse OK. Skip pleasantries. |
| Stakeholder file has `communication_preference: Teams` | Any | Note in prep notes: "Consider sending via Teams instead" |

---

## Nudge Threshold by Vertical

| Vertical | Days Before Nudge | Source |
|----------|-------------------|--------|
| HLS (hospitals, health systems) | 7 | Clinical duties, IRB cycles, grant deadlines |
| Enterprise (non-HLS) | 5 | Standard corporate cadence |
| Startup / SMB | 3 | Faster-moving orgs |
| Custom | Pull `nudge_threshold_days` from `Accounts/[name].md` | Account-specific override |

---

## Frontmatter Schema (Complete)

```yaml
---
entity_type: artifact
artifact_type: email_draft
date: 2026-02-11
to: Long Ho (Principal Data Scientist, CHLA)
to_type: technical  # technical | manager | executive | clinical | internal
from: Samuel Selvan
cc: Heather Fils, Mithun Karupuswamy  # optional
account: CHLA
topic: Onsite follow-up answers
email_type: research_answers
  # follow_up | group_follow_up | deliverable | research_answers |
  # introduction | check_in | scheduling | decline_redirect |
  # insight_share | reactive_response
status: draft  # draft | sent | skipped | suppressed
priority: high  # high | medium | low
due: 2026-02-14
suggested_send_time: "Tuesday AM"
stale_after: 72h
relationship_depth: working  # new | working | champion
thread_check: clear  # clear | active_thread | recently_sent
recipient_email: loho@chla.usc.edu     # resolved email (from vault or Gmail lookup)
gmail_draft_id: r123456789              # Gmail draft ID (if created)
gmail_thread_id: 18d1a2b3c4e5f678       # thread ID (if replying to existing thread)
gmail_last_sent: 2026-02-10             # last email sent to recipient (via Gmail)
gmail_last_received: 2026-02-08         # last email received from recipient (via Gmail)
related:
  - "[[Sessions/CHLA/customer/2026-02-10]]"
  - "[[Reference/chla-pdc-multisite-research-patterns]]"
---
```

---

## Priority Matrix

| Condition | Priority | Rationale |
|-----------|----------|-----------|
| Commitment <3 days, customer waiting | HIGH | Responsiveness = trust |
| Deliverable with specific timeline | HIGH | Promise made, clock ticking |
| Research answers ready | HIGH | Relationship-deepening moment |
| Reactive response to their input | HIGH | They initiated — match energy |
| Scheduling next meeting | MED | Keeps momentum |
| Introduction request | MED | Relationship investment |
| Nudge on overdue item | MED | Cadence maintenance |
| Decline / redirect | MED | Honesty builds trust |
| Insight share | LOW | Value-add, not time-sensitive |
| Nice-to-have follow-up | LOW | Background relationship |

---

## Due Date Defaults

| Type | Default Due |
|------|------------|
| Meeting follow-up | Same day or next business day |
| Deliverable | Per commitment date, or +2 business days |
| Research/answers | Per commitment date, or +5 business days |
| Introduction | +3 business days |
| Scheduling | +2 business days |
| Check-in/nudge | +1 business day after detection |
| Decline/redirect | +2 business days |
| Insight share | +5 business days |
| Reactive response | +1 business day |

---

## Quality Gate Checklist (Quick Scan)

Run before saving any draft:

```
[ ] BLUF first sentence — bottom line IS the first sentence
[ ] Word count within target for this type (use escalated target if technical depth applies)
[ ] No internal content leaked (strategy, competitor intel, MEDPICC scores)
[ ] No wiki-links in email body — plain text names only
[ ] No placeholder brackets — only ⚠️ VERIFY: flags
[ ] One clear ask or next step
[ ] Forwardable — makes sense without meeting context
[ ] Value-add present — teaches, advances, or delivers
[ ] Subject line benefit-focused, under 50 chars
[ ] Tone matches recipient type
[ ] Signed "Samuel" — not Sam, not Best regards
[ ] Prep notes complete (all 8 sections)
```

---

## Anti-Patterns (Red Flags)

Scan every draft for these. Auto-fix if found.

| Pattern | Detection | Fix |
|---------|-----------|-----|
| "Just checking in" | Opening with "checking in", "following up", "touching base" + no new content | Add value: data point, insight, timeline update |
| "Hope this finds you well" | Anywhere in opening | Delete. Start with BLUF. |
| "Per our conversation" | Without restating what was discussed | Restate the specific topic |
| "Please don't hesitate" | In closing | Replace with "Let me know if questions come up." |
| Feature dump | 3+ capabilities listed without business connection | Apply "So What?" filter — connect each to a stated pain |
| "When works for you?" | In scheduling emails | Propose a specific timeframe |
| Wall of text | Any paragraph >3 sentences | Break up. One idea per paragraph. |
| Vendor voice | "Our platform delivers...", "We provide..." | Rewrite: "The platform enables..." or their perspective |
| Signing as "Sam" | Signature | Always "Samuel" |
| Multiple asks | >1 distinct request in one email | Split into separate emails or highlight ONE primary ask |
