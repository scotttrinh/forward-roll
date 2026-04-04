# Plugin Source Layout

This directory is the source-of-truth authoring root for Forward Roll plugin assets.

## Contract

- `plugin-build.json` declares the authored roots, generated roots, and the expectation that the plugin can be rebuilt from source
- future shared script sources, templates, and prompt fragments should live under this tree
- generated plugin output should be emitted under `../plugins/forward-roll/`
- `src/` should contain everything needed to rebuild `../plugins/forward-roll/` entirely from scratch
- `python3 src/build.py` clears declared generated roots before regenerating them so missing directories are recreated and stale generated files cannot survive source removals

## Scope

Slice `01-02` relocated the initial authoring scaffold into this top-level source root.

Slice `01-05` extends the first shared generated asset path:

- `shared-scripts/resolve_context.py` is the authored source of truth for the generated `resolve_context.py` helpers used by `fr-specify`, `fr-plan-epic`, `fr-plan-slice`, `fr-do`, `fr-feedback`, and `fr-review`
- `python3 src/build.py` emits that shared script into the targeted generated skill bundle paths under `plugins/forward-roll/`

Slice `01-06` moves the generated plugin shell assets under source control:

- `plugin-shell/README.md` is the authored source of truth for the generated `plugins/forward-roll/README.md`
- `plugin-shell/.codex-plugin/plugin.json` is the authored source of truth for the generated `plugins/forward-roll/.codex-plugin/plugin.json`
- `python3 src/build.py` now emits those static shell assets alongside the shared generated helper paths

Slice `01-07` moves the generated skill definitions under source control:

- `skill-templates/<skill>/SKILL.md` is the authored source of truth for the generated `plugins/forward-roll/skills/<skill>/SKILL.md`
- `python3 src/build.py` now emits those static skill markdown assets alongside the plugin shell assets and shared helper paths

Slice `01-08` starts moving skill-owned Python entrypoints into the source tree:

- `skill-templates/fr-bootstrap/scripts/bootstrap.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-bootstrap/scripts/bootstrap.py`
- `skill-templates/fr-bootstrap/scripts/validate_skill_bundle.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py`
- `python3 src/build.py` now emits those bootstrap skill scripts alongside the generated shell assets, skill markdown, and shared helper paths

Slice `01-09` finishes moving the remaining skill-owned Python entrypoints into the source tree:

- `skill-templates/fr-specify/scripts/specify.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-specify/scripts/specify.py`
- `skill-templates/fr-plan-epic/scripts/plan_epic.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-plan-epic/scripts/plan_epic.py`
- `skill-templates/fr-plan-slice/scripts/plan_slice.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-plan-slice/scripts/plan_slice.py`
- `skill-templates/fr-do/scripts/do.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-do/scripts/do.py`
- `skill-templates/fr-feedback/scripts/feedback.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-feedback/scripts/feedback.py`
- `skill-templates/fr-review/scripts/review.py` is the authored source of truth for the generated `plugins/forward-roll/skills/fr-review/scripts/review.py`
- `python3 src/build.py` now emits every shipped skill-owned Python entrypoint from `src/skill-templates/` into the generated plugin bundle

Later slices may add:

- more shared authored helper sources
- prompt fragments
- broader file generation logic that materializes more of the distributed plugin bundle

## Verification

- `python3 src/build.py --check` validates the authored contract without requiring `plugins/forward-roll/` to already exist
- `python3 scripts/verify_plugin_rebuild.py` moves aside the generated plugin bundle, rebuilds it from `src/`, checks that every declared target reappears, confirms stale files are removed on rebuild, and validates the shipped skill bundles before restoring the original tree
