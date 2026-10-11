---
name: genie-space
description: Create, update, export, and manage Databricks AI/BI Genie Spaces programmatically via REST API
---

# Genie Space Management Skill

Create, update, export, and manage Databricks Genie Spaces using the REST API.

## Usage

```
/genie-space export <space_id>         — Export space config to YAML
/genie-space patch <space_id> <file>   — Apply config from YAML to space
/genie-space create <file>             — Create new space from YAML
/genie-space diff <space_id> <file>    — Show what would change
/genie-space validate <file>           — Validate config without sending
```

## Prerequisites

- Databricks CLI configured with a profile that has workspace access
- Profile name passed as `--profile <name>` or defaulting to `logfood`
- SQL warehouse ID (required for create, already set on existing spaces)

## serialized_space Schema (v2)

This is the COMPLETE, AUTHORITATIVE schema for `serialized_space`. Every field name, type, and constraint is documented below. This schema was reverse-engineered from the live API + official docs as of 2026-05-22.

### Root Structure

```json
{
  "version": 2,
  "config": { ... },
  "data_sources": { ... },
  "instructions": { ... },
  "benchmarks": { ... }
}
```

### ID Format

ALL items require a 32-character lowercase hexadecimal ID (UUID without hyphens).

```python
import uuid
def genie_id():
    return uuid.uuid4().hex  # e.g. "a1b2c3d4e5f6000000000000000000a0"
```

IDs must be unique across ALL collections (sample_questions + benchmarks share a namespace).

### Sorting Requirements

ALL collections must be sorted alphabetically:
- `tables` by `identifier`
- `column_configs` by `column_name`
- `sample_questions` by `id`
- `text_instructions` by `id`
- `example_question_sqls` by `id`
- `join_specs` by `id`
- `sql_snippets.filters` by `id`
- `sql_snippets.expressions` by `id`
- `sql_snippets.measures` by `id`
- `benchmarks.questions` by `id`

### config

```json
{
  "sample_questions": [
    {
      "id": "32-char-hex",
      "question": ["What were total sales last month?"]
    }
  ]
}
```

- `question`: Array of strings (typically single element)

### data_sources

```json
{
  "tables": [
    {
      "identifier": "catalog.schema.table_name",
      "description": ["Human-readable table description"],
      "column_configs": [
        {
          "column_name": "col_name",
          "description": ["Column description"],
          "synonyms": ["alt_name_1", "alt_name_2"],
          "enable_entity_matching": true,
          "enable_format_assistance": true,
          "exclude": false
        }
      ]
    }
  ],
  "metric_views": [
    {
      "identifier": "catalog.schema.metric_view",
      "description": ["Description"],
      "column_configs": []
    }
  ]
}
```

**Key rules:**
- `identifier`: Three-level namespace `catalog.schema.table` (NOT just table name)
- `description`: Array of strings (NOT a plain string)
- `column_configs`: Sorted alphabetically by `column_name`
- `tables`: Sorted alphabetically by `identifier`
- `(identifier, column_name)` pairs must be unique
- `exclude: true` hides column from Genie

### instructions

#### text_instructions

```json
{
  "text_instructions": [
    {
      "id": "32-char-hex",
      "content": [
        "Line 1 of instructions.",
        "Line 2 of instructions."
      ]
    }
  ]
}
```

**CONSTRAINT: Maximum 1 text_instruction per space.**
- `content`: Array of strings. Each string is a paragraph/section.
- Max 25,000 characters per string element.

#### example_question_sqls (certified queries)

```json
{
  "example_question_sqls": [
    {
      "id": "32-char-hex",
      "question": ["Show top 10 customers by revenue"],
      "sql": [
        "SELECT customer_name, SUM(amount) as total\n",
        "FROM catalog.schema.orders\n",
        "GROUP BY customer_name\n",
        "ORDER BY total DESC LIMIT 10"
      ],
      "parameters": [
        {
          "name": "region",
          "type_hint": "STRING",
          "description": ["Filter by region"],
          "default_value": {"values": ["North America"]}
        }
      ],
      "usage_guidance": ["Use when user asks about top customers"]
    }
  ]
}
```

- `question`: Array of strings. Multiple strings = multiple phrasings of the same question.
- `sql`: Array of strings joined to form the full SQL.
- `parameters`: Optional. For parameterized queries.
- `usage_guidance`: Optional. Tells Genie when to use this query.

#### join_specs

