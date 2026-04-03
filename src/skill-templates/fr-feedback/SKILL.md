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
Resolve the current context first:

```bash
python3 plugins/forward-roll/skills/fr-feedback/scripts/resolve_context.py --epic-id <epic-id> --slice-id <slice-id>
```

Record the decision with:

```bash
python3 plugins/forward-roll/skills/fr-feedback/scripts/feedback.py <epic-id> <slug> --scope <spec|epic|slice|follow-up> --outcome <accept|adjust-spec|adjust-epic|adjust-slice|queue-follow-up>
```
</tooling>

<process>
1. Run `resolve_context.py` first to load the runtime, specs root, plans root, and the filtered epic or slice files that frame the feedback.
2. Read the runtime contract plus the relevant epic, slice, and review context.
3. Choose exactly one allowed outcome.
4. Write the feedback artifact under the parent epic directory.
5. If the outcome implies spec, epic, or slice changes, update the affected artifact in the same pass instead of leaving the decision loose in chat.
</process>
