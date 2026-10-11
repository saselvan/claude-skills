---
name: email-render
description: "Draft follow-up emails from session context. USE WHEN: user says 'draft email', 'email [account]', 'send follow-up', or when /email command is invoked. Takes session notes and vault context as input. Produces ready-to-send email drafts in Artifacts/Emails/ with prep notes and frontmatter metadata."
allowed-tools: Read, Write, Bash, Task, Glob, Grep

CRITICAL_CONSTRAINT: "This skill CAN ONLY create email drafts. Sending emails is FORBIDDEN."
forbidden_operations: ["send", "sendMessage", "\.send\(", "smtp\.send", "mail\.send", "SEND", "Mail\.send"]
allowed_operations: ["create_draft", "write", "compose", "search", "read"]
on_violation: "IMMEDIATELY FAIL AND ALERT USER — this is a hard architectural rule"
---

# Email Render

You draft emails that get sent, not emails that get procrastinated. Every draft is copy-paste ready for Gmail — no placeholders, no "we should probably..." hedging. Specific names, specific dates, specific commitments.

## 🔒 HARD ARCHITECTURAL CONSTRAINT: Never Send, Only Draft

**This skill can ONLY create email drafts. Sending emails is FORBIDDEN.**

Three layers of safeguards enforce this:

### Safeguard A: Frontmatter Declaration
- Constraint explicitly declared in skill frontmatter (above)
- Forbidden and allowed operations listed
- Violation → IMMEDIATELY FAIL

### Safeguard B: Code-Level Wrapper Function
- All Gmail operations go through `gmail_safe_call()` wrapper
- Wrapper has hardcoded whitelist of allowed operations: `create_draft`, `search`, `read`, `list_drafts`
- Any forbidden operation (send, sendMessage, etc.) fails at wrapper level
- See "Gmail Safe Call Wrapper" section below

### Safeguard C: External Runtime Audit
- Every invocation captures all shell commands executed
- Runtime audit checks commands against forbidden-terms list
- If any send operation detected, entire workflow fails immediately
- See "Runtime Audit Protocol" section below

---

## Gmail Safe Call Wrapper (Safeguard B)

**Every Gmail operation must use this wrapper function. Do not call `gmail_builder.py` directly.**

```bash
# Define the whitelist
GMAIL_ALLOWED_OPS=("search" "read" "create_draft" "list_drafts" "get_draft" "list_messages")

# Wrapper function
gmail_safe_call() {
  local operation=$1
  shift  # Remove operation from args
  
  # Check if operation is in whitelist
  local is_allowed=false
  for allowed in "${GMAIL_ALLOWED_OPS[@]}"; do
    if [ "$operation" = "$allowed" ]; then
      is_allowed=true
      break
    fi
  done
  
  if [ "$is_allowed" = false ]; then
    echo "❌ CRITICAL: Forbidden Gmail operation: $operation"
    echo "   Email-render can ONLY create drafts."
    echo "   Allowed operations: ${GMAIL_ALLOWED_OPS[*]}"
    exit 1
  fi
  
  # Audit log
  echo "[GMAIL_AUDIT] Operation: $operation | Args: $@" >> "$EMAIL_RENDER_AUDIT_LOG"
  
  # Call Gmail tool
  python3 ~/.vibe/marketplace/plugins/fe-google-tools/skills/gmail/resources/gmail_builder.py "$operation" "$@"
  
  local exit_code=$?
  echo "[GMAIL_AUDIT] Exit code: $exit_code" >> "$EMAIL_RENDER_AUDIT_LOG"
  
  return $exit_code
}

# Usage examples (CORRECT):
gmail_safe_call search --query "to:[email]" --max-results 3
gmail_safe_call create_draft --to "[email]" --subject "[subject]" --body "[body]"
gmail_safe_call read --message-id "[msg_id]"

# Usage examples (INCORRECT — will fail):
gmail_safe_call send --message-id "[msg_id]"               # ❌ Forbidden
gmail_safe_call sendMessage --message-id "[msg_id]"        # ❌ Forbidden
```

---

## Runtime Audit Protocol (Safeguard C)

**At Step 0, initialize audit logging. At Step 9, verify no send operations occurred.**

