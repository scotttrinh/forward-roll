# Phase 5: First Executable Slice

## Purpose

Phase 5 turns the spec-first workflow into the first executable self-hosting slice.

## Status

Current focus: `05-02`

## Task Contracts

### Task 05-01: executable bootstrap contract

**Objective**  
Define the first executable self-hosting bootstrap contract so Forward Roll can take explicit roots and project identity inputs, then produce the planning and execution context needed to start a real agentic loop.

**Why**  
Phase 4 defined the workflow model, but there is still no executable contract that says what the first runnable self-hosting slice consumes, what it produces, and where it stops. This task creates the durable boundary the later Phase 5 implementation tasks will follow.

**Scope**  
- Define the minimum input bundle for the first executable slice, including `repo_root`, `specs_root`, `plans_root`, and project identity or default values.
- Define the defaulting rules and validation expectations for those inputs.
- Define the minimum durable outputs the bootstrap flow must create in `plans_root`.
- Define the boundary between bootstrap planning outputs, prompt/template assets, and execution launch behavior.
- Update Phase 5 planning artifacts so `05-01` is represented as a contract-level task.

**Out of Scope**  
- Implementing the bootstrap code path.
- Writing generic workflow prompt templates in full.
- Launching execution or review loops.
- Expanding into broader agent-provider abstractions.
- Reworking earlier phase contracts.

**References**  
- `lat.md/workflow.md`
- `lat.md/architecture.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/PROJECT.md`

**Design Constraints**  
- Keep the contract narrow enough that implementation can start immediately afterward.
- Preserve independent `specs_root` and `plans_root` handling.
- Treat `lat.md` as the aspirational source and planning artifacts as forward operational state.
- Keep the contract durable and human-legible.
- Avoid smuggling implementation detail into orchestration semantics prematurely.

**Implementation Notes**  
- The first executable slice should still be spec-first, but it no longer stops at planning-only artifacts.
- The contract should define outputs that are sufficient for later Phase 5 tasks to derive prompts and launch a phase.
- Defaults should be explicit, but the model should not assume the two roots share a parent or governance model.

**Minimum Input Bundle**  

| Input | Requirement | Default | Notes |
|-------|-------------|---------|-------|
| `repo_root` | Required | None | Resolved repository root for the codebase the phase will operate on. |
| `specs_root` | Optional | `repo_root / "lat.md"` | Readable aspirational-spec root. It may live inside or outside `repo_root`. |
| `plans_root` | Optional | `repo_root / ".planning"` | Writable planning root. It may live inside or outside `repo_root`. |
| `project.name` | Optional | `repo_root.name` | Human-legible project identity for generated planning context. Richer identity fields stay out of scope for `05-01`. |
| `values` | Optional | Forward Roll default value set | Omitted values use the current default set as a whole. Partial merge semantics stay out of scope for `05-01`. |

**Defaulting and Validation Expectations**  
- Resolve all path inputs at the adapter boundary before entering typed bootstrap logic.
- Require `repo_root` to exist and be a directory.
- Require `specs_root` to resolve to a readable specification root; `05-01` does not require deeper semantic validation of the graph contents.
- Require `plans_root` to resolve to a writable directory or a creatable directory under a writable parent.
- Reject empty project names after defaulting or normalization.
- Fail with stable, reviewable validation errors when required inputs are missing, roots are unusable, or defaults cannot be applied cleanly.
- Do not infer a shared workspace root, shared parent directory, or shared governance model between `specs_root` and `plans_root`.

**Minimum Durable Outputs in `plans_root`**  
- A machine-readable bootstrap context artifact that records the resolved input bundle, defaults actually applied, and the resolved `specs_root` and `plans_root` paths.
- The forward planning artifact set needed for execution handoff: `PROJECT.md`, `ROADMAP.md`, `STATE.md`, and the active `PHASE-XX.md` task-contract document for the first launched phase.
- A durable indication of the active phase and next task inside the planning artifacts so later tasks do not have to rediscover phase focus from raw specs alone.
- A concise human-reviewable bootstrap summary that explains what roots were used, what defaults were applied, and what planning target is ready for the later launch task.

