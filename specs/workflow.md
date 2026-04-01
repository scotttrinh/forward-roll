# Workflow

This document defines Forward Roll's plugin-first command model, planning loop, and jj-native review flow.

## Bootstrap Flow

Bootstrap should establish a deterministic runtime contract for the plugin.

The bootstrap flow should identify `repo_root`, `specs_root`, `plans_root`, project identity, and any required runtime conventions, then write those results into explicit config or derived files that every shipped skill can read. It should stop once later skills can resolve the same runtime view without guessing.

Related:

- [[architecture#Planning Storage]]
- [[architecture#Runtime Contract]]

## Executable Bootstrap Contract

Bootstrap should create runtime truth, not an install-time variant of the plugin.

For the plugin-shaped product, bootstrap should:

1. accept or discover `repo_root`, `specs_root`, `plans_root`, and project identity
2. validate that those roots are readable or writable where required
3. persist a machine-readable runtime contract the later skills can consume
4. explain the resolved runtime view in a concise human-readable summary
5. stop before milestone planning, phase execution, or review work begins

The durable outputs should make the rest of the plugin reproducible. If two runs begin from the same workspace and config inputs, later skills should resolve the same runtime context bundle.

## Bootstrap Config Loading

Bootstrap config loading should turn explicit configuration into a stable runtime contract.

Config should resolve installation-specific paths and conventions without requiring bundled skills to be rewritten. Loading should apply stable defaults, normalize paths, fail with reviewable errors when required inputs are missing or invalid, and keep the runtime contract legible enough for both humans and scripts to inspect.

## Bootstrap Summary Rendering

Bootstrap summary rendering should report the runtime contract clearly.

The bootstrap summary should surface the resolved repository, specs, and plans roots, the project identity, and any important runtime conventions the rest of the plugin will use. It should stay short enough to review quickly while still making the installation-specific context explicit.

## Bootstrap Command

The bootstrap command should be a shipped skill, not a standalone product entrypoint.

Operators should use a bootstrap skill to create or refresh runtime config, review the resolved roots, and confirm the plugin can see the expected planning and spec context. Repo-local CLI helpers may exist during development, but the product boundary should be the bootstrap skill inside the plugin.

## Workflow Prompt Templates

Forward Roll should ship stable workflow instructions rather than generating bespoke instructions for each run.

The plugin should include reusable prompt or instruction assets for planning, execution, review, and feedback-classification work. Those assets should accept runtime context through explicit inputs and keep their structure stable enough that the product boundary remains understandable and reproducible.

## Phase Launch Contract

Phase launch should consume planning truth and run one bounded phase to its review boundary.

The execution flow should read the active phase contract, resolve its ordered tasks, perform the required work, update planning artifacts only where the task or review boundary requires it, and stop at a reviewer-facing phase outcome. It should fail with stable errors when required planning context, runtime config, or execution assets are missing.

## Phase Review Loop

Every phase should end at an explicit review boundary.

Execution should produce reviewable jj revisions, then stop for a reviewer-facing outcome: accept the phase, extend the phase with concrete follow-on work, or trigger broader realignment. Review is part of the product loop, not an optional afterthought.

## Planning Units

Forward Roll uses milestones, phases, and tasks as distinct workflow units.

A milestone is the broad product objective. A phase is the review boundary that should produce a meaningful deliverable. A task is the smallest bounded unit that one skill, script, or future subagent can execute with a clear scope, verification story, and definition of done.

## Specification and Planning Flow

Specs and planning should remain separate layers of one workflow.

The intended loop is:

1. shape the aspirational product in linked spec documents
2. derive or update plans that move toward that product
3. execute the active phase against those plans
4. review the result and either accept it, extend it, or realign the plan

Specs should define what Forward Roll is trying to become. Planning artifacts should define the next concrete work needed to get there.

## jj Workflow Vocabulary

Forward Roll should use jj-native language throughout the workflow.

A revision is the reviewable output. A change is the mutable thing still being edited. A stack is the ordered revision context under review. Review states should describe the phase deliverable, not incidental local execution history.

## jj Execution Loop

Execution should optimize for reviewable jj output, not raw local history.

Agents or scripts may use whatever local editing flow is practical, but the workflow should surface task-sized revisions and meaningful stacks at review time. The product should preserve jj-native concepts instead of translating them into Git-shaped abstractions.

## Reviewer Loop

The reviewer loop should decide the next forward action.

The baseline review outcomes are:

- `accepted`
- `extend phase with follow-on task(s)`
- `needs broader realignment`

The workflow should update planning truth to reflect what happens next rather than trying to preserve a full execution transcript in the planning artifacts.

## Planning Updates After Review

Planning artifacts should be updated to show the next intended work.

`STATE.md` should keep the current focus legible. `ROADMAP.md` should reflect the next real tasks or phases. If review reveals more work inside the same phase boundary, append follow-on tasks. If review changes the phase boundary or milestone shape, treat that as broader realignment.

## Continuous Operator Feedback

Operator feedback should enter the workflow through explicit planning updates.

Raw comments are not durable planning state. Feedback must be turned into either concrete in-phase follow-on tasks, broader realignment, or a request for clarification before plans change.

## Plugin-First Self-Hosting

Forward Roll should ship first as one static Codex plugin.

The plugin should provide these operator-facing skills:

1. `$fr-bootstrap`
2. `$fr-plan-milestone`
3. `$fr-plan-phase <phase-number>`
4. `$fr-execute-phase <phase-number>`
5. `$fr-feedback-phase <phase-number>`

These skills should be understandable as static shipped assets. Installation-specific behavior should come from config and deterministic scripts, not from rewriting the shipped instructions.

## Plugin Composition

Each operator-facing command should be one bundled skill under the plugin `skills/` tree.

The plugin should ship static skill text, bundled scripts, reusable instruction assets, and marketplace metadata. A reviewer should be able to inspect the plugin package and understand what commands exist, what runtime helpers exist, and how config drives the installation-specific parts of behavior.

## Bootstrap Skill And Runtime Config

Bootstrap should be a skill that creates or refreshes config.

The bootstrap skill should discover or accept the relevant roots, validate them, write the runtime contract, and report the resolved view. It must not rewrite bundled skills, rewrite the plugin manifest for one installation, install dependencies, or recreate the old pattern of copying host-visible assets into place as the normal runtime path.

## Refactor Target State

The big refactor should end with a plugin-native product boundary.

The target state is:

1. Forward Roll ships as one plugin package with marketplace wiring.
2. The plugin contains static skills and deterministic runtime scripts.
3. `$fr-bootstrap` creates or refreshes config only.
4. Other skills resolve runtime context from config and shared conventions.
5. The runtime does not depend on a shared installable Python package or dependency installation.
6. Future subagent support can slot into pre-defined handoff boundaries without changing the operator-facing commands.

## Milestone Planning Command

Milestone planning should enter through one host-facing skill that updates the next milestone without guessing.

`$fr-plan-milestone` should treat all trailing operator text as milestone-planning intent, not as a phase selector. Before editing planning artifacts, it should load runtime config, active planning artifacts, the relevant spec excerpts or references identified for this project, and any jj or workspace context needed to keep the planning update reviewable.

The skill should update milestone-scoped planning artifacts consistently:

1. `PROJECT.md`
2. `REQUIREMENTS.md`
3. `ROADMAP.md`
4. `STATE.md`

It should stay narrow, stop instead of guessing when the milestone objective is vague, and hand specialized work to deterministic helper assets or future subagents without giving up final reporting and final spec-and-plan validation.

## Milestone-Local Phase Commands

Phase commands should resolve `<phase-number>` relative to the active milestone.

An operator should be able to say `$fr-plan-phase 1`, `$fr-execute-phase 1`, or `$fr-feedback-phase 1` for the first phase of the active milestone even when planning artifacts use global phase IDs. The skill layer should own that translation and should stop with a stable error when the selector is invalid or ambiguous.

## Agent Role Boundaries

Forward Roll should define subagent boundaries even before plugins can rely on subagent support.

The aspirational product should include specialized planning, execution, review, and feedback-classification roles. Until plugin subagents exist, skills and scripts should preserve those same handoff boundaries in deterministic local logic so the product does not have to be conceptually redesigned later.

## Shared Skill Context

Every Forward Roll skill should load the same core context first.

That shared context should include:

1. runtime config
2. the active planning artifacts from `plans_root`
3. the relevant spec context from `specs_root`
4. operator input
5. any jj or workspace context the command needs

Skills should name the kind of context they need instead of hard-coding one fixed repository shape into the instructions. They should identify the relevant spec sections or files through explicit references, project conventions, or deterministic lookup rules, and they should keep the spec layer current when workflow behavior changes.

## Shared Helper Handoff Bundle

Skills should hand helper scripts or future subagents one explicit context bundle.

That bundle should include the operator-facing intent, the selected milestone or phase context, the relevant planning artifacts, the relevant spec context, and the workspace facts needed for bounded execution. It should be reproducible from the same config and workspace inputs.

## End-to-End Verification

The first self-hosting slice should be validated with a small number of reviewable end-to-end stories.

One story should prove the happy path from specs and config through planning, execution, and accepted review. Another should prove the feedback path where review plus operator input appends follow-on work inside the same phase boundary. Reviewer-facing docs should explain the same boundary and artifact story those tests exercise.

## Specification Role

Forward Roll should rely on a generic spec layer rather than one required spec tool.

The spec layer should describe the product we want, the boundaries we intend to preserve, and the workflow ideas that should survive refactors. Planning should respond to that spec layer; it should not replace it. This repository may continue to maintain those specs in `specs/`, but the shipped plugin should treat them as ordinary project documents and explicit references rather than assuming any repo-specific spec tooling exists at runtime.

## jujutsu Role

Forward Roll should remain jj-native in both language and workflow intent.

The product should talk about revisions, changes, stacks, and review states directly, and should avoid falling back to Git-shaped assumptions when describing how work is planned, executed, or reviewed.
