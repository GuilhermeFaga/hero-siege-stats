import base64

import pytest

from src.engine.message_parser import MessageParser


def test_capture_extracts_json_from_packet_like_payload(json_payload_factory):
    payload = json_payload_factory({"totalGuildXp": 10, "message": "Gained 150 xp"})

    result = MessageParser.capture(f"b'{payload}'", "10.0.0.1", "10.0.0.2")

    assert result == {"totalGuildXp": 10, "message": "Gained 150 xp"}


@pytest.mark.parametrize("payload", ["not-json", "{not json}"])
def test_capture_returns_none_for_invalid_payloads(payload):
    assert MessageParser.capture(payload, "10.0.0.1", "10.0.0.2") is None


@pytest.mark.parametrize("excluded_key", ["steam", "inventory_charms"])
def test_capture_ignores_excluded_json_keys(excluded_key, json_payload_factory):
    payload = json_payload_factory({excluded_key: []})

    assert MessageParser.capture(payload, "10.0.0.1", "10.0.0.2") is None


def test_capture_parses_special_base64_json_packet(json_payload_factory):
    payload = json_payload_factory(
        {"message": "You have new mail", "padding": "x" * 80}
    )
    encoded = base64.b64encode(payload.encode()).decode()

    result = MessageParser.capture(f"xxx{encoded}", "10.0.0.1", "10.0.0.2")

    assert result == {"message": "You have new mail", "padding": "x" * 80}


def test_capture_parses_special_inventory_base64_json_packet(json_payload_factory):
    payload = json_payload_factory({"addedItemFingerprint": "abc", "padding": "x" * 80})
    encoded = base64.b64encode(payload.encode()).decode()

    result = MessageParser.capture(f"xxx[INV]{encoded}", "10.0.0.1", "10.0.0.2")

    assert result == {"addedItemFingerprint": "abc", "padding": "x" * 80}


def test_capture_parses_special_query_string_packet():
    result = MessageParser.capture(
        f"xxxmessage=mail+arrived&totalGuildXp=100&padding={'x' * 80}",
        "10.0.0.1",
        "10.0.0.2",
    )

    assert result == {
        "message": "mail arrived",
        "totalGuildXp": "100",
        "padding": "x" * 80,
    }
