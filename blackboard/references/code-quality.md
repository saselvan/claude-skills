# Code Quality Rules

Paste this section verbatim into the prompt of any stream that writes code. Agents do not see SKILL.md, so referencing these rules by name does nothing.

---

Code quality rules for this work:

**Decompose.** If a function has three or more independent responsibilities, split it. Each sub-function gets its own name, docstring, and failure logging, so the dispatcher reads like a table of contents and a failure points at one place.

**Never drop silently.** When a precondition fails, log at WARNING level with enough context to find the record. `if row: ... else: pass` hides data loss; someone will spend a day finding it later.

**One filter, one place.** If the same lookup or WHERE clause appears in more than one code path, extract it into a shared helper. Divergent copies are how two reports disagree on the same number.

**Tests before done.** Run the tests for your scope. If they fail and you cannot fix them, report `status: partial` with the failing tests listed. Do not delete, skip, or weaken tests to get green.

**Stay in scope.** Only touch files in your assigned scope. If the right fix needs a change outside it, describe the change under `decisions` in your result instead of making it.
