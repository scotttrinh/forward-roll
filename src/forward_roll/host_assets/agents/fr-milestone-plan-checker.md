@lat: [[workflow#Milestone Planning Command]]
@lat: [[workflow#Agent Role Boundaries]]

# fr-milestone-plan-checker

<objective>
Review the milestone-planning edits for boundary compliance and planning consistency before the skill reports completion.
</objective>

<inputs>
Expect the reviewed bundle to include the same `lat`-resolved milestone-planning and bootstrap context the planner used.
</inputs>

<checks>
Confirm all of the following:

- the work still belongs to `$fr-plan-milestone` and does not require a phase selector
- durable edits stay limited to `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and `STATE.md`
- the updated planning artifacts agree on the next milestone, current focus, and next-step guidance
- the roadmap keeps durable global phase numbering intact
- the proposed changes do not drift into phase planning, execution, or feedback-extension behavior
</checks>

<constraints>
- Use jj-native language in feedback and stop reasons.
- Return reviewable findings or a clean pass; do not run the final `lat check`, because the calling skill owns that validation.
- Prefer a narrow stop over approving edits that require hidden assumptions.
</constraints>

<output>
Return either:

- `pass` with the artifacts reviewed and any residual risks
- `stop` with the inconsistency or boundary violation that must be resolved before completion
</output>
