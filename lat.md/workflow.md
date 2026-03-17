# Workflow

This document defines bootstrap flow, review boundaries, and jj-native workflow intent.

## Bootstrap Flow

Bootstrap should establish typed project context and an externalizable planning boundary.

The first Forward Roll workflow should establish:

1. a typed project identity
2. a planning root that may be external to the repository
3. a durable default value set
4. a knowledge graph that stays readable by humans and queryable by agents

At the adapter boundary, bootstrap inputs should be loadable from TOML so agents can produce stable, reviewable config artifacts instead of relying only on ad hoc CLI flags.

Related:

- [[architecture#Planning Storage]]
- [[domain#Planning Root]]

## Bootstrap Config Loading

Bootstrap config loading turns a TOML document into a typed directive at the adapter boundary.

This path should resolve relative paths from the config location, apply default values when the values table is omitted, and fail with stable errors when the document shape is invalid.

Code references:

- [[src/forward_roll/adapters/bootstrap_config.py]]
- [[tests/test_bootstrap_config.py]]

## Bootstrap Summary Rendering

Bootstrap summary rendering turns a typed directive into a concise, reviewable text artifact.

The current slice is intentionally small: it surfaces project identity, repository and planning roots, and one headline each for architecture and version-control posture.

Code references:

- [[src/forward_roll/application/bootstrap.py]]
- [[tests/test_bootstrap_config.py]]

## Bootstrap Command

The bootstrap command is the current agent-facing entry point for this repository slice.

It should accept direct CLI inputs or a TOML config file, preserve the repo-root versus planning-root distinction, and print the rendered summary without embedding domain logic in the command body.

Code references:

- [[src/forward_roll/cli.py]]

## Phase Review Loop

Every phase should have a hard boundary between implementation and review. That review is part of the spec lifecycle: it can validate the phase, trigger scope realignment, or update the project model before the next phase begins.

## lat.md Role

`lat.md` is the intended human-and-agent-readable knowledge substrate.

The first milestone should prove that Forward Roll can keep architecture, workflow intent, and source references coherent through `lat` documents rather than a single monolithic `AGENTS.md`.

## jujutsu Role

Forward Roll should exploit jj's automatic change tracking rather than papering over it with Git-shaped assumptions. That means the workflow model should talk about revisions, change stacks, and review states in jj-native language.
