#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def meta_path_for(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def load_metadata(meta_path: Path) -> dict:
    return json.loads(meta_path.read_text(encoding="utf-8"))


def save_metadata(meta_path: Path, data: dict) -> None:
    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")