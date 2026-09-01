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
    parser = argparse.ArgumentParser(description="Create a Forward Roll epic artifact")
    parser.add_argument("epic_id", help="Epic identifier, for example 04")
    parser.add_argument("slug", help="Epic slug")
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument("--status", default="planned", help="Epic status")
    parser.add_argument("--goal", help="Epic goal")
    parser.add_argument("--why", action="append", help="Why this epic matters")
    parser.add_argument(
        "--spec-impact",
        choices=["spec-update-required", "spec-already-covers-this", "implementation-only"],
        help="Whether and how this epic affects durable specs",
    )
    parser.add_argument("--current-shape", action="append", help="Current system shape")
    parser.add_argument("--proposed-shape", action="append", help="Proposed system shape")
    parser.add_argument("--code", action="append", help="Relevant code reference or boundary")
    parser.add_argument("--constraint", action="append", help="Constraint or risk")
    parser.add_argument("--done", action="append", help="Definition of done item")
    parser.add_argument("--acceptance", action="append", help="Epic acceptance criterion")
    parser.add_argument("--manual-check", action="append", help="Manual verification step")
    parser.add_argument("--slice", action="append", help="Initial slice breakdown item")
    parser.add_argument("--question", action="append", help="Open question")
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
    epic_dir = Path(runtime_text(runtime, "plans_root")) / "epics" / f"{args.epic_id}-{args.slug}"
    target = epic_dir / "EPIC.md"
    body = f"""# Epic {args.epic_id}: {args.slug}

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- epic: {args.epic_id}
- slug: {args.slug}
- status: {args.status}

## Goal

{args.goal or '[state the reviewable deliverable this epic should achieve]'}

## Why

{render_list(args.why, "Explain why this change matters now.")}

## Spec Impact

- {args.spec_impact or 'Decide explicitly whether specs must change, already cover this, or are unaffected.'}

## Existing System Shape

{render_list(args.current_shape, "Describe the relevant current implementation shape and boundaries.")}

## Proposed Change Shape

{render_list(args.proposed_shape, "Describe the intended new system shape for this epic.")}

## Relevant Code References

{render_list(args.code, "Link relevant files, modules, or system boundaries.")}

## Constraints And Risks

{render_list(args.constraint, "Capture important constraints, dependencies, and likely risks.")}

## Definition Of Done

{render_list(args.done, "State what must be true for this epic to count as done.")}

## Acceptance Criteria

{render_list(args.acceptance, "Add concrete acceptance criteria for the epic.")}

## Manual Verification

{render_list(args.manual_check, "Describe how a human can manually verify the epic outcome.")}

## Slice Plan

{render_list(args.slice, "List the initial bounded slices that make up this epic.")}

## Open Questions

{render_list(args.question, "Capture unresolved questions that matter for the epic.")}
"""
    write_text(target, body)
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
