#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast


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


def runtime_dict(runtime: dict[str, object], key: str) -> dict[str, object]:
    value = runtime.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"runtime field '{key}' must be an object")
    return cast(dict[str, object], value)


def relative_to_root(path: Path, repo_root: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(repo_root.resolve()))
    except ValueError:
        return str(resolved)


def list_markdown_files(root: Path, repo_root: Path) -> list[dict[str, str]]:
    if not root.exists():
        return []
    return [
        {
            "path": str(path.resolve()),
            "relative_path": relative_to_root(path, repo_root),
        }
        for path in sorted(root.rglob("*.md"))
        if path.is_file()
    ]


def parse_epic_dir(epic_dir: Path) -> tuple[str, str]:
    name = epic_dir.name
    if "-" not in name:
        return name, ""
    epic_id, slug = name.split("-", 1)
    return epic_id, slug


def resolve_slice_key(epic_id: str | None, slice_id: str | None) -> tuple[str | None, str | None]:
    if slice_id and "-" in slice_id:
        parsed_epic_id, parsed_slice_id = slice_id.split("-", 1)
        return epic_id or parsed_epic_id, parsed_slice_id
    return epic_id, slice_id


def match_epic_dir(epic_dir: Path, epic_id: str | None) -> bool:
    if epic_id is None:
        return True
    return epic_dir.name == epic_id or epic_dir.name.startswith(f"{epic_id}-")


def match_slice_file(path: Path, slice_id: str | None) -> bool:
    if slice_id is None:
        return True
    return path.name == slice_id or path.name.startswith(f"{slice_id}-")


def epic_payload(epic_dir: Path, repo_root: Path) -> dict[str, Any]:
    epic_id, epic_slug = parse_epic_dir(epic_dir)
    epic_file = epic_dir / "EPIC.md"
    slices_dir = epic_dir / "slices"
    feedback_dir = epic_dir / "feedback"
    reviews_dir = epic_dir / "reviews"
    return {
        "epic_id": epic_id,
        "epic_slug": epic_slug,
        "epic_dir": str(epic_dir.resolve()),
        "epic_file": str(epic_file.resolve()) if epic_file.exists() else None,
        "relative_epic_dir": relative_to_root(epic_dir, repo_root),
        "slice_files": list_markdown_files(slices_dir, repo_root),
        "feedback_files": list_markdown_files(feedback_dir, repo_root),
        "review_files": list_markdown_files(reviews_dir, repo_root),
    }


def filtered_epics(
    plans_root: Path, repo_root: Path, epic_id: str | None, slice_id: str | None
) -> list[dict[str, Any]]:
    epics_dir = plans_root / "epics"
    if not epics_dir.exists():
        return []

    matches: list[dict[str, Any]] = []
    for epic_dir in sorted(path for path in epics_dir.iterdir() if path.is_dir()):
        if not match_epic_dir(epic_dir, epic_id):
            continue
        payload = epic_payload(epic_dir, repo_root)
        if slice_id is not None:
            payload["slice_files"] = [
                item
                for item in cast(list[dict[str, str]], payload["slice_files"])
                if match_slice_file(Path(item["path"]), slice_id)
            ]
            if not payload["slice_files"]:
                continue
        matches.append(payload)
    return matches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve Forward Roll runtime, spec, epic, and slice context"
    )
    parser.add_argument("--runtime-path", help="Path to the runtime contract JSON")
    parser.add_argument("--epic-id", help="Epic identifier, for example 04")
    parser.add_argument(
        "--slice-id",
        help="Slice identifier, for example 02 or 04-02 when epic is not passed",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level for printed output",
    )
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
    specs_root = Path(runtime_text(runtime, "specs_root")).resolve()
    plans_root = Path(runtime_text(runtime, "plans_root")).resolve()
    planning_layout = runtime_dict(runtime, "planning_layout")
    epic_id, slice_id = resolve_slice_key(args.epic_id, args.slice_id)

    payload: dict[str, Any] = {
        "runtime_path": str(runtime_path),
        "repo_root": str(Path(runtime_text(runtime, "repo_root")).resolve()),
        "specs_root": str(specs_root),
        "plans_root": str(plans_root),
        "planning_layout": planning_layout,
        "filters": {
            "epic_id": epic_id,
            "slice_id": slice_id,
        },
    }

    if epic_id is not None or slice_id is not None:
        payload["spec_files"] = list_markdown_files(specs_root, repo_root)
        payload["epic_matches"] = filtered_epics(plans_root, repo_root, epic_id, slice_id)

    print(json.dumps(payload, indent=args.indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
