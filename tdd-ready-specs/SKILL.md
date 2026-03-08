---
name: Writing TDD-Ready Specs
description: Use when creating or reviewing specs before implementation. Ensures specs have fixtures, Given-When-Then contracts, and exact assertions that enable true test-first development. Activates before brainstorming or writing-plans.
---

# Writing TDD-Ready Specs

Announce at start: "I'm using the tdd-ready-specs skill to ensure this spec supports test-first development."

## When to Use

- Creating a new feature spec
- Reviewing an existing spec before implementation
- User mentions "Ralph," "spec," "TDD," or "test-driven"
- Before invoking `superpowers:brainstorming` or `superpowers:writing-plans`

## Core Principle

**A spec is TDD-ready only if tests can be written from it WITHOUT reading implementation.**

If you can't write exact assertions from the spec, the spec is incomplete.

## Required Sections Checklist

Before proceeding to brainstorming or planning, verify spec has ALL:

- [ ] **Test Fixtures** — Exact data with IDs, names, values
- [ ] **Given-When-Then Contracts** — For every public method
- [ ] **Edge Case Contracts** — Unknown input, empty data, boundaries
- [ ] **Exact Assertions** — Executable Python, not vague descriptions
- [ ] **Formulas** (if applicable) — Full calculation with example

If ANY section is missing: **STOP. Add it before proceeding.**

## Prohibited Spec Language

| ❌ Banned | Why | ✅ Replace With |
|-----------|-----|-----------------|
| "handles gracefully" | Not testable | "returns string containing 'not found'" |
| "returns appropriate error" | Vague | "raises ValueError with message 'Invalid X'" |
| "includes relevant info" | Vague | "contains '72' and 'healthy'" |
| "see formula in spec" | Missing | The actual formula with example |

## Fixture Format

```python
# tests/fixtures/{component}_fixtures.py

ACCOUNTS = [
    {"id": "acc-1", "name": "Providence Health", "health_score": 72},
    {"id": "acc-2", "name": "CHLA", "health_score": None},  # Edge case: no Gold data
]

SESSIONS = [
    {"id": "sess-1", "account_id": "acc-1", "date": "2026-01-12", "title": "Weekly Sync"},
]
```

Rules:
- Specific IDs, names, values (not "example" or "test")
- Include edge cases: None values, empty lists
- Comment purpose of edge case fixtures

## Contract Format

```markdown
### method_name() — Scenario Description

**Given:** [Exact fixture state - reference fixture IDs]

**When:**
```python
result = component.method("exact_input")
```

**Then:**
| Assertion | Check |
|-----------|-------|
| [What to verify] | `[Executable Python assertion]` |
```

## Assertion Rules

### Banned Assertions (pass against placeholders)

```python
# ❌ NEVER use these alone
assert result is not None
assert isinstance(result, str)
assert len(result) > 0
```

### Required Pattern

```python
# ✅ Must verify actual content
assert result.startswith("## Account: Providence")
assert "72" in result  # Exact value from fixtures
assert "Joe Santos" in result  # Exact name from fixtures
```

### The Stub Test

Before approving a spec, ask:

> "If implementation returned empty string, would these assertions fail?"

If no → spec needs more specific assertions.

## Edge Cases Required

Every method needs contracts for:

1. **Unknown/Invalid Input**
   ```markdown
   **Given:** No account named "NonExistent"
   **When:** `builder.for_account("NonExistent")`
   **Then:** Returns string containing "not found" or "no data"
   ```

2. **Empty/Missing Data**
   ```markdown
   **Given:** Account exists but has no sessions
   **When:** `builder.for_account("Empty Corp")`
   **Then:** Contains "### Recent Sessions" with "No sessions" or empty list
   ```

3. **Missing Dependencies**
   ```markdown
   **Given:** Account exists in Silver but no Gold health data
   **When:** `builder.for_account("Acme")`
   **Then:** Health section contains "not computed" or "pending"
   ```

## Formula Specification

If the component calculates anything:

```markdown
## Health Score Formula

```
health_score = base + engagement_mod + risk_mod

base = 50

engagement_mod:
  +20 if days_since_engagement <= 7
  +10 if days_since_engagement <= 14
  -20 if days_since_engagement > 30

risk_mod:
  -15 per open risk (max -30)
```

### Example Calculation
Input: engagement 5 days ago, 1 open risk
Result: 50 + 20 + (-15) = 55
```

**No "see spec" references.** Include the actual formula.

## Workflow

```
┌─────────────────────────────────────┐
│ 1. Check spec for required sections │
│    - Fixtures?                      │
│    - Contracts?                     │
│    - Edge cases?                    │
│    - Exact assertions?              │
└──────────────┬──────────────────────┘
               │
       Missing sections?
               │
      ┌────────┴────────┐
      │ YES             │ NO
      ▼                 ▼
┌───────────────┐  ┌───────────────┐
│ STOP          │  │ Proceed to    │
│ Add missing   │  │ brainstorming │
│ sections      │  │ or planning   │
└───────────────┘  └───────────────┘
```

## Integration with Superpowers Workflow

This skill runs BEFORE:
- `superpowers:brainstorming` — Validate design has testable contracts
- `superpowers:writing-plans` — Ensure plan can include test-first tasks

After spec is TDD-ready:
1. Proceed to `superpowers:brainstorming` for design refinement
2. Then `superpowers:writing-plans` with test-first tasks
3. Then `superpowers:test-driven-development` during implementation

## Quick Reference

| Section | What It Contains | Example |
|---------|------------------|---------|
| Fixtures | Exact test data | `{"id": "acc-1", "name": "Providence", "health_score": 72}` |
| Contracts | Given-When-Then | "Given Providence exists, When for_account('Providence'), Then contains '72'" |
| Edge Cases | Error scenarios | "Unknown account returns 'not found'" |
| Assertions | Executable checks | `assert "72" in result` |
| Formulas | Full calculation | `health = 50 + engagement_mod + risk_mod` |

## What TDD-Ready Specs Enable

With proper specs, `superpowers:test-driven-development` can:
- Write tests FROM spec before implementation
- Use exact fixture values in assertions
- Verify content, not just types
- Catch placeholders and empty returns

Without proper specs, tests will:
- Check types instead of content
- Pass against stubs returning None
- Miss edge cases
- Require reading implementation (not TDD)

## Completion

Spec is TDD-ready when you can answer YES to all:
- [ ] Can I write `tests/fixtures/{x}_fixtures.py` from this spec?
- [ ] Can I write exact assertions without reading implementation?
- [ ] Do edge cases have specific expected outputs?
- [ ] Are all formulas fully specified?

Only then: proceed to brainstorming or planning.
