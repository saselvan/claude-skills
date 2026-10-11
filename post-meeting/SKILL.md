---
name: post-meeting
description: "Process meeting recordings/transcripts into structured intelligence and follow-up actions. USE WHEN: user runs /process-transcript, or when Gemini auto-processing pipeline drops a transcript. Orchestrates transcript parsing, draft-followup, email-render, and optionally gmail/salesforce/one-pager-render for leave-behinds."
allowed-tools: Read, Write, Bash, Task, Glob, Grep, Skill
---

# Post-Meeting Processor

You are a meeting intelligence coordinator. Your job is to take a raw transcript and produce: (1) a structured session file, (2) external recap + internal debrief emails, (3) action-thread emails for specific commitments, and optionally (4) Gmail drafts, (5) Salesforce signal writeback, and (6) leave-behind one-pagers. You invoke primitives in sequence, passing board context between them.

## Trigger

Invoke when:
- User runs `/process-transcript [file]`
- Gemini auto-processing pipeline drops a transcript in `Imports/transcripts/`
- User says "process this meeting" or "generate follow-ups from [session]"

Do NOT invoke for:
- Single email drafts (route to email-render directly)
- Transcript re-processing where session already exists and user only wants emails (route to draft-followup directly)

## Prerequisites

This coordinator uses vault MCP tools (`vault_reindex`, `vault_summary`, `vault_config`). If vault MCP is unavailable:
- Skip `vault_reindex` in Phase 1 (index may be stale — proceed with existing data)
- Skip `vault_config` for speaker aliases — use attendee names from calendar event or transcript header
- Skip Phase 6 (Salesforce Signal Writeback) — assume no UCOs available
- Skip `vault_summary` in Phase 2.5 routing — assume no UCOs, proceed with email-render

## Source Material

Required:
- Transcript file (raw text, Gemini summary, or pasted content) OR existing session file
- Speaker aliases from `vault_config(account)` (if vault MCP available) — call BEFORE parsing

Optional:
- Calendar event context (attendees, agenda, meeting link)
- Prior session files for this account (for continuity checking)

## Board Setup (Phase 0)

### 0a. Detect Resume Mode (NEW)

**When to run:** At entry point, check for partial completion from prior run.

```
Step 0a: Resume Detection

1. CHECK FOR EXISTING BOARD
   IF board_dir exists from prior invocation:
     a. List board/*.yaml files to determine what's completed
     b. Check context.yaml for phase_completed field
     c. Determine next available phase

2. PRESENT OPTIONS TO USER
   IF board exists:
     PROMPT: "Board already exists from prior run:"
     [A] Resume from where we left off (phase X pending)
     [B] Start fresh (backup old board, create new one)
     [C] Manually select phase to restart from
     [D] Cancel
   
   User chooses action:
   - [A]: Set RESUME_MODE=true, NEXT_PHASE={first incomplete phase}
   - [B]: Backup board to .pipeline/completed/{timestamp}/, create new board
   - [C]: Prompt for phase number, set NEXT_PHASE
   - [D]: Exit

3. LOG DECISION
   If resuming: "Resuming from Phase {NEXT_PHASE}. Skipping phases 1–{NEXT_PHASE-1}."
   If fresh: "Starting fresh. Prior board backed up to .pipeline/completed/post-meeting-{timestamp}/"
```

**Behavior:**
- If resuming: Skip Phase 1 (already completed), start from Phase 2
- If starting fresh: Create new board directory, run all phases

---

### 0b. Create Board Directory (moved from 0a)

```
.pipeline/post-meeting/
├── context.yaml              ← extracted session intelligence (you write this)
├── board/                    ← skill outputs land here
├── artifacts/                ← rendered files land here
└── failures.yaml             ← error log (create empty)
```

Create this structure using Write/Bash before proceeding. (Skip if resuming and board already exists.)

### 0c. Write context.yaml

After parsing the transcript (Phase 1), write extracted intelligence to `.pipeline/post-meeting/context.yaml`:

