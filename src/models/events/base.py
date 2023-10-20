from src.models.messages.added_item import AddedItemObject
from src.models.messages.gold import CurrencyData


class BaseEvent:
    name: str
    value: str | int | CurrencyData | AddedItemObject

    def __str__(self):
        return f"Event: {self.name} = {self.value}"
