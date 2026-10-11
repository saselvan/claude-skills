# Audience Adversarial Review

## Purpose

After an artifact (deck, email, one-pager, cheatsheet, enablement card, or newsletter) is rendered, conduct an audience perspective quality gate. A fresh agent assumes your target audience's role and assesses: What emotions will they feel? What knowledge will they gain? What actions will they take?

This is NOT a visual QA check (that's `deck-qa`). This is: "I am a VP Engineering with a 30-minute attention window and skepticism about new tools. Does this deck convince me to greenlight the pilot?"

## Usage

```
/audience-review [artifact-path] [audience-spec]
```

**Arguments:**
- `artifact-path` (required): Path to rendered artifact (deck.pptx, email.md, one-pager.pdf, etc.)
- `audience-spec` (optional): YAML-formatted audience persona. If omitted, read from strategy.yaml or manifest.

**Examples:**

```bash
# Review with audience persona from strategy
/audience-review Artifacts/nwm/deck/2026-04-18-operational-dashboards.pptx

# Review with explicit audience persona
/audience-review email.md "
audience_class: customer
motion_type: net_new
arc_template: challenger
persona:
  role: VP Engineering
  company: Northwestern Medicine
  pain: operational data quality
  skepticism: high (Snowflake incumbent)
"

# Review a cheatsheet from an SA peer perspective
/audience-review cheatsheet.pdf "
audience_class: sa_peer
arc_template: recognition_pattern_application
"
```

---

## Process

### Step 0: Load Artifact & Audience

**0a. Resolve Artifact Path**

Accept absolute or relative path. Supported formats:
- Deck: `.pptx`, `.pdf` (from pptxgenjs export)
- Email/Document: `.md`, `.html`
- PDF: `.pdf` (one-pager, cheatsheet, etc.)

If path is relative, resolve relative to `cwd` (current working directory at skill invocation).

**0b. Load Audience Persona**

**Option A: Explicit Persona (argument provided)**
Parse YAML from second argument. Required fields:
- `audience_class`: customer | partner | vp_internal | ae_enablement | sa_peer | bdr_enablement | technical_deepdive
- `arc_template`: challenger | why_evolve | opportunity | modified_challenger | recognition_pattern_application | proof_script_practice | technical_progressive
- `persona` (optional nested object): role, company, pain, skepticism, decision_authority, etc.

**Option B: From Strategy File (if artifact in engagement directory)**
If artifact path is `Artifacts/{account}/{type}/{date}-{title}.{ext}`:
1. Infer engagement directory from manifest
2. Load `strategy.yaml` from engagement directory
3. Extract `deck_mode` or `audience_class` + `arc_template`

**Option C: From Manifest (if provided in engagement)**
If strategy file not available, check manifest.yaml for audience context.

**Fallback:** If none available, ERROR with guidance on how to provide audience spec.

**Output:**
```yaml
artifact:
  path: {resolved_path}
  type: {deck|email|one_pager|cheatsheet|enablement_card|newsletter}
  size_kb: {file size}

audience:
  audience_class: {class}
  arc_template: {template}
  persona_summary: "{one-line summary of persona}"
```

---

### Step 1: Extract Artifact Content

**1a. For Decks (.pptx/.pdf)**

Extract slide-by-slide content:
- Slide title
- Bullet points / key text
- Visual descriptions (if accessible from PDF metadata)
- Speaker notes (if present in PPTX)

Output: Array of slides with text + visual summary.

**1b. For Email/Documents (.md/.html)**

Parse structure:
- Subject line (if .md has frontmatter)
- Greeting
- Each major section (problem, proof, proposal, etc.)
- Closing / CTA

Output: Structured sections with verbatim text.

**1c. For PDFs (one-pager, cheatsheet)**

Extract text via PDF library (pdfplumber or similar):
- Page-by-page text
- Section headers
- Tables / lists

Output: Full text content organized by page/section.

---

### Step 2: Spawn Fresh Agent with Audience Persona

**This is the core of adversarial review.** Spawn a new agent in an isolated context that assumes the audience role.

**Agent Instructions (Persona-Specific):**

The agent receives a system prompt that establishes it AS the audience member, with specific psychological framing:

**For VP Engineering (technical_deepdive):**
```
You are a VP Engineering at Northwestern Medicine with 30 minutes to review this deck.
You are skeptical of new tools and care deeply about operational risk.
Previous experience: Snowflake for 3 years, burned by a failed Databricks proof-of-concept in 2023.
Decision threshold: convinced that THIS (Lakebase) is better than doing nothing OR staying with Snowflake.

Read this deck with a critical eye. As you go through it:
1. Note emotions you feel at each step (skepticism, curiosity, confidence, risk)
2. List knowledge you gain (what you learn about Lakebase, the use case, the proposal)
3. Assess likelihood you'd commit to pilot (0-100%, with reasoning)

Be honest. If something doesn't land, say so. Don't be a cheerleader.
```

**For Customer VP (customer, net_new, challenger):**
```
You are a VP Operations at Northwestern Medicine, no prior Databricks exposure.
You care about operational efficiency and reducing manual data processes.
You are in a compliance-heavy industry and risk-averse.
You have 40 minutes to decide if you want to hear a deeper technical proposal.

Read this deck with the critical eye of a busy executive who's seen many vendor pitches.
1. Does this address MY specific pain, or is it generic?
2. What knowledge do I walk away with? (Can I explain this to my team?)
3. Am I more or less likely to move forward? (0-100% likelihood + reasoning)

Be skeptical. Vendor decks often gloss over implementation complexity or ROI assumptions.
```

**For AE Enablement (ae_enablement):**
```
You are an Account Executive covering mid-market healthcare providers.
You need to use this deck in a customer call next week.
Your concern: Can you deliver on what this deck promises? Will the customer call me out for overstatement?

Read this as a seller using it with a customer. Ask:
1. Am I confident explaining each slide in the customer's context?
2. Do I have backup for every claim? (Or am I wing-it-ing?)
3. Will the customer trust me after hearing this?

Be ruthless. If a slide looks oversold, flag it.
```

**For SA Peer (sa_peer, recognition_pattern_application):**
```
You are another Solutions Architect. This is supposed to be a pattern share — portable wisdom I can use with other customers.

As you read:
1. What pattern am I learning? (Can I articulate it to others?)
2. Is it specific to their account, or generalizable?
3. Would I use this in my next similar conversation?

Be direct. If it's account-specific fluff disguised as a pattern, say so.
```

Generate persona-specific instructions for each audience_class + role combination.

**Invocation:**
```
Task(
  subagent_type: "general-purpose",
  name: "audience-reviewer-{timestamp}",
  prompt: """
  {persona_system_prompt}

  ---

  HERE IS THE ARTIFACT YOU ARE REVIEWING:

  {artifact_content_formatted}

  ---

  PROVIDE YOUR ASSESSMENT IN THIS EXACT FORMAT:

  ## Emotions Felt

  [For each major section/slide, describe the emotional trajectory.
   e.g., "Slide 1 — I feel skeptical (another vendor pitch?). Slide 2 — Curiosity (wait, this is specific to our pain). Slide 4 — Doubt (is this really feasible?)."]

  ## Knowledge Gained

  [List 5-7 key insights you learned. For each: what it is, and whether you find it credible.]

  ## Actions You Will Take

  [Based on this artifact, what will you do?
   Examples:
   - "Ask for a technical deep-dive call"
   - "Forward to my architect for review"
   - "Politely decline and stay with Snowflake"
   - "Commit to a 2-week POC with guardrails"
   - "Need more proof on compliance/security before I'd consider it"]

  ## Confidence Score

  [On a scale of 0-100, how convinced are you to move forward? Include 1-2 sentence reasoning.]

  ## What Worked

  [1-2 things the artifact did well.]

  ## What Didn't Land

  [1-2 gaps, oversells, or confusing points.]

  ## If You Were Rewriting This

  [1-2 sentences on what you'd change.]
  """
)
```

---

### Step 3: Collect & Structure Feedback

**3a. Parse Agent Response**

Extract sections from agent output:
- Emotions Felt (verbatim)
- Knowledge Gained (list format)
- Actions You Will Take (specific commitments or next steps)
- Confidence Score (0-100 + reasoning)
- What Worked (strengths)
- What Didn't Land (gaps / oversells)
- If You Were Rewriting (suggestions)

**3b. Confidence Calculation**

Convert agent's confidence score to deal-health impact:
- 0-40: Red flag. This audience is unlikely to advance. Major rework needed.
- 41-70: Yellow. Audience interested but has concerns. Address "What Didn't Land" before next step.
- 71-100: Green. Audience convinced to move forward or deepened in their commitment.

**3c. Pattern Matching**

For each "What Didn't Land" point, classify the type of gap:
- **Credibility gap**: Agent doesn't believe the claim (needs proof/case study)
- **Relevance gap**: Content feels generic, not tailored to their pain
- **Complexity gap**: Oversimplified or overly dense
- **Execution gap**: Unclear how implementation would work in their environment
- **Risk gap**: Doesn't address compliance, security, or operational risk
- **Timeline gap**: Unclear timeline or unrealistic commitments

---

### Step 4: Generate Review Report

**4a. Summary Report (for artifact contributor)**

```yaml
audience_review:
  artifact:
    path: {path}
    type: {type}
  
  audience:
    persona: {persona_summary}
    confidence_score: {0-100}
    verdict: {red|yellow|green}
  
  emotions_felt: "{condensed emotional arc}"
  
  knowledge_gained:
    - "{insight 1}"
    - "{insight 2}"
    # ... 5-7 total
  
  actions_audience_will_take: "{specific next step or commitment}"
  
  strengths:
    - "{what worked 1}"
    - "{what worked 2}"
  
  gaps:
    - type: {gap_type}
      description: "{specific gap}"
      severity: {high|medium|low}
      fix: "{suggested fix}"
    # ... per gap
  
  rewrite_suggestion: "{1-2 sentence suggestion}"
  
  timestamp: {ISO8601}
```

**4b. Detailed Report (full agent response)**

Preserve full agent output for deeper review if needed.

---

### Step 5: Generate & Output

**5a. Write Review File**

Write summary to:
```
{artifact_directory}/{artifact_basename}-audience-review.yaml
```

Example:
```
Artifacts/nwm/deck/2026-04-18-operational-dashboards-audience-review.yaml
```

Also write full agent response to:
```
Artifacts/nwm/deck/2026-04-18-operational-dashboards-audience-review-FULL.md
```

**5b. Optional: Vault Sync**

If artifact has sidecar (.artifact.md), append review metadata:
```yaml
review_status: {pending|red|yellow|green}
review_confidence: {0-100}
review_timestamp: {ISO8601}
```

Call `vault_reindex(full=false, embed=false)`.

**5c. Report to User**

```markdown
## Audience Review Complete

**Artifact:** {artifact_path}
**Audience:** {persona_summary}

### Verdict

🟢 **GREEN** — Audience convinced to move forward ({confidence}%)

OR

🟡 **YELLOW** — Audience interested but has concerns ({confidence}%)
{gaps with fixes}

OR

🔴 **RED** — Major rework needed before next step ({confidence}%)
{critical gaps with rationale}

### Key Feedback

**What Worked:**
- {strength 1}
- {strength 2}

**What Didn't Land:**
- {gap 1}
- {gap 2}

**Rewrite Suggestion:**
{suggestion}

**Full Review:** {path to full report}
```

---

## Quality Gates

✓ Audience persona is unambiguous (audience_class + arc_template determine persona)
✓ Artifact is readable and extractable (PPTX → text, PDF → text, MD → parsed)
✓ Agent response follows expected format (5-7 key sections)
✓ Confidence score is justified (reasoning provided)
✓ Gaps are specific, not generic ("credibility gap: CEO salary claim not backed by case study" vs "doesn't feel credible")

---

## Integration with Rendering Skills

Rendering skills can optionally invoke audience review at the end:

```bash
# After /deck-render completes
/audience-review {deck_path}  # Audience from strategy.yaml
```

Or as part of a post-generation quality gate in content-factory:

```yaml
# In manifest, after deck artifact
quality_gates:
  - audience_review: true
```

Then content-factory invokes it automatically.

---

## Performance Notes

- Fresh agent spawn: 5-10 seconds overhead
- Agent reasoning time: 30-45 seconds (depends on artifact size)
- Total time: ~1 minute for a full deck review
- No parallelization (each audience is sequential)

---

## Common Personas (Shorthand)

When you don't provide explicit persona, shorthand audience_class triggers:

| audience_class | Default Persona | Pain Focus |
|---|---|---|
| customer | VP Engineering (net_new) or VP Ops (expand) | Operational efficiency, risk |
| technical_deepdive | Architect, 4+ years | Feasibility, integration, performance |
| vp_internal | VP Sales or VP Strategy | Pipeline, quota, competitive position |
| ae_enablement | Field AE | Credibility, sales confidence, proof |
| sa_peer | SA, 5+ years | Portability, pattern clarity, generalizable |
| partner | Systems integrator / consulting firm | Implementation complexity, margins, support |

---

## vault_speaker Integration (Production — W5 Cutover)

**Status:** PRIMARY (graduated from shadow mode)

vault_speaker is the primary context source for audience review, providing real stakeholder data to make the adversarial persona more accurate. Existing retrieval logic (strategy YAML, manifest) serves as fallback.

### At generation start:

1. Call vault_speaker: `/vault-speaker --intent retrieval --account {account_id}`
   - Only invoke when an account_id is available (account-specific artifacts). For generic artifacts, skip vault_speaker.
2. If vault_speaker succeeds (returns confidence != low): use its package as primary context
   - Stakeholder profiles, prior content outcomes, and likely objections come from vault_speaker
   - These enrich the adversarial persona with real data (actual pain points, known skepticism, prior interactions)
3. If vault_speaker fails or returns confidence=low: fall back to existing retrieval logic (strategy YAML + manifest + default personas)
4. Log outcome_tag to vault_speaker_invocations after generation completes

### Fallback behavior:

- vault_speaker timeout (>15s): use existing retrieval logic, log outcome_tag='timeout'
- vault_speaker error: use existing retrieval logic, log outcome_tag='error'
- vault_speaker confidence=low for all retrievers: use existing retrieval logic, log outcome_tag='low_confidence_fallback'
- No account_id available: skip vault_speaker, use default personas from audience_class

### What vault_speaker provides (when successful):

- **Stakeholder profiles**: real roles, pain points, skepticism levels, prior interactions
- **Prior content outcomes**: how previous artifacts landed (from artifact history)
- **Likely objections**: known concerns and pushback patterns from this account
- **Special**: Uses vault_speaker data to stress-test artifacts from a more realistic audience perspective

### What existing logic still owns (always):

- Artifact content extraction (Step 1)
- Adversarial agent spawning and persona construction (Step 2)
- Feedback collection and pattern matching (Step 3)
- Review report generation (Step 4)
- Verdict calculation (RED/YELLOW/GREEN)

### Logging:

After audience review completes, log the invocation to brain.db:
```python
import sqlite3, json, secrets
db = sqlite3.connect("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")
db.execute("""
    INSERT INTO vault_speaker_invocations
    (invocation_id, run_id, intent, scope, outcome_tag, latency_ms)
    VALUES (?, ?, 'retrieval', ?, ?, ?)
""", (
    secrets.token_hex(16), secrets.token_hex(16),
    json.dumps({"account_id": account_id, "skill": "audience-review"}),
    outcome_tag,  # 'success' | 'timeout' | 'error' | 'low_confidence_fallback' | 'skipped_no_account'
    latency_ms,
))
db.commit()
db.close()
```

---

## Limitations

- Cannot access embedded images/visuals from PPTX (only text extraction)
- Cannot review interactive elements (Gglide, Figma embeds, etc.)
- Persona may not perfectly match real customer (proxy, not substitute)
- Emotional assessment is agent interpretation (subjective)

---

## Why This Matters

Decks that pass visual QA can still fail with audience:
- Too technical for a buyer, too simplistic for an architect
- Emotionally dishonest (sounds desperate instead of confident)
- Oversells proof without acknowledging risk
- Assumes customer context they don't have

Audience review catches these before the deck is used in a customer call.
