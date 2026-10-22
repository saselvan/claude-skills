# Storyboard template — stage 3b, before any layout

The storyboard decides order, emphasis and the eye path. The designer decides space, type and colour later.
Write it in greyscale words and boxes. The owner approves it before the brief goes out.

## 1. Message hierarchy (one page max)

- **Claim** (quoted, with its source path): [one sentence]
- **Level:** feature | product | platform
- **Reason 1:** [one sentence] — proof: [observed result or log path] — honest limit: [one sentence]
- **Reason 2:** …
- **Reason 3:** …

A reason without a proof is a hope. A reason without a limit reads as marketing to a skeptic.

## 2. Frames (six to eight, one idea each)

| # | The one claim this frame carries | Eye lands 1st / 2nd / 3rd | What moves, and why (cause and effect only) | Proof shown (live, or log path) | Behind a click | The one number |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

Check each frame:
- It traces to the claim. If it only explains a mechanism, it belongs behind a click.
- Its order implies no false cause (see "Sequence is a claim").
- It holds at most one number, and that number has the same value in every frame.
- For a platform claim in a **deck or blog**: one frame pictures the real "before" system (boxes, pipelines, credentials and control planes, counted from a real source), and one shows the same job inside the platform.
- For a platform claim in a **demo**: no architecture picture. The platform shows up through this turn's observed steps, each labelled with the part that did it. A motion slot fills only after its trace event; a step that did not run says so.
- Each frame attributes a failure only to a baseline that actually ran.

## 3. Wireframe

Greyscale boxes and real words at a 1440×900 first screen. Number the eye path on it. Nothing below the fold may be needed to understand the claim.

## 4. Cut list (when a previous version exists)

| Element | Keep / drawer / delete | Reason (one line) |
|---|---|---|

## 5. Naming list

One name per concept, matched to the domain glossary. Mark internal words (layer names, persona labels, method names) "never on screen".

## 6. Claim tests (logged before the owner sees it)

- First-screen gate: viewport-clipped capture at 1440×900, `scrollY = 0` → pass / fail.
- 5-second test: three personas' one-sentence answers, verbatim → x of 3 repeat the claim at its level.
- First-click test: where each one would click for proof.
