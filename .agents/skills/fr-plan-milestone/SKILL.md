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
Plan the next milestone by updating these planning artifacts:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

Treat `$fr-plan-milestone` as the milestone-planning entrypoint only.
Use `.codex/agents/fr-milestone-planning-orchestrator.md` for specialized milestone-planning work, let it coordinate `.codex/agents/fr-milestone-planner.md` and `.codex/agents/fr-milestone-plan-checker.md`, and keep command parsing, final reporting, and the final `lat check` in this skill.
</objective>

<execution_context>
Read before editing:

- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- relevant `lat.md` sections covering milestone planning, shared skill context, bootstrap behavior, and host-asset boundaries, resolved through `lat`
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
</execution_context>

<context>
Treat all user text after `$fr-plan-milestone` as milestone-planning intent, constraints, or requested scope.

Do not accept a phase selector or milestone-local phase number. If the operator supplies one, stop with a stable, reviewable error instead of guessing.
</context>

<process>
1. Expand the operator request with `lat expand`.
2. Resolve the relevant milestone-planning, shared-context, bootstrap, and host-asset guidance with `lat search` when available, or `lat locate` plus direct file reads when it is not.
3. Read the planning artifacts, the resolved `lat.md` guidance, and the supporting role descriptors before proposing edits.
4. Restate the milestone-planning target and keep it scoped to the next milestone.
5. Stop if the request includes a phase selector or drifts into phase planning, execution, or feedback-extension work.
6. Assemble the shared handoff bundle: operator intent, the milestone-scoped planning artifacts, the relevant `lat.md` context, and any workspace or jj context needed for reviewable milestone planning.
7. Hand specialized milestone-planning work to `.codex/agents/fr-milestone-planning-orchestrator.md` and expect it to coordinate `.codex/agents/fr-milestone-planner.md` and `.codex/agents/fr-milestone-plan-checker.md`.
8. Review the resulting edits and ensure they stay limited to `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md`.
9. Update `lat.md` if milestone-planning behavior or host-asset behavior changed.
10. Run the final `lat check`.
11. Report the concrete planning artifacts changed and the verification actually run.
</process>

<stops>
Stop and escalate instead of guessing when any of these apply:

- required planning artifacts or supporting role descriptors are missing or inconsistent
- the milestone objective is too vague to encode reviewably
- the request would redefine shared context, selector rules, or runtime conventions instead of planning the next milestone
- the request requires specialized milestone-planning behavior beyond `.codex/agents/fr-milestone-planning-orchestrator.md`, `.codex/agents/fr-milestone-planner.md`, and `.codex/agents/fr-milestone-plan-checker.md`
- the request actually belongs to `$fr-plan-phase`, `$fr-execute-phase`, or `$fr-feedback-phase`
</stops>
