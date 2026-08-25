#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


CONFIG_PATH = Path("/home/kimberly/cics_v2/canonical_control_layer_config.json")


class DirectoryStructureError(Exception):
    pass


def load_config(config_path: Path = CONFIG_PATH) -> dict:
    return json.loads(config_path.read_text(encoding="utf-8"))


def sources_root(base_root: Path) -> Path:
    return base_root.expanduser().resolve() / "corpora" / "coding" / "sources"


def required_section_paths(root: Path, config: dict) -> list[Path]:
    paths: list[Path] = []

    split_sections = set(config["authority_split_sections"])
    non_split_sections = set(config["non_split_sections"])
    cloud_children = list(config["cloud_provider_children"])

    for section in config["sections"]:
        section_root = root / section

        if section == "cloud_providers":
            for authority in ("official", "community"):
                for child in cloud_children:
                    paths.append(section_root / authority / child)
        elif section in split_sections:
            paths.append(section_root / "official")
            paths.append(section_root / "community")
        elif section in non_split_sections:
            paths.append(section_root)
        else:
            raise DirectoryStructureError(f"Section classification missing for: {section}")

    return paths


def allowed_controlled_children(section: str, config: dict) -> set[str]:
    split_sections = set(config["authority_split_sections"])
    non_split_sections = set(config["non_split_sections"])

    if section == "cloud_providers":
        return {"official", "community"}

    if section in split_sections:
        return {"official", "community"}

    if section in non_split_sections:
        return set()

    raise DirectoryStructureError(f"Unknown section: {section}")


def validate_controlled_layer(root: Path, config: dict) -> list[str]:
    errors: list[str] = []

    if not root.exists():
        errors.append(f"Missing sources root: {root}")
        return errors

    expected_sections = set(config["sections"])
    actual_top_level = {p.name for p in root.iterdir() if p.is_dir()}

    missing_sections = sorted(expected_sections - actual_top_level)
    extra_sections = sorted(actual_top_level - expected_sections)

    for name in missing_sections:
        errors.append(f"Missing required section directory: {root / name}")
    for name in extra_sections:
        errors.append(f"Unexpected top-level section directory: {root / name}")

    split_sections = set(config["authority_split_sections"])
    non_split_sections = set(config["non_split_sections"])
    cloud_children = set(config["cloud_provider_children"])

    for section in sorted(expected_sections & actual_top_level):
        section_root = root / section
        child_dirs = {p.name for p in section_root.iterdir() if p.is_dir()}
        allowed_children = allowed_controlled_children(section, config)

        if section == "cloud_providers":
            unexpected = sorted(child_dirs - allowed_children)
            missing = sorted(allowed_children - child_dirs)

            for name in missing:
                errors.append(f"Missing required authority directory: {section_root / name}")
            for name in unexpected:
                errors.append(f"Unexpected controlled child in cloud_providers: {section_root / name}")

            for authority in sorted(allowed_children & child_dirs):
                authority_root = section_root / authority
                provider_dirs = {p.name for p in authority_root.iterdir() if p.is_dir()}
                missing_providers = sorted(cloud_children - provider_dirs)
                extra_providers = sorted(provider_dirs - cloud_children)

                for name in missing_providers:
                    errors.append(f"Missing required cloud provider directory: {authority_root / name}")
                for name in extra_providers:
                    errors.append(f"Unexpected cloud provider directory: {authority_root / name}")

        elif section in split_sections:
            unexpected = sorted(child_dirs - allowed_children)
            missing = sorted(allowed_children - child_dirs)

            for name in missing:
                errors.append(f"Missing required authority directory: {section_root / name}")
            for name in unexpected:
                errors.append(f"Unexpected controlled child in split section: {section_root / name}")

        elif section in non_split_sections:
            if child_dirs:
                errors.append(
                    f"Non-split section has controlled-layer subdirectories but must not: {section_root}"
                )
        else:
            errors.append(f"Unknown section classification: {section}")

    return errors


def create_required_structure(base_root: Path, config: dict) -> Path:
    root = sources_root(base_root)
    root.mkdir(parents=True, exist_ok=True)

    for path in required_section_paths(root, config):
        path.mkdir(parents=True, exist_ok=True)

    return root


def build_and_validate(base_root: Path, config_path: Path = CONFIG_PATH) -> Path:
    config = load_config(config_path)
    root = create_required_structure(base_root, config)
    errors = validate_controlled_layer(root, config)

    if errors:
        raise DirectoryStructureError("\\n".join(errors))

    return root


def main() -> None:
    base_root = Path("/home/kimberly/cics_v2")
    root = build_and_validate(base_root)
    print(f"[OK] Directory structure ready: {root}")


if __name__ == "__main__":
    main()
