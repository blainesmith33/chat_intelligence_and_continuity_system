#!/usr/bin/env python3
from __future__ import annotations

import re


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)


def parse_file_spec(raw: str) -> tuple[str, str]:
    match = PATTERN.match(raw)
    if not match:
        raise ValueError(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )
    return match.group(1), match.group(2)
