# claude-skills

A collection of [Claude Code](https://claude.com/claude-code) **skills** for Databricks
solutions-architect workflows. Each top-level directory is a self-contained skill defined
by a `SKILL.md` (name + trigger description). There is no application here — the repository
*is* the flat set of skills plus a couple of shared reference docs.

## Layout

- **Skills** — one folder per skill, each containing a `SKILL.md`
- **Shared reference docs** (root):
  - `arch-diagram-quality-gate.md` — objective rubric for evaluating architecture diagrams
  - `d2-architecture-rules.md` — D2 diagramming standards and pre-flight checklist
- **Supporting folders:**
  - `theme-factory/` — shared visual themes for the render skills
  - `territory-health-dashboard/` — dashboard spec
  - `deck-render-backup-pptxgenjs/` — older `deck-render` variant
  - `.claude/` — Claude Code configuration

## Skills

### Diagrams & visuals
| Skill | Purpose |
| --- | --- |
| `arch-diagram` | Customer-grade architecture diagrams as draw.io XML with Databricks/cloud icons |
| `diagram` | Multi-format technical diagrams (D2, PlantUML, C4, Mermaid, Graphviz, ERD, BPMN) |
| `interactive-diagrams` | Clickable, zoomable diagrams (D3.js, Cytoscape.js, Vis.js) |

### Content & artifact rendering
| Skill | Purpose |
| --- | --- |
| `deck-render` | Render PowerPoint decks slide-by-slide with visual QA |
| `one-pager-render` | Executive single-page PDF one-pagers |
| `cheatsheet-render` | Single-file dark-mode HTML cheat sheets |
| `email-render` / `draft-followup` | Follow-up email drafts from session/meeting context |
| `enablement-card-render` / `enablement-kit` | Role-specific job aids and multi-artifact kits |
| `theme-factory` | Shared visual themes for the render skills |

### Orchestrators (multi-step pipelines)
| Skill | Purpose |
| --- | --- |
| `content-factory` | Objective → finished multi-artifact content |
| `demo` / `demo-narrative` / `demo-factory` | Demo creation: brainstorm → spec → narrative → build |
| `post-meeting` | Transcript → structured intelligence + follow-up actions |
| `blackboard` | Recursive parallel multi-agent work coordinator |

### Forecast & consumption (Databricks GTM)
| Skill | Purpose |
| --- | --- |
| `consumption-vault-sync` | Local consumption intelligence: query, analyze, store, sync |
| `consumption-risk-detector` | Auto-generate risk signals from weekly consumption analysis |
| `forecast-consumption-validation` | Validate forecast UCO stages against actual consumption |
| `forecast-prep` | Biweekly forecast prep automation chaining the above |
| `territory-health-dashboard` | Territory health dashboard spec |

### Databricks engineering
| Skill | Purpose |
| --- | --- |
| `databricks-apps-deployment` | Deployment patterns for Databricks Apps, Lakebase, PostGIS, FastAPI+React |
| `dbdemos-setup` | Set up a project for dbdemos contribution |

### Process & quality
| Skill | Purpose |
| --- | --- |
| `tdd-ready-specs` | Ensure specs are ready for test-first development |
| `prp-gate-verification` | Verify PRP validation gates with evidence before claiming completion |
| `grill-me` | Adversarially stress-test a plan or design |
| `evolve` | Auto-research loop for self-improving skills via binary evals |

## Usage

These are Claude Code skills. Each skill's `SKILL.md` describes when it activates and what it
does. Point Claude Code at this repository (or symlink individual skills into your skills
directory) and invoke them via their trigger phrases or `/`-commands as documented in each
`SKILL.md`.
