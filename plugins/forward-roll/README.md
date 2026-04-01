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

- `.codex-plugin/plugin.json`: plugin metadata
- `skills/`: one skill per workflow command
- `skills/<command>/scripts/*.py`: self-contained standard-library helper scripts for that skill

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
