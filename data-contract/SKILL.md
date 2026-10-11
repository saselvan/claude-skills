---
name: data-contract
description: "Generate DATA_CONTRACT.md for any project with a frontend+backend. Introspects Pydantic models, API routes, and DB schemas to produce the positive field list, then generates domain-specific negative list of fields AI will hallucinate. USE WHEN: user runs /data-contract, a project needs a data contract, or demo-factory Phase 4c.5 invokes it."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Data Contract Generator

Anti-hallucination firewall for AI code generators. Produces a tool-agnostic `DATA_CONTRACT.md` that prevents Cursor, Copilot, Claude Code, and Gemini from inventing plausible fields that don't exist in the backend.

## Trigger

Invoke when:
- User runs `/data-contract` or `/data-contract [project-path]`
- Demo-factory Phase 4c.5 calls this skill
- User asks to "document the API contract" or "prevent field hallucination"
- A project has a backend API and a frontend being built by AI

## Phase 1: Locate Project

Parse $ARGUMENTS for a project path. If empty, use the current working directory.

```
IF $ARGUMENTS contains a path:
  PROJECT_ROOT = resolve($ARGUMENTS path)
ELSE:
  PROJECT_ROOT = current working directory
```

Verify this is a project with backend code:

```bash
# Check for Python backend
ls $PROJECT_ROOT/app/server/ 2>/dev/null || \
ls $PROJECT_ROOT/backend/ 2>/dev/null || \
ls $PROJECT_ROOT/api/ 2>/dev/null || \
ls $PROJECT_ROOT/src/server/ 2>/dev/null || \
ls $PROJECT_ROOT/server/ 2>/dev/null
```

If no backend found, check for other patterns:
```bash
# FastAPI/Flask/Django
grep -rl "FastAPI\|Flask\|Django" $PROJECT_ROOT --include="*.py" -l | head -5
# Node.js/Express
grep -rl "express\|fastify\|hono" $PROJECT_ROOT --include="*.ts" --include="*.js" -l | head -5
```

Set `BACKEND_DIR` to whichever directory contains the backend code.
Set `BACKEND_LANG` to `python` or `node` based on what was found.

If no backend found at all, tell the user: "No backend code found at {PROJECT_ROOT}. DATA_CONTRACT.md requires a backend with API routes or data models."

## Phase 2: Introspect Backend Schema

### 2a. Extract Data Models (Positive List)

**Python (Pydantic/dataclass/SQLAlchemy):**

```bash
# Pydantic models
grep -rn "class.*BaseModel\|class.*BaseSchema" $BACKEND_DIR --include="*.py"

# SQLAlchemy/SQLModel
grep -rn "class.*Base\)\|class.*SQLModel" $BACKEND_DIR --include="*.py"

# Dataclasses
grep -rn "@dataclass" $BACKEND_DIR --include="*.py"

# TypedDict
grep -rn "class.*TypedDict" $BACKEND_DIR --include="*.py"
```

**Node.js (TypeScript interfaces/Zod/Prisma):**

```bash
# TypeScript interfaces and types
grep -rn "interface.*{$\|type.*=.*{" $BACKEND_DIR --include="*.ts"

# Zod schemas
grep -rn "z\.object\|z\.schema" $BACKEND_DIR --include="*.ts"

# Prisma models
cat $PROJECT_ROOT/prisma/schema.prisma 2>/dev/null
```

For each model found, read the file and extract:
- Model/class name
- Field names with types
- Optional/required status
- Source annotation (if present — e.g., mapped column name, API source)

### 2b. Extract API Routes

**Python (FastAPI/Flask):**

```bash
# FastAPI routes
grep -rn "@app\.\(get\|post\|put\|patch\|delete\)\|@router\.\(get\|post\|put\|patch\|delete\)" $BACKEND_DIR --include="*.py"
```

**Node.js (Express/Fastify):**

```bash
# Express routes
grep -rn "app\.\(get\|post\|put\|patch\|delete\)\|router\.\(get\|post\|put\|patch\|delete\)" $BACKEND_DIR --include="*.ts" --include="*.js"
```

For each route, identify:
- HTTP method and path
- Response model (if typed)
- What data it returns

### 2c. Extract Database Schema (if available)

