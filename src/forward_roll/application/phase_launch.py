"""Application services for serial phase launch."""
# @lat: [[architecture#Application Layer]]
# @lat: [[workflow#Phase Launch Contract]]
# @lat: [[workflow#Phase Launch Contract]]
# @lat: [[workflow#Phase Launch Contract]]

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Literal, Protocol

from attrs import frozen

from forward_roll.application.prompts import (
    BoundPrompt,
    ContextDocument,
    PromptTemplateAsset,
    WorkspaceContext,
    bind_prompt_template,
    load_workflow_prompt_assets,
    render_context_documents,
    render_workspace_context,
)

_ROADMAP_PHASE_PATTERN = re.compile(r"^###\s+Phase\s+(?P<phase_id>\d+):\s+(?P<phase_name>.+)$")
_ROADMAP_TASK_PATTERN = re.compile(
    r"^- \[(?P<state>[ x-])\] (?P<task_id>\d{2}-\d{2}): (?P<task_title>.+)$"
)
_PHASE_TASK_HEADING_PATTERN = re.compile(
    r"^###\s+Task\s+(?P<task_id>\d{2}-\d{2}):\s+(?P<title>.+)$",
    re.MULTILINE,
)
_REFERENCE_PATH_PATTERN = re.compile(r"- `(?P<path>[^`]+)`")


@frozen
class ActiveTarget:
    """The currently durable phase/task target."""

    phase_id: str
    phase_name: str
    phase_document: str
    task_id: str
    task_title: str


@frozen
class BootstrapContext:
    """Durable bootstrap context loaded from plans_root."""

    project_name: str
    repo_root: Path
    specs_root: Path
    plans_root: Path
    defaults_applied: tuple[str, ...]
    active_target: ActiveTarget
    raw_json: str


@frozen
class RoadmapTask:
    """Task state loaded from ROADMAP.md."""

    phase_id: str
    phase_name: str
    task_id: str
    title: str
    state: Literal["todo", "in_progress", "done"]


@frozen
class PhaseTaskContract:
    """A task contract section extracted from a phase document."""

    task_id: str
    title: str
    markdown: str
    state: Literal["todo", "in_progress", "done"]


@frozen
class PhaseContract:
    """Ordered task contracts for a launched phase."""

    phase_id: str
    phase_name: str
    path: Path
    tasks: tuple[PhaseTaskContract, ...]


@frozen
class TaskExecutionResult:
    """Runner output for one task execution."""

    status: Literal["completed", "escalated"]
    summary: str
    verification: tuple[str, ...]
    review_ready: bool
    revision_ref: str | None = None


@frozen
class PhaseReviewResult:
    """Runner output for phase review."""

    outcome: Literal["accepted", "extend_phase", "broader_realignment"]
    summary: str


@frozen
class PhaseLaunchResult:
    """Structured outcome of a serial phase launch."""

    phase_id: str
    completed_tasks: tuple[str, ...]
    stopped_task: str | None
    review_result: PhaseReviewResult | None


class PhaseLaunchError(Exception):
    """Raised when phase launch cannot proceed cleanly."""

    pass


class ExecutionRunner(Protocol):
    """Narrow execution boundary for task execution and phase review."""

    def run_task_execution(
        self,
        prompt: BoundPrompt,
        *,
        task: PhaseTaskContract,
    ) -> TaskExecutionResult: ...

    def run_phase_review(
        self,
        prompt: BoundPrompt,
        *,
        phase: PhaseContract,
    ) -> PhaseReviewResult: ...


class UnavailableExecutionRunner:
    """Default runner used by the CLI until a live adapter exists."""

    def run_task_execution(
        self,
        prompt: BoundPrompt,
        *,
        task: PhaseTaskContract,
    ) -> TaskExecutionResult:
        del prompt, task
        msg = "phase launch requires a configured execution runner adapter"
        raise PhaseLaunchError(msg)

    def run_phase_review(
        self,
        prompt: BoundPrompt,
        *,
        phase: PhaseContract,
    ) -> PhaseReviewResult:
        del prompt, phase
        msg = "phase launch requires a configured execution runner adapter"
        raise PhaseLaunchError(msg)