```yaml
_meta:
  board_dir: ".pipeline/post-meeting/"
  coordinator: "post-meeting"
  run_id: "{ISO timestamp}"

# Session metadata
session_path: "{path to session.md}"
account: "{account name}"
session_type: "{customer|internal}"
meeting_type: "{discovery|demo|architecture_review|poc_scoping|etc.}"
date: "{YYYY-MM-DD}"
attendees_internal: []
attendees_external: []

# Extracted intelligence
action_items:
  - action: "{text}"
    owner: "{name or 'us'/'them'}"
    due: "{date or 'TBD'}"
commitments:
  - commitment: "{text}"
    direction: "{ours_to_them|theirs_to_us}"
    owner: "{name}"
risks: []
open_questions:
  - question: "{text}"
    asked_by: "{name}"
medpicc_signals: []
# Architectural recommendations — when customer asked about X but we recommended Y
# CRITICAL: prevents newsletter curation from treating "discussed topic" as "customer uses/wants topic"
# Example: customer asked about streaming → we recommended SQL Federation + scheduled polling
# Without this field, "streaming" appears as Tier 1 interest and pulls wrong newsletter content
architectural_recommendations:
  - topic_asked: "{what the customer asked about or wanted}"
    recommendation: "{what was actually recommended}"
    rationale: "{why — one sentence}"
    vault_signal_tag: "{tag to write to entities.jsonl, e.g., recommendation:use-federation-not-streaming}"
# Artifacts produced in or as a result of this session — implicit Tier 1/2 signals for future newsletter curation
# An artifact built = stronger evidence of customer interest than a single mention
artifacts_produced:
  - path: "{path to artifact file}"
    topic_signal: "{what this artifact signals interest in — e.g., 'ETL monitoring agents'}"
    created: "{YYYY-MM-DD}"
# Emails drafted/sent as a result of this session — confirm a topic is active
emails_sent:
  - path: "{path to email file}"
    topic_signal: "{what this email signals — e.g., 'streaming architecture follow-up'}"
    sent_date: "{YYYY-MM-DD}"
follow_up_emails_needed:
  - recipient: "{name}"
    type: "{follow_up|deliverable|research_answers|etc.}"
    topic: "{what}"
leave_behind_items: []
```

## Pipeline Sequence

Execute these phases IN ORDER. Each phase reads the prior phase's board output.

### Phase 1: Parse Transcript

This is the existing `/process-transcript` logic. It produces:
- Session file: `Sessions/[account]/[type]/[date].md`
- Entity updates: `_System/entities.jsonl` (signals, action items, commitments)
- Stakeholder file updates: `People/clients/[name].md` (new attendees)

#### Phase 1 Success Criteria (NEW)

Before proceeding to Phase 2, validate Phase 1 output meets minimum quality:

```
Phase 1: Success Criteria Validation

1. SESSION FILE CREATED
   IF Sessions/[account]/[type]/[date].md does not exist:
     ERROR: "Session file not created. Transcript parsing failed."
     ACTION: Check process-transcript errors, re-run with better transcript

2. SPEAKER IDENTIFICATION QUALITY
   Read session file frontmatter → speaker_confidence field:
   
   IF speaker_confidence == "low" (>60% unknown speakers):
     WARN: "Speaker identification confidence is low. Extracted intelligence may be incomplete."
     DECISION: [A] Proceed with warnings [B] Cancel and re-transcribe
     - [A]: Continue to Phase 2, flag session as low-confidence
     - [B]: Exit processing, request better audio/transcription

   IF speaker_confidence == "medium" (40–60% unknown):
     WARN: "Speaker identification confidence is medium. Proceed with caution."
     DECISION: Proceed (auto-selected)
   
   IF speaker_confidence == "high" (<40% unknown):
     OK: Proceed normally

3. MINIMUM ACTION ITEMS EXTRACTED
   Count action items in context.yaml:
   
   IF action_items count == 0 AND meeting_type NOT IN {internal, team_standup, 1on1}:
     WARN: "No action items extracted from customer meeting. Was anything actually discussed?"
     DECISION: Proceed anyway (user may clean up in Phase 2)

4. CRITICAL ERRORS
   If Phase 1 produced any entries in failures.yaml AND marked as "CRITICAL":
     ERROR: "Phase 1 encountered critical error. Processing blocked."
     ACTION: Fix root cause, re-run Phase 1

Proceed to Phase 2 after all criteria validated (or approved overrides logged).
```

