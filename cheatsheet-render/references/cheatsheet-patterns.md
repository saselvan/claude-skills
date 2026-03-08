# Cheat Sheet Patterns

> Philosophy tells you WHY. This file tells you HOW. Every template here is copy-paste ready.

---

## 1. Card Layout Templates

### 1A. Standard 3-Column Grid (9 Cards — Desktop)

The default layout. 3 columns × 3 rows = 9 cards. Single viewport, no scrolling.

```
┌─────────────────┬─────────────────┬─────────────────┐
│   CARD 1        │   CARD 2        │   CARD 3        │
│   (Highest      │   (High         │   (High         │
│    priority)    │    priority)    │    priority)    │
├─────────────────┼─────────────────┼─────────────────┤
│   CARD 4        │   CARD 5        │   CARD 6        │
│   (Medium       │   (Medium       │   (Medium       │
│    priority)    │    priority)    │    priority)    │
├─────────────────┼─────────────────┼─────────────────┤
│   CARD 7        │   CARD 8        │   CARD 9        │
│   (Lower        │   (Lower        │   (Reference/   │
│    priority)    │    priority)    │    meta)        │
└─────────────────┴─────────────────┴─────────────────┘
```

**Placement rules (Nielsen F-pattern):**
- Top-left (Card 1): Highest-frequency lookup item
- Top row: The 3 things the user reaches for most often
- Bottom-right (Card 9): Metadata, version info, or "about this sheet"
- Read priority: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

### 1B. Compact 4-Column Grid (12 Cards — Wide Desktop)

For domains with more surface area. 4 columns × 3 rows = 12 cards. Use only when 9 cards genuinely can't cover the domain.

```
┌────────────┬────────────┬────────────┬────────────┐
│  CARD 1    │  CARD 2    │  CARD 3    │  CARD 4    │
├────────────┼────────────┼────────────┼────────────┤
│  CARD 5    │  CARD 6    │  CARD 7    │  CARD 8    │
├────────────┼────────────┼────────────┼────────────┤
│  CARD 9    │  CARD 10   │  CARD 11   │  CARD 12   │
└────────────┴────────────┴────────────┴────────────┘
```

**Warning:** 12 cards is the absolute maximum (Miller). Beyond this, users can't hold the card taxonomy in memory and will resort to sequential scanning, defeating the purpose.

### 1C. Responsive Breakpoints

```
Desktop (>1024px):  3-column or 4-column grid
Tablet (768-1024px): 2-column grid
Mobile (<768px):     1-column stack (with sticky card-title nav)
```

---

## 2. Card Type Templates

### 2A. "When You Hear X → Think/Do Y" Card

The signature cheat sheet pattern. Bridges domain triggers to user actions.

```
┌─────────────────────────────────────────────────────┐
│  🔊 TRIGGER → RESPONSE                             │
├──────────────────────┬──────────────────────────────┤
│  When you hear...    │  Think / Say / Do...         │
├──────────────────────┼──────────────────────────────┤
│  "[domain term]"     │  → This means [translation]. │
│                      │    Ask: "[discovery question]"│
├──────────────────────┼──────────────────────────────┤
│  "[customer phrase]" │  → They care about [pain].   │
│                      │    Try: "[talk track]"        │
├──────────────────────┼──────────────────────────────┤
│  "[objection]"       │  → Counter: "[reframe]"      │
│                      │    Proof: [metric + date]     │
└──────────────────────┴──────────────────────────────┘
```

**Rules:**
- Left column: exact phrases the user will hear (in quotes)
- Right column: always starts with → and ends with a concrete action (ask/say/do)
- Right column verbs must be imperative: Ask, Say, Try, Counter, Lead with. Never passive ("This means..." without a follow-up action).
- Maximum 6 trigger-response pairs per card
- If you need more than 6, split into two cards by theme

### 2B. Jargon Decoder Card

Three-column lookup: what the term is, what it means, and what to do with it.