**Boundary for Later Phase 5 Tasks**  
- `05-01` owns input resolution, defaulting rules, validation expectations, and the durable planning-plus-context outputs written under `plans_root`.
- `05-02` owns the reusable prompt-template assets and the runtime input contract they consume; `05-01` should only make that consumption possible.
- `05-03` owns phase-launch behavior, task sequencing, and live execution context; `05-01` should stop before agent invocation or jj execution begins.
- `05-04` owns operator feedback handling after launch; `05-01` should not model live review or follow-up-task mechanics.
- `05-05` owns end-to-end verification and reviewer docs for the implemented slice; `05-01` only defines the contract that later verification must exercise.

**Automated Verification**  
- Run `lat check`.
- Confirm planning-doc references and any new `lat.md` links resolve cleanly.

**Manual Verification**  
- Confirm the contract makes Phase 5 implementation possible without reopening core bootstrap inputs and outputs.
- Confirm the contract preserves the independent-roots decision.
- Confirm later Phase 5 tasks can consume this contract without redefining bootstrap scope.

**Definition of Done**  
- Phase 5 planning artifacts clearly show `05-01` as a specified task contract.
- The contract defines the first executable slice inputs, defaults, outputs, and boundary clearly enough to implement.
- `lat check` passes.

**Dependencies**  
- Completed Phase 4 contracts.
- Spec-first workflow and independent-roots decisions already recorded in `lat.md` and `.planning/PROJECT.md`.

**Escalation Rules**  
- Escalate if the minimum executable contract cannot stay narrow enough for a first self-hosting slice.
- Escalate if input defaulting rules would force a shared workspace-root model.
- Escalate if later Phase 5 tasks still need to invent core bootstrap inputs or outputs.

### Task 05-02: generic workflow prompt templates

**Objective**  
Specify the generic, cacheable workflow prompt/template system that Phase 5 will use so prompts remain reusable assets with specs and plans as inputs rather than bespoke generated prompt text.

**Why**  
The first executable slice needs prompts, but prompt generation should not become a second planning system. This task defines the stable prompt-template layer so orchestration can supply changing context while the prompts themselves remain generic and cache-friendly.

**Scope**  
- Define the prompt-template roles needed for the first self-hosting slice.
- Define what runtime inputs those templates receive from `specs_root`, `plans_root`, and bootstrap context.
- Define what side effects or artifact expectations each template is allowed to have.
- Define cacheability expectations so prompt structure remains stable across runs.
- Update Phase 5 planning artifacts so `05-02` is represented as a contract-level task.

**Out of Scope**  
- Implementing the prompt-template loader or renderer.
- Full provider abstraction.
- Encoding project-specific prompt text per run.
- Defining the complete orchestration state machine.
- Broad execution telemetry design.

**References**  
- `.planning/PHASE-05.md`
- `lat.md/workflow.md`
- `lat.md/architecture.md`
- `.planning/PROJECT.md`

**Design Constraints**  
- Prompts should be generic assets, not bespoke output generated from planning data each time.
- Specs and plans should be prompt inputs, not hardcoded prompt bodies.
- Prompt structure should maximize cacheability across repeated runs.
- The contract should stay compatible with Codex-first execution.

**Implementation Notes**  
- The first slice likely needs at least planning, execution, and review/operator-facing prompt roles.
- Template inputs should be explicit enough that orchestration can remain typed and reviewable.
- Prompt outputs should align with the task-contract model rather than bypass it.

**Automated Verification**  
- Run `lat check`.
- Confirm any new spec references resolve cleanly.

**Manual Verification**  
- Confirm the template model does not depend on per-run custom-written prompts.
- Confirm specs and plans are treated as runtime context sources.
- Confirm the contract is narrow enough that implementation can stay cache-oriented.

**Definition of Done**  
- Phase 5 planning artifacts clearly show `05-02` as a specified task contract.
- The prompt-template model is generic, cacheable, and compatible with the rest of Phase 5.
- `lat check` passes.

