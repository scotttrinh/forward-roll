---
name: "fr-specify"
description: "Create or sharpen forward-facing living spec dossiers or fast-track bounded tasks directly from discovery"
metadata:
  short-description: "Specify living project dossiers or fast-track tasks"
---

<objective>
Capture ground truth, explore problem spaces, and frame durable direction for the project.

Specify supports three modes:
- `discover`: reverse-engineer existing systems into point-in-time ground truth research and direction dossiers
- `describe`: turn new product requirements or architectural ideas into forward-facing living domain dossiers
- `fast-track`: inline bounded work execution; when brainstorming reveals a small, bounded task (e.g. bugfix, helper, minor feature, follow-up), generate the epic and single slice upfront in one shot for immediate `fr-do` orchestration

For living dossiers (`discover`/`describe`), output focuses on:
- **Current State & Ground Truth**: active entry points, files, data flows, known landmines, and test posture
- **Functionality Under Discussion / Vector of Change**: problem statement, target behavior, and direction of travel
- **Durable Invariants & Design Decisions**: architectural boundaries, non-negotiable constraints, and technical rules
- **Open Findings & Questions**: point-in-time discoveries that steer future changes

Avoid static complete blueprints of imaginary future systems. Specs are living dossiers that anchor to real code today and point forward.
</objective>

<tooling>
If the runtime contract does not exist yet, run bootstrap first.

Resolve the current context first:

```bash
python3 skills/fr-specify/scripts/resolve_context.py
```

Create a living specification work artifact with:

```bash
python3 skills/fr-specify/scripts/specify.py <slug> --mode <discover|describe> --goal "<specification goal>"
```

Or fast-track a small, bounded task upfront with:

```bash
python3 skills/fr-specify/scripts/specify.py <slug> --mode fast-track --epic-id <epic-id> --goal "<task goal>" --archetype <bugfix|feature|refactor|perf|visual-parity> --acceptance "<criterion>"
```
</tooling>

<process>
1. Run `resolve_context.py` first to load the runtime, specs root, and plans root before deeper exploration.
2. Read the runtime contract before gathering context.
3. Explore the codebase, trace data flows, inspect tests, and talk with the operator.
4. **Determine the Track**:
   - **Living Spec Dossier (`discover`/`describe`)**: For broader features, new domains, or complex architectural areas, record the ground truth, vector of change, and invariants under `<specs_root>/specify/<slug>.md`. Update durable domain specs under `<specs_root>/<domain>.md` as truth settles.
   - **Inline Fast Track (`fast-track`)**: If the discussion confirms a small, bounded change (bugfix, quick helper, tight tweak, feedback follow-up), invoke `specify.py --mode fast-track`. This materializes the container epic and slice 01 upfront, ready for immediate dispatch via `fr-do`.
5. Keep the artifacts high-level and decision-oriented; do not dump raw unstructured terminal logs.
</process>
