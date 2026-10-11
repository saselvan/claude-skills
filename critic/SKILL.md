---
name: critic
description: "Cross-family adversarial critic. Pipes a code diff, file, or customer artifact to a DIFFERENT model family (deepseek-r1:32b, fully offline) for an independent review that does not share Claude's blind spots. USE WHEN: user says 'critic', 'critique this', 'second opinion', 'independent review', 'verify this', or as the cross-family pass in the build-methodology DA step. PHI-safe — nothing leaves the machine."
allowed-tools: Bash, Read, Edit
---

# Critic — Cross-Family Adversarial Review

A verifier that is genuinely independent. Every other adversarial tool in this
vault (`council`, `audience-review`, `grill-me`, the devil's-advocate reviewer
agent) is **Claude critiquing Claude** — same model family, same blind spots.
This skill routes the work to **deepseek-r1:32b** (a different family) running
**locally via ollama**, so:

- It catches failure modes Claude is structurally blind to.
- Nothing leaves the machine — safe for customer code, OMOP schemas, PHI-adjacent work.
- It is free (no API metering).

Engine: `~/.claude/scripts/critic.py`.

## CRITICAL: latency → always background

The critic is a reasoning model. A real critique takes **~1–4 minutes**. NEVER
run it in the foreground and wait, and NEVER wire it into a blocking `Stop`
hook. Always launch it as a **background Bash task** and check completion via
TaskOutput before using the result (per coding-guardrails: track background
tasks explicitly).

## Usage

| Intent | Command |
|---|---|
| Review current uncommitted changes | `python3 ~/.claude/scripts/critic.py --diff` |
| Review staged changes (pre-commit) | `python3 ~/.claude/scripts/critic.py --staged` |
| Review a specific file | `python3 ~/.claude/scripts/critic.py path/to/file.py` |
| Review a customer artifact (prose) | `python3 ~/.claude/scripts/critic.py --lens content path/to/email.md` |
| Review piped text | `echo "..." \| python3 ~/.claude/scripts/critic.py -` |

`--lens code` (default) hunts for bugs: undefined vars, silent failures,
`ON CONFLICT DO NOTHING`, dead guards, SQL injection, resource leaks, contract
violations. `--lens content` hunts for unanchored claims, salesy tone, feature
dumps, and credibility risks in customer-facing prose.

## Workflow when invoked

1. Determine the target (default to `--diff` if the user is mid-build and said
   nothing specific; otherwise the file/artifact they named).
2. Launch the engine as a **background** Bash task.
3. Do other useful work or tell the user it's running (~1–4 min).
4. When notified, read the task output. Present the critique findings grouped
   by `[SEVERITY]`.
5. For code: treat `critical`/`high` findings as must-fix. Verify each against
   the actual artifact before acting — the critic can be wrong (it is a
   different family, not an oracle). Read the expression, not the name.
6. If output is `NO DEFECTS FOUND` / `NO ISSUES FOUND`, report the clean pass.

## Preconditions

- ollama server running (`ollama serve`) with `deepseek-r1:32b` pulled.
- If the engine prints a "cannot reach ollama" error, surface it — do not
  silently fall back to a Claude self-review (that would defeat the purpose).

## Where this fits

- **Build loop:** the cross-family half of the build-methodology DA step. Run
  alongside the Claude devil's-advocate agent so two different families inspect
  every change. See memory `feedback-build-methodology`.
- **Customer content:** a second, independent pass after `tone-check`
  (`--lens content`) before delivery.

## Extending to other families

The engine reads `CRITIC_MODEL` / `CRITIC_HOST`. To use a cloud family instead
(e.g. another local model, or wire a Gemini path via the `deep-research`
skill), point those env vars or add a sibling caller. Default stays local +
offline because most SA work here is PHI-adjacent.
