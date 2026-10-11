# /correct — Correction Primitive

## Trigger
`/correct [source_page_path] [claim_selector]`

Examples:
- `/correct _wiki/accounts/nwm.md "## Tech Stack > Epic Version"`
- `/correct _wiki/accounts/chn.md "## Stakeholders > CIO"`

## Purpose
Record a structured correction against a wiki page claim. Corrections are applied by `compile_wiki.py` during reconciliation — overriding or demoting stale/wrong claims.

## Behavior

### Step 1: Read the source page
```
Read the file at {source_page_path} (resolve relative to VAULT_ROOT: ~/obsidian/sa-intel/).
If the file does not exist, abort with an error message.
```

### Step 2: Identify the claim
```
Locate the claim at {claim_selector}. The selector uses heading path notation:
  - "## Tech Stack > Epic Version" = under H2 "Tech Stack", the line about Epic Version
  - "## frontmatter.stage" = the stage field in frontmatter
  - "## Risks > #3" = third bullet under H2 "Risks"

Display the identified claim text to the user for confirmation.
```

### Step 3: Auto-fill fields
Determine these automatically from the source page:
- **source_type**: Infer from path:
  - `_wiki/accounts/` → `account_state`
  - `_wiki/stakeholders/` or `People/` → `stakeholder_view`
  - `_wiki/` (other) → `wiki_page`
  - Derived chunks → `derived_chunk`
- **source_id**: Extract from frontmatter (e.g., account slug, stakeholder ID) or filename stem
- **source_page_path**: The provided path
- **claim_selector**: The provided selector
- **applies_when**: Default to `"always"` unless the claim is account-specific (then `"when account={slug}"`)

### Step 4: Prompt user for correction details
Ask the user for:
1. **correction_type**: `override` (replace the claim) or `demote` (reduce confidence, flag as disputed)
2. **assertion**: What the correct value/claim should be
3. **rationale**: Why the original was wrong
4. **evidence** (optional): Supporting evidence — session references, external sources, etc.

### Step 5: Write correction markdown file
Generate a `correction_id` (use Python: `secrets.token_hex(16)`).

Write to `_wiki/_corrections/{correction_id}.md`:
```markdown
---
correction_id: {id}
source_page_path: {path}
claim_selector: {selector}
correction_type: override|demote
applies_when: always
is_active: true
created_at: {ISO8601}
---

## Assertion
{what the correct value should be}

## Rationale
{why the original was wrong}

## Evidence
{supporting evidence, session references, etc.}
```

### Step 6: Insert into brain.db
Run via Python or sqlite3 CLI:
```python
import sqlite3, secrets
from datetime import datetime, timezone

db = sqlite3.connect("/Users/samuel.selvan/obsidian/sa-intel/_System/brain.db")
correction_id = secrets.token_hex(16)
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

db.execute("""
    INSERT INTO corrections
    (correction_id, source_type, source_id, source_page_path, claim_selector,
     correction_type, assertion, rationale, applies_when, is_active, created_by, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'samuel', ?)
""", (correction_id, source_type, source_id, source_page_path, claim_selector,
      correction_type, assertion, rationale, applies_when, now))
db.commit()
db.close()
```

### Step 7: Confirm
Print summary:
```
Correction recorded:
  ID:        {correction_id}
  Type:      {correction_type}
  Source:    {source_page_path} > {claim_selector}
  Assertion: {assertion}
  File:      _wiki/_corrections/{correction_id}.md
  DB:        corrections row inserted

Next compile_wiki.py run will apply this correction.
```

## Output Convention
- Markdown file: `_wiki/_corrections/{correction_id}.md`
- Database: `corrections` table in `brain.db`
- No sidecar needed (corrections are internal, not artifacts)
- Do NOT call `vault_reindex` — corrections are compiler-internal, not vault entities

## Dependencies
- brain.db must have `corrections` table (migration 0014 creates it as `corrections_v2`; migration 0015 renames it to `corrections`)
- Run migrations first if table missing: `sqlite3 _System/brain.db < _System/migrations/0014-corrections-v2.sql && sqlite3 _System/brain.db < _System/migrations/0015-rename-corrections.sql`