**Dependencies**  
- `05-01` executable bootstrap contract.
- Existing spec-first and task-contract workflow definitions.

**Escalation Rules**  
- Escalate if prompt reuse and cacheability cannot coexist with the required workflow inputs.
- Escalate if templates would need to embed project-specific planning logic directly.
- Escalate if orchestration behavior cannot be expressed cleanly using generic templates.

### Task 05-03: phase execution launch contract

**Objective**  
Define how the first executable slice launches a full phase from plans and specs so Forward Roll can move beyond prompt emission into real self-hosted execution.

**Why**  
The project goal is not just to emit a single prompt. Forward Roll needs a clear contract for how a prepared phase becomes an active execution loop, including how task sequencing and prompt/template usage fit together.

**Scope**  
- Define the first supported execution entrypoint for launching a phase.
- Define how the orchestrator consumes task contracts, prompt templates, and runtime context to start execution.
- Define the initial task sequencing expectations for a phase launch without overcommitting to a long-term scheduler design.
- Define the handoff boundaries between planning artifacts and live execution context.
- Update Phase 5 planning artifacts so `05-03` is represented as a contract-level task.

**Out of Scope**  
- Implementing the launcher.
- Full multi-phase orchestration.
- Broad concurrency or delegation strategy beyond what the first phase launch needs.
- Automating retrospective planning updates after execution.
- Broad audit or telemetry features.

**References**  
- `.planning/PHASE-05.md`
- `lat.md/workflow.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

**Design Constraints**  
- The first entrypoint should launch a full phase, not merely emit one task prompt.
- The contract should stay narrow enough to support one meaningful vertical slice.
- Live execution should still respect the durable planner-owned task contracts.
- The phase launch should remain compatible with jj-native review boundaries.

**Implementation Notes**  
- The first launcher can stay simple if the task contracts are strong and prompt templates are well-scoped.
- It is acceptable for the initial sequencing model to be mostly serial if that keeps the slice reviewable.
- Execution context should be derived from existing plans and specs rather than inventing a third source of truth.

**Automated Verification**  
- Run `lat check`.
- Confirm any new references resolve cleanly.

**Manual Verification**  
- Confirm the contract defines a real phase launch rather than merely planning or prompt emission.
- Confirm the contract leaves room for later orchestration refinement without invalidating the first slice.
- Confirm the contract still treats task contracts as the durable execution unit.

**Definition of Done**  
- Phase 5 planning artifacts clearly show `05-03` as a specified task contract.
- The first phase-launch boundary is clear enough to implement.
- `lat check` passes.

**Dependencies**  
- `05-01` executable bootstrap contract.
- `05-02` generic workflow prompt-template contract.
- Completed Phase 4 review-boundary definitions.

**Escalation Rules**  
- Escalate if a meaningful first launch requires a much broader orchestration system than Phase 5 can carry.
- Escalate if phase launch would bypass task contracts or prompt-template boundaries.
- Escalate if the first launch cannot remain reviewable and narrow.

### Task 05-04: continuous operator feedback loop

**Objective**  
Define the first continuous operator-in-the-loop review and feedback contract so the self-hosting slice can absorb review input by extending the active phase with follow-on tasks.

**Why**  
The user goal is not only “plan once and run once.” The first usable self-hosting slice should support iterative work with the operator, where feedback becomes additional tasks inside the current phase whenever that is the right boundary.

**Scope**  
- Define how operator feedback enters the active phase loop.
- Define how new tasks are appended to an existing phase based on feedback.
- Define how the orchestrator distinguishes between in-phase follow-up work and broader realignment.
- Define the minimum durable planning updates needed when the operator steers the loop.
- Update Phase 5 planning artifacts so `05-04` is represented as a contract-level task.

**Out of Scope**  
- Implementing the loop mechanics.
- Full conversational UX design.
- Automating every possible replanning path.
- Reopening Phase 4 review semantics.
- General-purpose chat memory features.

**References**  
- `.planning/PHASE-05.md`
- `lat.md/workflow.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/PHASE-04.md`

**Design Constraints**  
- Feedback handling should compose naturally with the existing phase/task model.
- Adding follow-up tasks should be straightforward rather than a special-case workflow.
- The loop should stay forward-looking in planning artifacts.
- The contract should avoid creating a separate retrospective state machine.

**Implementation Notes**  
- The operator loop should reuse the review outcomes already defined in Phase 4.
- Follow-up tasks should be appended when work still belongs inside the current phase boundary.
- The first implementation can keep the operator loop explicit and reviewable rather than highly automated.

**Automated Verification**  
- Run `lat check`.
- Confirm any new references resolve cleanly.

**Manual Verification**  
- Confirm the loop supports iterative operator guidance without breaking the phase/task model.
- Confirm follow-up tasks can be added to the active phase without inventing subphases.
- Confirm broader realignment remains distinct from in-phase follow-up work.

**Definition of Done**  
- Phase 5 planning artifacts clearly show `05-04` as a specified task contract.
- The operator feedback loop is clear enough to implement as part of the first usable self-hosting slice.
- `lat check` passes.

**Dependencies**  
- Phase 4 reviewer-loop and planning-update contracts.
- `05-03` phase execution launch contract.

**Escalation Rules**  
- Escalate if iterative operator feedback cannot compose with the current phase/task model.
- Escalate if follow-up tasks would require a different phase structure.
- Escalate if the loop would force planning artifacts to become retrospective execution logs.

### Task 05-05: end-to-end verification and reviewer docs

**Objective**  
Define the verification and reviewer-facing documentation contract for the first self-hosting vertical slice so the new executable loop can be tested and understood end to end.

**Why**  
A self-hosting slice is only useful if it can be reviewed and validated. This task keeps verification and documentation first-class instead of treating them as cleanup after implementation.

**Scope**  
- Define the tests needed to validate the first end-to-end self-hosting slice.
- Define the reviewer-facing documentation needed to explain the flow from specs to planning to execution to operator feedback.
- Define the minimum happy-path and feedback-path verification expectations.
- Update Phase 5 planning artifacts so `05-05` is represented as a contract-level task.

**Out of Scope**  
- Writing the tests or docs.
- Broad QA infrastructure.
- Exhaustive failure-mode coverage beyond what the first slice needs.
- Broader milestone planning beyond Phase 5.

**References**  
- `.planning/PHASE-05.md`
- `lat.md/workflow.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

