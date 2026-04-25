import re

from src.models.messages.base import BaseMessage, int_message_field


class XPMessage(BaseMessage):
    xp: int
    totalGuildXp: int

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        match = re.search(r"\d+", self.message)
        self.xp = int(match.group(0)) if match is not None else int_message_field(
            msg_dict,
            'xp',
            'experienceGained',
            'experience_gained',
        )
        self.totalGuildXp = int_message_field(
            msg_dict,
            'totalGuildXp',
            'total_guild_xp',
            'totalGuildExp',
            'total_guild_exp',
        )
