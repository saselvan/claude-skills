# Domain: Databricks and Lakebase

Read this when the film is about Databricks, Lakebase, Unity Catalog, Delta, synced tables, CDF, Vector Search,
Model Serving, Apps or Agent Bricks. It adds rows to `../grammar.md`; the generic rows still apply.

## Facts

- Verified facts: `~/.claude/docs/lakebase-platform-facts.md`, Part 1 (owner's file). If it is not on this machine,
  copy it to `facts.md` next to this file or mark every number and mechanism detail `[verify]` and list them in the
  report. Docs and Glean come second; another model's description of the product comes nowhere.
- Standing rulings for this domain (owner): the whole platform is in scope; a Databricks film shows the platform story,
  not a generic Postgres app (the Course 1 failure in `../precedents.md`); never cite an institution as a customer
  unless the owner confirms; Lakebase gets the majority of a Lakebase film's time (v5: about 60%).
- Architect sequences (unify, branch, recover, remember): `databricks-sequences.md`, numbers `[verify]`.

## Rows

| Mechanism | What it physically is | How it looks and moves |
|---|---|---|
| Lakebase (Postgres) tables | Mutable row pages | Horizontal rows, modular cells; an update changes a cell in place. |
| Delta / Parquet | Immutable columnar files | Vertical stripes; new data adds files; old files stay until vacuum. Never the same cylinder as Lakebase. |
| Lakebase branch | A fork of the database at one point in time (verified: holds the parent's rows, schema and roles at that time, can start at an exact LSN, READY in seconds; facts Part 1 "Branching and PITR"). How storage is shared underneath is docs-only. | A track splits off the parent's timeline at one LSN in the branch's colour, usable at once. Do not draw a slow copy job. Do not claim "zero-copy" or shared blocks on screen unless the docs are cited as docs. |
| WAL and LSN | An append-only tape | A horizontal tape; a branch or restore point is a pointer clamped at one LSN. Check how Lakebase exposes it before naming it on screen. |
| Point-in-time restore | A fork from a past moment | The cursor moves back, a new track splits off, the live track keeps moving. Check the PITR window and restore-as-new-branch behaviour first. |
| Synced table (Delta → Lakebase) | A governed mirror | A change in the stripes ripples into the rows. SNAPSHOT is a full redraw; TRIGGERED and CONTINUOUS are ripples. A backed-up sync queue is labelled "backed up: data downstream is stale". |
| Lakebase CDF (Postgres → Delta) | A change stream into the lake | Row changes leave the grid as packets and land as new Delta files. |
| Synced table from a secured source | A refusal, not a leak | The sync is refused at create; nothing unfiltered is copied (verified, facts Part 1). Draw the refusal at the boundary. |
| Unity Catalog | One field everything inside obeys | One boundary around tables, models, indexes and apps; per-system permission rows merge into one set. |
| Row-level security, masks | Rows you may not see | Dark in place, never vanished; the hidden count can show. Synced tables have RLS limits: check the facts file before drawing RLS on one. |
| On-behalf-of identity | The user's badge travels with the request | Identity stays on the request through every hop; the data read is limited to it. |
| Audit, lineage, MLflow trace | A receipt per step | Receipts line up as one trail at the end. |
| Vector Search / hybrid in the served stack | Nearness plus term match | See grammar. The served search uses a fixed weighted sum (0.75 dense + 0.25 BM25 at reference-package `92cf68ed`, `search/agent_tool.py:56-80`); draw two scores added, not rank fusion. |
| Spark SQL on a SQL warehouse | A batch engine building something | Its own beats, its own colour; it builds the graph or table, then shrinks to context when serving starts. |
| Autoscaling, scale to zero, pooling, serverless | See grammar | Check whether and how Lakebase pools connections before drawing a pool. |

## Palette (v5 film register, design.md)

Systems: Unity Catalog teal (`#269685` line), Lakebase blue (`#669EE4`), Spark amber (`#F2A657`), app violet
(`#E2BFFC`); outside Databricks grey (`#91979D`, dashed); boundary coral (`#FF785F`); the one "now" lime (`#E2FF45`).
Ground `#0B0F13`. Delta is stripes; Lakebase is rows. When a colour round or owner decision sets a palette, it wins.
