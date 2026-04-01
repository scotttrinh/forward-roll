---
name: "fr-feedback"
description: "Turn operator feedback into one explicit durable workflow outcome"
metadata:
  short-description: "Record feedback as durable state"
---

<objective>
Resolve operator or review feedback into one explicit durable outcome:

- `accept`
- `adjust-spec`
- `adjust-epic`
- `adjust-slice`
- `queue-follow-up`
</objective>

<tooling>
Record the decision with:

```bash
python3 plugins/forward-roll/skills/fr-feedback/scripts/feedback.py <epic-id> <slug> --scope <spec|epic|slice|follow-up> --outcome <accept|adjust-spec|adjust-epic|adjust-slice|queue-follow-up>
```
</tooling>

<process>
1. Read the runtime contract plus the relevant epic, slice, and review context.
2. Choose exactly one allowed outcome.
3. Write the feedback artifact under the parent epic directory.
4. If the outcome implies spec, epic, or slice changes, update the affected artifact in the same pass instead of leaving the decision loose in chat.
</process>
