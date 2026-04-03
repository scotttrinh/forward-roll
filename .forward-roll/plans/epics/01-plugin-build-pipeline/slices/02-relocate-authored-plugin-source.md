# Slice 01-02: relocate-authored-plugin-source

## Metadata

- created_at: 2026-04-03T17:00:00+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-02
- status: completed
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Move the current authored plugin scaffolding into its eventual home under top-level `src/` while preserving `plugins/forward-roll/` as the generated distribution boundary.

## Why Now

Epic 01 now treats `plugins/forward-roll/` as distribution output, but the current repo still stores newly introduced authoring files inside that tree. Relocating those inputs before deeper generation work prevents the build pipeline from hard-coding the wrong boundary.

## In Scope

- Move the authored-source scaffolding introduced for Epic 01 out of `plugins/forward-roll/src/` and into an appropriate top-level `src/` subtree.
- Move or recreate the build manifest and repository-local build entrypoint so they clearly belong to the authoring side of the boundary.
- Update any docs, specs, and validation commands that currently point at the transitional in-plugin source layout.
- Preserve the current distributed plugin contents under `plugins/forward-roll/` until a later slice regenerates them from the new source layout.

## Out Of Scope

- Regenerating every skill bundle from templates in this slice.
- Large-scale helper deduplication beyond what is needed to complete the relocation cleanly.
- Changing the operator-facing Forward Roll command surface.

## Relevant Files And Systems

- .forward-roll/specs/architecture.md
- .forward-roll/specs/workflow.md
- .forward-roll/plans/epics/01-plugin-build-pipeline/EPIC.md
- plugins/forward-roll/
- plugins/forward-roll/src/
- src/
- Any build-manifest or build-entrypoint files introduced by slice 01-01

## Acceptance Criteria

- The repository has a top-level `src/` location that clearly owns the plugin's authored inputs.
- `plugins/forward-roll/` no longer contains authoring-only scaffolding that conceptually belongs to the source tree.
- The documented build entrypoint and manifest paths match the relocated source layout.
- Validation still passes after the relocation.

## Validation Strategy

- Inspect the repository layout and docs to confirm the source-versus-distribution boundary is explicit.
- Run the build-contract validation after updating paths.
- Run the Python constraint validation for any touched scripts.

## jj Review Shape

One readable relocation change that moves authoring files into `src/`, updates references, and leaves the plugin distribution tree easier to reason about.

## Stop Condition

Stop once the authoring scaffolding lives under top-level `src/`, the documentation references are updated, and the repo is ready for the later slice that turns those sources into generated plugin output.

## Log

- 2026-04-03T17:00:00+00:00 Planned slice artifact created.

- 2026-04-03T17:15:48+00:00 Relocated the authored plugin scaffold into top-level src/ and updated build contract paths.
  - Moved the manifest, build entrypoint, source layout README, and placeholder authoring roots from plugins/forward-roll/src into top-level src/.
  - Removed the empty legacy plugins/forward-roll/src tree and updated docs and specs to treat plugins/forward-roll/ as generated output.
  - python3 src/build.py --check
  - python3 -m py_compile src/build.py
  - python3 scripts/validate_python_constraints.py
  - No blockers recorded.
  - Implement the first generated asset path from src/ into plugins/forward-roll/ so later slices can replace checked-in distribution files with build output.
