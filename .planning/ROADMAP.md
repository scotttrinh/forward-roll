# Roadmap: Forward Roll

## Overview

Forward Roll completed its first milestone by defining the domain, proving `lat.md` as the spec substrate, and implementing a narrow executable slice. The next milestone should make Forward Roll usable on itself through versioned Codex host assets that can be copied directly or refreshed idempotently by bootstrap so operators can scaffold a milestone, plan a phase, execute it, extend it with feedback, and resume execution.

## Phases

- [x] **Phase 1: Product Domain** - Define the operating values, core concepts, and milestone boundaries.
- [x] **Phase 2: Python Foundation** - Establish the strict Python package, CLI shell, and planning-root model.
- [x] **Phase 3: Knowledge Graph Bootstrap** - Prove `lat.md` as the project knowledge substrate.
- [x] **Phase 4: jj Review Workflow** - Model jj-native workflow semantics and review gates.
- [x] **Phase 5: First Executable Slice** - Implement the first self-hosting spec-to-plan-and-execute loop.
- [x] **Phase 6: Self-Hosting Skill-Pack Surface** - Define the copyable `fr-*` skill pack and milestone-local command model.
- [ ] **Phase 7: Milestone Planning Bootstrap** - Ship `$fr-plan-milestone` and bootstrap its templated host assets.
- [ ] **Phase 8: Minimal Self-Hosting Templates** - Fill the remaining `fr-*` skill and role templates with minimal initial coverage.
- [ ] **Phase 9: Self-Hosting Roundtrip Proof** - Verify the full self-hosting loop and bootstrap refresh story.

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
**Tasks**: 8 tasks
**Task Contracts**: [Phase 5 task contracts](./PHASE-05.md)

Tasks:
- [x] 05-01: Define the first executable self-hosting bootstrap contract with independent `specs_root` and `plans_root` inputs.
- [x] 05-02: Define the generic, cacheable workflow prompt-template model.
- [x] 05-03: Define the first full-phase execution launch contract.
- [x] 05-04: Define the continuous operator feedback loop for extending the active phase.
- [x] 05-05: Define the end-to-end verification and reviewer-facing documentation contract.
- [x] 05-06: Implement the executable bootstrap handoff, including resolved roots, durable bootstrap context, and planning-target persistence.
- [x] 05-07: Implement reusable prompt assets and the first serial phase-launch loop against the active phase contract.
- [x] 05-08: Implement feedback-path planning updates plus the end-to-end verification and reviewer documentation for the executable slice.

### Phase 6: Self-Hosting Skill-Pack Surface
**Goal**: Define the copyable Forward Roll skill pack, agent-role boundaries, and milestone-local command surface needed for skill-first self-hosting.
**Depends on**: Phase 5
**Requirements**: [SELF-01]
**Success Criteria** (what must be TRUE):
  1. Forward Roll has a concrete artifact layout for copyable skills and agent role descriptors.
  2. The skill pack has a stable user-facing command surface: `$fr-plan-milestone`, `$fr-plan-phase`, `$fr-execute-phase`, and `$fr-feedback-phase`.
  3. Milestone-local phase selectors are defined clearly enough that `phase 1` in the active milestone maps cleanly to durable global planning artifacts.
**Tasks**: 3 tasks
**Task Contracts**: [Phase 6 task contracts](./PHASE-06.md)

Tasks:
- [x] 06-01: Define the Forward Roll skill-pack layout and installation story for local Codex directories.
- [x] 06-02: Define the `fr-*` command surface and milestone-local phase selector semantics.
- [x] 06-03: Define the shared context contract for Forward Roll skills, agent roles, `lat.md`, and jj workflows.

