# /dump — Quick Capture to Vault Raw Staging

Zero-friction content capture into `_raw/YYYY-MM-DD/` with automatic source tier classification and brain.db inbox registration.

## Trigger

User says `/dump`, "dump this", "quick capture", "save to raw", or "brain dump".

## Usage

```
/dump "Quick thought or observation"
/dump --tier customer_domain "Customer said X"
/dump --tier databricks_internal "SFDC shows renewal in 90 days"
/dump --file /path/to/content.md
/dump --file /path/to/content.md --tier auto
/dump --title "NWM Data Mesh Feedback" "They want schema-level governance for Unity Catalog"
```

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| content | (required) | Text to capture, or use `--file` |
| `--file` | - | Path to file to route instead of inline text |
| `--tier` | `auto` | Source tier: `auto`, `customer_domain`, `sa_observation`, `databricks_internal`, `curated_external`, `casual_external` |
| `--title` | - | Optional title (used for filename and frontmatter) |

## Steps

### 1. Parse Input

Extract content, tier, title, and optional file path from the user's message.

If no `--tier` specified, default to `auto` (classify_source.py decides).
If content is clearly SA-authored (no email headers, no URL), tier will resolve to `sa_observation`.

### 2. Route to _raw/

Run the routing script:

```bash
# For inline content:
echo "$CONTENT" | python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/route_to_raw.py \
  --stdin --tier "$TIER" --title "$TITLE"

# For file input:
python /Users/samuel.selvan/obsidian/sa-intel/_System/scripts/route_to_raw.py \
  --file "$FILE_PATH" --tier "$TIER"
```

This will:
- Write to `_raw/YYYY-MM-DD/{slug}.md` with source_tier frontmatter
- Register in `brain.db` inbox table for extraction scheduling

### 3. Confirm

Print confirmation with:
- Output file path
- Assigned source tier
- Inbox registration status

### 4. Reindex (optional)

If the content is high-priority (tier 1 or 2), suggest running extraction:

```
Captured to _raw/2026-04-19/nwm-data-mesh-feedback.md (tier: customer_domain)
Registered in brain.db inbox for extraction.

Tip: Run /process-notes to extract entities and signals from pending inbox items.
```

## Output Convention

- **Write path**: `_raw/YYYY-MM-DD/{title-slug}.md`
- **Frontmatter**: `source_tier`, `routed_at`, `title`, `source_file` (if from file)
- **brain.db**: Registered in `inbox` table with `extracted=0`

## Integration Points

- `/voice` routes transcribed voice through `/dump`
- `/process-transcript` routes raw transcripts through `/dump` before structured processing
- Orphan intake hook (`_System/hooks/orphan-intake.md`) catches files that bypass `/dump`
- `compile_wiki.py` processes `_raw/` items registered in inbox
- `promote_raw.py` archives processed items to `_raw/_archive/`
