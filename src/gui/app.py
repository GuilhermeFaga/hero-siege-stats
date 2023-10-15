import sys

from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication

from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QIcon

from scapy.sendrecv import AsyncSniffer

from src.engine import Engine
from src.gui.messages.error import ErrorMessages
from src.gui.widgets.main import MainWidget

from .styling import style

from src.consts.enums import ConnectionError

from src.consts import assets as assets_const
from src.utils import assets

from src.utils.icon_fix import icon_fix


icon_fix()


def run():
    print("Initializing...")
    initialization_result = Engine.initialize()

    WIDTH = 300
    HEIGHT = 0

    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(assets.font('cookierunbold.ttf'))
    QFontDatabase.addApplicationFont(assets.font('otsutomefont.ttf'))

    app.setStyleSheet(style)
    app.setStyle("fusion")

    app_icon = QIcon()
    app_icon.addFile(assets.icon(assets_const.IcLogo16), QSize(16, 16))
    app_icon.addFile(assets.icon(assets_const.IcLogo24), QSize(24, 24))
    app_icon.addFile(assets.icon(assets_const.IcLogo32), QSize(32, 32))
    app_icon.addFile(assets.icon(assets_const.IcLogo48), QSize(48, 48))
    app_icon.addFile(assets.icon(assets_const.IcLogo256), QSize(256, 256))
    app.setWindowIcon(app_icon)

    geometry = app.screens()[0].size()

    widget = MainWidget()
    widget.resize(WIDTH, HEIGHT)
    widget.move(0, geometry.height() - HEIGHT - 280)

    widget.setWindowTitle("Hero Siege Stats")

    widget.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    widget.show()

    if isinstance(initialization_result, ConnectionError):
        ErrorMessages.get_message(widget, initialization_result)
        print("Connection error")
        print(initialization_result)

    try:
        sys.exit(app.exec())
    except:
        print("Exiting...")
        if isinstance(initialization_result, AsyncSniffer):
            initialization_result.stop()
        print("Exited")
