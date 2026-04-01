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
Create the summary template with:

```bash
python3 plugins/forward-roll/skills/fr-review/scripts/review.py --epic <epic-file>
```
</tooling>

<process>
1. Read the runtime contract, relevant epic, nested slices, validation results, and diff summary.
2. Write the review summary under the parent epic directory.
3. Treat the review as an input to feedback rather than a separate terminal workflow state.
</process>
