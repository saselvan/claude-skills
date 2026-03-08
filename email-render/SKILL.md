---
name: email-render
description: "Draft follow-up emails from session context. USE WHEN: user says 'draft email', 'email [account]', 'send follow-up', or when /email command is invoked. Takes session notes and vault context as input. Produces ready-to-send email drafts in Artifacts/Emails/ with prep notes and frontmatter metadata."
allowed-tools: Read, Write, Bash, Task, Glob, Grep
---

# Email Render

You draft emails that get sent, not emails that get procrastinated. Every draft is copy-paste ready for Gmail — no placeholders, no "we should probably..." hedging. Specific names, specific dates, specific commitments.

## Before Writing Any Draft

**Read BOTH reference files. They serve different purposes:**

1. `references/email-philosophy.md` — **Expert judgment.** 8 core principles, 9 email types with structures, tone calibration rules, quality gates, anti-patterns. Use BEFORE and DURING drafting to get voice, structure, and word count right.
2. `references/email-patterns.md` — **Tactical patterns.** Subject line formulas, BLUF templates, prep notes schema, Challenger tailoring matrix, relationship depth signals. Use DURING drafting for specific phrasings and framings.

Do not skip either. The philosophy tells you WHAT to write. The patterns tell you HOW to phrase it.

### Audience Tailoring Engine (HLS domains)

If the email recipient or account involves healthcare/HLS/clinical context, read the shared tailoring map:

```
_System/tailoring/hls-tailoring-map.yaml   (relative to workspace/vault root)
```

This file defines 4 audience profiles (`clinical_executive`, `technical_gatekeeper`, `commercial_lead`, `customer_success`). Match the recipient's role to the closest profile and use its `lava_element` for the hero proof point to lead with, its `kill_list` to avoid irrelevant technical depth (e.g., don't mention FHIR flattening to a CFO), and its `mental_model` for framing (e.g., "The Nurse's Station" for clinical executives).

## Board Read Protocol (Coordinated Mode)

Check for a `_meta.board_dir` field. Since email-render doesn't consume strategy contracts, the coordinator passes `_meta.board_dir` via `context.yaml` in the board directory. Specifically: read `{board_dir}/context.yaml` (where `board_dir` is provided by the coordinator in the invocation prompt, e.g., "Board directory: .pipeline/post-meeting/"). If `context.yaml` exists and contains `_meta.board_dir`, you are in coordinated mode.

**If `_meta.board_dir` is present** — you are running inside a coordinator pipeline (typically post-meeting):
1. Read `{board_dir}/context.yaml` (post-meeting coordinator). This provides pre-extracted session intelligence:
   - `action_items` — what was committed, by whom, by when
   - `commitments` — ours-to-them and theirs-to-us
   - `open_questions` — questions that need researched answers
   - `attendees` — full attendee list with roles
   Use this instead of re-parsing the session file. The coordinator already extracted this.
2. Read `{board_dir}/board/draft-followup-output.yaml` if it exists (draft-followup ran before email-render). This tells you:
   - Which action items are already covered by the session recap email
   - Which leave-behind items are queued
   - `action_items_from_session` — the full list for coverage checking
   Use this to AVOID duplicating what draft-followup already handled. email-render handles action-thread emails for specific commitments that aren't covered by the general recap.
3. Read `{board_dir}/board/` for any other prior skill outputs that provide context.

**If `_meta.board_dir` is absent** — standalone mode. Skip this section entirely. Zero cost.

> **Note:** Email-render discovers board context via `context.yaml` in the board directory, not via `_meta.board_dir` in a strategy contract. This differs from other render primitives (deck, cheatsheet, one-pager, enablement-card) which read `_meta.board_dir` from the strategy contract. Coordinators should ensure `context.yaml` is present in the board directory when invoking email-render.

## Board Write Protocol (Coordinated Mode)

**Only when `_meta.board_dir` is present.** Execute this AFTER Step 9 (Reindex) and BEFORE presenting the output summary.

Write a board entry to `{board_dir}/board/email-render-output.yaml`. If the coordinator invokes email-render multiple times (e.g., once per uncovered action item), each invocation should APPEND its `emails_drafted` entries to the existing file rather than overwriting. Read the file first — if it exists, merge the new entries into the existing YAML (append to `emails_drafted`, `action_items_addressed`, update `quality_score`/`quality_max`). If it does not exist, create it:

