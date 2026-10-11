#!/usr/bin/env python3
"""
Oracle harness — a runnable grader skeleton for a verification-ladder loop.

Why this exists: a grader described in prose gets re-invented (differently)
every loop, and a grader that shares code with the thing it grades is not a
grader. This gives you a black-box harness in one file: it drives the RUNNING
system, compares against hand-authored expected values, AND independently
recomputes the invariants — two derivations of "correct", so a mis-authored
expectation still cannot hide a real defect.

The pattern (adapt the checks; keep the shape):
  1. fixtures/  — hand-authored inputs (never generated from the system)
  2. expected/  — hand-authored expected outputs (never generated from the
                  system; if you regenerate them from the code, you have a
                  change-detector, not an oracle)
  3. checks     — byte/value equality AND semantic invariants recomputed from
                  the fixture (e.g. row-count conservation, no-silent-drop)
  4. verdict    — PASS/FAIL per case with evidence, written to disk

Prove it discriminates before you trust it: run it against a deliberately
broken implementation (re-introduce the bug the loop exists to prevent) and
confirm it goes RED. A harness that has never failed is not evidence.

Usage:
    python oracle_harness.py --base-url http://localhost:8000 \
        --cases cases.json --out verdict.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.request


def fetch(url: str, timeout: float = 30.0) -> tuple[int, dict[str, str], bytes]:
    """Black-box call into the running system. Never import the app."""
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers or {}), exc.read()


def check_case(case: dict, base_url: str) -> dict:
    """Run one case. Returns a verdict dict with per-check evidence.

    A case looks like:
      {"name": "null_owner",
       "path": "/api/metrics/export.csv",
       "fixture": "fixtures/null_owner.json",
       "expected": "expected/null_owner.csv",
       "invariants": {"row_count_conservation": true,
                      "preserve_null_field": "owner_principal"}}
    """
    checks: list[dict] = []
    status, headers, body = fetch(base_url.rstrip("/") + case["path"])

    checks.append({
        "id": "reachable",
        "passed": status == 200,
        "evidence": f"HTTP {status}",
    })

    # Derivation 1 — hand-authored expected output, byte-exact.
    expected_path = case.get("expected")
    if expected_path and status == 200:
        expected = pathlib.Path(expected_path).read_bytes()
        checks.append({
            "id": "matches_hand_authored_expected",
            "passed": body == expected,
            "evidence": (
                "byte-exact match"
                if body == expected
                else f"got {len(body)}B, expected {len(expected)}B"
            ),
        })

    # Derivation 2 — invariants recomputed from the FIXTURE, independent of
    # the expected file. This is what catches a mis-authored expectation.
    fixture_path = case.get("fixture")
    inv = case.get("invariants") or {}
    if fixture_path and status == 200:
        rows = json.loads(pathlib.Path(fixture_path).read_text())
        lines = [ln for ln in body.decode().splitlines() if ln.strip()]
        data_rows = lines[1:]  # drop header

        if inv.get("row_count_conservation"):
            checks.append({
                "id": "row_count_conservation",
                "passed": len(data_rows) == len(rows),
                "evidence": f"output {len(data_rows)} rows, source {len(rows)} rows",
            })

        field = inv.get("preserve_null_field")
        if field:
            # The canonical silent-drop bug: rows with a null field vanish.
            want = sum(1 for r in rows if r.get(field) in (None, "", "null"))
            # Count output rows whose field position is empty — adapt the
            # parse to your format; the point is to count, not to eyeball.
            got = sum(1 for ln in data_rows if ",," in ln or ln.rstrip().endswith(","))
            checks.append({
                "id": f"preserve_null_{field}",
                "passed": got >= want,
                "evidence": f"null-{field} rows: output {got}, source {want}",
            })

    return {
        "case": case["name"],
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="running system, e.g. http://localhost:8000")
    ap.add_argument("--cases", required=True, help="JSON list of cases")
    ap.add_argument("--out", default="verdict.json")
    args = ap.parse_args()

    cases = json.loads(pathlib.Path(args.cases).read_text())
    results = [check_case(c, args.base_url) for c in cases]
    passed = sum(r["passed"] for r in results)
    verdict = {
        "verdict": "PASS" if passed == len(results) else "FAIL",
        "passed": passed,
        "total": len(results),
        "cases": results,
    }
    pathlib.Path(args.out).write_text(json.dumps(verdict, indent=2) + "\n")

    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"[{mark}] {r['case']}")
        for c in r["checks"]:
            if not c["passed"]:
                print(f"        {c['id']}: {c['evidence']}")
    print(f"\n{verdict['verdict']} {passed}/{len(results)} — wrote {args.out}")
    return 0 if verdict["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
