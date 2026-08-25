import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas"
EXPECTED_SCHEMAS = {
    "source_record_v1.json",
    "document_record_v1.json",
    "message_record_v1.json",
    "chunk_record_v1.json",
    "embedding_manifest_record_v1.json",
    "vector_payload_v1.json",
    "artifact_metadata_v1.json",
    "artifact_event_v1.json",
    "entity_v1.json",
}


def test_required_schema_family_exists() -> None:
    actual = {path.name for path in SCHEMA_ROOT.glob("*.json")}
    assert EXPECTED_SCHEMAS <= actual


def test_schema_family_is_valid_draft_2020_12() -> None:
    for path in sorted(SCHEMA_ROOT.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        assert schema["additionalProperties"] is False
