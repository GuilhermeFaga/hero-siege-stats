from PySide6.QtCore import Qt

from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QLabel

from src.gui.components.image import ImageWidget

from src.consts import assets as assets_const
from src.utils import assets


class GroupBox(QFrame):
    icon: ImageWidget
    label: QLabel

    def __init__(self):
        QFrame.__init__(self)

        self.setFixedSize(146, 26)

        self.setObjectName("GroupBox")

        layout = QHBoxLayout(self)

        layout.setSpacing(8)
        layout.setContentsMargins(8, 0, 8, 0)

        self.icon = ImageWidget(assets.icon(assets_const.IcCoins))
        self.label = QLabel()

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(self.icon)
        layout.addWidget(self.label)


class ValueDisplay(QWidget):
    groupBox: GroupBox

    def __init__(self, icon: str, value: str):
        QWidget.__init__(self)

        layout = QHBoxLayout(self)

        self.groupBox = GroupBox()
        layout.addWidget(self.groupBox)

        self.setIcon(icon)
        self.setValue(value)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def setIcon(self, icon: str):
        self.groupBox.icon = ImageWidget(assets.icon(icon))

    def setValue(self, value: str):
        self.groupBox.label.setText(value)
