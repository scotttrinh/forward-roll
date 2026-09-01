#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SKILL_NAMES = (
    "fr-bootstrap",
    "fr-specify",
    "fr-plan-epic",
    "fr-plan-slice",
    "fr-do",
    "fr-feedback",
    "fr-review",
)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    validator = repo_root / "skills" / "fr-bootstrap" / "scripts" / "validate_skill_bundle.py"
    skill_paths = [repo_root / "skills" / name for name in SKILL_NAMES]

    print("=== Validating SKILL.md Frontmatter ===")
    res1 = subprocess.run(
        [sys.executable, str(validator), *(str(p) for p in skill_paths)],
        cwd=repo_root,
        check=False,
    )
    if res1.returncode != 0:
        return res1.returncode

    print("\n=== Validating Python Constraints (Stdlib-only) ===")
    python_validator = repo_root / "scripts" / "validate_python_constraints.py"
    res2 = subprocess.run(
        [sys.executable, str(python_validator), str(repo_root / "skills")],
        cwd=repo_root,
        check=False,
    )
    if res2.returncode != 0:
        return res2.returncode

    print("\nAll skill and script validations passed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
