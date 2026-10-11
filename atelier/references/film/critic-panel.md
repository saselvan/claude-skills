# The script panel: 10 seats plus Director/DP

Used on the Lakebase teaser scripts (clinical-va-appkit, board `.pipeline/blackboard-video-script-gauntlet/`, 2026-09-29). Round 1 found 20 HIGH, round 2 found 0, and round 3 was a light pass on the messaging deltas. Run the panel through the `blackboard` skill: one wave, every seat a fresh `general-purpose` agent, read-only (`writes_files: false`), with claim-honesty as the one `critical` stream. The coordinator alone edits and commits.

## Protocol
1. Write `BRIEF.md` (template below) to the board. Every spawn prompt is: *"You are the **{seat}** seat on a 10-seat critic panel. First read `{abs path}/BRIEF.md` in full and follow it exactly (read-only; final message = one YAML block; at most 6 findings)."* followed by that seat's charter. Use absolute paths everywhere.
2. The coordinator **verifies every finding against the code, the ledger and the design law before acting on it.** In round 1 the DBA seat said "37 is the `care_coordinator_reader` scope". That was false: the probe counts as `ward_clinician`, and Gate 2 uses a different role. Two storyteller "HIGH"s were resolved notes that said "no fix needed". One vocabulary HIGH misread a captionless hold as a caption slot. Record false positives with the reason, and never "fix" them.
3. Write `artifacts/SYNTHESIS-round{n}.md`: a score table (seat × film, HIGH count), a verdict, **HIGH findings with dispositions** (accepted / accepted in part / resolved by verification / rejected + reason), MED/LOW accepted, rejected with reason, and demo improvements logged (`DI-n`).
4. **Round 2: resume the same agents** (`SendMessage` to each agent id) with the synthesis path and the changed ledger rows. Don't spawn fresh ones: the seat has to check that its own round-1 HIGH findings are resolved. The message says: "Same charter, same hard rules, same YAML. Check that your round-1 HIGH findings are resolved. Do not re-raise a finding the synthesis rejected unless you cite new evidence. Look hard for new problems v2 introduced. 'Good enough' still fails."
5. **A zero-finding verdict needs its reasoning on the record.** When a domain seat returns no findings, send it its charter questions as a follow-up. In round 1 the CMIO seat scored 9/9 with no findings until it was asked.
6. **Light round** for small deltas (a messaging change): resume only claim-honesty, vocabulary-tone and product-marketer, and list the changed captions verbatim.
7. **Stop** when a round ends with 0 HIGH that survive step 2's verification. Then run the coordinator's mechanical gates (reading time, lint) over the final tables, and generate `acts.json` from them.

## BRIEF.md template
```markdown
# Critic brief — {product} teaser films, script gauntlet
Read this first. You are one seat on a 10-seat panel reviewing {N} short film **scripts** in parallel. You are read-only: do not edit, create or delete any file. Do not call any live app, Databricks API or Playwright.

## What is being made
{Each film: abs path to its script, its persona(s), with owner quotes}. Each is {length}, {sound}, works with the sound off, delivered {formats}. Visuals: real app screens (animated crops and camera moves), real repo code shots, and plain type cards for product facts. {Reach.}
Also read: the claims ledger {abs path}, and {abs path}/CATECHISM.md (Q3 non-negotiables, Q4 the persons). Background only (leads, not evidence): {runbooks, storyboard}.

## The bar
Score against Apple product films, Stripe Sessions, Linear launch films, Vercel Ship, Figma Config and Arc: calm, exact, confident, one idea per shot, real product UI, generous whitespace, precise easing. "Good enough" or "better than before" is a failing verdict. The current scripts, storyboard and screens are a floor, not a ceiling. If you find a better beat or screen treatment for the real demo app, record it as `demo_improvement`.

## Hard rules (every seat enforces them)
{Numbered: the floors of house-style, writing-style and motion-style; then every rule in standing-rules.md, then the forbidden stems (checks.md §1), the app's banned vocabulary, the visual law with hex values, the honesty note for anything planted, and: never name the engine or show an endpoint host; no real people or patient data (real public content, such as FDA label text, only with its source in the ledger; standing rule 1).}

## Official public messaging (grade 3, read {date})
{Headline, sub-headline, pillars, key claims, GA/Preview statuses. Internal messaging: {available / unavailable — flag anything you would want checked there}.}

## Severity
- **HIGH**: the named skeptic would stop trusting the film; a claim is false, unsupported or overstated; a hard rule is broken; or the film fails its person's core question.
- **MED**: clearly below the peers; weakens the film.
- **LOW**: polish.

## Your final message
End with exactly one YAML block. At most **6 findings**, ranked most severe first. Findings, not essays.
agent_name: "<your seat>"
status: complete
scores: {film_a: <1-10 vs the peers>, film_b: <1-10>}
one_change: {film_a: "<the single change that would most improve it>", film_b: "<...>"}
rule_checks: []   # Production designer and Director/DP only: one {rule, result: pass | fail, shots} per floor, rule and check of the skill the seat runs
findings:
  - id: "<seat>-1"
    film: A | B | both
    shot: "<shot id | structure>"
    severity: HIGH | MED | LOW
    problem: "<one or two sentences>"
    rule_or_peer: "<the hard rule, the ledger id, or the peer and what it does instead>"
    fix: "<exact replacement caption, beat or structure>"
    demo_improvement: null   # or {current, better, route_or_component, size: S | M | L}
```

