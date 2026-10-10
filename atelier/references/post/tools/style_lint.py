#!/usr/bin/env python3
"""Check a post draft against writing-style's checkable mechanics.

Exits 1 on a failure. Warnings print for a person to judge and never fail the gate.

Failures:
  - more em dashes than allowed ("rarely, if at all")
  - more than one "X, not Y" contrast ("at most one per piece")
  - a bulleted or numbered list in the prose ("No list. Screams AI.")
  - three or more one-sentence paragraphs in a row ("A never B": no one sentence per line)
  - "my read" or "my take" ("Never stuff like 'my read.'")
  - an ending that asks for engagement, on a personal channel ("a statement, with no ask")
  - a LinkedIn post over its word limit ("LinkedIn posts around 60 words")

Warnings:
  - an acronym with no expansion anywhere in the draft ("Always good to expand on acronyms")
  - absolute words to check against the evidence ("Every is a lie")

Config: post.config.json, key "style" (all optional):
  max_em_dashes (1), max_contrasts (1), allow_lists (false), linkedin_max_words (100),
  known_acronyms ([]), channel ("medium"), ending ("statement"; "cta" for the Databricks blog).
A draft whose filename contains "linkedin" is checked as a LinkedIn post.
"""

import json
import re
import sys
from pathlib import Path


def load_cfg(start=None):
    """post.config.json from the repo root (cwd or a parent of the draft). Missing file = defaults."""
    for d in [Path.cwd(), *((Path(start).resolve().parents) if start else [])]:
        f = d / "post.config.json"
        if f.exists():
            return json.loads(f.read_text())
    return {}


DEFAULT_ACRONYMS = {"AI", "API", "SQL", "URL", "PDF", "CEO", "CIO", "CTO", "UI", "UX", "US", "UK", "OK", "FAQ"}
TAG = re.compile(r"\[C\d+\]|\((?:transcripts|runs|evidence|results)/[^)]*\)")
CONTRASTS = [
    re.compile(r",\s+not\s+(?:the\s+|a\s+|an\s+)?\w+", re.IGNORECASE),            # "the policy, not the pipeline"
    re.compile(r"\bisn['’]t\s+[^.;]+?[;,]\s+it['’]s\b", re.IGNORECASE),             # "isn't X; it's Y"
    re.compile(r"\bnot\s+(?:just\s+)?(?:a|an|the)?\s*\w+[^.;]*?,\s*but\b", re.IGNORECASE),  # "not X, but Y"
]
LIST_LINE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
MY_READ = re.compile(r"\bmy\s+(?:read|take)\b", re.IGNORECASE)
BAIT = re.compile(r"\b(?:thoughts\?|agree\?|comment below|let me know|what do you think|drop a comment)", re.IGNORECASE)
ABSOLUTE = re.compile(r"\b(?:every|always|never|all|none)\b", re.IGNORECASE)
ACRONYM = re.compile(r"\b[A-Z]{2,6}s?\b")


def prose_lines(text):
    """Yield (line_number, line) for prose: no code fences, headings, images or tables; tags removed."""
    in_code = False
    for n, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith(("#", "![", "|")):
            continue
        yield n, TAG.sub("", line)


def paragraphs(lines):
    """Group prose lines into paragraphs: list of (first_line_number, text)."""
    out, cur, start = [], [], None
    for n, line in lines:
        if line.strip() == "":
            if cur:
                out.append((start, " ".join(cur)))
            cur, start = [], None
        else:
            start = start or n
            cur.append(line.strip())
    if cur:
        out.append((start, " ".join(cur)))
    return out


def check(path, channel=None):
    cfg = load_cfg(path).get("style", {})
    text = Path(path).read_text()
    channel = channel or ("linkedin" if "linkedin" in Path(path).name.lower() else cfg.get("channel", "medium"))
    lines = list(prose_lines(text))
    paras = paragraphs(lines)
    prose = " ".join(t for _, t in paras)
    errors, warnings = [], []

    dashes = [(n, l) for n, l in lines for _ in range(l.count("—") + l.count(" -- "))]
    if len(dashes) > cfg.get("max_em_dashes", 1):
        errors.append(f"{len(dashes)} em dashes (max {cfg.get('max_em_dashes', 1)}); first at line {dashes[0][0]}")

    hits = [(n, m.group(0)) for n, l in lines for rx in CONTRASTS for m in rx.finditer(l)]
    if len(hits) > cfg.get("max_contrasts", 1):
        errors.append(f"{len(hits)} 'X, not Y' contrasts (max {cfg.get('max_contrasts', 1)}): "
                      + "; ".join(f"line {n}: {h!r}" for n, h in hits[:4]))

    if not cfg.get("allow_lists", False):
        for n, l in lines:
            if LIST_LINE.match(l):
                errors.append(f"Line {n}: a list in the prose; write it as a paragraph")
                break

    run = 0
    for start, t in paras:
        single = len(re.findall(r"[.!?](?:\s|$)", t)) <= 1 and len(t.split()) <= 15
        run = run + 1 if single else 0
        if run == 3:
            errors.append(f"Line {start}: three one-sentence paragraphs in a row; join them into a paragraph")
            break

    for n, l in lines:
        if MY_READ.search(l):
            errors.append(f"Line {n}: 'my read' or 'my take'; state it as analysis")

    if cfg.get("ending", "statement") == "statement" and paras:
        n, last = paras[-1]
        if last.rstrip().endswith("?") or BAIT.search(last):
            errors.append(f"Line {n}: the ending asks for a response; end on a statement")

    if channel == "linkedin":
        limit = cfg.get("linkedin_max_words", 100)
        words = len(prose.split())
        if words > limit:
            errors.append(f"LinkedIn post is {words} words (limit {limit}; writing-style aims for about 60)")

    known = DEFAULT_ACRONYMS | set(cfg.get("known_acronyms", []))
    for acr in sorted({m.group(0).rstrip("s") for m in ACRONYM.finditer(prose)} - known):
        if f"({acr})" not in prose and not re.search(rf"\b{acr}\s*\(", prose):
            warnings.append(f"'{acr}' has no expansion; expand it, use a plain term, or add it to known_acronyms")

    for n, l in lines:
        for m in ABSOLUTE.finditer(l):
            warnings.append(f"Line {n}: '{m.group(0)}', which must be provable or replaced")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <draft.md> [--channel linkedin|medium|blog|databricks-blog]")
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)
    channel = sys.argv[sys.argv.index("--channel") + 1] if "--channel" in sys.argv else None
    errors, warnings = check(path, channel)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
