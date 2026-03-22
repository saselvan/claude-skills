---
name: evolve
description: "Auto-research loop for self-improving Claude Code skills. Hill-climb any skill using binary evals. USE WHEN evolve, improve skill, optimize skill, auto-research, self-improve, benchmark skill, run evals, measure skill quality."
---

# Evolve

Auto-research applied to individual Claude Code skills. Based on Karpathy's autoresearch methodology: hill climbing with git as state manager, binary evals as the metric, baseline/challenger as the selection mechanism.

**Core principle:** Prompts are noisy distributions. You cannot evaluate a skill by running it once. Run it N times, score with binary evals, compare medians. Only keep improvements.

**Key constraint:** The agent that generates the output MUST NOT be the same context that scores it. Use a fresh `claude -p` invocation for each execution AND a separate `claude -p` invocation for scoring. Same-context scoring inflates results because the scorer remembers what it intended, not what it produced.

---

## /evolve {skill-name} [--runs N] [--rounds R] [--dry-run]

### Defaults
- `--runs 3` (executions per variant — balances signal vs token cost; increase to 5 if scores are unstable across runs)
- `--rounds 5` (challenger attempts before stopping — more attempts to find improvements)

### Prerequisites
- Target skill must be in `~/.claude/skills/{skill-name}/SKILL.md`
- Eval file must exist at `~/.claude/skills/{skill-name}/evals.md` (generate with `/evolve evals`)
- Git must be initialized in `~/.claude/` (for baseline/challenger ratchet)
- `claude` CLI must be available (for isolated execution via `claude -p`)
- If the target skill depends on MCP servers, verify they're accessible from `claude -p` by running: `claude -p "list your available MCP tools" --no-input`. MCP servers configured in user settings should carry over, but project-scoped servers may not.

### Flags
- `--dry-run` — run ONE execution + ONE score + validate JSON parsing + check git status. No commits, no branch. Use this to verify the pipeline works before burning tokens on a full evolution.

### Pre-flight checks
Before starting, verify:
```
1. git -C ~/.claude/skills status       (clean working tree, or commit first)
2. which claude                          (CLI available)
3. Test: claude -p "echo hello" --no-input  (CLI responding)
4. Read ~/.claude/skills/{skill-name}/SKILL.md
5. Read ~/.claude/skills/{skill-name}/evals.md
6. Validate evals.md has: ≥1 test input, 6-12 binary evals, YES/NO examples
7. If skill uses MCP: claude -p "list your available MCP tools" --no-input
   → Verify the required servers appear in the output
```

### --dry-run mode

If `--dry-run` is set, run a minimal pipeline check and stop:
```
1. Run pre-flight checks (all 7 steps above)
2. Execute skill ONCE with Input 1 (isolated claude -p)
3. Score the output ONCE (isolated claude -p)
4. Parse the score JSON (strip preamble, validate with jq)
5. Report:
   - "Dry run complete"
   - Pre-flight: PASS/FAIL per check
   - Execution: produced {N} bytes of output
   - Scoring: JSON parsed successfully → {score}/{max}
   - Git: working tree clean / has uncommitted changes
   - MCP: {list of available servers} (if applicable)
   - Estimated tokens per full run: ~{execution_tokens + scoring_tokens} × {runs} × {inputs} × 2 (baseline + challenger)
6. STOP. Do not create branch, do not commit, do not run further rounds.
```

---

## Step 1: Load and Snapshot

```
1. Read ~/.claude/skills/{skill-name}/SKILL.md        (the "train.py" — what gets modified)
2. Read ~/.claude/skills/{skill-name}/evals.md         (the metric — what measures quality)
3. Create branch: git checkout -b evolve/{skill-name}/{date}
4. Git commit current SKILL.md as baseline if uncommitted
5. Initialize results log: ~/.claude/skills/{skill-name}/evolve-results.tsv
   Header: round | role | run | input_id | E1 | E2 | ... | EN | total | hypothesis
```

The branch isolates evolution work from the main skill. Like autoresearch, each evolution session gets its own branch.

---

## Step 2: Baseline Run

### Execution (isolated)

For each test input in evals.md, for each run 1..N:
```bash
# Execute skill in isolated context — the executor has NO knowledge of evals
# IMPORTANT: Tell the executor to OUTPUT the artifact directly, not call MCP tools.
# claude -p runs non-interactively — MCP tool approvals will block.
claude -p "You have access to the skill at ~/.claude/skills/{skill-name}/SKILL.md. \
  Read it, then complete this task: {test_input} \
  \
  IMPORTANT: Output the result directly as text with code blocks. \
  Do NOT attempt to call MCP tools (they are not available in this context). \
  Write the diagram/code/artifact inline in your response." \
  > ~/.claude/skills/{skill-name}/runs/baseline-input{I}-run{J}.md 2>/dev/null
```

