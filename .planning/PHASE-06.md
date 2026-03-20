# Phase 6: Self-Hosting Skill-Pack Surface

## Purpose

Phase 6 defines the copyable Codex-hosted surface for Forward Roll self-hosting.

## Status

Contract coverage complete for `06-01` through `06-03`

## Task Contracts

### Task 06-01: skill-pack layout and installation story

**Objective**  
Define the concrete Forward Roll skill-pack layout and copy/install story so operators can place self-hosting assets into Codex directories without depending on the Python CLI.

**Why**  
Phase 5 proved the first executable workflow slice, but it is still repo-specific and not yet packaged as a host-native self-hosting surface. This task defines the durable artifact layout that later self-hosting skills and role descriptors will implement.

**Scope**  
- Define the repo-owned source layout for operator-facing `fr-*` skills.
- Define the repo-owned source layout for copyable agent-role descriptors.
- Define the supported repo-local and user-local installation targets for those assets.
- Define naming and composition rules so the pack can be copied as a whole or command-by-command.
- Update Phase 6 planning artifacts so `06-01` is represented as a contract-level task.

**Out of Scope**  
- Implementing the `fr-*` skills or role descriptors.
- Building an installer, package manager integration, or sync command.
- Defining every role prompt body in full.
- Replacing Python helpers with host assets where helper code remains the simpler boundary.
- Broad standalone CLI parity.

**References**  
- `lat.md/architecture.md`
- `lat.md/workflow.md`
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

**Design Constraints**  
- The install story must remain file-based and host-native.
- Operators should be able to self-host through copied assets without invoking the Python CLI.
- The artifact layout should mirror Codex host boundaries instead of inventing a private packaging model.
- Operator-facing commands should have stable names aligned with the roadmap.
- The contract should stay narrow enough that Phase 7 through Phase 10 can implement against it directly.

**Implementation Notes**  
- The repository-owned source of operator-facing skills should be `.agents/skills/fr-*`, with one directory per command and one `SKILL.md` entrypoint per directory.
- The repository-owned source of copyable role descriptors should be `.codex/agents/fr-*`, using `.md` instructions plus optional `.toml` runtime metadata when a role needs both files.
- Shared prompt assets, parsers, or Python helper code may live outside those host directories when they are implementation details rather than installable host artifacts.
- The contract should support two usage modes:
  1. repo-local self-hosting that uses the versioned `.agents/skills/` and `.codex/agents/` assets directly from the repository
  2. user-local installation that copies the same assets into user-local Codex directories such as `~/.codex/skills/` and `~/.codex/agents/`
- The copy/install story should work for the whole pack and for individual commands, without requiring a hidden registry or generated manifest before the first self-hosting milestone is usable.

**Minimal Artifact Layout**  

| Artifact Class | Repository-Owned Source | Host-Facing Purpose |
|----------------|-------------------------|---------------------|
| Operator skills | `.agents/skills/fr-plan-milestone/`, `.agents/skills/fr-plan-phase/`, `.agents/skills/fr-execute-phase/`, `.agents/skills/fr-feedback-phase/` | User-facing command entrypoints loaded by Codex. |
| Role descriptors | `.codex/agents/fr-*.md` plus optional `.codex/agents/fr-*.toml` | Specialized planning, execution, review, and planning-update roles referenced by the skills. |
| Helper assets | repo-owned implementation paths outside host directories | Shared prompt assets, parsers, and support code that skills or roles may consume without becoming installable host entrypoints themselves. |

**Boundary for Later Phases**  
- Phase 6 owns the artifact layout and copy/install contract.
- Phase 7 through Phase 10 own the concrete skill implementations and supporting role prompts that live inside that layout.
- Phase 11 owns proving the layout is reproducible end to end.

**Automated Verification**  
- Run `lat check`.
- Confirm all new planning and `lat.md` references resolve cleanly.

**Manual Verification**  
- Confirm an operator could understand where each host asset lives without reading implementation code.
- Confirm the layout supports both repo-local and user-local usage.
- Confirm later phases can add real skill content without reopening the install boundary.

**Definition of Done**  
- Phase 6 planning artifacts clearly show `06-01` as a specified task contract.
- The self-hosting skill pack has a concrete source layout and copy/install story.
- The layout does not depend on the Python CLI as the installation boundary.
- `lat check` passes.

**Dependencies**  
- Completed Phase 5 contracts and implementation.
- Existing Codex-first and `lat.md` workflow decisions in `PROJECT.md`.