```json
{
  "join_specs": [
    {
      "id": "32-char-hex",
      "left": {
        "identifier": "catalog.schema.left_table",
        "alias": "lt"
      },
      "right": {
        "identifier": "catalog.schema.right_table",
        "alias": "rt"
      },
      "sql": [
        "`lt`.`join_col` = `rt`.`join_col`",
        "--rt=FROM_RELATIONSHIP_TYPE_MANY_TO_ONE--"
      ],
      "comment": ["Join description"],
      "instruction": ["When to use this join"]
    }
  ]
}
```

**CRITICAL:**
- `sql` must have EXACTLY 2 elements:
  1. Join condition using backtick-quoted aliases
  2. Cardinality annotation: `--rt=FROM_RELATIONSHIP_TYPE_<TYPE>--`
- Valid types: `MANY_TO_ONE`, `ONE_TO_MANY`, `ONE_TO_ONE`, `MANY_TO_MANY`
- Aliases are short (2-3 chars), referenced in the join condition

#### sql_snippets

```json
{
  "sql_snippets": {
    "filters": [
      {
        "id": "32-char-hex",
        "sql": ["health_status = 'RED'"],
        "display_name": "RED accounts",
        "synonyms": ["at risk", "unhealthy"],
        "comment": ["Filter to RED health accounts"],
        "instruction": ["Use when asked about at-risk accounts"]
      }
    ],
    "expressions": [
      {
        "id": "32-char-hex",
        "alias": "spend_bucket",
        "sql": ["CASE WHEN spend > 1000 THEN 'High' ELSE 'Low' END"],
        "display_name": "Spend bucket",
        "synonyms": ["spend tier"],
        "comment": ["Categorize by spend level"],
        "instruction": ["Use for spend segmentation"]
      }
    ],
    "measures": [
      {
        "id": "32-char-hex",
        "alias": "total_spend",
        "sql": ["SUM(spend_recent_30d)"],
        "display_name": "Total recent spend",
        "synonyms": ["total spend", "aggregate spend"],
        "comment": ["Sum of 30-day spend"],
        "instruction": ["Use for total spend calculations"]
      }
    ]
  }
}
```

**Key differences from filters:**
- Expressions and measures have `alias` (required) — the output column name
- Filters do NOT have `alias`
- All three: `sql` is an array of strings, `display_name` is a string (not `name`)
- `synonyms`, `comment`, `instruction` are arrays of strings
- Filter `sql` does NOT need table prefixes if the column is unambiguous. If ambiguous across tables, prefix with table name (e.g., `vw_account_health.health_status`)

### benchmarks

```json
{
  "benchmarks": {
    "questions": [
      {
        "id": "32-char-hex",
        "question": ["What is the average health score?"],
        "answer": [
          {
            "format": "SQL",
            "content": [
              "SELECT AVG(health_score)\n",
              "FROM catalog.schema.vw_account_health"
            ]
          }
        ]
      }
    ]
  }
}
```

- Each benchmark has exactly 1 answer with `format: "SQL"`
- `content`: Array of strings joined to form SQL
- Benchmark IDs share namespace with sample_question IDs (must be globally unique)

## Implementation

### Step 1: Parse Arguments

Detect subcommand: `export`, `patch`, `create`, `diff`, `validate`

### Step 2: Auth

```python
import subprocess, json

def get_token(profile="logfood"):
    result = subprocess.run(
        ["databricks", "auth", "token", "--profile", profile],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)["access_token"]
```

### Step 3: Export (GET)

```python
GET /api/2.0/genie/spaces/{space_id}?include_serialized_space=true
```

**CRITICAL**: Must pass `include_serialized_space=true` query param, otherwise serialized_space is NOT returned.

