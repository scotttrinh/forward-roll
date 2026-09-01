---
name: "fr-review"
description: "Compare epic and slice implementations against intent, verifying TDD coverage, anti-slop hygiene, and acceptance criteria"
metadata:
  short-description: "Review implementation against intent and anti-slop discipline"
---

<objective>
Create an epic-scoped or slice-scoped review summary that compares the intended deliverable against the current implementation.

The review validates:
- what the epic or slice intended
- what is implemented now
- which acceptance criteria are satisfied
- automated validation and TDD evidence
- **Anti-Slop & Comment Hygiene**: absence of narrative/trivial AI comments, defensive over-engineering, dead code, or redundant wrappers
- **Minimal Blast Radius**: tightly scoped diffs without gratuitous formatting or unrelated edits
- what remains uncertain or requires follow-up
</objective>

<tooling>
Resolve the current context first:

```bash
python3 skills/fr-review/scripts/resolve_context.py --epic-id <epic-id> --slice-id <slice-id>
```

Create the summary template with:

```bash
python3 skills/fr-review/scripts/review.py --epic <epic-file>
```
</tooling>

<process>
1. Run `resolve_context.py` first to load the runtime, specs root, plans root, and the filtered epic or slice files relevant to the review.
2. Read the runtime contract, relevant epic, nested slices, validation results, and diff summary.
3. Verify test coverage, acceptance criteria, comment hygiene, and anti-slop discipline.
4. Write the review summary under the parent epic directory.
5. Treat the review as an input to feedback rather than a separate terminal workflow state.
</process>
