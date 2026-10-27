# Changes in this patch (2026-10-26)

One voice, generic, phased, checked. Against the previous skill folder:

- `SKILL.md` rewritten: four phases with time boxes and two owner stops; every rule names its check or is marked taste;
  no history in the rule text (it lives in `references/precedents.md`); audience and domain are `BRIEF.md` fields.
- `references/playbook.md` replaces `hyperframes-playbook.md` and the four research notes: written against the current
  upstream (7-skill layout, `timeline` edits, `history`, `.motion.json`, `snapshot --review`, local `tts`/`transcribe`),
  with the places upstream advice is overruled by motion-style listed in one section.
- `references/grammar.md` is generic; the platform rows moved to `references/domains/databricks.md` (plus
  `databricks-sequences.md`). A new domain is one file.
- `starter/` replaces `starter-v5/`: a two-scene 4:5 project in the native sub-composition structure, `tokens.css`,
  `tokens.js` (three eases, three durations, the edge speed), a caption scene, the seam files, `scene-harness.html`.
- Scripts: `film_probe.py` probes scene files through the harness and adds the tween audit and the determinism pass;
  `check_film.py` adds determinism, ease-presentation, ease-family, duration-set, hold, overlap (note), crossing,
  metronome, fragments, sentence-length, hierarchy, peak, transcript; `hf-safe.sh` is the only HyperFrames entry;
  `check_transcript.py`, `contact_sheet.py`, `cleanup.sh` are new; `check_captions.py` is vendored from motion-style;
  `selftest.sh` has a plant per check (32 rows); the fixture is in the scene structure.
- Removed: `.bak-*`, `__MACOSX`, `._*`, `.DS_Store`, `__pycache__`, `example-v6.html`, `hyperframes-research/`.
- Not verified in a browser or against a HyperFrames install at the time of writing: see `MIGRATION.md` steps 2–3.
  The dry run of `check_film.py` with a synthetic probe record passes clean and every selftest regex applies once.
