from __future__ import annotations

import unittest

from cics.ingestion.chatgpt_raw import (
    extract_active_messages,
    extract_conversation_id,
    normalize_payload,
)


class ChatGPTRawParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = {
            "__paginatedConversationPage": {
                "messagesLeafToRoot": [
                    {
                        "id": "assistant-1",
                        "author": {
                            "role": "assistant"
                        },
                        "content": {
                            "content_type": "text",
                            "parts": ["Answer"],
                        },
                        "create_time": 200.0,
                        "metadata": {
                            "parent_id": "hidden-1"
                        },
                    },
                    {
                        "id": "hidden-1",
                        "author": {
                            "role": "system"
                        },
                        "content": {
                            "content_type": "text",
                            "parts": ["hidden"],
                        },
                        "create_time": 150.0,
                        "metadata": {
                            "is_visually_hidden_from_conversation": True,
                            "parent_id": "user-1",
                        },
                    },
                    {
                        "id": "user-1",
                        "author": {
                            "role": "user"
                        },
                        "content": {
                            "content_type": "text",
                            "parts": ["Question"],
                        },
                        "create_time": 100.0,
                        "metadata": {},
                    },
                ]
            },
            "mapping": {
                "paginated-root:11111111-2222-3333-4444-555555555555": {
                    "id": (
                        "paginated-root:"
                        "11111111-2222-3333-4444-555555555555"
                    ),
                    "parent": "",
                },
                "user-1": {
                    "id": "user-1",
                    "parent": (
                        "paginated-root:"
                        "11111111-2222-3333-4444-555555555555"
                    ),
                },
                "hidden-1": {
                    "id": "hidden-1",
                    "parent": "user-1",
                },
                "assistant-1": {
                    "id": "assistant-1",
                    "parent": "hidden-1",
                },
            },
            "title": "Fixture Conversation",
            "update_time": 300.0,
        }

    def test_conversation_id_from_paginated_root(self) -> None:
        self.assertEqual(
            extract_conversation_id(self.payload),
            "11111111-2222-3333-4444-555555555555",
        )

    def test_active_messages_are_chronological(self) -> None:
        messages = extract_active_messages(
            self.payload
        )

        self.assertEqual(
            [message["message_id"] for message in messages],
            ["user-1", "assistant-1"],
        )

        self.assertEqual(
            [message["ordinal"] for message in messages],
            [0, 1],
        )

    def test_hidden_system_message_is_not_promoted(self) -> None:
        messages = extract_active_messages(
            self.payload
        )

        self.assertNotIn(
            "hidden-1",
            {
                message["message_id"]
                for message in messages
            },
        )

    def test_normalized_payload_preserves_provenance(self) -> None:
        normalized = normalize_payload(
            self.payload,
            source_id="source-123",
            source_import_id="import-123",
            source_file="cics/example.raw.json",
        )

        self.assertEqual(
            normalized["schema_id"],
            "cics.normalized_conversation.v1",
        )

        self.assertEqual(
            normalized["source_id"],
            "source-123",
        )

        self.assertEqual(
            normalized["source_import_id"],
            "import-123",
        )

        self.assertEqual(
            normalized["source_file"],
            "cics/example.raw.json",
        )

        self.assertEqual(
            normalized["title"],
            "Fixture Conversation",
        )

        self.assertEqual(
            len(normalized["messages"]),
            2,
        )


if __name__ == "__main__":
    unittest.main()