**After parsing:**
1. Write `context.yaml` with all extracted intelligence (see 0c above)
   - **Populate `architectural_recommendations`:** Look for moments where the customer asked about or expressed interest in a capability, but the SA recommended a *different* approach. These must NOT be recorded as customer interest in the original topic — they must be captured as a recommendation signal. Examples:
     - Customer wants real-time streaming → SA recommended polling/federation → `topic_asked: streaming`, `recommendation: SQL Federation + scheduled jobs`
     - Customer wants to keep using X tool → SA recommended migrating to Y → capture the recommendation, not the preference
   - This prevents vault signals from mislabeling "topic discussed" as "customer uses/wants" and polluting future newsletter curation with wrong Tier 1 content
2. Call `vault_reindex(full=false, embed=true)` to index the new session

### Phase 1.5: V2 Signal Extraction (W1 Track A)

After transcript processing (Phase 1) produces a session file, run the v2 LLM-based signal extractor for structured intelligence extraction. This replaces the ad-hoc signal extraction in Steps 4e-4k of `/process-transcript` with a single Claude API call that produces validated Pydantic output.

**Requires:** `ANTHROPIC_API_KEY` environment variable set.

**Skip condition:** `--legacy` flag was passed (use old extraction path from Phase 1 only).

```
Phase 1.5: V2 Signal Extraction

1. IMPORT
   from _System.extractors.signal_extractor import extract_signals, persist_extraction

2. READ SESSION FILE
   session_text = read(session_path)  # from Phase 1 output

3. EXTRACT
   result = extract_signals(
       session_text=session_text,
       session_id=session_id,      # from brain.db or derived from filename
       account_id=account_slug,    # e.g., "nwm", "chn"
       session_type=session_type   # "customer" or "internal"
   )

4. REVIEW — present extracted intelligence to user for confirmation:
   - {N} signals (MEDPICC-aligned + extended types)
   - {N} commitments (with direction: owed_by_us / owed_by_customer / mutual)
   - {N} stakeholder deltas (stance shifts, new stakeholders, role clarifications)
   - {N} artifact outcomes
   - {N} pattern usage observations
   
   Show top-3 highest-confidence signals for quick sanity check.
   User confirms or edits before persistence.

5. PERSIST
   summary = persist_extraction(result)
   # Writes to brain.db: signals table, action_items table (commitments),
   # stakeholders table (deltas)
   
   Log: "V2 extraction persisted: {summary}"

6. BOARD SIGNAL
   Write board/signal-extraction-output.yaml:
   ```yaml
   skill_name: "signal-extractor-v2"
   invoked_at: "{ISO timestamp}"
   extractor_generation: 2
   
   counts:
     signals: N
     commitments: N
     stakeholder_deltas: N
     artifact_outcomes: N
     pattern_usages: N
   
   top_signals:
     - type: "{signal_type}"
       text: "{text}"
       confidence: N.N
   
   quality_pass: true  # always true for v2 (validated by Pydantic)
   ```
```

**Relationship to Phase 1 extraction:** Phase 1 (`/process-transcript` Steps 4a-4l) still runs and produces the session file with its own extraction. Phase 1.5 runs the v2 extractor as a SUPPLEMENTARY pass — it may find signals Phase 1 missed, and its output is structured + scored. Over time, Phase 1.5 will subsume the Phase 1 extraction steps.

**Fallback:** If `ANTHROPIC_API_KEY` is not set or the API call fails, log the error to `failures.yaml` and continue to Phase 2. The Phase 1 extraction is still valid.

---

### Phase 2: Invoke draft-followup

