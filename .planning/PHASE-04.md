# Phase 4: jj Review Workflow

## Purpose

Phase 4 defines the jj-native workflow language and review boundaries that later executable work must follow.

## Status

Contract coverage complete for `04-01` through `04-03`

## Task Contracts

### Task 04-01: jj-native workflow vocabulary

**Objective**  
Define the jj-native workflow vocabulary for revisions, changes, stacks, review states, and the `edit`/`squash` execution loop so later Phase 4 tasks can build on stable terms instead of re-inventing them.

**Why**  
Phase 4 cannot specify reviewer behavior or planning-state transitions coherently until the project has durable jj-native nouns and state boundaries. This contract turns the Phase 4 opener from a title into a planner-owned specification the execution prompt can derive from.

**Scope**  
- Define the core jj-native nouns Forward Roll should use for revision-level and stack-level discussion.
- Define the review-state vocabulary that describes how a phase deliverable moves between execution, review, and realignment.
- Define how the `jj edit` and `jj squash` loop supports task execution without leaking raw work-in-progress history across the phase review boundary.
- Update Phase 4 planning artifacts so `04-01` is represented as a durable task contract instead of only a roadmap line item.
- Update workflow-definition documentation if the vocabulary or loop description changes materially.

**Out of Scope**  
- Python or CLI implementation work for Phase 4 behavior.
- Reviewer-loop details that belong to `04-02`.
- Planning-state transition mechanics that belong to `04-03`.
- Git-shaped fallback terms, aliases, or compatibility framing.
- Phase 5 bootstrap execution design.

**References**  
- `lat.md/workflow.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`

**Design Constraints**  
- Keep the contract human-legible and durable.
- Use jj-native language throughout.
- Preserve milestone, phase, and task as the planning hierarchy.
- Constrain intent and boundaries without over-predicting final file layout.
- Keep the planning diff narrow and reviewable.

**Implementation Notes**  
- Prefer defining vocabulary in workflow-definition docs and letting planning artifacts reference that intent rather than duplicating long prose everywhere.
- Treat a revision as the reviewable jj unit, a change as the mutable unit an agent edits locally, and a stack as the ordered review context that may contain one or more task deliverables.
- Describe review states in terms of phase deliverable readiness and outcome, not Git hosting concepts.
- Keep `04-02` and `04-03` as follow-on tasks that consume this vocabulary rather than partially specifying them here.

**Automated Verification**  
- Run `lat check`.
- Confirm any new `lat.md` links and planning-doc references resolve cleanly.

**Manual Verification**  
- Read the Phase 4 artifacts top to bottom and confirm `04-01` now has a durable contract with all required sections.
- Confirm the vocabulary stays jj-native and does not introduce Git-shaped fallback terminology.
- Confirm the contract gives `04-02` enough shared terms to define the reviewer-facing loop without reopening core nouns.

**Definition of Done**  
- Phase 4 planning artifacts clearly show `04-01` as a specified task contract.
- The contract includes every required section in the agreed planning format.
- Workflow-definition docs describe the jj-native vocabulary and `edit`/`squash` loop clearly enough to anchor later Phase 4 tasks.
- `lat check` passes.

**Dependencies**  
- Existing Phase 4 roadmap entry and task naming.
- Existing workflow intent in `lat.md/workflow.md`.
- Phase 1 through Phase 3 planning terminology already recorded in `.planning/PROJECT.md` and `.planning/STATE.md`.

**Escalation Rules**  
- Escalate if defining the vocabulary would require changing milestone, phase, or task semantics beyond Phase 4 planning scope.
- Escalate if the workflow definition appears to require Git compatibility language to stay coherent.
- Escalate if `04-02` or `04-03` cannot be expressed cleanly after this contract without reshaping the broader roadmap.

### Task 04-02: reviewer-facing loop

**Objective**  
Specify the reviewer-facing loop for alignment, feedback, and post-phase decisions using the `04-01` jj-native vocabulary so Phase 4 has a durable review contract before any execution behavior is implemented.

**Why**  
Forward Roll needs a clear rule for what happens when a phase deliverable reaches review: what the reviewer evaluates, what outcomes are possible, and how feedback becomes new forward work. Without that contract, review remains an implied social step instead of a planner-defined boundary.

**Scope**  
- Define the reviewer-facing loop around the phase deliverable rather than individual task revisions.
- Define the baseline review outcomes and when each should be used.
- Define how reviewer feedback turns into additional forward work, including extending the same phase with new tasks when the concrete deliverable reveals missing scope.
- Clarify the orchestrator role when a task deliverable is unsatisfactory: create follow-on execution work rather than inventing sub-review states.
- Update Phase 4 planning and workflow-definition docs so `04-02` is represented as a contract-level task.

**Out of Scope**  
- Python or CLI implementation work for reviewer behavior.
- Detailed planning-state transition mechanics for roadmap and state artifacts; that belongs to `04-03`.
- Modeling review status on individual revisions or other jj execution units.
- Tracking accepted change shape, stack cleanup, or post-acceptance execution bookkeeping inside the planning model.
- Phase 5 bootstrap execution design.

**References**  
- `.planning/PHASE-04.md`
- `lat.md/workflow.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/PROJECT.md`

**Design Constraints**  
- Keep the contract human-legible and durable.
- Use the jj-native vocabulary from `04-01`.
- Keep the planning model forward-looking rather than retrospective about executed changes.
- Allow early phases to absorb review feedback by adding tasks without collapsing phase boundaries.
- Keep the planning diff narrow and reviewable.

