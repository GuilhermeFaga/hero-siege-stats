from queue import Queue

from datetime import datetime

from message_parser import MessageParser
from consts import events as ev_consts
import backend


class GameStats():
    session_start_time: str

    def __init__(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pass

    def process_event(self, event):
        print("GameStats.process_event:", event)

    def register_event(self, event):
        pass

    def reset(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


game_stats = GameStats()
event_queue: Queue = Queue()


def queue_an_event(packet):
    event = MessageParser.packet_to_event(packet)
    if event is not None:
        game_stats.process_event(event)


def reset_stats():
    game_stats.reset()


def initialize():
    initialization_result = backend.initialize(queue_an_event)
    return initialization_result
