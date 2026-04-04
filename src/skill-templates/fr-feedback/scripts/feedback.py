#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

ALLOWED_FEEDBACK_OUTCOMES = [
    "accept",
    "adjust-spec",
    "adjust-epic",
    "adjust-slice",
    "queue-follow-up",
]


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
    parser = argparse.ArgumentParser(description="Create a Forward Roll feedback artifact")
    parser.add_argument("epic_id", help="Epic identifier, for example 04")
    parser.add_argument("slug", help="Feedback artifact name")
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument(
        "--scope",
        required=True,
        choices=["spec", "epic", "slice", "follow-up"],
        help="Artifact layer primarily affected by this feedback",
    )
    parser.add_argument("--epic-slug", help="Epic slug used in the directory name")
    parser.add_argument("--outcome", required=True, choices=ALLOWED_FEEDBACK_OUTCOMES)
    parser.add_argument("--note", action="append", help="Operator feedback note")
    parser.add_argument("--next-action", action="append", help="Single next durable action")
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
    target = (
        Path(runtime_text(runtime, "plans_root"))
        / "epics"
        / f"{args.epic_id}-{epic_slug}"
        / "feedback"
        / f"{now_iso().replace(':', '-')}-{args.slug}.md"
    )
    body = f"""# Feedback: {args.slug}

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- epic: {args.epic_id}
- scope: {args.scope}
- outcome: {args.outcome}

## Input

{render_list(args.note, "Capture the operator feedback that drove this decision.")}

## Required Next Action

{render_list(args.next_action, "State the single next durable action implied by this outcome.")}
"""
    write_text(target, body)
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