```
┌─────────────────────────────────────────────────────┐
│  📖 JARGON DECODER: [Domain]                        │
├──────────┬───────────────────┬──────────────────────┤
│  Term    │  Meaning          │  Your Angle          │
├──────────┼───────────────────┼──────────────────────┤
│  [term]  │  [plain English]  │  → [action/play]     │
├──────────┼───────────────────┼──────────────────────┤
│  [term]  │  [plain English]  │  → [action/play]     │
└──────────┴───────────────────┴──────────────────────┘
```

**Rules:**
- "Meaning" column: explain like the user has never encountered this term
- "Your Angle" column: always starts with → and connects to what the user can DO with this knowledge
- Sort alphabetically or by frequency (frequency preferred for <10 terms)
- Maximum 10 terms per card

### 2C. Persona Card

Who the user will encounter and how to engage them.

```
┌─────────────────────────────────────────────────────┐
│  👤 PERSONAS: [Domain/Account]                      │
├──────────────┬──────────────────┬───────────────────┤
│  Role        │  Cares About     │  Your Play        │
├──────────────┼──────────────────┼───────────────────┤
│  [Title]     │  • [priority 1]  │  → Lead with      │
│              │  • [priority 2]  │    [angle]         │
├──────────────┼──────────────────┼───────────────────┤
│  [Title]     │  • [priority 1]  │  → Lead with      │
│              │  • [priority 2]  │    [angle]         │
└──────────────┴──────────────────┴───────────────────┘
```

**Rules:**
- "Cares About" = their top 2 priorities (not a comprehensive list)
- "Your Play" = what to lead with in the first 60 seconds of conversation
- Maximum 5 personas per card
- Ordered by frequency of encounter (most common first)

### 2D. Discovery Questions Card

Questions organized by conversation phase, not by topic.

```
┌─────────────────────────────────────────────────────┐
│  ❓ DISCOVERY STARTERS: [Domain]                    │
├─────────────────────────────────────────────────────┤
│  🟢 OPENERS (first 5 minutes)                      │
│  • "[question]"                                     │
│  • "[question]"                                     │
├─────────────────────────────────────────────────────┤
│  🔵 DEEPENERS (mid-conversation)                    │
│  • "[question]"                                     │
│  • "[question]"                                     │
├─────────────────────────────────────────────────────┤
│  🟠 CLOSERS (last 5 minutes)                        │
│  • "[question]"                                     │
│  • "[question]"                                     │
└─────────────────────────────────────────────────────┘
```

**Rules:**
- Questions are in quotes (ready to say verbatim)
- Organized by WHEN in the conversation, not WHAT topic
- 2-3 questions per phase, 6-9 total per card
- Openers = broad/safe; Deepeners = specific/probing; Closers = commitment/next-step

### 2E. Metrics / Proof Points Card

Named statistics with attribution and dates for credibility.

```
┌─────────────────────────────────────────────────────┐
│  📊 METRICS TO NAME-DROP                            │
├─────────────────────────────────────────────────────┤
│  💰 [Metric]: [number + unit]                       │
│     Source: [attribution] ([date])                  │
│     → Use when: [trigger scenario]                  │
├─────────────────────────────────────────────────────┤
│  📈 [Metric]: [number + unit]                       │
│     Source: [attribution] ([date])                  │
│     → Use when: [trigger scenario]                  │
└─────────────────────────────────────────────────────┘
```

**Rules:**
- Every number has a source and date (undated metrics lose credibility)
- "Use when" connects the metric to a conversation trigger
- Maximum 5 metrics per card (more = nothing stands out)
- Bold the number itself — it's the hero element

### 2F. Decision Tree / If-Then Card

