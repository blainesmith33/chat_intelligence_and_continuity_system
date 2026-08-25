#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import COMMITTED_ROOT, resolve_path  # noqa: E402


REQUIRED_STATUS = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_committed_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(COMMITTED_ROOT)
    except ValueError:
        fail(f"Artifact must be inside committed root: {COMMITTED_ROOT}")

    if not artifact_path.exists():
        fail(f"Committed artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_committed_artifact.py <committed_artifact_path>")

    artifact_path = resolve_committed_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    status = data.get("status")

    if status != REQUIRED_STATUS:
        fail(f"Refusing to delete committed artifact in status {status}. Required status: {REQUIRED_STATUS}")

    meta_path.unlink()
    artifact_path.unlink()

    print(f"[OK] Deleted committed artifact: {artifact_path}")
    print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()