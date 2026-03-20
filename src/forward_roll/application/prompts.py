"""Workflow prompt assets and slot binding helpers."""
# @lat: [[architecture#Workflow Prompt Assets]]
# @lat: [[workflow#Workflow Prompt Templates]]
# @lat: [[workflow#Workflow Prompt Templates]]
# @lat: [[workflow#Workflow Prompt Templates]]

from __future__ import annotations

from pathlib import Path

from attrs import frozen


@frozen
class ContextDocument:
    """A concrete runtime document bound into a prompt slot."""

    label: str
    path: Path
    content: str


@frozen
class WorkspaceContext:
    """Execution-local repository context derived at launch time."""

    repo_root: Path
    jj_status: str


@frozen
class PromptRuntimeEnvelope:
    """Shared runtime inputs supplied to workflow prompt assets."""

    bootstrap_context: ContextDocument
    spec_context: tuple[ContextDocument, ...]
    planning_context: tuple[ContextDocument, ...]
    operator_input: str | None = None
    workspace_context: WorkspaceContext | None = None


@frozen
class PromptTemplateAsset:
    """A stable workflow prompt asset identified by role and version."""

    role: str
    version: str
    required_slots: tuple[str, ...]
    instructions: str
    output_contract: str
    allowed_effects: tuple[str, ...]


@frozen
class PromptSlotBinding:
    """A concrete slot binding for a prompt asset invocation."""

    slot_name: str
    content: str


@frozen
class BoundPrompt:
    """A prompt asset plus its stable slot bindings for one invocation."""

    asset: PromptTemplateAsset
    slot_bindings: tuple[PromptSlotBinding, ...]


class PromptAssetError(Exception):
    """Raised when prompt assets or slot bindings are invalid."""

    pass


_PROMPT_ASSETS: dict[str, PromptTemplateAsset] = {
    "planning_update": PromptTemplateAsset(
        role="planning_update",
        version="v1",
        required_slots=(
            "bootstrap_context",
            "spec_context",
            "planning_context",
            "operator_input",
        ),
        instructions=(
            "Update planning artifacts without inventing a second planning system. "
            "Use the bound specs, plans, and operator input to append or adjust "
            "durable planning state only when the workflow contract explicitly allows it."
        ),
        output_contract=(
            "Return the planning decision, the concrete artifact updates required, and "
            "any escalation when the current phase boundary no longer holds."
        ),
        allowed_effects=(
            "create_or_update_planning_artifacts",
            "append_in_phase_task_contracts_when_allowed",
            "report_escalation",
        ),
    ),
    "task_execution": PromptTemplateAsset(
        role="task_execution",
        version="v1",
        required_slots=(
            "bootstrap_context",
            "active_task_contract",
            "spec_context",
            "planning_context",
            "workspace_context",
        ),
        instructions=(
            "Execute exactly one active task contract. Stay within the task boundary, "
            "report the verification actually performed, and stop instead of widening scope."
        ),
        output_contract=(
            "Return task status, a concise execution summary, the verification actually "
            "performed, and whether the workspace history is reduced to one reviewable jj revision."
        ),
        allowed_effects=(
            "edit_repository_files_within_task_scope",
            "edit_planning_files_within_task_scope",
            "report_verification",
            "report_escalation",
        ),
    ),
    "phase_review": PromptTemplateAsset(
        role="phase_review",
        version="v1",
        required_slots=(
            "bootstrap_context",
            "spec_context",
            "planning_context",
            "review_target",
            "operator_input",
        ),
        instructions=(
            "Review the assembled phase deliverable against the bound specs and plans. "
            "Return a reviewer-facing outcome and next-step guidance without silently "
            "doing new implementation work."
        ),
        output_contract=(
            "Return one of: accepted, extend phase with follow-on task(s), or broader "
            "realignment, plus the supporting reviewer-facing explanation."
        ),
        allowed_effects=(
            "produce_review_outcome",
            "produce_planning_guidance",
            "report_escalation",
        ),
    ),
}


def load_workflow_prompt_assets() -> dict[str, PromptTemplateAsset]:
    """Load the stable workflow prompt assets used by phase launch."""
    return dict(_PROMPT_ASSETS)


def bind_prompt_template(
    asset: PromptTemplateAsset,
    *,
    slot_values: dict[str, str],
) -> BoundPrompt:
    """Bind stable slot values to a prompt asset in deterministic order."""
    bindings: list[PromptSlotBinding] = []
    for slot_name in asset.required_slots:
        try:
            slot_content = slot_values[slot_name]
        except KeyError as exc:
            msg = f"missing required prompt slot for {asset.role}: {slot_name}"
            raise PromptAssetError(msg) from exc
        bindings.append(PromptSlotBinding(slot_name=slot_name, content=slot_content))
    return BoundPrompt(asset=asset, slot_bindings=tuple(bindings))


def render_context_documents(documents: tuple[ContextDocument, ...]) -> str:
    """Render bound documents in a stable, reviewer-readable format."""
    if not documents:
        return "(none)"
    return "\n\n".join(
        "\n".join(
            [
                f"[{document.label}]",
                f"path={document.path}",
                document.content.rstrip(),
            ]
        )
        for document in documents
    )


def render_workspace_context(workspace_context: WorkspaceContext | None) -> str:
    """Render optional workspace context for prompt binding."""
    if workspace_context is None:
        return "(none)"
    return "\n".join(
        [
            f"repo_root={workspace_context.repo_root}",
            "jj_status:",
            workspace_context.jj_status.rstrip(),
        ]
    )
