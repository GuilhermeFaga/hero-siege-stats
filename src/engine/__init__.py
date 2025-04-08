

from src.engine.message_parser import MessageParser
from src.engine.game_stats import GameStats


class Engine:
    game_stats = GameStats()

    @staticmethod
    def get_stats():
        return Engine.game_stats.get_stats()

    @staticmethod
    def queue_an_event(packet):
        events = MessageParser.packet_to_event(packet)
        if events is not None or events:
            for event in events:
                Engine.game_stats.process_event(event)

    @staticmethod
    def reset_stats():
        Engine.game_stats.reset()


