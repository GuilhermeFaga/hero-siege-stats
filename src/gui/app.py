import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QIcon

from src.engine import Engine
from src.gui.widgets.main import MainWidget

from .styling import style
from src.consts import assets as assets_const
from src.utils import assets


def run():
    print("Initializing...")
    sniffer = Engine.initialize()

    WIDTH = 300
    HEIGHT = 0

    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(assets.font('cookierunbold.ttf'))
    QFontDatabase.addApplicationFont(assets.font('otsutomefont.ttf'))

    app.setStyleSheet(style)
    app.setStyle("fusion")

    geometry = app.screens()[0].size()

    widget = MainWidget()
    widget.resize(WIDTH, HEIGHT)
    widget.move(0, geometry.height() - HEIGHT - 280)

    widget.setWindowTitle("Hero Siege Stats")
    widget.setWindowIcon(QIcon(assets.icon(assets_const.IcLogo)))

    widget.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    widget.show()

    try:
        sys.exit(app.exec())
    except:
        print("Exiting...")
        sniffer.stop()
        print("Exited")
