# Slice 01-07: generate-skill-markdown-assets

## Metadata

- created_at: 2026-04-03T19:24:09+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-07
- status: planned
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Move the plugin SKILL.md assets under top-level src/ and generate them into plugins/forward-roll/.

## Why Now

The build now owns shared helper scripts and plugin-root shell assets, but the distributed skill definitions themselves are still hand-authored inside plugins/forward-roll/. Moving those static SKILL.md files into src/ is the next smallest step toward rebuilding the full plugin bundle from source without taking on script templating in the same slice.

## In Scope

- Add authored source files under src/skill-templates/ for the current skill SKILL.md assets.
- Extend the manifest-driven build so python3 src/build.py emits those SKILL.md files into the corresponding plugins/forward-roll/skills/*/SKILL.md targets.
- Update source/build documentation only where needed so contributors can see that SKILL.md assets now flow from src/ into the generated plugin bundle.

## Out Of Scope

- Templating or regenerating the skill-owned Python scripts such as bootstrap.py, specify.py, or plan_epic.py.
- Changing any operator-facing command names, workflow semantics, or skill instructions beyond relocation into authored source files.
- Removing plugins/forward-roll/ from version control or finishing the broader dist-only packaging story.

## Relevant Files And Systems

- src/skill-templates/
- src/plugin-build.json
- src/build.py
- src/README.md
- plugins/forward-roll/skills/fr-bootstrap/SKILL.md
- plugins/forward-roll/skills/fr-specify/SKILL.md
- plugins/forward-roll/skills/fr-plan-epic/SKILL.md
- plugins/forward-roll/skills/fr-plan-slice/SKILL.md
- plugins/forward-roll/skills/fr-do/SKILL.md
- plugins/forward-roll/skills/fr-feedback/SKILL.md
- plugins/forward-roll/skills/fr-review/SKILL.md

## Acceptance Criteria

- A contributor can edit a skill definition under src/skill-templates/, run python3 src/build.py, and see the corresponding plugins/forward-roll/skills/*/SKILL.md files regenerated deterministically.
- The generated SKILL.md files preserve the current operator-facing workflow surface and remain standalone plugin assets with no runtime coupling between skills.
- The build manifest validates the new generated SKILL.md entries and fails clearly when a declared source file or target path is missing.

## Validation Strategy

- Run python3 src/build.py and confirm the generated SKILL.md files are rewritten from src-authored sources into plugins/forward-roll/skills/.
- Run python3 src/build.py --check to validate the expanded manifest and path contract.
- Run python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap plugins/forward-roll/skills/fr-specify plugins/forward-roll/skills/fr-plan-epic plugins/forward-roll/skills/fr-plan-slice plugins/forward-roll/skills/fr-do plugins/forward-roll/skills/fr-feedback plugins/forward-roll/skills/fr-review to confirm the generated SKILL.md work preserves the expected bundle shape.

## jj Review Shape

One readable change that moves the static skill definitions under src/ and extends the existing manifest-driven build to emit those files into the generated plugin bundle.

## Stop Condition

Stop once the current SKILL.md assets are sourced from src/, regenerated into plugins/forward-roll/, documented, and locally validated; leave Python script generation and broader bundle templating for later slices.

## Log

- 2026-04-03T19:24:09+00:00 Planned slice artifact created.


- 2026-04-03T19:27:13+00:00 Moved SKILL.md authored sources into src/skill-templates, extended the build manifest to regenerate distributed skill markdown, and validated with python3 src/build.py, python3 src/build.py --check, and the skill bundle validator.
  - No detailed change summary recorded.
  - Validation not recorded for this run.
  - No blockers recorded.
  - No next step recorded.