**Design Constraints**  
- Verification should stay aligned with the user-facing self-hosting story.
- Tests should favor narrow, high-value end-to-end coverage over noisy breadth.
- Reviewer docs should explain the operator loop and planning updates clearly.
- The contract should keep verification work reviewable and scoped.

**Implementation Notes**  
- The core acceptance story is: go from vague idea and specs to an agentic first version through a reviewable loop.
- Verification should include at least one path where operator feedback appends new work to the active phase.
- Docs should show how generic prompts, specs, and plans interact without making prompts the source of truth.

**Automated Verification**  
- Run `lat check`.
- Confirm any new references resolve cleanly.

**Manual Verification**  
- Confirm the contract covers both the initial path and at least one iterative feedback path.
- Confirm the verification approach matches the intended self-hosting story.
- Confirm documentation needs are concrete enough for implementation.

**Definition of Done**  
- Phase 5 planning artifacts clearly show `05-05` as a specified task contract.
- Verification and reviewer-doc expectations are clear enough to implement after the earlier Phase 5 tasks land.
- `lat check` passes.

**Dependencies**  
- `05-01` through `05-04`.
- Existing quality posture recorded in the planning docs.

**Escalation Rules**  
- Escalate if end-to-end verification would require a broader implementation slice than Phase 5 currently targets.
- Escalate if reviewer documentation cannot stay aligned with the actual executable boundaries.
- Escalate if the intended self-hosting story still cannot be validated cleanly after the earlier tasks are defined.

## Phase 5 Contract Coverage

- `05-01`: Specified with explicit inputs, defaults, outputs, and handoff boundary
- `05-02`: Specified
- `05-03`: Specified
- `05-04`: Specified
- `05-05`: Specified
