import re

from cics.provenance import (
    chunk_id,
    document_id_from_native,
    message_id,
    new_artifact_id,
    source_id,
    validate_entity_id,
)
from cics.provenance.hashing import blake3_hex


def test_source_identity_depends_on_format_and_exact_bytes() -> None:
    payload = b'{"conversation":"same bytes"}'
    first = source_id("chatgpt_export_json", payload)
    second = source_id("chatgpt_export_json", payload)
    different_format = source_id("other_json", payload)

    assert first == second
    assert first != different_format
    assert re.fullmatch(r"src_[a-f0-9]{64}", first)


def test_native_document_identity_is_location_independent() -> None:
    first = document_id_from_native("chatgpt_export_json", "conversation", "abc-123")
    second = document_id_from_native("chatgpt_export_json", "conversation", "abc-123")

    assert first == second
    assert re.fullmatch(r"doc_[a-f0-9]{64}", first)


def test_chunk_identity_binds_span_order_and_policy() -> None:
    doc = document_id_from_native("chatgpt_export_json", "conversation", "abc-123")
    msg1 = message_id(doc, "node-a")
    msg2 = message_id(doc, "node-b")
    content_hash = blake3_hex(b"hello world")
    policy_hash = blake3_hex(b"chunk policy")

    first = chunk_id(
        document_id=doc,
        source_spans=[
            {"message_id": msg1, "start_offset": 0, "end_offset": 5},
            {"message_id": msg2, "start_offset": 0, "end_offset": 5},
        ],
        content_hash=content_hash,
        chunker_id="cics.chat_chunker",
        chunker_version="1",
        chunk_policy_hash=policy_hash,
    )
    reordered = chunk_id(
        document_id=doc,
        source_spans=[
            {"message_id": msg2, "start_offset": 0, "end_offset": 5},
            {"message_id": msg1, "start_offset": 0, "end_offset": 5},
        ],
        content_hash=content_hash,
        chunker_id="cics.chat_chunker",
        chunker_version="1",
        chunk_policy_hash=policy_hash,
    )

    assert first != reordered
    assert re.fullmatch(r"chk_[a-f0-9]{64}", first)


def test_artifact_ids_are_assigned_and_namespaced() -> None:
    first = new_artifact_id()
    second = new_artifact_id()

    assert first != second
    assert re.fullmatch(r"art_[a-f0-9]{32}", first)


def test_entity_ids_are_declared_stable_keys() -> None:
    assert validate_entity_id("ent_project_cics") == "ent_project_cics"