Generate the session recap emails (external + internal).

1. Invoke `draft-followup` with the session path
   - Pass `_meta.board_dir` as context so draft-followup writes a board entry
   - draft-followup will read `context.yaml` for pre-extracted intelligence
   - It will write `board/draft-followup-output.yaml` after completion
2. Read `board/draft-followup-output.yaml`
3. **Quality gate**: Check `quality_pass` (threshold: Forward Test 18/24)
   - If `true` → proceed
   - If `false` → retry once with enriched session context (max 1 retry)
   - If retry fails → produce with warnings, log to failures.yaml, continue (non-blocking — draft exists, user reviews manually)
4. Note `leave_behind_recommended` — if true, queue Phase 5
5. Note `open_questions_from_session` — if any have `needs_research: true`, queue Phase 3a
6. Note `action_items_from_session` — items with `covered_in_email: false` feed Phase 3

### Phase 2.1: Vault Consistency Validation (NEW)

**After draft-followup completes**, validate wiki-links in the session file are resolvable:

```
Phase 2.1: Wiki-Link Integrity Check

1. READ SESSION FILE
   Open Sessions/[account]/[type]/[date].md
   Extract all wiki-links from frontmatter:
   - attendees_internal
   - attendees_customer
   - use_cases
   - account

2. VALIDATE EACH LINK
   For each wiki-link [[Path/to/Entity]]:
   a. Check if file exists at that path
   b. IF not found:
      WARN: "Orphaned link in session frontmatter: [[Path]]. File does not exist."
      ACTION: "Add to vault manually or remove link if stale."
      RECORD: failures.yaml entry

3. PROCEED WITH WARNINGS
   Even if orphaned links found, continue to Phase 2.5 (non-blocking).
   Flag in processing report that manual cleanup may be needed.
```

---

### Phase 2.5: V2 Smart Follow-Up Routing (Enhanced)

After draft-followup completes, read its board output and make intelligent routing decisions:

```
READ board/draft-followup-output.yaml

# Quality-Pass Check (NEW)
# NOTE: If quality_pass is false from draft-followup, we may still need email-render
# to cover uncovered action items. Check below before skipping Phase 3.

quality_pass = board/draft-followup-output.yaml.quality_pass
IF quality_pass == false:
  WARN: "Draft-followup quality below threshold (Forward Test < 18/24)."
  LOG: "Proceeding with warnings. Check final output carefully."
  # Continue to decision logic below — don't block; just flag

# Decision 1: Is email-render needed?
uncovered_items = [a for a in action_items_from_session if a.covered_in_email == false]
IF len(uncovered_items) == 0:
  SKIP Phase 3 entirely (draft-followup covered everything)
  LOG: "All action items covered by session recap — skipping email-render"
ELIF quality_pass == false:
  # Low-quality draft → email-render may help cover gaps
  LOG: "Quality below threshold + uncovered items exist — proceeding with email-render"
  # Continue to Phase 3

# Decision 2: Is the meeting routine?
IF meeting_type in {"1on1", "team_standup", "weekly_sync"} AND len(action_items) <= 2:
  SKIP Phase 5 (leave-behind one-pager)
  LOG: "Routine meeting with few action items — skipping leave-behind"

# Decision 3: Should we research open questions?
research_worthy = [q for q in open_questions_from_session if q.needs_research == true]
IF len(research_worthy) == 0:
  SKIP Phase 3a
  LOG: "No research-worthy questions — skipping fe-answer-customer-questions"

# Decision 4: Is Salesforce writeback worthwhile?
READ vault_summary(account) → use_cases
uco_matches = [uc for uc in use_cases if uc.sfdc_id is not null]
IF len(uco_matches) == 0:
  SKIP Phase 6
  LOG: "No Salesforce UCOs for {account} — skipping writeback"
ELIF session_type == "internal":
  SKIP Phase 6
  LOG: "Internal meeting — no MEDPICC signals to write back"

# Decision 5: Is Gmail draft creation safe? (evaluated in Phase 4, after email-render runs)
# NOTE: thread_check comes from email-render board output, not draft-followup.
# This decision is applied when creating Gmail drafts in Phase 4, not here.
# Documented in Phase 2.5 for routing completeness; actual check is in Phase 4.
```

