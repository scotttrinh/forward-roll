"""CLI entry points for Forward Roll."""
# @lat: [[workflow#Bootstrap Command]]
# @lat: [[workflow#Phase Launch Contract]]
# @lat: [[architecture#CLI Adapter]]

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from forward_roll import __version__
from forward_roll.adapters.bootstrap_config import (
    BootstrapConfigError,
    load_bootstrap_directive,
    resolve_bootstrap_directive,
)
from forward_roll.application.bootstrap import (
    BootstrapApplicationError,
    bootstrap_project,
    render_bootstrap_summary,
)
from forward_roll.application.phase_launch import (
    PhaseLaunchError,
    UnavailableExecutionRunner,
    launch_phase,
)

app = typer.Typer(
    no_args_is_help=True,
    help="Codex-first workflow tooling with jj-native ergonomics.",
)


def version_callback(value: bool) -> None:
    """Print the package version and exit."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the Forward Roll version and exit.",
    ),
) -> None:
    """Forward Roll CLI root."""


@app.command()
def bootstrap(
    repo_root: Annotated[
        Path,
        typer.Argument(
            resolve_path=True,
            help="Repository root to target.",
        ),
    ] = Path("."),
    specs_root: Annotated[
        Path | None,
        typer.Option(
            "--specs-root",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Specification root. Defaults to repo_root/lat.md.",
        ),
    ] = None,
    plans_root: Annotated[
        Path | None,
        typer.Option(
            "--plans-root",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help=(
                "Planning workspace. Defaults to repo_root/.planning and may "
                "live outside the target repository."
            ),
        ),
    ] = None,
    host_skills_root: Annotated[
        Path | None,
        typer.Option(
            "--host-skills-root",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help=(
                "Host skill target directory. Defaults to repo_root/.agents/skills and "
                "may point at a user-local Codex skills directory."
            ),
        ),
    ] = None,
    host_agents_root: Annotated[
        Path | None,
        typer.Option(
            "--host-agents-root",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help=(
                "Host agent target directory. Defaults to repo_root/.codex/agents and "
                "may point at a user-local Codex agents directory."
            ),
        ),
    ] = None,
    project_name: Annotated[
        str | None,
        typer.Option(
            "--project-name",
            help="Project identity override. Defaults to the repository directory name.",
        ),
    ] = None,
    config: Annotated[
        Path | None,
        typer.Option(
            "--config",
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
            help="Load bootstrap inputs from a TOML config file.",
        ),
    ] = None,
) -> None:
    """Resolve and persist the executable bootstrap handoff artifacts."""
    if config is not None:
        try:
            directive = load_bootstrap_directive(config)
        except BootstrapConfigError as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(code=1) from exc
    else:
        try:
            directive = resolve_bootstrap_directive(
                repo_root=repo_root,
                specs_root=specs_root,
                plans_root=plans_root,
                host_skills_root=host_skills_root,
                host_agents_root=host_agents_root,
                project_name=project_name,
            )
        except BootstrapConfigError as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(code=1) from exc

    try:
        artifacts = bootstrap_project(directive)
    except BootstrapApplicationError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(render_bootstrap_summary(directive, host_assets=artifacts.host_assets))
    typer.echo(f"context_path={artifacts.context_path}")
    typer.echo(f"summary_path={artifacts.summary_path}")


@app.command("launch-phase")
def launch_phase_command(
    plans_root: Annotated[
        Path,
        typer.Option(
            "--plans-root",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Planning workspace containing bootstrap-context.json.",
        ),
    ] = Path(".planning"),
    phase: Annotated[
        str | None,
        typer.Option(
            "--phase",
            help=(
                "Optional explicit phase selector. Defaults to the active phase "
                "in bootstrap context."
            ),
        ),
    ] = None,
) -> None:
    """Launch the active phase through the serial execution boundary."""
    try:
        result = launch_phase(
            plans_root=plans_root,
            phase_selector=phase,
            runner=UnavailableExecutionRunner(),
        )
    except PhaseLaunchError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"phase_id={result.phase_id}")
    typer.echo(f"completed_tasks={','.join(result.completed_tasks) or '(none)'}")
    typer.echo(f"stopped_task={result.stopped_task or '(none)'}")
    typer.echo(
        "review_outcome="
        + ("(none)" if result.review_result is None else result.review_result.outcome)
    )


if __name__ == "__main__":
    app()
