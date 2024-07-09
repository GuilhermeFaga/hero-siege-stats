from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from src.gui.layouts.stats import StatsLayout


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setObjectName("MainWidget")
        self.setAttribute(Qt.WA_AlwaysShowToolTips, True)
        layout = QVBoxLayout(self)
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.view = StatsLayout()
        self.layout().addWidget(self.view)

        self.refresh()

        timer = QTimer(self)
        timer.timeout.connect(self.refresh)
        timer.start(500)

    def refresh(self):
        self.view.refresh()
