---
description: "Register a local path as an inventory entity in brain.db. USE WHEN: user says 'register this repo', 'add to inventory', 'track this app', or '/register [path]'. Inspects directory for project type and writes to brain.db repos or apps table."
allowed-tools: Read, Write, Bash, Glob, Grep
---

# /register — Vault Inventory Registration

## Purpose

Register a local directory as a first-class inventory entity in `_System/brain.db`.
Answers workflow #9: "Where is my stuff?"

## Trigger

- `/register [path]`
- `/register ~/repos/foo`
- `/register ~/repos/foo --account nwm --status active`
- `/register ~/repos/foo --type repo` (override auto-detection)

## Detection Logic

Given a directory path, inspect for project indicators:

| File Found | Entity Type | Language/Runtime |
|---|---|---|
| `app.yaml` | app (Databricks App) | python |
| `pyproject.toml` or `setup.py` | repo | python |
| `package.json` | repo | node |
| `go.mod` | repo | go |
| `Cargo.toml` | repo | rust |
| `app.yaml` + `pyproject.toml` | app (prefer app if app.yaml present) | python |
| `.git` only | repo | unknown |

**Priority:** app.yaml → repo with language detection → bare repo

## Step 1: Inspect Path

```bash
# Check for project indicators
ls {path}/app.yaml 2>/dev/null
ls {path}/pyproject.toml 2>/dev/null
ls {path}/package.json 2>/dev/null
git -C {path} remote get-url origin 2>/dev/null
git -C {path} log -1 --format='%ci' 2>/dev/null | cut -c1-10
```

## Step 2: Read app.yaml if present

Extract name, description, deploy_target, demo_url if present:
```yaml
# app.yaml fields of interest
command: ...
description: ...
```

## Step 3: Resolve account

1. Check if user passed `--account` flag → use that slug
2. Check path for account hints: `~/repos/{account}-*`, path contains `nwm`/`chn`
3. Check `_System/account-slugs.yaml` for valid slugs
4. Default to `_internal` if ambiguous

Account must be a valid slug from `_System/account-slugs.yaml` or `_cross` / `_internal`.

## Step 4: Check for existing artifact

```sql
-- Check if this repo's path is already in artifacts
SELECT id FROM artifacts WHERE file_path LIKE '%{basename}%' LIMIT 1
```

## Step 5: Write to brain.db

For **repos:**
```python
import sqlite3, hashlib, os
db = sqlite3.connect('_System/brain.db')
repo_id = hashlib.md5(path.encode()).hexdigest()[:16]
db.execute("""
  INSERT OR REPLACE INTO repos
    (id, name, path, language, last_commit, remote_url, account_id, artifact_id, created_at)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'))
""", [repo_id, name, path, language, last_commit, remote_url, account_id, artifact_id])
db.commit()
```

For **apps:**
```python
app_id = hashlib.md5(path.encode()).hexdigest()[:16]
db.execute("""
  INSERT OR REPLACE INTO apps
    (id, name, path, runtime, deploy_target, status, demo_url, account_id, created_at, updated_at)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'), date('now'))
""", [app_id, name, path, 'python', deploy_target, status, demo_url, account_id])
db.commit()
```

## Step 6: Reindex

```python
vault_reindex(full=False, embed=False)
```

## Step 7: Confirm

Output:
```
✓ Registered: {entity_type} — {name}
  ID:       {id}
  Path:     {path}
  Account:  {account}
  Language: {language}
  Remote:   {remote_url or "local only"}
  brain.db: repos/{apps} table updated
```

## Batch Mode

`/register ~/repos/` — registers ALL subdirectories that contain .git, app.yaml, pyproject.toml, or package.json.

Skip if:
- Already registered (same path in db with recent `created_at`)
- Path is a node_modules, .venv, or build directory
- No project indicators found

## Queries After Registration

```sql
-- All repos
SELECT name, language, account_id, last_commit FROM repos ORDER BY last_commit DESC;

-- Apps by account
SELECT name, status, deploy_target, demo_url FROM apps WHERE account_id = 'nwm';

-- Join: repo with artifact
SELECT r.name, r.path, a.title FROM repos r
  LEFT JOIN artifacts a ON r.artifact_id = a.id;
```

## Output Convention

This skill writes to `brain.db` only — no artifact files created.
After writing: `vault_reindex(full=false, embed=false)`.

$ARGUMENTS