```yaml
skill_name: "email-render"
invoked_at: "{ISO 8601 timestamp}"
invoked_by: "{coordinator name from _meta.coordinator}"

artifact_path: "{absolute path to Artifacts/Emails/ directory containing drafts}"
artifact_type: "email"

# What emails were produced
emails_drafted:
  - recipient: "{full name}"
    email_type: "{follow_up|deliverable|research_answers|introduction|scheduling|check_in|decline_redirect|insight_share|reactive_response|group_follow_up}"
    subject: "{subject line}"
    word_count: N
    priority: "{high|medium|low}"
    due_date: "{YYYY-MM-DD}"
    gmail_draft_created: true/false
    thread_check: "{clear|recently_sent|active_thread}"
    file_path: "{absolute path to draft .md}"

# Coverage tracking (critical for post-meeting coordinator consistency check)
action_items_addressed:
  - action: "{action item text}"
    email_to: "{recipient}"
    email_type: "{type}"
action_items_remaining:
  - action: "{action item NOT covered by any email}"
    reason: "{why — e.g., 'no recipient identified', 'internal-only action', 'already handled by draft-followup'}"

# Quality from existing Q1-Q14 gate
quality_score: N                        # count of emails with CLEAN verdict
quality_max: N                          # total emails drafted
quality_pass: true/false                # all CLEAN?
quality_notes: ""
emails_with_warnings: []                # list of {recipient, failed_gates: [Q1, Q5, ...]}

# Amendments
strategy_contract_amendments: []
discovered_entities: []
coverage_gaps: []

recommendations_for_downstream: []  # email-render is terminal — no downstream skills
```

**Write rules:**
- **New invocation** (coordinator calling email-render for another action item): Read existing `email-render-output.yaml`, merge new `emails_drafted` entries into the existing list, write the merged result.
- **Retry of SAME invocation** (quality gate failed, coordinator asked to retry): Overwrite the entire file with the corrected output.
- **File does not exist**: Create it with the Write tool.

To distinguish: if the coordinator passes `retry_of: "{previous_email_subject}"` in the invocation context, treat as retry (overwrite). Otherwise treat as new invocation (merge).

**Deduplication on merge**: When appending (new invocation), check for existing entries with the same `recipient` + `email_type` combination. If found, **replace** the existing entry with the new one (the new invocation supersedes). Only truly new recipient+type pairs get appended. This prevents duplicate entries when a coordinator retries a specific action item without passing `retry_of`.

**If `_meta.board_dir` is absent** — skip board write entirely. Do not create any files.

## Gmail Integration (Optional)

At workflow start, check Gmail availability:

```bash
# Ensure gcloud is on PATH (required for Gmail API auth)
export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"

# Test with a lightweight Gmail search — if this succeeds, Gmail is available
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py search --query "newer_than:1h" --max-results 1 2>/dev/null
```

- If exit code 0 → set `GMAIL_AVAILABLE = true` — enables Steps 1g, 1h, enhanced 4c, and 8c
- If non-zero → set `GMAIL_AVAILABLE = false` — fall back to vault-only behavior. In the output summary, report `Gmail status: ❌ Unavailable — drafts saved to vault only`

**Gmail tool path:** `~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py`
**Requires:** `export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"` (gcloud for API auth)

**Hard rules:**
- NEVER send emails — only search, read, and create drafts
- Vault remains source of truth — Gmail draft is a convenience copy
- User hits send manually from Gmail UI
- No Gmail modifications — don't modify labels, delete, trash, or alter existing emails
- If any Gmail command fails, log it and continue — never fail the workflow

## Input Modes

### Mode 1: From Account (scans latest session)
```
/email [account]                    # Draft all pending emails for latest session
/email [account] [session-date]     # Draft emails from a specific session
```

### Mode 2: By Email Type
```
/email followup [account]           # Meeting follow-up recap
/email deliverable [person] [topic] # Send a specific deliverable
/email answers [account]            # Send researched answers to open questions
/email intro [person-a] [person-b]  # Warm introduction
/email nudge [person]               # Check-in on overdue item
/email schedule [person] [topic]    # Propose a meeting
/email decline [person] [topic]     # Graceful redirect
/email insight [person] [topic]     # Share relevant insight
/email respond [person] [topic]     # Reply to their input
```

