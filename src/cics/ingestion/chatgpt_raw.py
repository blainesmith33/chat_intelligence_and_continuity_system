from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cics.config.settings import CICSSettings
from cics.provenance.identity import (
    source_content_hash,
    source_id_from_bytes,
)


PARSER_VERSION = "cics.chatgpt_raw.v1"
SOURCE_FORMAT = "chatgpt_raw_json"

VISIBLE_ROLES = {
    "user",
    "assistant",
}


class ChatGPTRawImportError(RuntimeError):
    pass


def _utc_iso_from_epoch(value: Any) -> str | None:
    if value is None:
        return None

    try:
        timestamp = float(value)
    except (TypeError, ValueError):
        return None

    return (
        datetime.fromtimestamp(timestamp, tz=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
    ) as handle:
        json.dump(
            payload,
            handle,
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        )
        handle.write("\n")
        temp_path = Path(handle.name)

    os.replace(temp_path, path)


def _active_branch_raw_messages(
    payload: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Return the active ChatGPT branch in leaf-to-root order.

    Supported captured export shapes:

    1. Paginated capture:
       __paginatedConversationPage.messagesLeafToRoot

    2. Mapping capture:
       mapping + current_node

       In this form the active branch is reconstructed by
       following current_node -> parent -> parent until root.

    The returned orientation is always leaf-to-root so the
    normalization layer can apply one chronological reversal.
    """

    page = payload.get("__paginatedConversationPage")

    if isinstance(page, dict):
        messages = page.get("messagesLeafToRoot")

        if isinstance(messages, list):
            return [
                message
                for message in messages
                if isinstance(message, dict)
            ]

    mapping = _mapping(payload)
    current_node = payload.get("current_node")

    if not isinstance(current_node, str) or not current_node:
        raise ChatGPTRawImportError(
            "Raw export contains neither "
            "messagesLeafToRoot nor a valid current_node"
        )

    branch: list[dict[str, Any]] = []
    seen: set[str] = set()

    node_id: str | None = current_node

    while node_id:
        if node_id in seen:
            raise ChatGPTRawImportError(
                f"Cycle detected in conversation mapping at: {node_id}"
            )

        seen.add(node_id)

        node = mapping.get(node_id)

        if not isinstance(node, dict):
            raise ChatGPTRawImportError(
                f"Active branch node missing from mapping: {node_id}"
            )

        message = node.get("message")

        if isinstance(message, dict):
            raw_message = dict(message)

            if not isinstance(raw_message.get("id"), str):
                raw_message["id"] = node_id

            branch.append(raw_message)

        parent = node.get("parent")

        if isinstance(parent, str) and parent:
            node_id = parent
        else:
            node_id = None

    if not branch:
        raise ChatGPTRawImportError(
            "Active mapping branch contained no messages"
        )

    return branch


def _mapping(payload: dict[str, Any]) -> dict[str, Any]:
    mapping = payload.get("mapping", {})

    if mapping is None:
        return {}

    if not isinstance(mapping, dict):
        raise ChatGPTRawImportError(
            "Top-level mapping must be an object when present"
        )

    return mapping


def extract_conversation_id(
    payload: dict[str, Any],
) -> str | None:
    explicit = payload.get("conversation_id")

    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()

    candidates: list[str] = []

    for node_id in _mapping(payload):
        if not isinstance(node_id, str):
            continue

        prefix = "paginated-root:"

        if node_id.startswith(prefix):
            value = node_id[len(prefix):].strip()

            if value:
                candidates.append(value)

    candidates = sorted(set(candidates))

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        raise ChatGPTRawImportError(
            "Multiple paginated-root conversation IDs found: "
            + ", ".join(candidates)
        )

    return None


def _parent_lookup(
    payload: dict[str, Any],
) -> dict[str, str | None]:
    result: dict[str, str | None] = {}

    for node_id, node in _mapping(payload).items():
        if not isinstance(node_id, str):
            continue

        if not isinstance(node, dict):
            continue

        parent = node.get("parent")

        if isinstance(parent, str) and parent:
            result[node_id] = parent
        else:
            result[node_id] = None

    return result


def _extract_text(message: dict[str, Any]) -> str | None:
    content = message.get("content")

    if not isinstance(content, dict):
        return None

    if content.get("content_type") != "text":
        return None

    parts = content.get("parts")

    if not isinstance(parts, list):
        return None

    text_parts = [
        part
        for part in parts
        if isinstance(part, str)
    ]

    if not text_parts:
        return None

    text = "\n".join(text_parts)

    if not text.strip():
        return None

    return text


def _is_human_visible(
    message: dict[str, Any],
) -> bool:
    author = message.get("author")

    if not isinstance(author, dict):
        return False

    role = author.get("role")

    if role not in VISIBLE_ROLES:
        return False

    metadata = message.get("metadata")

    if isinstance(metadata, dict):
        if metadata.get(
            "is_visually_hidden_from_conversation"
        ) is True:
            return False

    return _extract_text(message) is not None


def extract_active_messages(
    payload: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Normalize the human-visible user/assistant messages on the
    active conversation branch.

    ChatGPT's captured page structure exposes that branch as
    messagesLeafToRoot. CICS reverses it into chronological
    root-to-leaf order.

    Hidden system/developer/model-context material remains
    preserved in the immutable raw source but is not promoted
    into the Phase-1 retrieval conversation.
    """

    raw_messages = _active_branch_raw_messages(
        payload
    )

    parent_lookup = _parent_lookup(payload)

    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for raw in reversed(raw_messages):
        if not isinstance(raw, dict):
            continue

        if not _is_human_visible(raw):
            continue

        message_id = raw.get("id")

        if not isinstance(message_id, str) or not message_id:
            raise ChatGPTRawImportError(
                "Visible message is missing a valid id"
            )

        if message_id in seen_ids:
            raise ChatGPTRawImportError(
                f"Duplicate active message id: {message_id}"
            )

        seen_ids.add(message_id)

        author = raw["author"]
        role = author["role"]

        metadata = raw.get("metadata")
        metadata = (
            metadata
            if isinstance(metadata, dict)
            else {}
        )

        parent_message_id = metadata.get("parent_id")

        if not isinstance(parent_message_id, str):
            parent_message_id = parent_lookup.get(
                message_id
            )

        normalized.append(
            {
                "ordinal": len(normalized),
                "message_id": message_id,
                "parent_message_id": parent_message_id,
                "source_node_id": message_id,
                "role": role,
                "created_at": _utc_iso_from_epoch(
                    raw.get("create_time")
                ),
                "content": _extract_text(raw),
                "on_active_branch": True,
            }
        )

    if not normalized:
        raise ChatGPTRawImportError(
            "No human-visible user/assistant text messages "
            "were found on the active branch"
        )

    return normalized


def normalize_payload(
    payload: dict[str, Any],
    *,
    source_id: str,
    source_import_id: str,
    source_file: str,
) -> dict[str, Any]:
    messages = extract_active_messages(payload)

    title = payload.get("title")
    if not isinstance(title, str):
        title = None

    created_at = _utc_iso_from_epoch(
        payload.get("create_time")
    )

    if created_at is None and messages:
        created_at = messages[0]["created_at"]

    updated_at = _utc_iso_from_epoch(
        payload.get("update_time")
    )

    return {
        "schema_id": "cics.normalized_conversation.v1",
        "source_id": source_id,
        "source_import_id": source_import_id,
        "source_format": SOURCE_FORMAT,
        "source_file": source_file,
        "conversation_id": extract_conversation_id(
            payload
        ),
        "title": title,
        "created_at": created_at,
        "updated_at": updated_at,
        "messages": messages,
    }


def _relative_source_path(
    source_path: Path,
    source_root: Path,
) -> str:
    source = source_path.resolve()
    root = source_root.resolve()

    try:
        relative = source.relative_to(root)
    except ValueError as exc:
        raise ChatGPTRawImportError(
            f"Source is outside CICS_SOURCE_ROOT: {source}"
        ) from exc

    return relative.as_posix()


def import_raw_chat(
    source_path: Path,
    settings: CICSSettings,
) -> tuple[Path, Path]:
    source_path = source_path.expanduser().resolve()

    if not source_path.is_file():
        raise ChatGPTRawImportError(
            f"Source file does not exist: {source_path}"
        )

    relative_source = _relative_source_path(
        source_path,
        settings.source_root,
    )

    raw_bytes = source_path.read_bytes()

    try:
        payload = json.loads(
            raw_bytes.decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ChatGPTRawImportError(
            f"Invalid UTF-8 JSON source: {source_path}"
        ) from exc

    if not isinstance(payload, dict):
        raise ChatGPTRawImportError(
            "ChatGPT raw export root must be a JSON object"
        )

    source_id = source_id_from_bytes(
        raw_bytes,
        source_format=SOURCE_FORMAT,
    )

    content_hash = source_content_hash(
        raw_bytes
    )

    import_id = (
        f"cics-import:{PARSER_VERSION}:{source_id}"
    )

    normalized = normalize_payload(
        payload,
        source_id=source_id,
        source_import_id=import_id,
        source_file=relative_source,
    )

    manifest = {
        "schema_id": "cics.import_manifest.v1",
        "import_id": import_id,
        "imported_at": _utc_now_iso(),
        "source_id": source_id,
        "source_format": SOURCE_FORMAT,
        "source_file": relative_source,
        "conversation_id": normalized[
            "conversation_id"
        ],
        "paired_source_id": None,
        "content_hash": {
            "algorithm": "blake3",
            "digest": content_hash,
        },
        "parser_version": PARSER_VERSION,
        "status": "normalized",
    }

    normalized_path = (
        settings.normalized_root
        / f"{source_id}.normalized.json"
    )

    manifest_path = (
        settings.manifests_root
        / f"{source_id}.import.json"
    )

    _atomic_write_json(
        normalized_path,
        normalized,
    )

    _atomic_write_json(
        manifest_path,
        manifest,
    )

    return normalized_path, manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize one ChatGPT .raw.json archive "
            "into CICS Phase-1 artifacts."
        )
    )

    parser.add_argument(
        "source",
        type=Path,
        help="Path to a ChatGPT .raw.json archive",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = CICSSettings.from_env()

    normalized_path, manifest_path = import_raw_chat(
        args.source,
        settings,
    )

    print(
        f"[OK] normalized: {normalized_path}"
    )
    print(
        f"[OK] manifest:   {manifest_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