### Step 0: Initialize Audit Log
```bash
EMAIL_RENDER_AUDIT_LOG="/tmp/email_render_audit_$$.log"
FORBIDDEN_PATTERNS=(
  "\.send\("
  "sendMessage"
  "\.send"
  "smtp\.send"
  "mail\.send"
  "smtp\.sendmail"
  "/send"
  "POST.*send"
  "--send"
)

echo "=== Email-Render Audit Log ===" > "$EMAIL_RENDER_AUDIT_LOG"
echo "Session: $$ | Start: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$EMAIL_RENDER_AUDIT_LOG"
echo "Constraint: Never send, only create drafts" >> "$EMAIL_RENDER_AUDIT_LOG"
echo "" >> "$EMAIL_RENDER_AUDIT_LOG"

# Capture all commands
set -x  # Debug mode: log all commands
exec 1> >(tee -a "$EMAIL_RENDER_AUDIT_LOG")
exec 2>&1
```

### Step 9: Final Audit Verification
```bash
echo ""
echo "🔒 FINAL SEND-CAPABILITY AUDIT:"
echo ""

# Check 1: Scan audit log for forbidden patterns
VIOLATIONS=0
for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  MATCHES=$(grep -c "$pattern" "$EMAIL_RENDER_AUDIT_LOG" 2>/dev/null || echo "0")
  if [ "$MATCHES" -gt 0 ]; then
    echo "❌ VIOLATION: Pattern '$pattern' found $MATCHES times"
    grep "$pattern" "$EMAIL_RENDER_AUDIT_LOG" | head -5
    VIOLATIONS=$((VIOLATIONS+1))
  fi
done

# Check 2: Scan for unwhitelisted Gmail operations
if grep "gmail_builder.py" "$EMAIL_RENDER_AUDIT_LOG" > /dev/null 2>&1; then
  UNWHITELISTED=$(grep "gmail_builder.py" "$EMAIL_RENDER_AUDIT_LOG" | \
    grep -v "search\|read\|create_draft\|list_drafts\|get_draft\|list_messages" | wc -l)
  
  if [ $UNWHITELISTED -gt 0 ]; then
    echo "❌ VIOLATION: $UNWHITELISTED unwhitelisted Gmail operations detected"
    VIOLATIONS=$((VIOLATIONS+1))
  fi
fi

if [ $VIOLATIONS -gt 0 ]; then
  echo ""
  echo "❌ CRITICAL: Send operations detected in audit log."
  echo "   Audit log: $EMAIL_RENDER_AUDIT_LOG"
  echo "   This skill cannot proceed."
  exit 1
fi

echo "✅ Audit passed: No send operations detected"
echo "✅ All Gmail operations used whitelist wrapper"
echo "✅ Email-render operated in draft-only mode"
echo ""

# Clean up
set +x
exec 1>&-
exec 2>&-

# Report audit summary
echo ""
echo "📋 Audit Log: $EMAIL_RENDER_AUDIT_LOG"
echo "   (preserved for user review)"
```

---

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

## Gmail Integration (Safeguarded)

**FIX #3: Gmail Availability with Clear Reporting**

At workflow start (Step 0a), check Gmail availability:

```bash
# Step 0a: Check Gmail Availability (CRITICAL REPORTING)
echo ""
echo "🔐 Initializing Email-Render (Draft-Only Mode)"
echo ""

# Ensure gcloud is on PATH and PYTHONPATH includes google-auth resources
export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"
export PYTHONPATH=~/.vibe/marketplace/plugins/fe-google-tools/skills/google-auth/resources

# Test with a lightweight Gmail search — if this succeeds, Gmail is available
GMAIL_TEST=$(python3 ~/.vibe/marketplace/plugins/fe-google-tools/skills/gmail/resources/gmail_builder.py search --query "newer_than:1h" --max-results 1 2>&1)
GMAIL_EXIT=$?

if [ $GMAIL_EXIT -eq 0 ]; then
  GMAIL_AVAILABLE=true
  echo "✅ Gmail Available: Drafts will be created in both vault and Gmail"
else
  GMAIL_AVAILABLE=false
  echo "⚠️ Gmail Unavailable: Drafts will be saved to vault only"
  echo "   Error: $GMAIL_TEST"
  echo "   You will need to copy-paste email body into Gmail manually"
fi

echo "📧 Mode: DRAFT CREATION ONLY (user clicks send from Gmail UI)"
echo ""
```

