from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame
from src.consts import assets as assets_const
from src.consts.enums import Sizes
from src.gui.components.image import ImageWidget
from src.models.messages.satanic_zone import SzInfo
from src.utils import assets



display_width = {
    Sizes.Small: 96,
    Sizes.Medium: 104,
    Sizes.Large: 120
}

class SatanicZoneGroupBox(QFrame):
    icons: list[ImageWidget]
    sz_buffs_layout: QHBoxLayout
    def __init__(self, size: Sizes = Sizes.Large):
        QFrame.__init__(self)
        self.setStyleSheet("""
            QToolTip {
                background-color: black;
                color: white;
                border: 2px solid rgb(150, 37, 56);
                padding: 5px;
            }
        """)
        self.sz_buffs_layout = QHBoxLayout(self)

        self.icons = []
        self.setObjectName("GroupBox")

        self.setFixedSize(display_width[size], 26)

        

        self.sz_buffs_layout.setSpacing(10)
        self.sz_buffs_layout.setContentsMargins(8, 0, 8, 0)

        for i in range(0,3):
            icon = ImageWidget(assets.icon(assets_const.IcBuffDefault))
            self.icons.append(icon)
            self.sz_buffs_layout.addWidget(icon)
        

    def set_buffs_to_default_icon(self):
        for icon in self.icons:
            icon.setIcon(assets.icon(assets_const.IcBuffDefault))
            icon.setToolTip("")

class SatanicZoneDisplay(QWidget):
    groupBox: SatanicZoneGroupBox
    satanic_zone_info: SzInfo | None
    def __init__(self, satanic_zone_info:SzInfo | None = None , size: Sizes = Sizes.Large):
        QWidget.__init__(self)
        self.satanic_zone_info = satanic_zone_info
        layout = QHBoxLayout(self)

        self.groupBox = SatanicZoneGroupBox(size=size)
        layout.addWidget(self.groupBox)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def set_buff_icons_and_tooltip(self):
        if self.satanic_zone_info is not None:
            if len(self.groupBox.icons) != len(self.satanic_zone_info.buffs):
                self.groupBox.set_buffs_to_default_icon()
            if self.satanic_zone_info is not None:
                for i,buff in enumerate(self.satanic_zone_info.buffs):
                    self.groupBox.icons[i].setIcon(buff.buff_icon)
                    self.groupBox.icons[i].setToolTip(f"{buff.buff_name} : {buff.buff_description}")

    def set_satanic_zone_info(self, sz_info: SzInfo):
        self.satanic_zone_info = sz_info
        