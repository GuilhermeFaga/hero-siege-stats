from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel

from src.gui.components.row import Row
from src.models.stats.stats import Stats
from src.models.stats.gold import GoldStats

from src.engine import Engine


class GoldRow(Row):
    def __init__(self):
        self.gold_label = QLabel(str(0))
        Row.__init__(self, [
            QLabel("Gold:"),
            self.gold_label
        ])

    def update(self, gold: GoldStats):
        self.gold_label.setText(str(gold.total_gold))


class StatsLayout(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setLayout(QVBoxLayout())

        self.gold_row = GoldRow()
        self.layout().addWidget(self.gold_row)

    def update(self, stats: Stats):
        self.gold_row.update(stats.gold)

    def refresh(self):
        stats = Engine.get_stats()
        self.update(stats)