Apply these routing decisions to the subsequent phases. Each Phase still has its own Skip condition as a safety net — these V2 decisions are additive intelligence, not replacements.

### Phase 2.6: Update Deal Tracker (conditional)

Update the account's running Google Doc deal tracker with workstream entries from this meeting.

**Skip if:** `meeting_type` in `{internal, team_standup, 1on1}` OR no account identified.

```
1. Read account frontmatter for deal_tracker_doc_id
2. IF deal_tracker_doc_id is empty:
   - draft-followup Step 4d will handle creation during its run
   - Check board/draft-followup-output.yaml for deal_tracker.doc_id after Phase 2 completes
3. IF deal_tracker_doc_id is populated:
   - draft-followup Step 4d already updated the doc during Phase 2
   - Read deal_tracker results from board/draft-followup-output.yaml
4. Write board entry: board/deal-tracker-output.yaml (from draft-followup board data)
5. Slack notification text is at: Sessions/[Account]/[type]/emails/[YYYY-MM-DD]_slack.txt
```

**Note:** The actual doc creation/update logic lives in draft-followup Step 4d. This phase is the coordinator's awareness of the deal tracker — it reads the output and includes it in the processing report.

Add to Phase 7 Processing Report table:

```
| 2.6 | deal-tracker | {DONE/SKIP} | — | Doc: [link] |
```

### Phase 3: Invoke email-render (conditional)

Generate action-thread emails for commitments NOT covered by the session recap.

**Skip condition:** If `board/draft-followup-output.yaml` shows all action items with `covered_in_email: true`, skip this phase.

1. Invoke `email-render` for each action item where `covered_in_email: false`
   - In the invocation prompt, pass the `_meta.board_dir` value from `context.yaml` (e.g., "Board directory: {board_dir}") — email-render reads `context.yaml` from this path to discover `_meta.board_dir`
   - email-render will read `context.yaml` and `board/draft-followup-output.yaml` for context
   - It will append to `board/email-render-output.yaml` after completion (merge, not overwrite — supports multiple invocations)
2. Read `board/email-render-output.yaml`
3. **Quality gate**: Check `quality_pass` — all emails CLEAN?
   - If false → log warnings, continue (non-blocking)
4. Note `action_items_remaining` — these need manual follow-up (flag in processing report)

### Phase 3a: Invoke fe-answer-customer-questions (conditional, adapter)

**Skip condition:** If no open questions have `needs_research: true`, skip this phase.

1. Invoke `fe-answer-customer-questions` skill (fe-vibe — cannot write to board)
2. Capture output: question count, answers, confidence levels, gaps
3. Write adapter board entry to `board/fe-answer-customer-questions-output.yaml`:

```yaml
skill_name: "fe-answer-customer-questions"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "post-meeting"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  questions_answered: N
  questions:
    - question: "{text}"
      answer_summary: "{brief answer}"
      confidence: "{high|medium|low}"
      sources: []
  gaps: []                              # questions with no good answer

quality_assessment: "{coordinator's evaluation of answer quality}"
quality_pass: true/false
```

### Phase 4: Create Gmail Drafts (conditional, adapter)

**Skip condition:** If Gmail is unavailable (test via gmail_builder.py search), skip this phase.

1. For each email draft (from draft-followup AND email-render) where recipient email is resolved:
   - Invoke `gmail` skill (fe-vibe) to create Gmail draft
   - Capture: draft_id, recipient, subject, thread_ts
2. Write adapter board entry to `board/gmail-output.yaml`:

```yaml
skill_name: "gmail"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "post-meeting"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  drafts_created:
    - draft_id: "{id}"
      recipient: "{email}"
      subject: "{subject}"
      thread_id: "{if reply}"
      source_skill: "{draft-followup|email-render}"
  drafts_skipped:
    - recipient: "{name}"
      reason: "{no email resolved|gmail error|etc.}"

quality_assessment: ""
quality_pass: true/false
```

