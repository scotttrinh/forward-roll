"""TOML-backed bootstrap configuration adapter."""
# @lat: [[architecture#Adapter Layer]]
# @lat: [[architecture#Type Posture]]
# @lat: [[workflow#Bootstrap Config Loading]]

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from cattrs import Converter

from forward_roll.domain.model import BootstrapDirective, ProjectIdentity, ValueSet

_converter = Converter()


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
        identity = _converter.structure(
            {
                **project_section,
                "repo_root": _resolve_path(project_section["repo_root"], base_path),
            },
            ProjectIdentity,
        )
        planning_root = _converter.structure(
            _resolve_path(config_document["planning_root"], base_path),
            Path,
        )
        values_section = config_document.get("values")
        if values_section is None:
            values = ValueSet.default()
        else:
            values = _converter.structure(values_section, ValueSet)
    except KeyError as exc:
        msg = f"bootstrap config is missing required key: {exc.args[0]}"
        raise BootstrapConfigError(msg) from exc
    except TypeError as exc:
        msg = f"bootstrap config has invalid structure: {exc}"
        raise BootstrapConfigError(msg) from exc
    except ValueError as exc:
        msg = f"bootstrap config has invalid value: {exc}"
        raise BootstrapConfigError(msg) from exc

    return BootstrapDirective(identity=identity, planning_root=planning_root, values=values)


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
