# Forward Roll

## What This Is

Forward Roll is a Codex-first agentic workflow tool for software projects. It keeps the leverage of phase-based planning and execution, but reworks the system around jujutsu, strict Python types, externalizable planning roots, and reviewable knowledge graphs instead of Git-centric TypeScript tooling.

The product is for engineers who want agent-assisted delivery without giving up software craftsmanship, human review, or legible project memory.

## Core Value

Deliver an agentic workflow that remains structurally rigorous, reviewable by humans, and faithful to the domain even as automation increases.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Define a Codex-first workflow model instead of adapting Claude Code assumptions.
- [ ] Model planning artifacts so they can live outside the repository being changed.
- [ ] Build the tooling as a strictly typed Python application with explicit domain types.
- [ ] Encode the project's operating values as first-class workflow inputs.
- [ ] Make jujutsu-native change management part of the workflow model.
- [ ] Prove `lat.md` can serve as the initial human-and-agent-readable knowledge graph.
- [ ] Introduce explicit review and spec-realignment gates between implementation phases.

### Out of Scope

- Full feature parity with get-shit-done in the first milestone — bootstrap needs a clean domain model before broad coverage.
- Git-first workflow compatibility — it would dilute jj-native design decisions during the foundation stage.
- Multi-provider agent support at bootstrap — Codex-first focus is the deliberate constraint.

## Context

- The starting point is the design space explored by get-shit-done, but the implementation and defaults are intentionally different.
- The first milestone should try `lat.md`, a markdown knowledge graph tool that stores project knowledge in `lat.md/` with wiki links, code backlinks, and `lat check` validation.
- The repo starts greenfield, so the domain model and artifact layout can be designed cleanly instead of inherited from existing code.
- The intended users care about software architecture, type design, and legible artifacts that can be reviewed by humans as well as consumed by agents.

## Constraints

- **Tech stack**: Strictly typed modern Python — the tooling should not drift back toward TypeScript.
- **Architecture**: Prefer ports-and-adapters or equivalent production-grade architecture — shortcuts that collapse layers are out of bounds.
- **Version control**: jj-native workflow semantics — design should use jujutsu concepts directly.
- **Documentation**: Planning artifacts must be able to live separately from target repos — poly-repo and public-contribution workflows need this.
- **Process**: Review checkpoints between phases are mandatory — implementation cannot silently roll into the next phase.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Codex-first is the primary agent model | The tool should be optimized for the environment it actually targets | — Pending |
| Python is the implementation language | Strict typing and modern Python tooling fit the desired architecture and maintenance posture | Implement with `attrs` and `cattrs`, use TOML at boundaries, and prefer `mypy` over `pyright` |
| jj is a first-class workflow primitive | Automatic change tracking should improve, not fight, agent workflows | — Pending |
| `lat.md` is the first documentation substrate to validate | Human-legible graph documentation fits the project's reviewability goal | Implemented through linked architecture/domain/workflow sections, source backlinks, a repo-owned integrity test, and `lat check` |
| Planning roots must be externalizable | The workflow should work across poly-repos and public contribution contexts | Implemented through explicit repo-root versus planning-root types plus CLI and TOML adapter support |

---
*Last updated: 2026-03-17 after planning-doc audit*