### Mode 3: Sweep All
```
/email all                          # Draft all pending emails across all accounts
```

## Workflow: Per-Email Draft-Check Loop

This is the core workflow. Do not batch-generate without checking each draft.

### Step 1: Gather Context

**For account-based drafting (`/email [account]`):**

```
1. vault_summary(account) → stakeholders, recent sessions, open signals
2. vault_signals(account, signal_type="commitment", status="open") → what we owe
3. vault_signals(account, signal_type="action_item", status="open") → action items
4. Read latest session note → Sessions/[account]/[type]/[date].md
5. Read account file → Accounts/[account].md (for account_culture, nudge_threshold_days)
6. Read recipient stakeholder files → People/clients/[name].md (for relationship depth)
7. Check existing drafts → Artifacts/Emails/ (prevent duplicates)
```

#### 1f. Attendee Sanity Check (defensive)

After reading the session note, verify `attendees_external` is populated:

- **If populated:** Proceed normally.
- **If empty but session body describes a conversation** (names mentioned, dialogue present): Warn the user: `⚠️ Session has no attendees_external but appears to be a meeting transcript. Infer attendees? [list names found in body]`. Infer and proceed if user confirms, or auto-infer if running in batch (`/email all`).
- **If empty and session body has no conversation signals:** Skip this session for email generation. Log: `Skipped [session] — no attendees and no conversation detected.`

This prevents the silent-failure mode where a session exists but upstream `/process-transcript` didn't tag attendees, resulting in zero drafts with no explanation.

#### 1g. Resolve Recipient Email (if GMAIL_AVAILABLE)

For each recipient identified in context gathering:

1. **Vault first**: Read stakeholder file `People/clients/[name].md` → check `email:` frontmatter field
2. **Gmail fallback**: If vault email is empty and GMAIL_AVAILABLE:
   ```bash
   python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py search --query "to:[Full Name]" --max-results 3
   ```
   Parse the results to extract the recipient's email address from matching messages.
3. **Unknown fallback**: If neither works, set `recipient_email: unknown` — skip Gmail draft creation later, flag with `⚠️ VERIFY: No email found for [Name]`

#### 1h. Gmail Thread Intelligence (if GMAIL_AVAILABLE)

For each recipient with a resolved email, fetch recent email history:

- **Last sent:**
  ```bash
  python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py search --query "from:me to:[email] newer_than:30d" --max-results 1
  ```
- **Last received:**
  ```bash
  python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py search --query "from:[email] to:me newer_than:30d" --max-results 1
  ```

Extract from results: date, subject, snippet, messageId, threadId. Store for use in Steps 4c (thread check), 4d (drafting context), 4g (prep notes), and 8c (Gmail draft threading).

**For person-based drafting (`/email deliverable [person]`):**

```
1. vault_entity_lookup(name, entity_type="person") → find person
2. vault_graph(source_id="person:[slug]", depth=1) → connected sessions, account
3. Read person file → relationship depth, preferences
4. Read relevant session → what was discussed
```

### Step 2: Classify Email Type

For each action item or commitment where owner = "us" / "Samuel":

| Action Text Pattern | Email Type | Type Code |
|---------------------|-----------|-----------|
| "send [X] to [person]" | Deliverable | `deliverable` |
| "answer [person]'s questions" / "send answers" | Research/Answers | `research_answers` |
| "connect [A] with [B]" / "introduce" / "loop in" | Introduction | `introduction` |
| "schedule [meeting] with [person]" | Scheduling | `scheduling` |
| "decline [request]" / "redirect [person]" | Decline/Redirect | `decline_redirect` |
| "respond to [person]'s [email/doc/question]" | Reactive Response | `reactive_response` |
| default + multiple attendees (3+) | Group Follow-Up | `group_follow_up` |
| default + single attendee | Meeting Follow-Up | `follow_up` |
| Overdue "they owe" item past threshold | Check-In/Nudge | `check_in` |

**Insight Share** (Type 8) is only generated during `/email all` sweeps when relevant research exists and no insight was sent to this person in the last 7 days.

### Step 3: Determine Relationship Depth

Query `vault_graph(source_id="person:[slug]")` and count session edges:

| Session Count | Depth | Tone Effect |
|--------------|-------|-------------|
| 0-1 | `new` | More formal. Include title/role context. |
| 2-5 | `working` | Default warm professional. First names. |
| 5+ | `champion` | Direct, even terse. Drop pleasantries. |

