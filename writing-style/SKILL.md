---
name: writing-style
description: The user's personal writing style for prose published or shared under their name, including LinkedIn posts, Medium articles, personal blog posts, Databricks blog drafts, slide text and speaker notes, and internal documents such as account theses and memos. Read this before drafting, editing, tightening, or critiquing any of these, even if the user never says "my style" or "my voice." Also use it whenever the user asks whether a draft sounds like them, sounds like AI, or reads as cringe. For slides, the house-style skill governs the visuals and this skill governs the words. For captions in animation, this skill governs the words and the motion-style skill governs their timing.
---

# Writing style

Five rules, one break rule, a set of mechanics, channel rules, and floors, drawn from an interview about 18 writers the user loves, 5 things they dislike, 6 pieces of their own work, and 21 side-by-side rewrite tests. Every quotation below is the user's own words. The rule statements were drafted by Claude from those words and approved by the user.

One line frames all of it: "Envy is ignorance, imitation is suicide." The style learns from the writers the user loves and never imitates any of them.

## Baselines

### The tomorrow test

"Never go with unearned familiarity, oversharing, and feigned personableness. That is the one tangible baseline I would go for, so I am not cringing when I read it tomorrow."

Read every draft as the user will read it tomorrow. Any line that is overly familiar, overshares, or performs warmth gets cut or rewritten. Both baselines outrank everything below except the floors.

### The joy test

"I need to be proud of what I did, and it needs to spark joy in me." If a draft is correct but the user wouldn't be proud to put their name on it, it isn't done.

## How to use this skill

1. Identify the channel and apply its row in "Channels."
2. Write the Big Idea first: one sentence that carries the whole argument. It becomes the title or the opening.
3. Choose the narrative shape for the channel (see "Narrative shapes").
4. Draft using the five rules and the mechanics.
5. Run each rule's check, then the tomorrow test, then the floors. Fix failures before presenting; don't just report them.
6. For internal documents, run the heat check.
7. When a case is ambiguous, read `references/record.md` and decide from the user's own words.

## 1. For brevity

Say it in the fewest words that still read smoothly aloud. Use short sentences and short posts, and name a pattern so it costs two words every time it comes back.

The user's words: "For brevity." "Can't read as too abrupt when read aloud, so the brain doesn't feel harried." "Uses fewer words." "Making the reader do too much work."

Check: Read the draft aloud. Cut any word that can go without loss. If a run of short sentences sounds clipped or harried, join two of them.