**CRITICAL:** Redirect stderr to /dev/null (not stdout). Output goes to the file. This is directly from Karpathy's program.md — the agent redirects `train.py` output to `run.log` and reads only the metrics afterward.

### Render Hook (optional, declared in evals.md)

Some skills produce artifacts that need transformation before scoring. For example, diagram skills produce source code that must be **rendered to an image** before visual evals can be scored.

If evals.md declares a `## Render Pipeline` section, the orchestrator runs it between execution and scoring:

```bash
# Example: diagram skill render hook
# 1. Extract code block from execution output
CODE=$(sed -n '/^```/,/^```/p' runs/baseline-input{I}-run{J}.md | sed '1d;$d')
FORMAT=$(head -1 <<< "$CODE" | tr -d '`')  # e.g., "mermaid", "d2", "plantuml"

# 2. Render to PNG via deterministic tool (no LLM involved)
# Option A: Kroki public API (works for all formats)
curl -s -X POST https://kroki.io/${FORMAT}/png \
  --data-raw "$CODE" \
  -o runs/baseline-input{I}-run{J}.png

# Option B: mermaid CLI (local, Mermaid only)
echo "$CODE" | mmdc -i - -o runs/baseline-input{I}-run{J}.png -t dark

# Option C: uml-mcp generate_uml (if available in orchestrator context)
```

The renderer is a **deterministic transform** — same code always produces the same image. It adds no noise to the eval.

### Scoring (isolated, separate context)

The scorer receives BOTH the source text AND the rendered image (if render hook produced one).

For each output file:
```bash
# Score in a DIFFERENT context — the scorer never saw the execution
# If a rendered image exists, include it for visual evals
RENDER_ARG=""
if [ -f "runs/baseline-input{I}-run{J}.png" ]; then
  RENDER_ARG="A rendered PNG of this diagram is attached. Use it to evaluate visual quality evals (legibility, layout, contrast, flow direction)."
fi

claude -p "You are an eval scorer. Read this output and answer each question YES or NO. \
  Output ONLY a valid JSON object: {\"E1\": true/false, \"E2\": true/false, ...} \
  \
  EVALS: \
  $(cat ~/.claude/skills/{skill-name}/evals.md) \
  \
  SOURCE OUTPUT TO SCORE: \
  $(cat ~/.claude/skills/{skill-name}/runs/baseline-input{I}-run{J}.md) \
  \
  ${RENDER_ARG}" \
  $([ -f "runs/baseline-input{I}-run{J}.png" ] && echo "--files runs/baseline-input{I}-run{J}.png") \
  > score.json 2>/dev/null
```

**Structural evals** (syntax, format, arrow labels) are scored from the source text.
**Visual evals** (legibility, contrast, layout, spaghetti) are scored from the rendered PNG.
The scorer sees both and judges each eval against the appropriate artifact.

### Scoring JSON parsing (defensive)

The scorer may emit preamble text before the JSON. Always strip it:
```bash
# Extract JSON from scorer output — strip any preamble/explanation
RAW=$(cat score.json)
JSON=$(echo "$RAW" | grep -o '{.*}' | head -1)

# Validate with jq
echo "$JSON" | jq . > /dev/null 2>&1
if [ $? -ne 0 ]; then
  # Retry once — re-run the scoring call with stricter instructions
  claude -p "Output ONLY valid JSON, nothing else. {same scoring prompt}" \
    --no-input > score-retry.json 2>&1
  JSON=$(cat score-retry.json | grep -o '{.*}' | head -1)
  echo "$JSON" | jq . > /dev/null 2>&1 || echo "PARSE_FAILURE" > score-final.json
fi
```

If a score file has `PARSE_FAILURE` after retry, exclude that run from aggregation and log a warning. If >50% of runs fail to parse, abort the evolution — the scoring prompt needs fixing.

### Aggregation

```
Parse all score JSON files (excluding PARSE_FAILURE).
Per-eval pass rate = count(YES) / (valid_runs × N_inputs)
Baseline score = median(total_scores across valid runs)

Report:
  "Baseline: {score}/{max} (median of {N} runs × {M} inputs)"
  Per-eval breakdown: "E1: {pass_rate}%  E2: {pass_rate}% ..."
  Weakest evals (pass rate < 80%): list them
  Parse failures: {count} (if any)

