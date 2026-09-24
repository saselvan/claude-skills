# Brief template — paste as message 1 in a new Claude Design project

Fill every bracket from stages 1–3. Delete any sentence that prescribes an element. Attach the content contract and any decided ADRs; do not attach visual references from a sibling product unless you want its brand to leak.

---

You are the lead product designer on this. I am not going to tell you what it should look like. I am going to tell you what it is, who it is for, what bar it has to clear, whose work it should stand in the lineage of, what is already decided, and the handful of things it must never do. Then I want you to turn this into your own design prompt, ask me whatever is ambiguous, and only then start drawing.

## Non-negotiables

These are the only hard rules. Each states the failure it prevents. Everything not on this list is your call. If you think one of these is wrong, argue with me before you comply.

1. [Testable statement] — [failure it prevents].
2. …
(5–8 items. Include: domain colour collisions, accessibility floor for this population, claims the system cannot back, content the data model does not hold, leaks the privacy model forbids.)

## What this is

[Two or three plain paragraphs. What the product does, in the user's words. What it deliberately refuses to do. The one flow that matters. If it hides things from some users, say what is hidden and what is shown instead.]

## Who it is for

[People, not roles. Age, eyesight, lighting, device, how many minutes they have, what they are trying to do in the room they are walking into, what tools they live in all day and what those tools have done to them. If there is a secondary audience, name it and say the primary wins.]

## The bar

[Four to six qualities the result must have, each one sentence, each observable. e.g. "Calm: one question answered per screen." "Trustworthy on sight: before reading a word, it signals someone careful made this." "Honest: when a field is unknown, the design says so rather than showing a blank or a default."]

## The lineage

I want this to belong to a tradition. Read these (or bring what you know of them) and let them shape your choices. Do not imitate any one; synthesize.

[Group by the problem they solved, not by fame. Six to twelve entries. One line each on why they matter to *this* product. Include at least one public design system built for a similar audience, and say what to study in it.]

[Contemporary references, for feel, not for copying: three to five, one clause each.]

## What is already decided

Read the attached [contract / ADRs]. They constrain content, not visuals: which fields appear, in what order of importance, and what never appears. Layout, type, colour, spacing, motion, and component shape are yours.

[If there is an existing sibling product: state the relationship in one sentence — shared brand, shared language but different register, or deliberately different — and why. If trust or status signals must be recognisably the same across both, say that.]

## The states you must design

[List every screen *and state*: empty/first-run, results, zero results, degraded, each object type, the hidden/restricted case as seen by someone without access and by someone with it, pending/declined/failed, long values, mobile. Name the ones that need a decision from me rather than a guess, and I'll decide.]

## Mock data

[Paste the mock-data rules. Ask for a blind export (no captions, no inventory) as a separate file from the first export onward.]

## What I want from you first

Do not draw yet. Turn this brief into your own design prompt: the goal, the audience, the layout logic you intend, the content hierarchy you take from the contract, and the influences you are actually going to lean on. List every ambiguity you see and ask me. Then propose how you want to work through it. (My default is three genuinely different whole-page directions for the primary screen first; you may disagree.)

**Attachments:** [contract]; [decided ADRs]; [design-system reference URL if any].