- If exit code 0 → set `GMAIL_AVAILABLE = true` — enables Steps 1g, 1h, enhanced 4c, and 8c
- If non-zero → set `GMAIL_AVAILABLE = false` — fall back to vault-only behavior
- **Report this clearly in Step 0 AND in the final summary (Step 9)**

**Gmail tool path:** `~/.vibe/marketplace/plugins/fe-google-tools/skills/gmail/resources/gmail_builder.py`
**Requires:**
- `export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"` (gcloud for API auth)
- `export PYTHONPATH=~/.vibe/marketplace/plugins/fe-google-tools/skills/google-auth/resources` (imports `google_api_utils`)

**CRITICAL:** Every `python3` invocation of any fe-google-tools script MUST have `PYTHONPATH` set, or imports will fail.

**Hard rules (Safeguards):**
- ✅ ONLY create drafts — NEVER send emails
- ✅ Vault remains source of truth — Gmail draft is a convenience copy
- ✅ User hits send manually from Gmail UI — only after review
- ✅ No Gmail modifications — don't modify labels, delete, trash, or alter existing emails
- ✅ All Gmail operations go through `gmail_safe_call()` wrapper (whitelist enforcement)
- ✅ Runtime audit captures all commands (forbidden pattern detection)
- ✅ Final audit (Step 9) verifies no send operations occurred

If any Gmail command fails, log it and continue — never fail the workflow. **But if any send operation is attempted, fail immediately and alert user.**

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

---

### Step 0b: Coordinator Context Validation (FIX #5)

**If `_meta.board_dir` is provided** (running in coordinated mode):

```bash
BOARD_DIR="$_meta_board_dir"

if [ ! -z "$BOARD_DIR" ]; then
  if [ ! -f "$BOARD_DIR/context.yaml" ]; then
    echo ""
    echo "❌ CRITICAL: Coordinator context missing"
    echo "   Expected: $BOARD_DIR/context.yaml"
    echo "   Contains: action_items, commitments, attendees, open_questions"
    echo ""
    echo "   Fallback: Running in STANDALONE mode"
    echo "   ⚠️  Action items may not be tracked properly in board output"
    echo ""
    read -p "Proceed in standalone mode? [yes/no] " CONFIRM_FALLBACK
    if [ "$CONFIRM_FALLBACK" != "yes" ]; then
      exit 1
    fi
    BOARD_DIR=""  # Clear mode, switch to standalone
  fi
fi

echo "✅ Coordinator context validated"
echo ""
```

**Action:** If context.yaml is missing, warn and offer fallback. If proceeding, ensure board write captures "coordinator context missing" in the audit.

---

### Step 0c: Send-Capability Audit (SAFEGUARD VERIFICATION)

**Before proceeding with any email work, verify the three safeguards are in place:**

```bash
echo "🔒 Verifying Email-Render Hard Constraints..."
echo ""

# Check 1: Wrapper function defined
if ! declare -f gmail_safe_call > /dev/null 2>&1; then
  echo "❌ CRITICAL: Gmail safe call wrapper not defined"
  echo "   Function 'gmail_safe_call' must be defined before Gmail operations"
  exit 1
fi

# Check 2: Audit log initialized
if [ -z "$EMAIL_RENDER_AUDIT_LOG" ]; then
  echo "❌ CRITICAL: Audit log not initialized"
  echo "   EMAIL_RENDER_AUDIT_LOG environment variable must be set"
  exit 1
fi

# Check 3: Forbidden patterns list defined
if [ -z "${FORBIDDEN_PATTERNS[0]}" ]; then
  echo "❌ CRITICAL: Forbidden patterns list not defined"
  echo "   FORBIDDEN_PATTERNS array must be initialized"
  exit 1
fi

echo "✅ All three safeguards verified"
echo "✅ Draft-only mode enforced"
echo ""
```

