# Integrations

How other coordinators invoke blackboard. In every case the caller passes pre-decomposed `streams` (skipping Step 1) and a `synthesis_schema` or preset, then reads `artifacts/SYNTHESIS.*` from the nested board.

Invocation shape:

```
blackboard(
  task: "...",
  streams: [...],                       # full stream schema from SKILL.md Step 1
  synthesis_schema: {...} | synthesis_format: "preset",
  --nested {parent_board_dir} {parent_depth}
)
```

## Design-ops

### `/design discover` — parallel interface exploration

Four `Plan` agents each design the same module boundary from a different bias. None is critical; design-ops presents whichever return.

```yaml
streams:
  - {name: minimize-interface,      agent_type: Plan, critical: false, writes_files: false, timeout_min: 10}
  - {name: maximize-flexibility,    agent_type: Plan, critical: false, writes_files: false, timeout_min: 10}
  - {name: optimize-common-caller,  agent_type: Plan, critical: false, writes_files: false, timeout_min: 10}
  - {name: ports-and-adapters,      agent_type: Plan, critical: false, writes_files: false, timeout_min: 10}
synthesis_schema:
  output_format: markdown
  required_fields: [interface_signature, usage_example, hidden_complexity, tradeoffs]
```

### `/design prp` — validator + red-team (LARGE tier)

Both critical: a PRP with only one of the two reviews is not reviewed.

```yaml
streams:
  - {name: invariant-validation, agent_type: general-purpose, critical: true, writes_files: false, timeout_min: 15}
  - {name: red-team-review,      agent_type: general-purpose, critical: true, writes_files: false, timeout_min: 15}
synthesis_schema:
  output_format: yaml
  required_fields: [blocking_violations, advisory_violations, adversarial_findings, confidence_adjustment]
```

### `/design build` — parallel independent issues

After `/prp-to-issues` produces the dependency graph, design-ops groups issues that share a parent but not each other. One blackboard run per group; each issue is a write stream with a disjoint `scope`.

```yaml
target_branch: feature/xyz
streams:
  - name: issue-2-api-endpoints
    agent_type: general-purpose
    critical: true
    writes_files: true
    timeout_min: 30
    scope: ["src/api/**", "tests/api/**"]
  - name: issue-3-auth-middleware
    agent_type: general-purpose
    critical: true
    writes_files: true
    timeout_min: 30
    scope: ["src/middleware/auth*", "tests/middleware/**"]
synthesis_format: build-result
```

Blackboard merges both branches into `target_branch`, runs the integration suite, and reports. Design-ops reads `merge_status` and `tests_passed` per stream to decide whether to continue to the next group or stop for conflict resolution.

## Content-factory

```yaml
streams:
  - {name: render-deck,       agent_type: general-purpose, critical: true,  writes_files: true, scope: ["out/deck/**"]}
  - {name: render-cheatsheet, agent_type: general-purpose, critical: false, writes_files: true, scope: ["out/cheatsheet/**"]}
  - {name: render-one-pager,  agent_type: general-purpose, critical: false, writes_files: true, scope: ["out/one-pager/**"]}
synthesis_format: artifact-metadata
```

## Demo-factory

`deploy-resources` runs shell commands and writes state files, so it is `general-purpose`, not a separate "Bash" type (which does not exist).

```yaml
streams:
  - {name: scaffold-app,      agent_type: general-purpose, critical: true, writes_files: true, scope: ["app/**"]}
  - {name: deploy-resources,  agent_type: general-purpose, critical: true, writes_files: true, scope: ["infra/**", ".demo-state/**"]}
  - {name: generate-frontend, agent_type: general-purpose, critical: true, writes_files: true, scope: ["app/frontend/**"], depends_on: [scaffold-app]}
synthesis_format: demo-deployment
```
