# /morning-brief — Daily Morning Brief

## Trigger
- `/morning-brief`
- `/brief morning`

## Purpose
Single-screen daily summary: priority interrogations, account health, overdue commitments, today's meetings, recommended next action.

## Steps

### 1. Run the morning brief script
```bash
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/morning_brief.py
```

If the user specifies an account filter:
```bash
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/morning_brief.py --account {slug}
```

### 2. Present the output
Display the terminal markdown output directly in chat. Do not write to a file unless the user requests it.

### 3. Log invocation

```python
python3 -c "
import sys; sys.path.insert(0, '/Users/samuel.selvan/obsidian/sa-intel/_System/scripts')
from shared.invocation_logger import log_invocation
log_invocation(intent='morning_brief', caller_skill='morning-brief', outcome_tag='usable')
"
```

### 4. Offer next actions
Based on the brief content, offer to:
- Process a pending interrogation: `/process-transcript`
- Address an overdue commitment: `/follow-ups`
- Prep for today's meeting: `/prep {account}`

## Output
Terminal markdown with 5 sections:
1. **Priority Interrogations** — pending items from interrogation_queue (max 5)
2. **Account Health** — current health status per active account, flags changes
3. **Overdue Commitments** — action_items past due date
4. **Today's Meetings** — sessions scheduled for today (if data available)
5. **Recommended Next Action** — single highest-priority action

## Data Source
SQLite: `~/obsidian/sa-intel/_System/brain.db`

Tables queried:
- `interrogation_queue` — pending transcript processing
- `accounts` — health status for active accounts
- `action_items` — overdue commitments (kind in commitment, followup, general)
- `sessions` — today's meetings
- `signals` — recent open signals for context

## Scheduling

### Claude Code (recommended)
```
/schedule "Run morning brief" --cron "0 7 * * 1-5"
```

### crontab
```bash
# Edit with: crontab -e
0 7 * * 1-5 cd ~/obsidian/sa-intel && /usr/bin/python3 _System/scripts/morning_brief.py >> _System/scripts/logs/morning-brief.log 2>&1
```

### macOS launchd
Save as `~/Library/LaunchAgents/com.sa-intel.morning-brief.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sa-intel.morning-brief</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/samuel.selvan/obsidian/sa-intel/_System/scripts/morning_brief.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>7</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>1</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>7</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>2</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>7</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>3</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>7</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>4</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>7</integer>
            <key>Minute</key>
            <integer>0</integer>
            <key>Weekday</key>
            <integer>5</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>/Users/samuel.selvan/obsidian/sa-intel/_System/scripts/logs/morning-brief.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/samuel.selvan/obsidian/sa-intel/_System/scripts/logs/morning-brief.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/samuel.selvan/obsidian/sa-intel</string>
</dict>
</plist>
```

Load with:
```bash
launchctl load ~/Library/LaunchAgents/com.sa-intel.morning-brief.plist
```
