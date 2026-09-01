# OMP Tool Mapping

## Configuration

Forward Roll requires non-isolated task subagents so `fr-impl` and `fr-review` operate directly on working-copy change `@`.

Ensure `.omp/config.yml` contains:

```yaml
task:
  isolation:
    mode: none
```

## Agent Definitions

Agent markdown definitions are located in `agents/`:
- `agents/fr-impl.md` (TDD implementer with tools: `read`, `grep`, `glob`, `edit`, `write`, `bash`)
- `agents/fr-review.md` (Read-only spec reviewer with tools: `read`, `grep`, `glob`, `ast_grep`)

## Tool Equivalents

| Action | OMP Tool | Notes |
|---|---|---|
| **Dispatch Implementer** | `task` (`agent: "fr-impl"`) | Non-isolated subagent (`task.isolation.mode: none`). |
| **Dispatch Reviewer** | `task` (`agent: "fr-review"`) | Validates acceptance criteria + spec compliance. |
| **Run `jj` History Surgery** | `bash` (`jj describe ...`, `jj squash`) | Orchestrator runs `jj`. Subagents do not touch `jj`. |
