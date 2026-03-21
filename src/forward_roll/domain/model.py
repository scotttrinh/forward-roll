"""Domain model for bootstrapping Forward Roll workflows."""
# @lat: [[domain#Core Domain]]
# @lat: [[domain#Project Identity]]
# @lat: [[domain#Bootstrap Directive]]
# @lat: [[domain#Value Set]]
# @lat: [[domain#Planning Root]]

from __future__ import annotations

from pathlib import Path

from attrs import field, frozen


@frozen
class ProjectIdentity:
    """Stable identity for the repository being operated on."""

    name: str = field()
    repo_root: Path

    def __attrs_post_init__(self) -> None:
        if not self.name:
            msg = "project name must not be empty"
            raise ValueError(msg)


@frozen
class ValueSet:
    """Default principles that drive Forward Roll decisions."""

    architecture: tuple[str, ...]
    tests: tuple[str, ...]
    typing: tuple[str, ...]
    phase_verification: tuple[str, ...]
    version_control: tuple[str, ...]
    communication: tuple[str, ...]

    @classmethod
    def default(cls) -> ValueSet:
        return cls(
            architecture=(
                "Prefer ports-and-adapters, hexagonal, or clean architecture.",
                "Favor composition over inheritance.",
                "Use DDD to model the domain before implementation details.",
                "Optimize for software craftsmanship rather than speed shortcuts.",
            ),
            tests=(
                "Write phase tests first when that clarifies intent.",
                "Prefer strict types over excess tests.",
                "Prefer end-to-end happy-path coverage over heavily mocked unit tests.",
                "Use property-based tests for invariants.",
                "Delete low-value tests created only as temporary scaffolding.",
            ),
            typing=(
                "Adopt the strictest practical typing posture.",
                "Design domain types and interfaces during planning, not after coding starts.",
            ),
            phase_verification=(
                "Treat post-phase review as a mandatory alignment step.",
                "Use review feedback to refine specs, not as throwaway commentary.",
            ),
            version_control=(
                "Lean into jj idioms and automatic change tracking.",
                "Document specialized jj workflows explicitly for agents and reviewers.",
            ),
            communication=(
                "Prefer output that is human-legible and reviewer-friendly.",
                "Keep specs and knowledge graph documents readable without tool-specific context.",
            ),
        )


@frozen
class ActivePlanningTarget:
    """Active phase/task metadata derived from durable planning artifacts."""

    phase_id: str
    phase_name: str
    phase_document: str
    task_id: str
    task_title: str


@frozen
class HostAssetTargets:
    """Resolved host-visible skill and agent target directories."""

    skills_root: Path
    agents_root: Path


@frozen
class BootstrapDirective:
    """Typed bootstrap input for the executable bootstrap handoff."""

    identity: ProjectIdentity
    specs_root: Path
    plans_root: Path
    host_asset_targets: HostAssetTargets
    values: ValueSet
    active_target: ActivePlanningTarget
    defaults_applied: tuple[str, ...] = field(factory=tuple)
