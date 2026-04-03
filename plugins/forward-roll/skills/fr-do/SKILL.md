---
name: "fr-do"
description: "Execute one bounded work slice with clear validation and jj review boundaries"
metadata:
  short-description: "Do one planned slice"
---

<objective>
Execute exactly one planned slice, keep the work bounded, run the required validation, append a timestamped log entry to the slice file, and leave the result in a reviewable `jj` state.
</objective>

<tooling>
Resolve the current context first:

```bash
python3 plugins/forward-roll/skills/fr-do/scripts/resolve_context.py --epic-id <epic-id> --slice-id <slice-id>
```

Append a run summary to a slice with:

```bash
python3 plugins/forward-roll/skills/fr-do/scripts/do.py --slice <slice-file> --summary "<what happened>"
```
</tooling>

<process>
1. Run `resolve_context.py` first to load the runtime, specs root, plans root, and the filtered epic or slice files that scope this execution.
2. Read the runtime contract, parent epic, and active slice before editing code.
3. Perform only the scoped work.
4. Update specs or plan artifacts when the work changes product or workflow expectations.
5. Run the smallest validation set that still gives strong evidence for the slice.
6. Append a timestamped execution entry directly under the slice `Log` heading, including validation and next-step notes when relevant.
7. Preserve a readable `jj` history by folding scratch iteration into the intended change with `jj squash` when practical.
</process>
