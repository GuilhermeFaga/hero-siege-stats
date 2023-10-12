from engine.message_parser import MessageParser
from engine.game_stats import GameStats
from engine.backend import Backend


game_stats = GameStats()


def queue_an_event(packet):
    event = MessageParser.packet_to_event(packet)
    if event is not None:
        game_stats.process_event(event)


def reset_stats():
    game_stats.reset()


def initialize():
    initialization_result = Backend.initialize(queue_an_event)
    return initialization_result
