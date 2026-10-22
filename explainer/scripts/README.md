# Explainer code checks

Run them on the text-approved build, before the first render:

```bash
~/.claude/skills/explainer/scripts/run_checks.sh <film-dir>
```

It runs `check_film.py`, then `hyperframes lint` and `check` on each composition (offline, `GEMINI_API_KEY` unset).
Render only when it prints `run_checks: ALL PASS`.

`check_film.py` opens each composition in HyperFrames' local headless Chrome, with the network blocked. It seeks the
timeline every 0.1 s and records every painted text. So the checks see what the render paints, not what the source
says. On v5 (two 90 s compositions) the whole run took 29 s.

| Check | Fails when |
|---|---|
| fonts | a painted text's first font family is not a loaded local `@font-face` |
| network | the page asks for anything that is not a local file |
| numbers | a number on screen or in an `.srt` is in no `claims` file and not in `numbers_ok`, or is in `numbers_banned` |
| words | a `banned_words` word is on screen, in an `.srt` or in the script; a `banned_on_screen` word is on screen or in an `.srt` |
| sql | a code row (`[data-code]`, else any mono text) is not a piece of one line of `sql_dir/*.sql`; `...` may skip text |
| captions | motion-style's `check_captions.py` fails a cue |
| burned-captions | the caption band's text at a cue's middle differs from the `.srt` cue |
| text-size | a text's largest rendered size is under frame height / 36 (labels) or / 20 (captions); transforms count |
| layout | a text line is partly cut (clip, overflow or frame edge), sits on another panel, or crosses another text |
| hidden | a text is `visibility: hidden` at full opacity (v5's F6), or a `must_show` text shows for less than its `hold` |

## checks.json, in the film folder

```json
{
  "compositions": [{"dir": "film-4x5", "srt": "film-4x5.srt"}, {"dir": "film", "srt": "film-16x9.srt"}],
  "script": "script.md",
  "claims": ["claims.md", "~/repos/<repo>/docs/release/post-claims.md"],
  "numbers_ok": [],
  "numbers_banned": [],
  "banned_words": [],
  "banned_on_screen": [],
  "sql_dir": "sql",
  "mono_not_sql": [],
  "must_show": [{"text": "the headline of beat 5", "from": 26, "to": 32, "hold": 1.0}],
  "label_div": 36,
  "caption_div": 20
}
```

- Paths are relative to the film folder, or absolute, or start with `~`.
- `claims`: the film's claims file and the claim register. A number is allowed when it appears in one of them.
- `numbers_ok`: numbers that are structure, not claims (for example a step count). Keep it short; each entry is a claim
  you did not register.
- `must_show`: each headline, kicker and question the storyboard puts on screen, with its beat's time window.
- `label_div`, `caption_div`: motion-style's floors. Change them only when motion-style changes.

## Markup the checks read

The starter (`../starter-v5/`) uses all of it. The probe's docstring (`film_probe.py`) has the full list.

- `[data-caption-band]` on the caption track.
- `[data-panel="name"]` on each panel; `[data-in="name"]` on text drawn on a panel that is not its DOM child.
- `[data-code]` on the code panel. Without it, every mono text counts as code.
- `[data-layout-allow-overlap]` on text that may cross other text on purpose.

## Proof that each check can fail

```bash
~/.claude/skills/explainer/scripts/selftest.sh
```

It runs the checks on `fixture/` (a 6 s film), which passes clean. Then it plants one bug per row and shows that its
own check goes red. Add a row to `selftest.sh` when you add a check.

On 2026-10-22 these checks ran on the committed v5 film. They found the two v5 bugs that were known by eye: two 4:5
captions with three lines, and 14 texts in 16:9 left `visibility: hidden` (F6). The film's own v5 checks missed F6.
