# Architect sequences

Source: an owner-supplied brief (2026-10-20). The story structures are strong. Its numbers looked invented, so every number below is marked `[verify]`. Replace each one with a verified figure (facts file Part 1, a doc, or a logged run), or cut it.

## The argument: the "two-world tax"

Agents need a transactional database for state (Postgres). The enterprise's truth lives in the lakehouse (Delta). Connecting the two usually takes CDC pipelines, two governance models, and slow staging copies. Lakebase removes that tax: Postgres inside the Databricks platform, governed by Unity Catalog, with data moving through synced tables and CDF instead of a separate pipeline stack.

What architects want to see: state boundaries, latency penalties, storage layouts, failure-domain containment. No marketing abstractions.

## 1. Two worlds vs one platform

- **Before:** the agent writes to an external Postgres. Analytics reads the lakehouse. Between them sits a chain: CDC (e.g. Debezium) → Kafka → ingestion job, each hop with a queue. A latency counter `[verify]` runs on the chain. One hop fails and its queue backs up.
- **The collapse:** the chain's hops dissolve. The two stores move inward into one Databricks boundary. Writes reach the lake through Lakebase CDF or synced tables, with no hops in between (check which one the story needs, and its mode).
- **Security:** two permission sets (cloud IAM plus Postgres GRANTs, vs the lakehouse's) slide together. Duplicate rows cancel out, leaving one Unity Catalog boundary.

## 2. A branch per agent (copy-on-write)

- **The alternative:** a full clone of a large production database `[verify size]`. A progress bar creeps along, with a time `[verify]` and a storage cost `[verify]`. Per-task sandboxes look impossible.
- **The fork:** the same storage stays put. Thin compute pieces appear above it, each with pointer lines down to the same base blocks at one LSN. Time `[verify]`; added storage `[verify]`.
- **Divergence:** one agent runs a bad migration. Only the blocks it wrote appear, in its colour. Production keeps serving and is untouched.
- **Cleanup:** the agent finishes. Its compute scales to zero and its branch is deleted with its own blocks. The base never changed.

## 3. Point-in-time restore as blast-radius control

- **The event:** a timeline of commits. At one moment, an agent runs an unconstrained DELETE or DROP. The trace turns red, and reads downstream start to fail.
- **The fork:** a scrub cursor moves back to just before the event. A new branch splits off there. The live timeline keeps moving; nothing is overwritten.
- **Repair:** a diff shows what the recovery branch has that live lost. Only that table is copied back. The recovery branch is then deleted.
- Check first: the PITR window, and restore-as-a-new-branch behaviour (the facts file covers snapshots and restore as a new root branch).

## 4. Two kinds of agent memory

- **The split:** the agent at the top. One short, tight path leads to Lakebase (session state, conversation scratchpads, tool locks, pgvector working memory, latency `[verify]`). One long, deep path leads to the lakehouse (documents, history, governed Vector Search at scale).
- **Promotion:** closed sessions flow from Lakebase into the lakehouse through CDF, with no ETL script, and are then used for evaluation and tuning.
- **Closure:** one boundary is drawn around everything (model serving, Postgres state, vector index, lake), under one audit trail.

## Drawing rules from the brief

- Never one cylinder for two storage models: Postgres as grid cells (rows), Delta as vertical stripes (columns).
- A branch is drawn as pointer lines to the parent's point in time (LSN), never as a copy icon.
- Latency is physical distance: tight loops for agent ↔ Lakebase, long multi-hop spans for external APIs and batch scans.