---

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
   gmail_safe_call search --query "to:[Full Name]" --max-results 3
   ```
   Parse the results to extract the recipient's email address from matching messages.
3. **Unknown fallback**: If neither works, set `recipient_email: unknown` — skip Gmail draft creation later, flag with `⚠️ VERIFY: No email found for [Name]`

#### 1h. Gmail Thread Intelligence (if GMAIL_AVAILABLE)

For each recipient with a resolved email, fetch recent email history:

- **Last sent:**
  ```bash
  gmail_safe_call search --query "from:me to:[email] newer_than:30d" --max-results 1
  ```
- **Last received:**
  ```bash
  gmail_safe_call search --query "from:[email] to:me newer_than:30d" --max-results 1
  ```

Extract from results: date, subject, snippet, messageId, threadId. Store for use in Steps 4c (thread check), 4d (drafting context), 4g (prep notes), and 8c (Gmail draft threading).

#### 1d. Vault Reconciliation: Stale Action Item Data (FIX #1)

**After loading coordinator context or session file, cross-check action items against vault.**

For each action item extracted from coordinator or session:

```bash
# Query vault for current state of this action item
vault_signals(account, signal_type="action_item", owed_by="[owner]") | \
  grep "due\|status" | head -5

# Compare:
# IF vault has NEWER entry (updated after coordinator ran) → use vault version
# IF vault shows status=closed → offer to skip this email
# IF vault due date differs → note the discrepancy in email context

echo ""
echo "📋 Action Item Reconciliation:"
for action in "${coordinator_actions[@]}"; do
  VAULT_VERSION=$(vault_signals ... | grep "$action")
  if [ ! -z "$VAULT_VERSION" ]; then
    VAULT_DUE=$(echo "$VAULT_VERSION" | grep -o "due:[^ ]*")
    COORDINATOR_DUE=$(echo "$action" | grep -o "due:[^ ]*")
    if [ "$VAULT_DUE" != "$COORDINATOR_DUE" ]; then
      echo "ℹ️  Action '$action': due date updated in vault"
      echo "   Was: $COORDINATOR_DUE → Now: $VAULT_DUE"
    fi
  fi
done
```

**Result:** Email-render uses current vault state, not stale coordinator state.

#### 1e. Stakeholder Status Check: Catch Former Employees (FIX #2)

**Before including a recipient in the email list, verify they haven't left the company.**

For each recipient in the email list:

```bash
# Query vault for stakeholder status
vault_graph(source_id="person:[name]", rel_type="contact", direction="incoming") | \
  jq '.status, .departure_date, .email'

echo ""
echo "👥 Stakeholder Status Check:"
for recipient in "${recipients[@]}"; do
  PERSON_DATA=$(vault_graph "person:$(slugify $recipient)")
  STATUS=$(echo "$PERSON_DATA" | jq -r '.status')
  DEPARTURE=$(echo "$PERSON_DATA" | jq -r '.departure_date')
  CURRENT_EMAIL=$(echo "$PERSON_DATA" | jq -r '.email')
  
  if [ "$STATUS" = "former" ] || [ ! -z "$DEPARTURE" ] && [ "$DEPARTURE" < "$(date +%Y-%m-%d)" ]; then
    echo "⚠️  SKIP: $recipient left $DEPARTURE (status: $STATUS)"
    SKIP_RECIPIENTS+=("$recipient")
    continue
  fi
  
  if [ "$CURRENT_EMAIL" != "$SESSION_EMAIL_FOR_RECIPIENT" ]; then
    echo "ℹ️  Email updated: $SESSION_EMAIL_FOR_RECIPIENT → $CURRENT_EMAIL"
    UPDATE_EMAIL["$recipient"]="$CURRENT_EMAIL"
  fi
done

# Remove skipped recipients from email list
for skip in "${SKIP_RECIPIENTS[@]}"; do
  recipients=(${recipients[@]/$skip})
done
```

**Result:** Stale contacts are skipped, current contact information is used.

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
  python3 ~/.vibe/marketplace/plugins/fe-google-tools/skills/gmail/resources/gmail_builder.py search --query "from:me to:[email] newer_than:7d" --max-results 5
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
quality_audit:
  Q3_recipient_identification: PASS|FAIL|WARN
  Q5_uncertain_language: PASS|FAIL|WARN
  Q7_tone_calibration: PASS|FAIL|WARN
  Q11_action_clarity: PASS|FAIL|WARN
  Q13_subject_line: PASS|FAIL|WARN
  overall: "[N] PASS, [N] WARN, [N] FAIL"
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

### Step 8a: Quality Audit & Tone Check (FIX #4 & #6)

**Before saving, run all quality checks and optionally run tone-check.**

```bash
echo "🔍 Running Quality Audit..."
echo ""