def launch_phase(
    *,
    plans_root: Path,
    runner: ExecutionRunner,
    phase_selector: str | None = None,
    prompt_assets: dict[str, PromptTemplateAsset] | None = None,
    workspace_context: WorkspaceContext | None = None,
) -> PhaseLaunchResult:
    """Launch the selected phase through the narrow serial execution loop."""
    bootstrap_context = load_bootstrap_context(plans_root)
    templates = load_workflow_prompt_assets() if prompt_assets is None else prompt_assets
    _require_prompt_roles(templates, required_roles=("task_execution", "phase_review"))

    phase_contract = load_phase_contract(
        plans_root=bootstrap_context.plans_root,
        active_target=bootstrap_context.active_target,
        phase_selector=phase_selector,
    )
    incomplete_tasks = tuple(task for task in phase_contract.tasks if task.state != "done")
    if not incomplete_tasks:
        msg = f"no incomplete task contracts remain in {phase_contract.path}"
        raise PhaseLaunchError(msg)

    runtime_workspace_context = (
        collect_workspace_context(bootstrap_context.repo_root)
        if workspace_context is None
        else workspace_context
    )
    _mark_task_in_progress(
        plans_root=bootstrap_context.plans_root,
        current_task=incomplete_tasks[0],
    )

    completed_tasks: list[str] = []
    phase_contract = load_phase_contract(
        plans_root=bootstrap_context.plans_root,
        active_target=bootstrap_context.active_target,
        phase_selector=phase_selector,
    )

    for task_index, task in enumerate(phase_contract.tasks):
        if task.state == "done":
            continue

        task_prompt = bind_prompt_template(
            templates["task_execution"],
            slot_values={
                "bootstrap_context": bootstrap_context.raw_json.rstrip(),
                "active_task_contract": task.markdown.rstrip(),
                "spec_context": render_context_documents(
                    _load_spec_context(
                        bootstrap_context=bootstrap_context,
                        task=task,
                    )
                ),
                "planning_context": render_context_documents(
                    _load_task_planning_context(
                        plans_root=bootstrap_context.plans_root,
                        phase_contract=phase_contract,
                        task=task,
                    )
                ),
                "workspace_context": render_workspace_context(runtime_workspace_context),
            },
        )
        execution_result = runner.run_task_execution(task_prompt, task=task)

        if execution_result.status != "completed":
            return PhaseLaunchResult(
                phase_id=phase_contract.phase_id,
                completed_tasks=tuple(completed_tasks),
                stopped_task=task.task_id,
                review_result=None,
            )
        if not execution_result.verification:
            msg = f"task execution completed without reported verification: {task.task_id}"
            raise PhaseLaunchError(msg)
        if not execution_result.review_ready:
            return PhaseLaunchResult(
                phase_id=phase_contract.phase_id,
                completed_tasks=tuple(completed_tasks),
                stopped_task=task.task_id,
                review_result=None,
            )

        completed_tasks.append(task.task_id)
        next_task = _next_incomplete_task(phase_contract.tasks, start_index=task_index + 1)
        _advance_planning_focus(
            bootstrap_context=bootstrap_context,
            phase_contract=phase_contract,
            completed_task=task,
            next_task=next_task,
        )
        if next_task is None:
            break
        phase_contract = load_phase_contract(
            plans_root=bootstrap_context.plans_root,
            active_target=bootstrap_context.active_target,
            phase_selector=phase_selector,
        )

    refreshed_phase_contract = load_phase_contract(
        plans_root=bootstrap_context.plans_root,
        active_target=bootstrap_context.active_target,
        phase_selector=phase_selector,
    )
    review_prompt = bind_prompt_template(
        templates["phase_review"],
        slot_values={
            "bootstrap_context": bootstrap_context.raw_json.rstrip(),
            "spec_context": render_context_documents(
                _load_phase_spec_context(
                    bootstrap_context=bootstrap_context,
                    phase_contract=refreshed_phase_contract,
                )
            ),
            "planning_context": render_context_documents(
                _load_phase_planning_context(
                    plans_root=bootstrap_context.plans_root,
                    phase_contract=refreshed_phase_contract,
                )
            ),
            "review_target": _render_review_target(
                phase_contract=refreshed_phase_contract,
                completed_tasks=tuple(completed_tasks),
            ),
            "operator_input": "(none)",
        },
    )
    review_result = runner.run_phase_review(review_prompt, phase=refreshed_phase_contract)
    _update_state_for_phase_review(
        plans_root=bootstrap_context.plans_root,
        phase_contract=refreshed_phase_contract,
        review_result=review_result,
    )
    return PhaseLaunchResult(
        phase_id=refreshed_phase_contract.phase_id,
        completed_tasks=tuple(completed_tasks),
        stopped_task=None,
        review_result=review_result,
    )


