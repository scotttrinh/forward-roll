"""High-value tests for bootstrap configuration loading."""
# @lat: [[domain#Testing Philosophy]]
# @lat: [[workflow#Bootstrap Config Loading]]
# @lat: [[workflow#Bootstrap Summary Rendering]]

from __future__ import annotations

from pathlib import Path

from forward_roll.adapters.bootstrap_config import load_bootstrap_directive
from forward_roll.application.bootstrap import render_bootstrap_summary
from forward_roll.domain.model import ValueSet


def test_load_bootstrap_directive_from_toml(tmp_path: Path) -> None:
    config_path = tmp_path / "forward-roll.toml"
    config_path.write_text(
        """
planning_root = "../planning"

[project]
name = "Forward Roll"
repo_root = "../repo"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    directive = load_bootstrap_directive(config_path)

    assert directive.identity.name == "Forward Roll"
    assert directive.identity.repo_root == (tmp_path / "../repo").resolve()
    assert directive.planning_root == (tmp_path / "../planning").resolve()
    assert directive.values == ValueSet.default()

    summary = render_bootstrap_summary(directive)

    assert f"repo_root={(tmp_path / '../repo').resolve()}" in summary
    assert f"planning_root={(tmp_path / '../planning').resolve()}" in summary
