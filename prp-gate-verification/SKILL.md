---
name: prp-gate-verification
description: Verify PRP validation gates with evidence before claiming completion. Use when finishing any PRP phase, before deployment claims, or when asked to verify work. Triggers on 'verify gate', 'PRP complete', 'gate check', 'verification', 'is this done'.
---

# PRP Gate Verification Skill

Prevents false completion claims by requiring verifiable evidence for every PRP validation gate criterion.

## When to Use

- Before marking ANY PRP phase as complete
- Before claiming deployment is successful
- Before saying "all tests pass" or "everything works"
- When the user asks "is this actually done?"

## Process

### Step 1: Extract Gate Criteria

Read the PRP file for the phase being verified. Find the validation gate section (typically named `Validation Gate N` or `GATE_N_PASS`). List every criterion.

### Step 2: Produce Evidence for Each Criterion

For each criterion, produce ONE of these evidence types:

| Evidence Type | When to Use | Example |
|---|---|---|
| **Command output** | Build, test, lint results | `npm run build` output showing 0 errors |
| **Live API response** | Endpoint verification | Paste full JSON from `/api/search` |
| **Browser screenshot** | UI verification | Screenshot at 1440px showing map + providers |
| **Code reference** | Implementation check | File path + line numbers showing the feature |
| **SQL verification** | Schema alignment | Query table/column names matched against DDL |

### Step 3: Generate Pass/Fail Report

Create a table in this exact format:

```
| # | Criterion | Evidence | Result |
|---|-----------|----------|--------|
| 1 | App builds without error | `npm run build` → 0 errors, 0 warnings | PASS |
| 2 | Map tiles visible | Screenshot: map-verification.png | PASS |
| 3 | Adequacy meter shows 3 states | Only tested ADEQUATE, not AT_RISK or VIOLATION | FAIL |
```

### Step 4: Block or Proceed

```
IF any criterion is FAIL:
  - List all failures
  - Do NOT mark phase as complete
  - Do NOT proceed to next phase
  - Fix failures first

IF all criteria PASS:
  - Mark phase as complete with evidence summary
  - Proceed to next phase
```

## Anti-Patterns to Catch

These are signs of false completion. If you see any, the gate FAILS:

1. **Mock data in production code** — `import { mockProviders } from './test/mocks'` in a non-test file
2. **Empty component** — A React component that renders an empty `<div>` or placeholder text
3. **Tests that ignore parameters** — Mock returning same data for all inputs
4. **Schema mismatch** — SQL references table `isochrones` but DDL defines `isochrone_cache`
5. **"Works locally"** — Claimed as deployed but only tested via `TestClient` with mocks
6. **Null data** — API returns real records but most fields are `null`
7. **Hardcoded IDs** — `search_id = 'app-session'` instead of real value from prior API call

## Example Verification

For PRP-RR-004 Phase 1 (React + Layout + Map):

```
| # | Criterion | Evidence | Result |
|---|-----------|----------|--------|
| 1 | App builds and runs | `npm run dev` starts on :5173 | PASS |
| 2 | Split-screen renders (35%/65%) | Screenshot: sidebar 35%, map 65% | PASS |
| 3 | Map loads with tiles | Screenshot: OSM tiles visible, NYC center | PASS |
| 4 | Responsive stacked at <1024px | Chrome DevTools 768px screenshot | PASS |
| 5 | Independent scroll | Sidebar scrolls, map stays fixed | PASS |
```

## Integration with Superpowers

This skill extends the `verification-before-completion` superpowers skill by making it PRP-aware. Use BOTH:

1. This skill: PRP-specific gate criteria with evidence tables
2. `verification-before-completion`: General "run commands and confirm output before claiming done"
