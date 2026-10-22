---
name: house-style
description: The user's personal house style for anything visual or presented, including slides, decks, dashboards, data visualizations, documents, web pages, apps, UI, posters, and design briefs. Read this before designing, styling, laying out, or critiquing any visual output, and every time the design-brief or atelier skills run. It takes precedence over their defaults, and it requires every design brief to learn from references, starting with Information is Beautiful. Use it whenever the user asks for something that will be looked at, even if they never say "house style," and whenever they ask whether a design is good. For the words on slides, captions, and any other visual, the writing-style skill governs; for anything that moves, the motion-style skill governs.
---

# House style

Five rules and one break rule, drawn from an interview about 25 things the user loves and 7 they dislike. Every quotation below is the user's own words. The rule statements were drafted by Claude from those words and approved by the user.

Apply the rules to every visual decision. Where they conflict with another skill's defaults, including design-brief and atelier, these rules win. If a deliverable has explicit brand guidelines (a company or customer template), follow those for color and type, keep the other rules, and briefly note any conflict to the user.

This skill governs how things look. The writing-style skill governs the words on them, including slide titles, captions, and speaker notes. The motion-style skill governs how anything moves, and it inherits this skill. Which skill runs when: atelier's "The skill map".

## Baselines

Before anything ships, it passes both of the user's baselines:

- The tomorrow test: no unearned familiarity, no oversharing, no feigned personableness, "so I am not cringing when I read it tomorrow."
- The joy test: "I need to be proud of what I did, and it needs to spark joy in me."

## Floors

These outrank the five rules, the break rule, and any brand guidelines. Verve never breaks legibility or meaning.

- Contrast: body text at least 4.5:1 against its background. Large text (24px and up, or 18.66px and up bold) and chart marks at least 3:1.
- Robustness: every figure still reads in greyscale and for color-blind readers.
- Locked meanings: where a deliverable's grammar fixes a color's meaning (for example, red means only "changed production" in the branching kit), that meaning holds everywhere in the piece. The grab-me moment then uses size, scale, or space, never the locked color.
- Surfaces: feeds and phones compress images and may show them in dark mode. Use a solid ground there, never transparency. Tinted pales are fine on slides and web pages; check them after compression.

## How to use this skill

1. Before designing, read the floors and all five rules, choose the narrative shape for the piece (see "Narrative shapes"), and decide where the single grab-me moment goes, if anywhere.
2. Design.
3. Before presenting, check the floors, then run each rule's check against the output. Fix failures; don't just report them.
4. When a case is ambiguous, read `references/record.md` for the full interview, and decide from the user's own words.
5. When writing a design brief, consult references first, starting with Information is Beautiful. See "Learning from references" below.

The "In practice" lines are Claude's translations of the rules into screens, slides, and documents. They are starting points, not the rules themselves. When an "In practice" line seems to fight the rule above it, follow the rule.

## 1. Everything breathes

Give every element room. Nothing fights for attention, and the pacing is deliberate so the reader can think.

The user's words: "Everything breathes." "No elements fighting, everything in its place." "It gets me calm and I pay attention to everything." "Lets the story breathe, lets me think." "Pacing, spacing." "Negative space."

In practice: generous margins and whitespace; one focal point per slide, screen, or section; separate groups with space rather than boxes and rules; one idea per slide; deliberate transitions, no rapid cuts.

Check: Name the one thing the eye lands on first. If anything competes with it, or any region feels cramped, fix it.

Not this: "Clutter and things fighting for attention" (Amazon). Grids that "don't space well" (PowerBI).

## 2. Verve, not beige

Anything people look at actively gets real, brilliant color, used as pops against a sparse ground. Pale tones are never uniform; they carry shades of light. Restraint is only for things people look through.

The user's words: "In a world where beige is considered respectable, here he is showing a verve for life." "Sparse, but very interesting pops of color." "Their pales are not uniform, they show shades of light." Of pastels in a hard-edged grid: "I do not see pastels working in the sharp lines." Of the Leica: "the rangefinder I am looking through."

In practice: when a colour round or an owner decision has set the palette, it wins; otherwise motion-style's token file is the tested default for films and explainers. At least one brilliant color doing real work on every slide, page, or dashboard; a sparse ground so the color pops; tinted, varied neutrals instead of flat beige or gray; pure, saturated color when the structure is crisp and hard-edged, never pastels on sharp lines; quiet chrome and controls, so the content gets the color.

Check: Is a brilliant color doing work here? Is any large area flat beige or gray-on-gray? Are the pale areas varied, or uniform?

Not this: "Absolute lack of colors" (Databricks workspace). "No fucking color" (PowerBI). "The beige," "trite and sterile" (modern interior design).

## 3. A few captions

The story makes sense with a few captions. Reveal it progressively, and always show where we are, where we came from, and where we're headed.

