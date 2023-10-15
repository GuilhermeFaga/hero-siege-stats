from cgitb import small
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from src.gui.components.value_display import ValueDisplay
from src.gui.components.row import Row

from src.models.stats.stats import Stats
from src.models.stats.session import Session
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats

from src.engine import Engine

from src.consts import assets as assets_const


class SessionRow(Row):
    def __init__(self):
        self.session_duration = ValueDisplay(
            icon=assets_const.IcTime, value=str(0))
        self.mail = ValueDisplay(
            icon=assets_const.IcMailOff, value=str(0), small=True)

        Row.__init__(self, [
            self.session_duration,
            self.mail
        ])

    def update(self, session: Session):
        self.session_duration.setValue(session.get_duration_str())
        self.mail.setIcon(
            assets_const.IcMailOn if session.has_mail else assets_const.IcMailOff)
        self.mail.setValue("Mail!" if session.has_mail else "No mail")


class GoldRow(Row):
    def __init__(self):
        self.total_gold = ValueDisplay(icon=assets_const.IcCoins, value=str(0))
        self.total_gold_earned = ValueDisplay(value=str(0), small=True)
        self.gold_per_hour = ValueDisplay(value=str(0), small=True)

        Row.__init__(self, [
            self.total_gold,
            self.total_gold_earned,
            self.gold_per_hour
        ])

    def update(self, gold_stats: GoldStats):
        self.total_gold.setValue(f"{gold_stats.total_gold:,}")
        self.total_gold_earned.setValue(f"+{gold_stats.total_gold_earned:,}")
        self.gold_per_hour.setValue(f"{gold_stats.gold_per_hour:,}/h")


class XPRow(Row):
    def __init__(self):
        self.total_xp = ValueDisplay(icon=assets_const.IcXp, value=str(0))
        self.total_xp_earned = ValueDisplay(value=str(0), small=True)
        self.total_xp_per_hour = ValueDisplay(value=str(0), small=True)

        Row.__init__(self, [
            self.total_xp,
            self.total_xp_earned,
            self.total_xp_per_hour
        ])

    def update(self, xp_stats: XPStats):
        self.total_xp.setValue(f"{xp_stats.total_xp:,}")
        self.total_xp_earned.setValue(f"+{xp_stats.total_xp_earned:,}")
        self.total_xp_per_hour.setValue(f"{xp_stats.xp_per_hour:,}/h")


class StatsLayout(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        layout = QVBoxLayout(self)
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        self.session_row = SessionRow()
        self.gold_row = GoldRow()
        self.xp_row = XPRow()

        layout.addWidget(self.session_row)
        layout.addWidget(self.gold_row)
        layout.addWidget(self.xp_row)

    def update(self, stats: Stats):
        self.session_row.update(stats.session)
        self.gold_row.update(stats.gold)
        self.xp_row.update(stats.xp)

    def refresh(self):
        stats = Engine.get_stats()
        self.update(stats)
