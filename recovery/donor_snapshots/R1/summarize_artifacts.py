#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/summarize_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)
    counts: Counter[str] = Counter()

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        counts[str(data.get("status"))] += 1

    print(f"area: {area}")
    print(f"root: {root}")
    print(f"total_artifacts: {sum(counts.values())}")

    for status in sorted(counts):
        print(f"{status}: {counts[status]}")


if __name__ == "__main__":
    main()