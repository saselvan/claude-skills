#!/usr/bin/env python3
"""Generate script.md, both .srt files, and both compositions' CUES, CLOCK and clip times from screen-copy.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COPY = ROOT / "screen-copy.json"
CUES_BEGIN = "/* BEGIN GENERATED CUES */"
CUES_END = "/* END GENERATED CUES */"
CLOCK_BEGIN = "/* BEGIN GENERATED CLOCK */"
CLOCK_END = "/* END GENERATED CLOCK */"
# one cue list, two line breaks: 16:9 burns "lines", 4:5 burns "lines_4x5" (same words, about 30 characters a line)
LAYOUTS = (
    # the 16:9 layout, when the film has one:
    # ("lines", ROOT / "explainer-v5-16x9.srt", ROOT / "film" / "index.html"),
    ("lines_4x5", ROOT / "explainer-v5-4x5.srt", ROOT / "film-4x5" / "index.html"),
)


def layout_cues(cues: list, key: str) -> list:
    out = []
    for cue in cues:
        if key not in cue:
            raise SystemExit(f"cue {cue['id']} has no {key}")
        item = {k: v for k, v in cue.items() if k != "lines_4x5"}
        item["lines"] = list(cue[key])
        out.append(item)
    return out


def ms(seconds: float) -> int:
    return int(round(float(seconds) * 1000))


def srt_stamp(seconds: float) -> str:
    total = ms(seconds)
    hours, total = divmod(total, 3_600_000)
    minutes, total = divmod(total, 60_000)
    secs, milli = divmod(total, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milli:03d}"


def script_stamp(seconds: float) -> str:
    total = ms(seconds)
    minutes, total = divmod(total, 60_000)
    secs, milli = divmod(total, 1000)
    return f"{minutes:02d}:{secs:02d}.{milli:03d}"


def render_srt(cues: list) -> str:
    blocks = []
    for index, cue in enumerate(cues, 1):
        body = "\n".join(cue["lines"])
        blocks.append(
            f"{index}\n{srt_stamp(cue['start'])} --> {srt_stamp(cue['end'])}\n{body}"
        )
    return "\n\n".join(blocks) + "\n"


def render_script(data: dict) -> str:
    beats = data["beats"]
    cues = data["cues"]
    parts = [
        "---",
        "title: Lakebase Graph Kit film v5",
        f"duration_seconds: {float(beats[-1]['end']):g}",
        "scratch_voice: Samantha",
        "scratch_rate_wpm: 190",
        "subtitle: explainer-v5-16x9.srt",
        "---",
        "",
        "# Narration",
        "",
        "Generated from `screen-copy.json`. Each `- Cue:` is one event.",
        "",
    ]
    for beat in beats:
        start = float(beat["start"])
        end = float(beat["end"])
        parts.extend(
            [
                f"## Beat {beat['id']}",
                "",
                f"- Time: {script_stamp(start)} --> {script_stamp(end)}",
                f"- Seconds: {end - start:g}",
                f"- Claim: {beat['claim']}",
            ]
        )
        for cue in cues:
            # a cue may run past its beat's end; it is listed once, under the beat it starts in
            if not start <= float(cue["start"]) < end:
                continue
            parts.append(f"- Cue: {script_stamp(cue['start'])} --> {script_stamp(cue['end'])}")
            for line in cue["lines"]:
                parts.append(f"  {line}")
        parts.append("")
    parts.extend(
        [
            "## Run-time split",
            "",
            *render_split(beats),
            "",
        ]
    )
    return "\n".join(parts)


def render_split(beats: list) -> list:
    total = float(beats[-1]["end"])
    spark, landing, lakebase = beats[3], beats[4], (beats[5], beats[10])
    main = lakebase[1]["end"] - lakebase[0]["start"]
    landed = lakebase[1]["end"] - landing["start"]
    return [
        f"- Spark is the main system for {spark['end'] - spark['start']:g} seconds, "
        f"from {spark['start']:g} to {spark['end']:g} seconds.",
        f"- Lakebase is the main system for {main:g} seconds, "
        f"from {lakebase[0]['start']:g} to {lakebase[1]['end']:g} seconds.",
        f"- Including the {landing['end'] - landing['start']:g}-second landing beat, Lakebase receives "
        f"{landed:g} seconds, or {100 * landed / total:.1f}% of the film.",
    ]


def render_clock_block(beats: list) -> str:
    payload = json.dumps([{"id": b["id"], "start": b["start"], "end": b["end"]} for b in beats])
    return f"        {CLOCK_BEGIN}\n        const BEATS = {payload};\n        {CLOCK_END}\n"


def replace_clock_block(text: str, block: str) -> str:
    if CLOCK_BEGIN in text:
        start = text.rfind("\n", 0, text.index(CLOCK_BEGIN)) + 1
        end = text.index("\n", text.index(CLOCK_END)) + 1
        return text[:start] + block + text[end:]
    anchor = text.index("\n", text.index(CUES_END)) + 1
    return text[:anchor] + block + text[anchor:]


def replace_clip_times(text: str, beats: list) -> str:
    total = f"{float(beats[-1]['end']):g}"
    text, roots = re.subn(r'(<div id="root"[^>]*data-duration=")[\d.]+"', rf'\g<1>{total}"', text)
    text, audios = re.subn(r'(<audio id="[^"]+" src="[^"]+" data-start="0" data-duration=")[\d.]+"', rf'\g<1>{total}"', text)
    # the audio clip (a scratch voice or ticks) is optional; when it is there, it runs the whole film
    if roots != 1 or audios > 1:
        raise SystemExit("composition must hold one root and at most one audio clip")
    for beat in beats:
        start, length = f"{float(beat['start']):g}", f"{float(beat['end']) - float(beat['start']):g}"
        text, count = re.subn(
            rf'(<section id="b{beat["id"]:02d}"[^>]*?)data-start="[\d.]+" data-duration="[\d.]+"',
            rf'\g<1>data-start="{start}" data-duration="{length}"', text)
        if count != 1:
            raise SystemExit(f"composition has no section b{beat['id']:02d}")
    return text


def render_cues_block(cues: list) -> str:
    payload = json.dumps(cues, indent=2)
    return (
        f"        {CUES_BEGIN}\n"
        f"        const CUES = {payload};\n"
        f"        {CUES_END}\n"
    )


def replace_cues_block(text: str, block: str) -> str:
    if CUES_BEGIN not in text or CUES_END not in text:
        raise SystemExit("composition is missing the generated CUES markers")
    start = text.index(CUES_BEGIN)
    line_start = text.rfind("\n", 0, start) + 1
    _, after = text[start:].split(CUES_END, 1)
    after = after.lstrip("\n")
    return text[:line_start] + block + after


def main() -> int:
    data = json.loads(COPY.read_text(encoding="utf-8"))
    cues = data["cues"]
    (ROOT / "script.md").write_text(render_script(data), encoding="utf-8")
    clock = render_clock_block(data["beats"])
    for key, srt_path, path in LAYOUTS:
        layout = layout_cues(cues, key)
        srt_path.write_text(render_srt(layout), encoding="utf-8")
        text = replace_cues_block(path.read_text(encoding="utf-8"), render_cues_block(layout))
        text = replace_clip_times(replace_clock_block(text, clock), data["beats"])
        path.write_text(text, encoding="utf-8")
    print(f"generated {len(cues)} cues and {len(data['beats'])} beats into script.md, both .srt files, "
          "and both compositions (CUES, CLOCK, clip times)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
