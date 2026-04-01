# Context

This document defines the artifact model and context-shaping rules for Forward Roll.

## Context Philosophy

The main value of the workflow is not "more artifacts." It is better context.

Forward Roll should aggressively reduce low-signal input before execution work begins. The workflow should prefer a small amount of carefully curated context over a large amount of raw repository material.

## Artifact Classes

Forward Roll should operate on these main artifact classes:

- `specs`
- `epics`
- `slices`
- `feedback`
- `reviews`

Execution history is not a separate top-level artifact class. It should live inside the relevant slice as an append-only log.

## Specs

Specs capture durable project intent.

They describe:

- what the system is trying to become
- what workflow rules should remain true
- what product and engineering values should guide decisions
- high-level architecture and boundaries
- operator or user flows
- codebase standards and technical guidance

Specs are the longest-lived context layer.

## Epics

Epics capture reviewable deliverables that are too large for a single agent run but still have a clear definition of done.

A useful epic should include:

- a clear goal
- why the change matters
- whether specs must change
- the existing system shape
- the proposed change shape
- relevant code references
- constraints and risks
- definition of done
- acceptance criteria
- manual verification
- a slice breakdown

Epics are the main bridge between durable specs and bounded execution slices.

## Slices

Slices capture one bounded vertical cut of an epic.

A useful slice should include:

- the parent epic
- the slice goal
- explicit scope boundaries
- likely files or systems touched
- acceptance criteria
- validation requirements
- a stop condition
- an append-only execution log

Slices are the execution unit. They should be small enough for one agent session when things go well, but they must also preserve enough history to survive interruptions or follow-up runs when reality gets messier.

## Slice Logs

Every slice should carry its own operational memory in a `Log` section.

The log should record timestamped entries such as:

- planning updates
- execution attempts
- blockers
- decisions
- validation results
- end-of-run summaries

That log is the first place a follow-up agent should look when resuming work on the slice.

## Feedback

Feedback captures durable decisions made after operator inspection or automated review.

Feedback may affect:

- specs
- epic scope or acceptance
- slice scope or status
- queued follow-up work

Feedback should update the relevant durable artifacts rather than acting as an isolated comment stream.

## Reviews

Reviews compare intended behavior against implemented behavior, usually at epic scope.

A useful review should explain:

- what the epic intended
- what is implemented now
- which acceptance criteria are satisfied
- what validation exists
- what remains uncertain
- what follow-up work is implied

Review output should feed into feedback rather than stand apart as a disconnected report.

## Context Assembly

Each Forward Roll skill should assemble only the context it actually needs.

The default context inputs are:

1. runtime contract
2. relevant specs
3. relevant epic or slice artifacts
4. workspace facts needed for the command
5. operator input

The workflow should resist blindly loading every artifact just because it exists.

## Context Compression Rule

Raw exploration should not be handed directly to execution when a smaller high-signal artifact can be prepared first.

The point of specification and planning is to compress the input into a better execution context bundle.

## External And Private Artifact Roots

Specs and planning artifacts may live outside the repository or be gitignored.

Forward Roll should treat those locations as first-class runtime inputs. The context model should not assume that every useful artifact is committed to the target repository.

When planning artifacts live outside the repository, epic directories, nested slices, feedback, and review material should follow the same location.
