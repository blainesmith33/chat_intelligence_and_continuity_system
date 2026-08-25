#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec  # noqa: E402
from artifact_paths import resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    try:
        raw_path, content = parse_file_spec(raw)
    except ValueError as exc:
        fail(str(exc))

    output_path = resolve_path(raw_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote file: {output_path}")


if __name__ == "__main__":
    main()