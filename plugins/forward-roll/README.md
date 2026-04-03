# Forward Roll

Forward Roll is a Codex plugin for a personal, jj-first development loop.

This first pass turns the repository specs into a usable plugin skeleton:

- `fr-bootstrap` resolves and persists the runtime contract.
- `fr-specify` creates or sharpens high-level project specs.
- `fr-plan-epic` defines a reviewable deliverable and its slice breakdown.
- `fr-plan-slice` turns one epic into a bounded execution slice.
- `fr-do` executes a slice and appends a timestamped run summary to the slice log.
- `fr-feedback` records operator or review-driven changes as durable workflow state.
- `fr-review` compares epic intent against the current implementation.

## Layout

- `src/`: repository-local authoring inputs for generated plugin assets
- `src/plugin-build.json`: deterministic build manifest describing authored roots and generated outputs
- `src/build.py`: repository-local build entrypoint for validating and materializing generated plugin assets
- `src/shared-scripts/resolve_context.py`: authored shared helper currently generated into the planning, execution, feedback, and review skills
- `.codex-plugin/plugin.json`: current generated plugin metadata location
- `skills/`: current generated skill bundle location

The current contract is:

- top-level `src/` is the source of truth for all inputs required to build the plugin from scratch
- `plugins/forward-roll/` is the generated distribution output for the plugin bundle
- `python3 src/build.py` currently regenerates the shared `resolve_context.py` helper for `fr-plan-epic`, `fr-plan-slice`, `fr-do`, `fr-feedback`, and `fr-review` from `src/shared-scripts/resolve_context.py`
- `plugins/forward-roll/` should be rebuildable locally and in CI as additional generation paths land

## Local Development

Run the skill-owned helpers directly from the repository root:

```bash
python3 plugins/forward-roll/skills/fr-bootstrap/scripts/bootstrap.py
python3 plugins/forward-roll/skills/fr-specify/scripts/specify.py auth --mode discover --goal "Describe the current auth system"
python3 plugins/forward-roll/skills/fr-plan-epic/scripts/plan_epic.py 04 auth-session-hardening --goal "Harden session handling"
python3 plugins/forward-roll/skills/fr-plan-slice/scripts/plan_slice.py 04 02 cookie-rotation --goal "Implement cookie rotation"
python3 plugins/forward-roll/skills/fr-do/scripts/do.py --slice .forward-roll/plans/epics/04-auth-session-hardening/slices/02-cookie-rotation.md --summary "Implemented cookie rotation and updated tests"
python3 plugins/forward-roll/skills/fr-review/scripts/review.py --epic .forward-roll/plans/epics/04-auth-session-hardening/EPIC.md
python3 plugins/forward-roll/skills/fr-feedback/scripts/feedback.py 04 review-follow-up --scope epic --outcome adjust-epic
```

By default the runtime contract is stored at `.forward-roll/runtime.json`, durable specs live under `.forward-roll/specs/`, and planning artifacts live under `.forward-roll/plans/epics/`.

Validate skill bundles without third-party packages:

```bash
python3 plugins/forward-roll/skills/fr-bootstrap/scripts/validate_skill_bundle.py \
  plugins/forward-roll/skills/fr-bootstrap \
  plugins/forward-roll/skills/fr-specify \
  plugins/forward-roll/skills/fr-plan-epic \
  plugins/forward-roll/skills/fr-plan-slice \
  plugins/forward-roll/skills/fr-do \
  plugins/forward-roll/skills/fr-feedback \
  plugins/forward-roll/skills/fr-review
```

Validate the Python script constraints without third-party packages:

```bash
python3 scripts/validate_python_constraints.py
```

Use `uv` only for development tooling. Runtime scripts stay self-contained and stdlib-only:

```bash
uv run --group dev ruff check plugins/forward-roll/skills
uv run --group dev mypy plugins/forward-roll/skills
```

Validate the plugin authoring/build contract:

```bash
python3 src/build.py --check
```

Generate the shared authored helper into the targeted skill scripts:

```bash
python3 src/build.py
```
