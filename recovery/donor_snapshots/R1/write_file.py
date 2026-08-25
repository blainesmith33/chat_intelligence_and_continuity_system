#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: write_file.py <filepath>", file=sys.stderr)
        return 1

    filepath = Path(sys.argv[1]).expanduser().resolve()
    content = sys.stdin.read()

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote file: {filepath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())