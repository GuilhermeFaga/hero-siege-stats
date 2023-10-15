
from datetime import datetime


class Session:
    start_time: datetime

    def __init__(self):
        self.start_time = datetime.now()

    def get_duration(self):
        return datetime.now() - self.start_time

    def get_duration_str(self):
        return str(self.get_duration()).split(".")[0]

    def calculate_value_per_hour(self, value: int):
        duration = self.get_duration()
        if duration.seconds == 0:
            return 0
        return int(value / (duration.seconds / 3600))
