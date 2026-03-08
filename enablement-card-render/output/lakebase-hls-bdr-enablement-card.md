# Lakebase HLS Quick-Start: BDR

**Last validated:** 2026-02-07 | **Quota credit:** 3× | **SPIF:** Active

---

## What You're Selling ⏱️ 10s

AI apps need two things: memory and instant data access. Lakebase is Databricks' managed database that gives patient chatbots both — no ETL pipelines to build.

**The pitch:**
> "We help healthcare teams build AI apps that remember patients and access your data instantly."

---

## Who To Call

| Title | Why They Care | Signal to Look For |
|-------|---------------|-------------------|
| Database Administrator | HIPAA compliance is getting harder. Backup scripting eats their week. | Posts about "HA", "backup", "Aurora", "HIPAA audit" |
| Software Engineer | Stuck building ETL pipelines between their app and the lakehouse. | Mentions "API", "FHIR", "integration", "data sync" |
| Platform Engineer | Dev environments take hours to clone. Testing is slow. | Talks about "environments", "CI/CD", "containers" |
| VP Engineering | Team is drowning in infrastructure work instead of building apps. | Hiring for data roles, posts about "technical debt" |

**LinkedIn Sales Navigator:**
- Title: "Database Administrator" OR "DBA" OR "Software Engineer" + Healthcare
- Company: >1K employees, hospitals, health systems, pharma
- Filter: "Databricks" or "lakehouse" in profile

---

## Cold Call — They Pick Up ⏱️ 10s opener

### Opening Hook
> "Hi [Name], this is [You] from Databricks. I work with healthcare teams building patient apps and AI chatbots. Do you have 2 minutes?"

### If They Engage — Discovery ⏱️ 2min
1. "Are you building any patient-facing apps or AI chatbots?"
2. "How do you get lakehouse data into your operational apps today?"
3. "How long does it take to spin up a dev environment with real data?"

### If They Push Back
*(See objection scripts below)*

---

## When They Push Back

**"We already have Aurora/RDS."**
> Aurora's great for apps. Quick question: how do you get lakehouse insights into Aurora without building pipelines? A global logistics provider cut app delivery time 90% by eliminating that sync work.

**"We're a Snowflake shop."**
> Totally fair. Are you building anything that needs sub-10ms response times? Snowflake's great for analytics, but patient apps need a different architecture.

**"Not building operational apps right now."**
> Got it. Any patient portals or AI projects on the roadmap in the next 6 months? If not, I can reach back when timing's better — who should I follow up with?

**"We don't have budget."**
> Not looking to close anything today. A Fortune 500 healthcare org saw 20% efficiency gains — those numbers help build the case. Worth a 15-minute call to see if there's even a fit?

**"Send me an email."**
> Happy to. Quick question so I send the right thing: are you more focused on database infrastructure or application development?

---

## Proof Points to Drop

> "A global logistics provider saw **90% reduction in app delivery time** — 10-person team now supports 40+ apps."

> "Ibotta's team said Lakebase helped them **simplify their data architecture and deliver near real-time experiences**."

> "A Fortune 500 healthcare provider documented **20% efficiency improvement** and **5% revenue yield improvement**."

> "Heineken's data lead said they needed to deliver insights to apps at **low latency** — that's exactly what we solved."

⚠️ *Use company names internally only. Anonymize for external comms.*

---

## Qualification — Quick Check

| Signal | Criteria |
|--------|----------|
| 🟢 | Existing Databricks customer with Unity Catalog |
| 🟢 | Building patient apps, AI chatbots, or real-time dashboards |
| 🟢 | Currently using or evaluating PostgreSQL |
| 🟡 | No Postgres experience (can learn, adds ramp) |
| 🟡 | Data volumes >8TB (needs architecture discussion) |
| 🔴 | Analytics-only workload (not operational apps) |
| 🔴 | Committed to Snowflake with no lakehouse roadmap |
| 🔴 | GCP requirement (not supported today) |

---

## Handoff to AE

**When to hand off:**
- Persona confirmed (DBA, Engineer, or VP)
- Specific operational use case identified (not just "interested")
- Timeline <6 months
- Budget pathway identified

**What to include:**
- [ ] Contact name, title, company
- [ ] Which use case resonated (patient app, chatbot, dashboard)
- [ ] Their current stack (Aurora, RDS, on-prem Postgres)
- [ ] Timeline and any deadline pressure
- [ ] Objections raised and how they landed

**Positioning to the prospect:**
> "Based on what you shared, I'd like to connect you with [AE Name] who works with healthcare teams on exactly this. They can show you how [similar customer] handled [their specific use case]. Does [Day/Time] work for a 15-minute call?"

---

## Voicemail ⏱️ 30s

> "Hi [Name], [Your name] from Databricks. I work with healthcare DBAs building patient-facing apps. Saw your team uses Databricks — wondering if you're stuck syncing data between your operational database and the lakehouse. We helped a Fortune 500 healthcare org cut that work significantly. My number is [number]. Also sending an email with a quick one-pager. Talk soon."

---

## LinkedIn DM

> "[Name], saw you're at [Company] working on [data/engineering]. Quick question: building any patient apps that need lakehouse data at low latency? Happy to share how similar teams eliminated their ETL pipelines."

---

📎 **Collateral:**
- **After qualifying call:** [Lakebase One-Pager](#)
- **Before AE meeting:** [Customer Brief](#)

---

*Do NOT promise: real-time streaming (<1s), PHI production readiness, specific customer names externally.*
*Delta Sync = 10-15 second latency, not sub-second.*

---

*Generated via enablement-card-render | Role profile: bdr | Depth: shallow | Sections: 8/8*
