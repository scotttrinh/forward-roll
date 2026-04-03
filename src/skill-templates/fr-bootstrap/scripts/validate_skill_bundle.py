#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}


def load_frontmatter(skill_md: Path) -> tuple[list[str], str]:
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("No YAML frontmatter found")

    marker = "\n---\n"
    end = content.find(marker, 4)
    if end == -1:
        raise ValueError("Invalid frontmatter format")

    return content[4:end].splitlines(), content[end + len(marker) :]


def parse_top_level_keys(lines: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    current_key: str | None = None

    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if raw_line.startswith((" ", "\t")):
            continue

        if ":" not in raw_line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")

        key, value = raw_line.split(":", 1)
        current_key = key.strip()
        parsed[current_key] = value.strip()

    if current_key is None:
        raise ValueError("Frontmatter is empty")

    return parsed


def validate_frontmatter(frontmatter: dict[str, str]) -> None:
    unexpected = set(frontmatter) - ALLOWED_KEYS
    if unexpected:
        raise ValueError(
            "Unexpected key(s) in SKILL.md frontmatter: "
            + ", ".join(sorted(unexpected))
        )

    for required_key in ("name", "description"):
        if required_key not in frontmatter:
            raise ValueError(f"Missing '{required_key}' in frontmatter")

    name = frontmatter["name"].strip().strip("\"'")
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError(
            f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        )
    if name.startswith("-") or name.endswith("-") or "--" in name:
        raise ValueError(
            f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        )
    if len(name) > MAX_SKILL_NAME_LENGTH:
        raise ValueError(
            f"Name is too long ({len(name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH}."
        )

    description = frontmatter["description"].strip().strip("\"'")
    if "<" in description or ">" in description:
        raise ValueError("Description cannot contain angle brackets (< or >)")
    if len(description) > 1024:
        raise ValueError(
            f"Description is too long ({len(description)} characters). Maximum is 1024."
        )


def validate_skill(skill_path: Path) -> None:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise ValueError("SKILL.md not found")

    lines, _ = load_frontmatter(skill_md)
    frontmatter = parse_top_level_keys(lines)
    validate_frontmatter(frontmatter)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a Forward Roll skill bundle without third-party dependencies"
    )
    parser.add_argument("skill_path", nargs="+", help="Skill directory to validate")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    exit_code = 0

    for raw_path in args.skill_path:
        skill_path = Path(raw_path).resolve()
        try:
            validate_skill(skill_path)
        except ValueError as exc:
            print(f"{skill_path}: INVALID: {exc}")
            exit_code = 1
        else:
            print(f"{skill_path}: valid")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
