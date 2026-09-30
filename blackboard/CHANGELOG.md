# Changelog

## v2.2

- Step 4 is now collect **and verify**: the coordinator checks scope (its own changed-file list against a wave start marker, diffs of every touched file), re-runs each claim's evidence command, replays one mutation of its own, and rejects vacuous tests before writing a signal. A failed check sends the stream back as its one retry. From the clinical-va-appkit run (2026-09-29), where agents reported "tsc clean", "reverted", "captured 1,204", "checks fixed" and "mutations red" when false, and one agent's out-of-scope edit overwrote another's work.
- Result YAML gains `changed_files`, `evidence` and `mutations`; the Step 4 schema now points at the one copy in `references/agent-prompt.md`.
- Worktrees base on `main`: Step 3 says how to run branch work (hand-made worktrees, or a shared tree with disjoint scopes).

## v2.1.1

- Fixed the Step 3 spawn example: `name: stream.name` → `description: stream.name`. The Agent tool has no `name` parameter; `description` is the field that carries the label, and it is required.
- Corrected the stream-schema comment: the slug is the coordinator's own label (board filename, merge message), not the agent's assigned name. The Agent tool returns the assigned name; the coordinator cannot choose it.

## v2.1

- Wave scheduling replaces agent-side polling and cross-agent messaging. Agents never wait on each other; the coordinator spawns dependency levels in order and injects upstream deliverables into prompts.
- Agents return their result YAML as the final message; the coordinator writes board signals. Fixes Explore streams (no Write tool) never being able to signal completion.
- Removed nonexistent `Bash` agent type; `Task(...)` renamed to `Agent(...)`.
- Removed cost/benefit minute estimation and `~/.claude/blackboard-stats.yaml`. Decision is now: 2+ independent streams with meaningful work.
- Added `writes_files`, `scope`, and per-stream `timeout_min` to the stream schema; worktrees only for write streams; explicit `target_branch` for merges.
- Agent prompt template moved to `references/agent-prompt.md`; code-quality rules are pasted into prompts rather than assumed.
- Failure rules applied per wave; single retry only for transient failures; critical failure stops before dependent waves spawn.
- Resume mode described once.
- SKILL.md cut from ~860 to ~190 lines; presets, integrations, and code-quality rules moved to `references/`. Changelog moved out of frontmatter.
- Agent-teams tools made optional with a stated prerequisite.

## v2.0

LLM decomposition replaces regex parser, stream criticality, per-stream agent type selection, worktree isolation, caller-defined synthesis schema, `--resume`, execution history, dual-channel coordination, `.pipeline/` board convention, default max depth 2.

## v1.0

Initial skill with regex stream parsing, hardcoded synthesis formats, `scratch/` board directory, hard depth-3 limit.
