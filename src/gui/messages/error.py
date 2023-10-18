from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QFont

from src.consts.enums import ConnectionError


class ErrorMessages:

    @staticmethod
    def message_box(parent) -> QMessageBox:
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Critical)

        msg.setStyleSheet("""QLabel {font-family: %s;}""" %
                          (QFont().defaultFamily()))

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        return msg

    @staticmethod
    def no_interface(parent):
        msg = ErrorMessages.message_box(parent)
        msg.setWindowTitle("Unable to connect to the internet!")
        msg.setText(
            "Make sure that you are connected to the internet.")

        msg.show()

    @staticmethod
    def server_not_responding(parent):
        msg = ErrorMessages.message_box(parent)
        msg.setWindowTitle("Unable to connect to the game server!")
        msg.setText(
            "It appears that the game's server is offline.")

        msg.show()

    @staticmethod
    def interface_missing(parent):
        msg = ErrorMessages.message_box(parent)
        msg.setWindowTitle("Unable to get network interface!")
        msg.setText(
            "On windows make sure that WinPcap is installed in your system.")
        msg.setInformativeText("WinPcap can be installed from <a href='{}'>here</a> <br>\
            <b>Make sure to install with the \"Install Npcap in WinPcap API-compatible Mode\"<b> option."
                               .format('https://npcap.com/dist/npcap-1.77.exe'))

        msg.show()

    @staticmethod
    def get_message(parent, error: ConnectionError):
        if error == ConnectionError.InterfaceNotFound:
            ErrorMessages.interface_missing(parent)
        elif error == ConnectionError.ServerNotResponding:
            ErrorMessages.server_not_responding(parent)
        elif error == ConnectionError.NoInternet:
            ErrorMessages.no_interface(parent)