# Run all Q1-Q14 gates (from references/email-philosophy.md)
Q_RESULTS=()

# Q3: Recipient identification
if grep -q "\[RECIPIENT\]\|{{recipient}}\|UNKNOWN" draft.md; then
  Q_RESULTS+=("Q3_recipient_identification:FAIL")
else
  Q_RESULTS+=("Q3_recipient_identification:PASS")
fi

# Q5: Uncertain language
UNCERTAIN_COUNT=$(grep -o "might\|could\|potentially\|consider\|try to\|attempt" draft.md | wc -l)
if [ $UNCERTAIN_COUNT -gt 2 ]; then
  Q_RESULTS+=("Q5_uncertain_language:WARN (found $UNCERTAIN_COUNT uncertain phrases)")
else
  Q_RESULTS+=("Q5_uncertain_language:PASS")
fi

# Q7: Tone calibration (check against recipient profile)
if [ "$RECIPIENT_TYPE" = "executive" ] && grep -q "just\|might\|could\|try" draft.md; then
  Q_RESULTS+=("Q7_tone_calibration:WARN (too tentative for executive)")
else
  Q_RESULTS+=("Q7_tone_calibration:PASS")
fi

# Q11: Action clarity
if grep -q "please let me know\|I'll send you\|I'll get back to you" draft.md; then
  Q_RESULTS+=("Q11_action_clarity:PASS")
else
  Q_RESULTS+=("Q11_action_clarity:WARN (action items unclear)")
fi

# Q13: Subject line
SUBJECT_LENGTH=$(echo "$SUBJECT_LINE" | wc -c)
if [ $SUBJECT_LENGTH -gt 60 ]; then
  Q_RESULTS+=("Q13_subject_line:WARN (too long: $SUBJECT_LENGTH chars, target < 60)")
else
  Q_RESULTS+=("Q13_subject_line:PASS")
fi

# Add all results to frontmatter
QUALITY_AUDIT=$(printf '%s\n' "${Q_RESULTS[@]}" | sed 's/^/  /')
echo "$QUALITY_AUDIT" >> quality_audit_temp.txt

# Report summary
PASS_COUNT=$(grep -c "PASS" quality_audit_temp.txt)
WARN_COUNT=$(grep -c "WARN" quality_audit_temp.txt)
FAIL_COUNT=$(grep -c "FAIL" quality_audit_temp.txt)

echo "✅ PASS: $PASS_COUNT | ⚠️  WARN: $WARN_COUNT | ❌ FAIL: $FAIL_COUNT"
echo ""

# If tone warnings exist, optionally run tone-check
if [ $WARN_COUNT -gt 0 ] || [ $FAIL_COUNT -gt 0 ]; then
  echo "📋 Tone concerns detected. Running detailed tone check..."
  /tone-check "$DRAFT_FILE" --mode="email" --audience="$AUDIENCE_CLASS" 2>/dev/null || true
  echo ""
