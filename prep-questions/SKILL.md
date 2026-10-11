# Pre-Meeting Question Prep

Research answers to pre-submitted questions from a Google Form before weekly syncs. Reads from Google Sheet, researches using vault + Glean + docs + web, writes answers back to Sheet + vault prep doc.

## Weekly Lifecycle (IMPORTANT)

**One form, one Sheet, forever.** Never recreate them per week.

The `Researched` column is the week separator:
- **Empty** = queued for the next meeting
- **Timestamped** = answered and done

```
Mon-Sat: Attendees submit questions → Sheet rows with blank Researched column
Sun 9 PM: Cron runs → researches all unresearched rows → writes prep doc for next Monday
Mon AM: Review prep doc
Mon meeting: Discuss questions verbally
Mon PM onwards: New submissions queue for the following Monday
```

**Prep doc naming:** `Sessions/{account}/prep/{next_monday_date}-questions.md` — one doc per meeting, never overwrites.

**Meeting date resolution:**
- If `--meeting-date YYYY-MM-DD` flag → use that
- If today is Sun or Mon → use this coming Monday
- Otherwise → next Monday after today

**Carryover:** If a question was answered with low confidence and needs re-research, manually clear the `Researched` cell in the Sheet — it re-queues automatically.

**Late submissions:** If someone submits Monday morning after the Sunday cron ran, manually run `/prep-questions nwm` — it only researches new unresearched rows.

## Trigger

Invoke when:
- User runs `/prep-questions [account]`
- Cron fires Sunday night (automated)
- User says "prep the questions for [account]"

## Usage

```
/prep-questions nwm                                      # Research unanswered questions for next Monday
/prep-questions nwm --meeting-date 2026-04-20            # Override target meeting date
/prep-questions nwm --all                                # Re-research all questions (including answered)
/prep-questions nwm --reopen-low-confidence              # Re-queue previously low-confidence answers
/prep-questions setup --account nwm --sheet-id XXX --webapp-url YYY
```

## Config

**Location:** `~/.claude/skills/prep-questions/config.yaml`

```yaml
accounts:
  northwestern-medicine:
    sheet_id: ""           # Google Sheet ID from URL
    webapp_url: ""         # Apps Script web app URL
    form_url: ""           # Google Form URL (for reference/sharing)
    account_name: "Northwestern Medicine"  # Vault account name
```

## Prerequisites

- Google Form + linked Sheet with Apps Script deployed (see SETUP.md)
- `webapp_url` configured in config.yaml
- Vault MCP available (for account context)

## Pipeline

### Phase 0: Load Config

```
1. Read ~/.claude/skills/prep-questions/config.yaml
2. Resolve account alias:
   - "nwm" → "northwestern-medicine"
   - "northwestern" → "northwestern-medicine"
   - "chla" → "chla"
   (Add aliases as accounts are onboarded)
3. Validate webapp_url is set — if not, error with setup instructions
```

**Account aliases:**

| Alias | Config Key |
|-------|-----------|
| nwm, northwestern, nm | northwestern-medicine |
| chla, childrens-la | chla |
| providence, prov | providence |
| choc | choc |

### Phase 1: Fetch Unanswered Questions

```bash
curl -sL "{webapp_url}?action=unanswered"
```

Returns JSON:
```json
{
  "count": 3,
  "questions": [
    {
      "row": 2,
      "timestamp": "2026-04-04T10:30:00",
      "name": "Martin Ivanov",
      "question": "How do I get task-level DBU attribution for serverless jobs?",
      "context": "Looking at system tables but can't find 1:1 mapping"
    }
  ]
}
```

**If count is 0:** Report "No unanswered questions for {account}. Nothing to prep." and exit.

**If `--all` flag:** Use `?action=all` instead and research all rows (overwrite existing answers).

### Phase 2: Research Each Question

For each question, run a **4-layer research cascade**. Stop early if high-confidence answer found.

#### Layer 1: Vault Search (always runs)

```
vault_search(query="{question}", account="{account_name}", limit=10)
vault_signals(account="{account_name}")
```

Look for:
- Past session discussions about this topic
- Existing action items or commitments related to the question
- Stakeholder context (who's asking, what's their role, what have we discussed before)

**Confidence boost:** If vault has a direct answer from a prior session → high confidence.

#### Layer 2: Glean (if available)

```
mcp__glean__glean_read_api_call(endpoint="search.query", body={"query": "{question}"})
```

Search internal Databricks knowledge base for:
- Product documentation
- Internal field guides
- Best practices
- Known limitations

**Graceful degradation:** If Glean MCP is not available (tool not found, 403, timeout), skip and log: "Glean unavailable — skipping internal KB search."

#### Layer 3: Context7 / Databricks Docs (if available)

