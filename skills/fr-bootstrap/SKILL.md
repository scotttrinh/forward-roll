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
- verify the agent harness environment (e.g. omp `task.isolation.mode: none`, codex agents, etc.)
- persist the runtime contract to `.forward-roll/runtime.json`
- summarize the result
</objective>

<tooling>
Run the bootstrap helper:

```bash
python3 skills/fr-bootstrap/scripts/bootstrap.py
```

Pass explicit overrides when the user provides them, for example:

```bash
python3 skills/fr-bootstrap/scripts/bootstrap.py --specs-root ../shared-specs
```
</tooling>

<process>
1. Treat user arguments or context as path overrides, layout constraints, or testing-posture notes.
2. Run the bootstrap helper first so the runtime contract exists before deeper work begins.
   If the helper reports harness preconditions are unmet (such as `task.isolation.mode` not being `none` on OMP), surface the printed guidance and address it before continuing.
3. Read the generated runtime contract at `.forward-roll/runtime.json` unless the user asked for another path.
4. Summarize the resolved environment clearly and stop unless the user explicitly asked to continue into specification or planning.
5. Do not turn bootstrap into an installer or a broad project audit.
</process>

## Platform Adaptation

If your harness appears here, read its reference file for specific tool mappings and execution details:

- Codex: `references/codex-tools.md`
- OMP: `references/omp-tools.md`
- Antigravity: `references/antigravity-tools.md`
- Claude Code: `references/claude-code-tools.md`
- Cursor: `references/cursor-tools.md`
