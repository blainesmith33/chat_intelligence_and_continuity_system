from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import blake3


HASH_HEX_LENGTH = 64


def blake3_hex(data: bytes) -> str:
    return blake3.blake3(data).hexdigest()


def hash_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    resolved = Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(f"Not a file: {resolved}")

    digest = blake3.blake3()
    with resolved.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize a policy/identity projection deterministically.

    Record manifests use their schema-defined field order. This helper is for
    hash projections whose contract declares object-key order insignificant.
    """

    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def hash_canonical_json(value: Any) -> str:
    return blake3_hex(canonical_json_bytes(value))
