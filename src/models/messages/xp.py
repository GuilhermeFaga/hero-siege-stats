import re

from src.models.messages.base import BaseMessage


class XPMessage(BaseMessage):
    xp: int
    totalGuildXp: int

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        match = re.search(r"\d+", self.message)
        self.xp = int(match.group(0)) if match is not None else 0
        self.totalGuildXp = msg_dict['totalGuildXp']
