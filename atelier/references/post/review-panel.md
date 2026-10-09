# The post review panel

Used on lakebase-payer-search-blog and the CI/CD blog (2026-10). Runs **twice**: on the outline (before drafting) and on the final tagged draft (after the gates are green). It goes beyond the gates. The gates check facts and leaks mechanically; the panel checks whether a reader gets it, believes it and acts on it.

Follows the film panel's protocol (`../film/critic-panel.md`): one `blackboard` wave, every seat a fresh read-only `general-purpose` agent, one YAML block back, at most 6 findings each; the coordinator verifies every finding before acting, records false positives with the reason, and resumes the same agents for round 2. Stop at 0 HIGH that survive verification.

**Named experts are charters of their published rules, never voices** (`../studio-roster.md`). A seat cites the rule it applies; it never imitates the person.

## Seats

| # | Seat | Rules it applies (published work) | Checks | Veto |
|---|---|---|---|---|
| 1 | **Structure** (Minto, *The Pyramid Principle*) | answer first; SCQA opening; each section groups ideas that are MECE and sit under one governing idea; vertical "why/how" and horizontal logic | Can the title + first paragraph + section headings alone carry the argument? Does each section answer one question the previous one raised? | the reader has to reach the end to learn the point |
| 2 | **Data story** (Knaflic, *Storytelling with Data*) | context first (who, what, how); one point per chart; declutter; focus attention with one accent; a chart title that states the takeaway | For each number and figure: what should the reader do or believe after seeing it? Is the comparison (baseline, before/after) on the page? | a number with no baseline, or a figure whose point is not stated |
| 3 | **Graphic honesty** (Tufte, *The Visual Display of Quantitative Information*; Cairo, *How Charts Lie* / *The Truthful Art*) | data-ink ratio; lie factor = 1; no chartjunk; show the data; truthful, functional, insightful; is the chart showing the right measure, at the right scale, with its uncertainty? | Axes, scales, cut-off ranges, cherry-picked windows, a median shown without its spread, a diagram that implies something the system does not do (a merge line) | a figure that would mislead a careful reader |
| 4 | **Perception** (Kosslyn, *Graph Design for the Eye and Mind*: relevance, appropriate knowledge, salience, discriminability, perceptual organization, compatibility, informative changes, capacity limits) | at most ~4 chunks per figure; the most important thing is the most salient; labels close to marks; greyscale and 360 px still readable | Read each figure at phone size in 2 seconds: what do you see first? Is it the point? | the salient element is not the point |
| 5 | **Engineer clarity** (Julia Evans, her posts and zines) | one question per post or section; concrete example before abstraction; define every term on first use; say what surprised you or confused you; show the command and its real output | Mark every undefined term and every claim without a runnable example. Would a mid-level engineer try it tonight? | jargon a working engineer cannot decode, or a "how" with no example |
| 6 | **Reader and voice** (Ann Handley, *Everybody Writes*) | reader first ("so what?" after every paragraph); specific beats general; cut the throat-clearing opening; one idea per paragraph; plain words; a clear ending that says what to do | Mark paragraphs that serve the writer, not the reader; vague words; a weak first and last line | the opening does not earn the second paragraph |
| 7 | **Domain truth / fact-checker** (per post: e.g. a Postgres + IaC expert, a Lakebase DBA, an HLS clinician) | open the real repo, `docs/CATECHISM.md` and the evidence files READ-ONLY; every claim must match its evidence exactly (number, unit, conditions, date); flag any claim whose wording is stronger than its evidence; flag product status (GA/Preview) older than 30 days | For each [Cnn]: open the evidence file and quote the line that backs it. List claims with no tag, wrong tag, or stale status | any claim the evidence does not support as written |
| 8 | **Skeptic** (the post's named skeptic from CATECHISM Q4: a competitor's engineer, a senior DBA, a buyer) | what would you screenshot to mock? what did the author leave out? | The one sentence they would attack, and what is missing (cost, failure mode, limit) | a claim a competent skeptic can refute in one reply |
| 9 | **Skimmer** (phone, LinkedIn feed, 2 seconds) | title, image, first line only | What do you think the post is about after 2 s? Would you tap? | the first screen does not say what the post is about |

Add a seat when the post needs it: **SEO/discoverability** (title states the query a reader types; headings are questions; alt text), **Accessibility** (alt text, contrast, colour-only meaning), **Legal/comms** (disclosure line, customer names, unreleased features).

## What each seat receives

`BRIEF.md` on the board: the outline or draft path; `docs/CATECHISM.md` (Q1 goal, Q4 persons, claims table); `DECISIONS.md` standing rules; the figures' paths; the outlet and limits (Medium deep dive ≤ 2,500 words, LinkedIn teaser); the bar ("a post a senior engineer forwards to their team"). Read-only; no live calls except the fact-checker, which may re-run a read-only check if the CATECHISM row names one.

## YAML each seat returns

```yaml
agent_name: "<seat>"
status: complete
score: <1-10 against the bar>
one_change: "<the single change that would most improve the post>"
findings:
  - id: "<seat>-1"
    where: "<section heading or line>"
    severity: HIGH | MED | LOW
    problem: "<one or two sentences>"
    rule: "<the published rule or CATECHISM row it rests on>"
    fix: "<exact replacement text or structure>"
```

## Coordinator after each round

1. Verify each HIGH against the repo and claims; record dispositions in `reviews/SYNTHESIS-round{n}.md` (accepted / in part / resolved by verification / rejected + reason).
2. Edit the tagged source only; re-run EVERY gate; regenerate the publish copy.
3. Round 2: resume the same seats with the synthesis; they check their own HIGHs and look for new problems.
4. **Done when** a round ends with 0 surviving HIGH and every gate exits 0 on the final source.
