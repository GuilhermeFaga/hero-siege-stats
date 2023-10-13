from datetime import datetime

from src.models.messages.base import BaseMessage


class CurrencyData:
    account_id: int
    timestamp: str
    gold: int
    GSH: int
    GNS: int
    GNH: int

    def __init__(self, currencyData: dict):
        self.account_id = currencyData['account_id']
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.gold = currencyData['GSS']
        self.GSH = currencyData['GSH']
        self.GNS = currencyData['GNS']
        self.GNH = currencyData['GNH']

    @staticmethod
    def cast(model):
        if isinstance(model, CurrencyData):
            return model
        else:
            raise Exception("Invalid model")


class GoldMessage(BaseMessage):
    currency_data: CurrencyData

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.currency_data = CurrencyData(msg_dict['currencyData'])
