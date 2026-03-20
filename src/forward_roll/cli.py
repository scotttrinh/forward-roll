"""CLI entry points for Forward Roll."""
# @lat: [[workflow#Bootstrap Command]]
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
            help="Planning workspace. Defaults to repo_root/.planning and may live outside the target repository.",
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

    typer.echo(render_bootstrap_summary(directive))
    typer.echo(f"context_path={artifacts.context_path}")
    typer.echo(f"summary_path={artifacts.summary_path}")


if __name__ == "__main__":
    app()
