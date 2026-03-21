# Forward Roll

Forward Roll is a Codex-first agentic workflow tool for software projects. It takes the core idea behind GSD-style planning and execution, then reorients it around jujutsu, explicit review checkpoints, human-legible project knowledge, and a plugin-first Codex packaging model.

## Current direction

The current direction in this repository focuses on four foundations:

- Codex-first workflows instead of Claude Code-first workflows
- jujutsu-native change management instead of Git-centric assumptions
- local planning artifacts that are designed to live outside the target repository when needed
- a static Codex plugin whose skills read config at runtime instead of relying on install-time templating

The current implementation work uses:

- `attrs` for frozen domain types
- `cattrs` for boundary structuring in adapters
- deterministic config files and helper scripts as the runtime contract for shipped skills
- `mypy`, `ruff`, `pytest`, and `hypothesis` as the intended quality toolchain

## Early status

This repository currently contains:

- a strict Python package scaffold in `src/forward_roll/`
- local planning artifacts under `.planning/`
- an initial `lat.md/` knowledge graph that documents the intended architecture and domain

## Plugin direction

Forward Roll should ship as one Codex plugin, not as a standalone CLI product surface.

The plugin should bundle static `fr-*` skills plus deterministic helper scripts. A bootstrap skill should create or refresh config, and later skills should resolve repo, specs, and plans context from that config at runtime.

## Reviewer Guide

### Entry Conditions

The first executable slice expects a readable `specs_root`, a writable `plans_root`, and a bootstrap handoff already persisted in `plans_root`.

The minimum durable artifacts are `bootstrap-context.json`, `BOOTSTRAP.md`, `PROJECT.md`, `ROADMAP.md`, `STATE.md`, and the active `PHASE-XX.md` contract file.

### Bootstrap Handoff Boundary

Bootstrap resolves roots and defaults once, writes that durable context into `plans_root`, and stops before prompt rendering or execution begins.

Later launch and feedback steps consume `bootstrap-context.json` plus the copied planning artifacts instead of re-deriving scope from CLI input.

### Prompt-Template Roles

Forward Roll currently exposes three reusable prompt assets:

- `planning_update`: classifies review or operator feedback into appended in-phase tasks, broader realignment, or clarification.
- `task_execution`: executes one active task contract and must report the verification actually performed.
- `phase_review`: reviews the completed phase deliverable and returns the next forward action without silently doing more implementation.

### Phase Launch And Review Loop

`launch_phase` reads the active phase from bootstrap context, executes incomplete task contracts in roadmap order, updates planning truth between tasks, and stops at phase review.

The first slice stays serial on purpose. Each task must end with reported verification and a reviewable jj deliverable before the next task or the phase review proceeds.

### Operator Feedback Extension Path

When phase review plus operator input still belongs inside the active phase boundary, `apply_operator_feedback` binds the `planning_update` role and appends the next phase-local task IDs to `ROADMAP.md` and `PHASE-XX.md`.

`STATE.md` then moves focus to the first appended task. Broader realignment and clarification stay explicit in `STATE.md` without destructively rewriting the current phase plan.

### Verification Checklist

Review the slice by checking:

- the bootstrap handoff artifacts in `plans_root`
- the ordered task and review flow in `tests/test_phase_launch.py`
- the acceptance path where phase review returns `accepted`
- the feedback path where review plus operator input appends `05-0X` follow-on work without renumbering prior tasks
