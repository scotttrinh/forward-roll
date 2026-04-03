# Epic 01: plugin-build-pipeline

## Metadata

- created_at: 2026-04-03T16:26:01+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slug: plugin-build-pipeline
- status: planned

## Goal

Introduce a source-driven plugin authoring layout that renders templates and shared logic into self-contained Codex skill bundles.

## Why

- The current plugin duplicates identical helper scripts across skills because Codex plugins only expose skill-local files and no top-level shared scripts directory.
- A deterministic build step would let the repository author shared functionality once while still shipping the self-contained skill layout the plugin runtime expects.

## Spec Impact

- spec-update-required

## Existing System Shape

- Each Forward Roll skill lives directly under plugins/forward-roll/skills/<skill> with its own SKILL.md and stdlib-only scripts/ directory.
- resolve_context.py is copied verbatim across multiple skills, showing real authored-repo duplication already exists.
- Plugin metadata points Codex at a static ./skills/ directory, so the shipped layout is the authoring layout today.

## Proposed Change Shape

- Add a repository-local source tree for shared script logic, skill templates, and any reusable prompt fragments used during plugin authoring.
- Add a deterministic build command that materializes plugins/forward-roll/.codex-plugin and plugins/forward-roll/skills from source templates and shared assets.
- Ensure generated skill bundles remain self-contained, stdlib-only, and free of cross-skill runtime imports.

## Relevant Code References

- plugins/forward-roll/.codex-plugin/plugin.json
- plugins/forward-roll/skills/fr-plan-epic/scripts/resolve_context.py
- plugins/forward-roll/skills/fr-plan-slice/scripts/resolve_context.py
- plugins/forward-roll/skills/fr-do/scripts/resolve_context.py
- plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py
- .forward-roll/specs/architecture.md

## Constraints And Risks

- The distributed plugin contract must stay compatible with Codex plugin expectations: self-contained skills and no shared runtime package.
- Build outputs need to be deterministic so generated bundles can be reviewed and validated reliably.
- Development tooling can be richer than runtime tooling, but shipped helpers must stay stdlib-only.

## Definition Of Done

- The repository has an explicit source/build layout for authoring plugin assets and generating final skill bundles.
- At least one currently duplicated helper path is sourced from shared authored code and emitted into multiple generated skills.
- Documentation explains which directories are source-of-truth, which are generated, and how to rebuild the plugin layout.

## Acceptance Criteria

- A contributor can edit shared plugin logic once, run the build step, and see the change reflected in every affected generated skill bundle.
- Generated skills pass the existing bundle validation checks and preserve the current operator-facing command surface.
- The build process fails clearly when source templates or required generated outputs are inconsistent.

## Manual Verification

- Modify a shared source asset, run the build command, and confirm the corresponding generated files under plugins/forward-roll/skills change as expected.
- Run the skill-bundle validator and Python constraint checks against the generated output.
- Inspect a generated skill directory to confirm it remains self-contained with no imports from sibling skills or top-level runtime packages.

## Slice Plan

- Define the source-of-truth layout and build contract, including what is generated versus hand-authored.
- Implement the build pipeline and migrate one duplicated helper/template path to shared authored sources.
- Migrate the remaining duplicated skill assets, then update validation and contributor documentation around generated output.

## Open Questions

- Should generated plugin assets remain checked in, or should the build become a required packaging step for release and local validation?
- Do SKILL.md files need full templating support, or is shared script generation the primary requirement for the first pass?
