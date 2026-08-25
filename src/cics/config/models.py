from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PathsConfig:
    data_root: Path
    runtime_root: Path


@dataclass(frozen=True)
class ArtifactsConfig:
    staging_root: Path
    committed_root: Path


@dataclass(frozen=True)
class CorpusConfig:
    manifests_root: Path


@dataclass(frozen=True)
class ChunkingConfig:
    chunker_id: str
    chunker_version: str


@dataclass(frozen=True)
class EmbeddingsConfig:
    model_id: str
    model_revision: str | None
    vector_dimension: int
    vector_dtype: str
    device: str
    normalize: bool


@dataclass(frozen=True)
class VectorStoreConfig:
    provider: str
    host: str
    port: int
    collection_logical_name: str
    distance_metric: str


@dataclass(frozen=True)
class RegistryConfig:
    policy_path: Path


@dataclass(frozen=True)
class RuntimeConfig:
    checkpoint_root: Path
    log_root: Path


@dataclass(frozen=True)
class CICSConfig:
    paths: PathsConfig
    artifacts: ArtifactsConfig
    corpus: CorpusConfig
    chunking: ChunkingConfig
    embeddings: EmbeddingsConfig
    vector_store: VectorStoreConfig
    registry: RegistryConfig
    runtime: RuntimeConfig

    def processing_policy_projection(self) -> dict[str, object]:
        """Return only output-semantic settings suitable for canonical hashing.

        Deployment paths, hosts, ports, device selection, checkpoints, and logs
        are deliberately excluded.
        """

        return {
            "chunking": {
                "chunker_id": self.chunking.chunker_id,
                "chunker_version": self.chunking.chunker_version,
            },
            "embeddings": {
                "model_id": self.embeddings.model_id,
                "model_revision": self.embeddings.model_revision,
                "vector_dimension": self.embeddings.vector_dimension,
                "vector_dtype": self.embeddings.vector_dtype,
                "normalize": self.embeddings.normalize,
            },
            "vector_store": {
                "distance_metric": self.vector_store.distance_metric,
            },
        }
