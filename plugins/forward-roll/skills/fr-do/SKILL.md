---
name: "fr-do"
description: "Execute one planned slice by orchestrating fr-impl and fr-review subagents, gating the jj changeset on clean review"
metadata:
  short-description: "Orchestrate one slice via subagents"
---

<objective>
Execute exactly one planned slice by orchestrating two omp task subagents — fr-impl (TDD implementer) and fr-review (spec-compliance reviewer) — and materialize the result as a single reviewable jj change only after review returns clean. The main session is the orchestrator and does not write code itself.
</objective>

<tooling>
Resolve the current context first:

    python3 plugins/forward-roll/skills/fr-do/scripts/resolve_context.py --epic-id <epic-id> --slice-id <slice-id>

Append a run summary after the changeset materializes:

    python3 plugins/forward-roll/skills/fr-do/scripts/do.py --slice <slice-file> --summary "<what happened>"
</tooling>

<process>
1. Run resolve_context.py; read the runtime contract, parent epic, and the active slice before acting.
2. Verify the omp precondition: task.isolation.mode is none, so subagents share the working copy. If it is not none, fix .omp/config.yml and reload before continuing. Confirm fr-impl and fr-review are discoverable.
3. Name the intended review unit: jj describe the working-copy change with the slice's intent. Implementation work will accumulate in @; it is not yet a finalized changeset.
4. Dispatch a NON-ISOLATED fr-impl task (do not pass isolated:true). Pass the full slice contract: goal, in-scope/out-of-scope, TDD steps, acceptance criteria, and validation strategy. Its edits land in @. Await its structured result (files_changed, tests_written, validation_result, scope_adherence, deviations).
5. Dispatch a NON-ISOLATED fr-review task. It validates @ against the slice acceptance criteria + spec/epic intent + TDD coverage, returning verdict + findings.
6. Gate on the verdict:
   - ship → jj squash the @ work into the described change (the review unit). Append the slice run-log via do.py. Advance to the next slice.
   - revise → re-dispatch fr-impl with the specific findings (targeted fixes), then re-dispatch fr-review. Cap revision rounds at the slice's stop condition; on exhaustion, escalate to the operator rather than spinning.
7. You own ALL jj history surgery. Subagents never run jj. Fold local scratch iteration into the single described change before final review so the unit stays reviewable.
</process>

<notes>
- Slices execute sequentially: a non-isolated impl subagent edits @, so parallel impl subagents would clobber it. Use read-only scout subagents for any planning-time research instead.
- If fr-impl reports scope-creep-noted, decide explicitly whether to widen the slice (update the slice artifact) or trim the work before reviewing.
- The changeset must NOT appear in jj history as finalized until fr-review returns ship.
</notes>
