"""Focused tests for the milestone-planning skill contract."""
# @lat: [[domain#Testing Philosophy]]
# @lat: [[workflow#Milestone Planning Command]]

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_phase_07_contract_defines_the_skill_and_role_boundaries() -> None:
    phase_text = _read_text(".planning/PHASE-07.md")

    assert "### Task 07-01: `$fr-plan-milestone` skill contract" in phase_text
    assert "### Task 07-02: milestone-planning orchestrator and supporting roles" in phase_text
    assert ".agents/skills/fr-plan-milestone/SKILL.md" in phase_text
    assert ".codex/agents/fr-milestone-planning-orchestrator.md" in phase_text
    assert ".codex/agents/fr-milestone-planner.md" in phase_text
    assert ".codex/agents/fr-milestone-plan-checker.md" in phase_text
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
        ".codex/agents/fr-milestone-planning-orchestrator.md",
        ".codex/agents/fr-milestone-planner.md",
        ".codex/agents/fr-milestone-plan-checker.md",
    }

    for fragment in required_fragments:
        assert fragment in skill_text

    assert "lat.md/workflow.md" not in skill_text
    assert "lat.md/architecture.md" not in skill_text


def test_milestone_planning_role_descriptors_cover_orchestration_and_review() -> None:
    orchestrator_text = _read_text(".codex/agents/fr-milestone-planning-orchestrator.md")
    planner_text = _read_text(".codex/agents/fr-milestone-planner.md")
    checker_text = _read_text(".codex/agents/fr-milestone-plan-checker.md")

    assert "fr-milestone-planner" in orchestrator_text
    assert "fr-milestone-plan-checker" in orchestrator_text
    assert "PROJECT.md" in planner_text
    assert "REQUIREMENTS.md" in planner_text
    assert "ROADMAP.md" in planner_text
    assert "STATE.md" in planner_text
    assert "`lat`-resolved" in orchestrator_text
    assert "`lat`-resolved" in planner_text
    assert "`lat`-resolved" in checker_text
    assert "phase planning" in checker_text
    assert "feedback-extension" in checker_text
    assert "lat check" in checker_text


def test_phase_7_planning_artifacts_close_phase_7_and_advance_to_phase_8() -> None:
    roadmap_text = _read_text(".planning/ROADMAP.md")
    state_text = _read_text(".planning/STATE.md")

    assert "**Task Contracts**: [Phase 7 task contracts](./PHASE-07.md)" in roadmap_text
    assert "- [x] 07-01: Define and implement the `$fr-plan-milestone` skill contract." in roadmap_text
    assert "- [x] 07-02: Define the milestone-planning orchestrator and supporting agent roles." in roadmap_text
    assert (
        "- [x] 07-03: Add templated bootstrap support for the milestone-planning skill family "
        "and indirect `lat`-based spec resolution."
    ) in roadmap_text
    assert "| 7. Milestone Planning Bootstrap | 3/3 | Complete | 2026-03-21 |" in roadmap_text
    assert "Phase 8 - Minimal Self-Hosting Templates (08-01 ready for execution)" in state_text
    assert "Task: 08-01 of 3 in current phase" in state_text
    assert "Completed `07-03`" in state_text
