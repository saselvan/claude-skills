# CATECHISM.md — template (Heilmeier, adapted for agent-built work)

Answer in order, in a file, before any tool opens. One decision at a time if run as an interview. Tier 1 work answers only Q1 and Q8.

## Q1. What are you trying to do?
No jargon. Two or three sentences a smart outsider would understand. If you can't write this, no agent can build it.

## Q2. How is it done today, and what are the limits?
The incumbent practice and its specific pain. This becomes the agent's *why* and quietly shapes a hundred small decisions.

## Q3. What's new in your approach, and why will it succeed?
Extract the **non-negotiables** here: the 5–8 rules that distinguish this from the default the tools would produce. Each testable, each naming the failure it prevents. Any comparative/competitive claim gets verified before it becomes a rule, with the verification date in the rule.

**Claims inventory.** List every claim the artifact will make about how the system works: architecture, data, privacy, and comparisons. Include the ones that will only live in UI copy, diagram labels, or captions. For each one, write the claim, its evidence and grade, the date it was verified, and the exact true wording.

Evidence grades, strongest first:
1. **A check you ran:** the command or query, its output, and the date.
2. **Code or schema you read:** the file path, plus the line or object.
3. **Official product documentation:** the URL, the version, and the date read.

Anything below grade 3 is **not evidence. It is a lead.** That includes research notes, blog posts, sales or positioning wording, and another AI's output. **A research note written by an agent is agent output.** Citing it as proof is one agent citing another, laundered through a file. A claim that has only a lead is marked **UNPROVEN**. Before build, it is either verified up to grade 1–3 or cut from every artifact. It is never softened into weasel wording ("effectively one governance plane"), because that is how unproven claims survive review. Mark tempting overclaims next to their true form ("one copy" → "a managed mirror"; "same permissions" → "same catalog, same lineage"). This table goes into the design brief's non-negotiables word for word. An unverified claim may not appear in any artifact.

## Q4. Who cares? What difference does it make?
The user as a **person**: age, eyesight, lighting, device, minutes available, what they've been burned by. If the audience contains an expert, name them and name the artifact they will falsify.

A demo has **two audiences**: the persona inside the story (the patient finding a doctor) and the room watching it (the architect judging the platform). Name both. The room's expert is the named skeptic, and the claims inventory (Q3) is what they will check.

## Q5. What are the risks?
Always include the agent-work four: (a) the agent claims done when it isn't; (b) the data model can't support the design; (c) the demo data misleads; (d) the security model is decorative. For (c), check both directions: synthetic values that look measured (identical counts, one fixed date behind a "last 24 months" label), and **real identities next to synthetic facts** (real names beside made-up volumes). **Each risk maps to a named gate in the plan** — a risk without a gate is a wish.

## Q6. How much will it cost?
Sessions and money. Budget expensive runs (ultracode, large panels) explicitly.

## Q7. How long will it take?
Phases, each labelled **attended** or **unattended**. The 4 AM problem is mostly phases that needed a human, discovered to need one at midnight.

## Q8. What are the mid-term and final exams?
**Executable checks only.** "All S-tests green against the live branch; audit zero; panel unanimous" is an exam. "High quality" is not. The mid-term is the checkpoint (prove the machinery on one piece); the final is the stop condition. If Q8 cannot be written, the project is not ready to start — that is the answer, and it's a useful one.
