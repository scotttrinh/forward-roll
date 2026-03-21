"""Application services for bootstrap-oriented workflows."""
# @lat: [[architecture#Application Layer]]
# @lat: [[workflow#Bootstrap Summary Rendering]]
# @lat: [[workflow#Plugin-First Self-Hosting#Bootstrap Skill And Runtime Config]]

from __future__ import annotations

from importlib import resources
import json
import re
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
    host_assets: tuple[Path, ...]


class BootstrapApplicationError(Exception):
    """Raised when bootstrap cannot persist its durable handoff artifacts."""

    pass


_HOST_ASSET_TEMPLATE_TOKEN = re.compile(r"{{\s*([a-z0-9_]+)\s*}}")


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
        "REQUIREMENTS.md",
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

    written_host_assets = _refresh_milestone_planning_host_assets(directive)
    context_path = directive.plans_root / "bootstrap-context.json"
    summary_path = directive.plans_root / "BOOTSTRAP.md"
    try:
        context_path.write_text(
            _render_bootstrap_context_json(directive, host_assets=written_host_assets),
            encoding="utf-8",
        )
        summary_path.write_text(
            render_bootstrap_summary(directive, host_assets=written_host_assets),
            encoding="utf-8",
        )
    except OSError as exc:
        msg = f"failed to persist bootstrap artifacts in {directive.plans_root}"
        raise BootstrapApplicationError(msg) from exc

    return BootstrapArtifacts(
        context_path=context_path,
        summary_path=summary_path,
        planning_files=written_planning_files,
        host_assets=written_host_assets,
    )


def render_bootstrap_summary(
    directive: BootstrapDirective,
    *,
    host_assets: tuple[Path, ...] = (),
) -> str:
    """Render a concise bootstrap summary from a typed directive."""
    defaults = ", ".join(directive.defaults_applied) if directive.defaults_applied else "(none)"
    lines = [
        "# Bootstrap Summary",
        "",
        f"project={directive.identity.name}",
        f"repo_root={directive.identity.repo_root}",
        f"specs_root={directive.specs_root}",
        f"plans_root={directive.plans_root}",
        f"host_skills_root={directive.host_asset_targets.skills_root}",
        f"host_agents_root={directive.host_asset_targets.agents_root}",
        f"defaults_applied={defaults}",
        f"active_phase={directive.active_target.phase_id}",
        f"active_phase_name={directive.active_target.phase_name}",
        f"active_phase_document={directive.active_target.phase_document}",
        f"active_task={directive.active_target.task_id}",
        f"active_task_title={directive.active_target.task_title}",
        f"materialized_host_assets={len(host_assets)}",
    ]
    lines.extend(f"host_asset={host_asset}" for host_asset in host_assets)
    return "\n".join(lines)


def _refresh_planning_file(*, source_path: Path, target_path: Path) -> Path:
    if not source_path.exists() or not source_path.is_file():
        msg = f"required planning artifact is missing: {source_path}"
        raise BootstrapApplicationError(msg)
    if source_path == target_path:
        return target_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    return target_path


def _refresh_milestone_planning_host_assets(directive: BootstrapDirective) -> tuple[Path, ...]:
    template_root = resources.files("forward_roll.host_assets")
    template_context = _build_host_asset_template_context(directive)
    written_assets: list[Path] = []

    for asset_group, relative_parts in (
        ("skills", ("fr-plan-milestone", "SKILL.md")),
        ("agents", ("fr-milestone-planning-orchestrator.md",)),
        ("agents", ("fr-milestone-planner.md",)),
        ("agents", ("fr-milestone-plan-checker.md",)),
    ):
        if asset_group == "skills":
            target_path = directive.host_asset_targets.skills_root.joinpath(*relative_parts)
        else:
            target_path = directive.host_asset_targets.agents_root.joinpath(*relative_parts)
        template_text = template_root.joinpath(asset_group, *relative_parts).read_text(
            encoding="utf-8"
        )
        rendered_text = _render_host_asset_template(
            template_text=template_text,
            template_context=template_context,
        )
        written_assets.append(_refresh_text_file(target_path=target_path, content=rendered_text))

    return tuple(written_assets)


def _build_host_asset_template_context(directive: BootstrapDirective) -> dict[str, str]:
    repo_root = directive.identity.repo_root
    plans_root = directive.plans_root
    skills_root = directive.host_asset_targets.skills_root
    agents_root = directive.host_asset_targets.agents_root
    return {
        "plans_root": _render_host_asset_path(path=plans_root, repo_root=repo_root),
        "host_skills_root": _render_host_asset_path(path=skills_root, repo_root=repo_root),
        "host_agents_root": _render_host_asset_path(path=agents_root, repo_root=repo_root),
        "project_file": _render_host_asset_path(path=plans_root / "PROJECT.md", repo_root=repo_root),
        "requirements_file": _render_host_asset_path(
            path=plans_root / "REQUIREMENTS.md",
            repo_root=repo_root,
        ),
        "roadmap_file": _render_host_asset_path(path=plans_root / "ROADMAP.md", repo_root=repo_root),
        "state_file": _render_host_asset_path(path=plans_root / "STATE.md", repo_root=repo_root),
        "skill_file": _render_host_asset_path(
            path=skills_root / "fr-plan-milestone" / "SKILL.md",
            repo_root=repo_root,
        ),
        "orchestrator_file": _render_host_asset_path(
            path=agents_root / "fr-milestone-planning-orchestrator.md",
            repo_root=repo_root,
        ),
        "planner_file": _render_host_asset_path(
            path=agents_root / "fr-milestone-planner.md",
            repo_root=repo_root,
        ),
        "checker_file": _render_host_asset_path(
            path=agents_root / "fr-milestone-plan-checker.md",
            repo_root=repo_root,
        ),
    }


def _render_host_asset_path(*, path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


def _render_host_asset_template(
    *,
    template_text: str,
    template_context: dict[str, str],
) -> str:
    missing_tokens: set[str] = set()

    def replace_token(match: re.Match[str]) -> str:
        token = match.group(1)
        if token not in template_context:
            missing_tokens.add(token)
            return match.group(0)
        return template_context[token]

    rendered_text = _HOST_ASSET_TEMPLATE_TOKEN.sub(replace_token, template_text)
    if missing_tokens:
        missing = ", ".join(sorted(missing_tokens))
        msg = f"host asset template references undefined variable(s): {missing}"
        raise BootstrapApplicationError(msg)
    return rendered_text


def _refresh_text_file(*, target_path: Path, content: str) -> Path:
    if target_path.exists() and not target_path.is_file():
        msg = f"host asset target must be a file path: {target_path}"
        raise BootstrapApplicationError(msg)
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if target_path.exists() and target_path.read_text(encoding="utf-8") == content:
            return target_path
        target_path.write_text(content, encoding="utf-8")
    except OSError as exc:
        msg = f"failed to materialize host asset: {target_path}"
        raise BootstrapApplicationError(msg) from exc
    return target_path


def _render_bootstrap_context_json(
    directive: BootstrapDirective,
    *,
    host_assets: tuple[Path, ...],
) -> str:
    context = {
        "project": {
            "name": directive.identity.name,
            "repo_root": str(directive.identity.repo_root),
        },
        "specs_root": str(directive.specs_root),
        "plans_root": str(directive.plans_root),
        "host_assets": {
            "skills_root": str(directive.host_asset_targets.skills_root),
            "agents_root": str(directive.host_asset_targets.agents_root),
            "materialized": [str(host_asset) for host_asset in host_assets],
        },
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
