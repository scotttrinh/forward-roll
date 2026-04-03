# Plugin Source Layout

This directory is the source-of-truth authoring root for Forward Roll plugin assets.

## Contract

- `plugin-build.json` declares the authored roots, generated roots, and the expectation that the plugin can be rebuilt from source
- future shared script sources, templates, and prompt fragments should live under this tree
- generated plugin output should be emitted under `../plugins/forward-roll/`
- `src/` should contain everything needed to rebuild `../plugins/forward-roll/` entirely from scratch

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

Later slices may add:

- more shared authored helper sources
- prompt fragments
- broader file generation logic that materializes more of the distributed plugin bundle
