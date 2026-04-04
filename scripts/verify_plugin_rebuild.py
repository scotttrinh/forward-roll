#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_MARKERS = (".git", ".jj")
SKILL_NAMES = (
    "fr-bootstrap",
    "fr-specify",
    "fr-plan-epic",
    "fr-plan-slice",
    "fr-do",
    "fr-feedback",
    "fr-review",
)


def repo_root_from(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if any((candidate / marker).exists() for marker in REPO_MARKERS):
            return candidate
    raise ValueError("Could not locate repository root from verification script path")


def run(repo_root: Path, *args: str) -> None:
    subprocess.run(args, cwd=repo_root, check=True)


def generated_targets(repo_root: Path) -> list[Path]:
    manifest = json.loads((repo_root / "src" / "plugin-build.json").read_text(encoding="utf-8"))
    assets = manifest.get("generated_assets", [])
    if not isinstance(assets, list):
        return []

    targets: list[Path] = []
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        raw_targets = asset.get("targets", [])
        if not isinstance(raw_targets, list):
            continue
        for raw_target in raw_targets:
            if isinstance(raw_target, str):
                targets.append(repo_root / raw_target)
    return targets


def assert_targets_exist(targets: list[Path], repo_root: Path) -> None:
    missing = [target.relative_to(repo_root) for target in targets if not target.exists()]
    if missing:
        raise SystemExit(
            "Generated rebuild is incomplete. Missing target(s):\n"
            + "\n".join(f"- {path}" for path in missing)
        )


def validate_skills(repo_root: Path) -> None:
    validator = repo_root / "plugins" / "forward-roll" / "skills" / "fr-bootstrap" / "scripts" / "validate_skill_bundle.py"
    skill_paths = [
        repo_root / "plugins" / "forward-roll" / "skills" / skill_name
        for skill_name in SKILL_NAMES
    ]
    run(repo_root, "python3", str(validator), *(str(path) for path in skill_paths))


def assert_path_missing(path: Path, repo_root: Path) -> None:
    if path.exists():
        raise SystemExit(
            f"Generated rebuild did not clear stale file: {path.relative_to(repo_root)}"
        )


def main() -> int:
    repo_root = repo_root_from(Path(__file__).resolve().parent)
    plugin_root = repo_root / "plugins" / "forward-roll"
    plugin_parent = plugin_root.parent
    targets = generated_targets(repo_root)

    with tempfile.TemporaryDirectory(
        dir=plugin_parent, prefix="forward-roll-rebuild-check-"
    ) as temp_dir:
        backup_root = Path(temp_dir) / "forward-roll-backup"
        had_existing_plugin = plugin_root.exists()

        if had_existing_plugin:
            plugin_root.rename(backup_root)

        try:
            run(repo_root, "python3", "src/build.py")
            assert_targets_exist(targets, repo_root)
            validate_skills(repo_root)
            stale_file = plugin_root / "stale-file.txt"
            stale_file.write_text("stale\n", encoding="utf-8")
            run(repo_root, "python3", "src/build.py")
            assert_targets_exist(targets, repo_root)
            assert_path_missing(stale_file, repo_root)
            validate_skills(repo_root)
            print("Rebuild verification succeeded.")
        finally:
            if plugin_root.exists():
                shutil.rmtree(plugin_root)
            if had_existing_plugin:
                backup_root.rename(plugin_root)

    return 0


if __name__ == "__main__":
    sys.exit(main())
