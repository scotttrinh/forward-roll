# Forward Roll — Agent Guidelines

When Forward Roll is active in a repository, adhere to the Forward Roll development loop:

1. **Bootstrap First**: Ensure the runtime contract is resolved (`.forward-roll/runtime.json`) before planning or executing changes.
2. **Durable Specs**: Keep architecture, user flows, and codebase invariants in specs (`.forward-roll/specs/`), not in transient chat logs.
3. **Epic & Slice Decomposition**: Plan one reviewable epic at a time, broken down into small, bounded slices (`.forward-roll/plans/epics/<id>-<slug>/`).
4. **`jj`-First Review Boundaries**:
   - The orchestrator (`fr-do`) manages all Jujutsu (`jj`) history.
   - Slices accumulate in the working copy `@`, described with `jj describe`.
   - Subagents (`fr-impl`, `fr-review`) operate on the shared workspace and never execute `jj` commands.
   - On clean review (`ship`), the working copy changes are folded into a single clean change with `jj squash`.
5. **No Planning Clutter in Git/jj**: All specs, epics, slices, ledgers, and task briefs live in `.forward-roll/`, which is ignored by VCS.
