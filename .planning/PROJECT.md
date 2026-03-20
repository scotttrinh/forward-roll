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
- [ ] Ship the next self-hosting milestone as copyable `fr-*` skills and agent roles for Codex before broadening standalone CLI coverage.
- [ ] Let operators scaffold milestones, plan phases, execute phases, and extend phases with feedback through the same Forward Roll skill pack.

### Out of Scope

- Full feature parity with get-shit-done in the first milestone — bootstrap needs a clean domain model before broad coverage.
- Git-first workflow compatibility — it would dilute jj-native design decisions during the foundation stage.
- Multi-provider agent support at bootstrap — Codex-first focus is the deliberate constraint.

## Context

- The starting point is the design space explored by get-shit-done, but the implementation and defaults are intentionally different.
- The first milestone should try `lat.md`, a markdown knowledge graph tool that stores project knowledge in `lat.md/` with wiki links, code backlinks, and `lat check` validation.
- The intended workflow is spec-first: define or evolve the aspirational system in `lat.md`, then let Forward Roll derive phased execution work from the gap between specs and current implementation.
- Specifications and plans may need different storage and governance. Forward Roll should therefore model `specs_root` and `plans_root` as independent locations rather than force one shared workspace root.
- The repo starts greenfield, so the domain model and artifact layout can be designed cleanly instead of inherited from existing code.
- The intended users care about software architecture, type design, and legible artifacts that can be reviewed by humans as well as consumed by agents.
- The next milestone should optimize for usable self-hosting inside Codex by shipping copyable skill and agent assets before chasing richer deterministic orchestration or CLI parity.

## Constraints

- **Tech stack**: Strictly typed modern Python — the tooling should not drift back toward TypeScript.
- **Architecture**: Prefer ports-and-adapters or equivalent production-grade architecture — shortcuts that collapse layers are out of bounds.
- **Version control**: jj-native workflow semantics — design should use jujutsu concepts directly.
- **Documentation**: Planning artifacts must be able to live separately from target repos — poly-repo and public-contribution workflows need this.
- **Process**: Review checkpoints between phases are mandatory — implementation cannot silently roll into the next phase.
- **Host integration**: Codex remains the execution host; Forward Roll should integrate with that host through skills and agent roles before it tries to replace host orchestration.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Codex-first is the primary agent model | The tool should be optimized for the environment it actually targets | — Pending |
| Python is the implementation language | Strict typing and modern Python tooling fit the desired architecture and maintenance posture | Implement with `attrs` and `cattrs`, use TOML at boundaries, and prefer `mypy` over `pyright` |
| jj is a first-class workflow primitive | Automatic change tracking should improve, not fight, agent workflows | Use `edit` for intent-based atomic WIP changes and `squash` to produce task commits that together form a reviewable phase deliverable |
| Milestones, phases, and tasks are distinct workflow units | The planning model should separate portfolio grouping, review boundaries, and execution assignments | Milestones group phases; phases define reviewable deliverables; tasks define single-agent execution scope |
| Task contracts should be intent-based rather than file-predicted | Planners often cannot know the final code layout up front, and executors need room to improve structure while staying in bounds | Use `Scope` and `Out of Scope` instead of hard file lists by default, and include durable references for executor context |
| `lat.md` is the first documentation substrate to validate | Human-legible graph documentation fits the project's reviewability goal | Implemented through linked architecture/domain/workflow sections, source backlinks, a repo-owned integrity test, and `lat check` |
| `lat.md` owns aspirational specs and planning responds to their gaps | Specification and execution planning overlap, but they should remain layered rather than collapsed into one system | Start by shaping intended behavior in `lat.md`, then derive phases, tasks, and execution from the gap between current implementation and the specs |
| Specs and plans need independent roots | Teams may want durable in-repo specs and ephemeral or external plans, so storage policy should differ by layer | Model `specs_root` and `plans_root` independently and let bootstrap accept separate locations for each |
| Bootstrap should persist resolved execution context before launch | Later prompt-template and execution tasks need a stable handoff artifact instead of re-deriving operator inputs from CLI state | Record resolved roots, defaults, and active planning targets durably in `plans_root`, but keep prompt assets and live execution outside bootstrap scope |
| The first self-hosting slice should use generic prompts and launch a real phase | Self-hosting requires more than writing planning artifacts; it needs a narrow but real execution loop | Use reusable, cacheable prompt-template assets with stable role IDs and named runtime context slots, keep those assets outside `plans_root`, launch a full phase, and let operator feedback append follow-up tasks inside the active phase |
| Operator feedback should extend phases through appended task contracts | Review feedback must stay forward-looking without inventing subphases or durable task-review states | Classify operator input as either follow-on task contracts appended with the next phase-local IDs or broader realignment that reshapes later planning |
| Phase 5 verification should prove both acceptance and feedback extension paths | The first executable slice is only reviewable if humans can validate both the straight-through story and the in-phase follow-up story | Define two high-value end-to-end verification stories, drive them through public slice boundaries, and pair them with reviewer docs that explain what artifacts to inspect |
| Planning roots must be externalizable | The workflow should work across poly-repos and public contribution contexts | Implemented through explicit repo-root versus planning-root types plus CLI and TOML adapter support |
| Self-hosting should land first as a Codex skill pack | The fastest route to using Forward Roll on itself is to package the workflow for the host environment rather than wait for CLI parity | The next milestone centers copyable `fr-*` skills plus agent-role descriptors, with Python helpers remaining optional support |
| Self-hosting phase commands should be milestone-local | Operators think in terms of the active milestone, so `$fr-plan-phase 1` should target the first phase of that milestone rather than the global roadmap ordinal | Skill commands accept milestone-local phase numbers and resolve them to durable global phase IDs in planning artifacts |
| Self-hosting assets should mirror Codex host layout | Copy/install only stays simple if the repo-owned assets already match the host boundary | Keep command skills under `.agents/skills/fr-*`, role descriptors under `.codex/agents/fr-*`, and support copying the same assets into user-local Codex directories without invoking the Python CLI |
| Skills should assemble an explicit shared context bundle before delegating | `lat.md`, planning artifacts, and jj rules must stay aligned across every `fr-*` command | Skills own operator input expansion, spec lookup, selector resolution, bundle assembly, and final `lat check`, then pass command intent, resolved phase context, relevant planning/spec inputs, and workspace context to specialized planning, execution, review, or planning-update roles |

---
*Last updated: 2026-03-20 after completing Phase 6 of the skill-first self-hosting milestone*
