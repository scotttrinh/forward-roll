# Slice 01-09: generate-remaining-skill-scripts

## Metadata

- created_at: 2026-04-04T12:31:11+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-09
- status: completed
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Move every remaining skill-owned Python entrypoint under top-level src/ and generate those scripts into plugins/forward-roll/.

## Why Now

The build already owns every SKILL.md asset, the shared resolve_context helper, and the bootstrap skill's authored scripts. The only authored plugin assets still living directly under plugins/forward-roll/ are the remaining skill-owned Python entrypoints, so migrating them together would finish the source-to-plugin boundary for this epic instead of leaving one final round of small script moves.

## In Scope

- Add authored source files under src/skill-templates/ for the remaining non-generated skill scripts: fr-specify/scripts/specify.py, fr-plan-epic/scripts/plan_epic.py, fr-plan-slice/scripts/plan_slice.py, fr-do/scripts/do.py, fr-feedback/scripts/feedback.py, and fr-review/scripts/review.py.
- Extend src/plugin-build.json and the existing build flow so python3 src/build.py emits those six scripts into their matching plugins/forward-roll/skills/*/scripts/ targets.
- Update source/build documentation only where needed so contributors can see that the remaining skill-owned Python entrypoints now flow from src/ into the generated plugin bundle.

## Out Of Scope

- Changing any skill's command surface, runtime contract fields, or artifact formats beyond relocating authored sources into src/.
- Introducing broader script templating, shared runtime imports between shipped skills, or new cross-skill abstractions.
- Removing plugins/forward-roll/ from version control or changing the generated bundle layout beyond these remaining script targets.

## Relevant Files And Systems

- src/skill-templates/fr-specify/scripts/specify.py
- src/skill-templates/fr-plan-epic/scripts/plan_epic.py
- src/skill-templates/fr-plan-slice/scripts/plan_slice.py
- src/skill-templates/fr-do/scripts/do.py
- src/skill-templates/fr-feedback/scripts/feedback.py
- src/skill-templates/fr-review/scripts/review.py
- src/plugin-build.json
- src/build.py
- src/README.md
- plugins/forward-roll/skills/fr-specify/scripts/specify.py
- plugins/forward-roll/skills/fr-plan-epic/scripts/plan_epic.py
- plugins/forward-roll/skills/fr-plan-slice/scripts/plan_slice.py
- plugins/forward-roll/skills/fr-do/scripts/do.py
- plugins/forward-roll/skills/fr-feedback/scripts/feedback.py
- plugins/forward-roll/skills/fr-review/scripts/review.py

## Acceptance Criteria

- A contributor can edit any of the remaining authored skill scripts under src/skill-templates/, run python3 src/build.py, and see the matching generated script rewritten deterministically under plugins/forward-roll/skills/*/scripts/.
- The generated remaining skill scripts stay self-contained and stdlib-only, with no imports from sibling skills or a shared runtime package.
- python3 src/build.py --check fails clearly if any declared remaining skill script source path or generated target path is missing.

## Validation Strategy

- Run python3 src/build.py and confirm the remaining skill entrypoints are regenerated from src/.
- Run python3 src/build.py --check to validate the updated build contract and generated-path expectations.
- Run python3 scripts/validate_python_constraints.py src/skill-templates/fr-specify/scripts/specify.py src/skill-templates/fr-plan-epic/scripts/plan_epic.py src/skill-templates/fr-plan-slice/scripts/plan_slice.py src/skill-templates/fr-do/scripts/do.py src/skill-templates/fr-feedback/scripts/feedback.py src/skill-templates/fr-review/scripts/review.py plugins/forward-roll/skills/fr-specify/scripts/specify.py plugins/forward-roll/skills/fr-plan-epic/scripts/plan_epic.py plugins/forward-roll/skills/fr-plan-slice/scripts/plan_slice.py plugins/forward-roll/skills/fr-do/scripts/do.py plugins/forward-roll/skills/fr-feedback/scripts/feedback.py plugins/forward-roll/skills/fr-review/scripts/review.py
- Run python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap plugins/forward-roll/skills/fr-specify plugins/forward-roll/skills/fr-plan-epic plugins/forward-roll/skills/fr-plan-slice plugins/forward-roll/skills/fr-do plugins/forward-roll/skills/fr-feedback plugins/forward-roll/skills/fr-review to confirm the expanded script generation still preserves the expected bundle shape.

## jj Review Shape

Keep one readable change that moves the remaining skill-owned Python entrypoints into src and extends the manifest-driven build to regenerate those last authored scripts.

## Stop Condition

Stop once every remaining skill-owned Python entrypoint is sourced from src/, regenerated into the distributed bundle, documented, and locally validated; leave any post-epic cleanup or packaging policy changes for later work.

## Log

- 2026-04-04T12:31:11+00:00 Planned slice artifact created.


- 2026-04-04T12:42:13+00:00 Moved remaining skill-owned Python entrypoints under src and generated them into the plugin bundle
  - Added authored sources for fr-specify, fr-plan-epic, fr-plan-slice, fr-do, fr-feedback, and fr-review under src/skill-templates/*/scripts/.
  - Extended src/plugin-build.json so python3 src/build.py emits those six scripts into plugins/forward-roll/skills/*/scripts/.
  - Updated source/build documentation to state that all shipped skill-owned Python entrypoints now originate from src/.
  - python3 src/build.py
  - python3 src/build.py --check
  - python3 scripts/validate_python_constraints.py src/skill-templates/fr-specify/scripts/specify.py src/skill-templates/fr-plan-epic/scripts/plan_epic.py src/skill-templates/fr-plan-slice/scripts/plan_slice.py src/skill-templates/fr-do/scripts/do.py src/skill-templates/fr-feedback/scripts/feedback.py src/skill-templates/fr-review/scripts/review.py plugins/forward-roll/skills/fr-specify/scripts/specify.py plugins/forward-roll/skills/fr-plan-epic/scripts/plan_epic.py plugins/forward-roll/skills/fr-plan-slice/scripts/plan_slice.py plugins/forward-roll/skills/fr-do/scripts/do.py plugins/forward-roll/skills/fr-feedback/scripts/feedback.py plugins/forward-roll/skills/fr-review/scripts/review.py
  - python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap plugins/forward-roll/skills/fr-specify plugins/forward-roll/skills/fr-plan-epic plugins/forward-roll/skills/fr-plan-slice plugins/forward-roll/skills/fr-do plugins/forward-roll/skills/fr-feedback plugins/forward-roll/skills/fr-review
  - No blockers recorded.
  - A follow-on slice can move additional generated assets or build validations into src if the plugin contract expands further.
