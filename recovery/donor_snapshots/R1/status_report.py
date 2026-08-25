#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def summarize(root: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for meta_path in iter_metadata_files(root):
        data = load_metadata(meta_path)
        counts[str(data.get("status"))] += 1
    return counts


def print_summary(label: str, root: Path) -> None:
    counts = summarize(root)
    total = sum(counts.values())

    print(f"{label}:")
    print(f"  root: {root}")
    print(f"  total: {total}")

    if total == 0:
        print("  states: none")
        return

    for status in sorted(counts):
        print(f"  {status}: {counts[status]}")


def main() -> None:
    if len(sys.argv) != 1:
        print("[ERROR] Usage: python ~/cics/status_report.py", file=sys.stderr)
        raise SystemExit(1)

    print_summary("staging", STAGING_ROOT)
    print_summary("committed", COMMITTED_ROOT)


if __name__ == "__main__":
    main()