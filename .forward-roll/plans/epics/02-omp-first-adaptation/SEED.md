# SEED — how to execute Epic 02 (for a fresh omp agent)

You are starting cold. This brief orients you so you don't re-derive decisions already made or re-litigate settled questions. Read in this order:

1. `.forward-roll/specs/omp-first-adaptation.md` — the design spec (authoritative for *what* and *why*).
2. `.forward-roll/plans/epics/02-omp-first-adaptation/EPIC.md` — the epic: goal, definition of done, slice breakdown, interfaces.
3. This brief — settled decisions + grounding facts + concrete specs for the structural slices.
4. The per-slice docs in `slices/` (03, 04, 05 carry actual file contents; 01 and 02 are specified below).

Execute slices in order: **02-01 → 02-02 → 02-03 → 02-04 → 02-05 → 02-06**. Each leaves one reviewable `jj` change. Use omp's native tools (read/edit/write/bash/lsp) — you are NOT using the not-yet-built `fr-impl`/`fr-review` loop to build this epic; you're authoring it directly.

## Settled decisions (do not re-litigate)

1. **omp primary, Codex secondary.** Build emits both; omp is the supported path, Codex best-effort.
2. **Non-isolated subagent execution.** `task.isolation.mode: none` so `fr-impl`/`fr-review` edit the orchestrator's shared working copy. The orchestrator owns the jj squash flow and gates the changeset on clean review. Slices run sequentially (shared `@`).
3. **Brainstorm folded into `fr-specify`** (two phases). That's Epic 03, not this epic.
4. **Custom agents `fr-impl` + `fr-review`** on both targets.

## Resolved confirm-items (don't guess — these are settled)

- **omp isolation default** → set `task.isolation.mode: none` explicitly in `.omp/config.yml`. The default is moot.
- **Codex cannot bundle subagents in a plugin** → `plugin.json` has no `agents` field (plugin parts: skills/apps/MCP/hooks/browser-ext/scheduled-tasks). So Codex agents emit to **repo-root `.codex/agents/*.toml`**, not inside the plugin. omp agents DO bundle in the plugin (`plugins/forward-roll/agents/*.md`). This asymmetry is intended.
- **Model per agent** → omp uses role aliases (`fr-impl: @default`, `fr-review: @slow`); Codex **omits `model`** (inherit/auto-select) and pins only `model_reasoning_effort` (`medium`/`high`). No literal slugs anywhere.

## Grounding facts (verified against primary sources)

- **omp task agent** = markdown + YAML frontmatter (`name`, `description`, `tools`, `model`, `spawns`, `read-summarize`, `output`). `output` uses `properties`/`optionalProperties` with `metadata.description`, `enum`, `type`, `elements`. See the bundled `reviewer`/`scout` for the schema shape (mirrored in slice 02-03). Plugin agents discovered from the plugin's `agents/` dir.
- **omp skill** = `.agents/skills/<name>/SKILL.md` (project) — what this repo already uses for `jj`. The plugin's own skills live in `plugins/forward-roll/skills/`.
- **omp marketplace catalog** = repo-root `.omp-plugin/marketplace.json` with `source: "./plugins/forward-roll"`. The existing `.agents/plugins/marketplace.json` is misplaced (not a valid catalog root) — migrate it in 02-01.
- **Codex custom agent** = TOML at `.codex/agents/<name>.toml` (project) — required `name`/`description`/`developer_instructions`; optional `model_reasoning_effort`/`sandbox_mode` (omit `model`).
- **Codex plugin manifest** = `.codex-plugin/plugin.json` (already exists; `skills: "./skills/"`).

## Slice 02-01 spec — multi-target build scaffold

Extend the existing manifest-driven build (read `src/build.py` and `src/plugin-build.json` first — it clears `generated_roots` then renders `generated_assets`). Minimal, correct changes:

**`plugin-build.json`** — add the new assets and declare repo-root outputs:
```json
"repo_root_outputs": [
  ".omp-plugin/marketplace.json",
  ".codex/agents/fr-impl.toml",
  ".codex/agents/fr-review.toml"
],
"generated_assets": [
  // existing assets unchanged...
  { "source": "src/plugin-shell/.omp-plugin/marketplace.json", "target": ".omp-plugin/marketplace.json", "repo_root": true },
  { "source": "src/agent-templates/fr-impl.omp.md",   "target": "plugins/forward-roll/agents/fr-impl.md" },
  { "source": "src/agent-templates/fr-review.omp.md", "target": "plugins/forward-roll/agents/fr-review.md" },
  { "source": "src/agent-templates/fr-impl.codex.toml",   "target": ".codex/agents/fr-impl.toml",   "repo_root": true },
  { "source": "src/agent-templates/fr-review.codex.toml", "target": ".codex/agents/fr-review.toml", "repo_root": true }
]
```
(`"repo_root": true` ⇒ resolve `target` against the repo root, not the generated root. Default build renders ALL assets — both targets — clearing `generated_roots` + `repo_root_outputs` once. Do NOT try per-target partial clearing of the shared `plugins/forward-roll/` root.)

**`src/build.py`** — when an asset has `repo_root: true`, resolve its target against `repo_root` (not a generated root); extend `clear_generated_roots` to also remove declared `repo_root_outputs`. Keep `--check` working.

**`src/plugin-shell/.omp-plugin/marketplace.json`** (new source):
```json
{
  "name": "forward-roll",
  "owner": { "name": "Scott Trinh" },
  "metadata": { "description": "jj-first omp workflow plugin", "pluginRoot": "plugins" },
  "plugins": [
    { "name": "forward-roll", "source": "./plugins/forward-roll", "category": "productivity" }
  ]
}
```

**Migrate:** move `.agents/plugins/marketplace.json` content into the new `.omp-plugin/marketplace.json` source; delete the old file.

**Verify:** `python3 scripts/verify_plugin_rebuild.py` — extend it to also assert the repo-root outputs (`.omp-plugin/marketplace.json`, `.codex/agents/*.toml`) reappear after rebuild and are removed when stale.

## Slice 02-02 spec — omp runtime config + bootstrap check

**`.omp/config.yml`** (new, repo root):
```yaml
task:
  isolation:
    mode: none
```

**`fr-bootstrap` / `bootstrap.py` + shared `resolve_context.py`** — add an omp-environment check that:
- Reads the project `.omp/config.yml` and confirms `task.isolation.mode: none` is set. If absent, instruct the operator to add it (print the snippet above) and stop.
- Reports whether `fr-impl`/`fr-review` are discoverable (check `plugins/forward-roll/agents/*.md` exist; full discovery is omp's job — just confirm the files are present and emitted).
- For Codex users, prints the manual-copy note: agents live at repo-root `.codex/agents/` and must be copied to `~/.codex/agents/` if used outside this repo.

Keep writing `.forward-roll/runtime.json` as today; add an `omp` section recording `isolation_mode` and `agents_present`.

## Out of scope for Epic 02 (do not build these now — Epic 03)

- `fr-specify` brainstorm phase + `specify.py --mode brainstorm`.
- `fr-plan-slice` TDD-step contract + `plan_slice.py` template.
- Codex `fr-do` dialect (Codex subagent-workflow dispatch).
- Epic-level `fr-review` mechanism choice (still open in spec §10).

## When you hit something unspecified

Prefer the spec. If the spec is silent, choose the boring option that keeps omp-first and jj-reviewable, note the decision in the slice's run-log, and move on. Do not expand scope into Epic 03.