**Escalation Rules**  
- Escalate if the install story requires generated state or a registry before the first milestone can self-host.
- Escalate if the proposed layout collapses operator-facing skills and specialized role descriptors into one unclear boundary.
- Escalate if the copy/install story would force dependence on the Python CLI.

### Task 06-02: command surface and milestone-local phase selectors

**Objective**  
Define the stable `fr-*` command surface and milestone-local phase selector semantics so operators can target the active milestone without losing durable global planning IDs.

**Why**  
The self-hosting milestone is meant to feel local to the current milestone, but the planning artifacts still need stable global phase identifiers. This task defines that operator-facing translation boundary before later command implementations land.

**Scope**  
- Define the operator-facing command set and required arguments for the first self-hosting milestone.
- Define the milestone-local phase-number semantics for the commands that accept `<phase-number>`.
- Define the resolution boundary between milestone-local selectors and durable global phase IDs.
- Define the minimum error cases the command layer must surface instead of guessing.
- Update Phase 6 planning artifacts so `06-02` is represented as a contract-level task.

**Out of Scope**  
- Implementing the commands.
- Redesigning roadmap numbering outside what selector resolution requires.
- Adding alternate selector syntaxes such as labels, slugs, or fuzzy text lookup.
- Defining multi-milestone orchestration behavior.
- Broad command alias or shell-completion work.

**References**  
- `lat.md/workflow.md`
- `lat.md/architecture.md`
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

**Design Constraints**  
- Operator-facing phase numbers should be milestone-local and one-based.
- Durable planning artifacts should keep globally unique phase IDs as the canonical identifiers.
- Selector resolution should happen before specialized planning or execution work begins.
- Error cases should be explicit and reviewable rather than inferred from partial state.
- The command surface should stay small and predictable for the first self-hosting milestone.

**Implementation Notes**  
- The Phase 6 command surface should remain the four roadmap commands:
  1. `$fr-plan-milestone`
  2. `$fr-plan-phase <phase-number>`
  3. `$fr-execute-phase <phase-number>`
  4. `$fr-feedback-phase <phase-number>`
- `$fr-plan-milestone` should not take a phase selector.
- `$fr-plan-phase`, `$fr-execute-phase`, and `$fr-feedback-phase` should require a milestone-local `<phase-number>` argument.
- Selector resolution should follow a stable sequence:
  1. load the active milestone context from durable planning state
  2. identify the ordered phase list that belongs to that milestone
  3. map the one-based milestone-local selector to the corresponding durable global phase ID
  4. pass the resolved global phase ID to downstream planning, execution, or feedback workflows
- After resolution, planning artifacts and role handoffs should speak in global IDs such as `06` or `PHASE-06.md`; milestone-local numbers are host-facing convenience, not the canonical stored identifier.

**Required Error Cases**  
- No active milestone can be resolved from planning artifacts.
- The supplied milestone-local phase number is not a positive integer.
- The supplied milestone-local phase number is outside the active milestone range.
- The resolved global phase lacks the durable planning artifact the selected command needs, such as `PHASE-XX.md` for phase-specific work.
- The active milestone or roadmap state is internally inconsistent enough that selector resolution would be ambiguous.

**Boundary for Later Phases**  
- Phase 6 owns the command names, argument expectations, selector semantics, and resolution/error contract.
- Phase 7 through Phase 10 own the concrete behavior that each command performs after selector resolution succeeds.
- Future milestones may add richer selectors, but they must not weaken the stable global phase identity defined here.

**Automated Verification**  
- Run `lat check`.
- Confirm any new links between roadmap, state, and workflow sections resolve.

**Manual Verification**  
- Confirm an operator can understand why `$fr-plan-phase 1` targets the first phase of the active milestone.
- Confirm the contract preserves global phase IDs inside durable planning artifacts.
- Confirm the required error cases are explicit enough that later implementations will not guess.

**Definition of Done**  
- Phase 6 planning artifacts clearly show `06-02` as a specified task contract.
- The `fr-*` command surface is stable for the self-hosting milestone.
- Milestone-local phase selectors have explicit resolution and error rules.
- `lat check` passes.

**Dependencies**  
- `06-01` skill-pack layout and installation story.
- Existing roadmap and state artifacts that identify the current phase and milestone direction.

**Escalation Rules**  
- Escalate if milestone-local selectors cannot be resolved without mutating canonical phase IDs.
- Escalate if the command surface needs more than the four planned commands to stay coherent.
- Escalate if selector resolution depends on hidden host state rather than durable planning artifacts.

### Task 06-03: shared context contract for skills and roles

