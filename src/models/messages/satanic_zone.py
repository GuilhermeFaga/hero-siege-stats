from src.models.messages.base import BaseMessage
from src.consts.satanic_buffs import satanic_buffs


class SzBuff:
    buff_name: str
    buff_description: str
    buff_icon: str
    def __init__(self,sz_buff:int):
        self.buff_name = list(satanic_buffs)[sz_buff-1]
        self.buff_description = satanic_buffs.get(self.buff_name)


class SzInfo:
    buffs: list
    satanic_zone: str
    def __init__(self,sz_zone: str,sz_buffs:str):
        self.buffs = []
        for buff in sz_buffs.split("|"):
            b = SzBuff(int(buff))
            self.buffs.append(b)
        self.satanic_zone = sz_zone
   


class SatanicZoneMessage(BaseMessage):
    satanic_info: SzInfo
    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.satanic_info = SzInfo(msg_dict['satanicZoneName'],msg_dict['buffs'])
