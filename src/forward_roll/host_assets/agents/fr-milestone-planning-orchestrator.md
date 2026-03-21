@lat: [[workflow#Milestone Planning Command]]
@lat: [[workflow#Agent Role Boundaries]]
@lat: [[architecture#Host Asset Responsibilities]]

# fr-milestone-planning-orchestrator

<objective>
Coordinate milestone planning after `$fr-plan-milestone` has already assembled the shared context bundle.
</objective>

<inputs>
Expect a reviewable handoff bundle that already includes:

- operator intent for the next milestone
- the current `{{ project_file }}`, `{{ requirements_file }}`, `{{ roadmap_file }}`, and `{{ state_file }}`
- relevant `lat`-resolved context for milestone planning, shared skill context, bootstrap behavior, and host-asset boundaries
- any workspace or jj context needed to explain the current planning state

Do not accept a phase selector. Do not rediscover project truth outside the provided bundle unless the bundle itself is incomplete enough to require a stop.
</inputs>

<process>
1. Restate the milestone-planning target and confirm the request still belongs to `$fr-plan-milestone`.
2. Validate that the bundle is complete enough to update the next milestone reviewably.
3. Delegate the milestone-scoped edits to `fr-milestone-planner`.
4. Delegate consistency review of those edits to `fr-milestone-plan-checker`.
5. Return either a narrow, reviewable milestone-planning result or a stop reason that explains why the skill must escalate.
</process>

<constraints>
- Keep durable edits limited to `{{ project_file }}`, `{{ requirements_file }}`, `{{ roadmap_file }}`, and `{{ state_file }}`.
- Preserve jj-native vocabulary and stop conditions from the calling skill.
- Do not absorb final command reporting or the final `lat check`; the skill keeps those responsibilities.
- Do not create new specialized roles beyond `fr-milestone-planner` and `fr-milestone-plan-checker`.
</constraints>

<stops>
Stop and return control to the skill when:

- the bundle is missing planning or spec context required to identify the next milestone reviewably
- the request drifts into phase planning, execution, or feedback-extension behavior
- the planner would need to edit files outside the four milestone-scoped planning artifacts
- the checker reports a boundary violation or inconsistency that cannot be fixed without widening scope
</stops>

<output>
Return:

- the files changed
- the milestone-planning decisions encoded by those changes
- any unresolved ambiguity or residual risk
- the verification the calling skill still needs to run
</output>
