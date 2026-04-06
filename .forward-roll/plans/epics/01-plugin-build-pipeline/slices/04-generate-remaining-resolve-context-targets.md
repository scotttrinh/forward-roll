# Slice 01-04: generate-remaining-resolve-context-targets

## Metadata

- created_at: 2026-04-03T17:30:52+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-04
- status: completed
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Extend the shared resolve_context generation path to the remaining skills that still duplicate the same helper.

## Why Now

Slice 01-03 proved the src-to-plugin generation path for the planning skills, and the repo still carries identical resolve_context.py copies in fr-do, fr-feedback, and fr-review. Extending the same mechanism to those remaining verbatim targets is the smallest follow-on slice that deepens the build pipeline without expanding into broader skill templating.

## In Scope

- Add the remaining identical resolve_context.py targets to src/plugin-build.json.
- Update the build and docs only as needed so python3 src/build.py clearly owns regeneration of the helper for fr-do, fr-feedback, and fr-review.
- Preserve the current runtime contract and operator-facing command surface while replacing handwritten duplication with generated outputs.

## Out Of Scope

- Templating SKILL.md files or regenerating full skill directories.
- Refactoring non-identical scripts that need separate design work.
- Changing how runtime context resolution behaves.

## Relevant Files And Systems

- src/shared-scripts/resolve_context.py
- src/plugin-build.json
- src/build.py
- plugins/forward-roll/skills/fr-do/scripts/resolve_context.py
- plugins/forward-roll/skills/fr-feedback/scripts/resolve_context.py
- plugins/forward-roll/skills/fr-review/scripts/resolve_context.py
- plugins/forward-roll/README.md

## Acceptance Criteria

- A contributor can edit src/shared-scripts/resolve_context.py, run python3 src/build.py, and see the generated helper updated in fr-plan-epic, fr-plan-slice, fr-do, fr-feedback, and fr-review.
- The generated helper files in all targeted skills remain self-contained, stdlib-only, and byte-for-byte aligned with the shared authored source after generation.
- The manifest-driven build fails clearly if the shared helper source is missing or a declared target path is invalid.

## Validation Strategy

- Run python3 src/build.py and confirm the generated helper is emitted to all targeted skill paths.
- Run python3 src/build.py --check to validate the manifest and path contract.
- Run python3 scripts/validate_python_constraints.py on the shared helper and the targeted generated helper paths.

## jj Review Shape

One readable change that extends the existing shared-script generation mechanism from the planning skills to the remaining identical resolve_context consumers.

## Stop Condition

Stop once the remaining identical resolve_context.py copies are manifest-driven build outputs, the docs reflect the broader target set, and local validation passes; leave non-identical asset generation for later slices.

## Log

- 2026-04-03T17:30:52+00:00 Planned slice artifact created.


- 2026-04-03T19:02:47+00:00 Added fr-do, fr-feedback, and fr-review resolve_context.py targets to the build manifest, regenerated the shared helper across all five targeted skills, and updated build documentation. Validation: python3 src/build.py; python3 src/build.py --check; python3 scripts/validate_python_constraints.py src/shared-scripts/resolve_context.py plugins/forward-roll/skills/fr-plan-epic/scripts/resolve_context.py plugins/forward-roll/skills/fr-plan-slice/scripts/resolve_context.py plugins/forward-roll/skills/fr-do/scripts/resolve_context.py plugins/forward-roll/skills/fr-feedback/scripts/resolve_context.py plugins/forward-roll/skills/fr-review/scripts/resolve_context.py
  - No detailed change summary recorded.
  - Validation not recorded for this run.
  - No blockers recorded.
  - No next step recorded.
