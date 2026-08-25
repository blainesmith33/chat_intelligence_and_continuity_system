#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact_path(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = load_metadata(staged_meta)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = TARGET_STATE
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    save_metadata(committed_meta, data)

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()