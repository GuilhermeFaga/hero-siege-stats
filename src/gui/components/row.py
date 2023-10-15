from PySide6.QtWidgets import QBoxLayout
from PySide6.QtWidgets import QWidget


class Row(QWidget):
    def __init__(self, widgets):
        QWidget.__init__(self)

        layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, self)
        layout.setSizeConstraint(QBoxLayout.SizeConstraint.SetFixedSize)

        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        for widget in widgets:
            self.layout().addWidget(widget)
