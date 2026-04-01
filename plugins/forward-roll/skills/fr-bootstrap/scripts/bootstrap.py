#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
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


def run_command(
    args: list[str], cwd: Path | None = None
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None


def first_line(text: str) -> str:
    return text.strip().splitlines()[0] if text.strip() else ""


def detect_repo_root(start: Path) -> Path:
    jj_root = run_command(["jj", "root"], cwd=start)
    if jj_root and jj_root.returncode == 0:
        return Path(jj_root.stdout.strip()).resolve()

    git_root = run_command(["git", "rev-parse", "--show-toplevel"], cwd=start)
    if git_root and git_root.returncode == 0:
        return Path(git_root.stdout.strip()).resolve()

    return start.resolve()


def detect_jj(repo_root: Path) -> dict[str, object]:
    version = run_command(["jj", "--version"], cwd=repo_root)
    root = run_command(["jj", "root"], cwd=repo_root)
    available = bool(version and version.returncode == 0)
    return {
        "available": available,
        "version": first_line(version.stdout) if available and version else None,
        "repo_root": root.stdout.strip() if root and root.returncode == 0 else None,
        "workflow": "squash",
    }


def is_in_repo(path: Path, repo_root: Path) -> bool:
    try:
        path.resolve().relative_to(repo_root.resolve())
        return True
    except ValueError:
        return False


def is_gitignored(path: Path, repo_root: Path) -> bool:
    if not is_in_repo(path, repo_root):
        return False
    relative = path.resolve().relative_to(repo_root.resolve())
    result = run_command(["git", "check-ignore", str(relative)], cwd=repo_root)
    return bool(result and result.returncode == 0)


def describe_root(path: Path, repo_root: Path) -> dict[str, object]:
    resolved = path.resolve()
    return {
        "path": str(resolved),
        "location": "in-repo" if is_in_repo(resolved, repo_root) else "out-of-repo",
        "exists": resolved.exists(),
        "gitignored": is_gitignored(resolved, repo_root),
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def default_runtime_path(repo_root: Path) -> Path:
    return repo_root / ".forward-roll" / "runtime.json"


def default_specs_root(repo_root: Path) -> Path:
    return repo_root / ".forward-roll" / "specs"


def default_plans_root(repo_root: Path) -> Path:
    return repo_root / ".forward-roll" / "plans"

def runtime_text(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError(f"expected runtime string, got {type(value).__name__}")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve and persist the Forward Roll runtime contract"
    )
    parser.add_argument("--repo-root", help="Starting path for repo root detection")
    parser.add_argument("--runtime-path", help="Where to persist the runtime contract JSON")
    parser.add_argument("--project-name", help="Override the detected project name")
    parser.add_argument("--specs-root", help="Override the specs root")
    parser.add_argument("--plans-root", help="Override the plans root")
    parser.add_argument("--testing-posture", help="Override testing defaults for this project")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    start = Path(args.repo_root or ".").resolve()
    repo_root = detect_repo_root(start)
    runtime_path = (
        Path(args.runtime_path).resolve()
        if args.runtime_path
        else default_runtime_path(repo_root)
    )
    specs_root = (
        Path(args.specs_root).resolve()
        if args.specs_root
        else default_specs_root(repo_root)
    )
    plans_root = (
        Path(args.plans_root).resolve()
        if args.plans_root
        else default_plans_root(repo_root)
    )

    plans_root.mkdir(parents=True, exist_ok=True)
    (plans_root / "epics").mkdir(parents=True, exist_ok=True)

    runtime: dict[str, object] = {
        "project_name": args.project_name or repo_root.name,
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "runtime_path": str(runtime_path),
        "specs_root": str(specs_root),
        "plans_root": str(plans_root),
        "planning_layout": {
            "epics_dir": "epics",
            "epic_file": "EPIC.md",
            "slices_dir": "slices",
            "feedback_dir": "feedback",
            "reviews_dir": "reviews",
        },
        "roots": {
            "specs": describe_root(specs_root, repo_root),
            "plans": describe_root(plans_root, repo_root),
        },
        "jj": detect_jj(repo_root),
        "testing_posture": args.testing_posture or DEFAULT_TESTING_POSTURE,
    }

    write_json(runtime_path, runtime)

    print(f"runtime: {runtime_path}")
    print(f"project: {runtime_text(runtime['project_name'])}")
    print(f"repo_root: {repo_root}")
    print(f"specs_root: {specs_root}")
    print(f"plans_root: {plans_root}")
    jj = cast(dict[str, object], runtime["jj"])
    print(f"jj_available: {jj['available']}")
    print(f"jj_workflow: {runtime_text(jj['workflow'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
