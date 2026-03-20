# Phase 7: Milestone Planning Skill

## Purpose

Phase 7 ships the first concrete milestone-planning entrypoint in the Forward Roll skill pack.

## Status

Contract coverage in progress for `07-01`

## Task Contracts

### Task 07-01: `$fr-plan-milestone` skill contract

**Objective**  
Define the operator-facing `$fr-plan-milestone` contract and implement the repo-owned skill entrypoint so Forward Roll can scaffold the next milestone through a host-native skill.

**Why**  
Phase 6 defined the skill-pack layout, command surface, and shared context bundle, but there is still no concrete milestone-planning command an operator can load and review. This task makes the first self-hosting milestone-planning boundary explicit without taking on the later role orchestration work.

**Scope**  
- Define the operator input and stop conditions for `$fr-plan-milestone`.
- Define the minimum planning and spec context the skill must load before milestone planning begins.
- Define the milestone-scoped planning artifacts this skill is allowed to update.
- Implement the repo-owned skill entrypoint at `.agents/skills/fr-plan-milestone/SKILL.md`.
- Update Phase 7 planning artifacts so `07-01` is represented as a contract-level task.

**Out of Scope**  
- Defining milestone-planning orchestrators or supporting role descriptors.
- Verifying the end-to-end milestone scaffolding flow against real milestone updates.
- Implementing `$fr-plan-phase`, `$fr-execute-phase`, or `$fr-feedback-phase`.
- Reworking the Phase 6 shared-context or selector contracts.
- Adding Python-only wrappers for a host-native skill boundary.

**References**  
- `lat.md/workflow.md`
- `lat.md/architecture.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.agents/skills/fr-plan-milestone/SKILL.md`

**Design Constraints**  
- `$fr-plan-milestone` must not accept a phase selector or milestone-local phase number.
- The skill must stay host-native as a `SKILL.md` asset under `.agents/skills/`.
- The skill must reuse the Phase 6 shared context contract, including the repo `lat` workflow and jj-native vocabulary.
- The skill must limit durable edits to milestone-scoped planning artifacts: `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.
- The skill must stop for ambiguity instead of inventing milestone scope, numbering, or requirements.

**Implementation Notes**  
- The skill should treat any user text after `$fr-plan-milestone` as milestone-planning intent or constraints, not as a phase selector.
- Before planning, the skill should load `AGENTS.md`, the active planning artifacts, and the relevant `lat.md` sections that describe skill-first self-hosting and host-asset boundaries.
- The skill should follow the repo `lat` workflow by expanding operator input, searching for relevant spec sections when available, falling back to `lat locate` plus direct reads when semantic search is unavailable, updating `lat.md` when behavior changes, and running `lat check` before finishing.
- The skill should update `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md` consistently when milestone planning succeeds.
- The skill should execute directly for now and stop before inventing specialized milestone-planning role prompts or orchestration; Phase `07-02` owns that boundary.

**Required Stops**  
- The operator supplies a phase selector or milestone-local phase number.
- Required planning artifacts are missing or inconsistent enough that the next milestone cannot be identified reviewably.
- The milestone objective or scope is too vague to update planning artifacts without guessing.
- Relevant `lat.md` guidance cannot be resolved well enough to keep planning grounded in specs.
- The requested change would cross into phase-planning, execution, or feedback behavior reserved for later phases.

**Automated Verification**  
- Run `uv run pytest`.
- Run `lat check`.

**Manual Verification**  
- Confirm the skill entrypoint makes it clear that `$fr-plan-milestone` is a no-phase-selector command.
- Confirm the contract keeps milestone planning limited to `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.
- Confirm later Phase 7 tasks can add orchestrators and verification without reopening this operator-facing boundary.

**Definition of Done**  
- Phase 7 planning artifacts clearly show `07-01` as a specified task contract.
- The repo contains a reviewable `.agents/skills/fr-plan-milestone/SKILL.md` entrypoint.
- The skill contract states the required planning inputs, allowed artifact updates, and stable stop conditions.
- `lat check` passes.

**Dependencies**  
- Phase 6 skill-pack layout, command surface, and shared-context contracts.
- Existing self-hosting and `lat.md` workflow decisions in planning artifacts.

**Escalation Rules**  
- Escalate if `$fr-plan-milestone` needs a phase selector to stay coherent.
- Escalate if milestone planning cannot stay within `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.
- Escalate if the skill would need specialized role prompts before its operator-facing contract can be defined reviewably.
