from src.models.messages.gold import CurrencyData


class GoldStats:
    total_gold: int
    total_gold_earned: int
    gold_per_hour: int

    def __init__(self, total_gold=0, total_gold_earned=0, gold_per_hour=0,season_mode=None):
        self.total_gold = total_gold
        self.total_gold_earned = total_gold_earned
        self.gold_per_hour = gold_per_hour
        self.season_mode = season_mode

    def update(self, currencyData: CurrencyData | None = None, gold_per_hour=None, season_mode=None):
        if currencyData is not None and season_mode is not None:
            self.season_mode = season_mode
            current_gold = currencyData.get_gold_for_mode(season_mode)
            
            if self.total_gold != 0:
                diff = current_gold - self.total_gold
                self.total_gold_earned += diff if diff > 0 else 0
            self.total_gold = current_gold
        
        if gold_per_hour is not None:
            self.gold_per_hour = gold_per_hour
