---
name: "fr-do"
description: "Execute one planned slice by orchestrating fr-impl and fr-review subagents, gating the jj changeset on clean review"
metadata:
  short-description: "Orchestrate one slice via subagents"
---

<objective>
Execute exactly one planned slice by orchestrating two task subagents — fr-impl (TDD implementer) and fr-review (spec-compliance reviewer) — and materialize the result as a single reviewable jj change only after review returns clean. The main session is the orchestrator and does not write code itself.
</objective>

<tooling>
Resolve the current context first:

    python3 skills/fr-do/scripts/resolve_context.py --epic-id <epic-id> --slice-id <slice-id>

Append a run summary after the changeset materializes:

    python3 skills/fr-do/scripts/do.py --slice <slice-file> --summary "<what happened>"
</tooling>

<process>
1. Run `resolve_context.py`; read the runtime contract, parent epic, and the active slice before acting.
2. Verify harness preconditions: subagents must share the working copy (e.g. OMP `task.isolation.mode: none`, Codex/Antigravity default working directory inheritance). Confirm `fr-impl` and `fr-review` roles are discoverable.
3. Name the intended review unit: `jj describe` the working-copy change with the slice's intent. Implementation work will accumulate in `@`; it is not yet a finalized changeset.
4. Dispatch a NON-ISOLATED `fr-impl` subagent. Pass the full slice contract (goal, archetype, in-scope/out-of-scope, acceptance criteria, validation strategy):
   - **Apply the Archetype Playbook**:
     - `bugfix`: Write reproduction test first; confirm failure, fix root cause, confirm pass.
     - `refactor`: Migrate callers then delete legacy APIs; verify zero behavioral diff.
     - `feature`: Red-green TDD with minimal interface boundaries.
     - `perf`: Measure baseline, implement optimization, prove before/after metrics.
     - `visual-parity`: Verify rendering/styling against reference.
   - Await structured result (files_changed, tests_written, validation_result, scope_adherence, deviations).
5. Dispatch a NON-ISOLATED `fr-review` subagent. It validates `@` against slice acceptance criteria, TDD coverage, anti-slop hygiene, and comment discipline, returning verdict + findings.
6. Gate on the verdict:
   - **ship** → `jj squash` the `@` work into the described change (the review unit). Append the slice run-log via `do.py`. Advance to the next slice.
   - **revise** → re-dispatch `fr-impl` with the specific findings (targeted fixes / anti-slop cleanups), then re-dispatch `fr-review`. Cap revision rounds at the slice's stop condition; on exhaustion, escalate to the operator rather than spinning.
7. You own ALL `jj` history surgery. Subagents never run `jj`. Fold local scratch iteration into the single described change before final review so the unit stays reviewable.
</process>

<notes>
- Slices execute sequentially: an impl subagent edits `@`, so parallel impl subagents would clobber it. Use read-only scout subagents for any planning-time research instead.
- If `fr-impl` reports scope creep, decide explicitly whether to widen the slice (update the slice artifact) or trim the work before reviewing.
- The changeset must NOT appear in `jj` history as finalized until `fr-review` returns ship.
- All code committed to `@` must adhere to anti-slop and comment hygiene rules.
</notes>
