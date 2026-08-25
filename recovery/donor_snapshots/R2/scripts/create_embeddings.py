#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Sequence

import numpy as np
from numpy.lib.format import open_memmap
from sentence_transformers import SentenceTransformer


DEFAULT_CHUNK_DIR = Path("~/cics/corpora/coding/chunks").expanduser()
DEFAULT_OUTPUT_FILE = Path("~/cics/corpora/coding/embeddings/coding_embeddings.npy").expanduser()
DEFAULT_CHECKPOINT_FILE = Path("~/cics/runtime/embedding_checkpoint.json").expanduser()

DEFAULT_MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"
DEFAULT_VECTOR_DIM = 768

PREFERRED_BATCH_SIZE = 32
FALLBACK_BATCH_SIZES = (32, 16, 8)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministically generate embeddings for chunk .txt files and "
            "persist them to a single .npy matrix with checkpoint resume."
        )
    )
    parser.add_argument(
        "--chunk-dir",
        type=Path,
        default=DEFAULT_CHUNK_DIR,
        help=f"Directory containing chunk .txt files recursively (default: {DEFAULT_CHUNK_DIR})",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output .npy embedding matrix path (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "--checkpoint-file",
        type=Path,
        default=DEFAULT_CHECKPOINT_FILE,
        help=f"Checkpoint JSON path (default: {DEFAULT_CHECKPOINT_FILE})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL_NAME,
        help=f"Embedding model name (default: {DEFAULT_MODEL_NAME})",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=PREFERRED_BATCH_SIZE,
        help=f"Preferred batch size (default: {PREFERRED_BATCH_SIZE})",
    )
    parser.add_argument(
        "--expected-count",
        type=int,
        default=None,
        help="Optional authoritative expected chunk count. Hard-fails on mismatch.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help='Device for SentenceTransformer (default: "cpu")',
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Ignore existing checkpoint/output and start from zero.",
    )
    return parser.parse_args()


def atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        dir=path.parent,
        delete=False,
        encoding="utf-8",
    ) as tmp:
        json.dump(payload, tmp, indent=2, sort_keys=True)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def collect_chunk_files(chunk_dir: Path) -> List[Path]:
    if not chunk_dir.exists():
        raise FileNotFoundError(f"Chunk directory does not exist: {chunk_dir}")
    if not chunk_dir.is_dir():
        raise NotADirectoryError(f"Chunk path is not a directory: {chunk_dir}")

    chunk_files = sorted(
        p for p in chunk_dir.rglob("*.txt")
        if p.is_file()
    )

    if not chunk_files:
        raise RuntimeError(f"No .txt chunk files found recursively in {chunk_dir}")

    return chunk_files


def read_checkpoint(path: Path) -> Dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_checkpoint(
    checkpoint: Dict[str, Any],
    model_name: str,
    output_file: Path,
    chunk_count: int,
    vector_dim: int,
) -> int:
    required_keys = {
        "model_name",
        "output_file",
        "chunk_count",
        "vector_dim",
        "next_index",
    }
    missing = required_keys - set(checkpoint)
    if missing:
        raise RuntimeError(f"Checkpoint missing required keys: {sorted(missing)}")

    if checkpoint["model_name"] != model_name:
        raise RuntimeError(
            f"Checkpoint model mismatch: {checkpoint['model_name']} != {model_name}"
        )

    if Path(checkpoint["output_file"]).expanduser() != output_file:
        raise RuntimeError(
            f"Checkpoint output mismatch: {checkpoint['output_file']} != {output_file}"
        )

    if int(checkpoint["chunk_count"]) != chunk_count:
        raise RuntimeError(
            f"Checkpoint chunk_count mismatch: {checkpoint['chunk_count']} != {chunk_count}"
        )

    if int(checkpoint["vector_dim"]) != vector_dim:
        raise RuntimeError(
            f"Checkpoint vector_dim mismatch: {checkpoint['vector_dim']} != {vector_dim}"
        )

    next_index = int(checkpoint["next_index"])
    if next_index < 0 or next_index > chunk_count:
        raise RuntimeError(
            f"Checkpoint next_index out of range: {next_index} for chunk_count={chunk_count}"
        )

    return next_index


def read_chunk_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict").strip()


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def create_or_open_matrix(
    output_file: Path,
    chunk_count: int,
    vector_dim: int,
    rebuild: bool,
) -> np.memmap:
    ensure_parent_dir(output_file)

    if rebuild:
        if output_file.exists():
            output_file.unlink()
        mode = "w+"
    else:
        mode = "r+" if output_file.exists() else "w+"

    return open_memmap(
        filename=str(output_file),
        mode=mode,
        dtype=np.float32,
        shape=(chunk_count, vector_dim),
    )


def load_model(model_name: str, device: str) -> SentenceTransformer:
    return SentenceTransformer(
        model_name,
        trust_remote_code=True,
        device=device,
    )


def infer_vector_dim(
    model: SentenceTransformer,
    sample_text: str,
) -> int:
    sample_embedding = model.encode(
        [sample_text],
        batch_size=1,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=False,
    )
    if sample_embedding.ndim != 2 or sample_embedding.shape[0] != 1:
        raise RuntimeError(
            f"Unexpected sample embedding shape: {sample_embedding.shape}"
        )
    return int(sample_embedding.shape[1])


def build_batch_candidates(preferred_batch_size: int) -> List[int]:
    candidates: List[int] = []
    if preferred_batch_size >= 1:
        candidates.append(preferred_batch_size)
    for size in FALLBACK_BATCH_SIZES:
        if size not in candidates:
            candidates.append(size)
    candidates = [size for size in candidates if size >= 1]
    return candidates