Append to evolve-results.tsv
```

---

## Step 3: Generate Challenger

```
1. Identify the weakest evals (lowest pass rate across runs)
   → These are the target for improvement
2. Read the CURRENT SKILL.md (not from memory — read the file)
3. Generate a modified SKILL.md that addresses the weakest eval(s)
4. Save as SKILL.md (overwrite — git tracks the diff)
```

### Challenger generation constraints

- **One conceptual change per challenger.** Isolate variables so you know what worked.
- **Diff check:** After writing the challenger, run `git diff SKILL.md`. If the diff exceeds 15 lines of actual content change (excluding whitespace), you changed too much. Revert and try a smaller change.
- **Changes must be explainable in one sentence.** Log the hypothesis BEFORE running.
- **Never remove instructions that passing evals depend on.** Check which evals currently pass at 100% — those instructions are working. Augment or clarify; don't delete.
- **Avoid parrot-bait.** If your change adds language that mirrors an eval question too closely, the model will learn to echo the words without improving the actual output. Frame instructions as process guidance ("check X before outputting") not output prescription ("output must contain X").
- **Log the hypothesis:** "This change should improve E{n} because {reason}"

### What counts as "one conceptual change"

GOOD (one change):
- Adding an explicit step: "Before generating output, verify all labels are present"
- Adding an example of correct output for a specific case
- Rewording an ambiguous instruction to be more specific
- Adding a constraint: "Maximum 20 nodes per diagram"

BAD (multiple changes bundled):
- Rewriting the entire workflow section
- Adding a step AND changing the output format AND adding examples
- Restructuring the document organization while also changing instructions

---

## Step 4: Challenger Run

Identical process to Step 2 (isolated execution + isolated scoring) but against the modified SKILL.md.

```
For each test input in evals.md, for each run 1..N:
  1. Execute skill with SAME inputs as baseline (isolated claude -p)
  2. Score output with SAME evals (isolated claude -p, separate context)
  3. Record scores

Challenger score = median(total_scores across all runs)
```

---

## Step 5: Keep or Discard

```
If challenger_score > baseline_score:
  → git add SKILL.md
  → git commit -m "evolve({skill-name}): {one-line hypothesis} [{old}→{new}/{max}]"
  → New baseline = challenger
  → Log WIN to evolve-log.md with full detail
  → Report: "✓ Challenger wins: {old_score} → {new_score}. Committed."

If challenger_score == baseline_score:
  → git checkout -- SKILL.md (revert)
  → Log TIE to evolve-log.md
  → Report: "≈ Tie: {score} vs {score}. Ties go to baseline. Reverted."

If challenger_score < baseline_score:
  → git checkout -- SKILL.md (revert)
  → Log LOSS to evolve-log.md
  → Report: "✗ Challenger lost: {challenger_score} vs baseline {baseline_score}. Reverted."
```

**Important:** Ties are losses. This is the conservative ratchet — only strictly better changes survive. Karpathy's autoresearch uses the same rule: equal or worse means git reset.

---

## Step 6: Repeat or Stop

```
If rounds_remaining > 0 AND score < max_possible:
  → Go to Step 3 (new challenger targeting remaining weak evals)
  → IMPORTANT: Re-read the current SKILL.md from disk before generating next challenger.
    After a win, the file changed. After a loss, it reverted. Either way, read it fresh.

If score == max_possible:
  → Report: "Perfect score achieved. Evolution complete."
  → Stop

If rounds exhausted AND score < max_possible:
  → Report final summary
  → Suggest: "Consider improving evals.md (some evals may be too strict or ambiguous) 
    and running another evolution session."
  → Stop

If 3 consecutive losses:
  → Pause and report: "3 consecutive losses. The remaining failing evals may need 
    different evals (too strict?) or a structural skill change beyond single-step mutation."
  → Ask user whether to continue or stop.
```

---

## Final Report

After evolution completes, always output:

```
══ Evolution Summary: {skill-name} ══
Branch: evolve/{skill-name}/{date}
Rounds: {total} ({wins} wins, {ties} ties, {losses} losses)
Score: {start}/{max} → {final}/{max}

Winning changes:
  Round {n}: {hypothesis} [{old}→{new}]
  Round {m}: {hypothesis} [{old}→{new}]

Failed hypotheses:
  Round {x}: {hypothesis} (score unchanged)
  Round {y}: {hypothesis} (score dropped)

Per-eval trajectory:
  E1 ({name}): {start_rate}% → {final_rate}%
  E2 ({name}): {start_rate}% → {final_rate}%
  ...

