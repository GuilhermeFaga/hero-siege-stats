from src.models.messages.base import BaseMessage, get_message_field
from src.consts.satanic_buffs import satanic_buffs
from src.consts.satanic_zone_names import satanic_zone_names
from src.utils import assets
from src.consts import assets as assets_const


class SzBuff:
    buff_name: str
    buff_description: str | None
    buff_icon: str

    def __init__(self, sz_buff: int):
        buff_names = list(satanic_buffs)
        self.buff_name = (
            buff_names[sz_buff - 1]
            if 0 < sz_buff <= len(buff_names)
            else f"Unknown Buff {sz_buff}"
        )
        self.buff_description = satanic_buffs.get(self.buff_name)
        buff_icon = getattr(assets_const, f"IcBuff_{sz_buff}", assets_const.IcBuffDefault)
        self.buff_icon = assets.icon(buff_icon)


class SzInfo:
    buffs: list
    satanic_zone: str

    def __init__(self, sz_zone: str, sz_buffs: str | list):
        self.buffs = []
        buffs = (
            sz_buffs
            if isinstance(sz_buffs, list)
            else str(sz_buffs).replace(",", "|").split("|")
        )
        for buff in buffs:
            try:
                self.buffs.append(SzBuff(int(buff)))
            except (TypeError, ValueError):
                continue

        temp = str(sz_zone).split("_")
        if len(temp) >= 3 and temp[1].isdigit() and temp[2].isdigit():
            sz_act: int = int(temp[1])
            sz_zone_name_id: int = int(temp[2])
            all_act_zone_names_of_id: list | None = satanic_zone_names.get(sz_act)
            if (
                all_act_zone_names_of_id
                and 0 < sz_zone_name_id <= len(all_act_zone_names_of_id)
            ):
                sz_zone_name = all_act_zone_names_of_id[sz_zone_name_id - 1]
                self.satanic_zone = f"Act {sz_act} : {sz_zone_name}"
            else:
                self.satanic_zone = str(sz_zone)
        else:
            self.satanic_zone = str(sz_zone)
   


class SatanicZoneMessage(BaseMessage):
    satanic_info: SzInfo

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.satanic_info = SzInfo(
            get_message_field(
                msg_dict,
                'satanicZoneName',
                'satanic_zone_name',
                default='',
            ),
            get_message_field(
                msg_dict,
                'buffs',
                'satanicZoneBuffs',
                'satanic_zone_buffs',
                'zoneBuffs',
                'zone_buffs',
                default='',
            ),
        )
