#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()


def resolve_path(raw_path: str) -> Path:
    return Path(raw_path.strip()).expanduser().resolve()


def ensure_within_root(path: Path, root: Path) -> Path:
    path.relative_to(root)
    return path


def resolve_staging_artifact(raw_path: str) -> Path:
    path = resolve_path(raw_path)
    ensure_within_root(path, STAGING_ROOT)
    return path