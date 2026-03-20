"""Focused tests for prompt assets and serial phase launch."""
# @lat: [[domain#Testing Philosophy]]
# @lat: [[workflow#Workflow Prompt Templates]]
# @lat: [[workflow#Phase Launch Contract]]
# @lat: [[workflow#Continuous Operator Feedback]]
# @lat: [[workflow#End-to-End Verification]]

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forward_roll.adapters.bootstrap_config import resolve_bootstrap_directive
from forward_roll.application.bootstrap import bootstrap_project
from forward_roll.application.phase_launch import (
    ExecutionRunner,
    FollowOnTaskUpdate,
    PhaseLaunchError,
    PhaseReviewResult,
    PhaseTaskContract,
    PlanningUpdateResult,
    TaskExecutionResult,
    apply_operator_feedback,
    launch_phase,
)
from forward_roll.application.prompts import (
    BoundPrompt,
    ContextDocument,
    PromptRuntimeEnvelope,
    WorkspaceContext,
    bind_prompt_template,
    load_workflow_prompt_assets,
    render_context_documents,
)


def test_load_workflow_prompt_assets_exposes_stable_roles() -> None:
    templates = load_workflow_prompt_assets()

    assert set(templates) == {"planning_update", "task_execution", "phase_review"}
    assert templates["task_execution"].version == "v1"
    assert templates["task_execution"].required_slots == (
        "bootstrap_context",
        "active_task_contract",
        "spec_context",
        "planning_context",
        "workspace_context",
    )


def test_bind_prompt_template_uses_stable_slot_order(tmp_path: Path) -> None:
    templates = load_workflow_prompt_assets()
    envelope = PromptRuntimeEnvelope(
        bootstrap_context=ContextDocument(
            label="bootstrap_context",
            path=tmp_path / "bootstrap-context.json",
            content='{"active_target":{"task_id":"05-07"}}\n',
        ),
        spec_context=(
            ContextDocument(
                label="workflow_spec",
                path=tmp_path / "workflow.md",
                content="# Workflow\n",
            ),
        ),
        planning_context=(
            ContextDocument(
                label="roadmap_plan",
                path=tmp_path / "ROADMAP.md",
                content="# Roadmap\n",
            ),
        ),
    )

    bound = bind_prompt_template(
        templates["phase_review"],
        slot_values={
            "bootstrap_context": envelope.bootstrap_context.content.rstrip(),
            "spec_context": render_context_documents(envelope.spec_context),
            "planning_context": render_context_documents(envelope.planning_context),
            "review_target": "phase_id=05",
            "operator_input": "(none)",
        },
    )

    assert [binding.slot_name for binding in bound.slot_bindings] == list(
        templates["phase_review"].required_slots
    )
    assert bound.slot_bindings[1].content.startswith("[workflow_spec]")


def test_end_to_end_bootstrap_launch_and_acceptance(tmp_path: Path) -> None:
    repo_root = _write_bootstrap_source_fixture(tmp_path / "repo")
    specs_root = _write_external_specs_fixture(tmp_path / "specs")
    plans_root = tmp_path / "plans"
    directive = resolve_bootstrap_directive(
        repo_root=repo_root,
        specs_root=specs_root,
        plans_root=plans_root,
        project_name="Forward Roll E2E",
    )

    artifacts = bootstrap_project(directive)
    runner = RecordingRunner(
        task_results={
            "05-07": TaskExecutionResult(
                status="completed",
                summary="implemented prompt assets",
                verification=("uv run pytest tests/test_phase_launch.py",),
                review_ready=True,
                revision_ref="abc123",
            ),
            "05-08": TaskExecutionResult(
                status="completed",
                summary="implemented feedback path",
                verification=("uv run pytest tests/test_phase_launch.py",),
                review_ready=True,
                revision_ref="def456",
            ),
        },
        review_result=PhaseReviewResult(outcome="accepted", summary="phase accepted"),
    )

    result = launch_phase(
        plans_root=plans_root,
        runner=runner,
        workspace_context=_workspace_context(repo_root),
    )

    assert artifacts.context_path == plans_root / "bootstrap-context.json"
    assert artifacts.summary_path == plans_root / "BOOTSTRAP.md"
    assert result.completed_tasks == ("05-07", "05-08")
    assert result.review_result is not None
    assert result.review_result.outcome == "accepted"
    assert [task_id for task_id, _ in runner.seen_tasks] == ["05-07", "05-08"]

    roadmap_text = (plans_root / "ROADMAP.md").read_text(encoding="utf-8")
    assert "- [x] 05-07: Implement reusable prompt assets and serial launch." in roadmap_text
    assert "- [x] 05-08: Add feedback-path verification." in roadmap_text
    assert "05-09" not in roadmap_text

    state_text = (plans_root / "STATE.md").read_text(encoding="utf-8")
    assert "Status: Review outcome `accepted`" in state_text


