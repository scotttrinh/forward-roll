# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-20)

**Core value:** Deliver an agentic workflow that remains structurally rigorous, reviewable by humans, and faithful to the domain even as automation increases.
**Current focus:** Phase 6 - Self-Hosting Skill-Pack Surface (task contracts defined)

## Current Position

Phase: 6 of 11 (Self-Hosting Skill-Pack Surface)
Task: 06-02 of 3 in current phase
Status: Ready for execution
Last activity: 2026-03-20 — Completed task 06-01 by defining the repo-local and user-local skill-pack layout plus whole-pack and per-command copy rules

Progress: [█████-----] 48%

## Performance Metrics

**Velocity:**
- Total tasks completed: 19
- Planned tasks remaining: 17
- Average duration per task: -
- Total execution time: -

**By Phase:**

| Phase | Tasks | Total | Avg/Task |
|-------|-------|-------|----------|
| 1 | 2 | - | - |
| 2 | 3 | - | - |
| 3 | 3 | - | - |
| 4 | 3 | - | - |
| 5 | 8 | - | - |
| 6 | 1 | 3 | - |
| 7 | 0 | 3 | - |
| 8 | 0 | 3 | - |
| 9 | 0 | 3 | - |
| 10 | 0 | 3 | - |
| 11 | 0 | 3 | - |

**Recent Trend:**
- Last 5 tasks: 05-05, 05-06, 05-07, 05-08, 06-01
- Trend: Stable

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Phase 1: Bootstrap around Codex-first, jj-native, strict Python, and `lat.md`.
- Phase 1: Treat review checkpoints as mandatory specification realignment steps.
- Phase 2: Keep `lat.md/.cache/` on disk but out of version tracking.
- Phase 2: Keep runtime validation at the adapter boundary with TOML -> cattrs -> attrs rather than in the domain model.
- Phase 2: Use `typer` for the initial agent-facing CLI surface while keeping outputs stable and machine-legible.
- Phase 2: Use `.planning/` as the repo-local default instead of `.locals-only/.planning/`; planning-root override remains first-class.
- Phase 3: Treat `lat.md` leaf sections plus explicit `@lat` backlinks as the proof that project memory is first-class rather than incidental prose.
- Phase 3: Keep knowledge-graph validation narrow and end-to-end by testing section presence, code discoverability, and backlinks for the current Python slice.
- Planning docs are now intentionally committed with the codebase, so `.planning/` is part of the reviewable project history in this repository.
- Phase 4: Use `jj edit` for intent-named atomic working changes during execution, then `jj squash` to produce task commits that together form the reviewable phase deliverable.
- Forward Roll uses milestones as collections of phases, and tasks as the single-agent execution unit within a phase.
- Phase 4: Task contracts should describe intent and boundaries through `Scope`, `Out of Scope`, and `References` instead of predicting exact file touch points up front.
- Phase 4: `04-01` is the first contract-level task, and its durable specification now lives in `.planning/PHASE-04.md`.
- Phase 4: Review applies to the phase deliverable, and reviewer feedback should produce new forward tasks or broader realignment rather than task-level review states.
- Phase 4: Planning artifacts should record forward consequences after review by updating next focus, appending in-phase tasks when needed, and reshaping future phases without logging jj execution history.
- Forward Roll should treat `lat.md` as the aspirational specification layer first, then derive planning work from the gap between those specs and the current implementation state.
- Phase 5 should begin with a spec-to-plan bootstrap contract rather than a generic bootstrap artifact writer contract.
- Forward Roll should model `specs_root` and `plans_root` independently so durable specs and ephemeral plans can live under different storage policies.
- Phase 5: bootstrap should persist resolved roots, defaults, and the active planning target in `plans_root` before prompt rendering or execution launch begins.
- Phase 5 should use generic, cacheable workflow prompt templates with specs and plans as runtime inputs rather than bespoke generated prompts.
- Phase 5: prompt templates should be versioned workflow assets with stable role identities and named runtime slots instead of per-run rewritten prompt bodies.
- The first executable slice should launch a full phase and support iterative operator feedback by appending follow-up tasks inside the active phase.
- Phase 5: phase launch should consume durable planning context, execute task contracts serially to reviewable jj revisions, and stop at phase review rather than inventing new execution scope.
- Phase 5: launch should bind stable workflow assets to explicit bootstrap, spec, planning, and workspace slots, then update durable planning truth between serial task steps.
- Phase 5: operator feedback should enter through a planning update that either appends the next phase-local task contracts or triggers broader realignment without turning raw comments into durable plan state.
- Phase 5: the first executable slice is now verified by end-to-end acceptance and feedback-extension tests, with reviewer docs pointing at the same bootstrap, planning, and phase artifacts.
- Phase 6+: self-hosting should ship first as copyable Codex skills and agent role descriptors rather than waiting for richer standalone CLI coverage.
- Phase 6+: self-hosting commands should use milestone-local phase numbers, resolving `phase 1` in the active milestone to the correct durable global phase ID in planning artifacts.
- Phase 6: the repo-owned self-hosting pack should mirror Codex host boundaries, with command skills under `.agents/skills/fr-*` and role descriptors under `.codex/agents/fr-*`.
- Phase 6: every `fr-*` skill should assemble shared planning, spec, and jj context before delegating to specialized roles, then finish by validating `lat.md` integrity.

### Pending Todos

- None.

### Blockers/Concerns

- No active blockers. The main planning constraint is to stay jj-native in language and state modeling without leaking Git assumptions back into the workflow.

## Session Continuity

Last session: 2026-03-20 11:05 EDT
Stopped at: Planned Phase 6; next step is executing task `06-01` for the self-hosting skill-pack milestone
Resume file: None
