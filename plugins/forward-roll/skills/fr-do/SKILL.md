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
Append a run summary to a slice with:

```bash
python3 plugins/forward-roll/skills/fr-do/scripts/do.py --slice <slice-file> --summary "<what happened>"
```
</tooling>

<process>
1. Read the runtime contract, parent epic, and active slice before editing code.
2. Perform only the scoped work.
3. Update specs or plan artifacts when the work changes product or workflow expectations.
4. Run the smallest validation set that still gives strong evidence for the slice.
5. Append a timestamped execution entry directly under the slice `Log` heading, including validation and next-step notes when relevant.
6. Preserve a readable `jj` history by folding scratch iteration into the intended change with `jj squash` when practical.
</process>
