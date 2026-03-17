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
- repository root
- specification root
- planning root
- default value set

The directive is a frozen domain object. It is not responsible for parsing TOML or validating raw config documents.

The current Python foundation models only the earlier bootstrap slice. The first executable self-hosting contract should widen that directive boundary to preserve independent `specs_root` and `plans_root` handling without moving adapter-boundary validation into the domain.

Code references:

- [[src/forward_roll/domain/model.py]]

## Project Identity

Project identity captures the stable repository name and root path used by a bootstrap run.

The identity object keeps the repository boundary explicit and enforces that the project name is non-empty before any workflow can proceed.

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

## Knowledge Graph Validation

Knowledge-graph validation should prove that important source files remain discoverable from `lat.md/`.

The highest-value checks in this phase should confirm that key sections exist, that they reference the current Python slice, and that source files still carry explicit backlinks into the graph.

Code references:

- [[tests/test_bootstrap_config.py]]
- [[tests/test_lat_knowledge_graph.py]]
