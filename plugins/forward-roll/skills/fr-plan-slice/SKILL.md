---
name: "fr-plan-slice"
description: "Define the next bounded work slice from the active epic and project specs"
metadata:
  short-description: "Plan the next bounded slice"
---

<objective>
Turn the current context into one small, reviewable work slice within an epic.

The slice artifact should define:
- the parent epic
- the slice goal
- explicit in-scope and out-of-scope boundaries
- likely files or systems touched
- acceptance criteria
- validation strategy
- the intended `jj` review shape
- a stop condition
</objective>

<tooling>
Create the template with:

```bash
python3 plugins/forward-roll/skills/fr-plan-slice/scripts/plan_slice.py <epic-id> <slice-id> <slug> --goal "<slice-goal>"
```
</tooling>

<process>
1. Read the runtime contract, relevant specs, the active epic, and only the code that materially constrains the next slice.
2. Stop once the slice is small enough to execute and review clearly.
3. Write the slice artifact to `<plans_root>/epics/<epic-id>-<epic-slug>/slices/<slice-id>-<slice-slug>.md`.
4. Keep the `jj` plan coherent: prefer one readable change and fold local iteration into it before final review.
</process>
