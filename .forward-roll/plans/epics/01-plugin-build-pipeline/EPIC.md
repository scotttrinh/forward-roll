# Epic 01: plugin-build-pipeline

## Metadata

- created_at: 2026-04-03T16:26:01+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slug: plugin-build-pipeline
- status: planned

## Goal

Introduce a source-driven plugin authoring layout that uses top-level `src/` as the source of truth and builds the distributable plugin bundle at `plugins/forward-roll/`.

## Why

- The current plugin duplicates identical helper scripts across skills because Codex plugins only expose skill-local files and no top-level shared scripts directory.
- A deterministic build step would let the repository author shared functionality once while still shipping the self-contained skill layout the plugin runtime expects.
- A generated plugin bundle under `plugins/forward-roll/` makes local development and CI agree on the same packaging boundary instead of treating the distributed layout as authored source.

## Spec Impact

- spec-update-required

## Existing System Shape

- Each Forward Roll skill lives directly under plugins/forward-roll/skills/<skill> with its own SKILL.md and stdlib-only scripts/ directory.
- resolve_context.py is copied verbatim across multiple skills, showing real authored-repo duplication already exists.
- Plugin metadata points Codex at a static ./skills/ directory, so the distributed plugin layout is still conflated with the authored layout today.
- The current authored-source scaffolding also lives under plugins/forward-roll/, which means the source and distribution boundaries are still mixed together.

## Proposed Change Shape

- Add a top-level `src/` tree for shared script logic, skill templates, prompt fragments, build metadata, and any other inputs needed to build the plugin from scratch.
- Move the current authored-source scaffolding out of `plugins/forward-roll/` and into `src/` so the generated plugin bundle has a clean distribution boundary.
- Add a deterministic build command that materializes a complete `plugins/forward-roll/` bundle, including `.codex-plugin` metadata and generated `skills/`, from source templates and shared assets.
- Make `plugins/forward-roll/` disposable build output so CI and local development both regenerate the same plugin artifact instead of relying on checked-in generated files as source.
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

- The repository has an explicit source/build layout with top-level `src/` as the source of truth and `plugins/forward-roll/` as the generated plugin bundle.
- At least one currently duplicated helper path is sourced from shared authored code and emitted into multiple generated skills.
- Documentation explains which directories are source-of-truth, which are generated, and how to rebuild `plugins/forward-roll/` from scratch.

## Acceptance Criteria

- A contributor can edit shared plugin logic once under top-level `src/`, run the build step, and see the change reflected in the generated plugin bundle under `plugins/forward-roll/`.
- Generated skills pass the existing bundle validation checks and preserve the current operator-facing command surface.
- The build process can recreate `plugins/forward-roll/` from source after the generated bundle has been removed or relocated and fails clearly when source templates are inconsistent.

## Manual Verification

- Move aside or remove the generated plugin bundle under `plugins/forward-roll/`, modify a shared source asset under top-level `src/`, run the build command, and confirm the expected generated files reappear under `plugins/forward-roll/`.
- Run the skill-bundle validator and Python constraint checks against the generated output.
- Inspect a generated skill directory under `plugins/forward-roll/skills/` to confirm it remains self-contained with no imports from sibling skills or top-level runtime packages.

## Slice Plan

- Define the source-of-truth layout and build contract, including top-level `src/` as the full authoring root and `plugins/forward-roll/` as the generated distribution boundary.
- Move the existing authored-source scaffolding into its eventual home under `src/` and keep the generated bundle boundary explicit.
- Implement the build pipeline and migrate duplicated helper or template paths to shared authored sources.
- Update validation, packaging, and contributor documentation around generated output.

## Open Questions

- Do SKILL.md files need full templating support, or is shared script generation the primary requirement for the first pass?
