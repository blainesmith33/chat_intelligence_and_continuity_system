#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_path  # noqa: E402


ALLOWED_DELETE_STATES = {"STAGED", "REJECTED"}


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Staged artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_staged_artifact.py <staged_artifact_path>")

    artifact_path = resolve_staged_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    status = data.get("status")

    if status not in ALLOWED_DELETE_STATES:
        fail(
            f"Refusing to delete staged artifact in status {status}. "
            f"Allowed delete states: {sorted(ALLOWED_DELETE_STATES)}"
        )

    meta_path.unlink()
    artifact_path.unlink()

    print(f"[OK] Deleted staged artifact: {artifact_path}")
    print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()