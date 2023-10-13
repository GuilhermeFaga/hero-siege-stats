from datetime import datetime

from src.gui.widgets.main import MainView
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Signal


class GameStats:
    session_start_time: str

    test = None

    def __init__(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_event(self, event):
        print("GameStats.process_event:", event)
        self.test = event

    def reset(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_test(self):
        return self.test
