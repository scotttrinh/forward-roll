# Context

This document defines the artifact model and context-shaping rules for Forward Roll.

## Context Philosophy

The main value of the workflow is not "more artifacts." It is better context.

Forward Roll should aggressively reduce low-signal input before shaping or execution work begins. The workflow should prefer a small amount of carefully curated context over a large amount of raw repository material.

## Artifact Classes

Forward Roll should operate on four main artifact classes:

- `specs`
- `plans`
- `research`
- `review summaries`

Each class serves a different purpose and should remain distinct.

## Specs

Specs capture durable product intent.

They describe:

- what the system is trying to become
- what workflow rules should remain true
- what product and engineering values should guide decisions

Specs are the longest-lived context layer.

## Plans

Plans capture current intended work.

They should answer questions such as:

- what are we doing next
- what is currently active
- what is queued
- what changed because of review feedback

Plans should be lightweight and editable. They are not meant to preserve a full execution transcript.

## Research

Research captures distilled context for one bounded slice of work.

A useful research artifact should include:

- the current relevant behavior
- the relevant architecture or file boundaries
- known constraints
- likely failure modes
- test implications
- unanswered questions

Research should be compact, execution-oriented, and disposable once it has served its purpose.

## Review Summaries

Review summaries capture the handoff back to human judgment.

A useful review summary should explain:

- what changed
- why
- what was validated
- what remains uncertain
- what follow-up shape is implied

## Context Assembly

Each Forward Roll skill should assemble only the context it actually needs.

The default context inputs are:

1. runtime contract
2. relevant specs
3. relevant plans
4. relevant research
5. workspace facts needed for the command
6. operator input

The workflow should resist blindly loading every artifact just because it exists.

## Context Compression Rule

Raw exploration should not be handed directly to execution when a smaller high-signal artifact can be prepared first.

The point of research and shaping is to compress the input into a better execution context bundle.

## External And Private Artifact Roots

Specs, plans, and research may live outside the repository or be gitignored.

Forward Roll should treat those locations as first-class runtime inputs. The context model should not assume that every useful artifact is committed to the target repository.
