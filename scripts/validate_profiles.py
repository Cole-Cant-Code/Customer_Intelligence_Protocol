"""Validate domain profiles in a directory."""

from __future__ import annotations

import sys
from pathlib import Path

from cip_core.domain_profiles.loader import load_profile_file


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_profiles.py <profiles_dir>")
        return 2

    directory = Path(sys.argv[1])
    if not directory.exists():
        print(f"Directory does not exist: {directory}")
        return 2

    failures = 0
    checked = 0
    for path in sorted(directory.rglob("*.yaml")):
        if path.name.startswith("_") or "schema" in path.name:
            continue
        checked += 1
        try:
            load_profile_file(path)
            print(f"OK   {path}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {path}: {exc}")

    print(f"Checked {checked} profile file(s), failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
