#!/usr/bin/env python3
"""Validate claim tags [C#] in draft against CATECHISM.md inventory."""

import sys
import re
from pathlib import Path

def load_catechism(catechism_path):
    """Parse CATECHISM.md claims table; return dict {claim_id: {grade, file, date}}."""
    claims = {}
    with open(catechism_path) as f:
        in_table = False
        for line in f:
            if line.strip().startswith("| # |"):
                in_table = True
                continue
            if in_table and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 6 and parts[1].startswith("C"):
                    try:
                        claim_id = parts[1]
                        # parts[2] = claim text, parts[3] = evidence, parts[4] = grade
                        grade = parts[4].strip()
                        if grade:
                            claims[claim_id] = {"grade": grade}
                    except Exception:
                        pass
    return claims

def check_draft(draft_path, claims):
    """Check that all [C#] tags in draft exist and are graded; flag untagged numbers."""
    errors = []

    with open(draft_path) as f:
        lines = f.readlines()

    # Find all claim tags
    claim_pattern = re.compile(r'\[C(\d+)\]')

    for line_num, line in enumerate(lines, 1):
        # Check all [C#] tags
        for match in claim_pattern.finditer(line):
            claim_id = f"C{match.group(1)}"
            if claim_id not in claims:
                errors.append(f"Line {line_num}: Unknown claim tag [{claim_id}]")
            else:
                grade = claims[claim_id].get("grade", "").strip()
                if grade in ("UNPROVEN", ""):
                    errors.append(f"Line {line_num}: Claim {claim_id} is ungraded (grade: {grade})")

        # Flag numbers without a nearby claim tag (check same sentence)
        # Extract sentences and check each
        sentences = re.split(r'(?<=[.!?])\s+', line)
        for sent in sentences:
            # Look for numbers that don't have a claim tag
            numbers = re.findall(r'(?<!\[C)\b\d+(?:\.\d+)?\s*(?:ms|%|s|req/s|CU)?\b(?!\])', sent)
            if numbers and not claim_pattern.search(sent):
                # Flag this line as having untagged numbers
                # Only flag if there's a concrete metric (ms, %, etc.)
                metric_pattern = re.search(r'\d+(?:\.\d+)?\s*(?:ms|%|s|req/s|/s|CU|requests)', sent)
                if metric_pattern:
                    errors.append(f"Line {line_num}: Number '{metric_pattern.group()}' has no claim tag in sentence: {sent[:60]}...")

    return errors

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <draft.md>")
        sys.exit(1)

    draft_path = Path(sys.argv[1]).resolve()
    if not draft_path.exists():
        print(f"Error: {draft_path} not found")
        sys.exit(1)

    # Catechism should be in docs/ at repo root
    # Try multiple locations
    catechism_path = Path("docs/CATECHISM.md")
    if not catechism_path.exists():
        catechism_path = draft_path.parent.parent / "docs" / "CATECHISM.md"
    if not catechism_path.exists():
        catechism_path = Path.cwd() / "docs" / "CATECHISM.md"
    if not catechism_path.exists():
        print(f"Error: CATECHISM.md not found in docs/")
        sys.exit(1)

    claims = load_catechism(catechism_path)
    errors = check_draft(draft_path, claims)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
