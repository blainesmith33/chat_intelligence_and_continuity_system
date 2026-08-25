#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import List

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# ============================================================
# HARDENED CHAT RAG → QDRANT LOADER
# ============================================================
# Guarantees:
# - deterministic ordering (sorted chunk files)
# - 1:1 mapping: chunk file index == embedding row index
# - full metadata payload preservation
# - traceability back to original source
# ============================================================

CHUNK_ROOT = Path("/home/kimberly/cics/corpora/chats/chunks")
EMBEDDINGS_PATH = Path("/home/kimberly/cics/corpora/chats/embeddings/chat_embeddings.npy")

COLLECTION_NAME = "chat_rag"
BATCH_SIZE = 256

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333


# ============================================================
# UTILITIES
# ============================================================

def collect_chunk_files(root: Path) -> List[Path]:
    files = sorted(p for p in root.rglob("*.txt") if p.is_file())
    if not files:
        raise RuntimeError(f"No chunk files found under {root}")
    return files


def parse_chunk_metadata(path: Path):
    """
    Extract:
    - section
    - language
    - source_file
    - chunk_index
    - source_id
    """

    parts = path.parts

    try:
        idx = parts.index("chunks")
    except ValueError:
        raise RuntimeError(f"Invalid chunk path (missing 'chunks'): {path}")

    section = parts[idx + 1]
    language = parts[idx + 2]

    filename = path.name

    # Expected format:
    # stem__sourceid__language_chunk_000123.txt
    match = re.match(r"(.+)__([a-f0-9]+)__([a-z]+)_chunk_(\d+)\.txt", filename)

    if not match:
        raise RuntimeError(f"Invalid chunk filename format: {filename}")

    stem = match.group(1)
    source_id = match.group(2)
    lang_check = match.group(3)
    chunk_index = int(match.group(4))

    if lang_check != language:
        raise RuntimeError(f"Language mismatch in filename vs path: {path}")

    return {
        "section": section,
        "language": language,
        "source_file": stem,
        "source_id": source_id,
        "chunk_index": chunk_index,
    }


def load_chunk_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


# ============================================================
# MAIN
# ============================================================

def main():
    print("=== QDRANT INGEST (HARDENED) ===")

    chunk_files = collect_chunk_files(CHUNK_ROOT)
    embeddings = np.load(EMBEDDINGS_PATH)

    if embeddings.ndim != 2:
        raise RuntimeError(f"Embeddings must be 2D, got {embeddings.shape}")

    if len(chunk_files) != embeddings.shape[0]:
        raise RuntimeError(
            f"Mismatch: {len(chunk_files)} chunk files vs {embeddings.shape[0]} embedding rows"
        )

    print(f"Chunk files: {len(chunk_files)}")
    print(f"Embeddings shape: {embeddings.shape}")

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    total = len(chunk_files)
    uploaded = 0

    for start in range(0, total, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total)
        batch_points = []

        for idx in range(start, end):
            chunk_path = chunk_files[idx]
            vector = embeddings[idx]

            meta = parse_chunk_metadata(chunk_path)
            text = load_chunk_text(chunk_path)

            payload = {
                "chunk_id": f"{meta['source_id']}_{meta['chunk_index']}",
                "section": meta["section"],
                "language": meta["language"],
                "source_file": meta["source_file"],
                "source_id": meta["source_id"],
                "chunk_index": meta["chunk_index"],
                "embedding_row_index": idx,
                "text": text,
                "chunk_path": str(chunk_path),
            }

            point = PointStruct(
                id=idx,
                vector=vector.tolist(),
                payload=payload,
            )

            batch_points.append(point)

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch_points,
        )

        uploaded = end
        print(f"[UPLOAD] {uploaded}/{total}")

    print("=== COMPLETE ===")
    print(f"Total vectors uploaded: {uploaded}")


if __name__ == "__main__":
    main()