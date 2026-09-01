# Forward Roll — Claude Code Guidelines

Forward Roll provides a disciplined, jj-first development workflow for Claude Code.

## Workflow

1. **`fr-bootstrap`**: Resolve the repository contract and create `.forward-roll/runtime.json`.
2. **`fr-specify`**: Create or refine durable project specifications.
3. **`fr-plan-epic`**: Define one reviewable epic with a clear definition of done.
4. **`fr-plan-slice`**: Carve the next small, bounded execution unit from the active epic.
5. **`fr-do`**: Orchestrate the slice via `fr-impl` (TDD implementer) and `fr-review` (spec compliance).
6. **`fr-review`**: Perform a comprehensive review of the completed epic.
7. **`fr-feedback`**: Record review or operator feedback as an explicit next state.

## Core Rules

- Do not clutter VCS with planning documents. All planning artifacts reside in `.forward-roll/`.
- Maintain clean, single-change review boundaries in `jj`.
- Implement changes using red/green TDD.
