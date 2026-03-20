# Workflow

This document defines bootstrap flow, review boundaries, and jj-native workflow intent.

## Bootstrap Flow

Bootstrap should establish typed project context and an externalizable planning boundary.

The first Forward Roll workflow should establish:

1. a typed project identity
2. a specs root that may be distinct from the plans root
3. a plans root that may be external to the repository
4. a durable default value set
5. a knowledge graph that stays readable by humans and queryable by agents

At the adapter boundary, bootstrap inputs should be loadable from TOML so agents can produce stable, reviewable config artifacts instead of relying only on ad hoc CLI flags.

Related:

- [[architecture#Planning Storage]]
- [[domain#Planning Root]]

## Executable Bootstrap Contract

The first executable bootstrap contract should resolve roots and defaults, then stop at a durable handoff boundary.

For the first self-hosting slice, bootstrap should:

1. accept `repo_root`, `specs_root`, `plans_root`, project identity, and default values as explicit or defaultable inputs
2. resolve those inputs into concrete paths and stable typed context before execution begins
3. persist a machine-readable bootstrap context artifact in `plans_root`
4. materialize or update the forward planning artifacts the later launch step will consume
5. stop before prompt rendering, agent invocation, or live jj execution

The minimum durable planning outputs should include project, roadmap, state, and active phase/task context. Prompt templates and live execution are downstream concerns that must consume this boundary rather than redefine it.

## Bootstrap Config Loading

Bootstrap config loading turns a TOML document into a typed directive at the adapter boundary.

This path should resolve relative paths from the config location, apply default values when the values table is omitted, validate readable `specs_root` plus writable or creatable `plans_root`, and fail with stable errors when the document shape is invalid.

Code references:

- [[src/forward_roll/adapters/bootstrap_config.py]]
- [[tests/test_bootstrap_config.py]]

## Bootstrap Summary Rendering

Bootstrap summary rendering turns a typed directive into a concise, reviewable text artifact.

The executable bootstrap handoff should now surface the resolved repository, specification, and planning roots, the defaults actually applied, and the active phase/task target that later launch steps will consume.

Code references:

- [[src/forward_roll/application/bootstrap.py]]
- [[tests/test_bootstrap_config.py]]

## Bootstrap Command

The bootstrap command is the current agent-facing entry point for this repository slice.

It should accept direct CLI inputs or a TOML config file, preserve the repo-root versus `specs_root` versus `plans_root` distinction, persist the durable bootstrap handoff artifacts, and print stable success or validation outputs without embedding domain logic in the command body.

Code references:

- [[src/forward_roll/cli.py]]

## Workflow Prompt Templates

Forward Roll should use generic workflow prompt templates rather than generating bespoke prompt text for every run.

Those templates should treat specs, plans, and runtime context as inputs. The prompts themselves should remain stable enough to maximize cacheability across repeated executions.

This keeps prompt assets reusable and reviewable while preserving the planner-owned task contracts as the source of workflow intent.

The first slice should define three template roles:

1. `planning_update` for planning-artifact updates and in-phase task extension work
2. `task_execution` for executing one active task contract
3. `phase_review` for reviewer-facing outcome and next-step guidance

Each role should be a versioned asset with stable instructions and named input slots rather than a prompt body rewritten per run.

Code references:

- [[src/forward_roll/application/prompts.py]]
- [[tests/test_phase_launch.py]]

### Prompt Runtime Inputs

Runtime prompt inputs should come from explicit slots, not hidden process state.

The shared input envelope should include bootstrap context from `plans_root`, relevant spec context from `specs_root`, relevant planning artifacts from `plans_root`, and optional operator or workspace context when the selected role needs them.

Specs and plans should enter as referenced context blocks, excerpts, or attachments. They should not be collapsed into the invariant template instructions.

Code references:

- [[src/forward_roll/application/prompts.py]]
- [[src/forward_roll/application/phase_launch.py]]

### Prompt Cacheability

Cacheability depends on stable template assets and predictable context binding.

Forward Roll should keep role identity, template version, slot ordering, and output shape stable across runs. Changes to prompt semantics should happen by versioning the asset, while run-specific differences should show up only in the bound slot content.

Related:

- [[architecture#Workflow Prompt Assets]]
- [[architecture#Bootstrap Handoff Boundary]]

## Phase Launch Contract

Phase launch should consume durable planning state and run a real phase to its review boundary.

The first supported launch entrypoint should read bootstrap context from `plans_root`, resolve the active phase and its ordered task contracts, and execute that phase rather than emitting a single standalone prompt.

Launch should fail with stable, reviewable errors when the bootstrap artifact is missing, the active phase cannot be resolved, no incomplete task contracts remain, or the required prompt-template roles are unavailable.

Code references:

- [[src/forward_roll/application/phase_launch.py]]
- [[src/forward_roll/cli.py]]
- [[tests/test_phase_launch.py]]

### Initial Task Sequencing

The first launch slice should prefer a simple serial loop over a broad scheduler.

Task order should come from the active phase contract. The launcher should execute one task contract at a time with the `task_execution` template, require each task to end as one reviewable jj revision with reported verification, and stop immediately when a task escalates or cannot satisfy its contract.

When all currently planned tasks in the active phase are complete, the launcher should invoke the `phase_review` template and hand off a reviewer-facing outcome instead of inventing new execution scope on its own.

Code references:

- [[src/forward_roll/application/phase_launch.py]]
- [[tests/test_phase_launch.py]]

### Planning and Live Execution Context

Planning artifacts should stay the durable source of truth for scope and sequencing.

Bootstrap context, active phase and task contracts, and prompt-template identity should remain durable planning inputs. Live execution context should be derived at launch time from those artifacts plus runtime workspace state such as jj status, revision identifiers, bound prompt inputs, and task-local verification results.

The launcher may update planning artifacts only to keep the current focus truthful or because an active task contract explicitly requires a planning-file change. It should not create a separate permanent orchestration state store for the first slice.

Code references:

- [[src/forward_roll/application/phase_launch.py]]

## Phase Review Loop

Every phase should have a hard boundary between implementation and review. That review is part of the spec lifecycle: it can validate the phase, trigger scope realignment, or update the project model before the next phase begins.

Before work is handed to a reviewer, orchestrator, or user, the active stack should be reduced to a meaningful deliverable shape rather than exposing raw work-in-progress history.

## Planning Units

Forward Roll uses milestones, phases, and tasks as distinct workflow units.

A milestone is the broad collection of related phases. A phase is the planner-defined review boundary: it should produce a meaningful deliverable that can be accepted, rejected, or realigned before downstream work continues. A task is the execution unit inside a phase: it should be narrow enough for one autonomous agent to complete with a clear write scope, verification story, and definition of done.

Tasks should carry the practical context an execution agent needs without overcommitting to the final file layout. The planner should define the task through intent-based fields such as objective, why, scope, out of scope, references, design constraints, implementation notes, automated verification, manual verification, definition of done, dependencies, and escalation rules.

The planner owns that durable task contract. The orchestrator may package it with execution-specific context, but should not have to invent the scope or acceptance criteria from scratch. Phases carry the review contract that tells the orchestrator how those task outputs fit into the broader milestone.

## Specification and Planning Flow

Forward Roll should treat specification and planning as adjacent but distinct layers in one workflow rather than as disconnected tools.

The intended flow is:

1. Start by shaping the aspirational outcome in `lat.md` before planning or execution begins.
2. Use those linked specs as the semantic source for what the project is trying to become, even when there is no code yet.
3. Let Forward Roll turn the current specification gap into phases, then turn the active phase into task contracts, then orchestrate execution.
4. When specs evolve later, treat any new mismatch between specs and code as a new planning problem that Forward Roll must analyze and realign through more phases and tasks.

This means `lat.md` owns the aspirational specification layer, while planning artifacts own the forward execution plan that responds to those specifications. The two layers should be modeled as independent roots so durable specs do not require the same storage or governance as plans.

## jj Workflow Vocabulary

Forward Roll should name jj workflow objects and review states directly so planning and review stay aligned with jujutsu instead of drifting back to Git-shaped terms.

Use these terms consistently in planning and workflow docs:

- A revision is the reviewable jj history node that can be inspected, discussed, and accepted as part of a phase deliverable.
- A change is the mutable unit an agent is actively editing locally while work is still in progress.
- A stack is the ordered revision context that represents related work under review, including task deliverables that must still make sense together.
- A review state is the named outcome of a phase deliverable at the review boundary. Phase 4 currently needs `in execution`, `ready for review`, `needs realignment`, and `accepted` as the durable baseline.

These terms are intentionally not interchangeable. Agents work inside changes, reviewers evaluate revisions, and the phase boundary cares about the state of the deliverable stack rather than raw local work.

## jj Execution Loop

Forward Roll should use `jj edit` and `jj squash` together instead of treating them as competing workflows.

During execution, agents may use `edit` to create and rename small, intent-based working changes that keep intermediate steps legible and isolate atomic work. Before reporting back upstream, they should use `squash` to collapse those work-in-progress changes into the meaningful task-level commits that make up the phase deliverable the reviewer is meant to evaluate.

This split gives the workflow both local flexibility and reviewable output: granular history while the agent is thinking, and human-sized deliverables once the work is ready to leave the local execution loop.

The practical loop is: use `jj edit` while shaping or renaming active changes inside a task, then use `jj squash` before upstream handoff so the reviewer sees the intended task-level revisions rather than incidental execution steps.

Related:

- [[workflow#jj Workflow Vocabulary]]
- [[workflow#Phase Review Loop]]
- [[workflow#Planning Units]]
- [[workflow#jujutsu Role]]

## Reviewer Loop

The reviewer-facing loop should evaluate the phase deliverable and decide the next forward action rather than trying to track execution details of individual task changes.

The baseline outcomes are:

- `accepted` when the phase deliverable is good enough to let downstream work continue
- `extend phase with follow-on task(s)` when the review reveals concrete missing work that still belongs inside the current phase boundary
- `needs broader realignment` when the review shows the phase boundary, intent, or downstream assumptions need to be reframed before execution continues

If a specific task deliverable is weak, the orchestrator should create another execution task with that feedback instead of inventing a separate durable review state for the task itself.

This keeps the planning model forward-looking. Planning artifacts should describe the next intended work after review, not the accepted or rejected execution history of jj changes.

## Planning Updates After Review

After review, planning artifacts should be updated to reflect what happens next, not to preserve a detailed transition log of the completed execution.

`STATE.md` should stay lightweight by updating the current focus and a concise status summary. It should not become a ledger of review transitions.

If review reveals more work inside the same phase boundary, `ROADMAP.md` should append new tasks inside the existing phase rather than creating subphases.

If review triggers broader realignment, planning should reshape future phases and future task contracts based on what was learned. This is especially important because the detailed substance of later phases is expected to be planned after the current phase completes.

## Continuous Operator Feedback

Operator feedback should extend the running phase only through reviewable planning updates.

### Feedback Entry

Operator input should enter the loop alongside the active phase contract, current planning state, relevant spec context, and the latest review outcome.

Raw comments are not durable planning state by themselves. The planning-update step should classify them into either in-phase follow-on work or broader realignment before any planning artifact changes.

### In-Phase Follow-On Tasks

Follow-on tasks belong in the active phase only when the phase goal still stands and the missing work is concrete enough to express as a narrow task contract.

When that happens, planning should append the next phase-local task IDs at the end of the current phase order rather than creating subphases or renumbering existing tasks. The active phase stays open, and focus moves to the first new incomplete task.

### Broader Realignment Boundary

Broader realignment should remain distinct from in-phase follow-up work.

If feedback changes the phase goal, success criteria, review boundary, or future roadmap shape, planning should treat that as broader realignment instead of hiding it inside appended tasks. If feedback is too vague to become a reviewable task contract, the loop should stop for clarification rather than fabricating scope.

## First Self-Hosting Slice

The first executable self-hosting slice should go beyond planning-only bootstrap output.

It should take aspirational specs plus planning context, launch a real phase, and support iterative operator feedback by appending follow-up tasks inside the active phase when that feedback still belongs within the current phase boundary.

That slice should stay narrow by relying on strong task contracts and reusable prompt templates rather than a broad custom orchestration system.

Its bootstrap step should therefore persist the resolved execution context durably in `plans_root` so later prompt and launch steps can start from reviewable planning state rather than ephemeral CLI input.

## End-to-End Verification

The first self-hosting slice should be validated by a small set of reviewable end-to-end stories and reviewer docs.

### Happy-Path Coverage

One verification path should start from linked specs, persist bootstrap context and planning artifacts, launch the active phase, execute the planned tasks, and reach an `accepted` review outcome without manual state reconstruction.

### Feedback-Path Coverage

A second verification path should prove that review plus operator input can append the next phase-local task contracts inside the active phase, update `ROADMAP.md`, `STATE.md`, and the active phase contract consistently, and keep the same phase open.

### Reviewer-Facing Documentation

Reviewer docs should explain the slice entry conditions, bootstrap handoff artifacts, prompt-template roles, phase execution and review loop, operator-feedback append rules, and the artifacts to inspect during the happy-path and feedback-path checks.

## lat.md Role

`lat.md` is the intended human-and-agent-readable knowledge substrate.

It should carry the aspirational specification for the system first, before planning is decomposed into phases and tasks. Its search, linking, and templating features should already be useful even when the codebase is empty or incomplete.

Forward Roll should then consume that specification layer from `specs_root`, derive planning work into `plans_root`, execute against it, and keep specs and code in sync as the project evolves.

## jujutsu Role

Forward Roll should exploit jj's automatic change tracking rather than papering over it with Git-shaped assumptions. That means the workflow model should talk about revisions, change stacks, and review states in jj-native language.
