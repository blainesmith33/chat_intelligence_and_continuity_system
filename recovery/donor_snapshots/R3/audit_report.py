#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from metadata_validator import validate_entry, load_json


class AuditError(Exception):
    pass


def iter_manifest_entries(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if not line.strip():
                continue
            yield i, json.loads(line)


def build_audit(manifest_path: Path, schema_path: Path) -> dict:
    schema = load_json(schema_path)

    total_files = 0
    valid_files = 0
    invalid_files = 0

    per_section_counts: Counter[str] = Counter()
    authority_distribution: Counter[str] = Counter()
    language_distribution: Counter[str] = Counter()

    invalid_entries: list[dict] = []

    for line_num, entry in iter_manifest_entries(manifest_path):
        total_files += 1

        section = entry.get("section")
        authority = entry.get("authority_level")
        language = entry.get("language")

        if isinstance(section, str):
            per_section_counts[section] += 1
        if isinstance(authority, str):
            authority_distribution[authority] += 1
        if isinstance(language, str):
            language_distribution[language] += 1

        errors = validate_entry(entry, schema)
        if errors:
            invalid_files += 1
            invalid_entries.append(
                {
                    "line": line_num,
                    "errors": errors,
                }
            )
        else:
            valid_files += 1

    return {
        "total_files": total_files,
        "valid_files": valid_files,
        "invalid_files": invalid_files,
        "per_section_counts": dict(sorted(per_section_counts.items())),
        "authority_distribution": dict(sorted(authority_distribution.items())),
        "language_distribution": dict(sorted(language_distribution.items())),
        "status": "pass" if invalid_files == 0 else "fail",
        "invalid_entries": invalid_entries,
    }


def write_json_report(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text_report(report: dict, output_path: Path) -> None:
    lines: list[str] = []
    lines.append("CONTROL LAYER AUDIT REPORT")
    lines.append(f"status: {report['status']}")
    lines.append(f"total_files: {report['total_files']}")
    lines.append(f"valid_files: {report['valid_files']}")
    lines.append(f"invalid_files: {report['invalid_files']}")
    lines.append("")
    lines.append("per_section_counts:")
    for key, value in report["per_section_counts"].items():
        lines.append(f"  {key}: {value}")
    lines.append("")
    lines.append("authority_distribution:")
    for key, value in report["authority_distribution"].items():
        lines.append(f"  {key}: {value}")
    lines.append("")
    lines.append("language_distribution:")
    for key, value in report["language_distribution"].items():
        lines.append(f"  {key}: {value}")

    if report["invalid_entries"]:
        lines.append("")
        lines.append("invalid_entries:")
        for item in report["invalid_entries"]:
            lines.append(f"  line {item['line']}:")
            for err in item["errors"]:
                lines.append(f"    - {err}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    base = Path("/home/kimberly/cics_v2")
    manifest_path = base / "sources_manifest.jsonl"
    schema_path = base / "metadata_schema_v1.json"

    json_report_path = base / "audit_report.json"
    text_report_path = base / "audit_report.txt"

    report = build_audit(manifest_path, schema_path)
    write_json_report(report, json_report_path)
    write_text_report(report, text_report_path)

    if report["status"] != "pass":
        raise AuditError("[FAIL] Audit report generated with invalid entries")

    print(f"[OK] Wrote audit reports: {json_report_path} | {text_report_path}")


if __name__ == "__main__":
    main()
