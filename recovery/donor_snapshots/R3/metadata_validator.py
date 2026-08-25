#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


class MetadataValidationError(Exception):
    pass


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_required_fields(entry: dict, required: list[str]) -> list[str]:
    errors = []
    for field in required:
        if field not in entry:
            errors.append(f"Missing required field: {field}")
    return errors


def validate_no_extra_fields(entry: dict, allowed: set[str]) -> list[str]:
    return [f"Unexpected field: {k}" for k in entry.keys() if k not in allowed]


def validate_enum(value: str, allowed: list[str], field: str) -> list[str]:
    if value not in allowed:
        return [f"Invalid value for {field}: {value}"]
    return []


def validate_pattern(value: str, pattern: str, field: str) -> list[str]:
    import re

    if not re.match(pattern, value):
        return [f"Invalid pattern for {field}: {value}"]
    return []


def validate_entry(entry: dict, schema: dict) -> list[str]:
    errors = []

    required = schema["required"]
    properties = schema["properties"]
    allowed_fields = set(properties.keys())

    errors.extend(validate_required_fields(entry, required))
    errors.extend(validate_no_extra_fields(entry, allowed_fields))

    for field, rules in properties.items():
        if field not in entry:
            continue

        value = entry[field]

        if "enum" in rules:
            errors.extend(validate_enum(value, rules["enum"], field))

        if "pattern" in rules:
            errors.extend(validate_pattern(value, rules["pattern"], field))

        if rules.get("type") == "integer":
            if not isinstance(value, int):
                errors.append(f"Field {field} must be integer")

        if rules.get("type") == "string":
            if not isinstance(value, str):
                errors.append(f"Field {field} must be string")
            if "minLength" in rules and len(value) < rules["minLength"]:
                errors.append(f"Field {field} must have minLength {rules['minLength']}")

    return errors


def iter_manifest_entries(path: Path) -> Iterable[tuple[int, dict]]:
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if not line.strip():
                continue
            yield i, json.loads(line)


def validate_manifest(
    manifest_path: Path,
    schema_path: Path,
) -> None:
    schema = load_json(schema_path)

    all_errors: list[str] = []

    for line_num, entry in iter_manifest_entries(manifest_path):
        errors = validate_entry(entry, schema)
        for err in errors:
            all_errors.append(f"[line {line_num}] {err}")

    if all_errors:
        raise MetadataValidationError("\n".join(all_errors))


def main() -> None:
    base = Path("/home/kimberly/cics_v2")
    manifest_path = base / "sources_manifest.jsonl"
    schema_path = base / "metadata_schema_v1.json"

    validate_manifest(manifest_path, schema_path)
    print("[OK] Metadata validation passed")


if __name__ == "__main__":
    main()
