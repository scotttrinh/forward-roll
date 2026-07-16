# Epic 02 — end-to-end smoke

> Verification record for [`EPIC.md`](EPIC.md). Records what was exercised
> in-session during the build and the operator-run procedure for the live
> subagent loop.

## In-session evidence (build session)

Run from the repo root after `python3 src/build.py`:

| Check | Command | Result |
|---|---|---|
| DoD 1 — deterministic rebuild, both targets | `python3 scripts/verify_plugin_rebuild.py` | `Rebuild verification succeeded.` (stale `plugins/forward-roll/stale-file.txt` removed; repo-root outputs `.omp-plugin/marketplace.json` + `.codex/agents/*.toml` regenerated after deletion) |
| DoD 2 — omp catalog at repo root | `jq .plugins[0].source .omp-plugin/marketplace.json` | `"./plugins/forward-roll"` |
| DoD 3 — agents discoverable | `ls plugins/forward-roll/agents .codex/agents` | omp `fr-impl.md`, `fr-review.md`; Codex `fr-impl.toml`, `fr-review.toml` |
| AC3 — Codex agents omit `model`, pin reasoning effort | `grep -hE '^(model|model_reasoning_effort|sandbox_mode)' .codex/agents/*.toml` | no `model =`; `medium`/`high` effort; `workspace-write`/`read-only` |
| DoD 4 — bootstrap reports omp env | `python3 plugins/forward-roll/skills/fr-bootstrap/scripts/bootstrap.py` | `omp_isolation_mode: none`, `omp_agents_discoverable: fr-impl, fr-review`, Codex manual-copy note printed |
| AC2 — agent tool surface | frontmatter of `plugins/forward-roll/agents/*.md` | `fr-impl` has edit/write; `fr-review` omits edit/write (read-only) |

The `.forward-roll/runtime.json` `omp` section records `isolation_mode` and
`agents_present`; `resolve_context.py` (shared into the execution skills) emits
the same `omp` block so `fr-do` can re-verify the precondition before dispatch.

## Live subagent loop (operator run)

`fr-do` dispatches the plugin's bundled `fr-impl`/`fr-review` task agents, which
are discovered by omp only once the plugin is linked into an omp session
(`omp plugin link ./plugins/forward-roll`). That discovery is omp's job at link
time and does not happen inside this build session, so the full behavioral loop
is the operator-run smoke:

1. `python3 src/build.py`, then run `fr-bootstrap` → confirm the omp env summary
   above (`isolation_mode: none`, both agents listed).
2. Plan one trivial slice (e.g. "add a one-line changelog comment") via
   `fr-plan-slice`.
3. Run `fr-do` on it. Expected sequence:
   - it verifies `task.isolation.mode: none` and agent discoverability;
   - it `jj describe`s the working-copy change with the slice intent;
   - it dispatches a **non-isolated** `fr-impl` task whose edits land in `@`;
   - it dispatches a non-isolated `fr-review` task returning `verdict` + findings;
   - on `ship` it `jj squash`es `@` into the described change and appends the
     run-log via `do.py`; on `revise` it loops back to `fr-impl`.
4. `jj log` shows exactly one described change for the slice, and **before**
   `fr-review` returns `ship` the work exists only in `@` (AC4).

The contract this loop relies on is verified in-session: the two agents exist
and validate, the omp precondition is enforceable and checked, `fr-do`'s SKILL
encodes the seven-step loop, and the deterministic helpers
(`resolve_context.py`, `do.py`) run cleanly.
