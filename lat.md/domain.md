# Domain

This document defines the core bootstrap concepts and testing posture.

## Core Domain

Forward Roll manages the lifecycle of a project through typed planning artifacts, executable phases, explicit review checkpoints, and version-control-aware change management.

Related:

- [[architecture#System Shape]]
- [[workflow#Bootstrap Flow]]

## Bootstrap Directive

A typed expression of what a repository bootstrap needs:

- project identity
- planning root
- default value set

The directive is a frozen domain object. It is not responsible for parsing TOML or validating raw config documents.

Code references:

- [[src/forward_roll/domain/model.py]]

## Value Set

The default value set captures the behavioral posture of the tool. It is not presentation copy; it is a first-class input into planning, review, and execution decisions.

Code references:

- [[src/forward_roll/domain/model.py]]

## Planning Root

The planning root is distinct from the repository root. That distinction is intentional and should remain explicit throughout the domain model.

Boundary adapters may resolve paths from TOML or CLI inputs, but the domain model should always receive concrete `Path` values that preserve the repo-root and planning-root distinction.

## Testing Philosophy

Tests should document intent, enforce domain invariants, and validate end-to-end flows. Prefer a few high-value tests that prove the model over dense suites of mocked implementation-detail tests.

For the Python foundation, the first high-value test should prefer the bootstrap happy path: TOML document to typed directive to rendered summary.
