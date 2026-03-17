# Forward Roll

Forward Roll is a Codex-first agentic workflow tool for software projects. It takes the core idea behind GSD-style planning and execution, then reorients it around jujutsu, strict Python tooling, explicit review checkpoints, and human-legible project knowledge.

## Current direction

The bootstrap in this repository focuses on four foundations:

- Codex-first workflows instead of Claude Code-first workflows
- jujutsu-native change management instead of Git-centric assumptions
- local planning artifacts that are designed to live outside the target repository when needed
- a typed Python implementation with `lat.md` as a first-class knowledge graph for agents and reviewers

The current bootstrap slice uses:

- `attrs` for frozen domain types
- `cattrs` for boundary structuring in adapters
- TOML as the configuration format for bootstrap inputs
- `typer` for a typed, agent-legible CLI surface
- `mypy`, `ruff`, `pytest`, and `hypothesis` as the intended quality toolchain

## Early status

This repository currently contains:

- a strict Python package scaffold in `src/forward_roll/`
- local planning artifacts under `.planning/`
- an initial `lat.md/` knowledge graph that documents the intended architecture and domain

## Bootstrap config direction

Forward Roll now treats TOML config loading as an adapter concern. The existing `bootstrap` command can still take direct paths, but it also accepts `--config path/to/forward-roll.toml` and structures that file into typed domain objects before the application layer renders output.

The default in this repo is `.planning/`, but end users should be able to point Forward Roll at any planning root through CLI or TOML configuration.

The first milestone is to validate `lat.md` as the documentation substrate while shaping the initial Forward Roll domain model and workflow boundaries.
