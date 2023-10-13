
class XPStats:
    total_xp_earned: int
    xp_per_hour: int

    def __init__(self, total_xp_earned=0, xp_per_hour=0):
        self.total_xp_earned = total_xp_earned
        self.xp_per_hour = xp_per_hour

    def update(self, xp: int):
        self.total_xp_earned += xp
        # TODO - calculate xp per hour
