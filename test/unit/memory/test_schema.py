import json
import os
from pathlib import Path
import pytest

from src.core.memory.schema import Role, Message, Conversation


def test_role_from_str():
    assert Role.from_str("system") == Role.SYS
    assert Role.from_str("user") == Role.USER
    assert Role.from_str("assistant") == Role.ASSISTANT
    assert Role.from_str("tool") == Role.TOOL
    assert Role.from_str("other") is None


def test_message_token_accessors():
    msg = Message(role=Role.USER, content="hello")
    msg.set_tokens(5)
    assert msg.get_tokens() == 5


def test_conversation_from_json(tmp_path):
    data = {
        "id": 1,
        "name": "test",
        "messages": [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "hi"}
        ]
    }
    json_path = tmp_path / "conv.json"
    json_path.write_text(json.dumps(data))

    conv_id, conv = Conversation.from_json(str(json_path))
    assert conv_id == 1
    assert conv.name == "test"
    assert len(conv) == 2
    assert conv.messages[0].role == Role.SYS
    assert conv.messages[1].content == "hi"


