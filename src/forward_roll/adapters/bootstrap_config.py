"""TOML-backed bootstrap configuration adapter."""
# @lat: [[architecture#Adapter Layer]]
# @lat: [[architecture#Type Posture]]
# @lat: [[workflow#Bootstrap Config Loading]]

from __future__ import annotations

import os
import re
import tomllib
from pathlib import Path
from typing import Any

from cattrs import Converter

from forward_roll.domain.model import (
    ActivePlanningTarget,
    BootstrapDirective,
    ProjectIdentity,
    ValueSet,
)

_converter = Converter()
_PHASE_PATTERN = re.compile(r"^###\s+Phase\s+(?P<phase_id>\d+):\s+(?P<phase_name>.+)$")
_TASK_PATTERN = re.compile(
    r"^- \[(?P<state>[ x-])\] (?P<task_id>\d{2}-\d{2}): (?P<task_title>.+)$"
)


class BootstrapConfigError(Exception):
    """Raised when bootstrap configuration cannot be loaded."""

    pass


def load_bootstrap_directive(config_path: Path) -> BootstrapDirective:
    """Load a bootstrap directive from a TOML file."""
    try:
        resolved_config_path = config_path.expanduser().resolve()
        config_document = tomllib.loads(resolved_config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        msg = f"bootstrap config file not found: {config_path}"
        raise BootstrapConfigError(msg) from exc
    except tomllib.TOMLDecodeError as exc:
        msg = f"bootstrap config file is not valid TOML: {config_path}"
        raise BootstrapConfigError(msg) from exc

    return structure_bootstrap_directive(
        config_document,
        base_path=resolved_config_path.parent,
    )


def structure_bootstrap_directive(
    config_document: dict[str, Any],
    *,
    base_path: Path,
) -> BootstrapDirective:
    """Validate a raw bootstrap config document at the adapter boundary."""
    try:
        project_section = _require_table(config_document, "project")
        repo_root = _resolve_path(project_section["repo_root"], base_path)
        plans_root_value = config_document.get("plans_root")
        legacy_planning_root_value = config_document.get("planning_root")
        if plans_root_value is not None and legacy_planning_root_value is not None:
            msg = "bootstrap config cannot set both plans_root and planning_root"
            raise BootstrapConfigError(msg)
        values_section = config_document.get("values")
        values = None if values_section is None else _converter.structure(values_section, ValueSet)
    except KeyError as exc:
        msg = f"bootstrap config is missing required key: {exc.args[0]}"
        raise BootstrapConfigError(msg) from exc
    except TypeError as exc:
        msg = f"bootstrap config has invalid structure: {exc}"
        raise BootstrapConfigError(msg) from exc
    except ValueError as exc:
        msg = f"bootstrap config has invalid value: {exc}"
        raise BootstrapConfigError(msg) from exc

    return resolve_bootstrap_directive(
        repo_root=repo_root,
        specs_root=_resolve_optional_path(config_document.get("specs_root"), base_path),
        plans_root=_resolve_optional_path(
            plans_root_value if plans_root_value is not None else legacy_planning_root_value,
            base_path,
        ),
        project_name=project_section.get("name"),
        values=values,
    )


def resolve_bootstrap_directive(
    *,
    repo_root: Path,
    specs_root: Path | None = None,
    plans_root: Path | None = None,
    project_name: str | None = None,
    values: ValueSet | None = None,
) -> BootstrapDirective:
    """Resolve defaults and validate bootstrap inputs before application use."""
    defaults_applied: list[str] = []

    resolved_repo_root = repo_root.expanduser().resolve()
    _require_existing_directory(resolved_repo_root, "repo_root")

    if specs_root is None:
        resolved_specs_root = resolved_repo_root / "lat.md"
        defaults_applied.append("specs_root")
    else:
        resolved_specs_root = specs_root.expanduser().resolve()
    _require_readable_directory(resolved_specs_root, "specs_root")

    if plans_root is None:
        resolved_plans_root = resolved_repo_root / ".planning"
        defaults_applied.append("plans_root")
    else:
        resolved_plans_root = plans_root.expanduser().resolve()
    _require_writable_directory_or_parent(resolved_plans_root, "plans_root")

    if project_name is None:
        resolved_project_name = resolved_repo_root.name
        defaults_applied.append("project.name")
    else:
        resolved_project_name = project_name.strip()
    if not resolved_project_name:
        msg = "project name must not be empty"
        raise BootstrapConfigError(msg)

    resolved_values = values
    if resolved_values is None:
        resolved_values = ValueSet.default()
        defaults_applied.append("values")

    active_target = _resolve_active_target(resolved_repo_root / ".planning")

    return BootstrapDirective(
        identity=ProjectIdentity(name=resolved_project_name, repo_root=resolved_repo_root),
        specs_root=resolved_specs_root,
        plans_root=resolved_plans_root,
        values=resolved_values,
        active_target=active_target,
        defaults_applied=tuple(defaults_applied),
    )


def _resolve_active_target(source_plans_root: Path) -> ActivePlanningTarget:
    _require_existing_directory(source_plans_root, "source plans_root")
    roadmap_path = source_plans_root / "ROADMAP.md"
    try:
        roadmap_text = roadmap_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        msg = f"planning roadmap not found: {roadmap_path}"
        raise BootstrapConfigError(msg) from exc

    current_phase_id: str | None = None
    current_phase_name: str | None = None
    fallback_target: ActivePlanningTarget | None = None

    for line in roadmap_text.splitlines():
        phase_match = _PHASE_PATTERN.match(line)
        if phase_match is not None:
            current_phase_id = phase_match.group("phase_id").zfill(2)
            current_phase_name = phase_match.group("phase_name").strip()
            continue

        task_match = _TASK_PATTERN.match(line)
        if task_match is None or current_phase_id is None or current_phase_name is None:
            continue

        target = ActivePlanningTarget(
            phase_id=current_phase_id,
            phase_name=current_phase_name,
            phase_document=f"PHASE-{current_phase_id}.md",
            task_id=task_match.group("task_id"),
            task_title=task_match.group("task_title").strip(),
        )
        if task_match.group("state") == "-":
            _require_existing_file(
                source_plans_root / target.phase_document,
                "active phase contract",
            )
            return target
        if task_match.group("state") == " " and fallback_target is None:
            fallback_target = target

    if fallback_target is None:
        msg = f"no incomplete roadmap task found in {roadmap_path}"
        raise BootstrapConfigError(msg)

    _require_existing_file(
        source_plans_root / fallback_target.phase_document,
        "active phase contract",
    )
    return fallback_target


def _require_table(config_document: dict[str, Any], key: str) -> dict[str, Any]:
    value = config_document[key]
    if not isinstance(value, dict):
        msg = f"bootstrap config key must be a table: {key}"
        raise BootstrapConfigError(msg)
    return value


def _resolve_path(value: Any, base_path: Path) -> Path:
    if not isinstance(value, str):
        msg = f"bootstrap config path must be a string: {value!r}"
        raise BootstrapConfigError(msg)
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (base_path / candidate).resolve()


def _resolve_optional_path(value: Any, base_path: Path) -> Path | None:
    if value is None:
        return None
    return _resolve_path(value, base_path)


def _require_existing_directory(path: Path, label: str) -> None:
    if not path.exists():
        msg = f"{label} does not exist: {path}"
        raise BootstrapConfigError(msg)
    if not path.is_dir():
        msg = f"{label} must be a directory: {path}"
        raise BootstrapConfigError(msg)


def _require_existing_file(path: Path, label: str) -> None:
    if not path.exists():
        msg = f"{label} does not exist: {path}"
        raise BootstrapConfigError(msg)
    if not path.is_file():
        msg = f"{label} must be a file: {path}"
        raise BootstrapConfigError(msg)


def _require_readable_directory(path: Path, label: str) -> None:
    _require_existing_directory(path, label)
    if not os.access(path, os.R_OK):
        msg = f"{label} is not readable: {path}"
        raise BootstrapConfigError(msg)


def _require_writable_directory_or_parent(path: Path, label: str) -> None:
    if path.exists():
        if not path.is_dir():
            msg = f"{label} must be a directory: {path}"
            raise BootstrapConfigError(msg)
        if not os.access(path, os.W_OK):
            msg = f"{label} is not writable: {path}"
            raise BootstrapConfigError(msg)
        return

    parent = path.parent
    while not parent.exists() and parent != parent.parent:
        parent = parent.parent
    if not parent.exists():
        msg = f"{label} cannot be created because no writable parent exists: {path}"
        raise BootstrapConfigError(msg)
    if not parent.is_dir():
        msg = f"{label} cannot be created under a non-directory parent: {path}"
        raise BootstrapConfigError(msg)
    if not os.access(parent, os.W_OK):
        msg = f"{label} cannot be created because parent is not writable: {parent}"
        raise BootstrapConfigError(msg)
