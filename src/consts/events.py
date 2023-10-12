from models.messages.gold import GoldMessage
from models.messages.xp import XPMessage
from models.messages.mail import MailMessage
from models.messages.added_item import AddedItemMessage
from models.messages.satanic_zone import SatanicZoneMessage


EvNameUpdateGold: str = 'UpdateGold'
EvNameUpdateXP: str = 'UpdateXP'
EvNameUpdateMail: str = 'UpdateMail'
EvNameItemAdded: str = 'ItemAdded'
EvNameUpdateSatanicZone: str = 'UpdateSatanicZone'

EvKeyName: str = 'name'
EvKeyValue: str = 'value'


EvValues: dict = {
    EvNameUpdateGold: lambda msg: GoldMessage(msg).currency_data,
    EvNameUpdateXP: lambda msg: XPMessage(msg).xp,
    EvNameUpdateMail: lambda msg: MailMessage(msg).new_mail,
    EvNameItemAdded: lambda msg: AddedItemMessage(msg).addedItemObject,
}
