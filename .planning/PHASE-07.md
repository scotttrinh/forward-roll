# Phase 7: Milestone Planning Skill

## Purpose

Phase 7 ships the first concrete milestone-planning entrypoint in the Forward Roll skill pack.

## Status

Contract coverage in progress for `07-01` through `07-02`

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

### Task 07-02: milestone-planning orchestrator and supporting roles

**Objective**  
Define the specialized milestone-planning orchestrator and supporting role descriptors, and wire `$fr-plan-milestone` to delegate through that role family after it assembles the shared context bundle.

**Why**  
`07-01` defined the operator-facing command boundary, but milestone planning still needs a concrete role layer that can be copied with the skill pack and reviewed independently from the command entrypoint. This task makes the first milestone-planning delegation path explicit without taking on end-to-end milestone verification.

**Scope**  
- Define the milestone-planning role family for `$fr-plan-milestone`.
- Define the responsibility split between the operator-facing skill, the orchestrator, and the supporting milestone-planning roles.
- Implement the repo-owned role descriptors under `.codex/agents/`.
- Update `.agents/skills/fr-plan-milestone/SKILL.md` so the skill hands specialized work to the orchestrator while preserving the `07-01` guardrails.
- Update Phase 7 planning artifacts so `07-02` is represented as a contract-level task.

**Out of Scope**  
- Verifying the end-to-end milestone scaffolding flow against real milestone updates.
- Reworking the no-phase-selector contract from `07-01`.
- Defining role descriptors for `$fr-plan-phase`, `$fr-execute-phase`, or `$fr-feedback-phase`.
- Adding generated manifests, installers, or Python-only wrappers for the role layer.
- Expanding milestone planning beyond `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.

**References**  
- `lat.md/workflow.md`
- `lat.md/architecture.md`
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.agents/skills/fr-plan-milestone/SKILL.md`
- `.codex/agents/fr-milestone-planning-orchestrator.md`
- `.codex/agents/fr-milestone-planner.md`
- `.codex/agents/fr-milestone-plan-checker.md`

**Design Constraints**  
- `$fr-plan-milestone` must stay the operator-facing no-phase-selector command defined by `07-01`.
- The skill must keep owning command parsing, shared-context assembly, final reporting, and final `lat check`.
- Specialized milestone-planning work must flow through copyable role descriptors under `.codex/agents/`.
- The orchestrator and supporting roles must stay limited to milestone-scoped planning edits in `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.
- The role layer must use jj-native vocabulary and stop on ambiguity instead of guessing milestone scope or phase-level work.

**Implementation Notes**  
- The skill should assemble a reviewable handoff bundle containing operator intent, milestone-scoped planning artifacts, relevant `lat.md` context, and any workspace or jj context needed for milestone planning.
- Specialized work should flow first through `fr-milestone-planning-orchestrator`, which may delegate only to `fr-milestone-planner` and `fr-milestone-plan-checker`.
- `fr-milestone-planner` should propose or apply the minimum durable edits needed in `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.
- `fr-milestone-plan-checker` should verify those edits stay inside the milestone-planning boundary, preserve durable roadmap numbering, and leave the planning artifacts mutually consistent before the skill reports completion.
- The role layer should return reviewable stop reasons whenever ambiguity, missing context, or later-phase workflow drift prevents a narrow milestone update.

**Required Stops**  
- The shared context bundle is missing enough planning or spec context that the next milestone cannot be updated reviewably.
- The request would require edits outside `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.
- The operator request or proposed edits drift into phase planning, phase execution, or feedback-extension behavior.
- The checker cannot reconcile the milestone updates without widening scope or guessing missing decisions.
- The orchestrator would need hidden host state instead of the explicit shared bundle from the skill.

**Automated Verification**  
- Run `uv run pytest`.
- Run `lat check`.

**Manual Verification**  
- Confirm `$fr-plan-milestone` points to a concrete milestone-planning orchestrator role.
- Confirm the repo contains copyable supporting role descriptors under `.codex/agents/`.
- Confirm the role boundary keeps final validation in the skill and specialized milestone edits in the role layer.

**Definition of Done**  
- Phase 7 planning artifacts clearly show `07-02` as a specified task contract.
- The repo contains reviewable milestone-planning role descriptors under `.codex/agents/`.
- `.agents/skills/fr-plan-milestone/SKILL.md` delegates specialized work through the orchestrator without weakening the `07-01` guardrails.
- `lat check` passes.

**Dependencies**  
- The `07-01` skill contract.
- Phase 6 layout, selector, and shared-context contracts.
- Existing `lat.md` workflow and host-asset boundaries.

**Escalation Rules**  
- Escalate if milestone planning cannot stay within the four milestone-scoped planning artifacts.
- Escalate if the orchestrator needs a phase selector or unresolved hidden state to stay coherent.
- Escalate if the supporting roles would need to absorb final command validation that belongs in the skill.
