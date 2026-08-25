from __future__ import annotations

import re
import uuid
from collections.abc import Mapping, Sequence
from typing import Any

from .hashing import blake3_hex, canonical_json_bytes


_HASH_ID_PREFIXES = {"src", "doc", "msg", "chk", "emb"}
_HASH_ID_RE = re.compile(r"^(src|doc|msg|chk|emb)_[a-f0-9]{64}$")
_ARTIFACT_ID_RE = re.compile(r"^art_[a-f0-9]{32}$")
_ENTITY_ID_RE = re.compile(r"^ent_[a-z0-9][a-z0-9._-]*$")


def _hash_id(prefix: str, payload: bytes) -> str:
    if prefix not in _HASH_ID_PREFIXES:
        raise ValueError(f"Unsupported hash ID prefix: {prefix}")
    return f"{prefix}_{blake3_hex(payload)}"


def source_id(source_format: str, exact_source_bytes: bytes) -> str:
    if not source_format.strip():
        raise ValueError("source_format must be non-empty")
    return _hash_id("src", source_format.encode("utf-8") + b"\0" + exact_source_bytes)


def document_id_from_native(
    source_format: str,
    native_object_type: str,
    native_document_id: str,
) -> str:
    parts = (source_format, native_object_type, native_document_id)
    if any(not part.strip() for part in parts):
        raise ValueError("Native document identity fields must be non-empty")
    payload = b"\0".join(part.encode("utf-8") for part in parts)
    return _hash_id("doc", payload)


def document_id_from_fingerprint(
    source_format: str,
    canonicalization_version: str,
    canonical_document: Mapping[str, Any] | Sequence[Any],
) -> str:
    if not source_format.strip() or not canonicalization_version.strip():
        raise ValueError("source_format and canonicalization_version must be non-empty")
    payload = (
        source_format.encode("utf-8")
        + b"\0"
        + canonicalization_version.encode("utf-8")
        + b"\0"
        + canonical_json_bytes(canonical_document)
    )
    return _hash_id("doc", payload)


def message_id(document_id: str, native_or_deterministic_locator: str) -> str:
    validate_hash_id(document_id, expected_prefix="doc")
    if not native_or_deterministic_locator.strip():
        raise ValueError("message locator must be non-empty")
    payload = document_id.encode("ascii") + b"\0" + native_or_deterministic_locator.encode("utf-8")
    return _hash_id("msg", payload)


def chunk_id(
    *,
    document_id: str,
    source_spans: Sequence[Mapping[str, Any]],
    content_hash: str,
    chunker_id: str,
    chunker_version: str,
    chunk_policy_hash: str,
) -> str:
    validate_hash_id(document_id, expected_prefix="doc")
    if not source_spans:
        raise ValueError("source_spans must be non-empty")
    for value, name in (
        (content_hash, "content_hash"),
        (chunker_id, "chunker_id"),
        (chunker_version, "chunker_version"),
        (chunk_policy_hash, "chunk_policy_hash"),
    ):
        if not value.strip():
            raise ValueError(f"{name} must be non-empty")

    projection = {
        "document_id": document_id,
        "source_spans": list(source_spans),
        "content_hash": content_hash,
        "chunker_id": chunker_id,
        "chunker_version": chunker_version,
        "chunk_policy_hash": chunk_policy_hash,
    }
    return _hash_id("chk", canonical_json_bytes(projection))


def embedding_build_id(
    *,
    chunk_manifest_hash: str,
    model_id: str,
    model_revision: str | None,
    vector_dimension: int,
    embedding_policy_hash: str,
    implementation_id: str,
    implementation_version: str,
) -> str:
    if vector_dimension <= 0:
        raise ValueError("vector_dimension must be > 0")
    projection = {
        "chunk_manifest_hash": chunk_manifest_hash,
        "model_id": model_id,
        "model_revision": model_revision,
        "vector_dimension": vector_dimension,
        "embedding_policy_hash": embedding_policy_hash,
        "implementation_id": implementation_id,
        "implementation_version": implementation_version,
    }
    for key, value in projection.items():
        if key == "model_revision" or key == "vector_dimension":
            continue
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be non-empty")
    return _hash_id("emb", canonical_json_bytes(projection))


def new_artifact_id() -> str:
    return f"art_{uuid.uuid4().hex}"


def validate_hash_id(value: str, *, expected_prefix: str | None = None) -> str:
    match = _HASH_ID_RE.fullmatch(value)
    if not match:
        raise ValueError(f"Invalid canonical hash ID: {value!r}")
    if expected_prefix is not None and match.group(1) != expected_prefix:
        raise ValueError(f"Expected {expected_prefix}_ ID, got {value!r}")
    return value


def validate_artifact_id(value: str) -> str:
    if not _ARTIFACT_ID_RE.fullmatch(value):
        raise ValueError(f"Invalid artifact ID: {value!r}")
    return value


def validate_entity_id(value: str) -> str:
    if not _ENTITY_ID_RE.fullmatch(value):
        raise ValueError(f"Invalid governed entity ID: {value!r}")
    return value
