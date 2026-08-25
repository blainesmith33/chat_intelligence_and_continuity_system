#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT  # noqa: E402


TARGET_STATUS = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def artifact_path_for_meta(meta_path: Path) -> Path:
    if not meta_path.name.endswith(".meta.json"):
        raise ValueError(f"Not a metadata path: {meta_path}")
    artifact_name = meta_path.name[:-10]
    return meta_path.with_name(artifact_name)


def main() -> None:
    if len(sys.argv) != 1:
        fail("Usage: python ~/cics/purge_approved_staging.py")

    removed = 0

    for meta_path in iter_metadata_files(STAGING_ROOT):
        data = load_metadata(meta_path)
        if data.get("status") != TARGET_STATUS:
            continue

        artifact_path = artifact_path_for_meta(meta_path)

        if artifact_path.exists():
            artifact_path.unlink()
        meta_path.unlink()
        removed += 1

        print(f"[OK] Removed approved artifact: {artifact_path}")
        print(f"[OK] Removed metadata: {meta_path}")

    print(f"[OK] Total approved artifacts removed: {removed}")


if __name__ == "__main__":
    main()