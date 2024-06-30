from src.models.messages.added_item import AddedItemObject
from src.models.messages.gold import CurrencyData
from src.models.messages.satanic_zone import SzInfo


class BaseEvent:
    name: str
    value: str | int | CurrencyData | AddedItemObject | SzInfo

    def __str__(self):
        return f"Event: {self.name} = {self.value}"
