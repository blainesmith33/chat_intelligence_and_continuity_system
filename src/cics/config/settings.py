from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _absolute_path_from_env(name: str) -> Path:
    raw = os.environ.get(name)

    if not raw:
        raise RuntimeError(f"{name} must be set")

    path = Path(raw).expanduser()

    if not path.is_absolute():
        raise ValueError(f"{name} must be an absolute path: {raw}")

    return path.resolve(strict=False)


@dataclass(frozen=True)
class CICSSettings:
    """
    Runtime storage configuration for CICS Phase 1.

    Source archives and generated CICS runtime data are deliberately
    separate. Neither location is inferred from a username, machine,
    repository checkout, or removable-drive mount.
    """

    cics_root: Path
    source_root: Path

    embedding_model: str = "nomic-ai/nomic-embed-text-v1.5"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "chat_rag"

    @classmethod
    def from_env(cls) -> "CICSSettings":
        return cls(
            cics_root=_absolute_path_from_env("CICS_ROOT"),
            source_root=_absolute_path_from_env("CICS_SOURCE_ROOT"),
            embedding_model=os.environ.get(
                "CICS_EMBEDDING_MODEL",
                "nomic-ai/nomic-embed-text-v1.5",
            ),
            qdrant_host=os.environ.get(
                "CICS_QDRANT_HOST",
                "localhost",
            ),
            qdrant_port=int(
                os.environ.get(
                    "CICS_QDRANT_PORT",
                    "6333",
                )
            ),
            qdrant_collection=os.environ.get(
                "CICS_QDRANT_COLLECTION",
                "chat_rag",
            ),
        )

    @property
    def normalized_root(self) -> Path:
        return self.cics_root / "imports" / "normalized"

    @property
    def manifests_root(self) -> Path:
        return self.cics_root / "imports" / "manifests"

    @property
    def chunks_root(self) -> Path:
        return self.cics_root / "chunks"

    @property
    def embeddings_root(self) -> Path:
        return self.cics_root / "embeddings"

    @property
    def qdrant_root(self) -> Path:
        return self.cics_root / "vector_store" / "qdrant"

    @property
    def retrieval_root(self) -> Path:
        return self.cics_root / "retrieval"

    @property
    def runtime_root(self) -> Path:
        return self.cics_root / "runtime"
