# Slice 01-06: generate-plugin-shell-assets

## Metadata

- created_at: 2026-04-03T19:14:38+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-06
- status: done
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Move the plugin distribution shell assets under top-level src/ and generate them into plugins/forward-roll/.

## Why Now

The build currently owns only a shared helper script, while the generated bundle root still contains hand-authored README and plugin metadata. Moving those static shell assets into src/ establishes the generated distribution boundary more clearly before broader skill-directory templating.

## In Scope

- Add authored source files under src/ for plugins/forward-roll/README.md and plugins/forward-roll/.codex-plugin/plugin.json.
- Extend the manifest-driven build so python3 src/build.py can materialize those static distribution assets into the generated plugin root.
- Update authoring/build documentation only where needed to reflect that these distribution shell assets now come from src/.

## Out Of Scope

- Generating SKILL.md files or full skill directories from templates.
- Refactoring runtime script behavior or changing the operator-facing command surface.
- Removing plugins/forward-roll/ from version control or completing the full dist-only packaging story.

## Relevant Files And Systems

- src/plugin-build.json
- src/build.py
- src/README.md
- plugins/forward-roll/README.md
- plugins/forward-roll/.codex-plugin/plugin.json

## Acceptance Criteria

- A contributor can edit the authored README or plugin metadata under src/, run python3 src/build.py, and see the corresponding files regenerated under plugins/forward-roll/.
- The build manifest validates the new static generated asset entries and fails clearly when a declared source path is missing.
- The generated README and plugin metadata remain deterministic and preserve the current plugin identity and operator-facing surface.

## Validation Strategy

- Run python3 src/build.py and confirm the generated README and plugin.json are rewritten from src-authored inputs.
- Run python3 src/build.py --check to validate the expanded manifest and path contract.
- Run python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap plugins/forward-roll/skills/fr-specify plugins/forward-roll/skills/fr-plan-epic plugins/forward-roll/skills/fr-plan-slice plugins/forward-roll/skills/fr-do plugins/forward-roll/skills/fr-feedback plugins/forward-roll/skills/fr-review to confirm the generated shell asset work does not disturb bundle shape.

## jj Review Shape

One readable change that moves the plugin bundle shell assets out of the generated root as authored source while extending the existing build to render them deterministically.

## Stop Condition

Stop once README.md and .codex-plugin/plugin.json are sourced from src/, the build regenerates them into plugins/forward-roll/, and local validation passes; leave skill templating and broader bundle generation for later slices.

## Log

- 2026-04-03T19:14:38+00:00 Planned slice artifact created.


- 2026-04-03T19:20:59+00:00 Moved the plugin shell README and metadata into src/plugin-shell and generated them into plugins/forward-roll/.
  - Added src/plugin-shell/README.md and src/plugin-shell/.codex-plugin/plugin.json as authored source-of-truth files.
  - Extended src/plugin-build.json so python3 src/build.py generates plugins/forward-roll/README.md and plugins/forward-roll/.codex-plugin/plugin.json.
  - Updated src/README.md and plugins/forward-roll/README.md to document the new plugin-shell authoring paths and generated outputs.
  - python3 src/build.py
  - python3 src/build.py --check
  - python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap plugins/forward-roll/skills/fr-specify plugins/forward-roll/skills/fr-plan-epic plugins/forward-roll/skills/fr-plan-slice plugins/forward-roll/skills/fr-do plugins/forward-roll/skills/fr-feedback plugins/forward-roll/skills/fr-review
  - No blockers recorded.
  - Leave full skill-directory templating and broader dist-only generation for later slices.