**Implementation Notes**  
- The primary review object is the phase deliverable, even if that deliverable is composed from multiple task-level revisions.
- Baseline review outcomes should distinguish between `accepted`, `extend phase with follow-on task(s)`, and `needs broader realignment`.
- If a specific task deliverable misses the mark, the orchestrator should respond by defining another execution task with the feedback rather than assigning a separate durable review state to that task.
- The planning model should describe the next intended work, not the execution-history details of jj changes that were already reviewed.

**Automated Verification**  
- Run `lat check`.
- Confirm any new `lat.md` links and planning-doc references resolve cleanly.

**Manual Verification**  
- Read the Phase 4 artifacts top to bottom and confirm `04-02` now has a durable contract with all required sections.
- Confirm the review loop is defined around the phase deliverable rather than around individual revisions.
- Confirm the contract lets the orchestrator extend a phase with follow-on tasks after review without making the planning model track accepted change history.

**Definition of Done**  
- Phase 4 planning artifacts clearly show `04-02` as a specified task contract.
- The contract defines review outcomes in forward-looking planning terms.
- Workflow-definition docs describe how feedback creates new tasks or broader realignment without inventing task-level review states.
- `lat check` passes.

**Dependencies**  
- `04-01` jj-native workflow vocabulary.
- Existing Phase 4 roadmap entry and task naming.
- Existing workflow intent in `lat.md/workflow.md`.

**Escalation Rules**  
- Escalate if the reviewer loop cannot stay phase-deliverable-scoped without weakening the model.
- Escalate if follow-on task creation after review would require retroactive execution bookkeeping in planning artifacts.
- Escalate if `04-03` would need to absorb reviewer-loop semantics that should instead be settled here.

### Task 04-03: forward planning updates after review

**Objective**  
Define how planning artifacts should be updated after review so Forward Roll can record forward consequences of phase outcomes without turning planning docs into execution-history logs.

**Why**  
After `04-01` and `04-02`, the workflow has stable jj-native vocabulary and a clear reviewer loop, but it still lacks a planner-owned rule for how review outcomes should change `ROADMAP.md`, `STATE.md`, and future task planning. `04-03` closes that gap so Phase 4 can hand off a complete planning model to Phase 5.

**Scope**  
- Define how `.planning/STATE.md` should change after review while staying lightweight and forward-looking.
- Define how `.planning/ROADMAP.md` should change when review extends the current phase with new tasks.
- Define how broader realignment should update future phase/task planning without retroactively modeling executed jj history.
- Clarify the boundary between durable planning updates and execution/orchestration behavior.
- Update Phase 4 planning and workflow-definition docs so `04-03` is represented as a contract-level task.

**Out of Scope**  
- Python or CLI implementation work for planning updates.
- Execution-history tracking for accepted, rejected, or reshaped jj changes.
- Detailed subagent prompt design or orchestration tooling for Phase 5.
- Rewriting the full roadmap structure into nested subphases or retrospective state machines.
- Broadening into Phase 5 executable bootstrap behavior.

**References**  
- `.planning/PHASE-04.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `lat.md/workflow.md`
- `.planning/PROJECT.md`

**Design Constraints**  
- Keep planning artifacts forward-looking rather than retrospective.
- Keep `STATE.md` lightweight: current focus and concise status, not transition history.
- Allow a phase to grow by appending new tasks when review reveals more in-phase work.
- Let realignment reshape future planning without pretending the planner owns jj execution state.
- Keep the diff narrow and reviewable.

**Implementation Notes**  
- Treat review as a planning checkpoint that updates what happens next, not as a log of what already happened in the jj graph.
- When a phase is extended after review, append new tasks to the current phase in `ROADMAP.md` instead of creating subphases.
- When broader realignment happens, update future phase/task definitions based on what was learned, especially because later phases are expected to be planned in more detail only after the current phase completes.
- `STATE.md` should advance focus and summarize the next planning or execution target, but should not become a durable transition ledger.

**Automated Verification**  
- Run `lat check`.
- Confirm any new `lat.md` links and planning-doc references resolve cleanly.

**Manual Verification**  
- Read the Phase 4 artifacts top to bottom and confirm `04-03` now has a durable contract with all required sections.
- Confirm the planning-update rules stay forward-looking and do not model executed change history.
- Confirm the contract makes it clear how review can extend the current phase or reshape future phases without introducing subphases.

**Definition of Done**  
- Phase 4 planning artifacts clearly show `04-03` as a specified task contract.
- Workflow-definition docs explain how review changes planning artifacts in forward-looking terms.
- Phase 4 no longer has unspecified tasks.
- `lat check` passes.

**Dependencies**  
- `04-01` jj-native workflow vocabulary.
- `04-02` reviewer-facing loop contract.
- Existing planning artifact roles in `.planning/ROADMAP.md` and `.planning/STATE.md`.

**Escalation Rules**  
- Escalate if forward-only planning updates are not sufficient to keep later phase planning coherent.
- Escalate if review-driven phase extension would require nested phase structure rather than appended tasks.
- Escalate if Phase 5 planning would still need to infer artifact-update rules that should have been settled here.

## Phase 4 Contract Coverage

- `04-01`: Specified
- `04-02`: Specified
- `04-03`: Specified
