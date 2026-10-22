# Lakebase Graph Kit film v5: claims

Every factual narrator line, number, SQL line, and MONDO term is recorded here. Run numbers use only set B:
run `624175097872827`, dated folder `dated_a967b82a4b90`, run commit `a967b82`, filled at commit `550256b`.

## Ship gate

The explainer-surface rows are recorded on `main` at `590b105`. Read that register only
with `git show main:docs/release/post-claims.md`. Round-2 copy and motion tickets still
block a public post.

| Row | Status at `590b105` on `main` |
|---|---|
| GK-C1 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C6 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C7 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C10 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C13 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C23 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C25 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C34 | constant; no dated-run cell required |
| GK-C36 | prerequisites; no dated-run cell required |
| GK-C38 | Recorded 2026-10-20, dated Q14 run 624175097872827 |
| GK-C40 | Recorded 2026-10-03, live spike 3; owner approved 2026-10-21 |

Source: `git show main:docs/release/post-claims.md` at `590b105`.

## Film-local claims

These three lines are film-only. They do not replace a register row.

| Line | On-screen words | Evidence |
|---|---|---|
| GK-C40 | `Kit v1: a full copy each build.` / `Lakebase can also sync changes only.` | Register GK-C40 at `590b105` (`git show main:docs/release/post-claims.md`). Kit path: `src/lgk/steps/provision.py` SNAPSHOT (module docstring and synced-table create). Never draw the kit syncing incrementally. Never write `continuous`. |
| one SQL statement | `The whole walk is one SQL statement. Each hop is one CTE.` | `src/lgk/walks/sql.py` module docstring: web is one CTE per hop inside one statement. |
| join index | `index: edges(src_node_id)` | Commit `4948a69` (`provision: index edges src_node_id and dst_node_id`). Current pin: `src/lgk/steps/reapply.py` `("lgk_edges_src_node_id_idx", "edges", "src_node_id")`. |

## Build-engine finding

`src/lgk/steps/build.py:1,44` says “SDP”. The implementation imports `execute_sql` and calls it for
`CREATE OR REPLACE TABLE` and `INSERT INTO` statements. `src/lgk/uc_sql.py:45` sends each statement through
`w.statement_execution.execute_statement(warehouse_id=..., statement=...)`. The film therefore says
`"Spark SQL on a SQL warehouse"` and says nothing about SDP. This is a docstring mismatch, not a code edit.

## Number allowlist

### Dated run values

| Exact value or phrase | Meaning | Source |
|---|---|---|
| `1,000,000 nodes` | timing graph size | `550256b:docs/release/posts/medium-article.md:102,118,122` |
| `1,519,226 edges` | timing graph size | same |
| `4 CU` | timing graph compute setting | `medium-article.md:102,118` |
| `3.6 ms` | web depth 1 client p95 | `medium-article.md:102` |
| `4.2 ms` | web depths 2–4 client p95; maximum measured client p95 | `medium-article.md:102` |
| `3.8 ms` | tree depth 1 client p95 | `medium-article.md:102` |
| `3.9 ms` | tree depths 2 and 4 client p95 | `medium-article.md:102` |
| `19 of 20` | plain-language p95 | `medium-article.md:100,102` |
| `788 seconds` | first served graph | `medium-article.md:118` |
| `Web and tree, depths 1 to 4: 20 of 20 seeds equal` | correctness check | `medium-article.md:98` |

`788 seconds` always carries the caption `"sum of step run times · preflight to switch"`.
`4.2 ms` always carries the caption
`"client p95 · warm connection · prepared statements off · in-region · 4 CU"`.

### Kit settings

| Setting | Source line |
|---|---|
| `11` privacy floor | `src/lgk/privacy/floor.py:18`, `DEFAULT_FLOOR = 11` |
| `25` cut per hop | `src/lgk/steps/walks.py:39`, `top_n: int = 25` |
| `4 hops` | `src/lgk/walks/sql.py:43`, `WEB_MAX_DEPTH = 4` |
| `100 levels` | `src/lgk/walks/sql.py:44`, `TREE_MAX_DEPTH = 100` |
| `MONDO:0005015` | `tests/test_mondo_live.py:44`, diabetes mellitus seed |

### Refused set A values

`1,615,105`, `0.69 ms`, `180 of 180`, `180/180`, and `1,350 s` fail `check_numbers.py`.

## SQL on screen

The full generated sources are `sql/web_folded.sql`, `sql/web_unfolded.sql`, and `sql/tree.sql`.
The on-screen panel says `"simplified"` once. A displayed line can split visually, but its normalized text must be a
substring of one normalized generated line.

