from src.models.messages.gold import CurrencyData, GoldMessage
from src.models.events.base import BaseEvent

from src.consts import events as consts


class GoldEvent(BaseEvent):
    value: CurrencyData

    def __init__(self, gold_message: GoldMessage):
        self.name = consts.EvNameUpdateGold
        self.value = gold_message.currencyData
