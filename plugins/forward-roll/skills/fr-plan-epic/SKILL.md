---
name: "fr-plan-epic"
description: "Define a reviewable epic, its spec impact, and its bounded slice breakdown"
metadata:
  short-description: "Plan one reviewable epic"
---

<objective>
Create or update one epic that is large enough to require multiple slices but still has a clear definition of done.

The epic artifact should define:
- the epic goal
- why it matters
- whether specs must change
- the current system shape
- the proposed change shape
- relevant code references
- definition of done
- acceptance criteria
- manual verification
- an initial slice breakdown
</objective>

<tooling>
Resolve the current context first:

```bash
python3 plugins/forward-roll/skills/fr-plan-epic/scripts/resolve_context.py --epic-id <epic-id>
```

Create the epic template with:

```bash
python3 plugins/forward-roll/skills/fr-plan-epic/scripts/plan_epic.py <epic-id> <slug> --goal "<epic-goal>"
```
</tooling>

<process>
1. Run `resolve_context.py` first to load the runtime, specs root, plans root, and the current epic directory when the epic identifier is already known.
2. Read the runtime contract and the relevant specs before planning.
3. Decide explicitly whether the requested change requires spec updates, is already covered by existing specs, or is implementation-only.
4. Inspect only the code and repository context needed to explain the current system shape and intended change.
5. Write the epic artifact to `<plans_root>/epics/<epic-id>-<epic-slug>/EPIC.md`.
6. Keep the epic detailed and decision-oriented, but avoid turning it into an unbounded analysis dump.
</process>
