"""Check captions against the motion-style caption floors.

Input: a JSON file with a list of captions, each {"text": str, "start": s, "end": s},
where start is when the caption begins to arrive and end is when the next one begins.
Use "\n" in text for a deliberate line break.

Floors (BBC and Netflix subtitle standards, as adopted in motion-style):
  - at most 42 characters per line and at most two lines
  - a reading pace of about 15 characters per second
  - held at least 1 s and at most 7 s, counted from the moment it has settled

Usage: python check_captions.py captions.json [--settle 1.4]
Exit code 1 if any caption fails.
"""
import argparse
import json
import re
import sys


def _parse_srt_time(ts: str) -> float:
    h, m, rest = ts.strip().split(":")
    s, ms = rest.replace(".", ",").split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def _load_captions(path: str) -> list[dict]:
    raw = open(path, encoding="utf-8").read().strip()
    if raw.startswith("["):
        return json.loads(raw)
    blocks = re.split(r"\n\s*\n", raw)
    caps = []
    for block in blocks:
        lines = [ln for ln in block.strip().splitlines() if ln.strip()]
        if not lines:
            continue
        ts_idx = 1 if re.match(r"^\d+$", lines[0].strip()) else 0
        if ts_idx >= len(lines) or "-->" not in lines[ts_idx]:
            continue
        start_s, end_s = lines[ts_idx].split("-->")
        text = "\n".join(lines[ts_idx + 1 :])
        caps.append({"start": _parse_srt_time(start_s), "end": _parse_srt_time(end_s), "text": text})
    return caps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--settle", type=float, default=1.4, help="seconds for a caption to arrive")
    ap.add_argument("--cps", type=float, default=15.0)
    args = ap.parse_args()

    caps = _load_captions(args.path)
    failed = 0
    for c in caps:
        text = c["text"]
        lines = text.split("\n")
        chars = len(text.replace("\n", " "))
        hold = c["end"] - c["start"] - args.settle
        need = max(1.0, chars / args.cps)
        problems = []
        if len(lines) > 2:
            problems.append(f"{len(lines)} lines")
        long_lines = [l for l in lines if len(l) > 42]
        if long_lines:
            problems.append(f"line over 42 characters ({len(long_lines[0])})")
        if hold < need:
            problems.append(f"held {hold:.1f} s, needs {need:.1f} s")
        if hold > 7.0:
            problems.append(f"held {hold:.1f} s, over 7 s")
        status = "FAIL" if problems else "OK"
        failed += bool(problems)
        print(f"{status:4}  {hold:4.1f} s held, {need:4.1f} s needed  {text.replace(chr(10), ' / ')}"
              + (f"  [{'; '.join(problems)}]" if problems else ""))
    print(f"\n{len(caps) - failed} of {len(caps)} captions pass.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