Review: git log --oneline evolve/{skill-name}/{date}
Merge: git checkout master && git merge evolve/{skill-name}/{date}
```

**Remind the user:** "Review the diffs of winning commits before merging. Auto-research finds local optima — human judgment catches nonsense that scores well."

---

## /evolve evals {skill-name}

Generate binary evals for a skill. This is the measurement tool — get this right or nothing works.

### Eval design rules

**Rule 1: Binary only.** Every eval is YES/NO. No scales, no ratings, no "rate 1-10." Binary questions give the same answer every time. Scales compound noise.

**Rule 2: Observable outcomes.** Evals judge the OUTPUT, not the process. "Does the output contain labeled arrows?" not "Did the agent think about labeling arrows?"

**Rule 3: Cover the skill's purpose.** Each eval tests one aspect of what the skill promises to do. Extract every promise from the SKILL.md (explicit or implicit) and convert to a binary question.

**Rule 4: Outcome-focused, not pattern-matching.** Write evals about WHAT the output achieves, not WHAT WORDS it contains. Bad: "Does the output mention color palette?" Good: "Are all colors in the output from the specified palette?" The difference: the first one can be gamed by inserting the phrase "color palette" anywhere. The second requires actually using correct colors.

**Rule 5: Include representative inputs.** Evals need test inputs that exercise the skill's range. Don't test with only one input — a skill that scores 10/10 on input A and 3/10 on input B is not a good skill.

**Rule 6: No eval should be trivially passable.** If Claude can pass the eval without engaging with the skill's instructions at all, the eval is useless. Test this: would a generic response (no skill) pass this eval? If yes, make it more specific.

### Eval file format

```markdown
# Evals: {skill-name}

## Render Pipeline (optional)
Declares how to transform execution output before scoring.
Omit this section if the skill produces text-only output.

render_tool: kroki | mmdc | none
render_format_detect: "extract first code block, use language tag as format"
render_output: PNG
scorer_receives: source + rendered_image

## Test Inputs
Inputs the skill will be run against during evolution.
Include 2-3 inputs that cover different use cases of the skill.

### Input 1: {short description}
{The actual input/prompt to give the skill — be specific and realistic}

### Input 2: {short description}
{A different use case or edge case}

### Input 3: {short description}  (optional)
{A stress test or unusual request}

## Binary Evals
Answer YES or NO for each. Score = count(YES) / total.
Mark each eval as [source], [visual], or [both] to indicate what artifact the scorer judges it against.

### E1: {eval name}
{Question about the output that can be answered YES or NO}
Example YES: {concrete example of what a passing output looks like}
Example NO: {concrete example of what a failing output looks like}

### E2: {eval name}
...
```

### Eval generation process

```
1. Read the skill's SKILL.md thoroughly
2. List every promise the skill makes:
   - Explicit: "Always use pastel colors" → eval about color palette
   - Implicit: skill shows example with labeled arrows → eval about arrow labels
   - Structural: skill outputs a specific format → eval about format compliance
3. Convert each promise to a binary question about output quality
4. Sanity check: would a response with NO skill access pass this eval? 
   If yes → make it more specific to what the skill adds
5. Generate 2-3 representative test inputs:
   - Input 1: typical/happy-path use case
   - Input 2: different scenario exercising other skill features
   - Input 3: edge case or stress test (optional)
