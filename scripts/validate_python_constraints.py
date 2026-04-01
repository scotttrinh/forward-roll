#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


def stdlib_roots() -> set[str]:
    names = set(sys.stdlib_module_names)
    names.update({"__future__"})
    return names


def imported_roots(tree: ast.AST) -> list[tuple[int, str, int]]:
    roots: list[tuple[int, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.append((node.lineno, alias.name.split(".")[0], 0))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".")[0] if module else ""
            roots.append((node.lineno, root, node.level))
    return roots


def validate_file(path: Path, allowed: set[str]) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    errors: list[str] = []

    for lineno, root, level in imported_roots(tree):
        if level:
            errors.append(f"{path}:{lineno}: relative imports are not allowed")
            continue
        if not root:
            continue
        if root not in allowed:
            errors.append(
                f"{path}:{lineno}: non-stdlib import '{root}' is not allowed in skill scripts"
            )

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate that Forward Roll skill scripts use only stdlib imports"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["plugins/forward-roll/skills"],
        help="Script roots or files to validate",
    )
    return parser


def iter_python_files(paths: list[str]) -> list[Path]:
    result: list[Path] = []
    for raw in paths:
        path = Path(raw).resolve()
        if path.is_file() and path.suffix == ".py":
            result.append(path)
            continue
        if path.is_dir():
            result.extend(sorted(path.rglob("*.py")))
    return result


def main() -> int:
    args = build_parser().parse_args()
    allowed = stdlib_roots()
    files = iter_python_files(args.paths)
    errors: list[str] = []

    for path in files:
        errors.extend(validate_file(path, allowed))

    if errors:
        for error in errors:
            print(error)
        return 1

    for path in files:
        print(f"{path}: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