def load_bootstrap_context(plans_root: Path) -> BootstrapContext:
    """Load the persisted bootstrap context artifact from plans_root."""
    context_path = plans_root / "bootstrap-context.json"
    try:
        raw_json = context_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        msg = f"bootstrap context is missing: {context_path}"
        raise PhaseLaunchError(msg) from exc

    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        msg = f"bootstrap context is not valid JSON: {context_path}"
        raise PhaseLaunchError(msg) from exc

    active_target_payload = payload.get("active_target")
    if not isinstance(active_target_payload, dict):
        msg = f"bootstrap context is missing active_target: {context_path}"
        raise PhaseLaunchError(msg)
    project_payload = payload.get("project")
    if not isinstance(project_payload, dict):
        msg = f"bootstrap context is missing project identity: {context_path}"
        raise PhaseLaunchError(msg)

    return BootstrapContext(
        project_name=str(project_payload["name"]),
        repo_root=Path(str(project_payload["repo_root"])).expanduser().resolve(),
        specs_root=Path(str(payload["specs_root"])).expanduser().resolve(),
        plans_root=Path(str(payload["plans_root"])).expanduser().resolve(),
        defaults_applied=tuple(str(value) for value in payload.get("defaults_applied", [])),
        active_target=ActiveTarget(
            phase_id=str(active_target_payload["phase_id"]).zfill(2),
            phase_name=str(active_target_payload["phase_name"]),
            phase_document=str(active_target_payload["phase_document"]),
            task_id=str(active_target_payload["task_id"]),
            task_title=str(active_target_payload["task_title"]),
        ),
        raw_json=raw_json,
    )


def load_phase_contract(
    *,
    plans_root: Path,
    active_target: ActiveTarget,
    phase_selector: str | None,
) -> PhaseContract:
    """Load ordered task contracts for the selected phase."""
    target_phase_id = active_target.phase_id if phase_selector is None else phase_selector.zfill(2)
    roadmap_tasks = _load_roadmap_tasks(plans_root / "ROADMAP.md")
    phase_roadmap_tasks = tuple(task for task in roadmap_tasks if task.phase_id == target_phase_id)
    if not phase_roadmap_tasks:
        msg = f"selected phase is not present in ROADMAP.md: {target_phase_id}"
        raise PhaseLaunchError(msg)

    phase_name = phase_roadmap_tasks[0].phase_name
    phase_path = plans_root / f"PHASE-{target_phase_id}.md"
    try:
        phase_text = phase_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        msg = f"selected phase contract is missing: {phase_path}"
        raise PhaseLaunchError(msg) from exc

    tasks = _parse_phase_task_contracts(
        phase_text=phase_text,
        phase_path=phase_path,
        roadmap_tasks=phase_roadmap_tasks,
    )
    return PhaseContract(
        phase_id=target_phase_id,
        phase_name=phase_name,
        path=phase_path,
        tasks=tasks,
    )


