from src.models.messages.base import BaseMessage
from src.consts.satanic_buffs import satanic_buffs
from src.consts.satanic_zone_names import satanic_zone_names
from src.utils import assets
from src.consts import assets as assets_const
class SzBuff:
    buff_name: str
    buff_description: str | None
    buff_icon: str
    def __init__(self,sz_buff:int):
        self.buff_name = list(satanic_buffs)[sz_buff-1]
        self.buff_description = satanic_buffs.get(self.buff_name)
        buff_icon = assets_const.get_buff_icon(f"IcBuff_{sz_buff}")
        self.buff_icon = assets.icon(buff_icon)


class SzInfo:
    buffs: list
    satanic_zone: str
    def __init__(self,sz_zone: str,sz_buffs:str):
        self.buffs = []
        for buff in sz_buffs.split("|"):
            b = SzBuff(int(buff))
            self.buffs.append(b)
        temp = sz_zone.split("_")
        sz_act : int = int(temp[1])
        sz_zone_name_id: int = int(temp[2])
        all_act_zone_names_of_id : list | None = satanic_zone_names.get(sz_act)
        if all_act_zone_names_of_id:
            sz_zone_name = all_act_zone_names_of_id[sz_zone_name_id-1]
            self.satanic_zone = f"Act {sz_act} : {sz_zone_name}"
        else:
            self.satanic_zone = ""
   


class SatanicZoneMessage(BaseMessage):
    satanic_info: SzInfo
    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.satanic_info = SzInfo(msg_dict['satanicZoneName'],msg_dict['buffs'])
