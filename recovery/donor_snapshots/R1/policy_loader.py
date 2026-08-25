#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


POLICY_PATH = Path("~/cics/policies/roots.json").expanduser()


def load_roots() -> dict:
    if not POLICY_PATH.exists():
        raise RuntimeError(f"Policy file not found: {POLICY_PATH}")

    with POLICY_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required = [
        "staging_root",
        "committed_root",
        "artifacts_root",
        "imports_root",
    ]

    for key in required:
        if key not in data:
            raise RuntimeError(f"Missing required policy key: {key}")

    return data
