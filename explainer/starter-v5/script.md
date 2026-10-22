---
title: Lakebase Graph Kit film v5
duration_seconds: 90.6
scratch_voice: Samantha
scratch_rate_wpm: 190
subtitle: explainer-v5-16x9.srt
---

# Narration

Generated from `screen-copy.json`. Each `- Cue:` is one event.

## Beat 1

- Time: 00:00.000 --> 00:04.000
- Seconds: 4
- Claim: Owner-approved Question 1; illustrative names and counts are stated on screen.
- Cue: 00:00.000 --> 00:04.000
  Who shares patients with Dr. A?

## Beat 2

- Time: 00:04.000 --> 00:08.000
- Seconds: 4
- Claim: GK-C1; src/lgk/steps/build.py:81-83.
- Cue: 00:04.000 --> 00:08.000
  Source tables sit in Unity Catalog.

## Beat 3

- Time: 00:08.000 --> 00:14.500
- Seconds: 6.5
- Claim: Framing only; no measured number.
- Cue: 00:08.000 --> 00:14.500
  One path copies data out.
  One starts warehouse SQL.

## Beat 4

- Time: 00:14.500 --> 00:26.000
- Seconds: 11.5
- Claim: GK-C7; src/lgk/uc_sql.py:45; privacy floor 11.
- Cue: 00:14.500 --> 00:18.300
  Spark SQL builds the graph.
- Cue: 00:18.300 --> 00:22.100
  Keys become nodes and edges
- Cue: 00:22.100 --> 00:26.000
  Patients fold. Under 11 none

## Beat 5

- Time: 00:26.000 --> 00:32.000
- Seconds: 6
- Claim: GK-C23; GK-C40.
- Cue: 00:26.000 --> 00:30.200
  sum of step run times
  preflight to switch
- Cue: 00:30.200 --> 00:36.160
  Kit v1: a full copy each build.
  Lakebase can also sync changes only.

## Beat 6

- Time: 00:32.000 --> 00:49.500
- Seconds: 17.5
- Claim: GK-C7; src/lgk/walks/sql.py; walks.py:39.
- Cue: 00:36.160 --> 00:41.400
  The whole walk is one SQL statement.
  Each hop is one CTE.
- Cue: 00:41.400 --> 00:47.500
  Two routes, one row.
  Cut keeps 25 per hop.

## Beat 7

- Time: 00:49.500 --> 00:53.500
- Seconds: 4
- Claim: GK-C34; sql/web_folded.sql:20-37.
- Cue: 00:49.500 --> 00:53.800
  The walk adds hop 3 and hop 4
  the same way.

## Beat 8

- Time: 00:53.500 --> 01:01.500
- Seconds: 8
- Claim: GK-C6, GK-C13, GK-C34.
- Cue: 00:53.800 --> 01:01.500
  client p95 · warm · in-region
  prepared statements off · 4 CU

## Beat 9

- Time: 01:01.500 --> 01:10.500
- Seconds: 9
- Claim: GK-C38; sql/tree_display.sql; MONDO v2026-10-06.
- Cue: 01:01.500 --> 01:04.700
  The same kit walks a tree.
- Cue: 01:04.700 --> 01:10.500
  From diabetes mellitus,
  one loop adds one is-a level.

## Beat 10

- Time: 01:10.500 --> 01:15.500
- Seconds: 5
- Claim: GK-C25; src/lgk/versions.py.
- Cue: 01:10.500 --> 01:15.500
  A rebuild is a new version.

## Beat 11

- Time: 01:15.500 --> 01:20.500
- Seconds: 5
- Claim: GK-C10; timing graph, 20 seeds.
- Cue: 01:15.500 --> 01:20.500
  Timing graph: 20 seeds equal
  a source-table reference.

## Beat 12

- Time: 01:20.500 --> 01:30.600
- Seconds: 10.1
- Claim: GK-C1; exact subset of GK-C24; repo pointer.
- Cue: 01:20.500 --> 01:26.240
  Graph databases still win for ad hoc
  traversals of unknown length
- Cue: 01:26.240 --> 01:30.600
  github.com/saselvan/graph-kit-for-lakebase

## Run-time split

- Spark is the main system for 11.5 seconds, from 14.5 to 26 seconds.
- Lakebase is the main system for 48.5 seconds, from 32 to 80.5 seconds.
- Including the 6-second landing beat, Lakebase receives 54.5 seconds, or 60.2% of the film.
