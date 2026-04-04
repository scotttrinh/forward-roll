#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

DEFAULT_TESTING_POSTURE = (
    "Prefer high-signal end-to-end validation first, property-based tests for "
    "invariants, and targeted unit tests only for narrow edge cases."
)


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
    parser = argparse.ArgumentParser(description="Create a Forward Roll slice artifact")
    parser.add_argument("epic_id", help="Epic identifier, for example 04")
    parser.add_argument("slice_id", help="Slice identifier within the epic, for example 02")
    parser.add_argument("slug", help="Slice slug")
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument("--goal", help="Goal of the next slice")
    parser.add_argument("--epic-slug", help="Epic slug used in the directory name")
    parser.add_argument("--why-now", help="Why this slice should happen now")
    parser.add_argument("--scope", action="append", help="In-scope boundary")
    parser.add_argument("--out-of-scope", action="append", help="Out-of-scope boundary")
    parser.add_argument("--file", action="append", help="Relevant file or system")
    parser.add_argument("--acceptance", action="append", help="Acceptance criterion")
    parser.add_argument("--validation", action="append", help="Validation requirement")
    parser.add_argument("--review-shape", help="Intended jj review shape")
    parser.add_argument("--stop-condition", help="Explicit stop condition")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = detect_repo_root(Path("."))
    runtime_path = (
        Path(args.runtime_path).resolve()
        if args.runtime_path
        else default_runtime_path(repo_root)
    )
    runtime = load_runtime(runtime_path)
    epic_slug = args.epic_slug or "[fill-in-epic-slug]"
    epic_dir = (
        Path(runtime_text(runtime, "plans_root"))
        / "epics"
        / f"{args.epic_id}-{epic_slug}"
    )
    target = epic_dir / "slices" / f"{args.slice_id}-{args.slug}.md"
    testing_posture = runtime.get("testing_posture", DEFAULT_TESTING_POSTURE)
    if not isinstance(testing_posture, str):
        testing_posture = DEFAULT_TESTING_POSTURE
    body = f"""# Slice {args.epic_id}-{args.slice_id}: {args.slug}

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- epic: {args.epic_id}
- slice: {args.epic_id}-{args.slice_id}
- status: planned
- epic_dir: {epic_dir}

## Goal

{args.goal or '[define the goal of the next bounded slice]'}

## Why Now

{args.why_now or '[explain why this slice should happen now]'}

## In Scope

{render_list(args.scope, "Describe what is in scope for this slice.")}

## Out Of Scope

{render_list(args.out_of_scope, "Describe what is explicitly out of scope for this slice.")}

## Relevant Files And Systems

{render_list(args.file, "List the likely files, modules, or systems touched by this slice.")}

## Acceptance Criteria

{render_list(args.acceptance, "Add concrete acceptance criteria for the slice.")}

## Validation Strategy

{render_list(args.validation, testing_posture)}

## jj Review Shape

{args.review_shape or (
    "Keep one readable change and fold local iteration into it with jj squash as "
    "needed."
)}

## Stop Condition

{args.stop_condition or '[state when the agent should stop and hand back the slice]'}

## Log

- {now_iso()} Planned slice artifact created.
"""
    write_text(target, body)
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
