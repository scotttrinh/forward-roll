# Slice 01-03: generate-shared-resolve-context

## Metadata

- created_at: 2026-04-03T17:19:30+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-03
- status: completed
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Teach the build pipeline to source one shared resolve_context helper from top-level src/ and emit it into the generated plugin bundle.

## Why Now

Epic 01 now has the source/build boundary in place, but src/build.py still only validates the contract. Generating one duplicated helper path next proves the boundary is executable without expanding into full skill templating or a complete plugin rebuild.

## In Scope

- Add one authored shared helper source under src/ for the resolve_context logic currently duplicated across skills.
- Extend src/build.py so it can materialize that helper into the appropriate generated skill script paths under plugins/forward-roll/.
- Choose the smallest initial target set that already shares identical helper logic, such as the planning skills with matching resolve_context.py contents.
- Update docs or manifest notes only where needed to explain the first generated asset path.

## Out Of Scope

- Templating every skill bundle or regenerating the full plugin tree from src/.
- Changing the operator-facing Forward Roll commands or the runtime contract shape.
- Deduplicating non-identical helper scripts that need separate design work.

## Relevant Files And Systems

- src/build.py
- src/shared-scripts/
- src/plugin-build.json
- plugins/forward-roll/skills/fr-plan-epic/scripts/resolve_context.py
- plugins/forward-roll/skills/fr-plan-slice/scripts/resolve_context.py
- plugins/forward-roll/README.md
- .forward-roll/specs/architecture.md

## Acceptance Criteria

- A contributor can edit one shared resolve_context source under src/, run the build entrypoint, and see the generated helper updated in the targeted plugin skill directories.
- The generated helper files remain self-contained, stdlib-only script files with no imports from sibling skills or a shared runtime package.
- The initial generation target is intentionally narrow and leaves the rest of the checked-in plugin bundle untouched unless required by the selected helper path.
- The build command fails clearly when the authored shared helper input is missing or inconsistent.

## Validation Strategy

- Run python3 src/build.py and confirm the targeted generated helper paths are updated under plugins/forward-roll/.
- Inspect the emitted skill scripts to confirm they stay self-contained and preserve the current command surface.
- Run python3 scripts/validate_python_constraints.py if touched paths affect shipped Python scripts.

## jj Review Shape

One readable change that introduces the first real src-to-plugin generation path and shows a duplicated helper now flows from shared authored source into generated skill bundles.

## Stop Condition

Stop once one duplicated helper path is authored under src/, generated into a narrow set of plugin skill directories, documented where necessary, and validated locally; leave broader skill generation and additional deduplication for later slices.

## Log

- 2026-04-03T17:19:30+00:00 Planned slice artifact created.


- 2026-04-03T17:22:36+00:00 Implemented the first shared resolve_context generation path from src into the planning skills.
  - Added src/shared-scripts/resolve_context.py as the authored source of truth for the planning skills' resolve_context helper.
  - Extended src/plugin-build.json and src/build.py so the build validates and copies that shared helper into fr-plan-epic and fr-plan-slice.
  - Documented the first generated asset path in src/README.md and plugins/forward-roll/README.md.
  - python3 src/build.py
  - python3 src/build.py --check
  - python3 scripts/validate_python_constraints.py plugins/forward-roll/skills/fr-plan-epic/scripts/resolve_context.py plugins/forward-roll/skills/fr-plan-slice/scripts/resolve_context.py src/shared-scripts/resolve_context.py
  - No blockers recorded.
  - Expand generation to additional duplicated skill assets in a later slice once the first shared-script path is established.