| Displayed text | Source |
|---|---|
| `WITH hop0 AS (...)` | `sql/web_folded.sql:1` |
| `hop1 AS (` | `sql/web_folded.sql:2` |
| `hop2 AS (` | `sql/web_folded.sql:11` |
| `JOIN hop1 f ON ...` | `sql/web_folded.sql:14` |
| `NOT IN (... hop0 ... hop1)` | `sql/web_folded.sql:15` |
| `GROUP BY e.dst_node_id` | `sql/web_folded.sql:16` |
| `HAVING MIN(e.weight) >= 11` | `sql/web_folded.sql:16` |
| `ORDER BY c.support DESC, c.node_id` (4:5 wraps after the comma: `ORDER BY c.support DESC,` / `c.node_id`) | `sql/web_folded.sql:18` |
| `LIMIT 25` | `sql/web_folded.sql:19` |
| `hop3 AS (` | `sql/web_folded.sql:20` |
| `hop4 AS (` | `sql/web_folded.sql:29` |
| `SET ROLE reader` | `src/lgk/app/template/backend/app/reader.py.tmpl:16` |
| `WITH RECURSIVE walk(depth, frontier, seen)` (4:5 wraps: `WITH RECURSIVE` / `walk(...) AS (`) | `sql/tree_display.sql:1` |
| `UNION ALL` (4:5 only) | `sql/tree_display.sql:3` |
| `SELECT w.depth + 1` | `sql/tree_display.sql:4` |
| `NOT (e.dst_node_id = ANY(w.seen))` | `sql/tree_display.sql:11` |
| `WHERE w.depth < 2` | `sql/tree_display.sql:18` |

`GROUP BY`, not `NOT IN`, merges the hop-2 clinician reached by two hop-1 clinicians. `NOT IN` removes a clinician
already reached in an earlier hop. The folded SQL uses `MIN(e.weight)` and reapplies the floor. The unfolded timing
SQL has no `HAVING` clause, so Beat 8 leaves that line dim.

## MONDO provenance

Approved download: `https://purl.obolibrary.org/obo/mondo.json`.

- HEAD size: `107,871,006` bytes, below the 500 MB stop line.
- Release: `v2026-10-06`.
- versionIRI: `http://purl.obolibrary.org/obo/mondo/releases/2026-10-06/mondo.owl`.
- Download date: `2026-10-21`.
- SHA-256: `ddbf0b88d8a91007ed55a01d579a418f68940f7f897d3dd55750ba966b3912ab`.
- Parser: `python3 -I parse_mondo_data.py data/mondo.json data/diabetes_terms.json`.
- Parser source of truth: `src/lgk/loaders/mondo.py:128-138`, `parse_mondo`.
- Credit: `"MONDO · CC BY 4.0"`, from GK-C38 and `NOTICE`.

Only direct is-a children of `MONDO:0005015`, plus one level below, are eligible. Beat 9 uses:

| ID | Exact label | Relationship |
|---|---|---|
| MONDO:0005015 | diabetes mellitus | seed |
| MONDO:0005147 | type 1 diabetes mellitus | direct child |
| MONDO:0005148 | type 2 diabetes mellitus | direct child |
| MONDO:0005406 | gestational diabetes | direct child |
| MONDO:0015967 | monogenic diabetes | direct child |
| MONDO:0016391 | neonatal diabetes mellitus | child of monogenic diabetes |
| MONDO:0018911 | maturity-onset diabetes of the young | child of monogenic diabetes |

Exact labels and relationships: `data/diabetes_terms.json`, derived offline from the downloaded file.

## Narrator lines

These words are copied verbatim into `script.md` and the subtitle generator.

| Beat | Narrator words | Evidence |
|---|---|---|
| 1 | Which clinicians share patients with Dr. A? | User-approved question; illustrative status is on screen because no run record has names or counts. |
| 2 | The source tables sit in Unity Catalog, as Delta tables. | GK-C1; `src/lgk/steps/build.py:81-83`. |
| 3 | One path copies data out of Databricks. One starts a warehouse query per request. | `550256b:medium-article.md:24-26`; framing only, no measured warehouse time. |
| 4 | Spark SQL on a SQL warehouse builds the graph. Keys become nodes and edges. Shared patients fold into one count. Under the privacy floor of 11, no line. | Build-engine finding; `build.py:270-293,400-429`; `floor.py:18`. |
| 5 | Synced tables copy the graph into Lakebase in full. First served graph: 788 seconds, on the synthetic provider graph. Kit v1: a full copy each build. Lakebase can also sync changes only. | GK-C1; `provision.py:193-234` (SNAPSHOT); GK-C23, `medium-article.md:118`; GK-C40. |
| 6 | The app begins at Dr. A. Each hop is one step of the query. Earlier clinicians stay out. Two routes to one clinician become one row. The privacy floor runs again. The cut keeps up to 25 per hop. | Generated folded SQL lines 1-19; `walks.py:39`. The floor check acts, but every default-floor edge already passed the build floor. |
| 7 | The walk adds hop 3 and hop 4 the same way. | `sql/web_folded.sql:20-37`; GK-C34. |
| 8 | The app reads served views only. Web and tree walks, depth 1 to 4: 19 of 20 answer in 4.2 ms or less, timed by the kit's measure step. | GK-C6; GK-C13, `medium-article.md:100,102`. |
| 9 | The same kit walks a tree. From diabetes mellitus, one recursive loop adds one is-a level per turn. | `sql/tree_display.sql:1-19`; derived MONDO record; GK-C38. |
| 10 | A new version moves every served view in one transaction, or none moves. | GK-C25; `src/lgk/versions.py:284-296`. |
| 11 | Timing graph: 20 seeds equal a source-table reference. | GK-C10; `medium-article.md:98`. |
| 12 | Built from Unity Catalog. Served by Lakebase. No graph database outside Databricks. Graph databases still win for ad hoc traversals of unknown length. | GK-C1 exact scope; an exact subset of GK-C24. |

## Illustrative elements

- Dr. A and all other clinician names.
- Question 1's layout and edge thicknesses.
- The number of nodes drawn in the million-node field.
- Version labels `v1` and `v2`.

Question 2's listed MONDO terms are real values from the recorded release.
