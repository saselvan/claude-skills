#!/usr/bin/env python3
"""
Logfood Query Helper — queries consumption data with polling support.

Usage:
    python3 query_logfood.py --account-id 0016100000cF3SpAAK --account-name "Northwestern Medicine" --output-dir /tmp

Produces three files in output-dir:
    {prefix}_weekly.json
    {prefix}_sku.json
    {prefix}_workspace.json
"""

import argparse
import json
import os
import subprocess
import sys
import time

# Known account IDs — add new accounts here
ACCOUNT_IDS = {
    "Northwestern Medicine": "0016100000cF3SpAAK",
    "NWM": "0016100000cF3SpAAK",
    "Community Health Network": "0014N00001g7tAnQAI",
    "CHN": "0014N00001g7tAnQAI",
}

WAREHOUSE_ID = "927ac096f9833442"  # Shared SQL Endpoint - Stable
PROFILE = "logfood"
POLL_INTERVAL = 10  # seconds
MAX_POLLS = 15  # 150 seconds max wait


def load_sql(query_name: str, account_id: str, weeks: int = 52) -> str:
    """Load SQL template and substitute parameters."""
    query_dir = os.path.join(os.path.dirname(__file__), "queries")
    sql_path = os.path.join(query_dir, f"{query_name}.sql")

    with open(sql_path) as f:
        sql = f.read()

    sql = sql.replace(":account_id", f"'{account_id}'")
    sql = sql.replace(":weeks", str(weeks))
    return sql


def execute_query(sql: str) -> list:
    """Execute SQL via Databricks SQL Statement API with polling."""
    payload = {
        "warehouse_id": WAREHOUSE_ID,
        "statement": sql,
        "wait_timeout": "30s",
        "format": "JSON_ARRAY",
    }

    result = subprocess.run(
        ["databricks", "api", "post", "/api/2.0/sql/statements/",
         "--profile", PROFILE, "--json", json.dumps(payload)],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"ERROR: API call failed: {result.stderr}", file=sys.stderr)
        return None

    response = json.loads(result.stdout)
    status = response.get("status", {}).get("state", "UNKNOWN")

    # Poll if PENDING
    if status == "PENDING":
        stmt_id = response["statement_id"]
        print(f"  Query PENDING (id: {stmt_id}), polling...", file=sys.stderr)

        for i in range(MAX_POLLS):
            time.sleep(POLL_INTERVAL)
            poll_result = subprocess.run(
                ["databricks", "api", "get", f"/api/2.0/sql/statements/{stmt_id}",
                 "--profile", PROFILE],
                capture_output=True, text=True
            )

            if poll_result.returncode != 0:
                print(f"  Poll {i+1} failed: {poll_result.stderr}", file=sys.stderr)
                continue

            response = json.loads(poll_result.stdout)
            status = response.get("status", {}).get("state", "UNKNOWN")
            print(f"  Poll {i+1}/{MAX_POLLS}: {status}", file=sys.stderr)

            if status == "SUCCEEDED":
                break
            elif status == "FAILED":
                error = response.get("status", {}).get("error", {})
                print(f"  Query FAILED: {error}", file=sys.stderr)
                return None

    if status != "SUCCEEDED":
        print(f"ERROR: Query did not succeed. Final status: {status}", file=sys.stderr)
        return None

    # Extract data
    data = response.get("result", {}).get("data_array")
    columns = [c["name"] for c in response.get("manifest", {}).get("schema", {}).get("columns", [])]

    if data is None:
        print("ERROR: No data_array in response", file=sys.stderr)
        return None

    # Convert to list of dicts
    rows = [dict(zip(columns, row)) for row in data]
    return rows


def main():
    parser = argparse.ArgumentParser(description="Query Logfood for consumption data")
    parser.add_argument("--account-id", help="SFDC account ID (or use --account-name)")
    parser.add_argument("--account-name", help="Account name (looks up ID from known accounts)")
    parser.add_argument("--weeks", type=int, default=52, help="Number of weeks to query")
    parser.add_argument("--output-dir", default="/tmp", help="Directory for output JSON files")
    parser.add_argument("--prefix", help="Output file prefix (default: derived from account name)")
    args = parser.parse_args()

    # Resolve account ID
    account_id = args.account_id
    account_name = args.account_name

    if not account_id and account_name:
        account_id = ACCOUNT_IDS.get(account_name)
        if not account_id:
            print(f"ERROR: Unknown account '{account_name}'. Known: {list(ACCOUNT_IDS.keys())}", file=sys.stderr)
            sys.exit(1)
    elif not account_id:
        print("ERROR: Provide --account-id or --account-name", file=sys.stderr)
        sys.exit(1)

    # Derive prefix
    prefix = args.prefix
    if not prefix:
        if account_name:
            prefix = account_name.lower().replace(" ", "_")[:3]
        else:
            prefix = account_id[:8]

    queries = ["weekly_totals", "sku_breakdown", "workspace_attribution"]
    suffixes = ["weekly", "sku", "workspace"]

    print(f"Querying Logfood for {account_name or account_id} ({args.weeks} weeks)...", file=sys.stderr)

    for query_name, suffix in zip(queries, suffixes):
        output_path = os.path.join(args.output_dir, f"{prefix}_{suffix}.json")
        print(f"\n--- {query_name} ---", file=sys.stderr)

        sql = load_sql(query_name, account_id, args.weeks)
        rows = execute_query(sql)

        if rows is None:
            print(f"  FAILED — retrying once...", file=sys.stderr)
            time.sleep(5)
            rows = execute_query(sql)

        if rows is None:
            print(f"  FAILED on retry. Skipping {query_name}.", file=sys.stderr)
            continue

        with open(output_path, "w") as f:
            json.dump(rows, f, indent=2)

        print(f"  OK: {len(rows)} rows → {output_path}", file=sys.stderr)

    print(f"\nDone. Files in {args.output_dir}/{prefix}_*.json", file=sys.stderr)


if __name__ == "__main__":
    main()
