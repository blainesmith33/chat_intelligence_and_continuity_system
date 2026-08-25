#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Union

import blake3


PathLike = Union[str, Path]


def _to_path(p: PathLike) -> Path:
    if isinstance(p, Path):
        return p
    return Path(p)


def normalize_path(p: PathLike) -> str:
    """
    Apply canonical path normalization rules:

    - absolute path REQUIRED
    - resolve symlinks
    - normalize separators to '/'
    - preserve case
    - remove trailing slash
    - no relative paths allowed
    """
    path = _to_path(p).expanduser().resolve()

    if not path.is_absolute():
        raise ValueError(f"Path must be absolute: {p}")

    normalized = path.as_posix()

    if normalized != "/" and normalized.endswith("/"):
        normalized = normalized.rstrip("/")

    return normalized


def blake3_hex(data: bytes) -> str:
    return blake3.blake3(data).hexdigest()


def doc_id_from_path(p: PathLike) -> str:
    """
    doc_id = blake3(normalized_absolute_path)
    """
    normalized = normalize_path(p)
    return blake3_hex(normalized.encode("utf-8"))


def file_hash_from_path(p: PathLike) -> str:
    """
    file_hash = blake3(file_bytes)
    """
    path = _to_path(p).expanduser().resolve()

    if not path.is_file():
        raise ValueError(f"Not a file: {p}")

    h = blake3.blake3()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_size_bytes(p: PathLike) -> int:
    path = _to_path(p).expanduser().resolve()

    if not path.is_file():
        raise ValueError(f"Not a file: {p}")

    return path.stat().st_size


def manifest_hash_from_file(p: PathLike) -> str:
    """
    manifest_hash = blake3(bytes_of_sources_manifest.jsonl)
    """
    path = _to_path(p).expanduser().resolve()

    if not path.is_file():
        raise ValueError(f"Manifest not found: {p}")

    data = path.read_bytes()
    return blake3_hex(data)


def config_hash_from_file(p: PathLike) -> str:
    """
    config_hash = blake3(bytes_of_canonical_control_layer_config.json)
    """
    path = _to_path(p).expanduser().resolve()

    if not path.is_file():
        raise ValueError(f"Config not found: {p}")

    data = path.read_bytes()
    return blake3_hex(data)


def snapshot_id(manifest_hash: str, config_hash: str) -> str:
    """
    snapshot_id = blake3(manifest_hash + ":" + config_hash)
    """
    combined = f"{manifest_hash}:{config_hash}".encode("utf-8")
    return blake3_hex(combined)
