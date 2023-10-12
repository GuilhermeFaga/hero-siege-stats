from datetime import datetime


class GameStats():
    session_start_time: str

    def __init__(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pass

    def process_event(self, event):
        print("GameStats.process_event:", event)

    def register_event(self, event):
        pass

    def reset(self):
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
