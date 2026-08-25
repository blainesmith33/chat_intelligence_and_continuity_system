#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from typing import Dict, List

from qdrant_client import QdrantClient

COLLECTION = "chat_rag"
HOST = "localhost"
PORT = 6333

OUTPUT_PATH = "/home/kimberly/cics/analysis/project_candidates.json"

# ------------------------------------------------------------
# DETECTION PATTERNS (LOOSE MODE)
# ------------------------------------------------------------

PROJECT_PATTERNS = [
    r"\bi want to build\b",
    r"\bi am building\b",
    r"\bthis system\b",
    r"\bproject\b",
    r"\bplatform\b",
    r"\bframework\b",
    r"\bengine\b",
    r"\bpipeline\b",
    r"\bwe should build\b",
    r"\bi could build\b",
]

NAME_PATTERNS = [
    r"\b[A-Z]{2,}[-_ ]?[A-Z0-9]{2,}\b",  # e.g., DAFOS, CICS
    r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",      # e.g., AI Diagnostician
]

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def looks_like_project(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in PROJECT_PATTERNS)


def extract_names(text: str) -> List[str]:
    names = []
    for pattern in NAME_PATTERNS:
        matches = re.findall(pattern, text)
        names.extend(matches)
    return list(set(names))


def normalize_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    client = QdrantClient(host=HOST, port=PORT)

    print("=== PROJECT EXTRACTION (FULL SCAN) ===")

    offset = None
    limit = 256

    projects: Dict[str, dict] = {}

    total_scanned = 0
    total_candidates = 0

    while True:
        records, offset = client.scroll(
            collection_name=COLLECTION,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        if not records:
            break

        for r in records:
            total_scanned += 1
            payload = r.payload or {}
            text = payload.get("text", "")

            if not text:
                continue

            if not looks_like_project(text):
                continue

            total_candidates += 1

            names = extract_names(text)
            if not names:
                names = ["unnamed_project"]

            for name in names:
                key = normalize_key(name)

                if key not in projects:
                    projects[key] = {
                        "project_id": key,
                        "name": name,
                        "aliases": set(),
                        "evidence": [],
                        "count": 0,
                    }

                projects[key]["aliases"].add(name)
                projects[key]["evidence"].append({
                    "chunk_id": payload.get("chunk_id"),
                    "source_file": payload.get("source_file"),
                    "section": payload.get("section"),
                })
                projects[key]["count"] += 1

        print(f"[scan] {total_scanned} scanned | {total_candidates} candidates")

        if offset is None:
            break

    # finalize structure
    output = []
    for p in projects.values():
        output.append({
            "project_id": p["project_id"],
            "name": p["name"],
            "aliases": list(p["aliases"]),
            "mention_count": p["count"],
            "evidence": p["evidence"],
        })

    # sort by mention count
    output.sort(key=lambda x: x["mention_count"], reverse=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print("\n=== COMPLETE ===")
    print(f"scanned_chunks: {total_scanned}")
    print(f"project_candidates: {len(output)}")
    print(f"output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()