The user's words: "The story makes sense with just a few captions." "REDUCED COGNITIVE LOAD." "Progressive disclosure." "I don't have to hold too many things in my head at once, or my customers." "I can deliver and hold the attention of my customers better this way." Of Information is Beautiful, a "huge reference": "Illuminating," chosen for showing facts together with their connections, context, and relationships.

In practice: every label names what it marks, so a state such as "Not copied" always says what it applies to, as in "No row-level security"; headlines that carry the story on their own; detail revealed in order, one layer at a time; orientation always visible (progress, section markers, "you are here"); every number shown with the context that gives it meaning, such as a comparison, a trend, or a relationship; direct labels on charts instead of legends; few choices on screen at once.

Check: Read only the headlines and captions. Does the story hold? Count how many things the viewer must keep in mind at once, and cut that number.

Not this: "Option paralysis" (Databricks workspace). "Unfocused and unintuitive" (Salesforce).

## 4. A vision behind it

Disparate parts flow into one meaningful whole. Nothing is adornment for its own sake. Useful is the floor, not the goal; the result should also be beautiful.

The user's words: "There's a vision behind it and the disparate items flow together and it is beautiful." "Making unrelated parts a holistic, meaningful whole." "In itself an object and act of beauty." "What fun is a wholly utilitarian world." Of a grid with its structure removed: "just random looking."

In practice: one governing idea every element serves; a shared system of grid, palette, and type so charts, images, text, and code feel like one piece; structure strong enough to hold the composition (clear grid, firm lines, symmetry where it helps).

Check: State the vision in one sentence. For each element, ask what breaks if it is removed; if nothing breaks, cut it. Look for any area that reads as random.

Not this: Tacky, which the user defines as "trying too hard to be cool, unnecessary adornments, look-at-me design that screams with no utility." "Unimaginative, derivative" (cookie-cutter suburbs).

## 5. No corners cut

It should feel like a serious piece of work: consistent, reliable, and finished down to the details.

The user's words: "No plastic, no corners cut." "Sheer faith that this is a serious piece of work." "Consistent and reliable." "Industrial design and workmanship." "Quality." "Heft." "Solidity."

In practice: consistent spacing, alignment, and type scale; the same element looks the same everywhere; aligned numbers and real content, never placeholders; nothing that looks flimsy or unfinished.

Check: Inspect the edges and details: alignment, spacing, repeated elements, numbers. Anything inconsistent gets fixed before presenting.

Type the user has named, described as "clean, calm": IBM Plex Sans and IBM Plex Mono first, Helvetica as the fallback. On the web, use a stack such as `"IBM Plex Sans", "Helvetica Neue", Helvetica, Arial, sans-serif`, since Helvetica itself isn't web-hosted.

## Break rule: the grab-me moment

Once per piece, on purpose, break the calm with something in-your-face. It has to invite, never scream with no utility.

The user's words: "In-your-faceness." "Exciting and inviting." "A slap in the face, grab-me moment." "Visceral." "Wild."

In practice: one deliberate jolt, such as a full-bleed field of brilliant color, an oversized number, or a striking image, placed where the story needs it most.

Check: There is at most one, and you can say why it is there. If it only decorates, it is tacky, not a grab-me moment.

The "once per piece" limit was Claude's addition, approved by the user.

## Narrative shapes

Choose the order of a piece deliberately, by what it is. Take each shape's structure, never its register: the user rejected inspirational uplift as "pandering" in the writing interview.

| Piece | Shape | Source |
|---|---|---|
| Customer decks | Alternate between how things are today and how they could be, shifting the weight toward the proposal | Nancy Duarte's sparkline |
| Internal decks and documents | Situation, complication, question, answer; the answer leads and everything else supports it | Barbara Minto's Pyramid Principle and SCQA |
| Apps, dashboards, demos | A short guided path first, then open exploration | Segel and Heer's martini glass |
| Any deck, optionally | One slide where the audience guesses before the reveal | Hans Rosling's quiz; the Upshot's "You Draw It" |

A guess-then-reveal slide counts as the piece's grab-me moment, so a deck has at most one of either.

In a before-and-after piece, the thesis goes on the opening and closing title cards, not in a running header, because a thesis is true for only part of the story.

Check: Read only the slide titles or section headings. They should tell the whole story in order (Cole Nussbaumer Knaflic's test, and rule 3's).

## Learning from references

Every design brief draws on references for techniques worth learning from. References are sources of technique, never templates, and the five rules above govern everything taken from them. If a technique conflicts with a rule, the rule wins.

There are two kinds of reference: live sources, which are opened on the web during the brief, and knowledge references, which are drawn from what you already know.

### Live sources

