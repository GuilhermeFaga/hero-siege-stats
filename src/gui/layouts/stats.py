from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel

from src.gui.components.row import Row
from src.models.stats.stats import Stats
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats

from src.engine import Engine


class GoldRow(Row):
    def __init__(self):
        self.total_gold_label = QLabel(str(0))
        self.total_gold_earned_label = QLabel(str(0))
        Row.__init__(self, [
            QLabel("Gold:"),
            self.total_gold_label,
            QLabel("Gold earned:"),
            self.total_gold_earned_label
        ])

    def update(self, gold_stats: GoldStats):
        self.total_gold_label.setText(str(gold_stats.total_gold))
        self.total_gold_earned_label.setText(str(gold_stats.total_gold_earned))


class XPRow(Row):
    def __init__(self):
        self.total_xp_earned_label = QLabel(str(0))
        Row.__init__(self, [
            QLabel("XP earned:"),
            self.total_xp_earned_label
        ])

    def update(self, xp_stats: XPStats):
        self.total_xp_earned_label.setText(str(xp_stats.total_xp_earned))


class StatsLayout(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setLayout(QVBoxLayout())

        self.gold_row = GoldRow()
        self.xp_row = XPRow()

        self.layout().addWidget(self.gold_row)
        self.layout().addWidget(self.xp_row)

    def update(self, stats: Stats):
        self.gold_row.update(stats.gold)
        self.xp_row.update(stats.xp)

    def refresh(self):
        stats = Engine.get_stats()
        self.update(stats)