fi
```

**Result:** Quality checks embedded in frontmatter. User sees warnings before sending.

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

### Step 8c: Create Gmail Draft (if GMAIL_AVAILABLE) — FIX #3 (Gmail Safeguard)

After saving to vault and creating the symlink, optionally create a Gmail draft for each email where `recipient_email` is resolved (not `unknown`):

1. **Convert markdown body to HTML**: Transform the email body markdown into simple HTML — paragraphs (`<p>`), bold (`<strong>`), italic (`<em>`), lists (`<ul>/<ol>`), and links (`<a>`). Keep it clean, no CSS.

2. **Create the draft using safe wrapper:**
   - **If replying to existing thread** (gmail_message_id captured in Step 4c):
     ```bash
     RESPONSE=$(gmail_safe_call create_draft --message-id "[gmail_message_id]" --html "<html body>")
     ```
   - **If new thread:**
     ```bash
     RESPONSE=$(gmail_safe_call create_draft --to "[recipient_email]" --subject "[subject line]" --html "<html body>" [--cc "cc_emails"])
     ```

3. **Verify draft was created (NOT sent) — FIX #7 (Send Safeguard):**
   ```bash
   # Check 1: Response contains draft ID (not sent message ID)
   DRAFT_ID=$(echo "$RESPONSE" | jq -r '.id // empty')
   if [ -z "$DRAFT_ID" ]; then
     echo "❌ CRITICAL: No draft ID returned"
     echo "   Response: $RESPONSE"
     exit 1
   fi
   
   # Check 2: Draft marked with DRAFT label (not SENT)
   DRAFT_STATUS=$(echo "$RESPONSE" | jq -r '.message.labelIds[]' | grep -i draft)
   if [ -z "$DRAFT_STATUS" ]; then
     echo "❌ CRITICAL: Draft not marked with DRAFT label"
     echo "   This suggests email may have been sent"
     echo "   Response: $RESPONSE"
     exit 1
   fi
   
   # Check 3: NOT marked as SENT
   if echo "$RESPONSE" | jq -r '.message.labelIds[]' | grep -q "SENT"; then
     echo "❌ CRITICAL: Email was SENT, not drafted"
     exit 1
   fi
   
   echo "✅ Draft created successfully: $DRAFT_ID (DRAFT mode confirmed)"
   ```

4. **Store draft ID**: Parse the response → extract `id` field → update the vault draft's frontmatter with `gmail_draft_id: [id]`

5. **On error**: Log the failure in the output table's Gmail column (`Error: [reason]`). Do NOT fail the workflow — the vault draft is already saved.

### Step 9: Reindex

After writing all drafts and creating symlinks:
```
vault_reindex(full=false, embed=true)
```

### Step 9c: Final Send-Capability Audit Report (SAFEGUARD COMPLETION)

**After all drafts are created, run the final audit verification and report results:**

```bash
echo ""
echo "🔒 FINAL SEND-CAPABILITY AUDIT:"
echo ""

# Check 1: Scan audit log for forbidden patterns
VIOLATIONS=0
for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  MATCHES=$(grep -c "$pattern" "$EMAIL_RENDER_AUDIT_LOG" 2>/dev/null || echo "0")
  if [ "$MATCHES" -gt 0 ]; then
    echo "❌ VIOLATION: Pattern '$pattern' found $MATCHES times"
    VIOLATIONS=$((VIOLATIONS+1))
  fi
done

# Check 2: Verify no unwhitelisted Gmail operations
if grep "gmail_builder.py" "$EMAIL_RENDER_AUDIT_LOG" > /dev/null 2>&1; then
  UNWHITELISTED=$(grep "gmail_builder.py" "$EMAIL_RENDER_AUDIT_LOG" | \
    grep -v "search\|read\|create_draft\|list_drafts" | wc -l)
  
  if [ $UNWHITELISTED -gt 0 ]; then
    echo "❌ VIOLATION: $UNWHITELISTED unwhitelisted Gmail operations detected"
    VIOLATIONS=$((VIOLATIONS+1))
  fi
fi

if [ $VIOLATIONS -gt 0 ]; then
  echo ""
  echo "❌ CRITICAL: Send operations detected in audit log"
  echo "   Email-render operated in violation of draft-only constraint"
  exit 1
fi

echo "✅ Audit passed: No send operations detected"
echo "✅ All Gmail operations used whitelist wrapper"
echo "✅ Email-render operated in draft-only mode throughout"
echo ""