def test_end_to_end_feedback_path_appends_follow_on_task(tmp_path: Path) -> None:
    repo_root = _write_bootstrap_source_fixture(tmp_path / "repo")
    specs_root = _write_external_specs_fixture(tmp_path / "specs")
    plans_root = tmp_path / "plans"
    directive = resolve_bootstrap_directive(
        repo_root=repo_root,
        specs_root=specs_root,
        plans_root=plans_root,
        project_name="Forward Roll E2E",
    )
    bootstrap_project(directive)

    runner = RecordingRunner(
        task_results={
            "05-07": TaskExecutionResult(
                status="completed",
                summary="implemented prompt assets",
                verification=("uv run pytest tests/test_phase_launch.py",),
                review_ready=True,
                revision_ref="abc123",
            ),
            "05-08": TaskExecutionResult(
                status="completed",
                summary="implemented feedback path",
                verification=("uv run pytest tests/test_phase_launch.py",),
                review_ready=True,
                revision_ref="def456",
            ),
        },
        review_result=PhaseReviewResult(
            outcome="extend_phase",
            summary="review found one more in-phase documentation gap",
        ),
        planning_result=PlanningUpdateResult(
            outcome="append_tasks",
            summary="append one reviewer-doc follow-up task",
            follow_on_tasks=(
                FollowOnTaskUpdate(
                    title="Capture reviewer verification checklist",
                    contract_body="\n".join(
                        [
                            "**Objective**",
                            "Append the missing reviewer verification checklist for the phase 5 slice.",
                            "",
                            "**Scope**",
                            "- Update the reviewer-facing documentation for the executable slice.",
                            "",
                            "**Out of Scope**",
                            "- Broader roadmap replanning outside phase 5.",
                            "",
                            "**References**",
                            "- `lat.md/workflow.md`",
                            "- `.planning/ROADMAP.md`",
                            "- `.planning/STATE.md`",
                            "",
                            "**Automated Verification**",
                            "- Run `uv run pytest tests/test_phase_launch.py`.",
                            "",
                            "**Manual Verification**",
                            "- Confirm the reviewer checklist names the happy-path and feedback-path artifacts.",
                            "",
                            "**Definition of Done**",
                            "- The reviewer checklist is durable and points at the appended task path.",
                        ]
                    ),
                ),
            ),
        ),
    )

    launch_result = launch_phase(
        plans_root=plans_root,
        runner=runner,
        workspace_context=_workspace_context(repo_root),
    )
    assert launch_result.review_result is not None

    feedback_result = apply_operator_feedback(
        plans_root=plans_root,
        runner=runner,
        review_result=launch_result.review_result,
        operator_input="Please add the missing reviewer verification checklist.",
    )

    assert feedback_result.outcome == "append_tasks"
    assert feedback_result.appended_task_ids == ("05-09",)
    assert "review_outcome=extend_phase" in runner.seen_planning_updates[0]
    assert "Please add the missing reviewer verification checklist." in runner.seen_planning_updates[0]

    roadmap_text = (plans_root / "ROADMAP.md").read_text(encoding="utf-8")
    assert "**Tasks**: 3 tasks" in roadmap_text
    assert "- [x] 05-07: Implement reusable prompt assets and serial launch." in roadmap_text
    assert "- [x] 05-08: Add feedback-path verification." in roadmap_text
    assert "- [-] 05-09: Capture reviewer verification checklist" in roadmap_text

    state_text = (plans_root / "STATE.md").read_text(encoding="utf-8")
    assert "**Current focus:** Phase 05 - First Executable Slice (next task `05-09`)" in state_text
    assert "Task: 05-09 of 3 in current phase" in state_text
    assert "Status: Ready to execute" in state_text

    phase_text = (plans_root / "PHASE-05.md").read_text(encoding="utf-8")
    assert "### Task 05-09: Capture reviewer verification checklist" in phase_text
    assert "- `lat.md/workflow.md`" in phase_text

    context = json.loads((plans_root / "bootstrap-context.json").read_text(encoding="utf-8"))
    assert context["active_target"]["task_id"] == "05-08"


