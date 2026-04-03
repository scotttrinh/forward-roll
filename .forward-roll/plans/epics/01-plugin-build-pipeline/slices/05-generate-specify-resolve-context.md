# Slice 01-05: generate-specify-resolve-context

## Metadata

- created_at: 2026-04-03T19:10:05+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-05
- status: done
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Extend the shared resolve_context generation path to fr-specify so every identical helper copy is sourced from top-level src/.

## Why Now

Slice 01-04 expanded the shared helper to several remaining skills, but fr-specify still contains the same handwritten resolve_context.py. Finishing that last identical consumer keeps the generation boundary coherent before broader plugin-bundle templating or rebuild work.

## In Scope

- Add plugins/forward-roll/skills/fr-specify/scripts/resolve_context.py as a generated target in src/plugin-build.json.
- Update build or docs only where needed so python3 src/build.py clearly owns regeneration of the fr-specify helper too.
- Preserve fr-specify's current behavior and operator-facing command surface while replacing the handwritten duplicate with generated output.

## Out Of Scope

- Templating SKILL.md files or regenerating full skill directories.
- Refactoring non-identical scripts such as specify.py or bootstrap.py.
- Completing the broader work to rebuild plugins/forward-roll/ entirely from src/.

## Relevant Files And Systems

- src/shared-scripts/resolve_context.py
- src/plugin-build.json
- src/build.py
- plugins/forward-roll/skills/fr-specify/scripts/resolve_context.py
- plugins/forward-roll/README.md

## Acceptance Criteria

- A contributor can edit src/shared-scripts/resolve_context.py, run python3 src/build.py, and see the generated helper updated in fr-plan-epic, fr-plan-slice, fr-do, fr-feedback, fr-review, and fr-specify.
- The fr-specify resolve_context.py file remains self-contained, stdlib-only, and byte-for-byte aligned with the shared authored source after generation.
- The manifest-driven build fails clearly if the shared helper source is missing or the fr-specify target path is invalid.

## Validation Strategy

- Run python3 src/build.py and confirm the generated helper is emitted to the fr-specify skill path alongside the existing targets.
- Run python3 src/build.py --check to validate the manifest and path contract.
- Run python3 scripts/validate_python_constraints.py src/shared-scripts/resolve_context.py plugins/forward-roll/skills/fr-plan-epic/scripts/resolve_context.py plugins/forward-roll/skills/fr-plan-slice/scripts/resolve_context.py plugins/forward-roll/skills/fr-do/scripts/resolve_context.py plugins/forward-roll/skills/fr-feedback/scripts/resolve_context.py plugins/forward-roll/skills/fr-review/scripts/resolve_context.py plugins/forward-roll/skills/fr-specify/scripts/resolve_context.py

## jj Review Shape

One readable change that finishes the shared resolve_context rollout by moving the last identical consumer under the existing manifest-driven generation path.

## Stop Condition

Stop once fr-specify is included in the existing shared helper generation path, the docs reflect the full target set, and local validation passes; leave broader bundle templating and full rebuild work for later slices.

## Log

- 2026-04-03T19:10:05+00:00 Planned slice artifact created.


- 2026-04-03T19:12:24+00:00 Added fr-specify to the shared resolve_context build targets and updated build documentation.
  - Added plugins/forward-roll/skills/fr-specify/scripts/resolve_context.py to src/plugin-build.json generated targets.
  - Updated src/README.md and plugins/forward-roll/README.md to describe fr-specify as part of the shared helper generation path.
  - python3 src/build.py
  - python3 src/build.py --check
  - python3 scripts/validate_python_constraints.py src/shared-scripts/resolve_context.py plugins/forward-roll/skills/fr-plan-epic/scripts/resolve_context.py plugins/forward-roll/skills/fr-plan-slice/scripts/resolve_context.py plugins/forward-roll/skills/fr-do/scripts/resolve_context.py plugins/forward-roll/skills/fr-feedback/scripts/resolve_context.py plugins/forward-roll/skills/fr-review/scripts/resolve_context.py plugins/forward-roll/skills/fr-specify/scripts/resolve_context.py
  - No blockers recorded.
  - Leave broader plugin bundle templating and full rebuild generation for later slices.
