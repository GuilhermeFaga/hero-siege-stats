from datetime import datetime

from src.models.stats.stats import Stats
from src.models.stats.session import Session
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats

from src.models.events.base import BaseEvent
from src.models.events.gold import GoldEvent
from src.models.events.xp import XPEvent
from src.models.events.account import AccountEvent


class GameStats:
    session = Session()
    gold = GoldStats()
    xp = XPStats()

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
        # TODO - reset stats
        pass

    def get_stats(self):
        return Stats(
            session=self.session,
            gold_stats=self.gold,
            xp_stats=self.xp
        )
