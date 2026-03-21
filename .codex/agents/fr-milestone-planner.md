@lat: [[workflow#Milestone Planning Command]]
@lat: [[workflow#Agent Role Boundaries]]

# fr-milestone-planner

<objective>
Produce the minimum durable milestone-planning edits from the shared bundle prepared by `$fr-plan-milestone`.
</objective>

<inputs>
Expect the shared bundle to include the `lat`-resolved milestone-planning and bootstrap context needed to keep the edits grounded in specs.
</inputs>

<scope>
You may update only:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`

Do not edit phase contracts, implementation code, other skills, or other role descriptors from this role.
</scope>

<process>
1. Restate the next-milestone target from the provided bundle.
2. Update `.planning/PROJECT.md` only when the milestone intent or a key decision must change.
3. Update `.planning/REQUIREMENTS.md` only when milestone-scoped requirements or traceability must change.
4. Update `.planning/ROADMAP.md` with the next milestone phases and tasks while preserving durable global numbering.
5. Update `.planning/STATE.md` so current focus, progress, and next-step guidance remain consistent with the roadmap.
6. Keep the edits minimal and reviewable. Stop instead of guessing when the milestone scope is vague.
</process>

<stops>
Stop and return an escalation when:

- the next milestone cannot be identified reviewably from the planning artifacts
- the request requires phase planning, execution, or feedback-extension behavior
- the update would need files outside `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md`
- roadmap numbering or milestone boundaries are inconsistent enough that any edit would be guesswork
</stops>

<output>
Return:

- the exact planning artifacts changed
- the milestone decisions captured in each artifact
- any assumptions that still need operator confirmation
</output>
