from src.engine.message_parser import MessageParser
from src.engine.game_stats import GameStats
from src.engine.backend import Backend


class Engine:
    game_stats = GameStats()

    @staticmethod
    def get_stats():
        return Engine.game_stats.get_stats()

    @staticmethod
    def queue_an_event(packet):
        event = MessageParser.packet_to_event(packet)
        if event is not None:
            Engine.game_stats.process_event(event)

    @staticmethod
    def reset_stats():
        Engine.game_stats.reset()

    @staticmethod
    def initialize():
        initialization_result = Backend.initialize(Engine.queue_an_event)
        return initialization_result
