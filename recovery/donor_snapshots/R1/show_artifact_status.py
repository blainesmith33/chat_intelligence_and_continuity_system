#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        return meta_path

    fail(f"Metadata file not found: {meta_path}")


def display_artifact_path(data: dict) -> str:
    if data.get("status") == "COMMITTED" and data.get("committed_path"):
        return str(data["committed_path"])
    return str(data.get("file_path"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/show_artifact_status.py <artifact_path>")

    meta_path = resolve_meta(sys.argv[1])
    data = load_metadata(meta_path)

    print(f"artifact_path: {display_artifact_path(data)}")
    print(f"status: {data.get('status')}")
    print(f"metadata_path: {meta_path}")

    if "approved_utc" in data:
        print(f"approved_utc: {data['approved_utc']}")
    if "rejected_utc" in data:
        print(f"rejected_utc: {data['rejected_utc']}")
    if "rejection_reason" in data:
        print(f"rejection_reason: {data['rejection_reason']}")
    if "committed_utc" in data:
        print(f"committed_utc: {data['committed_utc']}")
    if "committed_path" in data:
        print(f"committed_path: {data['committed_path']}")


if __name__ == "__main__":
    main()