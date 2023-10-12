import re


class XPMessage:
    status: str
    message: str
    xp: int
    totalGuildXp: int

    def __init__(self, msg_dict: dict):
        self.status = msg_dict['status']
        self.message = msg_dict['message']
        match = re.search(r"\d+", self.message)
        self.xp = int(match.group(0)) if match is not None else 0
        self.totalGuildXp = msg_dict['totalGuildXp']