```
mcp__context7__resolve-library-id(libraryName="databricks")
mcp__context7__get-library-docs(libraryId="{id}", topic="{question}")
```

Search official Databricks documentation for:
- Feature documentation
- API references
- Configuration guides
- Known issues

**Graceful degradation:** If context7 MCP is not available, skip and log: "Context7 unavailable — skipping docs search."

#### Layer 4: Web Search (fallback)

```
WebSearch(query="{question} databricks")
```

Then fetch top 2-3 results:
```
WebFetch(url="{result_url}", prompt="Extract the answer to: {question}")
```

Use for:
- Community forum answers
- Blog posts with solutions
- Release notes
- Stack Overflow answers

**Only run if Layers 1-3 didn't produce a high-confidence answer.**

#### Answer Synthesis

After all layers complete, synthesize:

```yaml
answer: |
  {Direct answer in 2-4 sentences. Lead with the answer, not the context.
   If the answer is "you can't do this," say so clearly.
   Include specific steps, SQL, API calls, or config if applicable.
   Reference the source layer: "Based on our March 19 session..." or
   "Per Databricks docs..."}

confidence: high|medium|low
  # high: direct answer found in vault session or official docs
  # medium: answer synthesized from multiple sources, or partial match
  # low: best-effort from web search, or conflicting information

sources:
  - "Session: 2026-03-19 architecture deep-dive"
  - "Databricks docs: system tables reference"
  - "Community forum: stackoverflow.com/q/12345"
```

**Answer quality rules:**
- Lead with the answer, not preamble
- If the question references NWM-specific context (their notebooks, their clusters), use vault context to personalize
- If the answer requires a demo or hands-on session, say so: "This would be best covered with a live walkthrough. We can demo during the sync."
- Never fabricate — if unsure, say "Needs further investigation" with confidence: low
- Keep answers under 200 words — this goes into a spreadsheet cell

### Phase 3: Write Answers Back to Sheet

Construct the POST payload:

```json
{
  "answers": [
    {
      "row": 2,
      "answer": "There's no direct 1:1 mapping of job task to DBU for serverless...",
      "confidence": "high",
      "sources": "Session 2026-04-06; system tables docs"
    }
  ]
}
```

```bash
curl -sL -X POST "{webapp_url}" \
  -H "Content-Type: application/json" \
  -d '{payload}'
```

Verify response: `{"status": "ok", "rows_updated": N}`

If POST fails, log error but continue to Phase 4 (vault doc is the fallback).

### Phase 4: Write Vault Prep Doc

Create: `Sessions/{account_name}/prep/{YYYY-MM-DD}-questions.md`

```markdown
---
date: {YYYY-MM-DD}
type: prep
account: "[[Accounts/{account_name}]]"
source: google-form
questions_total: {N}
questions_answered: {N}
avg_confidence: {high|medium|low}
---

# Pre-Meeting Question Prep — {date}

**Account:** [[Accounts/{account_name}]] | **Source:** Google Form | **Researched:** {timestamp}

## Questions & Answers

### Q1: {question} — {asker_name}
{optional context from form}

**Answer:** {answer}

**Confidence:** {confidence} | **Sources:** {sources}

---

### Q2: {question} — {asker_name}
...

## Research Gaps

{List any questions with confidence: low or where further investigation is needed}

## Suggested Discussion Points

{Based on the questions, suggest related topics that might come up in the meeting.
 Cross-reference with vault signals and recent sessions.}
```

### Phase 5: Report

Output to user:

```
Prep complete for {account_name}

| # | Asker | Question (truncated) | Confidence |
|---|-------|---------------------|------------|
| 1 | Martin | How do I get task-level DBU... | high |
| 2 | Chris | Can we use metric views with... | medium |

Sheet updated: {N} answers written
Prep doc: Sessions/{account}/prep/{date}-questions.md

{If any low-confidence: "⚠ {N} questions need manual review before the meeting."}
```

## Error Handling

| Error | Action |
|-------|--------|
| webapp_url not configured | Print setup instructions, exit |
| Apps Script returns error | Log, skip Sheet write, still write vault doc |
| No questions to research | Report "nothing to prep", exit |
| Vault MCP unavailable | Skip Layer 1, continue with other layers |
| Glean unavailable | Skip Layer 2, continue |
| Context7 unavailable | Skip Layer 3, continue |
| All layers fail for a question | Write answer: "Needs manual research", confidence: low |

## Cron Behavior

When triggered by cron (Sunday night):
1. Run for ALL configured accounts (not just one)
2. Skip accounts with 0 unanswered questions
3. Write a summary to `_System/Logs/prep-questions-{date}.md`
4. No user interaction — fully autonomous

## Future Enhancements

- Slack notification when prep is ready
- Auto-tag questions by use case
- Learning loop: track which answers were useful in the meeting
- Multi-account rollup for Monday morning briefing
