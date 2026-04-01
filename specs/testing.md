# Testing

This document defines Forward Roll's testing posture and TDD guidance.

## Testing Philosophy

Forward Roll should prefer high-signal validation over large amounts of shallow testing.

The goal is not to maximize test count. The goal is to choose the few tests that most clearly prove the important behavior and the most likely failure modes.

## Preferred Testing Mix

The default testing strategy should prioritize:

1. high-signal end-to-end tests for primary workflows
2. property-based tests for invariants and broad input spaces
3. targeted unit tests for edge cases and tricky logic

Forward Roll should avoid defaulting to large numbers of narrow example tests when broader or more meaningful tests would validate the behavior better.

## TDD Guidance

Forward Roll should encourage a pragmatic form of TDD.

That means:

- start by clarifying the desired behavior and acceptance criteria
- write or choose the most informative failing validation when that helps shape the work
- implement only enough to satisfy the bounded slice
- refine tests when they are low-signal or overfit to implementation details

TDD here is a tool for precision and feedback, not a ritual requirement for every edit.

## End-to-End Tests

End-to-end tests should carry most of the confidence for important workflows.

They should focus on:

- core user-visible paths
- key review boundaries
- critical state transitions
- behavior that would be expensive to reconstruct from lower-level tests alone

## Property-Based Tests

Property-based tests should be used when the important claim is an invariant rather than one example.

Typical good uses include:

- parser or serializer round-trips
- state machine invariants
- ordering and selection rules
- normalization and idempotence guarantees

## Unit Tests

Unit tests should be reserved for edge cases, narrow tricky logic, and failure handling that would be too awkward or too noisy to validate through end-to-end or property-based coverage.

They should not become the default answer to every change.

## Validation During Execution

Every shaped work slice should name the validation it expects to run.

The execution workflow should choose the smallest validation set that still gives strong evidence for the scoped change. Validation should be part of the bounded slice definition, not a generic afterthought.