def test_launch_phase_executes_tasks_serially_and_updates_planning(tmp_path: Path) -> None:
    plans_root = _write_launch_fixture(tmp_path)
    runner = RecordingRunner(
        task_results={
            "05-07": TaskExecutionResult(
                status="completed",
                summary="implemented prompt assets",
                verification=("uv run pytest tests/test_phase_launch.py",),
                review_ready=True,
                revision_ref="abc123",
            ),
            "05-08": TaskExecutionResult(
                status="completed",
                summary="completed review docs",
                verification=("uv run pytest tests/test_phase_launch.py",),
                review_ready=True,
                revision_ref="def456",
            ),
        },
        review_result=PhaseReviewResult(
            outcome="accepted",
            summary="phase accepted",
        ),
    )

    result = launch_phase(
        plans_root=plans_root,
        runner=runner,
        workspace_context=_workspace_context(plans_root.parent / "repo"),
    )

    assert result.completed_tasks == ("05-07", "05-08")
    assert result.review_result is not None
    assert result.review_result.outcome == "accepted"
    assert [task_id for task_id, _ in runner.seen_tasks] == ["05-07", "05-08"]

    roadmap_text = (plans_root / "ROADMAP.md").read_text(encoding="utf-8")
    assert "- [x] 05-07: Implement reusable prompt assets and serial launch." in roadmap_text
    assert "- [x] 05-08: Add feedback-path verification." in roadmap_text
    assert "[-]" not in roadmap_text

    context = json.loads((plans_root / "bootstrap-context.json").read_text(encoding="utf-8"))
    assert context["active_target"]["task_id"] == "05-08"

    state_text = (plans_root / "STATE.md").read_text(encoding="utf-8")
    assert "Status: Review outcome `accepted`" in state_text


def test_launch_phase_stops_when_task_escalates(tmp_path: Path) -> None:
    plans_root = _write_launch_fixture(tmp_path)
    runner = RecordingRunner(
        task_results={
            "05-07": TaskExecutionResult(
                status="escalated",
                summary="needs clarification",
                verification=("uv run pytest tests/test_phase_launch.py",),
                review_ready=False,
            ),
        },
        review_result=PhaseReviewResult(outcome="accepted", summary="unused"),
    )

    result = launch_phase(
        plans_root=plans_root,
        runner=runner,
        workspace_context=_workspace_context(plans_root.parent / "repo"),
    )

    assert result.completed_tasks == ()
    assert result.stopped_task == "05-07"
    assert result.review_result is None

    roadmap_text = (plans_root / "ROADMAP.md").read_text(encoding="utf-8")
    assert "- [-] 05-07: Implement reusable prompt assets and serial launch." in roadmap_text
    assert "- [ ] 05-08: Add feedback-path verification." in roadmap_text


def test_launch_phase_rejects_missing_required_prompt_role(tmp_path: Path) -> None:
    plans_root = _write_launch_fixture(tmp_path)
    templates = load_workflow_prompt_assets()
    templates.pop("task_execution")
    runner = RecordingRunner(
        task_results={},
        review_result=PhaseReviewResult(outcome="accepted", summary="unused"),
    )

    with pytest.raises(
        PhaseLaunchError,
        match="required prompt-template roles are unavailable: task_execution",
    ):
        launch_phase(
            plans_root=plans_root,
            runner=runner,
            prompt_assets=templates,
            workspace_context=_workspace_context(plans_root.parent / "repo"),
        )


def test_launch_phase_rejects_missing_bootstrap_context(tmp_path: Path) -> None:
    plans_root = tmp_path / "plans"
    plans_root.mkdir()

    with pytest.raises(PhaseLaunchError, match="bootstrap context is missing"):
        launch_phase(
            plans_root=plans_root,
            runner=RecordingRunner(task_results={}, review_result=None),
            workspace_context=_workspace_context(tmp_path / "repo"),
        )


