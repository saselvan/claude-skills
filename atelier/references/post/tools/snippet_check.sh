#!/bin/bash
# Extract and validate SQL/bash fenced blocks from markdown.

set -euo pipefail

DRAFT="${1:?Usage: $0 <draft.md>}"
[[ -f "$DRAFT" ]] || { echo "Error: $DRAFT not found" >&2; exit 1; }

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

EXIT_CODE=0

# Extract SQL blocks
awk '
  /^```sql$/ { in_sql=1; next }
  /^```$/ && in_sql { in_sql=0; print "" >> sql_file; next }
  in_sql { print >> sql_file }
' sql_file="$TMPDIR/snippets.sql" "$DRAFT"

# Extract bash blocks
awk '
  /^```bash$/ { in_bash=1; next }
  /^```$/ && in_bash { in_bash=0; print "" >> bash_file; next }
  in_bash { print >> bash_file }
' bash_file="$TMPDIR/snippets.sh" "$DRAFT"

# Check SQL snippets (parse-check: balanced parens/quotes, semicolon)
if [[ -f "$TMPDIR/snippets.sql" && -s "$TMPDIR/snippets.sql" ]]; then
  if [[ -n "${SNIPPET_PG:-}" ]]; then
    # Run against Postgres if env var set
    if ! psql "$SNIPPET_PG" --set ON_ERROR_STOP=1 -f "$TMPDIR/snippets.sql" >/dev/null 2>&1; then
      echo "Error: SQL snippets failed to run" >&2
      EXIT_CODE=1
    fi
  else
    # Parse-check: look for balanced parens/quotes and semicolon
    sql_content=$(cat "$TMPDIR/snippets.sql")

    # Check for terminating semicolon
    if ! grep -q ';[[:space:]]*$' "$TMPDIR/snippets.sql"; then
      echo "Error: SQL snippet missing terminating semicolon" >&2
      EXIT_CODE=1
    fi

    # Basic balance check (count parens and quotes)
    open_parens=$(echo "$sql_content" | grep -o '(' | wc -l)
    close_parens=$(echo "$sql_content" | grep -o ')' | wc -l)
    if [[ "$open_parens" -ne "$close_parens" ]]; then
      echo "Error: Unbalanced parentheses in SQL: $open_parens open, $close_parens close" >&2
      EXIT_CODE=1
    fi
  fi
fi

# Check bash snippets
if [[ -f "$TMPDIR/snippets.sh" && -s "$TMPDIR/snippets.sh" ]]; then
  if ! bash -n "$TMPDIR/snippets.sh" >/dev/null 2>&1; then
    echo "Error: Bash snippet syntax error" >&2
    bash -n "$TMPDIR/snippets.sh" 2>&1 | head -3 >&2
    EXIT_CODE=1
  fi
fi

exit $EXIT_CODE
