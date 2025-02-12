from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from src.consts.enums import Sizes

button_width = {
    Sizes.Small: 96,
    Sizes.Medium: 104,
    Sizes.Large: 120,
    Sizes.XL: 212,
}

class Button(QWidget):
    button: QPushButton

    def __init__(self, text: str, size: Sizes = Sizes.Medium):
        QWidget.__init__(self)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton(text)
        self.button.setFixedSize(button_width[size], 26)

        self.button.setStyleSheet("""
            QPushButton {
                background-color: #2f3436;
                border: 2px solid #1a1c1e;
                border-radius: 2px;
                color: #c0c0c0;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #3f4446;
            }
            QPushButton:pressed {
                background-color: #1a1c1e;
            }
        """)

        layout.addWidget(self.button)

    def onclick(self, callback):
        """Connect click event to callback"""
        self.button.clicked.connect(callback) 