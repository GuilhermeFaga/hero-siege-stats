from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats


class Stats:
    gold: GoldStats
    xp: XPStats

    def __init__(self, gold_stats=GoldStats(), xp_stats=XPStats()):
        self.gold = gold_stats
        self.xp = xp_stats
