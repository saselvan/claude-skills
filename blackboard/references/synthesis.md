# Synthesis Formats

Synthesis is built only from board signals (`board/*-complete.yaml`), `context.yaml`, and the merge/test results. Don't re-read agent transcripts; if something isn't in a signal, it didn't happen as far as synthesis is concerned.

## Caller-defined schema (preferred for coordinators)

A parent coordinator passes exactly the fields it needs:

```yaml
synthesis_schema:
  output_format: yaml            # yaml | markdown
  required_fields:
    - tests_passed
    - files_modified
    - commit_sha
    - branch_name
    - merge_status
  include_board_signals: true    # embed raw signals under `signals:`
  include_timeline: false
```

Produce one entry per stream with those fields, plus a top-level `status: complete | partial | failed` and `failures: [...]`. If a requested field can't be derived from the signals, emit it as `null` with a note in `failures` rather than inventing a value.

## Named presets

| Preset | Format | Content | Used by |
|---|---|---|---|
| `markdown-report` (default) | md | Summary, deliverables table, merge + test results, failures | standalone runs |
| `build-result` | yaml | Per stream: tests, files_modified, commit_sha, branch_name, merge_status | design-ops `/design build` |
| `research-synthesis` | md | Per stream: findings, sources, open questions; cross-stream themes | research fan-out |
| `artifact-metadata` | yaml | Per stream: artifact paths, types, sizes | content-factory |
| `demo-deployment` | yaml | Per stream: URLs, resource IDs, credentials location | demo-factory |

## `markdown-report` template

```markdown
# Blackboard Synthesis: {task_description}

Board: `{BOARD_DIR}` · Started {start} · Finished {end} · Wall time {min} min
Streams: {N} ({complete} complete, {partial} partial, {failed} failed)

## Summary
{2–4 sentences: what was built, what state it is in, what the caller must do next.}

## Deliverables
| Stream | Deliverable | Path |
|---|---|---|

## Merge
{clean | conflicts: list files per branch}

## Tests
{passed}/{total} on merged result. {Which failures map to which stream, if determinable.}

## Decisions made by agents
{Bullets from each signal's `decisions`. These are judgment calls the user may want to revisit.}

## Failures and warnings
{From context.yaml.failures and each signal's `errors`.}
```

Keep the summary honest: a run with a failed critical stream is a failed run, however good the other streams look.
