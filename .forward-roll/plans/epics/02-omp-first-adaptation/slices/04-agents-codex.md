# Slice 02-04 — Codex custom agents (`fr-impl`, `fr-review`)

> Epic: 02-omp-first-adaptation · Depends on: 02-01 (build targets exist)
> Goal: author the two Codex custom agents as TOML and wire the build to emit them to **repo-root** `.codex/agents/`.

## Why this slice + the key constraint

Codex custom agents are standalone TOML files at `.codex/agents/` (project-scoped) or `~/.codex/agents/` (user). **Codex plugins cannot bundle subagents** — `plugin.json` has no `agents` field (confirmed against Codex's plugin docs; plugin parts are skills/apps/MCP/hooks/browser-ext/scheduled-tasks only). So unlike omp, these agents are NOT emitted inside `plugins/forward-roll/`; they go to **repo-root `.codex/agents/`** so Codex discovers them when running in the repo. A Codex user installing the plugin elsewhere must copy them manually (documented by `fr-bootstrap`).

Codex agents **omit `model`** (inherit the active session model or let Codex auto-select) and pin only `model_reasoning_effort` — the symmetric counterpart to omp's role-alias deferral, avoiding stale OpenAI slugs.

## Files

**Create (authored sources):**
- `src/agent-templates/fr-impl.codex.toml`
- `src/agent-templates/fr-review.codex.toml`

**Generated (by `build.py`) — to REPO ROOT, not the plugin bundle:**
- `.codex/agents/fr-impl.toml`
- `.codex/agents/fr-review.toml`

**Modify:**
- `src/plugin-build.json` — register under the `codex` target, with targets that resolve to repo-root `.codex/agents/`
- `src/build.py` — emit `src/agent-templates/*.codex.toml` → `<repo_root>/.codex/agents/<name>.toml` (verbatim). This is a second repo-root output alongside `.omp-plugin/marketplace.json`.

## Actual content

### `src/agent-templates/fr-impl.codex.toml`

```toml
name = "fr-impl"
description = "Forward Roll slice implementer. Executes one planned slice via red-green TDD. Use when fr-do dispatches a slice for implementation."
sandbox_mode = "workspace-write"
model_reasoning_effort = "medium"
developer_instructions = """
You implement exactly one Forward Roll slice.

- Work ONLY from the slice contract the orchestrator passed: goal, in-scope/out-of-scope, TDD steps, and acceptance criteria.
- Red-green: write or extend the failing test first, run it to confirm it fails, then implement the minimal change to make it pass.
- Run the slice's declared validation set before returning; report the command and pass/fail.
- Leave all work in the working tree. The orchestrator owns history (commits/squash); do not commit or amend unless the orchestrator asks.
- Do not expand scope. If a needed change is out of scope, note it and stop.
- Return a concise structured summary: files changed, tests written, validation result, scope adherence, deviations.
"""
```

### `src/agent-templates/fr-review.codex.toml`

```toml
name = "fr-review"
description = "Forward Roll slice reviewer. Validates the change against slice acceptance criteria, spec/epic intent, and TDD coverage. Use when fr-do needs the per-slice review gate."
sandbox_mode = "read-only"
model_reasoning_effort = "high"
developer_instructions = """
You review one Forward Roll slice's change.

1. Read the slice contract (goal, acceptance criteria, TDD steps, out-of-scope).
2. View the change read-only (e.g. git diff / jj diff --git).
3. For each acceptance criterion, confirm met / unmet / partial.
4. Confirm tests exist and pass for the required behaviors.
5. Confirm scope: no edits outside the slice's in-scope files.
6. Return a verdict (ship or revise) with a 1-3 sentence explanation, the per-criterion coverage, a scope check, and any findings ranked P0-P3. Report only issues that block shipping the slice; do not flag style/nits.
"""
```

## `plugin-build.json` registration (under the `codex` target)

```json
{ "source": "src/agent-templates/fr-impl.codex.toml",   "target": ".codex/agents/fr-impl.toml" },
{ "source": "src/agent-templates/fr-review.codex.toml", "target": ".codex/agents/fr-review.toml" }
```

(Resolve `target` against repo root, not `plugins/forward-roll/`.)

## Verification

- `python3 src/build.py` then confirm `.codex/agents/fr-impl.toml` and `fr-review.toml` exist at repo root, verbatim with sources.
- `python3 scripts/verify_plugin_rebuild.py` passes (the rebuild check must cover repo-root outputs too — extend it in 02-01 to assert these paths).
- AC3: both files omit `model` and set `model_reasoning_effort` (`medium` for fr-impl, `high` for fr-review).
- TOML validity: each parses (Codex requires `name`, `description`, `developer_instructions`).

## Acceptance criteria for this slice

- Both TOML files emitted to **repo-root** `.codex/agents/` (NOT inside the plugin bundle).
- `model` omitted; `model_reasoning_effort` pinned; `sandbox_mode` set (`workspace-write` / `read-only`).
- `fr-bootstrap` (slice 02-02) documents that Codex users installing the plugin elsewhere must copy these into their own `.codex/agents/`.
