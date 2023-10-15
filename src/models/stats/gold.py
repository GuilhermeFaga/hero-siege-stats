from src.models.messages.gold import CurrencyData


class GoldStats:
    total_gold: int
    total_gold_earned: int
    gold_per_hour: int

    def __init__(self, total_gold=0, total_gold_earned=0, gold_per_hour=0):
        self.total_gold = total_gold
        self.total_gold_earned = total_gold_earned
        self.gold_per_hour = gold_per_hour

    def update(self, currency_data: CurrencyData | None = None, gold_per_hour=None):
        if currency_data is not None:
            if self.total_gold != 0:
                diff = currency_data.gold - self.total_gold
                self.total_gold_earned += diff if diff > 0 else 0
            self.total_gold = currency_data.gold
        if gold_per_hour is not None:
            self.gold_per_hour = gold_per_hour
