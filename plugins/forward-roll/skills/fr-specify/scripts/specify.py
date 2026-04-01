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
        description="Create a Forward Roll specification work artifact"
    )
    parser.add_argument("slug", help="Specification work artifact name")
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument("--mode", choices=["discover", "describe"], required=True)
    parser.add_argument("--goal", help="Specification goal")
    parser.add_argument("--spec", action="append", help="Relevant spec path or note")
    parser.add_argument("--code", action="append", help="Relevant code or workspace fact")
    parser.add_argument("--constraint", action="append", help="Constraint to record")
    parser.add_argument("--flow", action="append", help="User or operator flow")
    parser.add_argument("--standard", action="append", help="Standard or technical guidance")
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
    target = Path(runtime_text(runtime, "specs_root")) / "specify" / f"{args.slug}.md"
    body = f"""# Specify: {args.slug}

## Metadata

- created_at: {now_iso()}
- runtime: {runtime_path}
- repo_root: {runtime_text(runtime, "repo_root")}
- mode: {args.mode}
- goal: {args.goal or "[fill in the specification goal]"}

## Relevant Specs

{render_list(args.spec, "List the durable spec documents that matter for this work.")}

## Code And Workspace Context

{render_list(args.code, "Summarize the relevant files, modules, and current workspace facts.")}

## Constraints

{render_list(args.constraint, "Capture architecture, workflow, or runtime constraints.")}

## Flows

{render_list(args.flow, "Describe the important user or operator flows.")}

## Standards And Guidance

{render_list(
    args.standard,
    "Record codebase standards, technical guidance, or architectural rules.",
)}

## Open Questions

{render_list(args.question, "List unresolved questions that matter for durable specs.")}
"""
    write_text(target, body)
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
