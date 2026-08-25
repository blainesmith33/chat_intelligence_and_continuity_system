#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec  # noqa: E402
from artifact_meta import meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def build_metadata(output_path: Path, content: str) -> dict:
    return {
        "file_path": str(output_path),
        "staging_root": str(STAGING_ROOT),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "size_bytes": len(content.encode("utf-8")),
        "status": "STAGED",
    }


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    try:
        raw_path, content = parse_file_spec(raw)
    except ValueError as exc:
        fail(str(exc))

    try:
        output_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Refusing to write outside staging root: {STAGING_ROOT}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    meta = build_metadata(output_path, content)
    meta_path = meta_path_for(output_path)
    save_metadata(meta_path, meta)

    print(f"[OK] Wrote staged file: {output_path}")
    print(f"[OK] Wrote metadata: {meta_path}")


if __name__ == "__main__":
    main()