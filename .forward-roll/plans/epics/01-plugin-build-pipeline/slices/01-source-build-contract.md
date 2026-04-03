# Slice 01-01: source-build-contract

## Metadata

- created_at: 2026-04-03T16:31:39+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-01
- status: planned
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Define the source-of-truth authoring layout and deterministic build contract for Forward Roll plugin assets.

## Why Now

Epic 01 depends on a stable authoring/build boundary before shared helpers or templates can move out of the shipped skill directories. Locking that contract first avoids rework in generator design, generated-output check-in policy, and contributor docs.

## In Scope

- Define the initial authored source tree and generated output boundaries for the plugin.
- Introduce the minimal build entrypoint or scaffold needed to make that contract executable in a later slice.
- Document which existing plugin paths stay operator-facing outputs and which paths become authoring inputs.

## Out Of Scope

- Migrating duplicated helper scripts into shared authored sources.
- Templating every SKILL.md or regenerating every skill bundle in this slice.
- Changing the operator-facing Forward Roll command surface.

## Relevant Files And Systems

- .forward-roll/specs/architecture.md
- .forward-roll/specs/workflow.md
- plugins/forward-roll/README.md
- plugins/forward-roll/.codex-plugin/plugin.json
- plugins/forward-roll/skills/
- plugins/forward-roll/src/ or another repo-local authoring root introduced by the slice
- A repository-local build script or manifest for generating plugin assets

## Acceptance Criteria

- The repository clearly distinguishes authoring inputs from generated plugin outputs for Forward Roll.
- A contributor can identify the intended command or script that will build generated plugin assets, even if later slices expand its behavior.
- Docs and planning artifacts agree on whether generated plugin outputs remain checked in during this epic.

## Validation Strategy

- Inspect the resulting layout and docs to confirm the source-versus-generated contract is explicit and consistent.
- Run the relevant documentation or script validation touched by the slice, such as python constraint checks if a build script is introduced.
- Confirm the planned build contract preserves self-contained skill bundles and does not introduce cross-skill runtime imports.

## jj Review Shape

One readable change that introduces the authoring/build contract and any minimal scaffolding needed to make later generation work obvious in review.

## Stop Condition

Stop once the repository has an explicit authored-versus-generated plugin contract and only the minimal scaffolding needed for the next implementation slice; leave helper migration and broad generation work for later slices.

## Log

- 2026-04-03T16:31:39+00:00 Planned slice artifact created.
