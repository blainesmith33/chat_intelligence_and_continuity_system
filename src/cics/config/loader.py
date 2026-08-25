from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any, Mapping

from .models import (
    ArtifactsConfig,
    ChunkingConfig,
    CICSConfig,
    CorpusConfig,
    EmbeddingsConfig,
    PathsConfig,
    RegistryConfig,
    RuntimeConfig,
    VectorStoreConfig,
)


class ConfigError(ValueError):
    """Raised when deployment configuration violates the canonical contract."""


_TOP_LEVEL_KEYS = {
    "paths",
    "artifacts",
    "corpus",
    "chunking",
    "embeddings",
    "vector_store",
    "registry",
    "runtime",
}

_SECTION_KEYS = {
    "paths": {"data_root", "runtime_root"},
    "artifacts": {"staging_root", "committed_root"},
    "corpus": {"manifests_root"},
    "chunking": {"chunker_id", "chunker_version"},
    "embeddings": {
        "model_id",
        "model_revision",
        "vector_dimension",
        "vector_dtype",
        "device",
        "normalize",
    },
    "vector_store": {
        "provider",
        "host",
        "port",
        "collection_logical_name",
        "distance_metric",
    },
    "registry": {"policy_path"},
    "runtime": {"checkpoint_root", "log_root"},
}


def _reject_unknown_keys(data: Mapping[str, Any], allowed: set[str], where: str) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ConfigError(f"Unknown configuration keys in {where}: {unknown}")


def _require_section(data: Mapping[str, Any], section: str) -> Mapping[str, Any]:
    value = data.get(section)
    if not isinstance(value, Mapping):
        raise ConfigError(f"Missing or invalid [{section}] configuration section")
    _reject_unknown_keys(value, _SECTION_KEYS[section], f"[{section}]")
    return value


def _require_str(section: Mapping[str, Any], key: str, where: str) -> str:
    value = section.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{where}.{key} must be a non-empty string")
    return value


def _optional_str(section: Mapping[str, Any], key: str, where: str) -> str | None:
    value = section.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{where}.{key} must be null/omitted or a non-empty string")
    return value


def _require_int(section: Mapping[str, Any], key: str, where: str, *, minimum: int = 0) -> int:
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ConfigError(f"{where}.{key} must be an integer >= {minimum}")
    return value


def _require_bool(section: Mapping[str, Any], key: str, where: str) -> bool:
    value = section.get(key)
    if not isinstance(value, bool):
        raise ConfigError(f"{where}.{key} must be a boolean")
    return value


def _resolve_path(raw: str, base_dir: Path) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def _path(section: Mapping[str, Any], key: str, where: str, base_dir: Path) -> Path:
    return _resolve_path(_require_str(section, key, where), base_dir)


def load_config(path: str | Path | None = None) -> CICSConfig:
    """Load strict TOML deployment configuration.

    If *path* is omitted, ``CICS_CONFIG`` selects the deployment file. There is
    intentionally no fallback to a historical ``~/cics`` or machine-specific
    directory.
    """

    selected = Path(path).expanduser() if path is not None else None
    if selected is None:
        env_value = os.environ.get("CICS_CONFIG")
        if not env_value:
            raise ConfigError("No configuration path supplied and CICS_CONFIG is unset")
        selected = Path(env_value).expanduser()

    selected = selected.resolve()
    if not selected.is_file():
        raise ConfigError(f"Configuration file not found: {selected}")

    try:
        with selected.open("rb") as handle:
            raw = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Invalid TOML in {selected}: {exc}") from exc

    if not isinstance(raw, Mapping):
        raise ConfigError("Configuration root must be a TOML table")

    _reject_unknown_keys(raw, _TOP_LEVEL_KEYS, "root")
    missing_sections = sorted(_TOP_LEVEL_KEYS - set(raw))
    if missing_sections:
        raise ConfigError(f"Missing required configuration sections: {missing_sections}")

    base_dir = selected.parent

    paths = _require_section(raw, "paths")
    artifacts = _require_section(raw, "artifacts")
    corpus = _require_section(raw, "corpus")
    chunking = _require_section(raw, "chunking")
    embeddings = _require_section(raw, "embeddings")
    vector_store = _require_section(raw, "vector_store")
    registry = _require_section(raw, "registry")
    runtime = _require_section(raw, "runtime")

    return CICSConfig(
        paths=PathsConfig(
            data_root=_path(paths, "data_root", "paths", base_dir),
            runtime_root=_path(paths, "runtime_root", "paths", base_dir),
        ),
        artifacts=ArtifactsConfig(
            staging_root=_path(artifacts, "staging_root", "artifacts", base_dir),
            committed_root=_path(artifacts, "committed_root", "artifacts", base_dir),
        ),
        corpus=CorpusConfig(
            manifests_root=_path(corpus, "manifests_root", "corpus", base_dir),
        ),
        chunking=ChunkingConfig(
            chunker_id=_require_str(chunking, "chunker_id", "chunking"),
            chunker_version=_require_str(chunking, "chunker_version", "chunking"),
        ),
        embeddings=EmbeddingsConfig(
            model_id=_require_str(embeddings, "model_id", "embeddings"),
            model_revision=_optional_str(embeddings, "model_revision", "embeddings"),
            vector_dimension=_require_int(embeddings, "vector_dimension", "embeddings", minimum=1),
            vector_dtype=_require_str(embeddings, "vector_dtype", "embeddings"),
            device=_require_str(embeddings, "device", "embeddings"),
            normalize=_require_bool(embeddings, "normalize", "embeddings"),
        ),
        vector_store=VectorStoreConfig(
            provider=_require_str(vector_store, "provider", "vector_store"),
            host=_require_str(vector_store, "host", "vector_store"),
            port=_require_int(vector_store, "port", "vector_store", minimum=1),
            collection_logical_name=_require_str(
                vector_store, "collection_logical_name", "vector_store"
            ),
            distance_metric=_require_str(vector_store, "distance_metric", "vector_store"),
        ),
        registry=RegistryConfig(
            policy_path=_path(registry, "policy_path", "registry", base_dir),
        ),
        runtime=RuntimeConfig(
            checkpoint_root=_path(runtime, "checkpoint_root", "runtime", base_dir),
            log_root=_path(runtime, "log_root", "runtime", base_dir),
        ),
    )
