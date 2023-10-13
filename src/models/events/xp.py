from src.models.messages.xp import XPMessage
from src.models.events.base import BaseEvent

from src.consts import events as consts


class XPEvent(BaseEvent):
    value: int

    def __init__(self, xp_message: XPMessage):
        self.name = consts.EvNameUpdateXP
        self.value = xp_message.xp

    @staticmethod
    def cast(model):
        if isinstance(model, XPEvent):
            return model
        else:
            raise Exception("Invalid model")
