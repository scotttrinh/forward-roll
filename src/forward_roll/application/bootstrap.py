"""Application services for bootstrap-oriented workflows."""
# @lat: [[architecture#Application Layer]]
# @lat: [[workflow#Bootstrap Summary Rendering]]

from __future__ import annotations

import json
import shutil
from pathlib import Path

from attrs import frozen

from forward_roll.domain.model import BootstrapDirective


@frozen
class BootstrapArtifacts:
    """Durable outputs written by the bootstrap handoff."""

    context_path: Path
    summary_path: Path
    planning_files: tuple[Path, ...]


class BootstrapApplicationError(Exception):
    """Raised when bootstrap cannot persist its durable handoff artifacts."""

    pass


def bootstrap_project(directive: BootstrapDirective) -> BootstrapArtifacts:
    """Persist the executable bootstrap handoff artifacts in plans_root."""
    source_plans_root = directive.identity.repo_root / ".planning"
    if not source_plans_root.exists() or not source_plans_root.is_dir():
        msg = f"source planning root does not exist: {source_plans_root}"
        raise BootstrapApplicationError(msg)

    try:
        directive.plans_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        msg = f"failed to create plans_root: {directive.plans_root}"
        raise BootstrapApplicationError(msg) from exc

    planning_files = (
        "PROJECT.md",
        "ROADMAP.md",
        "STATE.md",
        directive.active_target.phase_document,
    )
    written_planning_files = tuple(
        _refresh_planning_file(
            source_path=source_plans_root / relative_path,
            target_path=directive.plans_root / relative_path,
        )
        for relative_path in planning_files
    )

    context_path = directive.plans_root / "bootstrap-context.json"
    summary_path = directive.plans_root / "BOOTSTRAP.md"
    try:
        context_path.write_text(_render_bootstrap_context_json(directive), encoding="utf-8")
        summary_path.write_text(render_bootstrap_summary(directive), encoding="utf-8")
    except OSError as exc:
        msg = f"failed to persist bootstrap artifacts in {directive.plans_root}"
        raise BootstrapApplicationError(msg) from exc

    return BootstrapArtifacts(
        context_path=context_path,
        summary_path=summary_path,
        planning_files=written_planning_files,
    )


def render_bootstrap_summary(directive: BootstrapDirective) -> str:
    """Render a concise bootstrap summary from a typed directive."""
    defaults = ", ".join(directive.defaults_applied) if directive.defaults_applied else "(none)"
    return "\n".join(
        [
            "# Bootstrap Summary",
            "",
            f"project={directive.identity.name}",
            f"repo_root={directive.identity.repo_root}",
            f"specs_root={directive.specs_root}",
            f"plans_root={directive.plans_root}",
            f"defaults_applied={defaults}",
            f"active_phase={directive.active_target.phase_id}",
            f"active_phase_name={directive.active_target.phase_name}",
            f"active_phase_document={directive.active_target.phase_document}",
            f"active_task={directive.active_target.task_id}",
            f"active_task_title={directive.active_target.task_title}",
        ]
    )


def _refresh_planning_file(*, source_path: Path, target_path: Path) -> Path:
    if not source_path.exists() or not source_path.is_file():
        msg = f"required planning artifact is missing: {source_path}"
        raise BootstrapApplicationError(msg)
    if source_path == target_path:
        return target_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    return target_path


def _render_bootstrap_context_json(directive: BootstrapDirective) -> str:
    context = {
        "project": {
            "name": directive.identity.name,
            "repo_root": str(directive.identity.repo_root),
        },
        "specs_root": str(directive.specs_root),
        "plans_root": str(directive.plans_root),
        "defaults_applied": list(directive.defaults_applied),
        "active_target": {
            "phase_id": directive.active_target.phase_id,
            "phase_name": directive.active_target.phase_name,
            "phase_document": directive.active_target.phase_document,
            "task_id": directive.active_target.task_id,
            "task_title": directive.active_target.task_title,
        },
        "values": {
            "architecture": list(directive.values.architecture),
            "tests": list(directive.values.tests),
            "typing": list(directive.values.typing),
            "phase_verification": list(directive.values.phase_verification),
            "version_control": list(directive.values.version_control),
            "communication": list(directive.values.communication),
        },
    }
    return json.dumps(context, indent=2, sort_keys=True) + "\n"
