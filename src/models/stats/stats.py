from src.models.stats.gold import GoldStats


class Stats:
    gold: GoldStats

    def __init__(self, gold_stats=GoldStats()):
        self.gold = gold_stats
