# Requirements: Forward Roll

**Defined:** 2026-03-16
**Core Value:** Deliver an agentic workflow that remains structurally rigorous, reviewable by humans, and faithful to the domain even as automation increases.

## v1 Requirements

### Core Workflow

- [ ] **CORE-01**: User can bootstrap a Forward Roll project around Codex-first assumptions rather than Claude Code assumptions.
- [ ] **CORE-02**: User can define workflow values that become part of the project model and planning artifacts.
- [ ] **CORE-03**: User can progress through phases with an explicit post-phase review and realignment step.

### Planning Model

- [x] **PLAN-01**: User can separate the planning root from the repository root in the domain model and command surface.
- [x] **PLAN-02**: User can initialize local planning artifacts that describe the project, requirements, roadmap, and current state.
- [ ] **PLAN-03**: User can preserve human-legible planning artifacts suitable for separate source control.

### Version Control

- [ ] **VCS-01**: User can work with jj-native workflow concepts instead of Git-shaped abstractions.
- [ ] **VCS-02**: User can find documented jj conventions for agents and reviewers.

### Knowledge Graph

- [x] **LAT-01**: User can maintain project knowledge in `lat.md/` as a graph of markdown documents.
- [x] **LAT-02**: User can connect source code back to knowledge graph sections through explicit references.
- [x] **LAT-03**: User can validate knowledge graph integrity with `lat check` once the tool is installed.

### Python Platform

- [x] **PY-01**: Developer can work in a modern Python package with strict static type checking enabled.
- [x] **PY-02**: Developer can invoke a Forward Roll CLI entry point from the package.
- [x] **PY-03**: Developer can extend the codebase through ports-and-adapters style boundaries.

### Quality Model

- [ ] **QUAL-01**: Developers have a documented testing philosophy favoring end-to-end happy paths, property-based invariants, and low-noise suites.
- [x] **QUAL-02**: Domain concepts are modeled as explicit typed structures before broad workflow implementation begins.

## v2 Requirements

### Execution

- **EXEC-01**: User can execute complete Forward Roll workflows against a target repository.
- **EXEC-02**: User can run agentic plans in parallel where independence permits.

### Poly-Repo Support

- **POLY-01**: User can manage a single planning workspace across multiple implementation repositories.
- **POLY-02**: User can publish or share selected planning artifacts independently from code changes.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full GSD command parity | The bootstrap should define a sound domain before cloning command count |
| Git-first compatibility layer | jj-native workflow language is a deliberate product differentiator |
| Broad agent-provider abstraction | Codex-first scope keeps the initial design coherent |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 | Phase 1 | Pending |
| CORE-02 | Phase 1 | Pending |
| QUAL-02 | Phase 1 | Complete |
| PLAN-01 | Phase 2 | Complete |
| PLAN-02 | Phase 2 | Complete |
| PY-01 | Phase 2 | Complete |
| PY-02 | Phase 2 | Complete |
| PY-03 | Phase 2 | Complete |
| LAT-01 | Phase 3 | Complete |
| LAT-02 | Phase 3 | Complete |
| LAT-03 | Phase 3 | Complete |
| VCS-01 | Phase 4 | Pending |
| VCS-02 | Phase 4 | Pending |
| CORE-03 | Phase 4 | Pending |
| PLAN-03 | Phase 5 | Pending |
| QUAL-01 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0

---
*Requirements defined: 2026-03-16*
*Last updated: 2026-03-17 after progress audit*
