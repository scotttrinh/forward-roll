#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast


REPO_MARKERS = (".git", ".jj")


def repo_root_from(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if any((candidate / marker).exists() for marker in REPO_MARKERS):
            return candidate
    raise ValueError("Could not locate repository root from build script path")


def manifest_path(script_path: Path) -> Path:
    repo_root = repo_root_from(script_path.resolve().parent)
    return repo_root / "src" / "plugin-build.json"


def load_manifest(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    required_keys = {
        "schema_version",
        "source_root",
        "generated_roots",
        "generated_outputs_checked_in",
        "authoring_roots",
        "build_entrypoint",
    }
    missing = required_keys - manifest.keys()
    if missing:
        errors.append("Missing manifest key(s): " + ", ".join(sorted(missing)))

    generated_roots = manifest.get("generated_roots")
    if not isinstance(generated_roots, list) or not all(
        isinstance(path, str) for path in generated_roots
    ):
        errors.append("'generated_roots' must be a list of strings")

    authoring_roots = manifest.get("authoring_roots")
    if not isinstance(authoring_roots, dict) or not all(
        isinstance(name, str) and isinstance(path, str)
        for name, path in authoring_roots.items()
    ):
        errors.append("'authoring_roots' must be an object of string keys to string paths")

    if not isinstance(manifest.get("generated_outputs_checked_in"), bool):
        errors.append("'generated_outputs_checked_in' must be a boolean")

    generated_assets = manifest.get("generated_assets", [])
    if not isinstance(generated_assets, list):
        errors.append("'generated_assets' must be a list when present")
    else:
        for index, asset in enumerate(generated_assets):
            if not isinstance(asset, dict):
                errors.append(f"'generated_assets[{index}]' must be an object")
                continue
            source = asset.get("source")
            targets = asset.get("targets")
            if not isinstance(source, str):
                errors.append(f"'generated_assets[{index}].source' must be a string")
            if not isinstance(targets, list) or not all(
                isinstance(target, str) for target in targets
            ):
                errors.append(
                    f"'generated_assets[{index}].targets' must be a list of strings"
                )

    return errors


def check_paths(repo_root: Path, manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []

    source_root = manifest.get("source_root")
    if isinstance(source_root, str) and not (repo_root / source_root).is_dir():
        errors.append(f"Source root does not exist: {source_root}")

    authoring_roots = manifest.get("authoring_roots", {})
    if isinstance(authoring_roots, dict):
        for name, raw_path in sorted(authoring_roots.items()):
            if isinstance(raw_path, str) and not (repo_root / raw_path).exists():
                errors.append(f"Authoring root '{name}' does not exist: {raw_path}")

    generated_assets = manifest.get("generated_assets", [])
    if isinstance(generated_assets, list):
        for index, asset in enumerate(generated_assets):
            if not isinstance(asset, dict):
                continue
            source = asset.get("source")
            targets = asset.get("targets")
            if isinstance(source, str) and not (repo_root / source).is_file():
                errors.append(
                    f"Generated asset source does not exist: generated_assets[{index}] -> {source}"
                )
            if isinstance(targets, list):
                for target in targets:
                    if not isinstance(target, str):
                        continue
                    target_parent = (repo_root / target).parent
                    if not target_parent.exists():
                        errors.append(
                            "Generated asset target parent does not exist: "
                            f"generated_assets[{index}] -> {target_parent.relative_to(repo_root)}"
                        )

    return errors


def generated_assets(manifest: dict[str, object]) -> list[dict[str, Any]]:
    assets = manifest.get("generated_assets", [])
    if not isinstance(assets, list):
        return []
    return [cast(dict[str, Any], asset) for asset in assets if isinstance(asset, dict)]


def render_generated_assets(repo_root: Path, manifest: dict[str, object]) -> list[Path]:
    written: list[Path] = []
    for asset in generated_assets(manifest):
        source = repo_root / str(asset["source"])
        source_text = source.read_text(encoding="utf-8")
        for raw_target in cast(list[str], asset["targets"]):
            target = repo_root / raw_target
            target.write_text(source_text, encoding="utf-8")
            written.append(target)
    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the Forward Roll plugin authoring/build contract"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the manifest and required paths without attempting generation",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    path = manifest_path(Path(__file__))
    repo_root = repo_root_from(path.parent)
    manifest = load_manifest(path)

    errors = validate_manifest(manifest)
    errors.extend(check_paths(repo_root, manifest))
    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"Manifest: {path.relative_to(repo_root)}")
    print(f"Source root: {manifest['source_root']}")
    print("Generated roots:")
    for raw_path in manifest["generated_roots"]:
        print(f"- {raw_path}")
    print(
        "Generated outputs checked in: "
        + ("yes" if manifest["generated_outputs_checked_in"] else "no")
    )
    print(f"Build entrypoint: {manifest['build_entrypoint']}")

    if args.check:
        print("Build contract validated.")
        return 0

    written = render_generated_assets(repo_root, manifest)
    if written:
        print("Generated assets:")
        for path in written:
            print(f"- {path.relative_to(repo_root)}")
    else:
        print("No generated assets declared.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
