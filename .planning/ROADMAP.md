# Roadmap: Forward Roll

## Overview

Forward Roll starts by defining its own domain and aspirational specs clearly before it tries to automate much. The first milestone builds the specification and code skeleton needed to prove five things: the workflow can be Codex-first, `lat.md` can carry the aspirational specification layer, the planning model can be derived from those specs without being collapsed into them, specs and plans can live under different storage policies, and the implementation can stay strictly typed and reviewable.

## Phases

- [x] **Phase 1: Product Domain** - Define the operating values, core concepts, and milestone boundaries.
- [x] **Phase 2: Python Foundation** - Establish the strict Python package, CLI shell, and planning-root model.
- [x] **Phase 3: Knowledge Graph Bootstrap** - Prove `lat.md` as the project knowledge substrate.
- [x] **Phase 4: jj Review Workflow** - Model jj-native workflow semantics and review gates.
- [x] **Phase 5: First Executable Slice** - Implement the first self-hosting spec-to-plan-and-execute loop.

## Phase Details

### Phase 1: Product Domain
**Goal**: Capture the Forward Roll domain, values, and bootstrap scope in durable planning artifacts.
**Depends on**: Nothing (first phase)
**Requirements**: [CORE-01, CORE-02, QUAL-02]
**Success Criteria** (what must be TRUE):
  1. Forward Roll has a clear project definition, requirement set, and roadmap aligned with Codex-first goals.
  2. The product value system is documented as part of the domain, not as ad hoc prose.
  3. The first milestone boundary is clear enough to critique before deeper implementation starts.
**Tasks**: 2 tasks

Tasks:
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
**Tasks**: 3 tasks

Tasks:
- [x] 02-01: Configure packaging, typing, linting, and test tooling.
- [x] 02-02: Create the initial domain and application layers.
- [x] 02-03: Expose a CLI command surface for bootstrap-oriented flows.

### Phase 3: Knowledge Graph Bootstrap
**Goal**: Establish `lat.md` as the first-class knowledge graph for architecture, domain, and workflow context.
**Depends on**: Phase 2
**Requirements**: [LAT-01, LAT-02, LAT-03]
**Success Criteria** (what must be TRUE):
  1. The repo contains a readable `lat.md/` graph with linked sections covering architecture, domain, and workflow.
  2. Source files can point back to graph sections through explicit references.
  3. The roadmap includes validation of `lat check` once the dependency is installed.
**Tasks**: 3 tasks

Tasks:
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
**Tasks**: 3 tasks
**Task Contracts**: [Phase 4 task contracts](./PHASE-04.md)

Tasks:
- [x] 04-01: Define the jj-native workflow vocabulary for revisions, changes, stacks, review states, and the `edit`/`squash` execution loop.
- [x] 04-02: Specify the reviewer-facing loop for alignment, feedback, and post-phase decisions.
- [x] 04-03: Update planning artifacts so review gates and realignment outcomes are first-class state transitions.

### Phase 5: First Executable Slice
**Goal**: Implement the first self-hosting vertical slice that turns aspirational specs into plans, launches a phase, and supports operator-guided iteration.
**Depends on**: Phase 4
**Requirements**: [PLAN-03, QUAL-01]
**Success Criteria** (what must be TRUE):
  1. A user can start from linked aspirational specs and bootstrap a real self-hosting phase against a repository.
  2. The executable slice respects the documented spec-to-plan boundary, separate `specs_root` / `plans_root` handling, and generic prompt-template model.
  3. The user can iterate with operator feedback by appending follow-up work inside the active phase when appropriate.
  4. The executable path is backed by high-value tests and reviewer-facing documentation.
**Tasks**: 5 tasks
**Task Contracts**: [Phase 5 task contracts](./PHASE-05.md)

Tasks:
- [x] 05-01: Define the first executable self-hosting bootstrap contract with independent `specs_root` and `plans_root` inputs.
- [x] 05-02: Define the generic, cacheable workflow prompt-template model.
- [x] 05-03: Define the first full-phase execution launch contract.
- [x] 05-04: Define the continuous operator feedback loop for extending the active phase.
- [x] 05-05: Define the end-to-end verification and reviewer-facing documentation contract.

## Progress

| Phase | Tasks Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Product Domain | 2/2 | Complete | 2026-03-16 |
| 2. Python Foundation | 3/3 | Complete | 2026-03-16 |
| 3. Knowledge Graph Bootstrap | 3/3 | Complete | 2026-03-17 |
| 4. jj Review Workflow | 3/3 | Complete | 2026-03-17 |
| 5. First Executable Slice | 5/5 | Complete | 2026-03-19 |
