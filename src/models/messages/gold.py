from datetime import datetime

from src.models.messages.base import BaseMessage, get_message_field, int_message_field

class CurrencyData:
    account_id: int
    timestamp: str
    gold : int
    GSS: int
    GSH: int
    GNS: int
    GNH: int
    GBP: int

    def __init__(self, currencyData: dict):
        self.account_id = int_message_field(currencyData, 'account_id', 'accountId')
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.GSS = int_message_field(currencyData, 'GSS', 'gss')
        self.GSH = int_message_field(currencyData, 'GSH', 'gsh')
        self.GNS = int_message_field(currencyData, 'GNS', 'gns')
        self.GNH = int_message_field(currencyData, 'GNH', 'gnh')
        self.GBP = int_message_field(currencyData, 'GBP', 'gbp')

    def get_gold_for_mode(self, season_mode: str) -> int:
        mode_map = {
            "GSS": self.GSS,
            "GSH": self.GSH,
            "GNS": self.GNS,
            "GNH": self.GNH,
            "GBP": self.GBP
        }
        return mode_map.get(season_mode, 0)


class GoldMessage(BaseMessage):
    currencyData: CurrencyData

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        currency_data = get_message_field(
            msg_dict,
            'currencyData',
            'currency_data',
            default={},
        )
        self.currencyData = CurrencyData(currency_data)
