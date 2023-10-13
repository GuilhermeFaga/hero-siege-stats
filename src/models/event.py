from src.models.messages.added_item import addedItemObject
from src.models.messages.gold import CurrencyData

from src.consts import events as consts


class Event:
    data: dict[str, str | int | CurrencyData | addedItemObject]

    def __init__(self, event_name, event_value: str | int | CurrencyData | addedItemObject):
        self.data = {
            consts.EvKeyName: event_name,
            consts.EvKeyValue: event_value
        }

    def __str__(self):
        return f"Event: {self.data[consts.EvKeyName]} = {self.data[consts.EvKeyValue]}"
