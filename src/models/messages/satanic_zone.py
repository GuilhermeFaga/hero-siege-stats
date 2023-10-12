from src.models.messages.base import BaseMessage


class SatanicZoneMessage(BaseMessage):
    satanic_zone_name: str

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.satanic_zone_name = msg_dict['satanicZoneName']
