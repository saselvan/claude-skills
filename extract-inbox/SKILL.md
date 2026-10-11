# /extract-inbox

Process unprocessed inbox items from brain.db, extracting signals via the W1 extractor pipeline.

## Trigger

- User says `/extract-inbox`
- Scheduled every 15 minutes via Claude Code `/schedule` or system cron

## Behavior

1. Query brain.db for up to 20 rows where `triage_status = 'unreviewed'`, ordered by `created_at ASC`
2. For each item:
   - Classify source tier (`customer_domain`, `sa_observation`, `internal`, `unknown`)
   - Route to extractor by `source_type` (session / email / capture / raw_file)
   - Extract signals using `render_derived.process_chunk`
   - On success: set `triage_status = 'reviewed'`, `reviewed_at = now()`
   - On failure: set `triage_status = 'needs_clarification'`, log error, insert into `interrogation_queue`
3. Log summary: N processed, N failed, N remaining

## Steps

```bash
# Run the extractor script
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/extract_inbox.py
```

### Dry run (preview only, no DB writes)
```bash
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/extract_inbox.py --dry-run
```

### Custom batch size
```bash
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/extract_inbox.py --limit 10
```

### Custom DB path
```bash
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/extract_inbox.py --db /path/to/brain.db
```

## Scheduling

### Option A: Claude Code scheduled skill (preferred)
```
/schedule extract-inbox --cron "*/15 * * * *" --prompt "/extract-inbox"
```

### Option B: launchd plist
Copy `com.sa-intel.extract-inbox.plist` to `~/Library/LaunchAgents/` and load:
```bash
launchctl load ~/Library/LaunchAgents/com.sa-intel.extract-inbox.plist
```

### Option C: crontab
```
*/15 * * * * cd /Users/samuel.selvan/obsidian/sa-intel && python _System/scripts/extract_inbox.py >> _System/scripts/logs/extract_inbox.log 2>&1
```

## Error Handling

- Failed items get `triage_status = 'needs_clarification'` with error stored in `action_label`
- Failed items surface in morning brief via `SELECT * FROM inbox WHERE triage_status = 'needs_clarification'`
- Batching: max 20 items per run to avoid rate limits and context overflow
- Script is idempotent: re-running processes only `unreviewed` items

## Database

- **Table:** `inbox` in brain.db
- **Statuses:** `unreviewed` -> `reviewed` (success) | `needs_clarification` (failure) | `skipped` (manual)
- **Related table:** `interrogation_queue` for failed items needing human review

## Companion: watch_raw.py

The `watch_raw.py` script monitors `_raw/` for new .md files and inserts them into the inbox table automatically. Run it as a background daemon alongside this skill.

```bash
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/watch_raw.py
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/watch_raw.py --poll-interval 30
```
