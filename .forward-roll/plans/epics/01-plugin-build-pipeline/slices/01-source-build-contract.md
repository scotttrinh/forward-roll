# Slice 01-01: source-build-contract

## Metadata

- created_at: 2026-04-03T16:31:39+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-01
- status: completed
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Define the source-of-truth authoring layout and deterministic build contract for Forward Roll plugin assets.

## Why Now

Epic 01 depends on a stable authoring/build boundary before shared helpers or templates can move out of the shipped skill directories. Locking that contract first avoids rework in generator design, distribution layout, CI packaging, and contributor docs.

## In Scope

- Define the initial authored source tree and generated distribution boundaries for the plugin.
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
- src/ as the eventual repo-local authoring root
- plugins/forward-roll/ as the eventual generated plugin distribution root
- A repository-local build script or manifest for generating plugin assets

## Acceptance Criteria

- The repository clearly distinguishes authoring inputs under top-level `src/` from the generated plugin output under `plugins/forward-roll/`.
- A contributor can identify the intended command or script that will build generated plugin assets, even if later slices expand its behavior.
- Docs and planning artifacts agree that `plugins/forward-roll/` is generated output that can be rebuilt from scratch and does not define the long-term source of truth.

## Validation Strategy

- Inspect the resulting layout and docs to confirm the source-versus-generated contract is explicit and consistent around top-level `src/` and `plugins/forward-roll/`.
- Run the relevant documentation or script validation touched by the slice, such as python constraint checks if a build script is introduced.
- Confirm the planned build contract preserves self-contained skill bundles and does not introduce cross-skill runtime imports.

## jj Review Shape

One readable change that introduces the top-level `src/` to `plugins/forward-roll/` contract and any minimal scaffolding needed to make later generation work obvious in review.

## Stop Condition

Stop once the repository has an explicit top-level `src/` versus `plugins/forward-roll/` plugin contract and only the minimal scaffolding needed for the next implementation slice; leave helper migration, file shuffling, and broad generation work for later slices.

## Log

- 2026-04-03T16:31:39+00:00 Planned slice artifact created.


- 2026-04-03T16:47:30+00:00 Defined the plugin authoring/build contract and added a minimal build entrypoint.
  - Added plugins/forward-roll/src/ as the authored source root with a deterministic plugin-build.json manifest.
  - Added plugins/forward-roll/scripts/build.py to validate the contract and document the future generation boundary.
  - Updated architecture and workflow specs plus plugin docs to describe `src/` as the source of truth and `dist/` as the generated distribution target.
  - python3 plugins/forward-roll/scripts/build.py --check
  - python3 -m py_compile plugins/forward-roll/scripts/build.py
  - python3 scripts/validate_python_constraints.py
  - No blockers recorded.
  - Implement the first generated asset path by sourcing one duplicated helper from plugins/forward-roll/src and emitting it into the distribution bundle under plugins/forward-roll/dist/.

- 2026-04-03T16:53:27+00:00 Revised the contract after operator feedback.
  - Generated plugin output should live under plugins/forward-roll/ as the post-build distribution artifact.
  - The eventual version-controlled source of truth should live under top-level src/ instead of under the generated plugin tree.
  - The next slice should move the current authored-source scaffolding toward that final layout.