Always check Information is Beautiful, which the user calls a "huge reference." The list below is a starting point, not a limit. Then search the open web for the best sources for this brief's form, domain and audience, and use whichever genuinely fit. Prefer sources the audience already trusts (for a clinical chart, journal and methods-handbook guidance; for a deck, a design system or visual journalism team that solved the same chart form), and sources that explain their reasoning over galleries. There is no fixed number of sources; open as many pieces as genuinely relate, usually three to eight in total. A source that matches both the form and the audience beats one that matches only one of them.

- Information is Beautiful (https://informationisbeautiful.net): context, meaning facts shown with their connections, comparisons, and relationships. Search with `site:informationisbeautiful.net <subject or form>`, or start from the blog (https://informationisbeautiful.net/blog) and interactive graphics (https://informationisbeautiful.net/interactive). The homepage renders mostly navigation when fetched as text, so go through search results or specific pages.
- The Pudding (https://pudding.cool): visual essays and scrollytelling. Best for narrative pacing and progressive disclosure (rule 3). Its how-to guides are at https://pudding.cool/topics/#how.
- FT Visual Vocabulary (https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md): chart types organized by the relationship to show. Use it to pick the chart form.
- Data Sketches (https://www.datasketch.es), Nadieh Bremer (https://www.visualcinnamon.com), and Shirley Wu (https://shirleywu.studio): crafted, colorful custom visualizations with documented process and code. Best when the brief calls for a bespoke visual rather than a standard chart.
- Federica Fragapane and Giorgia Lupi: brilliant color, organic forms, and data treated as an object of beauty (rules 2 and 4). Find current work by searching their names; don't guess URLs.

Process:

1. Search for the brief's subject and form, in the listed sources and on the open web, and open the pieces that genuinely relate to the brief. Record what was searched, so a thin result is visible.
2. Look at how each piece shows context, and at its structure, labeling, pacing, and use of color.
3. Take techniques, not designs. Do not reproduce a specific graphic, its layout, its illustrations, or its branding. Name the source of every technique taken.

### Knowledge references

Draw on what you know of these works for principles. Name the source when you apply one.

- Edward Tufte, *The Visual Display of Quantitative Information* and *Envisioning Information*: data-ink, small multiples, integrating words and graphics, and color used sparingly for emphasis.
- Stephen Few, *Show Me the Numbers*: table and chart design for business data.
- Cole Nussbaumer Knaflic, *Storytelling with Data*: decluttering, focus, and narrative structure for presentations. Best for customer decks.
- Alberto Cairo, *The Functional Art* and *How Charts Lie*: function and beauty together, and honesty in charts.
- Josef Albers, *Interaction of Color*: how a color changes with its neighbors; the theory behind "pales that show shades of light."
- Giorgia Lupi and Stefanie Posavec, *Dear Data*: personal, hand-crafted data humanism.
- Nancy Duarte, *Resonate* and *DataStory*: the alternation between what is and what could be.
- Edward Segel and Jeffrey Heer, "Narrative Visualization: Telling Stories with Data" (2010): author-driven versus reader-driven stories, and the martini glass.

Two limits apply:

1. Your knowledge is reliable for principles, not for specifics. Do not quote these authors, cite page numbers, or describe a specific figure or project from memory. If a specific example matters, find and open it live, or describe the principle in your own words instead.
2. Tufte's and Few's restraint passes through rule 2. Their muted grounds are fine; colorless results are not. Keep at least one brilliant color doing real work.

### In the brief

Add a short section titled "Learning from references" containing:

- Live: each page consulted (title and URL), the technique taken, how the design will use it, and the house-style rule it serves.
- From knowledge: each principle applied, its source, and the rule it serves, labeled "from knowledge, not checked live."
- Left out: anything deliberately not taken, and why.

If nothing fits, say so in one line, with what was searched. Don't force a borrowing. If web access is unavailable, state that, use knowledge references only, and never describe pages that were not actually opened.

## Provenance

- All rules approved by the user in the interview session.
- Rothko's "depths" was explained by options Claude offered (soft edges, layered washes, scale); the user chose all three.
- Information is Beautiful's "context" was chosen from options Claude offered; "illuminating" and "huge reference" are the user's words.
- The "Learning from references" section was added at the user's request: check Information is Beautiful and other live sources, draw on well-known works from knowledge, and keep the house style on everything else. The source list was proposed by Claude and accepted by the user. On 2026-10-16 the user widened it: the list is a starting point, and each brief searches the open web for the best sources that fit, with no fixed cap (the old rule allowed at most two more from the list).
- The "In practice" lines are Claude's interpretation and have not been reviewed item by item. Revise them as real outputs are judged.
- The floors came from a review by the user's coding agent; the wording was drafted by Claude and approved by the user.
- The font order and web stack were approved by the user.
- The narrative shapes were researched with the user in session and approved by them.
- The baselines were approved by the user and are shared with the writing-style and motion-style skills.
- The label rule and the title-card rule came from the first explainer build and were approved by the user.
