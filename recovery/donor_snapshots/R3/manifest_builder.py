#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from directory_builder import CONFIG_PATH, load_config, sources_root, validate_controlled_layer
from hashing import doc_id_from_path, file_hash_from_path, file_size_bytes, normalize_path


class ManifestBuildError(Exception):
    pass


CANONICAL_MANIFEST_FIELDS = [
    "schema_id",
    "section",
    "authority_level",
    "language",
    "project",
    "source_path",
    "filename",
    "doc_id",
    "file_hash",
    "file_size_bytes",
    "corpus",
]


def detect_language(path: Path, config: dict) -> str:
    mapping = config["extension_language_map"]
    filename = path.name

    if filename in mapping:
        return mapping[filename]

    suffix = path.suffix
    if suffix in mapping:
        return mapping[suffix]

    raise ManifestBuildError(f"Unknown extension / language mapping for file: {path}")


def derive_authority_and_project(path: Path, root: Path, config: dict) -> tuple[str, str, str]:
    rel = path.relative_to(root)
    parts = rel.parts

    if len(parts) < 2:
        raise ManifestBuildError(f"Invalid file placement under sources root: {path}")

    section = parts[0]
    split_sections = set(config["authority_split_sections"])
    non_split_sections = set(config["non_split_sections"])

    if section == "cloud_providers":
        if len(parts) < 4:
            raise ManifestBuildError(f"Cloud provider file missing required structure: {path}")
        authority = parts[1]
        provider = parts[2]
        if authority not in {"official", "community"}:
            raise ManifestBuildError(f"Invalid cloud authority directory for file: {path}")
        if provider not in set(config["cloud_provider_children"]):
            raise ManifestBuildError(f"Invalid cloud provider directory for file: {path}")
        project = provider
        return section, authority, project

    if section in split_sections:
        authority = parts[1]
        if authority not in {"official", "community"}:
            raise ManifestBuildError(f"Invalid authority directory for file: {path}")

        remaining = parts[2:-1]
        project = remaining[0] if remaining else section
        return section, authority, project

    if section in non_split_sections:
        authority = "n/a"
        remaining = parts[1:-1]
        project = remaining[0] if remaining else section
        return section, authority, project

    raise ManifestBuildError(f"Unknown section for file: {path}")


def iter_source_files(root: Path) -> Iterable[Path]:
    files = [p for p in root.rglob("*") if p.is_file()]
    files.sort(key=lambda p: normalize_path(p))
    for path in files:
        yield path


def build_manifest_entry(path: Path, root: Path, config: dict) -> dict:
    section, authority_level, project = derive_authority_and_project(path, root, config)
    language = detect_language(path, config)

    entry = {
        "schema_id": config["metadata_schema_id"],
        "section": section,
        "authority_level": authority_level,
        "language": language,
        "project": project,
        "source_path": normalize_path(path),
        "filename": path.name,
        "doc_id": doc_id_from_path(path),
        "file_hash": file_hash_from_path(path),
        "file_size_bytes": file_size_bytes(path),
        "corpus": config["corpus_id"],
    }

    return entry


def canonicalize_manifest_entry(entry: dict) -> dict:
    missing = [k for k in CANONICAL_MANIFEST_FIELDS if k not in entry]
    extra = [k for k in entry if k not in CANONICAL_MANIFEST_FIELDS]

    if missing:
        raise ManifestBuildError(f"Manifest entry missing canonical fields: {missing}")
    if extra:
        raise ManifestBuildError(f"Manifest entry has unexpected fields: {extra}")

    return {key: entry[key] for key in CANONICAL_MANIFEST_FIELDS}


def write_manifest(entries: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        for entry in entries:
            canonical = canonicalize_manifest_entry(entry)
            line = json.dumps(
                canonical,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            f.write(line)
            f.write("\n")


def build_manifest(
    base_root: Path = Path("/home/kimberly/cics_v2"),
    config_path: Path = CONFIG_PATH,
) -> Path:
    config = load_config(config_path)
    root = sources_root(base_root)

    structure_errors = validate_controlled_layer(root, config)
    if structure_errors:
        raise ManifestBuildError("Controlled-layer validation failed:\n" + "\n".join(structure_errors))

    entries: list[dict] = []
    seen_doc_ids: set[str] = set()

    for path in iter_source_files(root):
        entry = build_manifest_entry(path, root, config)
        doc_id = entry["doc_id"]

        if doc_id in seen_doc_ids:
            raise ManifestBuildError(f"Duplicate doc_id detected: {doc_id} for {path}")
        seen_doc_ids.add(doc_id)

        entries.append(entry)

    output_path = base_root.expanduser().resolve() / "sources_manifest.jsonl"
    write_manifest(entries, output_path)
    return output_path


def main() -> None:
    output_path = build_manifest()
    print(f"[OK] Wrote manifest: {output_path}")


if __name__ == "__main__":
    main()
