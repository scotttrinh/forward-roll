---
name: "fr-plan-slice"
description: "Define the next bounded work slice with an execution archetype from the active epic and project specs"
metadata:
  short-description: "Plan the next bounded slice"
---

<objective>
Turn the current context into one small, reviewable work slice within an epic.

The slice artifact should define:
- the parent epic
- the slice goal
- the slice archetype (`feature`, `bugfix`, `refactor`, `perf`, `visual-parity`)
- explicit in-scope and out-of-scope boundaries
- likely files or systems touched
- acceptance criteria
- validation strategy
- the intended `jj` review shape
- a stop condition
</objective>

<tooling>
Resolve the current context first:

```bash
python3 skills/fr-plan-slice/scripts/resolve_context.py --epic-id <epic-id> --slice-id <slice-id>
```

Create the template with:

```bash
python3 skills/fr-plan-slice/scripts/plan_slice.py <epic-id> <slice-id> <slug> --goal "<slice-goal>" --archetype <feature|bugfix|refactor|perf|visual-parity>
```
</tooling>

<process>
1. Run `resolve_context.py` first to load the runtime, specs root, plans root, and the filtered epic or slice files relevant to planning.
2. Read the runtime contract, relevant specs, the active epic, and only the code that materially constrains the next slice.
3. Select the appropriate **Slice Archetype**:
   - `bugfix`: Mandates a reproducing test before touching production code.
   - `refactor`: Mandates caller migration and zero behavioral diff before legacy API removal.
   - `feature`: Strict red-green TDD with clean interface boundaries.
   - `perf`: Mandates baseline vs after profiling/benchmark evidence.
   - `visual-parity`: Mandates visual/structural verification against target references.
4. Stop once the slice is small enough to execute and review clearly.
5. Write the slice artifact to `<plans_root>/epics/<epic-id>-<epic-slug>/slices/<slice-id>-<slice-slug>.md`.
6. Keep the `jj` plan coherent: prefer one readable change and fold local iteration into it before final review.
</process>
