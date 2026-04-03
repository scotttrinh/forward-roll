# Slice 01-08: generate-bootstrap-skill-scripts

## Metadata

- created_at: 2026-04-03T19:33:15+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-08
- status: done
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Move the bootstrap skill's authored Python scripts under top-level src/ and generate them into plugins/forward-roll/.

## Why Now

The build already owns shared helpers, plugin-root shell assets, and every SKILL.md file, but all skill-owned Python entrypoints are still authored directly inside the generated bundle. Migrating the bootstrap skill first is the smallest next step because it establishes the source layout and build-manifest pattern for full script generation while touching only one skill directory.

## In Scope

- Add authored source files under `src/skill-templates/fr-bootstrap/scripts/` for `bootstrap.py` and `validate_skill_bundle.py`.
- Extend `src/plugin-build.json` and the existing build flow so `python3 src/build.py` emits those bootstrap scripts into `plugins/forward-roll/skills/fr-bootstrap/scripts/`.
- Update source/build documentation only where needed so contributors can see that the bootstrap skill scripts now flow from `src/` into the generated plugin bundle.

## Out Of Scope

- Moving script sources for `fr-specify`, `fr-plan-epic`, `fr-plan-slice`, `fr-do`, `fr-feedback`, or `fr-review`.
- Changing the bootstrap command surface, runtime contract fields, or validation behavior beyond relocating the authored sources.
- Adding template interpolation or broader code-generation logic for all scripts in one pass.

## Relevant Files And Systems

- `src/skill-templates/fr-bootstrap/scripts/bootstrap.py`
- `src/skill-templates/fr-bootstrap/scripts/validate_skill_bundle.py`
- `src/plugin-build.json`
- `src/build.py`
- `src/README.md`
- `plugins/forward-roll/skills/fr-bootstrap/scripts/bootstrap.py`
- `plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py`

## Acceptance Criteria

- A contributor can edit either authored bootstrap script under `src/skill-templates/fr-bootstrap/scripts/`, run `python3 src/build.py`, and see the matching generated script rewritten under `plugins/forward-roll/skills/fr-bootstrap/scripts/`.
- The generated bootstrap skill remains self-contained and stdlib-only, with no new imports from sibling skills or a shared runtime package.
- `python3 src/build.py --check` validates the expanded manifest and fails clearly if a declared bootstrap script source or target path is missing.

## Validation Strategy

- Run `python3 src/build.py` and confirm the bootstrap skill scripts are regenerated from the `src/` authored copies.
- Run `python3 src/build.py --check` to validate the updated build contract and generated-path expectations.
- Run `python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap` to confirm the generated bootstrap bundle shape remains valid after the script migration.

## jj Review Shape

One readable change that moves the bootstrap skill's authored Python scripts into `src/` and extends the current manifest-driven build to regenerate only that skill's scripts.

## Stop Condition

Stop once the bootstrap skill's Python scripts are sourced from `src/`, regenerated into the distributed bundle, documented, and locally validated; leave the remaining skill script migrations for later slices.

## Log

- 2026-04-03T19:33:15+00:00 Planned slice artifact created.


- 2026-04-03T19:44:48+00:00 Moved fr-bootstrap authored Python scripts into src and generated them back into the plugin bundle.
  - Added src/skill-templates/fr-bootstrap/scripts/bootstrap.py as the authored source for the generated bootstrap entrypoint.
  - Added src/skill-templates/fr-bootstrap/scripts/validate_skill_bundle.py as the authored source for the generated bundle validator.
  - Extended src/plugin-build.json and src/README.md so python3 src/build.py emits and documents the generated bootstrap scripts.
  - python3 src/build.py
  - python3 src/build.py --check
  - python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap
  - No blockers recorded.
  - Migrate the next skill-owned script set into src using the same manifest-driven pattern.