Parse `serialized_space` (it's a JSON string), convert to YAML for human editing, write to file.

### Step 4: Patch/Update (PATCH)

```python
PATCH /api/2.0/genie/spaces/{space_id}
Content-Type: application/json

{
  "serialized_space": "<JSON string of the full serialized_space object>"
}
```

The `serialized_space` value is a JSON **string** (double-encoded). The outer request body is JSON containing a `serialized_space` key whose value is a JSON string.

Before sending:
1. Validate all IDs are 32-char hex
2. Sort all collections alphabetically
3. Validate join_spec sql arrays have exactly 2 elements
4. Validate at most 1 text_instruction

### Step 5: Create (POST)

```python
POST /api/2.0/genie/spaces
Content-Type: application/json

{
  "title": "Space Title",
  "description": "Space description",
  "warehouse_id": "abc123",
  "parent_path": "/Users/user@databricks.com/path",
  "serialized_space": "<JSON string>"
}
```

### Step 6: Diff

GET current space, parse both configs, show structural diff (added/removed/changed items).

## YAML Config Format

For human authoring, use YAML. The skill converts to the API JSON format:

```yaml
# genie-space.yaml
space:
  title: "My Genie Space"
  description: "Description"
  warehouse_id: "927ac096f9833442"
  host: "adb-xxx.azuredatabricks.net"
  profile: "logfood"
  catalog: "my_catalog"
  schema: "my_schema"

instructions: |
  You are a helpful assistant.
  Answer concisely.

sample_questions:
  - "Which accounts need attention?"
  - "Show me pipeline by quadrant"

tables:
  - name: vw_my_table
    description: "Table description"
    columns:
      col_name:
        description: "Column description"
        synonyms: ["alt1", "alt2"]
        entity_matching: true
        format_assistance: true
      hidden_col:
        exclude: true

joins:
  - left: vw_left_table (lt)
    right: vw_right_table (rt)
    on: "`lt`.`col` = `rt`.`col`"
    cardinality: ONE_TO_MANY
    comment: "Join description"

filters:
  - name: "RED accounts"
    sql: "health_status = 'RED'"
    synonyms: ["at risk", "unhealthy"]
    comment: "Filter to RED health"

expressions:
  - name: "Spend bucket"
    alias: spend_bucket
    sql: "CASE WHEN spend > 1000 THEN 'High' ELSE 'Low' END"
    synonyms: ["spend tier"]

measures:
  - name: "Total spend"
    alias: total_spend
    sql: "SUM(spend_recent_30d)"
    synonyms: ["aggregate spend"]

certified_queries:
  - question: "Show top accounts"
    sql: |
      SELECT account_name, health_score
      FROM {table:vw_my_table}
      ORDER BY health_score ASC
    guidance: "Use for account ranking"

benchmarks:
  - question: "How many RED accounts?"
    sql: |
      SELECT COUNT(*)
      FROM {table:vw_my_table}
      WHERE health_status = 'RED'
```

### YAML-to-API Conversion Rules

1. **Auto-generate IDs**: Generate 32-char hex UUIDs for all items. On update, preserve existing IDs for unchanged items (match by question text or display_name).
2. **Auto-sort**: Sort all collections by ID after generation.
3. **`{table:name}`**: Expands to `catalog.schema.name` using the config's catalog/schema.
4. **Instructions**: Single string in YAML -> wrapped in `[{"id": "...", "content": ["line1", "line2", ...]}]` (split by double newline or explicit `---` separator).
5. **Descriptions**: Plain strings in YAML -> wrapped in arrays for API.
6. **Column configs**: Nested under table name, keyed by column name. Converted to sorted array.

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find field: text` | Used `text` instead of `text_instructions` in instructions | Use `text_instructions` array format |
| `Cannot find field: table_name` | Used `table_name` instead of `identifier` in data_sources | Use `identifier` with full 3-level namespace |
| `Invalid JSON in serialized_space` | Wrong field names or structure | Validate against this schema |
| `Table name or alias required for column` | Ambiguous column in filter sql | Prefix with table name in filter sql |
| `ID must be 32-char hex` | ID too short, has hyphens, or uppercase | Use `uuid.uuid4().hex` |

## Anti-Patterns (Hard-Learned)

1. **`"text"` is NOT a valid field** in instructions. The field is `text_instructions` (array of objects with `id` + `content`).
2. **`"table_name"` is NOT a valid field** in data_sources. The field is `identifier` (full `catalog.schema.table`).
3. **`"entity_matching"` is NOT a valid field**. Use `enable_entity_matching`.
4. **Descriptions are arrays**, not strings. `"description": "foo"` fails; use `"description": ["foo"]`.
5. **sql_snippets is an OBJECT** with keys `filters`, `expressions`, `measures` -- NOT a flat array.
6. **Filters use `display_name`** and `sql` (array) -- NOT `name` and `expression` (string).
7. **join_specs sql needs exactly 2 elements**: condition + `--rt=FROM_RELATIONSHIP_TYPE_*--`
8. **`include_serialized_space=true`** is required on GET -- otherwise the config isn't returned.
9. **benchmarks is `{"questions": [...]}`** -- NOT a flat array.
10. **All string fields that look like they should be strings are actually arrays of strings** (description, content, question, sql, comment, instruction, synonyms).