def _write_launch_fixture(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    specs_root = repo_root / "lat.md"
    specs_root.mkdir()
    (specs_root / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
    (specs_root / "architecture.md").write_text("# Architecture\n", encoding="utf-8")

    plans_root = tmp_path / "plans"
    plans_root.mkdir()
    (plans_root / "PROJECT.md").write_text("# Project\n", encoding="utf-8")
    (plans_root / "STATE.md").write_text(
        "\n".join(
            [
                "# Project State",
                "",
                "**Current focus:** Phase 05 - First Executable Slice (next task `05-07`)",
                "Phase: 5 of 5 (First Executable Slice)",
                "Task: 05-07 of 2 in current phase",
                "Status: Ready to execute",
                "Last activity: bootstrap persisted context",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (plans_root / "ROADMAP.md").write_text(
        "\n".join(
            [
                "# Roadmap",
                "",
                "### Phase 5: First Executable Slice",
                "",
                "Tasks:",
                "- [ ] 05-07: Implement reusable prompt assets and serial launch.",
                "- [ ] 05-08: Add feedback-path verification.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (plans_root / "PHASE-05.md").write_text(
        "\n".join(
            [
                "# Phase 5",
                "",
                "### Task 05-07: implement prompt assets and serial launch",
                "",
                "**References**",
                "- `lat.md/workflow.md`",
                "- `.planning/ROADMAP.md`",
                "",
                "**Definition of Done**",
                "- launch is wired",
                "",
                "### Task 05-08: feedback path",
                "",
                "**References**",
                "- `lat.md/architecture.md`",
                "- `.planning/STATE.md`",
                "",
                "**Definition of Done**",
                "- docs updated",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (plans_root / "bootstrap-context.json").write_text(
        json.dumps(
            {
                "project": {"name": "Forward Roll", "repo_root": str(repo_root)},
                "specs_root": str(specs_root),
                "plans_root": str(plans_root),
                "defaults_applied": ["values"],
                "active_target": {
                    "phase_id": "05",
                    "phase_name": "First Executable Slice",
                    "phase_document": "PHASE-05.md",
                    "task_id": "05-07",
                    "task_title": "Implement reusable prompt assets and serial launch.",
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return plans_root


def _write_external_specs_fixture(specs_root: Path) -> Path:
    specs_root.mkdir(parents=True)
    (specs_root / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
    (specs_root / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    return specs_root.resolve()


def _write_bootstrap_source_fixture(repo_root: Path) -> Path:
    repo_root.mkdir(parents=True)
    (repo_root / "lat.md").mkdir()
    planning_root = repo_root / ".planning"
    planning_root.mkdir()
    (planning_root / "PROJECT.md").write_text("# Project\n", encoding="utf-8")
    (planning_root / "STATE.md").write_text(
        "\n".join(
            [
                "# Project State",
                "",
                "**Current focus:** Phase 05 - First Executable Slice (next task `05-07`)",
                "Phase: 5 of 5 (First Executable Slice)",
                "Task: 05-07 of 2 in current phase",
                "Status: Ready to execute",
                "Last activity: bootstrap persisted context",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (planning_root / "ROADMAP.md").write_text(
        "\n".join(
            [
                "# Roadmap",
                "",
                "### Phase 5: First Executable Slice",
                "",
                "**Tasks**: 2 tasks",
                "",
                "Tasks:",
                "- [ ] 05-07: Implement reusable prompt assets and serial launch.",
                "- [ ] 05-08: Add feedback-path verification.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (planning_root / "PHASE-05.md").write_text(
        "\n".join(
            [
                "# Phase 5",
                "",
                "### Task 05-07: implement prompt assets and serial launch",
                "",
                "**References**",
                "- `lat.md/workflow.md`",
                "- `.planning/ROADMAP.md`",
                "",
                "**Definition of Done**",
                "- launch is wired",
                "",
                "### Task 05-08: feedback path",
                "",
                "**References**",
                "- `lat.md/architecture.md`",
                "- `.planning/STATE.md`",
                "",
                "**Definition of Done**",
                "- docs updated",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return repo_root.resolve()


def _workspace_context(repo_root: Path) -> WorkspaceContext:
    return WorkspaceContext(
        repo_root=repo_root,
        jj_status="Working copy clean.\n",
    )


class RecordingRunner(ExecutionRunner):
    def __init__(
        self,
        *,
        task_results: dict[str, TaskExecutionResult],
        review_result: PhaseReviewResult | None,
        planning_result: PlanningUpdateResult | None = None,
    ) -> None:
        self._task_results = task_results
        self._review_result = review_result
        self._planning_result = planning_result
        self.seen_tasks: list[tuple[str, str]] = []
        self.seen_planning_updates: list[str] = []

    def run_task_execution(
        self,
        prompt: BoundPrompt,
        *,
        task: PhaseTaskContract,
    ) -> TaskExecutionResult:
        self.seen_tasks.append((task.task_id, prompt.asset.role))
        return self._task_results[task.task_id]

    def run_phase_review(
        self,
        prompt: BoundPrompt,
        *,
        phase: object,
    ) -> PhaseReviewResult:
        del phase
        assert prompt.asset.role == "phase_review"
        assert self._review_result is not None
        return self._review_result

    def run_planning_update(
        self,
        prompt: BoundPrompt,
        *,
        phase: object,
        review_result: PhaseReviewResult,
        operator_input: str,
    ) -> PlanningUpdateResult:
        del phase, review_result, operator_input
        assert prompt.asset.role == "planning_update"
        assert self._planning_result is not None
        self.seen_planning_updates.append(prompt.slot_bindings[-1].content)
        return self._planning_result
