# Forward Roll — Agent Guidelines

When Forward Roll is active in a repository, adhere to the Forward Roll development loop:

1. **Bootstrap First**: Ensure the runtime contract is resolved (`.forward-roll/runtime.json`) before planning or executing changes.
2. **Forward-Facing Living Specs**: Maintain living domain dossiers (`.forward-roll/specs/`) capturing point-in-time ground truth research, the vector of change, and durable invariants—never static imaginary future blueprints.
3. **Dual-Track Execution**:
   - **Structured Epic Track**: For broad features or multi-slice milestones, decompose into reviewable epics and bounded slices (`.forward-roll/plans/epics/<id>-<slug>/`).
   - **Inline Fast Track**: For small, bounded changes (bugfixes, quick helpers, follow-ups), use `fr-specify --mode fast-track` to formulate the minimal epic and single slice upfront in one shot.
4. **Archetype Playbooks & TDD**: Execute slices according to their archetype (`bugfix`, `refactor`, `feature`, `perf`, `visual-parity`), applying red-green TDD, minimal blast radius, and anti-slop discipline.
5. **Anti-Slop & `jj`-First Review Boundaries**:
   - Slices accumulate in the working copy `@`, described with `jj describe`.
   - Subagents (`fr-impl`, `fr-review`) operate on the shared workspace and never execute `jj` commands.
   - `fr-review` enforces acceptance criteria, test coverage, comment hygiene (no narrative AI comments), and anti-slop standards.
   - On clean review (`ship`), the working copy changes are folded into a single clean change with `jj squash`.
6. **No Planning Clutter in Git/jj**: All specs, epics, slices, ledgers, and task briefs live in `.forward-roll/`, which is ignored by VCS.