Not this: "Exhausted" (of Tolkien's description and pacing).

## 2. Every is a lie

Qualify each claim as precisely as the evidence allows, and never claim more. Every number is real and sourced. First person appears only to report an experiment the user ran and verified.

The user's words: "Every is a lie technically, because I am not omniscient." On first-person authority: "I just don't feel comfortable with that voice unless it is experiments I have done and proved for a fact."

Check: Find every absolute word (every, all, always, never, none). Each one must be provably true, or it becomes "usually," "most," or a specific count. Every number must have a source the user can name. If a number can't be verified, ask the user for it; never fill it in.

Not this: anecdote as evidence, or big theories on thin support (the user's reasons for disliking Tom Friedman).

## 3. More PD James than memoirist

In public writing, observe the subject. No "my read," no personal anecdote, no sentiment the piece hasn't earned.

The user's words: "Drifts into sharing territory rather than observing territory. Not a memoirist, more of a PD James." "This personalizing feels so unearned to me." "Never stuff like 'my read.'"

Check: Find every "I," "me," and "my." Each must report a verified experiment; otherwise rewrite it in the third person or cut it. Remove any appeal to feeling that the facts haven't earned.

Not this: "Pandering and LinkedIn thought-leadery." The humble brag: "gaping hole of validation."

## 4. Name it

Give the central pattern a name, put the thesis in the title, and put the user's name on it, so authorship is never in doubt.

The user's words: "I named it... and set it on the record that I named it." The user chose named concepts as what they value in Morozov and Tillich.

Check: Does the piece name its central pattern? Does the title state the thesis? On internal theses and articles, is the user's name on it?

## 5. Write for the skeptic

Write for the reader most likely to think "what a load of crock." Everything earns its place by being useful, and nothing reaches for a reaction.

The user's words: "That customer turned out to be the one I resonated with the most." "Truth to power."

Check: For each sentence, ask whether the skeptic would find it useful. Cut anything that fishes for engagement, flatters the reader, or performs insight.

Not this: "Naked grasping for responses" (engagement bait). "The complete lack of any utility" and "a beige wall trying to be profound" (AI slop).

## Break rule: punch up, once

One line of wit per piece is allowed, if it lands on a real absurdity in the industry. It never lands on the reader or a customer, and never comes from the vendor's seat.

The vendor's seat means writing on behalf of Databricks or to customers: the Databricks blog, customer decks, and customer-facing material. This interpretation is Claude's; the user approved the rule.

Check: At most one witty line. Its target is an industry absurdity, not a person. If the piece speaks for the vendor, cut it.

The user's support: Pratchett ("on the floor laughing"), Quinn (snark with substance, punching up), and Scocca's voice. In Test 4 the user rejected wit "only because" of how it lands from a vendor. Claude proposed this rule from that gap; it has the thinnest support of anything here.

## Mechanics

Each comes from a single rewrite test. In post repos, `tools/style_lint.py` (atelier's post kit) checks the ones a script can check.

- Open with the argument, not a scene. (The user notes that others advise the opposite; their own preference is the argument.)
- Use a plain register, never elevated or sentimental.
- Write prose. Never use lists in posts: "Screams AI."
- Use normal paragraphs. Never put one sentence per line.
- No parenthetical asides or digressions.
- Be literal in writing. Analogies belong only in slide speaker notes.
- Prefer a plain term to an acronym whenever one exists, such as "reporting tool" instead of "BI tool." Otherwise, expand acronyms for public readers: "Always good to expand on acronyms." Skip the expansion only for terms the audience uses daily: "They all know DBUs."
- Use a crafted title with a plain, descriptive subtitle.
- Allow at most one "X, not Y" construction per piece. Use em dashes rarely, if at all. Both are recognizable marks of machine-written text.
- Prefer concrete, real numbers to general statements.
- State the strongest opposing case in one sentence and answer it in one.

## Narrative shapes

The advice the user keeps hearing, to open with a scene, comes from the dramatic-arc tradition of Cole Nussbaumer Knaflic and Brent Dykes: build tension and hold the insight for the climax. The user's own preference comes from Barbara Minto's: present the answer first. Both are legitimate. Choose by channel.

| Channel | Shape | Why it fits |
|---|---|---|
| LinkedIn posts | Minto, compressed: the Big Idea as the title, then two sentences of support | Argument first, about 60 words |
| Medium and personal blog articles | Situation, complication, question, answer as the opening, then the evidence ordered so each point builds on the last | The insight is already in the title, so nothing is withheld |
| Customer decks | Alternate between how things are and how they could be, with at most one slide where the room guesses before the reveal | Real questions for the room |
| Internal documents | Situation, complication, question, answer, ending on what must happen next and who decides | The shape of the user's own account thesis |
| Databricks blog | Answer first, then support, ending on the call to action | Prescriptive, as the channel requires |

Three lessons apply everywhere:

1. Write the Big Idea sentence before anything else (Knaflic). It becomes the title, which is rule 4.
2. Never narrate the analysis in the order it happened (Dykes's most common failure). A how-to needs its steps, but the argument comes before them.
3. Take the structure, never the register. Duarte's endings lean on inspiration, which the user rejected as "pandering" in Test 3.

Check: Read only the title and the first sentence of each paragraph or section. Together they should make the whole argument.

## Channels

| Channel | Address | Ending | Notes |
|---|---|---|---|
| LinkedIn, Medium, personal blog | Third person | A statement, with no ask | LinkedIn posts around 60 words |
| Databricks blog | Third person | A call to action | Prescriptive; Databricks' editorial guidelines govern structure |
| Slides and speaker notes | "You," for teams the user has met | A real question for the room | Analogies allowed |
| Internal documents | Direct | What must happen next, and who decides | Heat check before sending |

When a post carries a video or an animated explainer, the post text adds what the video can't: the context, a source, or why it matters now. It never repeats the captions. The channel's length and ending rules still apply.

The general principle, confirmed across four tests: written for the public, observe from a distance; spoken to people the user knows, come closer.

## Heat check (internal documents)

Internal writing must stay measured; the author's frustration should never show.

Write internal documents as requirements and consequences: what must be true, who decides, and what waiting costs. Before presenting, flag sarcasm, loaded adjectives, and any sentence that assigns blame to a person, and offer a cooler rewrite of each. Keep the full argument; remove only the heat.

A model sentence from the user's own work carries frustration with no contempt in it: "Every time I treated it as architecture, the work landed and the ceiling stayed where it was."

## Floors

These outrank every rule, the baseline, and the channels.

- Accuracy: never invent numbers, quotes, facts, or experiences. If something is missing, ask.
- Never name an institution as a Databricks customer unless the user has confirmed it.
- No confidential figures, pricing, or internal names in public writing.
- Databricks' social media policy applies to anything public. The user supplies its specifics; don't guess them. Public posts carry the disclosure line from atelier's post standing rules: "I work at Databricks. All opinions are my own."
- On the Databricks blog, Databricks' editorial guidelines govern structure. Don't guess them either.

## Provenance

- All rules, the break rule, the mechanics, the channels, and the floors were approved by the user.
- Many of the user's reasons for loving specific writers were chosen from options Claude offered; see `references/record.md`.
- The break rule and the definition of "the vendor's seat" are Claude's proposals.
- The narrative shapes were researched with the user in session (Minto, Duarte, Knaflic, Dykes, Segel and Heer, Rosling, and the Upshot) and approved by them.
- The joy test was added later and approved by the user; it is shared with house-style and motion-style.
- The plain-term rule and the video-post rule came from the first explainer build and were approved by the user.
- Aligned with atelier's post kit on 2026-10-10, with the user's approval: the disclosure line, and the `style_lint.py` gate.