For heuristic/diagnostic moments (Rossett's "coaching" job aid type).

```
┌─────────────────────────────────────────────────────┐
│  🔀 DECISION: [Scenario Name]                      │
├─────────────────────────────────────────────────────┤
│  IF [condition A]                                   │
│    → DO [action A]                                  │
│                                                     │
│  IF [condition B]                                   │
│    → DO [action B]                                  │
│                                                     │
│  IF [condition C] AND [condition D]                  │
│    → DO [action C], THEN [action D]                 │
│                                                     │
│  IF UNSURE                                          │
│    → ASK: "[safe fallback question]"                │
└─────────────────────────────────────────────────────┘
```

**Rules:**
- Always include an "IF UNSURE" fallback — the user needs an escape hatch
- Conditions use the user's observable inputs (what they hear, see, or know)
- Actions use imperative voice: DO, ASK, SAY, RUN, ESCALATE
- Maximum 5 branches per card (more = use a flowchart instead)

### 2G. Checklist Card (Gawande)

For DO-CONFIRM (post-task verification) or READ-DO (step-by-step execution) patterns.

```
┌─────────────────────────────────────────────────────┐
│  ✅ [CHECKLIST NAME] — [DO-CONFIRM or READ-DO]      │
│  Pause point: [When to run this checklist]          │
├─────────────────────────────────────────────────────┤
│  □ [Killer item 1]                                  │
│  □ [Killer item 2]                                  │
│  □ [Killer item 3]                                  │
│  □ [Killer item 4]                                  │
│  □ [Killer item 5]                                  │
└─────────────────────────────────────────────────────┘
```

**Rules:**
- 5-9 items maximum (Gawande). Only include steps that, if missed, cause real failure.
- Explicitly label as DO-CONFIRM or READ-DO
- Define the pause point: WHEN should the user pull out this checklist?
- Items use imperative voice: "Verify [X]," "Confirm [Y]," "Check [Z]"

---

### 2H. Warning Banner Card

For compliance, liability, or "stop before you start" constraints that must be seen before any card content.

```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️ [CONSTRAINT] — [consequence] • [safe path]              │
└─────────────────────────────────────────────────────────────┘
```

**Rules:**
- Full width, above the card grid (not inside a card)
- One line maximum: constraint + consequence + safe alternative
- Red/amber accent to signal "read this first"
- Format: `⚠️ [WHAT'S RESTRICTED] — [WHY / CONSEQUENCE] • [WHAT TO DO INSTEAD]`
- Maximum 1 warning banner per sheet (if you need more, you have a compliance problem, not a cheat sheet problem)

**Example:**
```
⚠️ AZURE AUTOSCALING: NO BAA — do not pitch for PHI • Start non-PHI to prove value
```

---

## 2I. Card Type Decision Framework

When assembling a sheet, use this mapping to select the right template for each piece of content:

| You have... | Use card type... | Because... |
|---|---|---|
| Vocabulary / acronyms the user won't know | **Jargon Decoder (2B)** | Three-column lookup: term → meaning → action |
| Phrases the user will hear in conversation | **Trigger-Response (2A)** | Bridges what they hear to what they should do |
| People/roles the user will encounter | **Persona (2C)** | Maps who → what they care about → your play |
| Questions the user should ask | **Discovery Questions (2D)** | Organized by conversation phase, not topic |
| Statistics or proof points to cite | **Metrics (2E)** | Attributed, dated, with "use when" triggers |
| Branching logic ("if X then Y") | **Decision Tree (2F)** | Explicit branches with fallback escape hatch |
| Steps that must not be skipped | **Checklist (2G)** | 5-9 killer items with defined pause point |
| Compliance, liability, or beta-feature constraints | **Warning Banner (2H)** | Full-width alert above grid: constraint + consequence + safe path |
| Objections or competitive counters | **Trigger-Response (2A)** | Objections ARE triggers — same hear→think→do |
| Systems, tools, or architecture components | **Jargon Decoder (2B)** variant | System → What It Does → Your Angle |
| Error codes or troubleshooting | **Decision Tree (2F)** | Symptom → diagnosis → fix |

**If you're unsure:** Default to Trigger-Response (2A). It's the most versatile card type and works for any content that can be framed as "when [input] → do [action]."

---

## 3. Formulas

### Title Formula
```
[Action/Object Keyword] + [Scope/Domain Qualifier]
```
Examples:
- "EDI Transactions: Key Codes"
- "Personas: Data Platform Team"
- "Objection Responses: Security & Compliance"
- "Troubleshooting: Auto Loader Failures"

### Talk Track Formula
```
"[Empathy/Acknowledgment], [Bridge to Insight], [Proof Point], [Question/CTA]"
```
Example:
- "That's a common challenge — we've seen [X% of customers] hit the same issue. [Customer Y] solved it by [approach]. Would it help to walk through how they did it?"

### Trigger-Response Formula
```
HEAR: "[exact phrase]" → THINK: [what it means] → DO: [your action]
```
Example:
- HEAR: "We're stuck on 835 reconciliation" → THINK: Claims payment matching problem → DO: Ask "What's your current denial rate, and where does the manual work happen?"

---

## 4. Tailoring Matrix

Adapt card selection and density based on the audience parameters from the strategy contract.

| Parameter | Adjustment |
|-----------|------------|
| **Role: AE** | Prioritize: trigger-response, objection handling, metrics. De-prioritize: technical deep-dives, troubleshooting. |
| **Role: SA** | Prioritize: jargon decoder, architecture patterns, discovery questions. Include: technical decision trees. |
| **Role: DBA/Engineer** | Prioritize: commands, troubleshooting steps, error code lookup. De-prioritize: talk tracks, personas. |
| **Role: CSM** | Prioritize: health signals, expansion triggers, renewal prep. Include: persona cards for existing contacts. |
| **Moment: Apply** | Maximum density, minimum context. Every card = action. Strip all "why." |
| **Moment: Remember** | Medium density. Include brief context cues to reactivate prior knowledge. |
| **Moment: Learn New** | Lower density per card (more whitespace). Include inline definitions. Allow more cards. |
| **Experience: Expert** | Fewer cards, higher density, abbreviations okay, no inline definitions. |
| **Experience: New to domain** | More cards allowed (up to 12), lower density per card, all terms defined inline. |

---

## 5. Quality Gate Checklist

Binary pre-delivery checks. Every item must pass before the cheat sheet ships.

| # | Gate | Check |
|---|------|-------|
| 1 | **Single viewport** | Does the entire sheet fit on one screen without scrolling? (Desktop: 1440×900 viewport) |
| 2 | **5-second test** | Can a first-time viewer identify the right card for a given scenario in <5s? |
| 3 | **Title scan** | Reading ONLY card titles: can you tell what every card is about? |
| 4 | **Action audit** | Does every card contain at least one DO/SAY/ASK/RUN action? |
| 5 | **Self-containment** | Can every card be understood without referencing another card? |
| 6 | **Chunk count** | Is every card ≤9 items? Is the total ≤12 cards? |
| 7 | **Color audit** | Are ≤4 colors used? Does each color have exactly one semantic meaning? |
| 8 | **Jargon check** | Are all domain-specific terms defined inline or in a decoder card? |
| 9 | **Freshness** | Does the footer show version date, owner, and update trigger? |
| 10 | **Audience fit** | Does the density and action type match the strategy contract's role + moment? |

---

## 6. Anti-Patterns (Tactical)

| Mistake | Example | Fix |
|---------|---------|-----|
| **Passive card titles** | "Overview of Key Concepts" | → "Key Concepts: [Domain]" (front-load the keyword) |
| **Orphan facts** | "The 837 is a claim transaction." (no action) | → "837 = Claim submission. → Ask: 'Are you using 837P (professional) or 837I (institutional)?'" |
| **Wall-of-text card** | A card with 3+ sentences of prose | → Break into bullet points. If it needs prose, it belongs in the field guide, not the cheat sheet. |
| **Decorative icons** | Using 🏥🔬💊 on every card for visual flair | → Icons only if they aid scanning (category markers). One icon style, used consistently. |
| **"See also" references** | "For more detail, see the Field Guide section 3.2" | → Either include the essential info inline or cut it. The user won't leave mid-call. |
| **Undated metrics** | "Customers see 40% improvement" | → "40% reduction in processing time (Customer X, Q3 2024)" — source + date or delete. |
| **Role-specific jargon** | Using "ARR" without defining it on an SA cheat sheet | → Define inline: "ARR (Annual Recurring Revenue)" or use full term. |
