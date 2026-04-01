---
name: "fr-specify"
description: "Create or sharpen high-level project specs through discovery or description"
metadata:
  short-description: "Specify the project at a high level"
---

<objective>
Create or sharpen the durable high-level specs for the project.

Specify supports two modes:
- `discover` for reverse-engineering an existing codebase into durable high-level specs
- `describe` for turning a new idea or change direction into tight high-level specs

The output should focus on:
- architecture and boundaries
- technical guidance
- codebase standards
- user or operator flows
- key constraints and invariants

Stay above implementation detail. The result should help recreate the project or steer future changes without becoming code-level instructions for one local edit.
</objective>

<tooling>
If the runtime contract does not exist yet, run bootstrap first.

Create a specification work artifact with:

```bash
python3 plugins/forward-roll/skills/fr-specify/scripts/specify.py <slug> --mode <discover|describe> --goal "<specification goal>"
```
</tooling>

<process>
1. Read the runtime contract before gathering context.
2. Load only the specs, code, and repository facts that materially constrain the requested specification work.
3. Create or update the specification work artifact under `<specs_root>/specify/<slug>.md`.
4. Keep the artifact high-level and decision-oriented; do not dump raw exploration.
5. Update durable spec documents directly when the resulting project truth is clear enough.
</process>
