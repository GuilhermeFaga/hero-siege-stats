from src.models.stats.session import Session
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats


class Stats:
    session: Session
    gold: GoldStats
    xp: XPStats

    def __init__(self, session=Session(), gold_stats=GoldStats(), xp_stats=XPStats()):
        self.session = session
        self.gold = gold_stats
        self.xp = xp_stats
