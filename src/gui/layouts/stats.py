from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from src.gui.components.value_display import ValueDisplay
from src.gui.components.row import Row
from src.models.stats.stats import Stats
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats

from src.engine import Engine

from src.consts import assets as assets_const


class GoldRow(Row):
    def __init__(self):
        self.total_gold = ValueDisplay(assets_const.IcCoins, str(0))
        self.total_gold_earned = ValueDisplay(assets_const.IcCoins, str(0))

        Row.__init__(self, [
            self.total_gold,
            self.total_gold_earned
        ])

    def update(self, gold_stats: GoldStats):
        self.total_gold.setValue(str(gold_stats.total_gold))
        self.total_gold_earned.setValue(str(gold_stats.total_gold_earned))


class XPRow(Row):
    def __init__(self):
        self.total_xp = ValueDisplay(assets_const.IcCoins, str(0))
        self.total_xp_earned = ValueDisplay(assets_const.IcCoins, str(0))

        Row.__init__(self, [
            self.total_xp,
            self.total_xp_earned
        ])

    def update(self, xp_stats: XPStats):
        self.total_xp.setValue(str(xp_stats.total_xp))
        self.total_xp_earned.setValue(str(xp_stats.total_xp_earned))


class StatsLayout(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        layout = QVBoxLayout(self)
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        self.gold_row = GoldRow()
        self.xp_row = XPRow()

        layout.addWidget(self.gold_row)
        layout.addWidget(self.xp_row)

    def update(self, stats: Stats):
        self.gold_row.update(stats.gold)
        self.xp_row.update(stats.xp)

    def refresh(self):
        stats = Engine.get_stats()
        self.update(stats)
