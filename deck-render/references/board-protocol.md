# Board Protocol

This protocol only applies when `_meta.board_dir` is present in the strategy contract. If `_meta.board_dir` is absent, ignore this file entirely — you are in standalone mode. Zero cost.

---

## Board Read Protocol (Coordinated Mode)

Check the strategy contract (strategy YAML or strategy-contract.yaml) for a `_meta.board_dir` field.

**If `_meta.board_dir` is present** — you are running inside a coordinator pipeline:
1. Read `{board_dir}/invariants.yaml` if it exists (enablement-kit coordinator). These are HARD constraints:
   - `hero_message` — must appear verbatim (or semantic equivalent) in the deck
   - `proof_points[].assigned_to` — only use proof points assigned to "deck" or "all"
   - `competitive_frame` — use this positioning, do not invent your own
   - `call_to_action` — unified CTA
2. Read `{board_dir}/board/` for any prior skill outputs. Deck is typically rendered FIRST in an enablement-kit, so the board may be empty. When it's not empty (e.g., content-factory re-renders after consistency failure), read prior outputs to understand what the coordinator wants fixed.
3. `{board_dir}/strategy-contract.yaml` (at the coordinator root, NOT in `board/`) is the LIVING strategy. Use it instead of any stale copy. Check its `version` field — higher = more recent amendments.

---

## Board Write Protocol (Coordinated Mode)

**Only when `_meta.board_dir` is present.**

After completing the deck-level review (after all slides pass per-slide eval AND the deck-level arc/rhythm check passes), write a board entry to `{board_dir}/board/deck-render-output.yaml`:

```yaml
skill_name: "deck-render"
invoked_at: "{ISO 8601 timestamp}"
invoked_by: "{coordinator name from _meta.coordinator}"

artifact_path: "{absolute path to final .pptx}"
artifact_type: "deck"

# What the deck actually contains (for downstream skills to read)
hero_message_as_rendered: "{exact hero text from the deck}"
proof_points_used:
  - point: "{proof point text}"
    slide_number: N
    treatment: "{how it was presented — stat hero, supporting evidence, etc.}"
competitive_frame_as_rendered: "{how competitive positioning landed}"
slide_count: N

# Quality from existing per-slide evaluation
quality_score: N                        # count of slides with CLEAN verdict
quality_max: N                          # total slides
quality_pass: true/false                # all slides CLEAN?
quality_notes: "{summary of any fixes applied}"
per_slide_scores:
  slide_1: { verdict: "CLEAN", layout: "title_slide" }
  slide_2: { verdict: "CLEAN", layout: "stat_hero" }
  # ... one entry per slide

# Amendments the deck discovered
strategy_contract_amendments:
  - field: "{e.g., design_decisions.color_system}"
    current_value: "{what strategy said}"
    recommended_value: "{what actually worked better}"
    reason: "{why}"
discovered_entities: []
coverage_gaps: []

recommendations_for_downstream:
  - target_skill: "cheatsheet-render"
    recommendation: "{e.g., 'cheatsheet should reference slide 4 terminology for consistency'}"
    priority: "medium"
```

Use the Write tool to create this file. If the file already exists (retry scenario), overwrite it.

**If `_meta.board_dir` is absent** — skip board write entirely. Do not create any files.
