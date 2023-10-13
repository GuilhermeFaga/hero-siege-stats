from typing import Callable

from src.models.messages.gold import GoldMessage
from src.models.messages.xp import XPMessage
from src.models.messages.mail import MailMessage
from src.models.messages.added_item import AddedItemMessage
from src.models.messages.satanic_zone import SatanicZoneMessage


EvNameUpdateGold: str = 'UpdateGold'
EvNameUpdateXP: str = 'UpdateXP'
EvNameUpdateMail: str = 'UpdateMail'
EvNameItemAdded: str = 'ItemAdded'
EvNameUpdateSatanicZone: str = 'UpdateSatanicZone'

EvKeyName: str = 'name'
EvKeyValue: str = 'value'


EvValues: dict[str, Callable] = {
    EvNameUpdateGold: lambda msg: GoldMessage(msg).currency_data,
    EvNameUpdateXP: lambda msg: XPMessage(msg).xp,
    EvNameUpdateMail: lambda msg: MailMessage(msg).new_mail,
    EvNameItemAdded: lambda msg: AddedItemMessage(msg).addedItemObject,
}
