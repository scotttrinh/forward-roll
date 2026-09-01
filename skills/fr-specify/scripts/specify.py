#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import cast


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def detect_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".jj").exists() or (candidate / ".git").exists():
            return candidate
    return current


def default_runtime_path(repo_root: Path) -> Path:
    return repo_root / ".forward-roll" / "runtime.json"


def load_runtime(runtime_path: Path) -> dict[str, object]:
    if not runtime_path.exists():
        raise SystemExit(
            "runtime contract not found at "
            f"{runtime_path}. Run bootstrap first or pass --runtime-path."
        )
    data = json.loads(runtime_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"runtime contract at {runtime_path} must be a JSON object")
    return cast(dict[str, object], data)


def runtime_text(runtime: dict[str, object], key: str) -> str:
    value = runtime.get(key)
    if not isinstance(value, str):
        raise SystemExit(f"runtime field '{key}' must be a string")
    return value


def render_list(items: list[str] | None, empty_value: str) -> str:
    values = [item for item in (items or []) if item]
    if not values:
        return f"- {empty_value}"
    return "\n".join(f"- {item}" for item in values)


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a Forward Roll specification work artifact or fast-track epic+slice"
    )
    parser.add_argument("slug", help="Specification work artifact or fast-track task name")
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument(
        "--mode",
        choices=["discover", "describe", "fast-track"],
        required=True,
        help="Specification mode (discover/describe for living spec dossiers, fast-track for inline bounded work)",
    )
    parser.add_argument("--goal", help="Specification or fast-track goal")
    parser.add_argument("--epic-id", default="01", help="Epic ID for fast-track mode (e.g. 01)")
    parser.add_argument("--spec", action="append", help="Relevant spec path or note")
    parser.add_argument("--code", action="append", help="Relevant code, entry points, or workspace facts")
    parser.add_argument("--current-state", action="append", help="Current system state / ground-truth research")
    parser.add_argument("--vector", action="append", help="Functionality under discussion / vector of change")
    parser.add_argument("--invariant", action="append", help="Durable invariant, constraint, or non-negotiable")
    parser.add_argument("--flow", action="append", help="User or operator flow")
    parser.add_argument("--standard", action="append", help="Standard or technical guidance")
    parser.add_argument("--acceptance", action="append", help="Acceptance criterion (for fast-track)")
    parser.add_argument("--file", action="append", help="Relevant file or system touched (for fast-track)")
    parser.add_argument("--validation", action="append", help="Validation requirement (for fast-track)")
    parser.add_argument("--archetype", default="feature", choices=["feature", "bugfix", "refactor", "perf", "visual-parity"], help="Slice archetype for fast-track")
    parser.add_argument("--question", action="append", help="Open question or finding")
    return parser


def generate_dossier(args: argparse.Namespace, runtime: dict[str, object], runtime_path: Path) -> Path:
    target = Path(runtime_text(runtime, "specs_root")) / "specify" / f"{args.slug}.md"
    current_state_items = (args.current_state or []) + (args.code or [])
    invariant_items = (args.invariant or []) + (args.standard or [])
    body = f"""# Specify: {args.slug}

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- repo_root: {runtime_text(runtime, "repo_root")}
- mode: {args.mode}
- goal: {args.goal or "[fill in the specification goal]"}

## Current State & Point-in-Time Ground Truth

{render_list(current_state_items, "Document entry points, current files/modules, actual data flows, known landmines, and test posture.")}

## Functionality Under Discussion / Vector of Change

{render_list(args.vector, "Describe the problem being solved, the target behavior, and the direction of travel.")}

## Invariants & Design Decisions

{render_list(invariant_items, "Capture architectural boundaries, non-negotiable constraints, and technical rules.")}

## Relevant Specs & Flows

{render_list(args.spec or args.flow, "List relevant spec references and key operator/user flows.")}

## Open Findings & Questions

{render_list(args.question, "List point-in-time discoveries, research findings, or open questions.")}
"""
    write_text(target, body)
    return target


def generate_fast_track(args: argparse.Namespace, runtime: dict[str, object], runtime_path: Path) -> tuple[Path, Path]:
    plans_root = Path(runtime_text(runtime, "plans_root"))
    epic_dir = plans_root / "epics" / f"{args.epic_id}-{args.slug}"
    epic_target = epic_dir / "EPIC.md"
    slice_target = epic_dir / "slices" / f"01-{args.slug}.md"

    testing_posture = runtime.get("testing_posture", "Run automated test suite and verify behavior.")
    if not isinstance(testing_posture, str):
        testing_posture = "Run automated test suite and verify behavior."

    epic_body = f"""# Epic {args.epic_id}: {args.slug} (Fast Track)

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- epic: {args.epic_id}
- slug: {args.slug}
- status: planned
- mode: fast-track

## Goal

{args.goal or '[state the fast-track deliverable]'}

## Why

- Fast-track bounded task formulated directly from discovery/brainstorming.

## Spec Impact

- implementation-only

## Definition Of Done

{render_list(args.acceptance, "All slice acceptance criteria met and verified cleanly.")}

## Slice Plan

- 01-{args.slug}: Execute fast-track implementation via fr-do
"""

    slice_body = f"""# Slice {args.epic_id}-01: {args.slug}

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- epic: {args.epic_id}
- slice: {args.epic_id}-01
- archetype: {args.archetype}
- status: planned
- epic_dir: {epic_dir}

## Goal

{args.goal or '[define the goal of the fast-track slice]'}

## Archetype

- {args.archetype}

## In Scope

{render_list(args.vector or [args.goal], "Bounded implementation of the requested task.")}

## Out Of Scope

- Unrelated refactoring or speculative features outside the immediate goal.

## Relevant Files And Systems

{render_list(args.file or args.code, "List files, modules, or systems touched by this fast-track slice.")}

## Acceptance Criteria

{render_list(args.acceptance, "Concrete acceptance criteria for this fast-track slice.")}

## Validation Strategy

{render_list(args.validation, testing_posture)}

## jj Review Shape

- Keep one readable atomic change and fold local iteration into it with jj squash.

## Stop Condition

- fr-review returns ship on slice acceptance criteria and clean test run.

## Log

- {now_iso()} Fast-track epic and slice artifacts created upfront.
"""
    write_text(epic_target, epic_body)
    write_text(slice_target, slice_body)
    return epic_target, slice_target


def main() -> int:
    args = build_parser().parse_args()
    repo_root = detect_repo_root(Path("."))
    runtime_path = (
        Path(args.runtime_path).resolve()
        if args.runtime_path
        else default_runtime_path(repo_root)
    )
    runtime = load_runtime(runtime_path)

    if args.mode == "fast-track":
        epic_path, slice_path = generate_fast_track(args, runtime, runtime_path)
        print(f"Fast-track epic created: {epic_path}")
        print(f"Fast-track slice created: {slice_path}")
    else:
        target = generate_dossier(args, runtime, runtime_path)
        print(target)

    return 0


if __name__ == "__main__":
    sys.exit(main())
