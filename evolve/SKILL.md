---
name: evolve
description: "Auto-research loop for self-improving Claude Code skills. Hill-climb any skill using binary evals. USE WHEN evolve, improve skill, optimize skill, auto-research, self-improve, benchmark skill."
---

# Evolve

Auto-research applied to individual Claude Code skills. Based on Karpathy's auto-research methodology: hill climbing with git as state manager, binary evals as the metric, baseline/challenger as the selection mechanism.

**Core principle:** Prompts are noisy distributions. You cannot evaluate a skill by running it once. Run it N times, score with binary evals, compare medians. Only keep improvements.

---

## /evolve {skill-name} [--runs N] [--rounds R]

### Defaults
- `--runs 5` (executions per variant — enough to average out noise)
- `--rounds 3` (challenger attempts before stopping)

### Prerequisites
- Target skill must be in `~/.claude/skills/{skill-name}/SKILL.md`
- Eval file must exist at `~/.claude/skills/{skill-name}/evals.md` (generate with `/evolve evals`)
- Git must be initialized in `~/.claude/` (for baseline/challenger ratchet)

---

## Step 1: Load

```
1. Read ~/.claude/skills/{skill-name}/SKILL.md        (the "train.py" — what gets modified)
2. Read ~/.claude/skills/{skill-name}/evals.md         (the metric — what measures quality)
3. Git commit current SKILL.md as baseline if uncommitted
```

## Step 2: Baseline Run

```
For i in 1..N:
  1. Execute the skill with a representative input from evals.md
  2. Score output against every binary eval question
  3. Record: run_id, eval scores (0 or 1 per question), total score

Baseline score = median(total_scores across N runs)
Report: "Baseline: {score}/{max} (median of {N} runs)"
```

## Step 3: Generate Challenger

```
1. Analyze which evals the baseline FAILS most often
   → These are the weak spots to target
2. Generate a modified SKILL.md that addresses the weakest evals
   → Change instructions, add examples, reword guidance
   → Do NOT change the skill's purpose or scope
3. Save as SKILL.md (overwrite — git tracks the diff)
```

**Challenger generation constraints:**
- One conceptual change per challenger (isolate variables)
- Changes must be explainable in one sentence
- Never remove working instructions — augment or clarify them
- Log the hypothesis: "This change should improve eval X because Y"

## Step 4: Challenger Run

```
For i in 1..N:
  1. Execute the skill with the SAME inputs as baseline
  2. Score output against the SAME binary evals
  3. Record scores

Challenger score = median(total_scores across N runs)
```

## Step 5: Keep or Discard

```
If challenger_score > baseline_score:
  → git commit SKILL.md "evolve({skill-name}): {one-line hypothesis} [score: {old}→{new}]"
  → New baseline = challenger
  → Log win to ~/.claude/skills/{skill-name}/evolve-log.md
  → Report: "✓ Challenger wins: {old_score} → {new_score}. Committed."

If challenger_score <= baseline_score:
  → git checkout -- SKILL.md (revert to baseline)
  → Log loss to evolve-log.md
  → Report: "✗ Challenger lost: {challenger_score} vs baseline {baseline_score}. Reverted."
```

## Step 6: Repeat or Stop

```
If rounds_remaining > 0 AND score < max_possible:
  → Go to Step 3 (new challenger targeting remaining weak evals)

If score == max_possible OR rounds exhausted:
  → Report final summary
  → Stop
```

---

## /evolve evals {skill-name}

Generate binary evals for a skill. This is the measurement tool — get this right or nothing works.

### How to write evals

**Rule 1: Binary only.** Every eval is yes/no. No scales, no ratings, no "rate 1-10."

**Rule 2: Observable outcomes.** Evals judge the output, not the process. "Did the output contain X?" not "Did the agent think about X?"

**Rule 3: Cover the skill's purpose.** Each eval tests one aspect of what the skill promises to do.

**Rule 4: Include representative inputs.** Evals need test inputs that exercise the skill's range.

### Eval file format

