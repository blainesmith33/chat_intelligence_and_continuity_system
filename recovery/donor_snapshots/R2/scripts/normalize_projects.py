#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set

INPUT_PATH = Path("/home/kimberly/cics/analysis/project_candidates.json")
OUTPUT_PATH = Path("/home/kimberly/cics/analysis/project_candidates_normalized.json")

# ------------------------------------------------------------
# HARD FILTERS
# ------------------------------------------------------------

GENERIC_BLACKLIST = {
    "",
    "project",
    "system",
    "engine",
    "framework",
    "pipeline",
    "platform",
    "layer",
    "architecture",
    "program",
    "model",
    "tool",
    "tools",
    "process",
    "workflow",
    "structure",
    "logic",
    "design",
    "implementation",
    "analysis",
    "approval",
    "safety",
    "archive",
    "catalog",
    "operator",
    "doctor",
    "index",
    "continuation",
    "continuity",
    "setup",
    "build",
    "progress",
    "handoff",
    "validation",
    "chat",
    "local",
    "remote",
    "runtime",
    "governance",
    "policy",
    "quality",
    "identity",
    "execution",
    "retrieval",
    "knowledge",
    "memory",
    "idea",
    "ideas",
}

EXACT_ALIAS_MAP = {
    "ai diagnostician": "DAIRP — Deterministic AI Inspection & Remediation Platform",
    "ai computer diagnostician": "DAIRP — Deterministic AI Inspection & Remediation Platform",
    "dairp": "DAIRP — Deterministic AI Inspection & Remediation Platform",

    "aletheia forensis": "Aletheia Forensis",
    "reel forensics engine": "Aletheia Forensis",

    "cics": "CICS — Chat Intelligence & Continuity System",
    "chat intelligence continuity system": "CICS — Chat Intelligence & Continuity System",

    "dafos": "DAFOS — Deterministic AI Financial Operations System",
    "deterministic ai financial operations system": "DAFOS — Deterministic AI Financial Operations System",

    "acis": "ACIS",
    "cadance ai": "ACIS",
    "aletheia cadentia": "ACIS",

    "alip": "ALIP",
    "ai infrastructure provisioning platform": "ALIP",
    "ai lab infrastructure program": "ALIP",

    "campaign master": "Campaign Master",
    "narraiator": "NarrAIator",
    "blaineai website": "blaineai_website",
    "blaineai.me website": "blaineai_website",
    "blaineai": "blaineai_website",

    "imperium aletheiae": "Imperium Aletheiae",
    "umb": "UMB — Cross-Project Governance Framework",
    "cross project governance framework": "UMB — Cross-Project Governance Framework",
}

MIN_MENTION_COUNT = 2


def normalize_text(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("_", " ")
    s = s.replace("-", " ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    return s.strip()


def canonicalize_name(name: str) -> str | None:
    raw = normalize_text(name)
    if not raw:
        return None

    if raw in GENERIC_BLACKLIST:
        return None

    if raw in EXACT_ALIAS_MAP:
        return EXACT_ALIAS_MAP[raw]

    # reject very short weak names unless uppercase acronym-like original
    if len(raw) < 4:
        return None

    # reject generic 1-word weak tokens
    if " " not in raw and raw in GENERIC_BLACKLIST:
        return None

    # convert cleaned raw back to title-ish fallback
    return " ".join(word.capitalize() for word in raw.split())


def dedupe_evidence(evidence: List[dict]) -> List[dict]:
    seen: Set[tuple] = set()
    out: List[dict] = []

    for item in evidence:
        key = (
            item.get("chunk_id"),
            item.get("source_file"),
            item.get("section"),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(item)

    return out


def choose_display_name(aliases: List[str], canonical: str) -> str:
    # prefer longest alias with strong formatting if canonical is fallback-ish
    if canonical in EXACT_ALIAS_MAP.values():
        return canonical

    ranked = sorted(
        aliases,
        key=lambda x: (len(x), sum(1 for c in x if c.isupper())),
        reverse=True,
    )
    return ranked[0] if ranked else canonical


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"Input file does not exist: {INPUT_PATH}")

    raw_candidates = json.loads(INPUT_PATH.read_text(encoding="utf-8"))

    grouped: Dict[str, dict] = defaultdict(lambda: {
        "canonical_name": "",
        "aliases": set(),
        "evidence": [],
        "mention_count": 0,
        "sections": set(),
        "source_files": set(),
    })

    total_in = 0
    rejected = 0

    for item in raw_candidates:
        total_in += 1
        raw_name = item.get("name", "")
        aliases = item.get("aliases", [])
        mention_count = int(item.get("mention_count", 0))
        evidence = item.get("evidence", [])

        all_names = [raw_name] + list(aliases)

        canonical_names: Set[str] = set()
        for name in all_names:
            canonical = canonicalize_name(name)
            if canonical:
                canonical_names.add(canonical)

        if not canonical_names:
            rejected += 1
            continue

        # choose one canonical bucket per record:
        # prefer mapped exact alias if present, else longest canonical
        chosen = sorted(
            canonical_names,
            key=lambda x: (
                x in EXACT_ALIAS_MAP.values(),
                len(x),
            ),
            reverse=True,
        )[0]

        bucket = grouped[chosen]
        bucket["canonical_name"] = chosen
        bucket["mention_count"] += mention_count

        for alias in all_names:
            if alias and canonicalize_name(alias):
                bucket["aliases"].add(alias)

        for ev in evidence:
            bucket["evidence"].append(ev)
            if ev.get("section"):
                bucket["sections"].add(ev["section"])
            if ev.get("source_file"):
                bucket["source_files"].add(ev["source_file"])

    normalized: List[dict] = []

    for canonical, data in grouped.items():
        deduped_evidence = dedupe_evidence(data["evidence"])
        unique_mentions = len(deduped_evidence)

        if unique_mentions < MIN_MENTION_COUNT and canonical not in EXACT_ALIAS_MAP.values():
            rejected += 1
            continue

        aliases = sorted(data["aliases"])
        display_name = choose_display_name(aliases, canonical)

        normalized.append({
            "project_id": re.sub(r"[^a-z0-9]+", "_", canonical.lower()).strip("_"),
            "name": display_name,
            "canonical_name": canonical,
            "aliases": aliases,
            "unique_evidence_count": unique_mentions,
            "raw_mention_count": data["mention_count"],
            "sections": sorted(data["sections"]),
            "source_files": sorted(data["source_files"]),
            "evidence": deduped_evidence,
        })

    normalized.sort(
        key=lambda x: (x["unique_evidence_count"], x["raw_mention_count"], x["name"]),
        reverse=True,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(normalized, indent=2), encoding="utf-8")

    print("=== COMPLETE ===")
    print(f"raw_candidates_in: {total_in}")
    print(f"normalized_projects: {len(normalized)}")
    print(f"rejected_candidates: {rejected}")
    print(f"output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()