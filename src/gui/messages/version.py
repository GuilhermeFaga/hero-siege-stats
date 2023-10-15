from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QFont

from src.utils.version import current_version as get_current_version
from src.utils.version import latest_version as get_latest_version


class VersionMessages:

    @staticmethod
    def outdated_version(parent):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Update available!")

        msg.setText("Another version of app is available.")
        msg.setInformativeText("You are using app in version {}, latest version is {}".format(
            get_current_version(), get_latest_version()))

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg.setStyleSheet("""QLabel {font-family: %s;}""" %
                          (QFont().defaultFamily()))

        msg.show()
