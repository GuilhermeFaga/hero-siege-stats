from scapy.layers.inet import IP, TCP

from src.engine.message_parser import MessageParser
from src.models.events.xp import XPEvent


def test_packet_to_event_returns_none_for_packet_without_ip_or_tcp():
    assert MessageParser.packet_to_event(TCP()) is None


def test_packet_to_event_returns_none_for_tcp_packet_without_load():
    packet = IP(src="10.0.0.1", dst="10.0.0.2") / TCP(ack=1)

    assert MessageParser.packet_to_event(packet) is None


def test_packet_to_event_waits_until_ack_changes(
    scapy_tcp_packet_factory,
    xp_message_factory,
    json_payload_factory,
):
    payload = json_payload_factory(xp_message_factory(message="Gained 15 xp"))

    first_result = MessageParser.packet_to_event(
        scapy_tcp_packet_factory(payload, ack=1)
    )
    second_result = MessageParser.packet_to_event(scapy_tcp_packet_factory("{}", ack=2))

    assert first_result is None
    assert len(second_result) == 1
    assert isinstance(second_result[0], XPEvent)
    assert second_result[0].value == 15


def test_packet_to_event_joins_chunks_with_same_ack(
    scapy_tcp_packet_factory,
):
    MessageParser.packet_to_event(
        scapy_tcp_packet_factory('{"message":"Gained ', ack=1)
    )
    MessageParser.packet_to_event(
        scapy_tcp_packet_factory('30 xp","totalGuildXp":100}', ack=1)
    )

    result = MessageParser.packet_to_event(scapy_tcp_packet_factory("{}", ack=2))

    assert len(result) == 1
    assert isinstance(result[0], XPEvent)
    assert result[0].value == 30


def test_packet_to_event_splits_multiple_messages_in_buffer(
    scapy_tcp_packet_factory,
    xp_message_factory,
    mail_message_factory,
    json_payload_factory,
):
    xp_payload = json_payload_factory(xp_message_factory(message="Gained 12 xp"))
    mail_payload = json_payload_factory(mail_message_factory())
    combined_payload = f"{xp_payload}\\{mail_payload}"

    MessageParser.packet_to_event(scapy_tcp_packet_factory(combined_payload, ack=1))
    result = MessageParser.packet_to_event(scapy_tcp_packet_factory("{}", ack=2))

    assert [type(event).__name__ for event in result] == ["XPEvent", "MailEvent"]
