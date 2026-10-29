# Precedents

One entry per piece: the concept, the picture chosen, and the owner's verdict in the owner's words. Newest first. Source files: `/private/tmp/hf-vision-proto/` (prototype, not committed).

## Graph Kit film v3/v4: owner rulings after watching v2 (2026-10-21)

- Cost: the v2 judging loop ran 4 h 47 min, 2 judges per beat per round. Owner: "I know Opus 5.5 is the dude for motion graphics but I'll need to make the other parts less expensive, which is also why I am spending so much time on this explainer skill."
- Rulings: no camera zoom; scene changes are 0.5 s crossfades, after the element you go into fills with its colour and holds. Film is dark, one colour per system (lake, Spark, Lakebase) plus one bright "what happens now" colour. Spark gets its own beats ("Spark SQL on a SQL warehouse"), then shrinks left; Lakebase gets about 60% of the time. Voice-over plus `.srt` (LinkedIn plays muted); the question at frame 0; a phone-width text check. No glows.
- Numbers: a number appears in the beat that earns it. 4.2 ms is the top of a p95 range: "Walks of 1 to 4 hops: 19 of 20 answer in 4.2 ms or less (client p95)". A mean is never called a p95.
- Look question: why is our graph less nice than 3Blue1Brown's? Answer adopted: dark ground, strong colours, few marks, one shape becoming the next, eased holds, the voice carries the sentences, large type. Keep HyperFrames; no 3D unless a dimension carries data.

## Skill A/B test: did the new look rules change the storyboards? (2026-10-21)

- Set-up: 4 blind builds (Opus 5.5) of the same DNB storyboard, 2 with the new skill and 2 with the old one. Judges GPT-5.6 Sol and Gemini 4 Argon, both orders, 8 runs. Rule fixed before judging: 6 of 8 picks for one arm. Files: `/Users/samuel.selvan/src/lakebase-agentic-search/.scratch/explainer/skill-ab/REPORT.md`.
- Owner's question: "I am looking to see if the new changes to the skill you made make a difference".
- Result: no difference on "one idea fills the frame", "one thing becomes the next", "pictures, short sentences", text size, or number sources. Only the map or diagram question differed, and it favoured the OLD skill (6 of 8). Overall pick, reported only: new 5, old 3. Controls were fine.
- Sol picked "Sheet 2" in 28 of 31 answers: it judged the position, not the content.
- Lesson: a rule written as advice did not move the output. Each look rule now has a check you can count. A possible cause for the map result (not proven): "one idea fills the frame" made builders shrink the connected-parts diagram. So when the beat is about how parts connect, the whole map stays the one idea.

## Graph Kit film v2: gauntlet loop in Cursor (2026-10-21)

- Set-up: Opus 5.5 builds each beat; Sol and Argon judge it blind against one reference per beat; 4 rounds per beat at most. Prompt: `/Users/samuel.selvan/repos/lakebase-graph-kit/.scratch/explainer-v2/gauntlet-prompt.md`.
- Result: 7 beats and the pacing pass passed. b06 split between the judges. b09 stayed unresolved, because Claude's "no rerun" pick (the owner said "your picks") blocked the fix its bar needed.
- Owner: "I already have it building with B numbers why do you keep going to A". The owner's "B" meant the number set; it was read as a camera option.
- Lessons: resolve a clash between a ruling and a bar before round 1 (the bar fit check); when both judges name the same gap, fix it at once; give options names, not letters; stamp the judge model in each pack; capture the reference frames before judging; count labels apart from sentences; judge the whole sheet first.

## Course 1 film: agentic search on Databricks (2026-10-20)

**Cursor rebuild on real data (Gemini model, from v6 + `cursor-prompt-course1-film.md`)**
- Picture: 10 beats, 67 s. Each frame is a dashboard: the question as a form field, four clause cards of verbatim text, a row of trace-span chips (`tr-…`, span ids, ms) at the bottom, badges (`REAL · tr-…`, `TARGET SETUP · TICKET P3`), and a boxed caption. Beats 1 to 7 are almost the same frame. The bottom half is empty. Beat 10 is a table list inside a red box.
- Gates all passed: honesty tests A1–A10, 10/10 mutations killed, HyperFrames check, caption checker. The film still failed.
- Verdict: "the cursor gemini model effort was a colossal disappintment".
- What broke, against v6: (1) it went back to a log of spans, the pre-v1 failure; (2) it dropped v6's grammar: no Search vs Agentic search side by side, no colour per page, no threads tied from claim to page, no growth in place; (3) the honesty labels became the content, so receipts sit on every frame instead of at the end; (4) the question became catalogue words ("promotional spend window") in place of a customer's words; (5) the text is too small to read at 1080p.
- Lesson: the honesty gate tests labels, not story. A brief for another model must also gate the picture: one frame per v6 beat, the same marks, and a contact sheet compared with v6 before any test runs. The real data (unfiltered baseline, trace `tr-2918490d…`) is good; keep it and re-skin it in v6's grammar.