### Phase 5: Invoke one-pager-render (conditional)

**Skip condition:** If `board/draft-followup-output.yaml` shows `leave_behind_recommended: false`, skip this phase.

1. Generate a minimal strategy contract for the one-pager from the leave-behind details:
   - `variant_type` from draft-followup's assessment
   - `hero_message` from `hero_message_seed`
   - `audience` from session attendees and missing stakeholder analysis
2. Inject `_meta.board_dir` into the strategy contract
3. Invoke `one-pager-render` with the strategy contract
   - It will write `board/one-pager-render-output.yaml` after completion
4. **Quality gate**: Check `quality_pass` (threshold: 18/24)
   - If pass → include in processing report
   - If fail → retry once, then skip (non-blocking)

### Phase 6: Salesforce Signal Writeback (conditional, adapter)

**Skip condition:** If account has no Salesforce UCOs (check via `vault_summary(account)` → use_cases with SFDC IDs), skip this phase.

1. Invoke `salesforce-actions` skill (fe-vibe) to write signals:
   - MEDPICC signal updates from context.yaml
   - Risk severity changes
   - Commitment tracking
2. Write adapter board entry to `board/salesforce-actions-output.yaml`:

```yaml
skill_name: "salesforce-actions"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "post-meeting"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  objects_read: []
  objects_written: []
  uco_ids: []

quality_assessment: ""
quality_pass: true/false
```

### Phase 7: Write Processing Report

Write a summary to `_System/Logs/post-meeting-report-{timestamp}.md`:

```markdown
# Post-Meeting Processing Report

**Session:** {session_path}
**Account:** {account}
**Meeting Type:** {meeting_type}
**Date:** {date}
**Processed:** {timestamp}
**Board:** .pipeline/post-meeting/

## Results

| Phase | Skill | Status | Quality | Notes |
|-------|-------|--------|---------|-------|
| 1 | transcript-parse | {DONE} | — | Session: {path} |
| 1.5 | signal-extractor-v2 | {DONE/SKIP/FAIL} | — | {N} signals, {N} commitments, {N} deltas |
| 2 | draft-followup | {DONE/WARN/FAIL} | {score}/{max} | {notes} |
| 2.6 | deal-tracker | {DONE/SKIP} | — | Doc: {link} |
| 3 | email-render | {DONE/SKIP/WARN} | {score}/{max} | {notes} |
| 3a | answer-questions | {DONE/SKIP} | {confidence} | {notes} |
| 4 | gmail | {DONE/SKIP/ERROR} | — | {N} drafts created |
| 5 | one-pager | {DONE/SKIP/WARN} | {score}/{max} | {notes} |
| 6 | salesforce | {DONE/SKIP/ERROR} | — | {notes} |

## Action Items

### Covered by Emails
{list from draft-followup + email-render board outputs}

### Requiring Manual Follow-Up
{list from email-render action_items_remaining}

## Warnings
{list from failures.yaml}
```

### Phase 8: Archive Board

After processing report is written:

1. Move `.pipeline/post-meeting/` to `.pipeline/completed/post-meeting-{timestamp}/`
2. Present processing report summary to user

## Supervision Tree

