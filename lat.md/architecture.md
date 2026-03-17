# Architecture

This document defines Forward Roll's layers, storage boundaries, and type posture.

## System Shape

Forward Roll uses a typed Python core with explicit workflow boundaries.

The system should prefer ports-and-adapters style seams so the domain can evolve independently of CLI plumbing, jujutsu integration, and documentation backends.

Related:

- [[domain#Core Domain]]
- [[workflow#Bootstrap Flow]]
- [[workflow#Phase Review Loop]]

## Primary Layers

1. Domain: policies, types, workflow concepts, and invariants.
2. Application: use-cases that compose domain concepts into commands and workflows.
3. Adapters: CLI, jujutsu integration, filesystem/planning-root access, and external tool execution.

Code references:

- [[src/forward_roll/domain/model.py]]
- [[src/forward_roll/application/bootstrap.py]]
- [[src/forward_roll/adapters/bootstrap_config.py]]
- [[src/forward_roll/cli.py]]

## Domain Layer

The domain layer owns the typed bootstrap concepts and their invariants.

It defines the frozen types that express project identity, planning-root separation, and the default value set without coupling those concepts to TOML parsing or CLI concerns.

Code references:

- [[src/forward_roll/domain/model.py]]

## Application Layer

The application layer turns typed directives into stable workflow-facing outputs.

The current slice keeps application logic narrow: it accepts a validated `BootstrapDirective` and renders a concise summary without re-validating adapter input.

Code references:

- [[src/forward_roll/application/bootstrap.py]]

## Adapter Layer

The adapter layer translates external documents and command inputs into typed application calls.

Bootstrap configuration loading belongs here because it resolves filesystem paths, parses TOML, and concentrates runtime validation before handing a clean directive to the application layer.

Code references:

- [[src/forward_roll/adapters/bootstrap_config.py]]

## CLI Adapter

The CLI is an adapter that exposes the current bootstrap slice without leaking transport concerns inward.

It owns option parsing, exit behavior, and config-file error presentation while delegating typed work to the application and adapter modules.

Code references:

- [[src/forward_roll/cli.py]]

## Planning Storage

Planning storage is a first-class product boundary, not an implementation detail.

Planning artifacts are part of the product model, but they should not be coupled to the target repository. Forward Roll should support a planning root that can live outside the code repository so that poly-repo work, public contributions, and private planning can all share the same workflow model.

This repository uses `.planning/` as its local default, but that default should remain an adapter concern rather than a domain constraint.

## Type Posture

Strict typing is a design tool, not just a correctness tool. We model domain concepts explicitly and force ambiguity to the edges. Runtime validation should be concentrated at adapter boundaries.

The current foundation uses `attrs` for frozen domain structures and `cattrs` to structure TOML documents into those types at the adapter layer. The domain stays free of config parsing concerns.
