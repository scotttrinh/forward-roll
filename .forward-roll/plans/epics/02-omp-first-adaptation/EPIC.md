# Epic 02 — omp-first plugin foundation

> Implements spec: [`../../../specs/omp-first-adaptation.md`](../../../specs/omp-first-adaptation.md)
> Status: planned · Prerequisite: Epic 01 (src→plugin build pipeline) ✓

## Goal

Ship Forward Roll as a dual-target **omp-first** plugin where an omp operator can bootstrap and execute a slice via the `fr-impl` → `fr-review` subagent loop, with the orchestrator gating a single reviewable `jj` change on clean review. A best-effort Codex target also builds.

## Why it matters

Pivot from Codex-first to omp-first; enable the superpowers-style subagent execution loop (TDD implementer + spec-compliance reviewer) while preserving the jj review boundary that is Forward Roll's identity. The Codex secondary target keeps existing users working.

## Spec impact

Implements `omp-first-adaptation.md` §4 (fr-do loop), §5 (custom agents), §7 (multi-target build), §8 (jj contract). Defers §6 (fr-specify brainstorm, fr-plan-slice TDD contract) to Epic 03.

## Current system shape

- `src/` authoring root generates `plugins/forward-roll/` (Codex-only) via `build.py` + `plugin-build.json` (`generated_assets[]`, `generated_roots[]`).
- Plugin bundle: `.codex-plugin/plugin.json` + `skills/fr-*/` (Codex-framed, invoke `python3 plugins/forward-roll/skills/.../scripts/*.py`).
- `.agents/skills/jj/` + a misplaced `.agents/plugins/marketplace.json` (valid omp catalog location is repo-root `.omp-plugin/marketplace.json`).
- 7 skills; `fr-do` is currently inline execution, not subagent orchestration.

## Proposed change shape

- `build.py` gains a **targets** concept: emit `omp` (repo-root `.omp-plugin/marketplace.json` + `plugins/forward-roll/{skills,agents}/`) and `codex` (`plugins/forward-roll/.codex-plugin/` + **repo-root** `.codex/agents/` — Codex plugins cannot bundle subagents, so these live at the repo root).
- Two custom task agents (`fr-impl`, `fr-review`) authored per-platform under `src/agent-templates/`.
- omp `fr-do` rewritten to orchestrate non-isolated `task` dispatch of the two agents + `jj squash` gate.
- `.omp/config.yml` pins `task.isolation.mode: none`; `fr-bootstrap` verifies it.

## File map

**Create:**
- `src/agent-templates/fr-impl.omp.md`, `src/agent-templates/fr-impl.codex.toml`
- `src/agent-templates/fr-review.omp.md`, `src/agent-templates/fr-review.codex.toml`
- `src/plugin-shell/.omp-plugin/marketplace.json` (omp catalog source)
- `.omp/config.yml` (pins `task.isolation.mode: none`)

**Modify:**
- `src/plugin-build.json` — add `targets` (omp/codex) and the new generated assets
- `src/build.py` — render all assets (both targets) in one pass; clear generated roots + repo-root outputs once (do NOT per-target-clear the shared `plugins/forward-roll/` root); emit catalog + Codex agents to repo root
- `plugins/forward-roll/skills/fr-bootstrap/SKILL.md` + `src/skill-templates/fr-bootstrap/SKILL.md` — omp environment verification
- `src/skill-templates/fr-bootstrap/scripts/bootstrap.py` (+ shared `resolve_context.py`) — read/verify `task.isolation.mode`, agent discoverability
- `plugins/forward-roll/skills/fr-do/SKILL.md` + `src/skill-templates/fr-do/SKILL.md` — omp orchestration loop

**Migrate/remove:**
- `.agents/plugins/marketplace.json` → repo-root `.omp-plugin/marketplace.json`

## Definition of done

1. `python3 src/build.py` regenerates **both** targets from `src/`; `python3 scripts/verify_plugin_rebuild.py` passes for both.
2. omp catalog resolves at repo-root `.omp-plugin/marketplace.json` with `source: "./plugins/forward-roll"`.
3. `fr-impl` and `fr-review` are discoverable as omp task agents (and as Codex `.codex/agents/*.toml`).
4. `fr-bootstrap` reports `task.isolation.mode: none` effective and lists both agents.
5. End-to-end smoke (below) produces exactly one `jj` change, materialized only after `fr-review` returns clean.

## Acceptance criteria

