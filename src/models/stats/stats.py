from src.models.stats.session import Session
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats
from src.models.stats.added_items import AddedItemsStats


class Stats:
    session: Session
    gold: GoldStats
    xp: XPStats
    added_items: AddedItemsStats

    def __init__(self, session=Session(), gold_stats=GoldStats(), xp_stats=XPStats(), added_items=AddedItemsStats()):
        self.session = session
        self.gold = gold_stats
        self.xp = xp_stats
        self.added_items = added_items
