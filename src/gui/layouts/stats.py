from PySide6.QtWidgets import QVBoxLayout, QPushButton
from PySide6.QtWidgets import QWidget

from src.gui.components.value_display import ValueDisplay
from src.gui.components.satanic_zone_display import SatanicZoneDisplay
from src.gui.components.row import Row
from src.gui.components.button import Button

from src.models.stats.satanic_zone import SatanicZoneStats
from src.models.stats.stats import Stats
from src.models.stats.session import Session
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats
from src.models.stats.added_items import AddedItemsStats

from src.engine import Engine

from src.consts import assets as assets_const
from src.consts.enums import Sizes


class SessionRow(Row):
    def __init__(self):
        self.session_duration = ValueDisplay(
            icon=assets_const.IcTime, value=str(0))
        self.mail = ValueDisplay(
            icon=assets_const.IcMailOff, value=str(0), size=Sizes.Medium)

        self.reset_button = Button("Reset Stats", size=Sizes.Medium)
        self.reset_button.onclick(self._handle_reset)

        Row.__init__(self, [
            self.session_duration,
            self.mail,
            self.reset_button,
        ])

    def _handle_reset(self):
        Engine.reset_stats()
        # Update all stats displays
        self.parent().refresh()  # This will update all stats through StatsLayout.refresh()

    def update_session(self, session: Session):
        self.session_duration.setValue(session.get_duration_str())
        self.mail.setIcon(
            assets_const.IcMailOn if session.has_mail else assets_const.IcMailOff)
        self.mail.setValue("Mail!" if session.has_mail else "No mail")

class SatanicZoneRow(Row):
    def __init__(self):
        self.satanic_zone_buffs = SatanicZoneDisplay()
        self.satanic_zone_name = ValueDisplay(value="Satanic_Zone",size=Sizes.XL)
        Row.__init__(self,[self.satanic_zone_buffs,self.satanic_zone_name])

    def update_satanic(self, satanic_zone:SatanicZoneStats):
        self.satanic_zone_buffs.set_satanic_zone_info(satanic_zone.satanic_zone_info)
        self.satanic_zone_buffs.set_buff_icons_and_tooltip()
        if satanic_zone.satanic_zone_info is not None:
            self.satanic_zone_name.setValue(satanic_zone.satanic_zone_info.satanic_zone)

class GoldRow(Row):
    def __init__(self):
        self.total_gold = ValueDisplay(icon=assets_const.IcCoins, value=str(0))
        self.total_gold_earned = ValueDisplay(value=str(0), size=Sizes.Medium)
        self.gold_per_hour = ValueDisplay(value=str(0), size=Sizes.Medium)

        Row.__init__(self, [
            self.total_gold,
            self.total_gold_earned,
            self.gold_per_hour
        ])

    def update_gold(self, gold_stats: GoldStats):
        self.total_gold.setValue(f"{gold_stats.total_gold:,}")
        self.total_gold_earned.setValue(f"+{gold_stats.total_gold_earned:,}")
        self.gold_per_hour.setValue(f"{gold_stats.gold_per_hour:,}/h")


class XPRow(Row):
    def __init__(self):
        self.total_xp = ValueDisplay(icon=assets_const.IcXp, value=str(0))
        self.total_xp_earned = ValueDisplay(value=str(0), size=Sizes.Medium)
        self.total_xp_per_hour = ValueDisplay(value=str(0), size=Sizes.Medium)

        Row.__init__(self, [
            self.total_xp,
            self.total_xp_earned,
            self.total_xp_per_hour
        ])

    def update_xp(self, xp_stats: XPStats):
        self.total_xp.setValue(f"{xp_stats.total_xp:,}")
        self.total_xp_earned.setValue(f"+{xp_stats.total_xp_earned:,}")
        self.total_xp_per_hour.setValue(f"{xp_stats.xp_per_hour:,}/h")


class AddedItemsRow(Row):
    def __init__(self):
        self.total_angelic = ValueDisplay(
            icon=assets_const.IcChest, value=str(0))
        self.total_heroic = ValueDisplay(value=str(0), size=Sizes.Medium)
        self.total_satanic = ValueDisplay(value=str(0), size=Sizes.Medium)

        Row.__init__(self, [
            self.total_angelic,
            self.total_heroic,
            self.total_satanic
        ])

    def update_added_item(self, added_items_stats: AddedItemsStats):
        angelic_and_unholy_total = added_items_stats.added_items['Angelic']['total'] + added_items_stats.added_items['Unholy']['total']
        angelic_and_unholy_mf = added_items_stats.added_items['Angelic']['mf'] + added_items_stats.added_items['Unholy']['mf']
        self.total_angelic.setValue(
            f"{assets_const.FcAngelic}{angelic_and_unholy_total:,} {assets_const.FcBlue}({angelic_and_unholy_mf:,})")
        self.total_heroic.setValue(
            f"{assets_const.FcHeroic}{added_items_stats.added_items['Heroic']['total']:,} {assets_const.FcBlue}({added_items_stats.added_items['Heroic']['mf']:,}) {assets_const.FcDefault}| {assets_const.FcHeroic}{added_items_stats.items_per_hour['Heroic']:,}/h")
        self.total_satanic.setValue(
            f"{assets_const.FcSatanic}{added_items_stats.added_items['Satanic']['total']:,} {assets_const.FcBlue}({added_items_stats.added_items['Satanic']['mf']:,}) {assets_const.FcDefault}| {assets_const.FcSatanic}{added_items_stats.items_per_hour['Satanic']:,}/h")


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
        self.added_items_row = AddedItemsRow()
        self.satanic_zone_row = SatanicZoneRow()

        layout.addWidget(self.session_row)
        layout.addWidget(self.gold_row)
        layout.addWidget(self.xp_row)
        layout.addWidget(self.added_items_row)
        layout.addWidget(self.satanic_zone_row)

    def update_stats(self, stats: Stats):
        self.session_row.update_session(stats.session)
        self.gold_row.update_gold(stats.gold)
        self.xp_row.update_xp(stats.xp)
        self.added_items_row.update_added_item(stats.added_items)
        self.satanic_zone_row.update_satanic(stats.satanic_zone)


    def refresh(self):
        stats = Engine.get_stats()
        self.update_stats(stats)