```markdown
# Evals: {skill-name}

## Test Inputs
Inputs the skill will be run against during evolution.

### Input 1: {short description}
{The actual input/prompt to give the skill}

### Input 2: {short description}
{The actual input/prompt to give the skill}

## Binary Evals
Answer YES or NO for each. Score = count(YES) / total.

### E1: {eval name}
{Question about the output that can be answered YES or NO}
Example YES: {what a passing output looks like}
Example NO: {what a failing output looks like}

### E2: {eval name}
...
```

### Eval generation process

```
1. Read the skill's SKILL.md
2. Extract every promise the skill makes (explicit or implicit)
3. Convert each promise to a binary question about output quality
4. Generate 2-3 representative test inputs that cover the skill's range
5. Write to ~/.claude/skills/{skill-name}/evals.md
6. Present to user for review before running evolution
```

**Target: 8-12 evals per skill.** Fewer than 6 lacks discrimination. More than 15 adds noise without signal.

---

## /evolve status {skill-name}

Show evolution history from `~/.claude/skills/{skill-name}/evolve-log.md`.

```
Displays:
- Current baseline score
- Rounds run (wins/losses)
- Score trajectory (round-by-round)
- Winning hypotheses (what changes stuck)
- Losing hypotheses (what changes didn't help)
```

---

## evolve-log.md format

Auto-maintained per skill. Append-only.

```markdown
# Evolution Log: {skill-name}

## Round 1 — {date}
- **Hypothesis:** {one sentence}
- **Change:** {what was modified in SKILL.md}
- **Baseline:** {score}/{max}
- **Challenger:** {score}/{max}
- **Result:** WIN/LOSS
- **Commit:** {sha} (if win)

## Round 2 — {date}
...
```

---

## Constraints

- **Never evolve design-ops itself.** The orchestration pipeline is too slow for hill climbing. Evolve leaf skills only.
- **Never modify evals during evolution.** Evals are the fixed ruler. If evals are wrong, fix them between evolution runs, not during.
- **One skill at a time.** Don't run parallel evolutions — git state conflicts.
- **Human reviews wins.** After evolution completes, user should read the diff of all winning commits to verify the changes make sense. Auto-research finds local optima — human judgment catches nonsense that scores well.
- **Eval quality > run count.** Bad evals with 100 runs produces garbage. Good evals with 5 runs produces signal. Invest time in `/evolve evals` first.

---

## Example Session

```
User: /evolve art --runs 5 --rounds 3

Claude:
Loading skill: art
Loading evals: ~/.claude/skills/art/evals.md (10 binary evals)
Committing current SKILL.md as baseline...

── Baseline Run (5 executions) ──
Run 1: 7/10  Run 2: 8/10  Run 3: 7/10  Run 4: 8/10  Run 5: 7/10
Baseline score: 7/10 (median)
Weakest evals: E3 (negative prompt included: 2/5), E7 (output path organized: 3/5)

── Round 1: Challenger ──
Hypothesis: Adding explicit "ALWAYS include negative prompt" rule will improve E3
Change: Added mandatory negative prompt step to Generation Workflow
Running 5 executions...
Run 1: 8/10  Run 2: 9/10  Run 3: 8/10  Run 4: 8/10  Run 5: 9/10
Challenger score: 8/10 (median)
✓ Challenger wins: 7 → 8. Committed. (abc1234)

── Round 2: Challenger ──
Hypothesis: Adding output path template with auto-naming will improve E7
Change: Added "Auto-name files as {subject}-{style}-v{n}.png" to Output Organization
Running 5 executions...
Run 1: 8/10  Run 2: 8/10  Run 3: 9/10  Run 4: 8/10  Run 5: 8/10
Challenger score: 8/10 (median)
✗ Challenger lost: 8 vs baseline 8. Reverted.

── Round 3: Challenger ──
Hypothesis: Adding "check model compatibility" step will improve E9
...

── Evolution Complete ──
Final score: 9/10 (was 7/10)
Rounds: 3 (2 wins, 1 loss)
Review commits: git log --oneline abc1234..def5678
```

---

*"Evals are the spec. The skill is the implementation. Evolution is the compiler."*
