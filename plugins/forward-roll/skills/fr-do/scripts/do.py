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


def render_log_items(items: list[str] | None, empty_value: str) -> str:
    values = [item for item in (items or []) if item]
    if not values:
        return f"  - {empty_value}"
    return "\n".join(f"  - {item}" for item in values)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Append a Forward Roll slice log entry")
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument("--slice", required=True, help="Slice file to update")
    parser.add_argument("--status", help="Updated slice status")
    parser.add_argument("--summary", required=True, help="End-of-run summary")
    parser.add_argument("--change", action="append", help="Change completed during the run")
    parser.add_argument("--validation", action="append", help="Validation run during the execution")
    parser.add_argument("--blocker", action="append", help="Blocker or unresolved risk")
    parser.add_argument("--next-step", action="append", help="Likely next step for this slice")
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
    target = Path(args.slice).resolve()
    if not target.exists():
        raise SystemExit(f"slice file not found at {target}")
    existing = target.read_text(encoding="utf-8").rstrip() + "\n"
    if args.status:
        lines = existing.splitlines()
        updated = False
        for index, line in enumerate(lines):
            if line.startswith("- status: "):
                lines[index] = f"- status: {args.status}"
                updated = True
                break
        if not updated:
            for index, line in enumerate(lines):
                if line == "## Metadata":
                    lines.insert(index + 1, f"- status: {args.status}")
                    updated = True
                    break
        existing = "\n".join(lines).rstrip() + "\n"
    if "## Log" not in existing:
        existing += "\n## Log\n"
    entry = f"""
- {now_iso()} {args.summary}
{render_log_items(args.change, "No detailed change summary recorded.")}
{render_log_items(args.validation, "Validation not recorded for this run.")}
{render_log_items(args.blocker, "No blockers recorded.")}
{render_log_items(args.next_step, "No next step recorded.")}
""".rstrip()
    target.write_text(existing.rstrip() + "\n\n" + entry + "\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