**v6 (Lakebase is the state)**
- Picture: a memory row is read first (short tight line), then fades. A failed check is a dashed coral thread straight to the named page, plus a dashed outline on it ("known but unread"); the next round's wire snaps and the thread becomes solid. Zoom out to seven systems. The pages slide into rows of a `pages` table; the vector database, session cache, memory store and app database fly into one Lakebase box (4 into 1); `memory`, `sessions`, `citations`, `app_state` fill; Unity Catalog, Model Serving, MLflow settle around it inside the Databricks boundary.
- Owner ruling before build: "A, go one last round and then we have Cursor do it for the real blog series". Verdict: pending.
- Owner question: "the vertical stacked bar at 30 seconds, what does it mean?" It was a backed-up sync queue with no label. Lesson: label every new symbol the first time it appears.

**v5 (paper look, grammar applied)**
- Picture: paper ground, 1 px lines, a thin chapter line at the bottom. Search is a query point whose rings spread (clipped to the page area); each page lightens when the ring reaches it, by distance. Each claim gets a thread pulled taut to its page. A failed check is a coral thread that reaches toward the named page and drops. Following a reference is a straight wire that snaps (linear). Unused pages move to a top row so threads stay clear. Zoom out: queues sit on each hop between five systems, and one hop backs up.
- Verdict: "V5 is nice but why do the lines go limp and back to the rectangle below". Lesson: a failed check must point forward to where the answer is, not fall back. A limp line reads as a glitch.

**v4 (trail through the pages)**
- Picture: all 8 pages sit faint like a map. Each round lights one page, draws one wire to the page the check named, and adds one clause in that page's colour. Rounds speed up (3.0 s, 2.4 s, 1.9 s, 1.5 s). Then a zoom out to five systems in a ring, which fold into one Databricks boundary.
- Verdict: "Closer". Next: apply the grammar (round 1 is a search, so it should flow by distance; later rounds follow references, so they snap; a failed check is a thread that drops).

**v3 (circle loop, two passes)**
- Verdict on the loop: "it won't be a proper circle or shouldn't be because who wants to see me go around a loop 4 times". On pass 2: "it is not clear why and how pass2 helped". On the five systems: "looked half-assed".
- Lesson: show progress, not repetition. Put the cause of each round on screen.

**v1–v2 (question → plain search fails → agentic loop → zoom out → one platform)**
- Verdict on v1: "Closer". Asked for: "someone's vision… clean, sparse and just tells the story".

**Before v1: the 6-beat causal trace (made in Cursor)**
- Picture: six equal boxes with `file:line` chips and span ids.
- Verdict: "kinda boring and not creative and still feel like the causality and the sheer improvement Agentic Search gets you and the platform benefit isn't coming through".
- Lesson: a log is not a story. One hero moment, few words, receipts at the end.

## Graph Kit film v6: the care finder walk, muted first (2026-10-26 to 2026-10-29)
- Picture: the kit's story on one stage (Delta → Spark SQL → Lakebase, inside Unity Catalog). The followed object is a patient's
  question, "Who near me treats type 2 diabetes?"; the walk is the care finder app's four hops on the graph the kit builds
  (words → condition → nearby doctors → co-conditions, keeping doctors with a line to all → similar-practice doctors). A bright mark
  rides each edge; doctors without all three conditions go dark in place; one doctor lights as the answer. 107.5 s, 4:5, 60 fps, muted.
- Verdicts: on the computer voice cut in separate takes, "correct mechanically but hardly flows as in these are disjoint sentences with
  no narrative at all. What is the purpose of adding voice to this video?"; on the muted cut, "much better"; on the hops, "is the
  language and visuals intuitive to show how the hops happen and what they mean … what exactly the 2 and 3 hops achieve?"; on a caption,
  "I see whole patient, what is a whole patient, is there a half patient?"; on the framing, "kit just builds the graph bro".
- Lessons: (1) a voice built from captions sounds like a list; the owner's own voice, written for the ear, comes first (target:
  LinkedIn muted + Medium). (2) A walk needs a question that takes more than one hop; if hop 1 answers it, the later hops have no reason.
  (3) Name what each hop gets the viewer, not the SQL rule. (4) Cutting sentences out of one long text-to-speech take leaves the next
  word's first sound on the ending; record one take per sentence. (5) Never present the app's queries as the kit's own claim.
- Process: seams with a carried frame hold 0.6 s then crossfade 0.5 s; an owner-ruled exception goes in `checks.json` with a reason
  (`crossing_ok`), and a check without its reason must fail. `hyperframes check --strict` found what the probe did not (a headline
  deadline, two code strips overlapping); run it before the render.

## Standing owner rulings
- No guess-first or quiz moves: "infantile and disrespectful if a system architect is in the room".
- References are cues to make the piece better, for example "using 3Blue1Brown to make ideas like Pareto or vectors look nice and associated with physics", and "if you're looking up data in a table as opposed to unstructured data the motion and graphics themselves should make those differences clear".
- The whole platform is in scope, guided by heuristics rather than strict rules.