For staleness detection (skills that don't produce board output within expected turns), see `.pipeline/schemas/README.md → Skill Invocation Timeout Guidance`.

| Primitive | Threshold | Retry | Degrade | Escalate |
|-----------|-----------|-------|---------|----------|
| Transcript parse | All speakers identified | Re-parse with vault entity hints | Accept [Unknown] speakers, flag in session.md | Log, user resolves manually |
| signal-extractor-v2 | Pydantic validation passes | 1 retry with reduced max_tokens | Fall back to Phase 1 extraction only | Log API error, continue to Phase 2 |
| draft-followup | Forward Test 18/24 | 1 retry with enriched context | Produce with warnings | Log, skip Gmail draft creation |
| email-render | Q1-Q14 all CLEAN | 1 retry per email | Save with `status: flag_review` | Log warnings |
| gmail (adapter) | Draft created | 2 retries on API call | Save as local .md only (no Gmail draft) | Log API error |
| one-pager-render | 18/24 rubric | 1 retry | Skip leave-behind, note in report | Log |
| fe-answer-questions (adapter) | Confidence >= medium | 1 retry with refined query | Accept with low-confidence flag | Log |
| salesforce-actions (adapter) | Records updated | 1 retry on API call | Skip SF writeback, note in report | Log SF error |

## Cross-Primitive Consistency Check (V1 — Count-Based)

After all skills complete (before Phase 7), run a simple count-based consistency check:

```
CONSISTENCY CHECK:
  Action items in context.yaml:      [N]
  Action items in draft-followup:    [M] (covered_in_email: true)
  Action items in email-render:      [K] (addressed)
  Action items remaining:            [N - M - K]
  → PASS if remaining = 0 | FLAG if remaining > 0

  Commitments in context.yaml:       [N]
  Commitments in draft-followup:     [M] (referenced in emails)
  → FLAG if M < N (some commitments not in any email)
```

Write results to `board/consistency-check.yaml`. This is V1 (count-based only). V2 will add semantic matching.

## Fe-Vibe Adapter Protocol

Fe-vibe skills cannot write to the board. When this coordinator invokes them, it captures the output and writes a board entry on their behalf. Adapter board entries are written inline during the pipeline phases above. This section defines the canonical capture schemas.

### gmail Adapter

**When invoked:** Phase 4, for each email draft where recipient email is resolved.

**Write to:** `{board_dir}/board/gmail-output.yaml`

```yaml
skill_name: "gmail"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "post-meeting"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  drafts_created:
    - draft_id: "{Gmail draft ID}"
      recipient: "{email address}"
      subject: "{subject line}"
      thread_id: "{if replying to existing thread}"
      source_skill: "{draft-followup|email-render}"
  drafts_skipped:
    - recipient: "{name}"
      reason: "{no email resolved|gmail API error|rate limit|etc.}"
  total_created: N
  total_skipped: N

quality_assessment: "{e.g., '3/4 drafts created successfully, 1 skipped — no email for Dr. Chen'}"
quality_pass: true/false
```

### salesforce-actions Adapter

**When invoked:** Phase 6, when MEDPICC signals or commitments need Salesforce writeback.

**Write to:** `{board_dir}/board/salesforce-actions-output.yaml`

```yaml
skill_name: "salesforce-actions"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "post-meeting"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  objects_read:
    - object_type: "{UCO|Account|Opportunity}"
      object_id: ""
      fields_read: []
  objects_written:
    - object_type: "{UCO|Account|Opportunity}"
      object_id: ""
      fields_updated: []
      operation: "{create|update}"
  uco_ids: []                           # UCO IDs touched
  signals_written:
    - signal_type: "{medpicc_type}"
      severity: "{critical|high|medium|low}"
      status: "{open|in_progress|resolved}"

quality_assessment: ""
quality_pass: true/false
```

### fe-answer-customer-questions Adapter

**When invoked:** Phase 3a, when open questions from the session need researched answers.

**Write to:** `{board_dir}/board/fe-answer-customer-questions-output.yaml`

```yaml
skill_name: "fe-answer-customer-questions"
adapter: true
invoked_at: "{ISO timestamp}"
invoked_by: "post-meeting"
proxy_reason: "fe-vibe skill cannot write to board"

captured_output:
  questions_answered: N
  questions:
    - question: "{text from session}"
      asked_by: "{stakeholder name}"
      answer_summary: "{brief answer}"
      confidence: "{high|medium|low}"
      sources:
        - title: ""
          url: ""
  gaps:
    - question: "{unanswered question}"
      reason: "{no authoritative source found|ambiguous question|etc.}"
  avg_confidence: "{high|medium|low}"

quality_assessment: ""
quality_pass: true/false
```
