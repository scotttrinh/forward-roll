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


def render_list(items: list[str] | None, empty_value: str) -> str:
    values = [item for item in (items or []) if item]
    if not values:
        return f"- {empty_value}"
    return "\n".join(f"- {item}" for item in values)


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a Forward Roll epic review summary")
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument("--epic", required=True, help="Epic file to review")
    parser.add_argument("--implemented", action="append", help="What is implemented now")
    parser.add_argument("--accepted", action="append", help="Acceptance criteria satisfied")
    parser.add_argument("--validation", action="append", help="Validation that exists")
    parser.add_argument("--uncertainty", action="append", help="Remaining uncertainty")
    parser.add_argument("--follow-up", action="append", help="Follow-up implied by review")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = detect_repo_root(Path("."))
    runtime_path = (
        Path(args.runtime_path).resolve()
        if args.runtime_path
        else default_runtime_path(repo_root)
    )
    load_runtime(runtime_path)
    epic = Path(args.epic).resolve()
    if not epic.exists():
        raise SystemExit(f"epic file not found at {epic}")
    target = epic.parent / "reviews" / f"review-{now_iso().replace(':', '-')}.md"
    body = f"""# Review: {epic.parent.name}

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- epic: {epic}

## Intended Deliverable

Read the parent epic and compare its stated intent against the current implementation before finalizing this summary.

## Implemented Now

{render_list(args.implemented, "Summarize the user-visible and structural behavior that exists now.")}

## Acceptance Criteria Satisfied

{render_list(args.accepted, "Record the epic acceptance criteria that appear satisfied.")}

## Validation Evidence

{render_list(args.validation, "Record the validation that actually ran.")}

## Remaining Uncertainty

{render_list(args.uncertainty, "Name remaining uncertainty or follow-up risk.")}

## Follow-Up For Feedback

{render_list(args.follow_up, "State the follow-up work or artifact updates implied by this review.")}
"""
    write_text(target, body)
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
