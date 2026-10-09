#!/usr/bin/env python3
"""Check draft for forbidden content: customer names, hosts, tokens, IDs, etc."""

import sys
import re
from pathlib import Path

import json as _json
def load_cfg(start=None):
    """post.config.json from the repo root (cwd or a parent of the draft). Missing file = defaults."""
    from pathlib import Path as _P
    for d in [_P.cwd(), *((_P(start).resolve().parents) if start else [])]:
        f = d / "post.config.json"
        if f.exists():
            return _json.loads(f.read_text())
    return {}

FORBIDDEN_PATTERNS = {
    "workspace_host": (r'[\w-]+\.cloud\.databricks\.com|[\w-]+\.databricks\.net', "workspace host URL"),
    "dapi_token": (r'\bdapi[a-z0-9]{20,}', "DAPI token"),
    "jwt_token": (r'\beyJ[A-Za-z0-9_-]{20,}', "JWT token"),
    "uuid": (r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', "UUID-like ID"),
    "claude_mention": (r'(?<!databricks-)\bClaude\b', "coding assistant name 'Claude'"),
    "cursor_mention": (r'\bCursor\b', "coding assistant name 'Cursor'"),
    "copilot_mention": (r'\bCopilot\b', "coding assistant name 'Copilot'"),
    "codex_mention": (r'\bCodex\b', "coding assistant name 'Codex'"),
}

def check_draft(draft_path):
    """Scan draft for forbidden patterns; return list of (line_num, message)."""
    errors = []
    cfg = load_cfg(draft_path)
    patterns = dict(FORBIDDEN_PATTERNS)
    for i, (rx, why) in enumerate(cfg.get("forbidden", [])):
        patterns[f"cfg_{i}"] = (rx, why)

    with open(draft_path) as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, 1):
        for pattern_name, (pattern, description) in patterns.items():
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                hit = match.group()
                # Redact to first 4 chars + "…"
                redacted = hit[:4] + "…" if len(hit) > 4 else hit
                errors.append(f"Line {line_num}: {description} ({redacted})")

    return errors

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <draft.md>")
        sys.exit(1)

    draft_path = Path(sys.argv[1])
    if not draft_path.exists():
        print(f"Error: {draft_path} not found")
        sys.exit(1)

    errors = check_draft(draft_path)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