- AC1: rebuild is deterministic and idempotent across both targets (stale files removed).
- AC2: `fr-impl` is edit-capable, read-only-`jj`; `fr-review` is read-only (no edit/write).
- AC3: omp agents use role aliases (`@default`/`@slow`); Codex agents omit `model`, pin `model_reasoning_effort`.
- AC4: the smoke test's changeset does not appear until review is clean (work sits in `@` until `jj squash`).

## Manual verification

Smoke test in this repo (dogfooding):
1. `python3 src/build.py` then run `fr-bootstrap` → confirm omp env summary.
2. Plan one trivial slice (e.g. "add a one-line changelog comment") via `fr-plan-slice`.
3. Run `fr-do`: confirm it dispatches `fr-impl` (non-isolated), then `fr-review`, then `jj squash` on clean.
4. `jj log` shows exactly one described change for the slice; before review, the work was only in `@`.

## Slice breakdown

| Slice | Deliverable | Key files |
|---|---|---|
| **02-01** | Multi-target build scaffold (targets concept, omp catalog at repo root, migrate old marketplace.json) | `plugin-build.json`, `build.py`, `src/plugin-shell/.omp-plugin/marketplace.json`, `scripts/verify_plugin_rebuild.py` |
| **02-02** | omp runtime config + bootstrap check (`.omp/config.yml`; `fr-bootstrap` verifies isolation mode + agent discoverability) | `.omp/config.yml`, `fr-bootstrap` SKILL + `bootstrap.py` + `resolve_context.py` |
| **02-03** | Custom agents — omp (`fr-impl.omp.md`, `fr-review.omp.md`; build emits `agents/*.md`) | `src/agent-templates/*.omp.md`, `plugin-build.json`, `build.py` |
| **02-04** | Custom agents — Codex (`*.codex.toml`; build emits `.codex/agents/*.toml`) | `src/agent-templates/*.codex.toml`, `plugin-build.json`, `build.py` |
| **02-05** | omp `fr-do` orchestration loop (task-dispatch `fr-impl`→`fr-review`→`jj squash` gate) | `fr-do` SKILL (omp variant) |
| **02-06** | End-to-end smoke + README/docs omp-first update | README.md, `src/plugin-shell/README.md`, smoke notes |

### Slice interfaces (contracts between slices)

- **02-01 produces** the `targets` schema in `plugin-build.json` (`{ omp: {...}, codex: {...} }`) and a `build.py` entry point that accepts `--target omp|codex|all`. **02-03/02-04 consume** it to register the agent assets under the right target.
- **02-02 produces** a `resolve_context.py` helper (e.g. `omp_environment()`) returning `{isolation_mode, agents_discoverable[]}`. **02-05 consumes** the isolation-mode guarantee before dispatching a non-isolated subagent.
- **02-03/02-04 produce** agents named exactly `fr-impl` and `fr-review` (name is the discovery key on both platforms). **02-05 consumes** those names in its dispatch instructions.

### Notes on verification posture (per `.forward-roll/runtime.json`)

- Build slices (02-01, 02-03, 02-04) verify via the existing `scripts/verify_plugin_rebuild.py` (deterministic rebuild, stale-file removal) extended for two targets — this is the high-signal end-to-end check, not unit tests on `build.py` internals.
- Agent definitions (02-03, 02-04) verify by confirming omp/Codex discovery surfaces them (a bootstrap/list check), not by asserting file text.
- The orchestration loop (02-05) verifies via the end-to-end smoke (02-06), since the contract is behavioral (changeset gated on review).

## Follow-up epic

**Epic 03 — workflow enrichment + Codex parity** (outlined; detailed via `fr-plan-epic` when reached):
- fr-specify brainstorm phase (`--mode brainstorm`) → spec.
- fr-plan-slice TDD-step contract (ordered steps + checkable acceptance).
- Codex `fr-do` dialect (dispatch via Codex subagent workflow).
- fr-review skill: dispatch the `fr-review` subagent across the epic stack (decided — same agent at epic scope; pass the epic's definition-of-done + full stack diff as the contract).

## Open confirm-items carried from spec §10

- omp isolation **default** — verify against omp source; determines whether `.omp/config.yml` *sets* `mode: none` or merely documents it (slice 02-02).
- Exact `output` schema fields for omp agents — finalize when authoring (slice 02-03).
- ~~How Codex discovers plugin-bundled agents~~ — **RESOLVED:** it does not; Codex plugins cannot bundle subagents. Codex agents emit to repo-root `.codex/agents/*.toml` (slice 02-04).
