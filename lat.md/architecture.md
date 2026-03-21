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

## Plugin Boundary

Forward Roll should integrate with Codex first as a static plugin.

The next milestone should package Forward Roll as one Codex plugin with a required `.codex-plugin/plugin.json`, bundled `fr-*` skills, and plugin-local helper scripts that resolve config and runtime context deterministically. The Python implementation in this repository may remain as a reference or migration aid, but the plugin should become the primary product and runtime boundary for self-hosting.

Related:

- [[workflow#Plugin-First Self-Hosting]]
- [[workflow#Workflow Prompt Templates]]

### Plugin Artifact Layout

The self-hosting package should mirror the Codex plugin layout it ships.

The plugin boundary should define:

1. one plugin root under `plugins/forward-roll/`
2. `.codex-plugin/plugin.json` as the required package manifest
3. bundled operator-facing skills under `skills/fr-*`, one directory per user-facing command
4. plugin-local scripts and prompt assets that skills can call to resolve config, locate planning or spec roots, and assemble runtime context without rewriting installed `SKILL.md` files

The installation story should support both repo-local and user-local marketplace flows. An operator should be able to point a repo marketplace at the versioned plugin folder during development or install the same plugin through a personal marketplace without depending on a generated CLI bootstrap step.

### Plugin Installation Targets

Phase 6 should keep installation plugin-based and host-native.

Repo-local self-hosting should expose the plugin through `.agents/plugins/marketplace.json` and a repo plugin directory such as `plugins/forward-roll/`. User-local installation should use a personal marketplace that points at a user-local plugin directory. The product should not require copying loose skill directories into host roots or rewriting plugin files after install.

Code references:

- [[src/forward_roll/application/bootstrap.py]]
- [[src/forward_roll/adapters/bootstrap_config.py]]

### Runtime Configuration Responsibilities

Skills, plugin-local scripts, and any retained Python helpers should have different jobs.

Operator-facing skills should own command entry, config loading, milestone-local selector resolution when needed, assembly of the shared planning/spec/workspace handoff bundle, and final validation. Plugin-local scripts should own deterministic config discovery, path resolution, and repeatable context assembly so installed skill text can stay static. Python code in this repository may still provide reference implementations or reusable logic, but the shipped plugin should not rely on post-install templating or mutation of bundled skills.

The plugin should therefore include one bootstrap skill that creates or refreshes the expected config file and explains the resolved runtime roots. After that, the other `fr-*` skills should read config and resolve context at runtime instead of depending on a separate bootstrap CLI command.

## Knowledge and Planning Boundary

`lat.md` and planning artifacts should be integrated layers with different responsibilities, not duplicate systems.

`lat.md` owns the aspirational specification layer: linked concepts, intended behavior, rationale, and semantic context. Planning artifacts own the operational layer: current phases, task contracts, and the next forward changes needed to bring code and specs back into alignment.

Forward Roll should consume both layers together. It should read `specs_root` to understand what the system is meant to be, and read `plans_root` to understand what work is next.

## Type Posture

Strict typing is a design tool, not just a correctness tool. We model domain concepts explicitly and force ambiguity to the edges. Runtime validation should be concentrated at adapter boundaries.

The current foundation uses `attrs` for frozen domain structures and `cattrs` to structure TOML documents into those types at the adapter layer. The domain stays free of config parsing concerns.
