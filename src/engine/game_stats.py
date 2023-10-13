from datetime import datetime

from src.consts import events as consts

from src.models.messages.gold import CurrencyData
from src.models.stats.stats import Stats
from src.models.stats.gold import GoldStats
from src.models.event import Event


class GameStats:
    session_start_time: str

    gold = GoldStats()
    test = None

    def __init__(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_event(self, event: Event):
        print("GameStats.process_event:", event)
        if event.data[consts.EvKeyName] == consts.EvNameUpdateGold:
            _event = CurrencyData.cast(event.data[consts.EvKeyValue])
            self.gold.update(_event)
        self.test = event

    def reset(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_test(self):
        return self.test

    def get_stats(self):
        return Stats(
            gold_stats=self.gold
        )
