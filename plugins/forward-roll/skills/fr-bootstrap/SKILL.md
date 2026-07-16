---
name: "fr-bootstrap"
description: "Resolve the Forward Roll runtime contract for the current project"
metadata:
  short-description: "Bootstrap Forward Roll for one repository"
---

<objective>
Resolve the runtime contract for the current project and stop once the operator has a usable environment summary.

Bootstrap is intentionally narrow:
- resolve `repo_root`
- resolve or accept `specs_root`
- resolve or accept `plans_root`
- resolve the planning layout under `plans_root`
- detect whether `jj` is available
- verify the omp environment (`task.isolation.mode: none` effective; `fr-impl`/`fr-review` discoverable)
- persist the runtime contract
- summarize the result
</objective>

<tooling>
Run:

```bash
python3 plugins/forward-roll/skills/fr-bootstrap/scripts/bootstrap.py
```

Pass explicit overrides when the user provides them, for example:

```bash
python3 plugins/forward-roll/skills/fr-bootstrap/scripts/bootstrap.py --specs-root ../shared-specs
```
</tooling>

<process>
1. Treat the user text after the command as path overrides, layout constraints, or testing-posture notes.
2. Run the bootstrap helper first so the runtime contract exists before deeper work begins.
   If the helper reports `task.isolation.mode` is not `none`, surface the printed snippet (add it to `.omp/config.yml`, reload omp) and stop — non-isolated `fr-impl`/`fr-review` subagents require it.
3. Read the generated runtime contract at `.forward-roll/runtime.json` unless the user asked for another path.
4. Summarize the resolved environment clearly and stop unless the user explicitly asked to continue into specification or planning.
5. Do not turn bootstrap into an installer or a broad project audit.
</process>
