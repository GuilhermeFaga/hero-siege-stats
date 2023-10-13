from math import ceil, floor


class XPStats:
    total_xp_earned: int
    xp_per_hour: int

    def __init__(self, total_xp_earned=0, xp_per_hour=0):
        self.total_xp_earned = total_xp_earned
        self.xp_per_hour = xp_per_hour

    def update(self, xp: int):
        self.total_xp_earned += int(test(xp) / 0.15)
        # TODO - calculate xp per hour


def test(a):
    for i in range(20):
        b = a - 1 + (i + 1) * 0.05
        if b / 0.15 - floor(b / 0.15) == 0:
            return b

    return a
