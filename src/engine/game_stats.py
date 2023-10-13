from datetime import datetime

from src.models.stats.stats import Stats
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats

from src.models.events.base import BaseEvent
from src.models.events.gold import GoldEvent
from src.models.events.xp import XPEvent
from src.models.events.account import AccountEvent


class GameStats:
    session_start_time: str

    gold = GoldStats()
    xp = XPStats()
    test = None

    def __init__(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_event(self, event: BaseEvent):
        print("GameStats.process_event:", event)
        if isinstance(event, GoldEvent):
            self.gold.update(event.value)
        if isinstance(event, XPEvent):
            self.xp.add(event.value)
        if isinstance(event, AccountEvent):
            self.xp.update(
                total_xp=event.value.experience
            )

    def reset(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # TODO - reset stats

    def get_stats(self):
        return Stats(
            gold_stats=self.gold,
            xp_stats=self.xp
        )
