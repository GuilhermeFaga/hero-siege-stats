from math import ceil, floor


class XPStats:
    total_xp: int
    total_xp_earned: int
    xp_per_hour: int

    def __init__(self, total_xp=0, total_xp_earned=0, xp_per_hour=0):
        self.total_xp = total_xp
        self.total_xp_earned = total_xp_earned
        self.xp_per_hour = xp_per_hour

    def update(self, total_xp=None, total_xp_earned=None, xp_per_hour=None):
        if total_xp is not None:
            if self.total_xp != 0:
                diff = total_xp - self.total_xp
                self.total_xp_earned += diff if diff > 0 else 0
            self.total_xp = total_xp
        if total_xp_earned is not None:
            self.total_xp_earned = total_xp_earned
        if xp_per_hour is not None:
            self.xp_per_hour = xp_per_hour

    def add(self, xp: int):
        self.total_xp += int(xp / 0.15)
        self.total_xp_earned += int(xp / 0.15)

    def replace(self, total_xp=None, total_xp_earned=None, xp_per_hour=None):
        if total_xp is not None:
            self.total_xp = total_xp
        if total_xp_earned is not None:
            self.total_xp_earned = total_xp_earned
        if xp_per_hour is not None:
            self.xp_per_hour = xp_per_hour