### Step 4: Draft Each Email

For each email, apply the philosophy doc rules. This is the per-draft loop:

#### 4a. Look up recipient
- Read `People/clients/[name].md` or `People/internal/[name].md`
- Determine relationship depth (Step 3)
- Determine recipient type: technical | manager | executive | clinical | internal
- Apply tone adjustments per philosophy doc → `references/email-philosophy.md` Tone Calibration section

#### 4b. Check account culture
- Read `Accounts/[name].md` → `account_culture` section
- Check preferred communication channel
- Check nudge_threshold_days if drafting Type 5

#### 4c. Check for active threads
- **Vault check (always):** Check `Artifacts/Emails/` for recent drafts to same person on same topic
- **Gmail check (if GMAIL_AVAILABLE and recipient email resolved):**
  ```bash
  python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py search --query "from:me to:[email] newer_than:7d" --max-results 5
  ```
- **Decision matrix:**

  | Gmail Result | thread_check | Action |
  |---|---|---|
  | Same topic sent in last 48h | `active_thread` | Suppress draft |
  | Same topic sent 48h–7d ago | `recently_sent` | Draft proceeds + warning in prep notes |
  | Different topic or no results | `clear` | Draft proceeds normally |
  | Gmail unavailable | vault-only result | Current behavior (vault Artifacts/Emails/ check only) |

- If a matching Gmail thread is found, store `gmail_thread_id` and `gmail_message_id` for use in Step 8c (reply threading)

#### 4d. Draft the email body
- Use the type-specific template from philosophy doc
- **BLUF first sentence** — no exceptions
- Stay within type-specific word target (see philosophy doc Principle 5). If `to_type = technical` AND answering 3+ questions, apply technical depth escalation.
- No wiki-links — plain text names only
- No internal-only content
- Specific dates, names, artifacts — no placeholder brackets
- Flag unknowns with `⚠️ VERIFY:` inline

**Anti-keyword-soup rule (critical):**
Every sentence must pass: "Would the reader know what to DO, or just what to Google?" Feature names without workflow context are worthless. This applies to ALL email types, not just research_answers.

- BAD: "Use Unity Catalog for governance and Lakehouse Monitoring for quality."
- GOOD: "Register models in Unity Catalog with a three-level namespace (`catalog.schema.model_name`) so researchers across sites can discover them without wading through experiment runs."

**Gmail context adaptation:** If Step 1h returned recent thread data, check the last message snippet. If it contains an unanswered question from the recipient, open with acknowledgment ("Coming back to your question about [X]..."). If the last sent email from us included specific proof points or commitments, avoid repeating them — reference them ("Building on what I sent about [X]..."). This prevents the "I just got the same email twice" experience that erodes trust.

**For technical recipients (`to_type = technical`):**
- Include inline code when explaining APIs, commands, or config
- Reference specific documentation or guides when recommending workflows
- Use bold headers to separate distinct answers — scannable structure matters more than paragraph flow
- Depth > brevity: a 600-word email with 8 explained answers beats a 150-word email with 8 keywords

#### 4e. Internal leak check (Pass 2)
After drafting, compare every fact/name/detail against:
- Session `attendees_external` list
- What was explicitly discussed in-meeting (not internal prep or strategy)

Flag anything sourced from internal-only context with `⚠️ INTERNAL?:` inline.

#### 4f. Write subject line LAST
After the body is complete, write a benefit-focused subject line. Use the subject line patterns table from the philosophy doc.

#### 4g. Generate prep notes
Use the standardized prep notes schema from `references/email-philosophy.md`:
- Strategic Context
- What to Share if They Ask
- Questions to Ask
- Don't Mention
- Do Mention
- Suggested Send Time
- If No Response
- Thread Status

### Step 5: Determine Priority

| Condition | Priority |
|-----------|----------|
| Commitment from session <3 days ago, customer waiting | `high` |
| Deliverable promised with specific timeline | `high` |
| Answer to open questions (relationship-deepening) | `high` |
| Reactive response to customer input | `high` |
| Scheduling next meeting | `medium` |
| Introduction / connection request | `medium` |
| Nudge on overdue item | `medium` |
| Decline / redirect | `medium` |
| Insight share | `low` |
| Nice-to-have follow-up, no urgency | `low` |

