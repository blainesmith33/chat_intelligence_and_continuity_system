#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from manifest_builder import build_manifest


class DeterminismError(Exception):
    pass


def verify_manifest_determinism(base_root: Path) -> Path:
    manifest_path = build_manifest(base_root=base_root)
    first_bytes = manifest_path.read_bytes()

    manifest_path = build_manifest(base_root=base_root)
    second_bytes = manifest_path.read_bytes()

    if first_bytes != second_bytes:
        raise DeterminismError("Manifest determinism verification failed: byte contents differ between runs")

    return manifest_path


def main() -> None:
    base_root = Path("/home/kimberly/cics_v2")
    manifest_path = verify_manifest_determinism(base_root)
    print(f"[OK] Determinism verified for manifest: {manifest_path}")


if __name__ == "__main__":
    main()
