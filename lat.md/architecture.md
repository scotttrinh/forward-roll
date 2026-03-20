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
- [[src/forward_roll/application/prompts.py]]
- [[src/forward_roll/application/phase_launch.py]]
- [[src/forward_roll/adapters/bootstrap_config.py]]
- [[src/forward_roll/cli.py]]

## Domain Layer

The domain layer owns the typed bootstrap concepts and their invariants.

It defines the frozen types that express project identity, planning-root separation, and the default value set without coupling those concepts to TOML parsing or CLI concerns.

Code references:

- [[src/forward_roll/domain/model.py]]

## Application Layer

The application layer turns typed directives into stable workflow-facing outputs.

The executable bootstrap slice keeps application logic narrow: it accepts validated input, writes durable bootstrap artifacts, binds stable prompt assets to explicit runtime slots, runs the serial phase-launch loop, and applies operator-feedback planning updates through the same typed boundary.

Code references:

- [[src/forward_roll/application/bootstrap.py]]
- [[src/forward_roll/application/prompts.py]]
- [[src/forward_roll/application/phase_launch.py]]
- [[tests/test_phase_launch.py]]

## Adapter Layer

The adapter layer translates external documents and command inputs into typed application calls.

Bootstrap configuration loading belongs here because it resolves filesystem paths, parses TOML, derives the active planning target from durable planning docs, and concentrates runtime validation before handing a clean directive to the application layer.

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

Forward Roll should also treat the specification layer as a distinct root. Some teams may keep specifications in-repo while plans stay ephemeral or user-local, so the product should model `specs_root` and `plans_root` independently rather than forcing a single shared workspace root.

## Bootstrap Handoff Boundary

Bootstrap should persist only the durable context later workflow layers need.

The bootstrap boundary should write resolved roots, project identity, applied defaults, and the active planning target into `plans_root`. Prompt-template assets should remain reusable workflow assets, and live execution state should begin only when the later phase-launch layer consumes those durable planning outputs.

## Workflow Prompt Assets

Workflow prompt templates should be versioned product assets, not per-run planning outputs.

They should live with the Forward Roll implementation, carry stable role identities and output contracts, and accept runtime context through named slots bound from `specs_root`, `plans_root`, and operator or workspace state. This keeps cacheable instructions separate from project-specific planning data.

Code references:

- [[src/forward_roll/application/prompts.py]]

## Host Skill-Pack Boundary

Forward Roll should integrate with Codex first as a copyable skill pack.

The next milestone should package Forward Roll as reusable `SKILL.md` assets plus agent-role descriptors that can be copied into local Codex directories. The Python implementation may still supply helper logic, but Codex remains the execution host and primary runtime boundary for self-hosting.

Related:

- [[workflow#Skill-First Self-Hosting]]
- [[workflow#Workflow Prompt Templates]]

### Skill-Pack Artifact Layout

The self-hosting pack should mirror the host directories it targets.

The Phase 6 boundary should define:

1. repository-owned operator skills under `.agents/skills/fr-*`, one directory per user-facing command
2. copyable agent-role descriptors under `.codex/agents/fr-*`, with paired `.md` instructions and optional `.toml` runtime metadata when a role needs both
3. shared helper code or prompt assets outside those host directories when they are implementation details rather than installable host assets

The installation story should support both repo-local self-hosting and user-local copy/install flows. An operator should be able to use the repo-owned `.agents/skills/` plus `.codex/agents/` assets directly, or copy the same assets into user-local Codex directories such as `~/.codex/skills/` and `~/.codex/agents/`, without depending on the Python CLI to bootstrap the pack.

### Skill-Pack Installation Targets

Phase 6 should keep installation file-based and host-native.

Repo-local self-hosting should read the versioned assets in `.agents/skills/` and `.codex/agents/` directly from the repository. User-local installation should copy the same directories into `~/.codex/skills/` and `~/.codex/agents/` without rewriting the asset model or introducing generated host state.

### Whole-Pack and Per-Command Copy Rules

The copy/install contract should work for the full pack and for one command at a time.

Whole-pack installation should copy every `fr-*` skill directory plus the `fr-*` role descriptors they rely on. Per-command installation should copy one operator-facing skill directory with the `fr-*` role descriptors that command references. This boundary should stay explicit in the host assets themselves so the first self-hosting milestone does not depend on a hidden registry, generated manifest, or Python CLI installer.

### Host Asset Responsibilities

Skills, role descriptors, and Python helpers should have different jobs.

Operator-facing skills should own command entry, context loading, and final validation. Agent-role descriptors should own specialized planning, execution, review, or planning-update work. Python code may still provide helper logic for parsing, rendering, or validation, but Phase 6 should keep that helper layer optional so the copy/install story remains file-based and host-native.

## Knowledge and Planning Boundary

`lat.md` and planning artifacts should be integrated layers with different responsibilities, not duplicate systems.

`lat.md` owns the aspirational specification layer: linked concepts, intended behavior, rationale, and semantic context. Planning artifacts own the operational layer: current phases, task contracts, and the next forward changes needed to bring code and specs back into alignment.

Forward Roll should consume both layers together. It should read `specs_root` to understand what the system is meant to be, and read `plans_root` to understand what work is next.

## Type Posture

Strict typing is a design tool, not just a correctness tool. We model domain concepts explicitly and force ambiguity to the edges. Runtime validation should be concentrated at adapter boundaries.

The current foundation uses `attrs` for frozen domain structures and `cattrs` to structure TOML documents into those types at the adapter layer. The domain stays free of config parsing concerns.