### Step 6: Determine Due Date

| Email Type | Default Due |
|-----------|------------|
| Meeting follow-up | Same day or next business day |
| Deliverable send | Per commitment date, or +2 business days |
| Research/answers | Per commitment date, or +5 business days |
| Introduction | +3 business days |
| Scheduling | +2 business days |
| Check-in/nudge | +1 business day after detection |
| Decline/redirect | +2 business days |
| Insight share | +5 business days (low urgency) |
| Reactive response | +1 business day (responsiveness matters) |

### Step 7: Quality Gate

Before saving each draft, run the full checklist from `references/email-philosophy.md` Quality Gates section:

```
QUALITY CHECK: [recipient] — [type]
  Q1-NoLeaks:     PASS|FAIL — [internal content check]
  Q2-InternalPass: PASS|FAIL — [Pass 2 cross-reference]
  Q3-NoWikiLinks:  PASS|FAIL — [wiki-link check]
  Q4-WordCount:    PASS|FAIL — [count] words vs [target] target (use escalated target if technical depth applies)
  Q5-NoPlaceholders: PASS|FAIL — [placeholder check]
  Q6-OneAsk:       PASS|FAIL — [clear next step present?]
  Q7-BLUF:         PASS|FAIL — [first sentence is bottom line?]
  Q8-Forwardable:  PASS|FAIL — [makes sense without context?]
  Q9-ValueAdd:     PASS|FAIL — [teaches, advances, or delivers?]
  Q10-Subject:     PASS|FAIL — [benefit-focused?]
  Q11-ToneMatch:   PASS|FAIL — [matches recipient type?]
  Q12-Signature:   PASS|FAIL — [signed "Samuel"?]
  Q13-EmailResolved: PASS|FAIL|N/A — [recipient email found?]
  Q14-ThreadSafe:  PASS|FAIL|N/A — [no active thread collision?]
  VERDICT:         CLEAN | FIX REQUIRED → [what to fix]
```

Fix any FAILs before saving. Attempt up to 2 fix passes. If VERDICT is still FAIL after 2 attempts:
1. Save the draft with `status: flag_review` in frontmatter
2. Add `warnings: [list of failed gate IDs and reasons]` to frontmatter
3. Log in the output table: `⚠️ Saved with warnings — manual review needed`
4. Proceed to the next draft. Do not loop indefinitely.

### Step 8: Save Draft

**Location:** `~/obsidian/sa-intel/Artifacts/Emails/[date]-[recipient-slug]-[topic-slug].md`

**File structure:**
```markdown
---
[frontmatter per schema in philosophy doc]
---

# Email: [Subject Line]

**To:** [Full Name (Title, Company)]
**From:** Samuel Selvan
**CC:** [Names, if any]
**Subject:** [Subject line]

---

[Email body — copy-paste ready]

---

## Prep Notes (not in email)

[Full prep notes per schema]
```

### Step 8b: Symlink to Customer Folder

After saving each draft, create a symlink in `~/Customer/[account]/01-Emails/` pointing back to the vault original. This gives Finder-based access organized by account while keeping the vault as source of truth.

**Account name mapping** (vault account → folder name):
```
CHLA → CHLA
CHOC → CHOC
City of Hope → City_of_Hope
Mayo Clinic → Mayo_Clinic
Providence → Providence
Renown Health → Renown_Health
Geisinger → Geisinger
Kaiser → Kaiser
Access Hope → Access_Hope
Deloitte → Deloitte
```

**For each saved draft, run via Bash:**
```bash
ln -sf ~/obsidian/sa-intel/Artifacts/Emails/[filename].md ~/Customer/[account_folder]/01-Emails/[filename].md
```

- Use `-sf` (force) to overwrite stale symlinks if re-drafting
- If the account folder doesn't exist yet, create the full structure first:
  ```bash
  for sub in 01-Emails 02-Decks 03-Reference_Docs 04-Notebooks 05-Proposals 06-Meeting_Prep 07-Contracts_Legal 08-Screenshots; do
    mkdir -p ~/Customer/[account_folder]/$sub
  done
  ```
- Always use full absolute paths in the symlink target, not relative paths

### Step 8c: Create Gmail Draft (if GMAIL_AVAILABLE)

After saving to vault and creating the symlink, optionally create a Gmail draft for each email where `recipient_email` is resolved (not `unknown`):

