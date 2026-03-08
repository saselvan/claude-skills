# Lakebase HLS — AE Enablement Card

**Last validated:** 2026-02-07 | **Quota credit:** 2× | **Avg deal size:** $150-300K ARR

---

## Quick Navigation

- [The Pitch](#the-pitch)
- [Buying Committee](#buying-committee)
- [First Discovery](#first-discovery)
- [Discovery Framework](#discovery-framework)
- [Commercial Objections](#commercial-objections)
- [Proof Points](#proof-points)
- [vs Aurora/RDS](#vs-aurorards)
- [Qualification Scorecard](#qualification-scorecard)
- [When to Bring in SA](#when-to-bring-in-sa)
- [Deal Sizing](#deal-sizing)
- [Collateral by Stage](#collateral-by-stage)

---

## The Pitch

Lakebase is Databricks' managed Postgres for operational apps. Healthcare teams building patient portals, AI chatbots, or clinical dashboards get sub-10ms queries on lakehouse data — no ETL pipelines to build or maintain. Unity Catalog governance included.

**For the business buyer:** "Eliminate the engineering tax of syncing operational and analytical data. Teams see 70-80% cost savings and weeks of pipeline work eliminated."

**For the technical stakeholder:** "Standard Postgres wire protocol. Your existing tools work. Delta Sync keeps lakehouse and operational data in sync automatically."

---

## Buying Committee

| Title | Role in Decision | What They Care About | Your Message |
|-------|-----------------|---------------------|--------------|
| **VP Engineering / CTO** | Economic buyer | Total cost, team velocity, technical debt | "Eliminate pipeline maintenance. Your engineers build apps, not plumbing." |
| **Director of Data Platform** | Technical evaluator | Architecture fit, governance, ops burden | "Native Unity Catalog integration. One governance model across lakehouse and operational data." |
| **DBA / Platform Engineer** | Implementer / blocker | Reliability, Postgres compatibility, DR | "Managed Postgres with automatic backups, instant branching, 60+ extensions." |
| **Clinical Informatics / Biz Ops** | Champion / user | Time to insight, data freshness | "Lakehouse insights in your apps in seconds, not hours." |

---

## First Discovery

**Frame the conversation** ⏱️ 2min

> "Before I show you anything, I want to understand your world. You're building operational applications on top of your lakehouse — tell me about the architecture today."

**Business pain questions:**
1. "How do you get lakehouse insights into your operational apps today?"
   → *Listen for:* ETL pipelines, batch jobs, data staleness
2. "What's the engineering cost of keeping operational and analytical data in sync?"
   → *Listen for:* FTE time, pipeline maintenance, incidents
3. "When clinical teams need real-time data, how quickly can you deliver?"
   → *Listen for:* Hours/days vs minutes, manual processes

**Technical pain questions (light touch):**
4. "What's your current operational database? Aurora? RDS? On-prem Postgres?"
   → *Listen for:* Satisfaction level, pain with current solution
5. "How do you handle dev/test environments with production-like data?"
   → *Listen for:* Clone times, data masking challenges

---

## Discovery Framework ⏱️ 15-30min

### Opening — Situation Framing ⏱️ 2min

> "I've been working with healthcare data teams building patient-facing apps. Common pattern: lakehouse for analytics, but operational apps need sub-second queries. The bridge between them becomes a tax on engineering. Is that resonating?"

### Pain Discovery ⏱️ 10min

| Pain Area | Question | Signal to Listen For |
|-----------|----------|---------------------|
| **Data sync** | "Walk me through how lakehouse data gets to your operational apps today." | Manual pipelines, batch delays, freshness issues |
| **Engineering cost** | "How many engineers touch that pipeline? What else could they be doing?" | FTE allocation, opportunity cost |
| **Time to value** | "When a new use case comes up, how long from idea to production data access?" | Weeks/months = pain, days = less urgent |
| **Governance** | "How do you handle access controls across lakehouse and operational data?" | Dual systems, audit complexity, HIPAA concerns |
| **Dev velocity** | "How long to spin up a dev environment with realistic data?" | Hours = pain (Lakebase: seconds) |

### Value Articulation ⏱️ 3min

> "Based on what you've shared, here's what I'm hearing: [reflect their pain]. Teams in similar situations have eliminated [X] pipelines and freed up [Y] engineering weeks per quarter. Ensemble Health Partners went from 20-hour data sync to 4 minutes."

### Next Step Close ⏱️ 2min

> "The next step that makes sense: a technical deep-dive with my SA to map your architecture and see where Lakebase fits. Who else should be in that conversation?"

---

## Commercial Objections

**"We already have Aurora — why switch?"**
> "Aurora's great for operational workloads. The question is: how do you get lakehouse data INTO Aurora? Most teams build pipelines that take weeks to maintain. Lakebase eliminates that — Delta Sync keeps operational and analytical data in sync automatically. A global logistics provider cut app delivery time 90% by removing that integration tax."

**"This sounds expensive."**
> "Let's talk TCO. Lakebase customers typically see 70-80% cost savings vs over-provisioned dedicated Postgres. But the bigger number is engineering time — eliminating pipelines frees up weeks per quarter. A Fortune 500 healthcare org documented 20% efficiency improvement. What's a week of your data engineering team worth?"

**"We're not ready — this is a future initiative."**
> "Makes sense. What's the trigger that would make this a priority? HIPAA audit? New patient app launch? When that happens, the lead time to architect and pilot is 2-4 weeks. Happy to scope what that would look like so you're ready."

**"Our team doesn't know Databricks well enough."**
> "Fair concern. Two things: First, Lakebase is standard Postgres — your team's existing skills transfer. Second, healthcare customers typically start with a 2-week pilot on a non-PHI use case to build confidence. Low risk to validate the fit."

**"What about vendor lock-in?"**
> "Lakebase uses open formats — standard Postgres wire protocol, Delta Lake for storage. Your data stays portable. The value is in the integration, not the lock-in."

---

## Proof Points

> **Ensemble Health Partners** — Reduced data sync from 20+ hours to 4 minutes for Clinical Viewer application. Daily Lakebase spend: $900-1,000. Non-PHI deployment, expanding when HIPAA BAA available.

> **Fortune 500 Healthcare Provider** — 20% efficiency improvement and 5% revenue yield improvement after unifying operational and analytical data.

> **Global Logistics Provider** — 90% reduction in time to deliver production apps. 10-person team now supports 40+ applications through unified data platform.

> **Ibotta** — "Lakebase helped us simplify our data architecture and deliver near real-time experiences, enabling faster innovation across teams."

> **Heineken** — "Our analytical data platform is now evolving to be an operational AI data platform and needs to deliver insights to applications at low latency."

⚠️ *Ensemble metrics approved for internal use. Anonymize for external: "Fortune 500 healthcare provider."*

---

## vs Aurora/RDS

| Dimension | Lakebase | Aurora/RDS | Why It Matters |
|-----------|----------|-----------|----------------|
| **Lakehouse integration** | Native Delta Sync (10-15s) | Build your own pipelines | Weeks of engineering eliminated |
| **Governance** | Unity Catalog built-in | Separate IAM policies | One audit trail for HIPAA |
| **Dev environments** | Instant branching (seconds) | Clone (hours) | 10x faster dev cycles |
| **Scaling** | Serverless, scale to zero | Provisioned or Serverless v2 | Pay for what you use |
| **Postgres compatibility** | Full wire protocol, 60+ extensions | Full compatibility | No migration risk |

**Trap question for Aurora users:**
> "How many pipelines do you maintain between Aurora and your lakehouse today? What would you do with that engineering time if it went to zero?"

**Honest weakness:**
- HIPAA BAA not yet available — non-PHI pilots only for now
- Delta Sync is 10-15s, not real-time streaming (<1s)

---

## Qualification Scorecard

| Signal | 🟢 Strong | 🟡 Needs Work | 🔴 Walk Away |
|--------|----------|---------------|--------------|
| **Use case** | Operational app with lakehouse data need | Analytics-adjacent, could go either way | Pure BI/reporting |
| **Tech stack** | Databricks customer, Unity Catalog | Evaluating Databricks | Snowflake-committed |
| **Timeline** | Project in next 6 months | "Future initiative" with trigger | No timeline, no trigger |
| **Budget** | Allocated or path to allocation | Needs business case | No budget pathway |
| **Champion** | Named internal advocate | Interest but no champion | Passive recipients |

**MEDDIC Quick-Check:**
- **M**etrics: What does success look like? (sync time, engineering hours, cost)
- **E**conomic buyer: Who signs? (VP Eng, CTO, CDO)
- **D**ecision criteria: How will they evaluate? (POC success criteria)
- **D**ecision process: Timeline, stages, other vendors?
- **I**dentify pain: Confirmed and quantified?
- **C**hampion: Who's selling internally when you're not there?

---

## When to Bring in SA

**Bring in SA when:**
- ✓ Technical deep-dive requested (architecture review, POC scoping)
- ✓ Technical blocker identified (specific Postgres extension, performance requirement)
- ✓ Multiple technical stakeholders in next meeting
- ✓ Competitive technical evaluation (Aurora benchmark, feature comparison)
- ✓ Deal size >$200K ARR

**What to hand off:**
- Discovery notes (pain points in their words)
- Architecture context (current stack, data volumes, use cases)
- Technical stakeholders (names, titles, concerns)
- Competitive context (what else they're evaluating)
- Success criteria (what would make a POC successful)

**Positioning to prospect:**
> "For the technical deep-dive, I'd like to bring in [SA Name] who works with healthcare data architects. They can map your specific architecture and show you exactly how Lakebase would fit. Does [Day/Time] work?"

---

## Deal Sizing

| Component | Typical Range | Sizing Question |
|-----------|---------------|-----------------|
| **Compute** | $50-150K/yr | "How many concurrent connections? Query volume?" |
| **Storage** | $20-50K/yr | "Data volume in operational DB? Growth rate?" |
| **Professional Services** | $30-75K | "Migration complexity? Custom integrations?" |

**Back-of-napkin:** For a mid-size healthcare deployment (10-50 concurrent users, 1-5TB operational data): **$150-250K ARR** first year including services.

**Expansion motion:** Land with one use case (patient portal, clinical dashboard), expand to additional apps as they see value.

---

## Collateral by Stage

| Stage | Asset | When to Send |
|-------|-------|--------------|
| **Post-discovery** | [Lakebase One-Pager](#) | After qualifying, before technical deep-dive |
| **Pre-SA meeting** | [Technical Architecture Overview](#) | Day before SA call |
| **During evaluation** | [Customer Case Study](#) | When they ask "who else uses this?" |
| **POC kickoff** | [POC Success Criteria Template](#) | At POC scoping meeting |
| **Procurement** | [Security & Compliance FAQ](#) | When infosec gets involved |

---

*Generated via enablement-card-render | Role: ae | Output: self_contained | Sections: 11/12*
