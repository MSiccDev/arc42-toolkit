#!/usr/bin/env python3
"""Synchronize canonical skills/ into the APM package mirror.

The toolkit keeps skills/ as the human-facing canonical source because existing
install instructions and agent integrations reference that path. APM expects
multi-skill packages under .apm/skills/, so this script maintains a byte-for-byte
mirror for one-command APM installs.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
TARGET = ROOT / ".apm" / "skills"

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def copy_mirror() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, TARGET, ignore=IGNORE)


def compare_dirs(left: Path, right: Path) -> list[str]:
    if not left.exists():
        return [f"missing source directory: {left}"]
    if not right.exists():
        return [f"missing APM mirror directory: {right}"]

    comparison = filecmp.dircmp(left, right)
    problems: list[str] = []

    def walk(cmp: filecmp.dircmp[str], rel: Path = Path("")) -> None:
        for name in cmp.left_only:
            problems.append(f"missing from APM mirror: {rel / name}")
        for name in cmp.right_only:
            problems.append(f"extra in APM mirror: {rel / name}")
        for name in cmp.diff_files:
            problems.append(f"differs in APM mirror: {rel / name}")
        for name in cmp.funny_files:
            problems.append(f"could not compare: {rel / name}")
        for name, subcmp in cmp.subdirs.items():
            walk(subcmp, rel / name)

    walk(comparison)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if .apm/skills is not synchronized with skills/",
    )
    args = parser.parse_args()

    if args.check:
        problems = compare_dirs(SOURCE, TARGET)
        if problems:
            for problem in problems:
                print(problem, file=sys.stderr)
            return 1
        print("APM skills mirror is synchronized")
        return 0

    copy_mirror()
    print(f"Synchronized {SOURCE.relative_to(ROOT)} -> {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