1. **Convert markdown body to HTML**: Transform the email body markdown into simple HTML — paragraphs (`<p>`), bold (`<strong>`), italic (`<em>`), lists (`<ul>/<ol>`), and links (`<a>`). Keep it clean, no CSS.

2. **Create the draft:**
   - **If replying to existing thread** (gmail_message_id captured in Step 4c):
     ```bash
     python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py create-reply-draft --message-id "[gmail_message_id]" --html "<html body>"
     ```
   - **If new thread:**
     ```bash
     python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/gmail/resources/gmail_builder.py create-draft --to "[recipient_email]" --subject "[subject line]" --html "<html body>" [--cc "cc_emails"]
     ```

3. **Store draft ID**: Parse the JSON response → extract `id` field → update the vault draft's frontmatter with `gmail_draft_id: [id]`

4. **On error**: Log the failure in the output table's Gmail column (`Error: [reason]`). Do NOT fail the workflow — the vault draft is already saved.

### Step 9: Reindex

After writing all drafts and creating symlinks:
```
vault_reindex(full=false, embed=true)
```

## Output

After all drafts are saved:

```markdown
## 📧 Email Drafts Generated

| # | To | Email | Type | Topic | Priority | Due | Thread | Gmail | Vault Source |
|---|-----|-------|------|-------|----------|-----|--------|-------|-------------|
| 1 | Long Ho | loho@chla.usc.edu | research_answers | Onsite open questions | HIGH | Feb 14 | clear | Draft created | Artifacts/Emails/2026-02-11-long-ho-onsite-answers.md |
| 2 | Tina Huang | unknown | deliverable | MLflow workflow guide | MED | Feb 13 | clear | Skipped (no email) | Artifacts/Emails/2026-02-11-tina-huang-mlflow-guide.md |

### Summary
- **Total drafts:** 2
- **High priority:** 1 (send this week)
- **Suppressed:** 0
- **Gmail status:** Available — 1 draft created, 1 skipped (no email)
- **Symlinked:** 2 → ~/Customer/[account]/01-Emails/

### Next Steps
- Open in Finder: `~/Customer/[account]/01-Emails/` → double-click to review/edit
- Or ask Claude to edit: "fix the BLUF in the Long Ho email"
- After sending, update `status: sent` in frontmatter
- Run `/follow-ups` to track
```

## Relationship to draft-followup Skill

This skill (`email-render`) and `draft-followup` are complementary. Both are governed by the philosophy doc (`_System/prompts/email-drafting-philosophy.md`).

| | `email-render` (this skill) | `draft-followup` |
|---|---|---|
| **Scope** | Action-thread emails between meetings | Session recap emails (external + internal debrief) |
| **Types** | 10 types: follow-up, deliverable, research, intro, nudge, schedule, decline, insight, reactive, group follow-up | 10 meeting-type recaps: discovery, demo, arch review, POC scope, POC checkpoint, EBC, QBR, kickoff, security, working session |
| **Trigger** | `/email` command or post-session action items | `/draft-followup` or auto after `/process-transcript` |
| **Output** | Markdown drafts in `Artifacts/Emails/` | HTML + MD in `Sessions/[account]/[type]/emails/` |
| **Format** | Short (50-300 words), one purpose per email | Full recap, meeting-type-specific structure |
| **Internal email** | No — action threads are external only | Yes — MEDPICC updates, champion assessment, political dynamics, deal health |
| **Seniority ladder** | Simple recipient-type adjustment | 4-tier vocabulary ladder with HLS substitutions |

### Handoff Rule

After `/process-transcript` completes:
1. `draft-followup` generates the **session recap** (external + internal)
2. `email-render` generates **action-thread emails** for specific commitments extracted from the session

Both run independently. `draft-followup` captures "what happened." `email-render` delivers "what we owe them."

### Shared from Philosophy
- Core principles (BLUF, signature, tone, quality gates)
- Anti-patterns
- Relationship depth calibration
- Account culture rules

## Reference Files

Read BOTH before starting any email drafting session:
- **`references/email-philosophy.md`** — Core principles, email types, tone calibration, quality gates, anti-patterns, prep notes schema
- **`references/email-patterns.md`** — Subject line formulas, BLUF templates, Challenger tailoring, word count targets, frontmatter schema

$ARGUMENTS
