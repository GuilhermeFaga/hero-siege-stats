from src.engine.game_stats import GameStats
from src.engine.message_parser import MessageParser


def test_game_stats_processes_packet_derived_events(
    account_message_factory,
    gold_message_factory,
    added_item_message_factory,
    json_payload_factory,
    scapy_tcp_packet_factory,
):
    game_stats = GameStats()
    account_payload = json_payload_factory(account_message_factory(experience=1_000))
    gold_payload = json_payload_factory(gold_message_factory(GSS=250))
    item_payload = json_payload_factory(added_item_message_factory(rarity=6, mf_drop=1))

    MessageParser.packet_to_event(scapy_tcp_packet_factory(account_payload, ack=1))
    events = MessageParser.packet_to_event(
        scapy_tcp_packet_factory(gold_payload, ack=2)
    )
    for event in events:
        game_stats.process_event(event)

    events = MessageParser.packet_to_event(
        scapy_tcp_packet_factory(item_payload, ack=3)
    )
    for event in events:
        game_stats.process_event(event)

    events = MessageParser.packet_to_event(scapy_tcp_packet_factory("{}", ack=4))
    for event in events:
        game_stats.process_event(event)

    assert game_stats.season_mode == "GSS"
    assert game_stats.xp.total_xp == 1_000
    assert game_stats.gold.total_gold == 250
    assert game_stats.added_items.added_items["Satanic"] == {"total": 1, "mf": 1}


def test_game_stats_reset_clears_mutable_state(added_item_message_factory):
    game_stats = GameStats()
    event = MessageParser.message_to_event([added_item_message_factory(rarity=7)])[0]

    game_stats.process_event(event)
    game_stats.reset()

    assert game_stats.added_items.added_items["Angelic"]["total"] == 0
    assert game_stats.season_mode is None