def collect_workspace_context(repo_root: Path) -> WorkspaceContext:
    """Collect the launch-time workspace context from jj."""
    result = subprocess.run(
        ["jj", "status"],
        check=False,
        capture_output=True,
        cwd=repo_root,
        encoding="utf-8",
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        msg = f"workspace is not ready for jj-native launch: {stderr}"
        raise PhaseLaunchError(msg)
    return WorkspaceContext(repo_root=repo_root, jj_status=result.stdout)


def _require_prompt_roles(
    templates: dict[str, PromptTemplateAsset],
    *,
    required_roles: tuple[str, ...],
) -> None:
    missing = [role for role in required_roles if role not in templates]
    if missing:
        msg = f"required prompt-template roles are unavailable: {', '.join(missing)}"
        raise PhaseLaunchError(msg)


def _load_roadmap_tasks(roadmap_path: Path) -> tuple[RoadmapTask, ...]:
    try:
        roadmap_text = roadmap_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        msg = f"planning roadmap is missing: {roadmap_path}"
        raise PhaseLaunchError(msg) from exc

    current_phase_id: str | None = None
    current_phase_name: str | None = None
    tasks: list[RoadmapTask] = []
    for line in roadmap_text.splitlines():
        phase_match = _ROADMAP_PHASE_PATTERN.match(line)
        if phase_match is not None:
            current_phase_id = phase_match.group("phase_id").zfill(2)
            current_phase_name = phase_match.group("phase_name").strip()
            continue
        task_match = _ROADMAP_TASK_PATTERN.match(line)
        if task_match is None or current_phase_id is None or current_phase_name is None:
            continue
        tasks.append(
            RoadmapTask(
                phase_id=current_phase_id,
                phase_name=current_phase_name,
                task_id=task_match.group("task_id"),
                title=task_match.group("task_title").strip(),
                state=_decode_task_state(task_match.group("state")),
            )
        )
    return tuple(tasks)


def _parse_phase_task_contracts(
    *,
    phase_text: str,
    phase_path: Path,
    roadmap_tasks: tuple[RoadmapTask, ...],
) -> tuple[PhaseTaskContract, ...]:
    matches = list(_PHASE_TASK_HEADING_PATTERN.finditer(phase_text))
    if not matches:
        msg = f"no task contracts found in phase document: {phase_path}"
        raise PhaseLaunchError(msg)

    task_states = {task.task_id: task for task in roadmap_tasks}
    contracts: list[PhaseTaskContract] = []
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(phase_text)
        markdown = phase_text[match.start() : next_start].strip()
        task_id = match.group("task_id")
        roadmap_task = task_states.get(task_id)
        if roadmap_task is None:
            msg = f"phase task {task_id} is missing from ROADMAP.md"
            raise PhaseLaunchError(msg)
        contracts.append(
            PhaseTaskContract(
                task_id=task_id,
                title=match.group("title").strip(),
                markdown=markdown,
                state=roadmap_task.state,
            )
        )
    return tuple(contracts)


def _decode_task_state(state_marker: str) -> Literal["todo", "in_progress", "done"]:
    if state_marker == "x":
        return "done"
    if state_marker == "-":
        return "in_progress"
    return "todo"


def _load_spec_context(
    *,
    bootstrap_context: BootstrapContext,
    task: PhaseTaskContract,
) -> tuple[ContextDocument, ...]:
    documents = _load_reference_documents(
        references=_extract_reference_paths(task.markdown),
        bootstrap_context=bootstrap_context,
        include_prefix="spec",
    )
    if documents:
        return documents
    fallback_path = bootstrap_context.specs_root / "workflow.md"
    return (_read_context_document("workflow_spec", fallback_path),)


def _load_phase_spec_context(
    *,
    bootstrap_context: BootstrapContext,
    phase_contract: PhaseContract,
) -> tuple[ContextDocument, ...]:
    references: list[str] = []
    for task in phase_contract.tasks:
        references.extend(_extract_reference_paths(task.markdown))
    documents = _load_reference_documents(
        references=tuple(dict.fromkeys(references)),
        bootstrap_context=bootstrap_context,
        include_prefix="spec",
    )
    if documents:
        return documents
    fallback_path = bootstrap_context.specs_root / "workflow.md"
    return (_read_context_document("workflow_spec", fallback_path),)


def _load_task_planning_context(
    *,
    plans_root: Path,
    phase_contract: PhaseContract,
    task: PhaseTaskContract,
) -> tuple[ContextDocument, ...]:
    documents = [
        _read_context_document("project_plan", plans_root / "PROJECT.md"),
        _read_context_document("roadmap_plan", plans_root / "ROADMAP.md"),
        _read_context_document("state_plan", plans_root / "STATE.md"),
        _read_context_document("phase_contract", phase_contract.path),
        ContextDocument(
            label="active_task_contract",
            path=phase_contract.path,
            content=task.markdown,
        ),
    ]
    return tuple(documents)


def _load_phase_planning_context(
    *,
    plans_root: Path,
    phase_contract: PhaseContract,
) -> tuple[ContextDocument, ...]:
    return (
        _read_context_document("project_plan", plans_root / "PROJECT.md"),
        _read_context_document("roadmap_plan", plans_root / "ROADMAP.md"),
        _read_context_document("state_plan", plans_root / "STATE.md"),
        _read_context_document("phase_contract", phase_contract.path),
    )


def _load_reference_documents(
    *,
    references: tuple[str, ...],
    bootstrap_context: BootstrapContext,
    include_prefix: Literal["spec", "planning"],
) -> tuple[ContextDocument, ...]:
    documents: list[ContextDocument] = []
    for reference in references:
        resolved = _resolve_reference_path(reference, bootstrap_context=bootstrap_context)
        if resolved is None:
            continue
        is_spec = resolved.is_relative_to(bootstrap_context.specs_root)
        if include_prefix == "spec" and not is_spec:
            continue
        if include_prefix == "planning" and is_spec:
            continue
        documents.append(_read_context_document(f"{include_prefix}_{resolved.name}", resolved))
    return tuple(documents)


def _extract_reference_paths(markdown: str) -> tuple[str, ...]:
    return tuple(match.group("path") for match in _REFERENCE_PATH_PATTERN.finditer(markdown))


def _resolve_reference_path(
    reference: str,
    *,
    bootstrap_context: BootstrapContext,
) -> Path | None:
    if reference.startswith("lat.md/"):
        return (bootstrap_context.specs_root / reference.removeprefix("lat.md/")).resolve()
    if reference.startswith(".planning/"):
        return (bootstrap_context.plans_root / reference.removeprefix(".planning/")).resolve()
    return None


def _read_context_document(label: str, path: Path) -> ContextDocument:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        msg = f"context document is missing: {path}"
        raise PhaseLaunchError(msg) from exc
    return ContextDocument(label=label, path=path, content=content)


def _next_incomplete_task(
    tasks: tuple[PhaseTaskContract, ...],
    *,
    start_index: int,
) -> PhaseTaskContract | None:
    for task in tasks[start_index:]:
        if task.state != "done":
            return task
    return None


def _mark_task_in_progress(*, plans_root: Path, current_task: PhaseTaskContract) -> None:
    roadmap_path = plans_root / "ROADMAP.md"
    roadmap_text = roadmap_path.read_text(encoding="utf-8")
    updated_lines: list[str] = []
    for line in roadmap_text.splitlines():
        match = _ROADMAP_TASK_PATTERN.match(line)
        if match is None:
            updated_lines.append(line)
            continue
        task_id = match.group("task_id")
        title = match.group("task_title").strip()
        if task_id == current_task.task_id:
            updated_lines.append(f"- [-] {task_id}: {title}")
        elif match.group("state") == "-":
            updated_lines.append(f"- [ ] {task_id}: {title}")
        else:
            updated_lines.append(line)
    roadmap_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def _advance_planning_focus(
    *,
    bootstrap_context: BootstrapContext,
    phase_contract: PhaseContract,
    completed_task: PhaseTaskContract,
    next_task: PhaseTaskContract | None,
) -> None:
    _update_roadmap_after_task(
        roadmap_path=bootstrap_context.plans_root / "ROADMAP.md",
        completed_task=completed_task,
        next_task=next_task,
    )
    if next_task is not None:
        _update_bootstrap_context_target(
            bootstrap_context_path=bootstrap_context.plans_root / "bootstrap-context.json",
            next_task=next_task,
            phase_contract=phase_contract,
        )
    _update_state_after_task(
        state_path=bootstrap_context.plans_root / "STATE.md",
        phase_contract=phase_contract,
        next_task=next_task,
        completed_task=completed_task,
    )


def _update_roadmap_after_task(
    *,
    roadmap_path: Path,
    completed_task: PhaseTaskContract,
    next_task: PhaseTaskContract | None,
) -> None:
    roadmap_text = roadmap_path.read_text(encoding="utf-8")
    updated_lines: list[str] = []
    for line in roadmap_text.splitlines():
        match = _ROADMAP_TASK_PATTERN.match(line)
        if match is None:
            updated_lines.append(line)
            continue
        task_id = match.group("task_id")
        title = match.group("task_title").strip()
        if task_id == completed_task.task_id:
            updated_lines.append(f"- [x] {task_id}: {title}")
        elif next_task is not None and task_id == next_task.task_id:
            updated_lines.append(f"- [-] {task_id}: {title}")
        elif match.group("state") == "-":
            updated_lines.append(f"- [ ] {task_id}: {title}")
        else:
            updated_lines.append(line)
    roadmap_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def _update_bootstrap_context_target(
    *,
    bootstrap_context_path: Path,
    next_task: PhaseTaskContract,
    phase_contract: PhaseContract,
) -> None:
    payload = json.loads(bootstrap_context_path.read_text(encoding="utf-8"))
    payload["active_target"] = {
        "phase_id": phase_contract.phase_id,
        "phase_name": phase_contract.phase_name,
        "phase_document": phase_contract.path.name,
        "task_id": next_task.task_id,
        "task_title": next_task.title,
    }
    bootstrap_context_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _update_state_after_task(
    *,
    state_path: Path,
    phase_contract: PhaseContract,
    next_task: PhaseTaskContract | None,
    completed_task: PhaseTaskContract,
) -> None:
    state_text = state_path.read_text(encoding="utf-8")
    if next_task is None:
        focus = (
            f"**Current focus:** Phase {phase_contract.phase_id} - "
            f"{phase_contract.phase_name} (phase review)"
        )
        task_line = f"Task: Review for phase {phase_contract.phase_id}"
        status_line = "Status: Awaiting phase review"
    else:
        focus = (
            f"**Current focus:** Phase {phase_contract.phase_id} - {phase_contract.phase_name} "
            f"(next task `{next_task.task_id}`)"
        )
        task_position = _task_position(phase_contract.tasks, next_task.task_id)
        task_line = (
            f"Task: {next_task.task_id} of {len(phase_contract.tasks)} in current phase"
            if task_position is not None
            else f"Task: {next_task.task_id} in current phase"
        )
        status_line = "Status: Ready to execute"
    updated = _replace_state_line(state_text, prefix="**Current focus:**", replacement=focus)
    updated = _replace_state_line(updated, prefix="Task:", replacement=task_line)
    updated = _replace_state_line(updated, prefix="Status:", replacement=status_line)
    updated = _replace_state_line(
        updated,
        prefix="Last activity:",
        replacement=(
            f"Last activity: advanced after `{completed_task.task_id}`; "
            f"next focus is `{next_task.task_id}`"
            if next_task is not None
            else f"Last activity: completed `{completed_task.task_id}` and reached phase review"
        ),
    )
    state_path.write_text(updated, encoding="utf-8")


def _update_state_for_phase_review(
    *,
    plans_root: Path,
    phase_contract: PhaseContract,
    review_result: PhaseReviewResult,
) -> None:
    state_path = plans_root / "STATE.md"
    state_text = state_path.read_text(encoding="utf-8")
    updated = _replace_state_line(
        state_text,
        prefix="**Current focus:**",
        replacement=(
            f"**Current focus:** Phase {phase_contract.phase_id} - {phase_contract.phase_name} "
            f"(review outcome `{review_result.outcome}`)"
        ),
    )
    updated = _replace_state_line(
        updated,
        prefix="Status:",
        replacement=f"Status: Review outcome `{review_result.outcome}`",
    )
    updated = _replace_state_line(
        updated,
        prefix="Last activity:",
        replacement=f"Last activity: phase review returned `{review_result.outcome}`",
    )
    state_path.write_text(updated, encoding="utf-8")


def _replace_state_line(state_text: str, *, prefix: str, replacement: str) -> str:
    lines = state_text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            replaced = True
            break
    if not replaced:
        lines.append(replacement)
    return "\n".join(lines) + "\n"


def _task_position(tasks: tuple[PhaseTaskContract, ...], task_id: str) -> int | None:
    for index, task in enumerate(tasks, start=1):
        if task.task_id == task_id:
            return index
    return None


def _render_review_target(
    *,
    phase_contract: PhaseContract,
    completed_tasks: tuple[str, ...],
) -> str:
    completed_summary = ", ".join(completed_tasks) if completed_tasks else "(none)"
    return "\n".join(
        [
            f"phase_id={phase_contract.phase_id}",
            f"phase_name={phase_contract.phase_name}",
            f"completed_tasks={completed_summary}",
            f"phase_contract={phase_contract.path}",
        ]
    )
