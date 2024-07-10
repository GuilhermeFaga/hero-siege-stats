from src.models.messages.satanic_zone import SatanicZoneMessage, SzInfo
from src.models.events.base import BaseEvent

from src.consts import events as consts


class SatanicZoneEvent(BaseEvent):
    value: SzInfo
    def __init__(self, satanic_zone_message: SatanicZoneMessage):
        self.name = consts.EvNameUpdateSatanicZone
        self.value = satanic_zone_message.satanic_info

    @staticmethod
    def cast(model):
        if isinstance(model, SatanicZoneEvent):
            return model
        else:
            raise Exception("Invalid model")