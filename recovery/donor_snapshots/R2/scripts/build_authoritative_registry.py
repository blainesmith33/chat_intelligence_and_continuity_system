#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


RAW_ROOT = Path("/home/kimberly/cics/imports/raw")
SCHEMA_PATH = Path("/home/kimberly/cics/schemas/entity_schema.json")
OUTPUT_PATH = Path("/home/kimberly/cics/analysis/authoritative_registry.json")
SUMMARY_PATH = Path("/home/kimberly/cics/analysis/authoritative_registry_summary.json")


# -------------------------------------------------------------------
# AUTHORITATIVE FOLDER POLICY
# -------------------------------------------------------------------
# This is the source of truth for top-level corpus sections.
# No inference is allowed here.
#
# Rules:
# - every top-level folder under imports/raw must appear here
# - unknown folders = hard fail
# - formal project existence is defined here, not by RAG
# -------------------------------------------------------------------

FOLDER_POLICY: Dict[str, Dict[str, Any]] = {
    "ALIP-AI_Infrastructure_Provisioning_Platform": {
        "entity_type": "formal_project",
        "canonical_name": "ALIP — AI Infrastructure Provisioning Platform",
        "aliases": [
            "ALIP",
            "AI Infrastructure Provisioning Platform",
        ],
        "status": "active",
        "notes": "Authoritative project folder; one ALIP branch.",
    },
    "ALIP-AI_Lab_Infrastructure_Program": {
        "entity_type": "formal_project",
        "canonical_name": "ALIP — AI Lab Infrastructure Program",
        "aliases": [
            "ALIP",
            "AI Lab Infrastructure Program",
        ],
        "status": "active",
        "notes": "Authoritative project folder; second ALIP branch.",
    },
    "ARCHIVE": {
        "entity_type": "archive_bucket",
        "canonical_name": "Archive",
        "aliases": ["ARCHIVE"],
        "status": "archived",
        "notes": "Historical archive bucket; not counted as an active formal project.",
    },
    "Ai_Diagonstician": {
        "entity_type": "formal_project",
        "canonical_name": "DAIRP — Deterministic AI Inspection & Remediation Platform",
        "aliases": [
            "AI Diagnostician",
            "AI Computer Diagnostician",
            "Aletheia Diagnostica",
            "DAIRP",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "Aletheia_Forensis": {
        "entity_type": "formal_project",
        "canonical_name": "Aletheia Forensis",
        "aliases": [
            "The Reel Forensics Engine",
            "Aletheia Forensis",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "CICS": {
        "entity_type": "formal_project",
        "canonical_name": "CICS — Chat Intelligence & Continuity System",
        "aliases": [
            "CICS",
            "Chat Intelligence & Continuity System",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "Deterministic_AI_Infrastructure": {
        "entity_type": "formal_project",
        "canonical_name": "Deterministic AI Infrastructure",
        "aliases": [
            "Deterministic AI Infrastructure",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "ExosWoW_Addon_Project": {
        "entity_type": "formal_project",
        "canonical_name": "ExosWoW Addon Project",
        "aliases": [
            "ExosWoW Addon Project",
            "ExosAddons",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "ExosWoW_Mod_Ecosystem": {
        "entity_type": "formal_project",
        "canonical_name": "ExosWoW Mod Ecosystem",
        "aliases": [
            "ExosWoW Mod Ecosystem",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "Imperium_Aletheiae": {
        "entity_type": "formal_project",
        "canonical_name": "DAFOS — Deterministic AI Financial Operations System",
        "aliases": [
            "Imperium Aletheiae",
            "DAFOS",
            "Deterministic AI Financial Operations System",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "Non-project_chats": {
        "entity_type": "non_project_corpus",
        "canonical_name": "Non-project Chats",
        "aliases": [
            "Non-project chats",
        ],
        "status": "non_project",
        "notes": "Catchment for unpromoted or miscellaneous chats; not authoritative project identity.",
    },
    "UMB_Cross-Project_Governance_Framework": {
        "entity_type": "formal_project",
        "canonical_name": "UMB — Cross-Project Governance Framework",
        "aliases": [
            "UMB",
            "Cross-Project Governance Framework",
        ],
        "status": "active",
        "notes": "Authoritative umbrella/governance project folder.",
    },
    "blAine": {
        "entity_type": "formal_project",
        "canonical_name": "blAine",
        "aliases": [
            "blAine",
        ],
        "status": "active",
        "notes": "Authoritative formal project folder.",
    },
    "blaineai.me_website": {
        "entity_type": "formal_project",
        "canonical_name": "blaineai.me website",
        "aliases": [
            "blaineai website",
            "blaineai.me website",
            "blaineai",
        ],
        "status": "active",
        "notes": "Authoritative website/project folder.",
    },
        "gods_and_men": {
        "entity_type": "candidate_idea",
        "canonical_name": "gods and men",
        "aliases": [
            "gods and men"
        ],
        "status": "candidate",
        "notes": "Unpromoted concept folder; not a formal project yet."
    },
}


# -------------------------------------------------------------------
# REGISTRY POLICY
# -------------------------------------------------------------------

COLLAPSED_PROJECT_FAMILIES: Dict[str, str] = {
    "ALIP-AI_Infrastructure_Provisioning_Platform": "alip",
    "ALIP-AI_Lab_Infrastructure_Program": "alip",
}

COLLAPSED_CANONICALS: Dict[str, str] = {
    "alip": "ALIP",
}

COUNTABLE_ENTITY_TYPES = {"formal_project"}
NON_COUNTABLE_ENTITY_TYPES = {"archive_bucket", "non_project_corpus"}

REQUIRED_SCHEMA_KEYS = {
    "entity_id",
    "entity_type",
    "canonical_name",
    "authority_level",
    "source_basis",
    "status",
}

ALLOWED_ENTITY_TYPES = {
    "formal_project",
    "candidate_idea",
    "subsystem",
    "corpus_section",
    "non_project_corpus",
    "archive_bucket",
    "infrastructure_component",
}

ALLOWED_AUTHORITY_LEVELS = {"authoritative", "supporting", "inferred"}
ALLOWED_SOURCE_BASIS = {
    "folder_structure",
    "section_map",
    "project_index",
    "charter",
    "mission",
    "rag_evidence",
    "heuristic",
}
ALLOWED_STATUS = {"active", "archived", "candidate", "subsystem", "non_project", "unknown"}


def make_entity_id(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    if not slug:
        raise RuntimeError(f"Could not derive entity_id from: {text!r}")
    return slug


def load_schema(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Schema file does not exist: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema_compatibility(schema: Dict[str, Any]) -> None:
    props = set(schema.get("properties", {}).keys())
    missing = REQUIRED_SCHEMA_KEYS - props
    if missing:
        raise RuntimeError(
            f"Entity schema missing required properties for registry use: {sorted(missing)}"
        )


def list_top_level_folders(root: Path) -> List[Path]:
    if not root.exists():
        raise SystemExit(f"Raw root does not exist: {root}")
    folders = sorted(p for p in root.iterdir() if p.is_dir())
    if not folders:
        raise SystemExit(f"No top-level folders found under: {root}")
    return folders


def build_entity(folder_path: Path) -> Dict[str, Any]:
    folder_name = folder_path.name

    if folder_name not in FOLDER_POLICY:
        raise RuntimeError(f"Unknown top-level folder (not in FOLDER_POLICY): {folder_name}")

    policy = FOLDER_POLICY[folder_name]

    entity_type = policy["entity_type"]
    if entity_type not in ALLOWED_ENTITY_TYPES:
        raise RuntimeError(f"Invalid entity_type for {folder_name}: {entity_type}")

    status = policy["status"]
    if status not in ALLOWED_STATUS:
        raise RuntimeError(f"Invalid status for {folder_name}: {status}")

    canonical_name = policy["canonical_name"]
    aliases = sorted(set(policy.get("aliases", [])))

        authority_level = "authoritative"
    if entity_type == "candidate_idea":
        authority_level = "inferred"

    entity = {
        "entity_id": make_entity_id(canonical_name),
        "entity_type": entity_type,
        "canonical_name": canonical_name,
        "aliases": aliases,
        "authority_level": authority_level,
        "source_basis": ["folder_structure", "section_map"],
        "status": status,
        "parent_entity_id": None,
        "related_entity_ids": [],
        "evidence_refs": [
            {
                "source_type": "folder",
                "ref": str(folder_path),
            }
        ],
        "notes": policy.get("notes", ""),
        # registry-internal metadata
        "folder_name": folder_name,
    }

    if entity["authority_level"] not in ALLOWED_AUTHORITY_LEVELS:
        raise RuntimeError(f"Invalid authority_level for {folder_name}")

    for basis in entity["source_basis"]:
        if basis not in ALLOWED_SOURCE_BASIS:
            raise RuntimeError(f"Invalid source_basis {basis!r} for {folder_name}")

    if entity_type == "formal_project" and entity["authority_level"] != "authoritative":
        raise RuntimeError(f"formal_project must be authoritative: {folder_name}")

    return entity


def collapse_formal_projects(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}

    for entity in entities:
        folder_name = entity["folder_name"]
        family_key = COLLAPSED_PROJECT_FAMILIES.get(folder_name, entity["entity_id"])
        grouped.setdefault(family_key, []).append(entity)

    collapsed: List[Dict[str, Any]] = []

    for family_key, members in sorted(grouped.items(), key=lambda kv: kv[0]):
        if len(members) == 1 and family_key == members[0]["entity_id"]:
            entity = dict(members[0])
            entity.pop("folder_name", None)
            collapsed.append(entity)
            continue

        canonical_name = COLLAPSED_CANONICALS.get(family_key)
        if not canonical_name:
            raise RuntimeError(f"Missing collapsed canonical name for family: {family_key}")

        aliases = sorted(
            {alias for member in members for alias in member.get("aliases", [])} |
            {member["canonical_name"] for member in members}
        )
        evidence_refs = []
        notes_parts = []
        for member in members:
            evidence_refs.extend(member["evidence_refs"])
            if member.get("notes"):
                notes_parts.append(member["notes"])

        collapsed.append(
            {
                "entity_id": family_key,
                "entity_type": "formal_project",
                "canonical_name": canonical_name,
                "aliases": aliases,
                "authority_level": "authoritative",
                "source_basis": ["folder_structure", "section_map"],
                "status": "active",
                "parent_entity_id": None,
                "related_entity_ids": [],
                "evidence_refs": evidence_refs,
                "notes": "Collapsed project family from multiple authoritative folders. " + " ".join(notes_parts),
            }
        )

    return sorted(collapsed, key=lambda x: x["canonical_name"].lower())


def validate_entity_record(entity: Dict[str, Any]) -> None:
    missing = REQUIRED_SCHEMA_KEYS - set(entity.keys())
    if missing:
        raise RuntimeError(f"Entity missing required keys: {sorted(missing)}")

    if entity["entity_type"] not in ALLOWED_ENTITY_TYPES:
        raise RuntimeError(f"Invalid entity_type: {entity['entity_type']}")

    if entity["authority_level"] not in ALLOWED_AUTHORITY_LEVELS:
        raise RuntimeError(f"Invalid authority_level: {entity['authority_level']}")

    if entity["status"] not in ALLOWED_STATUS:
        raise RuntimeError(f"Invalid status: {entity['status']}")

    for basis in entity["source_basis"]:
        if basis not in ALLOWED_SOURCE_BASIS:
            raise RuntimeError(f"Invalid source_basis: {basis}")

    if entity["entity_type"] == "formal_project" and entity["authority_level"] != "authoritative":
        raise RuntimeError("formal_project must be authoritative")

    if entity["entity_type"] == "candidate_idea" and entity["authority_level"] == "authoritative":
        raise RuntimeError("candidate_idea must not be authoritative")


def make_summary(
    raw_entities: List[Dict[str, Any]],
    collapsed_entities: List[Dict[str, Any]],
) -> Dict[str, Any]:
    raw_by_type: Dict[str, int] = {}
    for entity in raw_entities:
        raw_by_type[entity["entity_type"]] = raw_by_type.get(entity["entity_type"], 0) + 1

    collapsed_formal_projects = [
        e for e in collapsed_entities if e["entity_type"] in COUNTABLE_ENTITY_TYPES
    ]

    non_countable = [
        e for e in collapsed_entities if e["entity_type"] in NON_COUNTABLE_ENTITY_TYPES
    ]

    return {
        "raw_top_level_folder_count": len(raw_entities),
        "raw_entity_counts_by_type": raw_by_type,
        "formal_project_count": len(collapsed_formal_projects),
        "formal_project_names": [e["canonical_name"] for e in collapsed_formal_projects],
        "non_countable_entities": [
            {
                "entity_type": e["entity_type"],
                "canonical_name": e["canonical_name"],
            }
            for e in non_countable
        ],
        "collapsed_project_families": [
            {
                "family_id": family_id,
                "canonical_name": COLLAPSED_CANONICALS[family_id],
                "member_folders": sorted(
                    [
                        folder_name
                        for folder_name, fam in COLLAPSED_PROJECT_FAMILIES.items()
                        if fam == family_id
                    ]
                ),
            }
            for family_id in sorted(set(COLLAPSED_PROJECT_FAMILIES.values()))
        ],
    }


def main() -> None:
    schema = load_schema(SCHEMA_PATH)
    validate_schema_compatibility(schema)

    folders = list_top_level_folders(RAW_ROOT)

    raw_entities: List[Dict[str, Any]] = []
    for folder in folders:
        raw_entities.append(build_entity(folder))

    # Hard fail if policy has extra entries not present on disk? No.
    # Missing on disk is acceptable; unknown on disk is not.
    unknown_on_disk = sorted({p.name for p in folders} - set(FOLDER_POLICY.keys()))
    if unknown_on_disk:
        raise RuntimeError(f"Unknown top-level folders on disk: {unknown_on_disk}")

    # Keep archive/non-project as-is; collapse only formal projects.
    formal_entities = [e for e in raw_entities if e["entity_type"] == "formal_project"]
    non_formal_entities = [e for e in raw_entities if e["entity_type"] != "formal_project"]

    collapsed_formal_entities = collapse_formal_projects(formal_entities)
    final_entities = sorted(
        collapsed_formal_entities + [
            {k: v for k, v in entity.items() if k != "folder_name"} for entity in non_formal_entities
        ],
        key=lambda x: (x["entity_type"], x["canonical_name"].lower()),
    )

    for entity in final_entities:
        validate_entity_record(entity)

    summary = make_summary(raw_entities, final_entities)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(final_entities, indent=2), encoding="utf-8")
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== COMPLETE ===")
    print(f"raw_top_level_folders: {len(folders)}")
    print(f"formal_projects: {summary['formal_project_count']}")
    print(f"output: {OUTPUT_PATH}")
    print(f"summary: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()