#!/usr/bin/env python3
"""Validate markdown structure: title, word count, cited mentions (post.config.json "cite_rules"), paragraph length."""

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


def check_shape(draft_path, max_words=None):
    """Check markdown structure; return list of errors."""
    errors = []
    cfg = load_cfg(draft_path)
    if max_words is None:
        max_words = cfg.get("max_words", 2500)
    para_max = cfg.get("max_paragraph_words", 120)
    rules = [(re.compile(r["mention"], re.IGNORECASE), re.compile(r["citation"]), r["mention"])
             for r in cfg.get("cite_rules", [])]

    with open(draft_path) as f:
        content = f.read()
        lines = content.split('\n')

    # Check for title (# at start)
    has_title = any(line.startswith('#') for line in lines[:10])
    if not has_title:
        errors.append("Missing title (# at the beginning)")

    # Check word count
    word_count = len(content.split())
    if word_count > max_words:
        errors.append(f"Word count {word_count} exceeds limit of {max_words}")

    # Each cite rule: a paragraph that mentions X must carry a citation matching Y
    def check_para(text):
        for mention, citation, name in rules:
            if mention.search(text) and not citation.search(text):
                errors.append(f"{name} mentioned without citation: {text[:60]}...")

    current_paragraph = []
    for line in lines:
        if line.lstrip().startswith(("#", "![")):  # headings and image captions
            continue
        if line.strip() == "":
            check_para(" ".join(current_paragraph))
            current_paragraph = []
        else:
            current_paragraph.append(line.strip())
    check_para(" ".join(current_paragraph))

    # Check paragraph length (no paragraph > para_max words)
    current_paragraph = []
    for i, line in enumerate(lines):
        if line.strip() == "":
            paragraph_text = " ".join(current_paragraph)
            para_word_count = len(paragraph_text.split())
            if para_word_count > para_max:
                errors.append(f"Line {i}: Paragraph exceeds {para_max} words ({para_word_count} words)")
            current_paragraph = []
        else:
            current_paragraph.append(line.strip())

    # Check last paragraph
    paragraph_text = " ".join(current_paragraph)
    para_word_count = len(paragraph_text.split())
    if para_word_count > para_max:
        errors.append(f"Last paragraph exceeds {para_max} words ({para_word_count} words)")

    return errors

def main():
    max_words = None
    draft_path = None

    # Parse arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--max-words":
            i += 1
            if i < len(sys.argv):
                try:
                    max_words = int(sys.argv[i])
                except ValueError:
                    print(f"Error: --max-words requires an integer, got {sys.argv[i]}")
                    sys.exit(1)
            i += 1
        else:
            draft_path = sys.argv[i]
            i += 1

    if not draft_path:
        print(f"Usage: {sys.argv[0]} [--max-words N] <draft.md>")
        sys.exit(1)

    draft_path = Path(draft_path)
    if not draft_path.exists():
        print(f"Error: {draft_path} not found")
        sys.exit(1)

    errors = check_shape(draft_path, max_words)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
