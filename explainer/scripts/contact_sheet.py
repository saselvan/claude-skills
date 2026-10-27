#!/usr/bin/env python3
"""Tile frames of the rendered film into one contact sheet, sampled by time, for the builder's own look.

Usage: python3 -I contact_sheet.py <film-dir> [--video <mp4>] [--cols 5] [--rows 4] [--out contact_sheet.png]
Picks the newest .mp4 under <film-dir>/renders/ (or <film-dir>) when --video is not given. Needs ffprobe and ffmpeg.
The sheet is for eyes: the builder lists every problem seen (overlap, repeated text, a caption naming something not in
the frame, faint scope text), fixes, re-renders, and puts the list in the report (SKILL.md, phase 3).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("film", type=Path)
    ap.add_argument("--video", type=Path)
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--rows", type=int, default=4)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    film = a.film.resolve()
    video = a.video
    if not video:
        mp4s = sorted(list((film / "renders").glob("*.mp4")) + list(film.glob("*.mp4")), key=lambda p: p.stat().st_mtime)
        if not mp4s:
            print("FAIL contact-sheet: no .mp4 under renders/ or the film folder; render a draft first")
            return 1
        video = mp4s[-1]
    out = a.out or film / "checks-out" / "contact_sheet.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True, check=True).stdout.strip())
    n = a.cols * a.rows
    fps = n / dur  # one frame every dur/n seconds; the fps filter resamples by time, so no frame count is needed
    vf = f"fps={fps:.6f},scale=480:-1,tile={a.cols}x{a.rows}"
    run = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf", vf, "-frames:v", "1", str(out)],
                         capture_output=True, text=True)
    if run.returncode:
        print(f"FAIL contact-sheet: ffmpeg: {run.stderr.strip()[:300]}")
        return 1
    print(f"PASS contact-sheet: {out} ({n} frames of {video.name}, {dur:.1f} s, one every {dur / n:.2f} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
