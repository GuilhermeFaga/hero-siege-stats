import logging
from src.consts.logger import LOGGING_NAME
from src.models.stats.stats import Stats
from src.models.stats.session import Session
from src.models.stats.account import Account
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats
from src.models.stats.fortune import FortuneStats
from src.models.stats.added_items import AddedItemsStats
from src.models.stats.satanic_zone import SatanicZoneStats

from src.models.events.base import BaseEvent
from src.models.events.gold import GoldEvent
from src.models.events.xp import XPEvent
from src.models.events.account import AccountEvent
from src.models.events.mail import MailEvent
from src.models.events.added_item import AddedItemEvent
from src.models.events.satanic_zone import SatanicZoneEvent
from src.consts.sets import ItemsRarity


class GameStats:
    session = Session()
    account = Account()
    gold = GoldStats()
    xp = XPStats()
    fortune = FortuneStats()
    added_items = AddedItemsStats()
    satanic_zone = SatanicZoneStats()
    logger = logging.getLogger(LOGGING_NAME)

    def process_event(self, event: BaseEvent):
        self.logger.log(logging.INFO,f"GameStats.process_event: {event}")
        if isinstance(event, GoldEvent):
            self.gold.update(currencyData=event.value, season_mode=self.season_mode)
        if isinstance(event, XPEvent):
            self.xp.add(event.value)
        if isinstance(event, AccountEvent):
            self.xp.update(total_xp=event.value.experience)
            self.season_mode = event.value.get_current_season_mode()
            # TODO - Find the correct fortune_enemies_killed value
            # TODO - Fortune Message changed and logic is not working anymore rightnow.
            #self.fortune.update(total_fortune=event.value.fortune_enemies)
        if isinstance(event, MailEvent):
            self.session.update(has_mail=bool(event.value))
        if isinstance(event, AddedItemEvent):
            self.added_items.update(added_item_object=event.value)
        if isinstance(event, SatanicZoneEvent):
            self.satanic_zone.update(event.value)

    def reset(self):
        logger = logging.getLogger(LOGGING_NAME)
        logger.info("Resetting all game stats...")
        
        self.session = Session()
        self.account = Account()
        self.gold = GoldStats()
        self.xp = XPStats()
        self.added_items = AddedItemsStats()
        self.satanic_zone = SatanicZoneStats()
        self.season_mode = None
        
        logger.info("All stats have been reset")

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
        _items_per_hour = {}
        for rarity_id in ItemsRarity:
            _items_per_hour[ItemsRarity[rarity_id]] = self.session.calculate_value_per_hour(
                self.added_items.added_items[ItemsRarity[rarity_id]]['total']
            )
        self.added_items.update(items_per_hour=_items_per_hour)

    def get_stats(self):
        self.update_hourly_stats()
        return Stats(
            session=self.session,
            gold_stats=self.gold,
            xp_stats=self.xp,
            added_items=self.added_items,
            satanic_zone = self.satanic_zone
        )
