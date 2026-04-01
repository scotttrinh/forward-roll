# Workflow

This document defines Forward Roll's operator-facing workflow.

## Main Loop

Forward Roll should feel fluid to use while still enforcing high-signal context and clear review boundaries.

The main loop is:

1. `$fr-bootstrap`
2. `$fr-research`
3. `$fr-shape`
4. `$fr-do`
5. `$fr-review`
6. `$fr-feedback`

These commands are the product surface. Everything else exists to support them.

## `$fr-bootstrap`

Bootstrap establishes the operator's working contract for one project.

It should:

1. resolve `repo_root`
2. resolve or accept `specs_root`
3. resolve or accept `plans_root`
4. resolve or accept `research_root`
5. detect jj availability and basic workflow assumptions
6. record whether those roots are in-repo, out-of-repo, or gitignored
7. persist the runtime contract
8. summarize the resolved environment and stop

Bootstrap must not turn into a broad setup installer. Its job is to make the workflow usable here and now.

## `$fr-research`

Research creates the high-signal context bundle for a bounded slice of work.

It should:

1. inspect the relevant code and repository context
2. inspect the relevant spec and planning context
3. identify constraints, likely failure modes, and open questions
4. identify likely validation requirements
5. produce a compact research artifact for later shaping and execution

The purpose of research is aggressive context filtering. Raw exploration is not the final handoff artifact.

## `$fr-shape`

Shaping defines the next bounded work slice.

It should:

1. read the current specs
2. read the current plans
3. read the relevant research artifact
4. define the goal of the next work slice
5. define scope boundaries
6. define acceptance criteria
7. define the intended testing strategy
8. define the intended jj review shape

Shaping should stop once the slice is small enough to execute and review clearly.

## `$fr-do`

Execution performs one bounded work slice.

It should:

1. read the runtime contract
2. read the shaping artifact
3. read the relevant research artifact
4. perform only the scoped work
5. update specs when behavior or workflow expectations change
6. update planning state when the next intended action becomes clearer
7. run the required validation
8. leave the result in a reviewable jj state

Execution should prefer a coherent revision story over preserving every local iteration step.

## `$fr-review`

Review produces a concise handoff for human judgment.

It should summarize:

- what changed
- why it changed
- what validation ran
- what remains uncertain
- what kind of feedback is needed

The review step should make it easy for the operator to respond without first reconstructing the entire execution history.

## `$fr-feedback`

Feedback turns operator comments into durable workflow state.

Feedback should resolve into exactly one of these outcomes:

- `accept`
- `revise current slice`
- `queue follow-up`
- `reshape plan`

The plugin should make those transitions easy and explicit. Feedback should not force a heavy re-planning ceremony unless the feedback actually changes the scope or direction of the work.

## Fluid Refinement

Forward Roll should optimize for easy refinement after agent work.

The normal case is:

1. run a bounded slice
2. review it
3. refine it with targeted feedback
4. fold that refinement into the same work stream until it is ready

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

Forward Roll may still keep planning artifacts that describe larger goals, active work, and queued follow-ups, but the user-facing workflow should center on shaping and executing the next useful bounded slice rather than managing a heavy phase machine.

## Relationship To GSD

Forward Roll should borrow several useful ideas from Get Shit Done:

- explicit durable state
- bounded work units
- research before execution
- verification as part of the loop
- feedback that updates durable state instead of living as loose chat

Forward Roll should diverge in a few deliberate ways:

- more fluid operator experience
- stronger jj-first posture
- lighter user-facing planning ceremony
- stronger emphasis on personal tooling and external artifact roots
- explicit support for fast refinement after an agent run
