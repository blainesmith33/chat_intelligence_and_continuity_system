from __future__ import annotations

from pathlib import Path


SOURCE_ID_DOMAIN = b"cics:source:v1\0"


class MissingBlake3Dependency(RuntimeError):
    pass


def _blake3_hex(data: bytes) -> str:
    try:
        import blake3
    except ImportError as exc:
        raise MissingBlake3Dependency(
            "The 'blake3' package is required for CICS identity generation."
        ) from exc

    return blake3.blake3(data).hexdigest()


def source_content_hash(data: bytes) -> str:
    """
    Hash immutable source bytes.

    This value is independent of filesystem location.
    """

    return _blake3_hex(data)


def source_id_from_bytes(data: bytes, source_format: str) -> str:
    """
    Produce the stable CICS source identity.

    Identity depends on:
    - identity-contract version
    - source format
    - immutable source bytes

    It does NOT depend on:
    - absolute path
    - username
    - machine
    - mount point
    - traversal order
    """

    normalized_format = source_format.strip().lower()

    if not normalized_format:
        raise ValueError("source_format cannot be empty")

    material = (
        SOURCE_ID_DOMAIN
        + normalized_format.encode("utf-8")
        + b"\0"
        + data
    )

    return _blake3_hex(material)


def source_id_from_path(path: Path, source_format: str) -> str:
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")

    return source_id_from_bytes(
        path.read_bytes(),
        source_format=source_format,
    )
