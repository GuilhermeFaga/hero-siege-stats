from PySide6.QtWidgets import QBoxLayout
from PySide6.QtWidgets import QWidget


class Row(QWidget):
    def __init__(self, widgets):
        QWidget.__init__(self)

        self.setLayout(QBoxLayout(QBoxLayout.Direction.LeftToRight))
        for widget in widgets:
            self.layout().addWidget(widget)
