from math import ceil, floor


class FortuneStats:
    total_fortune: int
    total_fortune_kills: int
    fortune_per_hour: int

    def __init__(self, total_fortune=0, total_fortune_kills=0, fortune_per_hour=0):
        self.total_fortune = total_fortune
        self.total_fortune_kills = total_fortune_kills
        self.fortune_per_hour = fortune_per_hour

    def update(self, total_fortune=None, total_fortune_kills=None, fortune_per_hour=None):
        if total_fortune is not None:
            if self.total_fortune != 0:
                diff = total_fortune - self.total_fortune
                self.total_fortune_kills += diff if diff > 0 else 0
            self.total_fortune = total_fortune
        if total_fortune_kills is not None:
            self.total_fortune_kills = total_fortune_kills
        if fortune_per_hour is not None:
            self.fortune_per_hour = fortune_per_hour

    def add(self, fortune: int):
        self.total_fortune += int(fortune / 0.15)
        self.total_fortune_kills += int(fortune / 0.15)

    def replace(self, total_fortune=None, total_fortune_kills=None, fortune_per_hour=None):
        if total_fortune is not None:
            self.total_fortune = total_fortune
        if total_fortune_kills is not None:
            self.total_fortune_kills = total_fortune_kills
        if fortune_per_hour is not None:
            self.fortune_per_hour = fortune_per_hour
