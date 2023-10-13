import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from src.engine import Engine
from src.gui.widgets.main import MainWidget


def run():
    print("Initializing...")
    sniffer = Engine.initialize()

    WIDTH = 300
    HEIGHT = 220

    app = QApplication(sys.argv)

    geometry = app.screens()[0].size()

    widget = MainWidget()
    widget.resize(WIDTH, HEIGHT)
    widget.move(0, geometry.height() - HEIGHT - 280)

    widget.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    widget.show()

    try:
        sys.exit(app.exec())
    except:
        print("Exiting...")
        sniffer.stop()
        print("Exited")