### Phase 7: Milestone Planning Bootstrap
**Goal**: Ship `$fr-plan-milestone` and the templated bootstrap path for its host assets so the next milestone can be scaffolded through Forward Roll on itself.
**Depends on**: Phase 6
**Requirements**: [SELF-01, SELF-02]
**Success Criteria** (what must be TRUE):
  1. An operator can invoke `$fr-plan-milestone` and get updated milestone-scoped planning artifacts.
  2. The milestone-planning workflow updates `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md` consistently.
  3. Bootstrap can materialize or refresh the milestone-planning skill family from versioned templates without hidden host state.
  4. The templated milestone-planning assets use the same Codex-first, `lat.md`-grounded workflow model as the rest of the project, including indirect spec resolution through `lat`.
**Tasks**: 3 tasks
**Task Contracts**: [Phase 7 task contracts](./PHASE-07.md)

Tasks:
- [x] 07-01: Define and implement the `$fr-plan-milestone` skill contract.
- [x] 07-02: Define the milestone-planning orchestrator and supporting agent roles.
- [ ] 07-03: Add templated bootstrap support for the milestone-planning skill family and indirect `lat`-based spec resolution.

### Phase 8: Minimal Self-Hosting Templates
**Goal**: Fill the remaining `fr-*` skill and role templates with minimal but usable coverage so bootstrap can materialize a complete first-pass self-hosting pack.
**Depends on**: Phase 7
**Requirements**: [SELF-03, SELF-04, SELF-05]
**Success Criteria** (what must be TRUE):
  1. Bootstrap can materialize minimal templates for `$fr-plan-phase`, `$fr-execute-phase`, and `$fr-feedback-phase` plus their supporting roles.
  2. The templated skills resolve milestone-local phase selectors and indirect `lat` context consistently enough to be reviewed and iterated on in use.
  3. The resulting host asset pack stays minimal and reviewable instead of overcommitting to mature orchestration details too early.
**Tasks**: 3 tasks

Tasks:
- [ ] 08-01: Define the shared template contract and pack-materialization rules for the remaining `fr-*` skills and roles.
- [ ] 08-02: Add minimal `$fr-plan-phase` skill and role templates.
- [ ] 08-03: Add minimal `$fr-execute-phase` and `$fr-feedback-phase` skill and role templates plus pack-level verification.

### Phase 9: Self-Hosting Roundtrip Proof
**Goal**: Prove the templated self-hosting loop and document how bootstrap refreshes repo-local or user-local Codex assets.
**Depends on**: Phase 8
**Requirements**: [SELF-06, SELF-07, EXEC-01]
**Success Criteria** (what must be TRUE):
  1. A user can refresh the latest host assets, scaffold the next milestone, plan phase 1, execute phase 1, extend phase 1 with feedback, and resume execution through the same self-hosting pack.
  2. The bootstrap refresh path is idempotent and reviewable for repo-local self-hosting and user-local installation targets.
  3. The roundtrip keeps `lat.md`, planning artifacts, and jj-oriented workflow guidance aligned.
**Tasks**: 3 tasks

Tasks:
- [ ] 09-01: Verify the end-to-end self-hosting roundtrip across bootstrap refresh, planning, execution, feedback, and replay.
- [ ] 09-02: Document the templated bootstrap and installation layout for repo-local and user-local Codex asset directories.
- [ ] 09-03: Capture the operator checklist and validation criteria for refreshing and using the self-hosting pack.

## Progress

| Phase | Tasks Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Product Domain | 2/2 | Complete | 2026-03-16 |
| 2. Python Foundation | 3/3 | Complete | 2026-03-16 |
| 3. Knowledge Graph Bootstrap | 3/3 | Complete | 2026-03-17 |
| 4. jj Review Workflow | 3/3 | Complete | 2026-03-17 |
| 5. First Executable Slice | 8/8 | Complete | 2026-03-20 |
| 6. Self-Hosting Skill-Pack Surface | 3/3 | Complete | 2026-03-20 |
| 7. Milestone Planning Bootstrap | 2/3 | In Progress | - |
| 8. Minimal Self-Hosting Templates | 0/3 | Pending | - |
| 9. Self-Hosting Roundtrip Proof | 0/3 | Pending | - |
