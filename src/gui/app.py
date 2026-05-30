import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication

from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QIcon

from scapy.sendrecv import AsyncSniffer


from src.gui.widgets.main import MainWidget

from src.gui.messages.error import ErrorMessages
from src.gui.messages.version import VersionMessages

from .styling import style

from src.consts.enums import ConnectionError

from src.consts import assets as assets_const
from src.consts.logger import LOGGING_NAME
from src.utils import assets

from src.utils.version import current_version as get_current_version
from src.utils.version import latest_version as get_latest_version
from src.utils.icon_fix import icon_fix


def run():
    logger = logging.getLogger(LOGGING_NAME)
    logger.log(logging.INFO, "Initializing...")
    if not sys.platform.startswith("win32"):
        logger.info("Running on a non-Windows platform")
    icon_fix()
    WIDTH = 300
    HEIGHT = 0

    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(assets.font("cookierunbold.ttf"))
    QFontDatabase.addApplicationFont(assets.font("otsutomefont.ttf"))

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
    current_version, latest_version = (get_current_version(), get_latest_version())

    if latest_version and current_version != latest_version:
        VersionMessages.outdated_version(widget)
    from src.engine.sniffer_manager import sniffer_manager

    if isinstance(sniffer_manager.sniffer, ConnectionError):
        ErrorMessages.get_message(widget, sniffer_manager.sniffer)
        logger.log(logging.WARNING, "Sniffer unavailable; UI will stay open")
        logger.log(logging.INFO, sniffer_manager.sniffer)

    exit_code = 0
    try:
        exit_code = app.exec()
    except KeyboardInterrupt:
        logger.log(logging.INFO, "Application terminated by user (KeyboardInterrupt)")
    except RuntimeError as e:
        logger.log(logging.ERROR, f"Qt runtime error: {str(e)}")
        exit_code = 1
    except Exception as e:
        logger.log(logging.ERROR, f"Unexpected error: {str(e)}")
        exit_code = 1
    finally:
        logger.log(logging.INFO, "Exiting...")
        if isinstance(sniffer_manager.sniffer, AsyncSniffer):
            try:
                if sniffer_manager.sniffer.running:
                    sniffer_manager.sniffer.stop()
            except Exception as e:
                logger.log(logging.WARNING, f"Failed to stop sniffer cleanly: {e}")
        logger.log(logging.INFO, "Exited")

    return exit_code