6. Write to ~/.claude/skills/{skill-name}/evals.md
7. Present to user for review BEFORE running evolution
```

**Target: 8-12 evals per skill.** Fewer than 6 lacks discrimination. More than 15 adds noise without signal. Aim for 10.

---

## /evolve status {skill-name}

Show evolution history from `~/.claude/skills/{skill-name}/evolve-log.md`.

```
Displays:
- Current baseline score and max possible
- Branch name for current/last evolution
- Rounds run (wins/ties/losses) 
- Score trajectory (round-by-round with per-eval breakdown)
- Winning hypotheses (what changes stuck and their score impact)
- Losing hypotheses (what changes didn't help — equally informative)
- Stale eval warning: if evals.md was modified since last evolution run
```

---

## evolve-log.md format

Auto-maintained per skill. Append-only.

```markdown
# Evolution Log: {skill-name}

## Session: {date} (branch: evolve/{skill-name}/{date})

### Round 1
- **Hypothesis:** {one sentence}
- **Change:** {what was modified in SKILL.md — specific section/line}
- **Diff size:** {N lines changed}
- **Baseline:** {score}/{max} (per-eval: E1=Y E2=N E3=Y ...)
- **Challenger:** {score}/{max} (per-eval: E1=Y E2=Y E3=Y ...)
- **Result:** WIN / TIE / LOSS
- **Commit:** {sha} (if win)
- **Tokens:** ~{execution_tokens} exec + ~{scoring_tokens} score = ~{total} round total
- **Parse failures:** {count} (if any)
- **Note:** {any observation about why this worked/failed}

### Round 2
...

### Summary
- Start: {score}/{max} → End: {score}/{max}
- Wins: {n}, Ties: {n}, Losses: {n}
- Total tokens: ~{sum of all round tokens} (observability, not a gate)
- Parse failures: {total across all rounds}
```

---

## Constraints

1. **Never evolve the evolve skill itself.** Meta-optimization creates circular dependencies. Evolve leaf skills only.

2. **Never modify evals during evolution.** Evals are the fixed ruler — like `prepare.py` in Karpathy's repo, which the agent cannot touch. If evals are wrong, fix them BETWEEN evolution sessions, not during one.

3. **One skill at a time.** Don't run parallel evolutions — git state conflicts.

4. **Human reviews wins.** After evolution completes, user MUST read the diffs of winning commits before merging the branch. Auto-research finds local optima — human judgment catches nonsense that scores well. This is non-negotiable.

5. **Eval quality > run count.** Bad evals with 100 runs produce garbage. Good evals with 3 runs produce signal. Invest time in `/evolve evals` first.

6. **Separate generator and judge.** Every execution and every scoring call uses a fresh `claude -p` context. The same context must never both generate and score output. This is the equivalent of Karpathy's separation between `train.py` (generates the model) and `prepare.py`'s eval function (scores it).

7. **Read from disk, not memory.** Before generating each challenger, re-read SKILL.md from the filesystem. After each keep/discard, the file state changed. Your memory of what's in it may be stale.

8. **Don't flood your context.** Redirect execution output to files. Read only the scores. This keeps the orchestrator's context clean and prevents the agent from being influenced by output details when generating the next challenger.

---

## Example Session

```
User: /evolve diagram --runs 3 --rounds 5

Claude:
Pre-flight checks... ✓
Loading skill: diagram
Loading evals: ~/.claude/skills/diagram/evals.md (10 binary evals, 2 test inputs)
Creating branch: evolve/diagram/2026-03-22
Committing current SKILL.md as baseline...

── Baseline Run (3 runs × 2 inputs = 6 executions) ──
Executing via claude -p (isolated)... ████████████ done
Scoring via claude -p (isolated)... ████████████ done

Per-eval pass rates:
  E1 (legible text):      6/6 (100%)
  E2 (pastel palette):    5/6 (83%)
  E3 (labeled arrows):    2/6 (33%)  ← weakest
  E4 (linear flow):       6/6 (100%)
  E5 (no ordinals):       4/6 (67%)  ← weak
  ...
Baseline score: 7/10 (median)

── Round 1: Challenger ──
Target: E3 (labeled arrows — 33% pass rate)
Hypothesis: Adding "EVERY arrow must have a text label describing the data flow" 
  to the Layout section will improve E3
Change: Added arrow labeling instruction to Layout Rules (3 lines)
Diff check: 3 lines changed ✓

Executing 6 runs (isolated)... ████████████ done
Scoring (isolated)... ████████████ done
  E3 pass rate: 2/6 → 5/6 (83%)
Challenger score: 8/10 (median)
✓ Wins: 7 → 8. Committed. (abc1234)

── Round 2: Challenger ──
Target: E5 (no ordinals — 67% pass rate)
Hypothesis: Adding "Use descriptive labels instead of numbers (e.g., 'Extract' not '1')" 
  as an anti-pattern example will improve E5
Change: Added anti-pattern example to Labeling section (4 lines)
Diff check: 4 lines changed ✓

Executing 6 runs (isolated)... ████████████ done
Scoring (isolated)... ████████████ done
  E5 pass rate: 4/6 → 4/6 (67%) — no change
Challenger score: 8/10 (median)
≈ Tie: 8 vs 8. Reverted.

── Round 3: Challenger ──
Target: E5 (no ordinals — still 67%)
Hypothesis: Rewording E5-related instruction as a "why" explanation rather than a rule
...

══ Evolution Complete ══
Branch: evolve/diagram/2026-03-22
Rounds: 5 (3 wins, 1 tie, 1 loss)
Score: 7/10 → 9/10
Review: git log --oneline evolve/diagram/2026-03-22
Merge: git checkout master && git merge evolve/diagram/2026-03-22

⚠ Review the diffs before merging. I optimized for eval scores — 
  verify the changes make sense to you.
```

---

*"Evals are the spec. The skill is the implementation. Evolution is the compiler."*
