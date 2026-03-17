"""CLI entry points for Forward Roll."""
# @lat: [[workflow#Bootstrap Flow]]
# @lat: [[architecture#Primary Layers]]

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from forward_roll import __version__
from forward_roll.adapters.bootstrap_config import BootstrapConfigError, load_bootstrap_directive
from forward_roll.application.bootstrap import render_bootstrap_summary
from forward_roll.domain.model import BootstrapDirective, ProjectIdentity, ValueSet

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
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Repository root to target.",
        ),
    ] = Path("."),
    planning_root: Annotated[
        Path,
        typer.Option(
            "--planning-root",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Planning workspace. This may live outside the target repository.",
        ),
    ] = Path(".planning"),
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
    """Render the current bootstrap assumptions as a typed domain object."""
    if config is not None:
        try:
            directive = load_bootstrap_directive(config)
        except BootstrapConfigError as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(code=1) from exc
    else:
        directive = BootstrapDirective(
            identity=ProjectIdentity(name="Forward Roll", repo_root=repo_root),
            planning_root=planning_root,
            values=ValueSet.default(),
        )

    typer.echo(render_bootstrap_summary(directive))


if __name__ == "__main__":
    app()
