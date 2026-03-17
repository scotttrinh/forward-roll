# Roadmap: Forward Roll

## Overview

Forward Roll starts by defining its own domain clearly before it tries to automate much. The first milestone builds the specification and code skeleton needed to prove three things: the workflow can be Codex-first, the planning model can be separated from the code repository, and `lat.md` can carry a readable knowledge graph alongside a strictly typed Python implementation.

## Phases

- [x] **Phase 1: Product Domain** - Define the operating values, core concepts, and milestone boundaries.
- [ ] **Phase 2: Python Foundation** - Establish the strict Python package, CLI shell, and planning-root model.
- [x] **Phase 3: Knowledge Graph Bootstrap** - Prove `lat.md` as the project knowledge substrate.
- [ ] **Phase 4: jj Review Workflow** - Model jj-native workflow semantics and review gates.
- [ ] **Phase 5: First Executable Slice** - Implement the first real bootstrap workflow end to end.

## Phase Details

### Phase 1: Product Domain
**Goal**: Capture the Forward Roll domain, values, and bootstrap scope in durable planning artifacts.
**Depends on**: Nothing (first phase)
**Requirements**: [CORE-01, CORE-02, QUAL-02]
**Success Criteria** (what must be TRUE):
  1. Forward Roll has a clear project definition, requirement set, and roadmap aligned with Codex-first goals.
  2. The product value system is documented as part of the domain, not as ad hoc prose.
  3. The first milestone boundary is clear enough to critique before deeper implementation starts.
**Plans**: 2 plans

Plans:
- [x] 01-01: Define project context, requirements, and phase structure.
- [x] 01-02: Capture initial domain concepts in the knowledge graph.

### Phase 2: Python Foundation
**Goal**: Create the typed Python scaffold and model the separation between repository root and planning root.
**Depends on**: Phase 1
**Requirements**: [PLAN-01, PLAN-02, PY-01, PY-02, PY-03]
**Success Criteria** (what must be TRUE):
  1. The repository contains a strict Python package and CLI entry point.
  2. The code models planning-root separation as an explicit domain concern.
  3. The package layout leaves room for ports-and-adapters style growth.
**Plans**: 3 plans

Plans:
- [ ] 02-01: Configure packaging, typing, linting, and test tooling.
- [ ] 02-02: Create the initial domain and application layers.
- [ ] 02-03: Expose a CLI command surface for bootstrap-oriented flows.

### Phase 3: Knowledge Graph Bootstrap
**Goal**: Establish `lat.md` as the first-class knowledge graph for architecture, domain, and workflow context.
**Depends on**: Phase 2
**Requirements**: [LAT-01, LAT-02, LAT-03]
**Success Criteria** (what must be TRUE):
  1. The repo contains a readable `lat.md/` graph with linked sections covering architecture, domain, and workflow.
  2. Source files can point back to graph sections through explicit references.
  3. The roadmap includes validation of `lat check` once the dependency is installed.
**Plans**: 3 plans

Plans:
- [x] 03-01: Define the initial knowledge graph structure and linked sections.
- [x] 03-02: Add source-to-graph references in Python modules.
- [x] 03-03: Validate the graph with `lat check` when the toolchain is available.

### Phase 4: jj Review Workflow
**Goal**: Define jj-native review and spec realignment semantics for phase execution.
**Depends on**: Phase 3
**Requirements**: [VCS-01, VCS-02, CORE-03]
**Success Criteria** (what must be TRUE):
  1. The workflow model uses jj-native concepts instead of Git-shaped language.
  2. A mandatory review/alignment step exists between implementation phases.
  3. jj conventions for agents and reviewers are documented in durable project artifacts.
**Plans**: 3 plans

Plans:
- [ ] 04-01: Model review-state and change-state concepts for jj-native workflows.
- [ ] 04-02: Write reviewer-facing jj workflow guidance.
- [ ] 04-03: Update planning artifacts to embed review gates explicitly.

### Phase 5: First Executable Slice
**Goal**: Implement an end-to-end bootstrap flow that turns typed input into initial project artifacts.
**Depends on**: Phase 4
**Requirements**: [PLAN-03, QUAL-01]
**Success Criteria** (what must be TRUE):
  1. A user can run a Forward Roll bootstrap command against a repository.
  2. The resulting artifacts reflect the documented values and planning-root model.
  3. The executable path is backed by high-value tests and reviewable documentation.
**Plans**: 3 plans

Plans:
- [ ] 05-01: Define the bootstrap use-case contract and output model.
- [ ] 05-02: Implement the initial artifact writer path.
- [ ] 05-03: Add high-value tests and reviewer-facing documentation.

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Product Domain | 2/2 | Complete | 2026-03-16 |
| 2. Python Foundation | 0/3 | In progress | - |
| 3. Knowledge Graph Bootstrap | 3/3 | Complete | 2026-03-17 |
| 4. jj Review Workflow | 0/3 | Not started | - |
| 5. First Executable Slice | 0/3 | Not started | - |