def is_memory_related_error(exc: BaseException) -> bool:
    if isinstance(exc, MemoryError):
        return True

    msg = str(exc).lower()
    memory_markers = (
        "out of memory",
        "oom",
        "cannot allocate memory",
        "std::bad_alloc",
        "not enough memory",
        "allocation",
    )
    return any(marker in msg for marker in memory_markers)


def encode_with_fallback(
    model: SentenceTransformer,
    texts: Sequence[str],
    preferred_batch_size: int,
) -> tuple[np.ndarray, int]:
    last_exc: BaseException | None = None

    for candidate_size in build_batch_candidates(preferred_batch_size):
        try:
            embeddings = model.encode(
                list(texts),
                batch_size=candidate_size,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=False,
            )
            return embeddings, candidate_size
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if not is_memory_related_error(exc) or candidate_size <= 8:
                raise
            gc.collect()

    if last_exc is not None:
        raise last_exc

    raise RuntimeError("encode_with_fallback failed without raising a concrete exception")


def write_checkpoint(
    checkpoint_file: Path,
    model_name: str,
    output_file: Path,
    chunk_count: int,
    vector_dim: int,
    next_index: int,
) -> None:
    payload = {
        "model_name": model_name,
        "output_file": str(output_file),
        "chunk_count": chunk_count,
        "vector_dim": vector_dim,
        "next_index": next_index,
    }
    atomic_write_json(checkpoint_file, payload)


def main() -> int:
    args = parse_args()

    chunk_dir = args.chunk_dir.expanduser()
    output_file = args.output_file.expanduser()
    checkpoint_file = args.checkpoint_file.expanduser()
    model_name = args.model
    preferred_batch_size = int(args.batch_size)
    device = args.device

    if preferred_batch_size < 1:
        raise ValueError("--batch-size must be >= 1")

    chunk_files = collect_chunk_files(chunk_dir)
    chunk_count = len(chunk_files)

    if args.expected_count is not None and chunk_count != args.expected_count:
        raise RuntimeError(
            f"Authoritative expected_count mismatch: discovered {chunk_count}, "
            f"expected {args.expected_count}"
        )

    print(f"[embed] chunk_dir={chunk_dir}")
    print(f"[embed] output_file={output_file}")
    print(f"[embed] checkpoint_file={checkpoint_file}")
    print(f"[embed] model={model_name}")
    print(f"[embed] device={device}")
    print(f"[embed] discovered_chunk_count={chunk_count}")
    print(f"[embed] preferred_batch_size={preferred_batch_size}")

    if args.rebuild:
        print("[embed] rebuild mode enabled")
        if checkpoint_file.exists():
            checkpoint_file.unlink()

    if not output_file.parent.exists():
        output_file.parent.mkdir(parents=True, exist_ok=True)
    if not checkpoint_file.parent.exists():
        checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

    model = load_model(model_name, device=device)

    sample_text = read_chunk_text(chunk_files[0])
    vector_dim = infer_vector_dim(model, sample_text)

    if vector_dim != DEFAULT_VECTOR_DIM:
        raise RuntimeError(
            f"Model vector dimension mismatch: got {vector_dim}, expected {DEFAULT_VECTOR_DIM}"
        )

    next_index = 0
    checkpoint = read_checkpoint(checkpoint_file)
    if checkpoint is not None and not args.rebuild:
        next_index = validate_checkpoint(
            checkpoint=checkpoint,
            model_name=model_name,
            output_file=output_file,
            chunk_count=chunk_count,
            vector_dim=vector_dim,
        )
        print(f"[embed] resuming from checkpoint next_index={next_index}")

    matrix = create_or_open_matrix(
        output_file=output_file,
        chunk_count=chunk_count,
        vector_dim=vector_dim,
        rebuild=args.rebuild,
    )

    if next_index >= chunk_count:
        print("[embed] embeddings already complete according to checkpoint")
        return 0

    for start in range(next_index, chunk_count, preferred_batch_size):
        end = min(start + preferred_batch_size, chunk_count)
        batch_paths = chunk_files[start:end]
        batch_texts = [read_chunk_text(path) for path in batch_paths]

        embeddings, actual_batch_size = encode_with_fallback(
            model=model,
            texts=batch_texts,
            preferred_batch_size=preferred_batch_size,
        )

        if embeddings.ndim != 2:
            raise RuntimeError(f"Unexpected embedding rank: {embeddings.ndim}")
        if embeddings.shape[0] != len(batch_texts):
            raise RuntimeError(
                f"Embedding row mismatch: got {embeddings.shape[0]}, expected {len(batch_texts)}"
            )
        if embeddings.shape[1] != vector_dim:
            raise RuntimeError(
                f"Embedding dimension mismatch: got {embeddings.shape[1]}, expected {vector_dim}"
            )

        matrix[start:end] = embeddings.astype(np.float32, copy=False)
        matrix.flush()

        write_checkpoint(
            checkpoint_file=checkpoint_file,
            model_name=model_name,
            output_file=output_file,
            chunk_count=chunk_count,
            vector_dim=vector_dim,
            next_index=end,
        )

        print(
            f"[embed] wrote batch start={start} end={end} "
            f"done={end}/{chunk_count} actual_batch_size={actual_batch_size}"
        )

        gc.collect()

    print("[embed] completed successfully")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n[embed] interrupted", file=sys.stderr)
        raise SystemExit(130)