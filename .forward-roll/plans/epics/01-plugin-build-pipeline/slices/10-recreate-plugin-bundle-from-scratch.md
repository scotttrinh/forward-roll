# Slice 01-10: recreate-plugin-bundle-from-scratch

## Metadata

- created_at: 2026-04-04T12:54:21+00:00
- runtime: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/runtime.json
- epic: 01
- slice: 01-10
- status: done
- epic_dir: /Users/scotttrinh/github.com/scotttrinh/forward-roll/.forward-roll/plans/epics/01-plugin-build-pipeline

## Goal

Make the plugin build recreate the generated bundle from a clean or missing plugins/forward-roll/ tree so epic 01's rebuild-from-source contract is true in practice.

## Why Now

Epic 01 claims the plugin can be rebuilt entirely from source and the epic acceptance criteria explicitly require recreating plugins/forward-roll/ after the generated bundle has been removed or relocated. The current builder only rewrites declared files into existing parent directories, so the contract still depends on checked-in output structure.

## In Scope

- Update src/build.py so generation creates any missing parent directories for declared plugin targets before writing files.
- Add one high-signal verification path that exercises rebuilding plugins/forward-roll/ from a missing or moved-aside generated bundle instead of only validating the manifest against an already-present tree.
- Document the stricter rebuild-from-scratch expectation where the source/build contract is described, only as needed to match the implemented behavior.

## Out Of Scope

- Changing the operator-facing skill surface, plugin layout, or generated file contents beyond what is needed to recreate the bundle from source.
- Retargeting lint, mypy, or other repo tooling from generated plugin paths to src-owned paths.
- Deciding whether generated outputs stay checked in or are removed from version control; that policy cleanup can follow once rebuild-from-scratch behavior exists.

## Relevant Files And Systems

- src/build.py
- src/plugin-build.json
- src/README.md
- plugins/forward-roll/README.md
- plugins/forward-roll/.codex-plugin/plugin.json
- plugins/forward-roll/skills/

## Acceptance Criteria

- A contributor can move aside or remove plugins/forward-roll/, run python3 src/build.py, and see the declared generated bundle paths recreated without manually pre-creating directories.
- python3 src/build.py --check still fails clearly when a declared source file is missing or when the manifest declares an impossible target path.
- The regenerated skill bundles still pass python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py for the shipped skills after the clean rebuild flow.

## Validation Strategy

- Run python3 src/build.py --check before and after the change.
- Temporarily move or remove plugins/forward-roll/, run python3 src/build.py, and confirm the generated bundle is recreated from src/.
- Run python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap plugins/forward-roll/skills/fr-specify plugins/forward-roll/skills/fr-plan-epic plugins/forward-roll/skills/fr-plan-slice plugins/forward-roll/skills/fr-do plugins/forward-roll/skills/fr-feedback plugins/forward-roll/skills/fr-review.

## jj Review Shape

Keep one readable change focused on builder directory creation and rebuild verification so review stays anchored on the rebuild-from-scratch contract.

## Stop Condition

Stop once the build can recreate the declared plugin bundle paths from src with no manual directory setup, the contract docs match that behavior, and the regenerated skill bundles validate successfully.

## Log

- 2026-04-04T12:54:21+00:00 Planned slice artifact created.


- 2026-04-04T13:07:23+00:00 Updated the plugin builder to recreate generated bundle paths from a missing plugins/forward-roll tree and added automated rebuild verification.
  - Updated src/build.py so --check validates generated target safety without requiring pre-existing output directories.
  - Updated src/build.py generation to create missing parent directories before writing generated assets.
  - Added scripts/verify_plugin_rebuild.py to move aside plugins/forward-roll, rebuild from src, confirm all declared targets are recreated, and validate shipped skill bundles.
  - Documented the rebuild-from-scratch contract and verification command in the authored READMEs.
  - python3 src/build.py --check
  - python3 src/build.py
  - python3 scripts/verify_plugin_rebuild.py
  - python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py plugins/forward-roll/skills/fr-bootstrap plugins/forward-roll/skills/fr-specify plugins/forward-roll/skills/fr-plan-epic plugins/forward-roll/skills/fr-plan-slice plugins/forward-roll/skills/fr-do plugins/forward-roll/skills/fr-feedback plugins/forward-roll/skills/fr-review
  - No blockers recorded.
  - A follow-up slice can add richer target-shape validation to the manifest if the build grows beyond static file generation.


- 2026-04-04T13:12:05+00:00 Updated the build step to clear generated roots before regeneration so stale plugin files cannot persist.
  - Updated src/build.py to remove each declared generated root before emitting generated assets.
  - Extended scripts/verify_plugin_rebuild.py to create a stale file, rerun the build, and confirm the stale file is removed.
  - Updated the authored READMEs to document that builds now clear generated output before regeneration.
  - python3 src/build.py --check
  - python3 src/build.py
  - python3 scripts/verify_plugin_rebuild.py
  - No blockers recorded.
  - If generated_roots ever overlap, the builder should reject that manifest shape explicitly before deletion.
