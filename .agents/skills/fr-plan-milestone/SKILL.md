---
name: fr-plan-milestone
description: Scaffold the next Forward Roll milestone by updating milestone-scoped planning artifacts
metadata:
  short-description: Scaffold the next Forward Roll milestone by updating milestone-scoped planning artifacts
---

@lat: [[workflow#Milestone Planning Command]]
@lat: [[workflow#Shared Skill Context]]

# fr-plan-milestone

<objective>
Use `$fr-plan-milestone` to scaffold the next milestone by updating the milestone-scoped planning artifacts:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

This skill owns the operator-facing contract only. Do not invent specialized milestone-planning roles here; Phase `07-02` owns that boundary.

Specialized milestone-planning work should now flow through `.codex/agents/fr-milestone-planning-orchestrator.md`, which coordinates `.codex/agents/fr-milestone-planner.md` and `.codex/agents/fr-milestone-plan-checker.md`.
</objective>

<inputs>
Treat all user text after `$fr-plan-milestone` as milestone-planning intent, constraints, or requested scope.

Do not accept a phase selector or milestone-local phase number. If the operator supplies one, stop with a stable, reviewable error instead of guessing.
</inputs>

<required_context>
Load the shared project truth before editing:

- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `lat.md/architecture.md`
- `lat.md/workflow.md`
- `.codex/agents/fr-milestone-planning-orchestrator.md`
- `.codex/agents/fr-milestone-planner.md`
- `.codex/agents/fr-milestone-plan-checker.md`
- the repo-local `lat` and `jj` skills when present

Use the repository `lat` workflow:

1. Run `lat expand` on the operator request.
2. Run `lat search` for relevant milestone-planning sections when semantic search is available.
3. If `lat search` is unavailable, fall back to `lat locate` and direct file reads.
4. Update `lat.md` when milestone-planning behavior or host-asset behavior changes.
5. Run `lat check` before finishing.

Use jj-native language throughout. Talk about changes, revisions, stacks, and reviewable planning state instead of Git-shaped terms.
</required_context>

<process>
1. Restate the milestone-planning target and keep it scoped to the next milestone.
2. Validate that the request does not include a phase selector and does not drift into phase planning, execution, or feedback-extension work.
3. Read the active planning artifacts and relevant `lat.md` sections before proposing edits.
4. Assemble the explicit shared handoff bundle: operator intent, the milestone-scoped planning artifacts, relevant `lat.md` context, and any workspace or jj context needed for reviewable milestone planning.
5. Hand specialized milestone-planning work to `.codex/agents/fr-milestone-planning-orchestrator.md`.
6. Expect the orchestrator to coordinate `.codex/agents/fr-milestone-planner.md` and `.codex/agents/fr-milestone-plan-checker.md`, and stop instead of guessing if their reviewable boundary fails.
7. Review the resulting edits to ensure they stay limited to `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`.
8. Run the final `lat check`, then report the concrete planning artifacts changed and the verification actually run.
</process>

<stops>
Stop and escalate instead of guessing when any of these apply:

- required planning artifacts are missing or inconsistent
- the milestone objective is too vague to encode reviewably
- the request would redefine shared context or selector semantics owned by earlier phases
- the request requires specialized milestone-planning roles that do not exist yet
- the request actually belongs to `$fr-plan-phase`, `$fr-execute-phase`, or `$fr-feedback-phase`
</stops>
