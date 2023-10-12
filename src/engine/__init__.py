from src.engine.message_parser import MessageParser
from src.engine.game_stats import GameStats
from src.engine.backend import Backend


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
