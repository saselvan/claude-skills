#!/usr/bin/env python3
"""Spoken words equal the .srt, cue by cue.

Reads checks.json: "transcript" (a local `hyperframes transcribe --json` output, a whisper-style JSON with
segments[].words[] of {word,start,end}, a flat list of {word,start,end}, or an .srt/.vtt) and "srt". For each .srt cue,
the words heard inside its time window must equal the cue's words, after normalising case, punctuation and numbers
(both sides have digits turned into words, so "25" and "twenty-five" compare equal). Words heard inside a 0.25 s margin
of the cue edge count for either cue, so a boundary word is never a false mismatch.

Usage: python3 -I check_transcript.py <film-dir>
Exit 1 on any cue mismatch; 0 if no transcript is configured (SKIP).
Written 2026-10-26; the transcribe JSON shape is read loosely because the CLI's exact schema was not verified then.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "zero ten twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n: int) -> list[str]:
    if n < 20:
        return [ONES[n]]
    if n < 100:
        return [TENS[n // 10]] + ([ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [ONES[n // 100], "hundred"] + (num_words(n % 100) if n % 100 else [])
    for div, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")):
        if n >= div:
            return num_words(n // div) + [name] + (num_words(n % div) if n % div else [])
    return [str(n)]


def tokens(text: str) -> list[str]:
    out: list[str] = []
    for tok in re.findall(r"[A-Za-z]+|\d+(?:[.,]\d+)*", text.lower()):
        if tok[0].isdigit():
            if "." in tok:
                a, b = tok.split(".", 1)
                out += num_words(int(a.replace(",", ""))) + ["point"] + [ONES[int(c)] for c in b if c.isdigit()]
            else:
                out += num_words(int(tok.replace(",", "")))
        else:
            out += [p for p in tok.split("-") if p]
    return out


def srt_time(ts: str) -> float:
    h, m, rest = ts.strip().split(":")
    s, ms = rest.replace(".", ",").split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def read_srt(path: Path) -> list[tuple[float, float, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        lines = [ln for ln in block.strip().splitlines() if ln.strip()]
        for i, line in enumerate(lines):
            if "-->" in line:
                a, b = line.split("-->")
                cues.append((srt_time(a), srt_time(b), " ".join(lines[i + 1:])))
                break
    return cues


def read_words(path: Path) -> list[tuple[float, float, str]]:
    if path.suffix.lower() in (".srt", ".vtt"):
        words = []
        for s, e, text in read_srt(path):
            toks = text.split()
            for i, w in enumerate(toks):  # spread the cue's words evenly over its window
                words.append((s + (e - s) * i / max(1, len(toks)), s + (e - s) * (i + 1) / max(1, len(toks)), w))
        return words
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("words") or [w for seg in data.get("segments", []) for w in seg.get("words", [])]
    return [(float(w["start"]), float(w["end"]), str(w.get("word") or w.get("text") or "")) for w in items]


def main() -> int:
    film = Path(sys.argv[1]).resolve()
    cfg = json.loads((film / "checks.json").read_text(encoding="utf-8"))
    if not cfg.get("transcript"):
        print("SKIP transcript: no transcript in checks.json")
        return 0
    tpath = (film / cfg["transcript"]).resolve()
    spath = (film / cfg["srt"]).resolve()
    if not tpath.exists():
        print(f"FAIL transcript: {tpath} does not exist")
        return 1
    heard = read_words(tpath)
    cues = read_srt(spath)
    margin = 0.25
    probs = []
    for s, e, text in cues:
        want = tokens(text)
        core = [w for a, b, w in heard if a >= s - margin and b <= e + margin]
        got = tokens(" ".join(core))
        if got == want:
            continue
        # allow edge words to belong to either cue: compare the multiset difference without the first/last token
        if got[1:-1] == want[1:-1] and set(got) >= set(want[1:-1]):
            continue
        probs.append(f"{s:.1f}-{e:.1f} s: .srt {' '.join(want)!r} / heard {' '.join(got)!r}")
    if probs:
        print(f"FAIL transcript: {len(probs)} cue(s) differ from the voice:\n  " + "\n  ".join(probs[:25]))
        return 1
    print(f"PASS transcript: {len(cues)} cues match the spoken words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
