"""Focused tests for the milestone-planning skill contract."""
# @lat: [[domain#Testing Philosophy]]
# @lat: [[workflow#Milestone Planning Command]]

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_phase_07_contract_defines_the_skill_boundary() -> None:
    phase_text = _read_text(".planning/PHASE-07.md")

    assert "### Task 07-01: `$fr-plan-milestone` skill contract" in phase_text
    assert ".agents/skills/fr-plan-milestone/SKILL.md" in phase_text
    assert "Phase `07-02` owns that boundary." in phase_text
    assert "Run `uv run pytest`." in phase_text
    assert "Run `lat check`." in phase_text


def test_fr_plan_milestone_skill_covers_required_artifacts_and_guards() -> None:
    skill_text = _read_text(".agents/skills/fr-plan-milestone/SKILL.md")

    required_fragments = {
        "$fr-plan-milestone",
        "PROJECT.md",
        "REQUIREMENTS.md",
        "ROADMAP.md",
        "STATE.md",
        "lat expand",
        "lat search",
        "lat locate",
        "lat check",
        "Do not accept a phase selector or milestone-local phase number.",
        "Do not invent specialized milestone-planning roles here; Phase `07-02` owns that boundary.",
    }

    for fragment in required_fragments:
        assert fragment in skill_text


def test_phase_7_planning_artifacts_advance_to_the_next_task() -> None:
    roadmap_text = _read_text(".planning/ROADMAP.md")
    state_text = _read_text(".planning/STATE.md")

    assert "**Task Contracts**: [Phase 7 task contracts](./PHASE-07.md)" in roadmap_text
    assert "- [x] 07-01: Define and implement the `$fr-plan-milestone` skill contract." in roadmap_text
    assert "Task: 07-02 of 3 in current phase" in state_text
    assert "Completed task `07-01`" in state_text