```bash
# SQL DDL files
find $PROJECT_ROOT -name "*.sql" -path "*/migrations/*" -o -name "*.sql" -path "*/ddl/*" -o -name "schema.sql" | head -10

# Alembic migrations
ls $PROJECT_ROOT/alembic/versions/ 2>/dev/null

# Prisma schema
cat $PROJECT_ROOT/prisma/schema.prisma 2>/dev/null
```

## Phase 3: Generate Negative List

Based on the project's domain, generate a list of fields that AI code generators will plausibly hallucinate but that DO NOT exist in the actual schema.

### Domain Detection

```
READ $PROJECT_ROOT for domain signals:
- File/folder names containing: health, patient, clinical, medical → HLS
- File/folder names containing: finance, bank, trade, portfolio → FSI
- File/folder names containing: retail, product, cart, order → RETAIL
- File/folder names containing: iot, sensor, device, telemetry → IOT
- README.md or spec mentioning industry keywords → detected domain
- If unclear → GENERAL
```

### Domain-Specific Hallucination Targets

**HLS (Healthcare & Life Sciences):**
`patient_id`, `mrn`, `dob`, `age`, `gender`, `ethnicity`, `insurance_id`, `insurance_provider`, `clinical_notes`, `diagnosis_code`, `icd10_code`, `icd9_code`, `cpt_code`, `drg`, `provider_npi`, `attending_physician`, `lab_results`, `vitals`, `blood_pressure`, `heart_rate`, `medications`, `allergies`, `immunizations`, `family_history`, `staging_info`, `biomarkers`, `staining_method`, `laterality`, `grade`, `tnm_stage`, `specimen_type`, `accession_number`, `pathology_report`

**FSI (Financial Services):**
`ssn`, `account_balance`, `credit_score`, `fico_score`, `routing_number`, `account_number`, `tax_id`, `portfolio_value`, `risk_score`, `credit_limit`, `apr`, `payment_history`, `delinquency_count`, `debt_to_income`, `annual_income`, `employment_status`, `kyc_status`, `aml_flag`, `sanctions_match`

**Retail/E-Commerce:**
`purchase_history`, `loyalty_points`, `cart_abandonment_rate`, `lifetime_value`, `customer_segment`, `churn_probability`, `nps_score`, `referral_code`, `subscription_tier`, `return_rate`, `average_order_value`, `session_duration`, `click_through_rate`

**IoT/Manufacturing:**
`device_firmware`, `calibration_date`, `maintenance_schedule`, `mtbf`, `failure_mode`, `operating_temperature`, `power_consumption`, `signal_strength`, `battery_level`, `geofence_status`, `anomaly_score`

**General (always include):**
`created_by`, `updated_at`, `deleted_at`, `version`, `audit_trail`, `permissions`, `tenant_id`, `api_key`, `access_level`, `last_login`, `ip_address`, `user_agent`, `session_token`

### Filter Step

Compare the hallucination targets against the ACTUAL schema extracted in Phase 2. Remove any field that actually exists. Only keep fields that are plausible but absent.

## Phase 4: Generate Interpretation Rules

Scan the actual fields for patterns that need interpretation guardrails:

| Pattern | Rule |
|---------|------|
| `score`, `similarity`, `confidence` | "This is a {algorithm} score, not a calibrated probability. Display as numeric or qualitative tier, never as X% match." |
| `label`, `class`, `category`, `type` | "Derived from {source} labels, not authoritative classification. Include disclaimer when displaying." |
| `embedding`, `vector` | "Internal representation, not human-readable. Never display raw values." |
| `prediction`, `forecast` | "Model output with uncertainty. Always display confidence interval or caveat." |
| Domain-specific labels (e.g., tissue types, risk categories) | "Dataset-derived, not clinical/regulatory evaluation. Never use authoritative language." |

Also check for:
- **Institutional attribution**: Does the data come from a named dataset? Add rule: "Data is from {dataset}, not from {institution}. Do not attribute to {institution}."
- **Score semantics**: Is there a cosine similarity, confidence, or probability field? Add rule clarifying what it means and what it doesn't.

## Phase 5: Assemble Contract

### 5a. Build DATA_CONTRACT.md

