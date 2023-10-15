from src.models.stats.stats import Stats
from src.models.stats.session import Session
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats

from src.models.events.base import BaseEvent
from src.models.events.gold import GoldEvent
from src.models.events.xp import XPEvent
from src.models.events.account import AccountEvent
from src.models.events.mail import MailEvent


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
            self.xp.update(total_xp=event.value.experience)
        if isinstance(event, MailEvent):
            self.session.update(has_mail=bool(event.value))

    def reset(self):
        # TODO - reset stats
        pass

    def update_hourly_stats(self):
        self.gold.update(
            gold_per_hour=self.session.calculate_value_per_hour(
                self.gold.total_gold_earned
            )
        )
        self.xp.update(
            xp_per_hour=self.session.calculate_value_per_hour(
                self.xp.total_xp_earned
            )
        )

    def get_stats(self):
        self.update_hourly_stats()
        return Stats(
            session=self.session,
            gold_stats=self.gold,
            xp_stats=self.xp
        )
