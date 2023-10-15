from PySide6.QtCore import Qt

from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QLabel

from src.gui.components.image import ImageWidget

from src.consts import assets as assets_const
from src.utils import assets


normal_bg = """
    #GroupBox {
        background-image: url('%s');
        background-repeat: no-repeat;
    }
""" % assets.hud(assets_const.HudValueDisplay)

small_bg = """
    #GroupBox {
        background-image: url('%s');
        background-repeat: no-repeat;
    }
""" % assets.hud(assets_const.HudValueDisplaySm)


class GroupBox(QFrame):
    icon: ImageWidget
    label: QLabel

    def __init__(self, icon: str | None = None, value: str | None = None):
        QFrame.__init__(self)

        self.setObjectName("GroupBox")

        layout = QHBoxLayout(self)

        layout.setSpacing(8)
        layout.setContentsMargins(8, 0, 8, 0)

        if icon is not None:
            self.setFixedSize(146, 26)
            self.setStyleSheet(normal_bg)
            self.icon = ImageWidget(assets.icon(icon))
            layout.addWidget(self.icon)
        else:
            self.setFixedSize(93, 26)
            self.setStyleSheet(small_bg)

        self.label = QLabel()

        if value is not None:
            self.label.setText(value)

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(self.label)


class ValueDisplay(QWidget):
    groupBox: GroupBox

    def __init__(self, icon: str | None = None, value: str | None = None):
        QWidget.__init__(self)

        layout = QHBoxLayout(self)

        self.groupBox = GroupBox(icon=icon, value=value)
        layout.addWidget(self.groupBox)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def setIcon(self, icon: str):
        self.groupBox.icon.setIcon(assets.icon(icon))

    def setValue(self, value: str):
        self.groupBox.label.setText(value)