## Seat charters
Each charter gives a person, the questions to judge, the **code paths to open read-only** (so the seat verifies rather than trusts), and a veto class. Named legends are **charters of published rules, never voices**: the seat cites the rule in `rule_or_peer` and never imitates anyone (`studio-roster.md`).

1. **app-dev.** A senior app developer on the customer's digital team (TypeScript/Python, Postgres daily), who reads literally and is allergic to marketing that hides the code. Would you forward the film to your team, and which caption would you screenshot to mock? Is it unmistakably the real thing (driver, SQL, extensions), and are the code shots meaningful? Open {the code-shot files and lines}. Is the developer loop visible (branch per idea, test, throw away)? Propose only additions a ledger row can back. Peers: Vercel Ship, Linear. *Veto:* anything a developer would call fake, hand-wavy or "no-code marketing".
2. **dba.** A senior Postgres DBA with 15 years of roles, RLS, migrations, PITR and replication. Checks every database statement for precision in front of other DBAs: "RLS is off" vs "not enabled and forced", what each gate tests and **under which role**, copy-on-write semantics, and what "only a reviewer role can apply it" means in the code. Open {gate, probe, promote and memory files}. Name the one database moment that would make a DBA lean in, if the demo really does it. *Veto:* any sentence a DBA would call wrong or sloppy.
3. **enterprise-architect.** Owns the reference architecture and chairs the review board. Has been burned by silos, nightly-ETL "integrations", identity bolted on afterwards, and lock-in. Does "one platform" hold for identity, governance and data flow? Is the data-flow story stated defensibly (GA parts only)? Are identity and access coherent (service principal, reviewer role, inherited permissions)? What would you ask the seller right after (recovery, HA, network, residency, cost), and does a `P` row back it? *Veto:* an architectural claim that would not survive your review board.
4. **product-marketer.** The product's PMM, who owns message consistency across every field asset. Checks one core message with three proof points (or a feature list?), differentiators landed or buried, the audience split, the title, end card, naming and call to action, and anything a competitor's marketer would enjoy attacking. Lists what they would want checked in internal messaging. *Veto:* an off-message claim, or a film that sells a feature instead of the product.
5. **comms-legends.** Applies published rules. **Duarte** (*Resonate*): the contrast between what is and what could be, the call to adventure, the STAR moment. **Heath** (*Made to Stick*): SUCCESs and the Curse of Knowledge. **Raskin** (strategic narrative): name the big change, show winners and losers, tease the promised land, present features as "magic gifts", show evidence. For each film: name the STAR moment or say it has none, find Curse-of-Knowledge captions for a first-time viewer, find missing contrast, and judge whether the opening earns the rest. Proposes exact replacement captions inside the ledger. *Veto:* a film with no memorable moment or no contrast.
6. **master-storytellers.** Breaks the frame. **Pixar** (Emma Coats' 22 rules, the story spine), **Ira Glass** (the anecdote, then the reflection), **McKee** (inciting incident, turning point, the gap between expectation and result), **Apple** film craft (show, don't tell; one idea per shot; stillness as emphasis). May propose **at most one** radically better structure per film (a beat list with times, ≤ 120 words, `shot: structure`). Names the single most powerful image the demo offers and says where a film is a list rather than a story. *Veto:* a film that is a list, not a story.
7. **buyer.** The customer's CIO (the economic buyer), with the CISO and CFO in mind. Writes the one sentence their people would use to defend the purchase, or says it can't be written. Gives the CISO's question and the CFO's question (for example "four extra databases, four bills?"), the risk each film reduces in business terms, which caption would embarrass the champion if it turned out false, and whether the call to action is right for a seller sending it. May add `defend_sentence_*`, `ciso_question` and `cfo_question` keys. *Veto:* anything that would embarrass the internal sponsor.
8. **cmio** (the domain-truth seat; swap in the domain's equivalent). A practising physician-informaticist with 20 years of EHR governance. Checks roles and scopes for realism, regulatory terms used without implying a compliance claim ("minimum necessary"), the synthetic persona's realism, and **every clinical number worked out by hand**. Give the seat the numbers to compute. *Veto:* any clinical statement a physician would call wrong, and any framing that trivialises patient safety or implies real patient data.
9. **claim-honesty** (the Integrity gate; `critical`; up to 8 findings). For **every** caption: find its ledger row (no row = orphan = HIGH); check the grade by opening the cited code read-only (a row that fails verification = HIGH); check the class (PRODUCT only on type cards; diagram cards show only what the demo runs); check the wording doesn't exceed the evidence, and list the riskiest captions verbatim for it to test. Flags any implication that a planted flaw was accidental, any measured time or cost the demo doesn't have, and any value the running app wouldn't produce. For a no-change claim, finds its paired change row (standing rule 15); for a caption number the screen also shows, checks that the row cites the capture (standing rule 3). Gives the exact safe wording as the fix. *Veto:* HIGH on any unsupported, unverifiable or overstated claim.
10. **vocabulary-tone** (the Content gate). Runs the `tone-check` skill on the on-screen captions only (RED = HIGH, YELLOW = MED), without letting it edit, and runs writing-style's floors, rules and mechanics on the same captions. Mechanically checks the forbidden stems (checks.md §1: leading word boundary, case-insensitive, so "instantly" and "captured" hit). Checks grammar and parallelism, term consistency across films (branch/fork/copy, gate/check, approve/apply, memory on/off), the mono rule from the app's nouns file, reading time per slot, and plain language (GOV.UK). *Veto:* any banned word, any jargon an outsider can't parse, any promise the system can't keep.
11. **director-dp** (added after the first film; seat it from round 1). Charter, six checks and veto: `director-lenses.md`. It also runs motion-style as written: the clocks, "Beats", the patterns, the never list and the floors. Like the Production designer seat, it returns `rule_checks`, in motion-style's own order: the floors, then each rule's check, then the baselines. It judges the shot list's screen column and editor notes in the script round, and the stills in the visual gauntlet.


## Production designer seat (added 2026-10-09)
Owns look and feel across the film, the app and the deck. Judges: inviting (at least one confident colour; not black on paper); one language (same few colours, shapes, type, motion mean the same thing everywhere); restraint with a signature; colour never carries state alone, red is errors only. Lineage to learn from, not copy: Apple, Teenage Engineering, Hasselblad, Braun/Dieter Rams. Colour changes go in their own round with a contrast table, and cover the app's states the film never shows (errors, refusals, empty and loading states, drawers), because the app wears a palette before the film reads it (standing rule 16). It loads and runs house-style as written, the way the post panel's seat 10 does: the Floors first, then each rule's Check and the break rule, on every shot, cited by name and never restated. Beyond its six findings it returns one pass or fail line per Floor and rule (`rule_checks` in the YAML), so the cap can't hide a failing rule. Project 3's draft 3 said "house style applied" while the checks for three rules failed.