# Report mode and capability
echo "📧 EMAIL DELIVERY:"
echo "   Drafts saved to: ~/obsidian/sa-intel/Artifacts/Emails/"
echo "   Symlinked to: ~/Customer/[account]/01-Emails/"
echo "   Gmail drafts: [✅ Created | ⚠️ Unavailable]"
echo ""
echo "🚫 USER ACTION REQUIRED:"
echo "   1. Open Gmail (or vault drafts)"
echo "   2. Review each draft"
echo "   3. Click Send when ready"
echo "   4. Email-render never sends — you do"
echo ""
```

---

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

## Audience Review Quality Gate (Auto-Invoked)

After customer-facing emails are rendered, `/audience-review` is automatically invoked to assess whether the recipient will find it compelling.

**Process:**
1. Email .md is written to Artifacts/{account}/emails/
2. `/audience-review {email_path}` is automatically invoked
3. Audience is auto-read from strategy.yaml or manifest
4. Fresh agent assumes recipient role and assesses: will they act on this?
5. Verdict (RED/YELLOW/GREEN) reported to user

**Verdicts:**
- 🟢 **GREEN (71-100%)**: Recipient likely to act. Email ready to send.
- 🟡 **YELLOW (41-70%)**: Recipient interested but may have concerns. Consider revisions before sending.
- 🔴 **RED (0-40%)**: Recipient unlikely to act. Major rework needed.

**If YELLOW or RED:**
```
⚠️ Suggested Revision
Gap: [specific concern audience flagged]

Run: /iterate {email_path}
Then: /audience-review {email_path} (re-review after changes)
```

**Note:** Audience-review applies to customer-facing emails (external To: fields). Internal follow-ups and self-reminders skip this gate.

## vault_speaker Integration (Production — W5 Cutover)

**Status:** PRIMARY (graduated from shadow mode)

vault_speaker is the primary context source for email drafting. Existing retrieval logic (vault_summary, vault_signals, session reads, stakeholder lookups) serves as fallback.

### At generation start:

1. Call vault_speaker: `/vault-speaker --intent email --account {account_id}`
2. If vault_speaker succeeds (returns confidence != low): use its package as primary context
   - Account context, stakeholder profiles, and prior communications come from vault_speaker
   - Gmail thread intelligence (Steps 1g/1h) still runs independently — vault_speaker enriches, not replaces, Gmail data
3. If vault_speaker fails or returns confidence=low: fall back to existing retrieval logic (vault_summary + vault_signals + session reads + stakeholder lookups)
4. Log outcome_tag to vault_speaker_invocations after generation completes

### Fallback behavior:

- vault_speaker timeout (>15s): use existing retrieval logic, log outcome_tag='timeout'
- vault_speaker error: use existing retrieval logic, log outcome_tag='error'
- vault_speaker confidence=low for all retrievers: use existing retrieval logic, log outcome_tag='low_confidence_fallback'

### What vault_speaker provides (when successful):

- **Account context**: deal state, health, recent session summaries
- **Stakeholder profiles**: roles, relationship depth, communication preferences, stance
- **Prior communications**: recent email history from vault (complements Gmail thread intelligence)

### What existing logic still owns (always):

- Gmail thread intelligence (Steps 1g/1h) — vault_speaker has no Gmail access
- Action item reconciliation (Step 1d) — vault_signals for current state
- Stakeholder status check (Step 1e) — departure detection
- Quality gates (Step 7) and audit protocol (Steps 0/9c)

### Logging:

After email generation completes, log the invocation to brain.db:
```python
import sqlite3, json, secrets
db = sqlite3.connect("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")
db.execute("""
    INSERT INTO vault_speaker_invocations
    (invocation_id, run_id, intent, scope, outcome_tag, latency_ms)
    VALUES (?, ?, 'email', ?, ?, ?)
""", (
    secrets.token_hex(16), secrets.token_hex(16),
    json.dumps({"account_id": account_id, "skill": "email-render"}),
    outcome_tag,  # 'success' | 'timeout' | 'error' | 'low_confidence_fallback'
    latency_ms,
))
db.commit()
db.close()
```

---

## Reference Files

Read BOTH before starting any email drafting session:
- **`references/email-philosophy.md`** — Core principles, email types, tone calibration, quality gates, anti-patterns, prep notes schema
- **`references/email-patterns.md`** — Subject line formulas, BLUF templates, Challenger tailoring, word count targets, frontmatter schema

## Output Convention

**Write path:** `Artifacts/{account-slug}/emails/{YYYY-MM-DD}-{recipient-slug}-{topic-slug}.md`
**artifact_type:** `email`
**Frontmatter:** Embed canonical frontmatter directly in the .md file (no separate sidecar for markdown).
**After save:** Call `vault_reindex(full=false, embed=false)`.

Example:
```
Artifacts/nwm/emails/2026-04-09-bhasker-bingari-demand-planning-recap.md
```


$ARGUMENTS
