from PySide6.QtCore import Qt

from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QComboBox

from src.gui.components.image import ImageWidget

from src.consts import assets as assets_const
from src.consts.enums import Sizes, Regions
from src.utils import assets

from src.engine import Engine
from src.engine.backend import Backend


region_str_to_enum: dict[str, Regions] = {
    "Asia-Karponia": Regions.ASIA,
    "America-Mevius": Regions.AMERICAS,
    "Europe-Inoya": Regions.EUROPE_1,
    "Europe-Damien": Regions.EUROPE_2
}


xlarge_bg = """
    #GroupBox {
        background-image: url('%s');
        background-repeat: no-repeat;
    }
""" % assets.hud(assets_const.HudValueDisplayXl)

large_bg = """
    #GroupBox {
        background-image: url('%s');
        background-repeat: no-repeat;
    }
""" % assets.hud(assets_const.HudValueDisplayLg)

normal_bg = """
    #GroupBox {
        background-image: url('%s');
        background-repeat: no-repeat;
    }
""" % assets.hud(assets_const.HudValueDisplayMd)

small_bg = """
    #GroupBox {
        background-image: url('%s');
        background-repeat: no-repeat;
    }
""" % assets.hud(assets_const.HudValueDisplaySm)


display_width = {
    Sizes.Small: 96,
    Sizes.Medium: 104,
    Sizes.Large: 120,
    Sizes.XLarge: 125,
}

display_bg = {
    Sizes.Small: small_bg,
    Sizes.Medium: normal_bg,
    Sizes.Large: large_bg,
    Sizes.XLarge: xlarge_bg
}


class GroupBox(QFrame):
    icon: ImageWidget
    label: QLabel

    def __init__(self, icon: str | None = None, value: str | None = None, size: Sizes = Sizes.Large):
        QFrame.__init__(self)

        self.setObjectName("GroupBox")

        self.setFixedSize(display_width[size], 26)
        self.setStyleSheet(display_bg[size])

        layout = QHBoxLayout(self)

        layout.setSpacing(8)
        layout.setContentsMargins(8, 0, 8, 0)

        if icon is not None:
            self.icon = ImageWidget(assets.icon(icon))
            layout.addWidget(self.icon)

        self.label = QLabel()

        if value is not None:
            self.label.setText(value)

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(self.label)


class ComboGroupBox(GroupBox):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(None)


class ValueDisplay(QWidget):
    groupBox: GroupBox

    def __init__(self, icon: str | None = None, value: str | None = None, size: Sizes = Sizes.Large):
        QWidget.__init__(self)

        layout = QHBoxLayout(self)

        self.groupBox = GroupBox(icon=icon, value=value, size=size)
        layout.addWidget(self.groupBox)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def setIcon(self, icon: str):
        self.groupBox.icon.setIcon(assets.icon(icon))

    def setValue(self, value: str):
        self.groupBox.label.setText(value)


class ComboBox(QComboBox):
    groupBox: GroupBox

    def __init__(self):
        QComboBox.__init__(self)

        for region in Regions:
            self.addItem(region.value)

        layout = QHBoxLayout(self)

        self.groupBox = ComboGroupBox()
        layout.addWidget(self.groupBox)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.activated.connect(slot=self.on_select)

    def on_select(self) -> None:
        Backend.initialize(Engine.queue_an_event, region=region_str_to_enum[self.currentText()])
        Engine.reset_stats()