**Objective**  
Define the shared context contract that keeps Forward Roll skills, agent roles, `lat.md`, planning artifacts, and jj workflow guidance aligned across the self-hosting milestone.

**Why**  
The self-hosting pack only works if every command starts from the same project truth. Without a shared context contract, the new skills would rediscover specs, plans, and workflow rules independently and drift away from each other.

**Scope**  
- Define the minimum planning, spec, and workflow context every `fr-*` skill must load before specialized work.
- Define the shared handoff bundle that skills pass to specialized role descriptors.
- Define how the `lat.md` workflow and jj-native vocabulary stay mandatory inside the self-hosting commands.
- Define the responsibility split between operator-facing skills, specialized roles, and optional Python helpers.
- Update Phase 6 planning artifacts so `06-03` is represented as a contract-level task.

**Out of Scope**  
- Writing the final role prompt bodies.
- Defining a broad scheduler or concurrency model.
- Implementing runtime parsing utilities.
- Replacing repo-level agent instructions.
- Reworking the earlier executable slice contracts.

**References**  
- `lat.md/workflow.md`
- `lat.md/architecture.md`
- `lat.md/domain.md`
- `.planning/PROJECT.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

**Design Constraints**  
- Every `fr-*` command should begin from the same durable project truth.
- Skills should respect the repository `lat` workflow instead of bypassing it.
- Skills and roles should use jj-native workflow language consistently.
- The shared context should be explicit and reviewable, not hidden in host-local memory.
- The contract should keep role responsibilities narrow enough that later phases can implement them independently.

**Implementation Notes**  
- Before specialized work, every `fr-*` skill should load:
  - project agent instructions
  - active planning artifacts such as `PROJECT.md`, `ROADMAP.md`, `STATE.md`, and the relevant `PHASE-XX.md` contract when one exists
  - relevant `lat.md` sections from `specs_root`
  - repo-local `lat` and jj skills or their documented equivalents when present
- Every `fr-*` skill should follow the repo `lat` workflow by:
  1. expanding operator input
  2. searching or locating relevant spec sections before changing behavior or plans
  3. updating `lat.md` when functionality, architecture, tests, or workflow behavior change
  4. running `lat check` before handoff
- Every `fr-*` skill should preserve jj-native terms such as revision, change, stack, and review state instead of falling back to Git-shaped language.
- Skills should pass a shared handoff bundle to specialized roles that includes command intent, resolved global phase ID when applicable, relevant planning artifacts, relevant spec context, operator input, and any workspace context required by the selected role.
- Skills own command parsing, selector resolution, shared context assembly, and final validation. Specialized roles own milestone planning, phase planning, plan checking, execution, review, or planning updates after that context is assembled. Python helpers may support parsing or rendering, but they should remain optional implementation support rather than the primary host boundary.

**Minimal Role Families**  

| Command | Minimum Specialized Roles |
|---------|---------------------------|
| `$fr-plan-milestone` | milestone planning roles |
| `$fr-plan-phase <phase-number>` | phase research, planning, and plan-checking roles |
| `$fr-execute-phase <phase-number>` | execution and review roles |
| `$fr-feedback-phase <phase-number>` | planning-update roles |

**Boundary for Later Phases**  
- Phase 6 owns the shared context contract and role-family boundaries.
- Phase 7 through Phase 10 own the concrete role content and command implementations that consume this contract.
- Phase 11 owns proving the roles and shared context remain aligned through the full roundtrip.

**Automated Verification**  
- Run `lat check`.
- Confirm the new spec and planning references resolve cleanly.

**Manual Verification**  
- Confirm each command starts from the same planning and spec context.
- Confirm `lat.md` maintenance and jj terminology remain mandatory instead of optional guidance.
- Confirm later command implementations can divide work between skills and specialized roles without reopening the shared context contract.

**Definition of Done**  
- Phase 6 planning artifacts clearly show `06-03` as a specified task contract.
- The shared context contract is explicit enough to keep all `fr-*` commands aligned.
- Skill versus role responsibilities are clear enough that later phases can implement them independently.
- `lat check` passes.

**Dependencies**  
- `06-01` skill-pack layout contract.
- `06-02` command surface and milestone-local selector contract.
- Existing `lat.md` and jj workflow decisions from earlier phases.

**Escalation Rules**  
- Escalate if the shared context contract still leaves core planning or spec inputs implicit.
- Escalate if `lat.md` maintenance or jj language becomes optional inside the self-hosting commands.
- Escalate if role boundaries are too vague for later phases to implement without redefining scope.
