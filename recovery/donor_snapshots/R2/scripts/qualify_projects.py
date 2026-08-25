#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Set

INPUT_PATH = Path("/home/kimberly/cics/analysis/project_candidates_normalized.json")
OUTPUT_PATH = Path("/home/kimberly/cics/analysis/project_inventory_strict.json")

# ------------------------------------------------------------
# HARD QUALIFICATION POLICY
# ------------------------------------------------------------

# Candidate survives if ANY of the following is true:
MIN_UNIQUE_EVIDENCE = 3
MIN_UNIQUE_SOURCE_FILES = 2

# Strong file/title hints that indicate formalization or real project structure.
STRONG_FILE_PATTERNS = [
    r"project[_ -]?index",
    r"project[_ -]?charter",
    r"charter",
    r"mission",
    r"handoff",
    r"continuity",
    r"scope",
    r"architecture",
    r"system",
    r"framework",
    r"engine",
    r"platform",
]

# Strong naming patterns that suggest project/system identity.
STRONG_NAME_PATTERNS = [
    r"\b[A-Z]{2,}[A-Z0-9_-]*\b",                         # CICS, DAFOS, ACIS, UMB
    r"\bDeterministic\b",
    r"\bAletheia\b",
    r"\bImperium\b",
    r"\bCampaign Master\b",
    r"\bNarrAIator\b",
    r"\bblaineai\b",
]

# Canonical names you definitely want preserved if found.
PINNED_CANONICALS = {
    "CICS — Chat Intelligence & Continuity System",
    "DAIRP — Deterministic AI Inspection & Remediation Platform",
    "DAFOS — Deterministic AI Financial Operations System",
    "Aletheia Forensis",
    "Imperium Aletheiae",
    "ALIP",
    "ACIS",
    "Campaign Master",
    "NarrAIator",
    "blaineai_website",
    "UMB — Cross-Project Governance Framework",
}

# Weak/generic names that should still die even if they slipped through normalization.
WEAK_NAME_PATTERNS = [
    r"^Chat \d+[A-Za-z]?$",
    r"^S\d+[A-Za-z]?$",
    r"^Phase \d+",
    r"^Index$",
    r"^Continuation$",
    r"^Handoff$",
    r"^Validation$",
    r"^Progress$",
    r"^Setup$",
    r"^Build$",
    r"^Architecture$",
    r"^System$",
    r"^Framework$",
    r"^Platform$",
    r"^Engine$",
    r"^Pipeline$",
    r"^Layer$",
    r"^Operator$",
    r"^Doctor$",
]


def load_json(path: Path) -> List[dict]:
    if not path.exists():
        raise SystemExit(f"Input file does not exist: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def matches_any(text: str, patterns: List[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def has_strong_name_signal(name: str, aliases: List[str]) -> bool:
    pool = [name] + aliases
    return any(matches_any(item, STRONG_NAME_PATTERNS) for item in pool if item)


def has_weak_name_signal(name: str, aliases: List[str]) -> bool:
    pool = [name] + aliases
    return any(matches_any(item, WEAK_NAME_PATTERNS) for item in pool if item)


def has_strong_source_signal(source_files: List[str]) -> bool:
    return any(matches_any(src, STRONG_FILE_PATTERNS) for src in source_files)


def qualifies(candidate: dict) -> tuple[bool, List[str]]:
    reasons: List[str] = []

    canonical = candidate.get("canonical_name", "") or candidate.get("name", "")
    aliases = candidate.get("aliases", [])
    unique_evidence_count = int(candidate.get("unique_evidence_count", 0))
    source_files = candidate.get("source_files", [])
    sections = candidate.get("sections", [])

    unique_source_file_count = len(source_files)
    unique_section_count = len(sections)

    pinned = canonical in PINNED_CANONICALS or candidate.get("name", "") in PINNED_CANONICALS
    if pinned:
        reasons.append("pinned_canonical")

    if unique_evidence_count >= MIN_UNIQUE_EVIDENCE:
        reasons.append(f"unique_evidence>={MIN_UNIQUE_EVIDENCE}")

    if unique_source_file_count >= MIN_UNIQUE_SOURCE_FILES:
        reasons.append(f"unique_source_files>={MIN_UNIQUE_SOURCE_FILES}")

    if has_strong_name_signal(candidate.get("name", ""), aliases):
        reasons.append("strong_name_signal")

    if has_strong_source_signal(source_files):
        reasons.append("strong_source_signal")

    if unique_section_count >= 2:
        reasons.append("cross_section_presence")

    weak_name = has_weak_name_signal(candidate.get("name", ""), aliases)

    # Hard rejection only if candidate is weak and has no pinned status.
    if weak_name and not pinned:
        if unique_evidence_count < 5 and unique_source_file_count < 3:
            return False, ["weak_name_signal"]

    # Final qualification rule:
    # - pinned survives
    # - otherwise require at least 2 strong reasons
    if pinned:
        return True, reasons

    if len(reasons) >= 2:
        return True, reasons

    return False, reasons if reasons else ["insufficient_evidence"]


def make_quality_tier(candidate: dict, reasons: List[str]) -> str:
    ue = int(candidate.get("unique_evidence_count", 0))
    usf = len(candidate.get("source_files", []))
    pinned = "pinned_canonical" in reasons

    if pinned or (ue >= 8 and usf >= 3):
        return "high"
    if ue >= 4 or usf >= 2:
        return "medium"
    return "low"


def main() -> None:
    candidates = load_json(INPUT_PATH)

    qualified: List[dict] = []
    rejected: List[dict] = []

    for candidate in candidates:
        ok, reasons = qualifies(candidate)

        enriched = {
            "project_id": candidate.get("project_id"),
            "name": candidate.get("name"),
            "canonical_name": candidate.get("canonical_name"),
            "aliases": candidate.get("aliases", []),
            "unique_evidence_count": candidate.get("unique_evidence_count", 0),
            "raw_mention_count": candidate.get("raw_mention_count", 0),
            "sections": candidate.get("sections", []),
            "source_files": candidate.get("source_files", []),
            "evidence": candidate.get("evidence", []),
            "qualification_reasons": reasons,
        }

        if ok:
            enriched["qualification_tier"] = make_quality_tier(candidate, reasons)
            qualified.append(enriched)
        else:
            rejected.append(enriched)

    qualified.sort(
        key=lambda x: (
            {"high": 3, "medium": 2, "low": 1}.get(x["qualification_tier"], 0),
            x["unique_evidence_count"],
            len(x["source_files"]),
            x["name"] or "",
        ),
        reverse=True,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(qualified, indent=2), encoding="utf-8")

    rejected_path = OUTPUT_PATH.with_name("project_inventory_rejected.json")
    rejected_path.write_text(json.dumps(rejected, indent=2), encoding="utf-8")

    print("=== COMPLETE ===")
    print(f"normalized_candidates_in: {len(candidates)}")
    print(f"qualified_projects: {len(qualified)}")
    print(f"rejected_candidates: {len(rejected)}")
    print(f"output: {OUTPUT_PATH}")
    print(f"rejected_output: {rejected_path}")


if __name__ == "__main__":
    main()