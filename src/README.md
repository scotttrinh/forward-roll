# Plugin Source Layout

This directory is the source-of-truth authoring root for Forward Roll plugin assets.

## Contract

- `plugin-build.json` declares the authored roots, generated roots, and the expectation that the plugin can be rebuilt from source
- future shared script sources, templates, and prompt fragments should live under this tree
- generated plugin output should be emitted under `../plugins/forward-roll/`
- `src/` should contain everything needed to rebuild `../plugins/forward-roll/` entirely from scratch

## Scope

Slice `01-02` relocated the initial authoring scaffold into this top-level source root.

Slice `01-04` extends the first shared generated asset path:

- `shared-scripts/resolve_context.py` is the authored source of truth for the generated `resolve_context.py` helpers used by `fr-plan-epic`, `fr-plan-slice`, `fr-do`, `fr-feedback`, and `fr-review`
- `python3 src/build.py` emits that shared script into the targeted generated skill bundle paths under `plugins/forward-roll/`

Later slices may add:

- more shared authored helper sources
- SKILL.md templates or prompt fragments
- broader file generation logic that materializes more of the distributed plugin bundle
