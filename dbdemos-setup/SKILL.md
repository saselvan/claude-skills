---
name: dbdemos-setup
description: Set up a project for dbdemos contribution. Use when building a new demo for dbdemos, contributing to an existing demo, or setting up the dbdemos development environment. Triggers on "dbdemos", "contribute demo", "new demo setup".
---

# dbdemos Contribution Setup

Automate the FULL setup for contributing to [dbdemos](https://dbdemos.ai) — Databricks' official demo distribution platform. This skill does everything, not just scaffolding.

Reference: https://databricks.atlassian.net/wiki/spaces/HUB/pages/5034082566/How+to+Contribute+to+dbdemos

## Who gets what

Every demo has TWO audiences. Same app code, two deployment targets:

- **AEs** can't run notebooks. They need a live app URL they can bookmark and show customers. You deploy this once to a shared workspace using `databricks-demo` skill. You maintain it.
- **SAs + customers** can run `dbdemos.install()`. They get the notebooks + app code on their own workspace. This skill packages that.

**Build once, deploy twice.** Build the demo in dbdemos format from the start (this skill scaffolds it). Then:
1. Deploy the app to a shared workspace for AEs → use `databricks-demo` / `databricks-apps` skills
2. PR the notebooks to dbdemos for SAs/customers → this skill handles it

## Architecture

dbdemos consists of 4 GitHub repos (all public, all under `databricks-demos/`):

| Repo | Purpose | Fork When |
|------|---------|-----------|
| `dbdemos-notebooks` | The actual demo notebooks | Always |
| `dbdemos-resources` | Static images, GIFs, icons | Demo has visual assets |
| `dbdemos-dataset` | Raw/bronze datasets (syncs to public S3) | Demo ships data |
| `dbdemos` | Packaging (`pip install dbdemos`) | Rarely (maintainer only) |

## Workflow

### Phase 1: Discover Existing Project

If the user points to an existing project directory, READ IT FIRST:
- Read `README.md`, `PROJECT.md`, `DEMO.md` to understand what the demo does
- Check for existing `_dbdemos/` directory (partial conversion already started)
- Inventory: notebooks, datasets, images, architecture diagrams, scripts
- Auto-derive answers to Phase 2 questions from what you find

**Upstream skill artifacts (richest sources — check these first):**

| File | Produced By | What to Extract |
|------|-------------|-----------------|
| `*-DEMO_SPEC.md` | `/demo spec` | Demo name, industry, category, description, data tables, platform features, scope, build sequence, app framework |
| `gap-analysis.md` | `/demo brainstorm` | Outcome map position, target audience, wow moment, plugin stack, complexity tier |
| `*-research.md` | `/demo research` | Proof points, competitive landscape, data model details, existing Databricks assets |
| `DEMO.md` | `databricks-demo` skill | Architecture, brand guidelines, what the demo does |
| `TASKS.md` | `databricks-demo` skill | Build progress, notebook inventory, deployment status |

If a `DEMO_SPEC.md` exists, it contains nearly everything Phase 2 needs — present for confirmation rather than asking.

### Phase 2: Gather Info (or confirm auto-derived)

If auto-derived from Phase 1, present for confirmation. Otherwise ask via AskUserQuestion:

1. **Demo name** — kebab-case identifier (e.g., `hls-patient-readmission`)
2. **Category** — one of:
   - Industry: `demo-HLS`, `demo-FSI`, `demo-manufacturing`, `demo-retail`, `demo-media`
   - Product: pick from `product_demos/` subcategories (e.g., `Data-Science`, `Delta-Live-Table`, `Unity-Catalog`)
3. **Short description** — one sentence on what the demo does
4. **Includes images?** — yes/no (determines if dbdemos-resources fork is needed)
5. **Includes datasets?** — yes/no (determines if dbdemos-dataset fork is needed)

### Phase 3: Fork Repos

Use `gh` CLI with the user's **personal GitHub account** (non-Databricks email).

```bash
# Check current GitHub auth — identify personal vs Databricks accounts
gh auth status

# Switch to personal account if needed
gh auth switch --user <personal-username>

# Fork notebooks (always required)
gh repo fork databricks-demos/dbdemos-notebooks --clone=false

# Fork resources (if images)
gh repo fork databricks-demos/dbdemos-resources --clone=false

# Fork datasets (if datasets)
gh repo fork databricks-demos/dbdemos-dataset --clone=false

# Switch back to primary account
gh auth switch --user <primary-username>
```

### Phase 4: Clone and Branch

```bash
gh repo clone <personal-username>/dbdemos-notebooks ~/repos/dbdemos-notebooks
cd ~/repos/dbdemos-notebooks && git checkout -b demo/<demo-name>
```

### Phase 5: Scaffold Demo Folder

Look at existing demos in the same category for the exact structure. Copy patterns from them.

**Industry demo** goes in `demo-HLS/<demo-name>/`, **product demo** in `product_demos/<subcategory>/<demo-name>/`.

Standard structure:
```
<demo-name>/
├── _resources/
│   ├── 00-setup.py            # Setup notebook (uses DBDemos class)
│   └── bundle_config.py       # REQUIRED — dbdemos packaging metadata
├── 00-<name>-introduction.py  # Intro notebook (markdown TOC with $./path links)
├── 01-<step>.py               # Numbered step notebooks
├── config.py                  # Catalog/schema/volume config
├── <app-folder>/              # App code (if demo includes a Databricks App)
│   ├── app.yaml
│   ├── main.py
│   └── requirements.txt
```

Create `config.py` following the existing demo pattern (includes analytics pixel).

**If the demo includes a Databricks App**, the app code lives directly in the demo folder as a subdirectory — NOT in a separate repo. See Phase 5d.

### Phase 5b: Create `_resources/bundle_config.py` (CRITICAL)

**Without this file, `dbdemos.install()` cannot find or package the demo.** This is a Python file containing a single dict expression — not a JSON file.

Read an existing demo's `bundle_config.py` in the same category for the exact pattern. Key fields:

```python
{
  "name": "<demo-name>",
  "category": "lakehouse",  # or "data-engineering", etc.
  "title": "<Human-Readable Title>",
  "serverless_supported": True,
  "custom_schema_supported": True,
  "default_catalog": "main",
  "bundle": True,
  "default_schema": "dbdemos_<short_slug>",
  "description": "<one-liner>",
  "fullDescription": "<HTML string with <br/>, <ul>, <li> tags>",
  "notebooks": [
    {
      "path": "_resources/00-setup",     # no .py extension
      "pre_run": False,
      "publish_on_website": False,
      "add_cluster_setup_cell": False,
      "title": "Setup",
      "description": "Provision catalog, schema, volume."
    },
    {
      "path": "01-Step-Name",
      "pre_run": True,                   # True if auto-run during install
      "publish_on_website": True,
      "add_cluster_setup_cell": True,
      "title": "Step Title",
      "description": "What this step does."
    }
    # ... one entry per notebook
  ],
  "init_job": { ... },   # Job definition for pre_run notebooks
  "cluster": { ... }     # Cluster spec for interactive use
}
```

**Rules:**
- `pre_run: True` only for notebooks that generate data (setup, load). Manual steps (deploy app, configure sync) = `pre_run: False`
- `add_cluster_setup_cell: True` for any notebook with executable code cells
- Notebook paths have NO `.py` extension
- `init_job.tasks` should only include notebooks that can run without manual intervention

### Phase 5c: Create `_resources/00-setup.py` (DBDemos Pattern)

**MUST use the shared `DBDemos` class** — do not manually create catalog/schema/volume.

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Setup — <Demo Title>
# MAGIC
# MAGIC Provisions the catalog, schema, and volume.
# MAGIC
# MAGIC <img width="1px" src="https://ppxrzfxige.execute-api.us-west-2.amazonaws.com/v1/analytics?category=lakehouse&notebook=_resources/00-setup&demo_name=<demo-name>&event=VIEW">

# COMMAND ----------

# MAGIC %run ../config

# COMMAND ----------

dbutils.widgets.dropdown("reset_all_data", "false", ["true", "false"], "Reset all data")
reset_all_data = dbutils.widgets.get("reset_all_data") == "true"

# COMMAND ----------

# MAGIC %run ../../../_resources/00-global-setup-v2

# COMMAND ----------

DBDemos.setup_schema(catalog, db, reset_all_data, volume_name)
```

**Add any demo-specific setup** (e.g., CDF enablement for Delta Sync) AFTER the `DBDemos.setup_schema()` call.

### Phase 5d: Include App Code (if demo has a Databricks App)

**App code lives directly in the demo folder as regular files (not notebooks).** dbdemos copies everything to the workspace — notebooks as notebooks, regular files as workspace files.

Proven pattern from existing dbdemos (`chatbot-rag-llm`, `ai-agent`):

```
<demo-name>/
├── 04-Deploy-App.py              # Notebook with deployment instructions
├── app/                          # or chatbot_app/, sentiment_app/, etc.
│   ├── app.yaml                  # Databricks App config
│   ├── main.py                   # FastAPI entrypoint
│   ├── requirements.txt          # Python dependencies
│   └── frontend/                 # React/static frontend (if applicable)
│       └── dist/                 # Built frontend assets
```

**Rules:**
- App folder name should be descriptive (e.g., `sentiment_app/`, `chatbot_app/`)
- The deploy notebook references app code via relative workspace paths
- App code is NOT listed in `bundle_config.py` notebooks array — only notebooks go there
- `app.yaml` widget/resource references should use generic defaults (same rule as notebooks)
- Build frontend locally (`npm run build`) and commit `dist/` — dbdemos users won't run `npm`

**Development workflow:**
- Build and test the app directly in the demo folder — no separate repo
- Use personal widget values during development
- Clean to generic defaults before PR (Phase 10b catches this)

### Phase 6: Port Notebooks from Source Project

**This is the critical step.** Don't just scaffold — actually convert the source project's notebooks into dbdemos format:

1. **Read each source notebook** from the existing project (e.g., `~/repos/hls-tech-demo/notebooks/`)
2. **Convert to dbdemos format**:
   - Add `# Databricks notebook source` header
   - Use `# MAGIC %md` for markdown cells
   - Use `# COMMAND ----------` separators
   - Add analytics pixel: `<img width="1px" src="https://ppxrzfxige.execute-api.us-west-2.amazonaws.com/v1/analytics?category=lakehouse&notebook=<name>&demo_name=<demo-name>&event=VIEW">`
   - Replace hardcoded catalog/schema with `config.py` references
   - Use `dbutils.widgets` for configurable parameters
3. **Copy setup/seed scripts** into `_resources/`
4. **Write each converted notebook** to the scaffolded folder

**SELF-CONTAINMENT RULES (hard-won):**

- **Inline all SQL/schema** — Notebooks must NOT reference external `.sql` files. `dbdemos.install()` copies notebooks to `/Repos/` where relative file paths break. Inline all DDL as Python strings.
- **No external file dependencies** — If the source project uses `open("../schema/001_initial.sql")`, convert that to an inline `SCHEMA_SQL = """..."""` variable in the notebook.
- **Widget defaults must be generic** — Never use personal instance names, workspace-specific profiles, or dev-specific values. Use empty strings (`""`) for instance names and `"DEFAULT"` for CLI profiles.
- **No hardcoded catalog/schema** — Always use `config.py` references (`catalog`, `schema`, `db`). Zero occurrences of the source project's catalog/schema names should remain.
- **Verify zero source-specific references** — After conversion, grep for the source project's catalog, schema, workspace URL, and personal usernames. All must be zero.

### Phase 7: Port Images to dbdemos-resources Fork

If the source project has architecture diagrams, screenshots, or images:

1. Clone the dbdemos-resources fork: `gh repo clone <user>/dbdemos-resources ~/repos/dbdemos-resources`
2. Create folder: `~/repos/dbdemos-resources/<demo-name>/`
3. Copy images from source project (e.g., `docs/*.png`, `docs/*.mmd`)
4. Update notebook image references to use the dbdemos-resources URL pattern:
   `https://raw.githubusercontent.com/databricks-demos/dbdemos-resources/main/<demo-name>/<image>`

### Phase 8: Port Datasets to dbdemos-dataset Fork

If the source project has datasets (CSVs, parquet files):

1. Clone the dbdemos-dataset fork: `gh repo clone <user>/dbdemos-dataset ~/repos/dbdemos-dataset`
2. Create folder: `~/repos/dbdemos-dataset/<demo-name>/`
3. Copy data files from source project
4. Update notebook data loading to use the dbdemos dataset URL pattern

### Phase 9: Write Vault Atom

After the build/scaffold is complete, write a vault artifact file so all demo metadata survives across sessions. This enables creating the JIRA ticket and Demo Review Doc in a later session without context loss.

**Write to:** `~/obsidian/sa-intel/Artifacts/dbdemos/<demo-name>.md`

```markdown
---
entity_type: artifact
artifact_type: dbdemos-submission
status: built  # built → tested → submitted → published
demo_name: <demo-name>
category: <category>
industry: <HLS|FSI|MFG|RCG|general>
github_fork: github.com/<user>/dbdemos-notebooks
branch: demo/<demo-name>
local_path: ~/repos/dbdemos-notebooks/<category>/<demo-name>/
feip_ticket: null  # filled after JIRA creation
demo_review_doc: null  # filled after Google Doc creation
pr_url: null  # filled after PR submission
---

# dbdemos: <demo-name>

## Description
<short description of what the demo does>

## Notebooks
- `00-<name>.py` — Introduction
- `01-<name>.py` — <purpose>
- `02-<name>.py` — <purpose>
...

## Platform Features Demonstrated
- <feature 1>
- <feature 2>

## Repos Involved
- [x] dbdemos-notebooks (always)
- [ ] dbdemos-resources (images: yes/no)
- [ ] dbdemos-dataset (datasets: yes/no)

## JIRA Fields (pre-filled for ticket creation)
- **Project:** FEIP
- **Type:** Task
- **Summary:** dbdemos: <demo-name> — <short description>
- **Labels:** dbdemos
- **Industry ID:** <30410 for HLS, 30409 for FINS, 30412 for MFG, 30403 for RCG>
```

After writing, run `vault_reindex()`.

### Phase 10: Create FEIP JIRA Ticket (Optional — can run in a later session)

**Ask the user:** "Create FEIP ticket now, or later when the demo is tested?" Skip if they say later.

**If running in a later session**, read the vault atom at `Artifacts/dbdemos/<demo-name>.md` to get all fields.

**Project key is `FEIP`** (no hyphen). Use `fe-jira-tools:jira-ticket-assistant` agent via Task tool.

**Create a Task** (lightest issue type — only summary required):

```python
jira_write_api_call("issues.create", {
    "project": "FEIP",
    "issuetype": "Task",
    "summary": "dbdemos: <demo-name> — <short description>",
    "description": "Category: <category>\nWhat it demonstrates: <description>\nGitHub fork: github.com/<user>/dbdemos-notebooks\nBranch: demo/<demo-name>",
    "additional_fields": {
        "labels": ["dbdemos"],
        "customfield_18422": {"value": "fe-demos"}
    }
})
```

For HLS demos, add: `"customfield_19587": [{"id": "30410"}]` (Aligned Industry: HLS)

Other industry IDs: FINS=`30409`, MFG=`30412`, RCG=`30403`

**After creating**, update the vault atom frontmatter: `feip_ticket: FEIP-XXXX`

This is important for **PERF tracking** at year-end.

### Phase 11: Create Demo Review Document (Optional — can run in a later session)

Use `fe-google-tools:google-docs` to create a new Google Doc from the template structure.

Template source: https://docs.google.com/document/d/1idHpQKXPyjOqHbhSg1UDpmshiqOzDZT1cFiedsWXHKY/edit
Full template structure: see `references/demo-review-template.md`

**Pre-fill ALL fields possible** from the source project:

| Field | Source |
|-------|--------|
| Title | `<demo-name> - Q<quarter>, FY<year>` |
| Author(s) | User's name |
| Industry | From category selection |
| FEIP Ticket | Link from Phase 9 |
| Business Context | From README.md / DEMO.md of source project |
| Unique value prop | From DEMO.md architecture section |
| Bill of Materials | Inventory from Phase 1 (notebooks, app, datasets, images) |
| Business-line Story | From demo scripts if they exist (e.g., `docs/demo-scripts/`) |

**Only leave truly user-dependent fields** (Tech GM sign-off name, exact timeline dates, sync cadence).

### Phase 11b: Pre-PR Validation Checklist

**Run this before submitting.** dbdemos has NO automated CI — review is 100% manual by maintainers (Quentin Ambard, Cal Reynolds). Pre-empt their feedback.

**Structural checks:**
- [ ] `_resources/bundle_config.py` exists with all notebook entries
- [ ] `_resources/00-setup.py` uses `DBDemos.setup_schema()` via `%run ../../../_resources/00-global-setup-v2`
- [ ] `config.py` exists with `catalog = "main__build"` and appropriate schema/volume names
- [ ] Every notebook has `# Databricks notebook source` header
- [ ] Every notebook has analytics tracking pixel in first markdown cell
- [ ] Every notebook uses `# MAGIC %md` for markdown, `# COMMAND ----------` for separators

**Self-containment checks:**
- [ ] Zero references to external `.sql`, `.json`, `.yaml` files — all inlined
- [ ] Zero hardcoded catalog/schema names from source project (grep for them)
- [ ] Zero personal workspace URLs, instance names, or CLI profile names
- [ ] Widget defaults are generic: `""` for instance names, `"DEFAULT"` for profiles
- [ ] All `%run` paths are relative to the demo folder (e.g., `./config`, `../_resources/00-setup`)

**Functional checks:**
- [ ] `config.py` variables match what notebooks reference (`catalog`, `schema`/`db`, `volume_name`)
- [ ] `bundle_config.py` notebook paths match actual file names (no `.py` extension in paths)
- [ ] `pre_run: True` only on notebooks that can run without manual intervention
- [ ] `add_cluster_setup_cell: True` on all notebooks with executable code
- [ ] Setup notebook CDF/prerequisite steps run AFTER `DBDemos.setup_schema()`

**Content checks:**
- [ ] `fullDescription` in bundle_config uses HTML tags (`<br/>`, `<ul>`, `<li>`), not markdown
- [ ] `default_schema` follows `dbdemos_<short_slug>` convention
- [ ] Cluster spec uses a current LTS runtime version

### Phase 12: Submit PR

After all notebooks, images, and datasets are ported:

```bash
cd ~/repos/dbdemos-notebooks
git add demo-HLS/<demo-name>/
git commit -m "Add <demo-name> demo — <short description>"
git push origin demo/<demo-name>
gh pr create --title "Add <demo-name> HLS demo" --body "..."
```

Do the same for dbdemos-resources and dbdemos-dataset if applicable. **Ask user before pushing/creating PRs.**

### Phase 13: Checklist Output

Print what was done and what genuinely requires human judgment:

```markdown
## dbdemos Setup Complete

### Automated (done by skill)
- [x] Forked repos (notebooks + resources + dataset as needed)
- [x] Cloned locally, created feature branch
- [x] Scaffolded demo folder with dbdemos conventions
- [x] Created `_resources/bundle_config.py` with all notebook entries
- [x] Created `_resources/00-setup.py` using DBDemos.setup_schema() pattern
- [x] Ported and converted notebooks to dbdemos format (self-contained)
- [x] Inlined all external SQL/schema into notebooks
- [x] Cleaned widget defaults (no personal instance names)
- [x] Ported images to dbdemos-resources
- [x] Ported datasets to dbdemos-dataset
- [x] Wrote vault atom to `Artifacts/dbdemos/<demo-name>.md`
- [ ] Created FEIP JIRA ticket (run later: "create FEIP ticket for <demo-name>")
- [ ] Created Demo Review Document (run later: "create demo review doc for <demo-name>")
- [x] Ran pre-PR validation checklist (Phase 11b)
- [x] Submitted PRs to all repos

### Requires Human Judgment
- [ ] Get Tech GM sign-off on Demo Review Document
- [ ] Test `dbdemos.install('<demo-name>')` in a clean workspace with `reset_all_data=true`
- [ ] Respond to reviewer feedback on PR (Quentin Ambard / Cal Reynolds)
```

## Examples

### Example: Port existing project to dbdemos
User says: "cd ~/repos/hls-tech-demo && /dbdemos-setup"
Result: Reads the project, auto-derives demo name/category/description, forks repos, converts all notebooks, ports images and datasets, creates FEIP ticket, creates Demo Review Doc, submits PRs.

### Example: New demo from scratch
User says: "/dbdemos-setup"
Result: Asks for demo details, forks repos, scaffolds empty folder, creates FEIP ticket, creates Demo Review Doc. User builds notebooks from there.

### Example: Quick reference
User says: "What repos do I need to fork for dbdemos?"
Result: Shows the 4-repo table without running the full setup flow.
