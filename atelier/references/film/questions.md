# The six upfront questions for a demo film

Ask all six in **one message**, with the defaults filled in, so the user only corrects what differs. The defaults are the owner's answers for the Lakebase teaser films (clinical-va-appkit, `docs/video/CATECHISM.md`, 2026-09-29). Quote the answers when you route (atelier Step 3).

| # | Question | Default (last film) | What it decides |
|---|---|---|---|
| 1 | **Reach:** who sends it, where, and how often? | Field use: SAs send it and show it many times. Narrowed later to internal outreach plus the presenter prep screen in the app (D15). | Tier. "Shown many times" and a falsifier in Q2 trigger the named-skeptic rule → Tier 3 for every claim. |
| 2 | **Audience:** which person, and what will they check? | Film A: a health-system data platform lead who "will check every Lakebase claim". Film B: an app developer **and** an enterprise architect. | One film per persona pair; the one question each film answers; which seats are musts. |
| 3 | **Length** | 60–90 s teaser (the finals ran 75.5 s and 84 s) | Shot count (about 18) and on-screen words (about 135–150) |
| 4 | **Sound** | Text on screen plus music; it must work muted. Music added later on a 90 BPM grid (1 beat = 0.667 s). | Reading-time gate; cut grid; the music licence stop |
| 5 | **Format** | 16:9 (1920×1080) and 1:1 (1080×1080), H.264, 30 fps | Crop and safe-area checks on every cut; the 1:1 cut stacks the caption above a tighter crop |
| 6 | **Screens** | Real app screens, animated (crops and push-ins), plus real repo code shots and plain type cards | Screen source (see "Screen source" below); pill and crop-text checks |

Ask one follow-up only if the answer changes the route: **"Is any of it for customers?"** A yes is a promotion trigger (below).

## Screen source (decide at the attended script gate, not before)
- **Default:** capture every app screen **from one real rehearsal run**, read-only (GET-only script, free port, `<title>` checked). All shots come from that single run.
- The replay mode was the first choice last time and failed. It never rendered the probe panes, so the key frame didn't exist (D16). Don't plan a film around a replay until a capture proves the key frame renders.

## Promotion triggers (copy verbatim into `SESSION_PLAN.md`; any one → stop and re-plan)
- **Any customer use.** It needs the Remotion Company License (cleared through procurement) **or** a HyperFrames (Apache 2.0) re-render. The Remotion Free License covers individuals, companies of up to 3 employees, non-profits and evaluation, so Databricks is not covered (D3, D9).
- It goes to marketing or any public channel.
- A clinician or a customer reviews it.
- A new cut: another length, ratio or language.
- A claim in the app changes (re-run the ledger on every artifact that reuses it).
- A voice-over is added (the `demo-narrative` TTS scaffold then applies; it was skipped for text-only, D8).

## Hard stops that come with the defaults
Money (licences, paid music) · anything that dirties the demo slot (a live race or promote) · any deploy · anything public.
