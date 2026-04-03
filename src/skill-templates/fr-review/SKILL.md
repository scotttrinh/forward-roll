---
name: "fr-review"
description: "Compare epic intent against the current implementation and record findings"
metadata:
  short-description: "Review an epic against intent"
---

<objective>
Create an epic-scoped review summary that compares the intended deliverable against the current implementation.

The summary should cover:
- what the epic intended
- what is implemented now
- which acceptance criteria are satisfied
- what validation exists
- what remains uncertain
- what follow-up work should feed back into planning
</objective>

<tooling>
Resolve the current context first:

```bash
python3 plugins/forward-roll/skills/fr-review/scripts/resolve_context.py --epic-id <epic-id> --slice-id <slice-id>
```

Create the summary template with:

```bash
python3 plugins/forward-roll/skills/fr-review/scripts/review.py --epic <epic-file>
```
</tooling>

<process>
1. Run `resolve_context.py` first to load the runtime, specs root, plans root, and the filtered epic or slice files relevant to the review.
2. Read the runtime contract, relevant epic, nested slices, validation results, and diff summary.
3. Write the review summary under the parent epic directory.
4. Treat the review as an input to feedback rather than a separate terminal workflow state.
</process>
