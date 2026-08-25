#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    save_metadata(meta_path, data)

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()