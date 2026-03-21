"""High-value tests for bootstrap configuration loading."""
# @lat: [[domain#Testing Philosophy]]
# @lat: [[workflow#Bootstrap Config Loading]]
# @lat: [[workflow#Bootstrap Summary Rendering]]
# @lat: [[workflow#Plugin-First Self-Hosting#Bootstrap Skill And Runtime Config]]

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forward_roll.adapters.bootstrap_config import (
    BootstrapConfigError,
    load_bootstrap_directive,
    resolve_bootstrap_directive,
)
from forward_roll.application.bootstrap import bootstrap_project, render_bootstrap_summary
from forward_roll.domain.model import ValueSet


def test_load_bootstrap_directive_from_toml(tmp_path: Path) -> None:
    repo_root = _write_repo_fixture(tmp_path / "repo")
    config_path = tmp_path / "forward-roll.toml"
    config_path.write_text(
        """
specs_root = "specs"
plans_root = "planning"
host_skills_root = "codex-skills"
host_agents_root = "codex-agents"

[project]
name = "Forward Roll"
repo_root = "repo"
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "specs").mkdir()

    directive = load_bootstrap_directive(config_path)

    assert directive.identity.name == "Forward Roll"
    assert directive.identity.repo_root == repo_root
    assert directive.specs_root == (tmp_path / "specs").resolve()
    assert directive.plans_root == (tmp_path / "planning").resolve()
    assert directive.host_asset_targets.skills_root == (tmp_path / "codex-skills").resolve()
    assert directive.host_asset_targets.agents_root == (tmp_path / "codex-agents").resolve()
    assert directive.active_target.task_id == "05-06"
    assert directive.values == ValueSet.default()

    summary = render_bootstrap_summary(directive)

    assert f"repo_root={repo_root}" in summary
    assert f"specs_root={(tmp_path / 'specs').resolve()}" in summary
    assert f"plans_root={(tmp_path / 'planning').resolve()}" in summary
    assert f"host_skills_root={(tmp_path / 'codex-skills').resolve()}" in summary
    assert f"host_agents_root={(tmp_path / 'codex-agents').resolve()}" in summary


def test_resolve_bootstrap_directive_applies_defaults(tmp_path: Path) -> None:
    repo_root = _write_repo_fixture(tmp_path / "repo")

    directive = resolve_bootstrap_directive(repo_root=repo_root)

    assert directive.identity.name == repo_root.name
    assert directive.specs_root == repo_root / "lat.md"
    assert directive.plans_root == repo_root / ".planning"
    assert directive.host_asset_targets.skills_root == repo_root / ".agents" / "skills"
    assert directive.host_asset_targets.agents_root == repo_root / ".codex" / "agents"
    assert directive.defaults_applied == (
        "specs_root",
        "plans_root",
        "host_skills_root",
        "host_agents_root",
        "project.name",
        "values",
    )
    assert directive.active_target.phase_document == "PHASE-05.md"


def test_resolve_bootstrap_directive_rejects_missing_specs_root(tmp_path: Path) -> None:
    repo_root = _write_repo_fixture(tmp_path / "repo")

    with pytest.raises(BootstrapConfigError, match="specs_root does not exist"):
        resolve_bootstrap_directive(repo_root=repo_root, specs_root=tmp_path / "missing-specs")


def test_resolve_bootstrap_directive_rejects_file_plans_root(tmp_path: Path) -> None:
    repo_root = _write_repo_fixture(tmp_path / "repo")
    invalid_plans_root = tmp_path / "plans.txt"
    invalid_plans_root.write_text("not a directory\n", encoding="utf-8")

    with pytest.raises(BootstrapConfigError, match="plans_root must be a directory"):
        resolve_bootstrap_directive(repo_root=repo_root, plans_root=invalid_plans_root)


def test_bootstrap_project_persists_artifacts_for_external_roots(tmp_path: Path) -> None:
    repo_root = _write_repo_fixture(tmp_path / "repo")
    specs_root = tmp_path / "external-specs"
    specs_root.mkdir()
    plans_root = tmp_path / "external-plans"
    host_skills_root = tmp_path / "user-codex" / "skills"
    host_agents_root = tmp_path / "user-codex" / "agents"

    directive = resolve_bootstrap_directive(
        repo_root=repo_root,
        specs_root=specs_root,
        plans_root=plans_root,
        host_skills_root=host_skills_root,
        host_agents_root=host_agents_root,
        project_name="External Planning Project",
    )

    artifacts = bootstrap_project(directive)

    assert {
        plans_root / "PROJECT.md",
        plans_root / "REQUIREMENTS.md",
        plans_root / "ROADMAP.md",
        plans_root / "STATE.md",
        plans_root / "PHASE-05.md",
    } <= set(artifacts.planning_files)
    assert {
        host_skills_root / "fr-plan-milestone" / "SKILL.md",
        host_agents_root / "fr-milestone-planning-orchestrator.md",
        host_agents_root / "fr-milestone-planner.md",
        host_agents_root / "fr-milestone-plan-checker.md",
    } == set(artifacts.host_assets)
    assert artifacts.context_path == plans_root / "bootstrap-context.json"
    assert artifacts.summary_path == plans_root / "BOOTSTRAP.md"

    context = json.loads(artifacts.context_path.read_text(encoding="utf-8"))
    assert context["project"]["name"] == "External Planning Project"
    assert context["project"]["repo_root"] == str(repo_root)
    assert context["specs_root"] == str(specs_root)
    assert context["plans_root"] == str(plans_root)
    assert context["host_assets"]["skills_root"] == str(host_skills_root)
    assert context["host_assets"]["agents_root"] == str(host_agents_root)
    assert set(context["host_assets"]["materialized"]) == {str(path) for path in artifacts.host_assets}
    assert context["active_target"]["task_id"] == "05-06"
    assert context["defaults_applied"] == ["values"]

    summary = artifacts.summary_path.read_text(encoding="utf-8")
    assert f"specs_root={specs_root}" in summary
    assert f"plans_root={plans_root}" in summary
    assert f"host_skills_root={host_skills_root}" in summary
    assert f"host_agents_root={host_agents_root}" in summary
    assert "active_task=05-06" in summary
    assert "materialized_host_assets=4" in summary

    skill_text = (host_skills_root / "fr-plan-milestone" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    skill_template_text = (
        Path("src/forward_roll/host_assets/skills/fr-plan-milestone/SKILL.md")
    ).read_text(encoding="utf-8")
    planner_text = (host_agents_root / "fr-milestone-planner.md").read_text(encoding="utf-8")
    assert "lat expand" in skill_text
    assert "lat search" in skill_text
    assert "lat locate" in skill_text
    assert "lat.md/workflow.md" not in skill_text
    assert "lat.md/architecture.md" not in skill_text
    assert "{{ project_file }}" in skill_template_text
    assert "{{ orchestrator_file }}" in skill_template_text
    assert "{{" not in skill_text
    assert "{{" not in planner_text
    assert "07-02" not in skill_text
    assert f"`{plans_root / 'PROJECT.md'}`" in skill_text
    assert f"`{plans_root / 'REQUIREMENTS.md'}`" in skill_text
    assert f"`{host_agents_root / 'fr-milestone-planning-orchestrator.md'}`" in skill_text
    assert f"`{plans_root / 'PROJECT.md'}`" in planner_text
    assert f"`{plans_root / 'ROADMAP.md'}`" in planner_text

    stale_skill_path = host_skills_root / "fr-plan-milestone" / "SKILL.md"
    stale_skill_path.write_text("stale\n", encoding="utf-8")

    refreshed_artifacts = bootstrap_project(directive)

    assert refreshed_artifacts.host_assets == artifacts.host_assets
    assert stale_skill_path.read_text(encoding="utf-8") == skill_text


def _write_repo_fixture(repo_root: Path) -> Path:
    repo_root.mkdir(parents=True)
    (repo_root / "lat.md").mkdir()
    planning_root = repo_root / ".planning"
    planning_root.mkdir()
    (planning_root / "PROJECT.md").write_text("# Project\n", encoding="utf-8")
    (planning_root / "REQUIREMENTS.md").write_text("# Requirements\n", encoding="utf-8")
    (planning_root / "STATE.md").write_text("# State\n", encoding="utf-8")
    (planning_root / "PHASE-05.md").write_text("# Phase 5\n", encoding="utf-8")
    (planning_root / "ROADMAP.md").write_text(
        """
# Roadmap

### Phase 5: First Executable Slice

Tasks:
- [ ] 05-06: Implement the executable bootstrap handoff.
- [ ] 05-07: Implement reusable prompt assets.
""".lstrip(),
        encoding="utf-8",
    )
    return repo_root.resolve()
