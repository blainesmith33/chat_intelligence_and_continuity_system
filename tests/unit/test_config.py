from pathlib import Path

import pytest

from cics.config import ConfigError, load_config


VALID_CONFIG = """
[paths]
data_root = "data"
runtime_root = "runtime"

[artifacts]
staging_root = "runtime/artifacts/staging"
committed_root = "runtime/artifacts/committed"

[corpus]
manifests_root = "runtime/manifests"

[chunking]
chunker_id = "cics.chat_chunker"
chunker_version = "1"

[embeddings]
model_id = "nomic-ai/nomic-embed-text-v1.5"
vector_dimension = 768
vector_dtype = "float32"
device = "cpu"
normalize = false

[vector_store]
provider = "qdrant"
host = "127.0.0.1"
port = 6333
collection_logical_name = "chat_rag"
distance_metric = "cosine"

[registry]
policy_path = "config/registry_policy.json"

[runtime]
checkpoint_root = "runtime/checkpoints"
log_root = "runtime/logs"
"""


def test_relative_paths_resolve_against_config_file(tmp_path: Path) -> None:
    config_path = tmp_path / "cics.toml"
    config_path.write_text(VALID_CONFIG, encoding="utf-8")

    config = load_config(config_path)

    assert config.paths.data_root == (tmp_path / "data").resolve()
    assert config.runtime.log_root == (tmp_path / "runtime/logs").resolve()


def test_unknown_keys_fail_closed(tmp_path: Path) -> None:
    config_path = tmp_path / "cics.toml"
    config_path.write_text(VALID_CONFIG + "\n[paths.extra]\nfoo = 'bar'\n", encoding="utf-8")

    with pytest.raises(ConfigError):
        load_config(config_path)


def test_no_hidden_default_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CICS_CONFIG", raising=False)
    with pytest.raises(ConfigError):
        load_config(None)
