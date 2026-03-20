"""Validation for the current knowledge-graph slice."""
# @lat: [[domain#Knowledge Graph Validation]]

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = REPO_ROOT / "lat.md"
SECTION_PATTERN = re.compile(r"^##\s+(?P<section>.+)$", re.MULTILINE)
CODE_REF_PATTERN = re.compile(r"\[\[(?P<path>(?:src|tests)/[^\]]+)\]\]")
LAT_BACKLINK_PATTERN = re.compile(r"@lat:\s+\[\[(?P<target>[^\]]+)\]\]")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_knowledge_graph_covers_current_bootstrap_slice() -> None:
    docs = {
        "architecture": _read_text(DOC_ROOT / "architecture.md"),
        "domain": _read_text(DOC_ROOT / "domain.md"),
        "workflow": _read_text(DOC_ROOT / "workflow.md"),
    }

    expected_sections = {
        "architecture": {
            "Domain Layer",
            "Application Layer",
            "Adapter Layer",
            "CLI Adapter",
        },
        "domain": {
            "Project Identity",
            "Bootstrap Directive",
            "Value Set",
            "Planning Root",
            "Knowledge Graph Validation",
        },
        "workflow": {
            "Bootstrap Config Loading",
            "Bootstrap Summary Rendering",
            "Bootstrap Command",
        },
    }
    expected_code_refs = {
        "src/forward_roll/domain/model.py",
        "src/forward_roll/application/bootstrap.py",
        "src/forward_roll/application/prompts.py",
        "src/forward_roll/application/phase_launch.py",
        "src/forward_roll/adapters/bootstrap_config.py",
        "src/forward_roll/cli.py",
        "tests/test_bootstrap_config.py",
        "tests/test_phase_launch.py",
        "tests/test_lat_knowledge_graph.py",
    }
    expected_backlinks = {
        "src/forward_roll/domain/model.py": {
            "domain#Project Identity",
            "domain#Bootstrap Directive",
            "domain#Value Set",
            "domain#Planning Root",
        },
        "src/forward_roll/application/bootstrap.py": {
            "architecture#Application Layer",
            "workflow#Bootstrap Summary Rendering",
        },
        "src/forward_roll/application/prompts.py": {
            "architecture#Workflow Prompt Assets",
            "workflow#Workflow Prompt Templates",
        },
        "src/forward_roll/application/phase_launch.py": {
            "architecture#Application Layer",
            "workflow#Phase Launch Contract",
        },
        "src/forward_roll/adapters/bootstrap_config.py": {
            "architecture#Adapter Layer",
            "workflow#Bootstrap Config Loading",
        },
        "src/forward_roll/cli.py": {
            "architecture#CLI Adapter",
            "workflow#Bootstrap Command",
            "workflow#Phase Launch Contract",
        },
        "tests/test_bootstrap_config.py": {
            "domain#Testing Philosophy",
            "workflow#Bootstrap Config Loading",
            "workflow#Bootstrap Summary Rendering",
        },
        "tests/test_phase_launch.py": {
            "domain#Testing Philosophy",
            "workflow#Workflow Prompt Templates",
            "workflow#Phase Launch Contract",
        },
        "tests/test_lat_knowledge_graph.py": {
            "domain#Knowledge Graph Validation",
        },
    }

    for name, expected in expected_sections.items():
        found = set(SECTION_PATTERN.findall(docs[name]))
        assert expected <= found

    found_code_refs = set()
    for contents in docs.values():
        found_code_refs.update(CODE_REF_PATTERN.findall(contents))
    assert expected_code_refs <= found_code_refs

    for relative_path, expected in expected_backlinks.items():
        backlinks = set(LAT_BACKLINK_PATTERN.findall(_read_text(REPO_ROOT / relative_path)))
        assert expected <= backlinks
