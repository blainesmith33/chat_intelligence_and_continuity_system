from __future__ import annotations

import unittest

from cics.ingestion.chatgpt_raw import (
    extract_active_messages,
    extract_conversation_id,
)


class ChatGPTRawMappingTests(unittest.TestCase):
    def setUp(self) -> None:
        root_id = (
            "paginated-root:"
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        )

        self.payload = {
            "conversation_id": (
                "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
            ),
            "current_node": "assistant-1",
            "title": "Mapping Fixture",
            "mapping": {
                root_id: {
                    "id": root_id,
                    "parent": "",
                },
                "user-1": {
                    "id": "user-1",
                    "parent": root_id,
                    "message": {
                        "id": "user-1",
                        "author": {
                            "role": "user",
                            "metadata": {},
                        },
                        "content": {
                            "content_type": "text",
                            "parts": ["Question"],
                        },
                        "create_time": 100.0,
                        "metadata": {},
                    },
                },
                "hidden-1": {
                    "id": "hidden-1",
                    "parent": "user-1",
                    "message": {
                        "id": "hidden-1",
                        "author": {
                            "role": "system",
                            "metadata": {},
                        },
                        "content": {
                            "content_type": "text",
                            "parts": ["Hidden context"],
                        },
                        "create_time": 150.0,
                        "metadata": {
                            "is_visually_hidden_from_conversation": True
                        },
                    },
                },
                "assistant-1": {
                    "id": "assistant-1",
                    "parent": "hidden-1",
                    "message": {
                        "id": "assistant-1",
                        "author": {
                            "role": "assistant",
                            "metadata": {},
                        },
                        "content": {
                            "content_type": "text",
                            "parts": ["Answer"],
                        },
                        "create_time": 200.0,
                        "metadata": {},
                    },
                },
            },
        }

    def test_mapping_branch_is_reconstructed(self) -> None:
        messages = extract_active_messages(
            self.payload
        )

        self.assertEqual(
            [message["message_id"] for message in messages],
            ["user-1", "assistant-1"],
        )

        self.assertEqual(
            [message["content"] for message in messages],
            ["Question", "Answer"],
        )

    def test_explicit_conversation_id_is_preserved(self) -> None:
        self.assertEqual(
            extract_conversation_id(self.payload),
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        )


if __name__ == "__main__":
    unittest.main()
