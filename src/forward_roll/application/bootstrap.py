"""Application services for bootstrap-oriented workflows."""
# @lat: [[architecture#Primary Layers]]
# @lat: [[workflow#Bootstrap Flow]]

from __future__ import annotations

from forward_roll.domain.model import BootstrapDirective


def render_bootstrap_summary(directive: BootstrapDirective) -> str:
    """Render a concise bootstrap summary from a typed directive."""
    architecture_headline = directive.values.architecture[0]
    vcs_headline = directive.values.version_control[0]
    return "\n".join(
        [
            f"project={directive.identity.name}",
            f"repo_root={directive.identity.repo_root}",
            f"planning_root={directive.planning_root}",
            f"architecture={architecture_headline}",
            f"version_control={vcs_headline}",
        ]
    )