```markdown
# Data Contract: What the Backend Actually Sends

> **Purpose:** Every UI field must trace back to a real backend field. If the backend doesn't send it, the UI must not render it. This contract is the single source of truth for all AI code generators (Cursor, Copilot, Claude Code, Gemini) working on this project's frontend.

## Ground Truth

{For each endpoint/model, document exact fields}

### {ModelName} (from `{route}`)

| Field | Type | Description |
|-------|------|-------------|
| {name} | {type} | {source/meaning} |

{Repeat for each endpoint/model}

## Fields That Do NOT Exist

These fields are plausible for this domain but are NOT in our data. Never render UI for them, never add them to TypeScript types, never write fallbacks for them:

`{comma-separated list of filtered hallucination targets}`

If a future version adds any of these fields, update this contract FIRST, then update the UI.

## Interpretation Rules

{Generated rules from Phase 4}

## Maintenance

- **When to update:** After any backend schema change (new model, new field, new endpoint)
- **Who updates:** The developer who changes the backend schema
- **Validation:** Before any frontend PR, diff field references against this contract
- **AI generators:** When using Cursor/Copilot/Claude to generate frontend code, ensure this file is in the AI's context window
```

### 5b. Build .cursor/rules/data-contract.mdc

Same content as DATA_CONTRACT.md, but with Cursor frontmatter:

```markdown
---
description: Enforces frontend-backend data contract. Apply when editing any frontend component that renders API data.
globs:
  - {frontend glob patterns based on project structure}
---

{Same content as DATA_CONTRACT.md}
```

Detect frontend glob patterns:
```bash
# React/Next.js
ls $PROJECT_ROOT/app/frontend/src/ 2>/dev/null && echo "apps/frontend/src/**/*.tsx apps/frontend/src/**/*.ts"
ls $PROJECT_ROOT/frontend/src/ 2>/dev/null && echo "frontend/src/**/*.tsx frontend/src/**/*.ts"
ls $PROJECT_ROOT/src/components/ 2>/dev/null && echo "src/**/*.tsx src/**/*.ts"
# Vue
ls $PROJECT_ROOT/src/components/ 2>/dev/null && echo "src/**/*.vue"
```

## Phase 6: User Review Gate

Present the contract to the user with emphasis on the negative list:

```
DATA CONTRACT GENERATED
=======================
Project: {PROJECT_ROOT}
Backend: {BACKEND_LANG} ({framework detected})
Domain: {detected domain}

Positive fields: {count} fields across {count} endpoints/models
Negative fields: {count} hallucination targets filtered for this project
Interpretation rules: {count}

Files written:
  - {PROJECT_ROOT}/DATA_CONTRACT.md
  - {PROJECT_ROOT}/.cursor/rules/data-contract.mdc

REVIEW THE NEGATIVE LIST:
{Display the negative list}

Are these correct? Should any be added or removed?
```

Use AskUserQuestion to confirm:
- "Review the negative list (fields AI should NOT generate). Any to add or remove?"

After user confirms, the contract is final.

## Output

Final output after user review:

```
DATA CONTRACT COMPLETE
======================
Project: {PROJECT_ROOT}
Files:
  - DATA_CONTRACT.md (canonical, tool-agnostic)
  - .cursor/rules/data-contract.mdc (Cursor auto-apply)

Coverage:
  - {N} endpoints documented
  - {N} positive fields
  - {N} negative fields (anti-hallucination)
  - {N} interpretation rules

The contract is now active. Any AI code generator with access to
this project will see the contract and respect field boundaries.
```

## Examples

### Example: Existing Python/FastAPI project
```
User: /data-contract /Users/samuel.selvan/projects/hls-pathology-dual-corpus
```
Introspects `app/server/`, finds Pydantic models for RetrievalResult, detects HLS domain, generates negative list with `patient_id`, `clinical_notes`, etc., writes DATA_CONTRACT.md and .cursor/rules/data-contract.mdc.

### Example: Current directory
```
User: /data-contract
```
Uses cwd, introspects backend, generates contract.

### Example: Called by demo-factory
```
Demo-factory Phase 4c.5 invokes this skill after scaffolding the app.
Reads board context for domain detection. Writes board entry to
board/data-contract-output.yaml in addition to the standard outputs.
```
