# Workflow

This document defines Forward Roll's operator-facing workflow.

## Main Loop

Forward Roll should feel fluid to use while still enforcing high-signal context and clear review boundaries.

The main loop is:

1. `$fr-bootstrap`
2. `$fr-specify`
3. `$fr-plan-epic`
4. `$fr-plan-slice`
5. `$fr-do`
6. `$fr-feedback`
7. `$fr-review`

These commands are the product surface. Everything else exists to support them.

The internal plugin authoring workflow may use a repository-local build step to assemble those commands into the final Codex plugin layout, as long as the shipped skill bundles remain self-contained and the operator-facing command surface does not change.

## `$fr-bootstrap`

Bootstrap establishes the operator's working contract for one project.

It should:

1. resolve `repo_root`
2. resolve or accept `specs_root`
3. resolve or accept `plans_root`
4. resolve the planning layout used inside `plans_root`
5. detect jj availability and basic workflow assumptions
6. record whether those roots are in-repo, out-of-repo, or gitignored
7. persist the runtime contract
8. summarize the resolved environment and stop

Bootstrap must not turn into a broad setup installer. Its job is to make the workflow usable here and now.

The bootstrap implementation should live inside the bootstrap skill bundle rather than depending on a plugin-wide runtime module.

## `$fr-specify`

Specify creates or sharpens the durable high-level specs for the project.

It should support two modes:

- `discover`: inspect an existing codebase and derive high-level specs from what already exists
- `describe`: turn a new idea or change direction into tight high-level specs before implementation work begins

In either mode, specify should focus on:

- architecture
- technical guidance
- workflow rules
- user and operator flows
- codebase standards
- system boundaries and invariants

Specify should remain above implementation detail. It should describe the system well enough that the project could be recreated, but not sink into code-level instruction for one local change.

## `$fr-plan-epic`

Plan epic defines one reviewable deliverable that may require several agent sessions and several slices.

It should:

1. read the current specs
2. determine whether the specs must change to accommodate the requested work
3. make any needed spec changes or explicitly record that none are required
4. inspect the relevant codebase and existing implementation boundaries
5. define the epic goal and why it matters
6. capture the current system shape and the proposed change shape
7. define definition of done, acceptance criteria, and manual verification
8. break the epic into an initial set of bounded slices

Epic planning should be highly interactive with the operator. It is where user intent gets translated into durable project direction and a concrete implementation strategy.

## `$fr-plan-slice`

Plan slice turns an epic into one bounded execution unit.

It should:

1. read the current specs
2. read the active epic
3. inspect only the code and context that materially constrain the next slice
4. define the next slice goal
5. define explicit in-scope and out-of-scope boundaries
6. define slice acceptance criteria
7. define the intended validation strategy
8. define the intended jj review shape

A slice should be good-commit-sized: one coherent vertical cut that is meaningful on its own, small enough for a single agent to hold in context, and still understandable in review without replaying the entire epic.

## `$fr-do`

Execution performs one bounded work slice.

It should:

1. read the runtime contract
2. read the active slice and parent epic
3. perform only the scoped work
4. update specs when behavior or workflow expectations change
5. update epic or slice planning state when the next intended action becomes clearer
6. run the required validation
7. append a timestamped run log entry directly to the slice file
8. leave the result in a reviewable jj state

Execution should prefer a coherent revision story over preserving every local iteration step.

`$fr-do` should own the end-of-run summary. A separate handoff step is unnecessary when the slice itself can carry both the durable scope definition and the execution history.

Execution helpers should stay local to the skill bundle that uses them. A work slice may update several artifacts, but the runtime implementation should still preserve skill-local script boundaries and stdlib-only execution.

During plugin development, those helpers may be generated from shared source files or templates before distribution. The generated result must still preserve the same skill-local runtime boundary seen by operators.

## `$fr-feedback`

Feedback turns operator comments or review findings into durable workflow state.

Feedback should be able to mutate the right artifact layer:

- specs
- epic
- slice
- queued follow-up work

The feedback step should make those transitions explicit. It should update the relevant durable artifacts rather than leaving decisions loose in chat.

## `$fr-review`

Review is usually epic-scoped.

It should compare epic intent against the implementation and summarize:

- what was completed
- which acceptance criteria are satisfied
- what validation ran
- what remains uncertain or incomplete
- what follow-up work should feed back into the epic or specs

Review is a source of feedback, not a separate terminal state. If review finds additional work, the epic remains open and the resulting changes should flow through the same feedback mechanism that operator comments use.

## Fluid Refinement

Forward Roll should optimize for easy refinement after agent work.

The normal case is:

1. run a bounded slice
2. inspect the result
3. refine it with targeted feedback
4. update the slice, epic, or specs as needed
5. continue with the next bounded slice

The workflow should feel conversational and iterative, not phase-gated.

## jj Review Model

Forward Roll should stay jj-native in language and intent.

The workflow should talk about:

- changes
- revisions
- stacks
- squashing
- splitting
- reviewable history

The operator should end up with a small number of readable revisions that tell a coherent story. Local agent iteration should be folded into that readable history before finalization whenever practical.

## Planning Model

Plans should support execution, not dominate the user experience.

The primary planning hierarchy is:

1. specs
2. epics
3. slices

Epics capture reviewable deliverables. Slices capture bounded execution units nested under an epic. The user-facing workflow should center on shaping and executing the next useful slice while still keeping the broader epic intent explicit and durable.

## Relationship To GSD

Forward Roll should borrow several useful ideas from Get Shit Done:

- explicit durable state
- bounded work units
- planning before execution
- verification as part of the loop
- feedback that updates durable state instead of living as loose chat

Forward Roll should diverge in a few deliberate ways:

- more fluid operator experience
- stronger jj-first posture
- lighter user-facing planning ceremony
- stronger emphasis on personal tooling and external artifact roots
- explicit support for epics that span several agent runs
