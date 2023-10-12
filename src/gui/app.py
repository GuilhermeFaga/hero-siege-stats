import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel

from src.engine import initialize


def run():
    print("Initializing...")
    sniffer = initialize()

    WIDTH = 300
    HEIGHT = 220

    app = QApplication(sys.argv)
    label = QLabel("Hello World")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.show()

    try:
        sys.exit(app.exec())
    except:
        print("Exiting...")
        sniffer.stop()
        print("Exited")
