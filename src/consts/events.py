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
EvNameUpdateAccount: str = 'UpdateAccount'

EvKeyName: str = 'name'
EvKeyValue: str = 'value'
