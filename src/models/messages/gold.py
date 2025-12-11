from datetime import datetime

from src.models.messages.base import BaseMessage

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
        self.account_id = currencyData.get('account_id', 0)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.GSS = currencyData['GSS']
        self.GSH = currencyData['GSH']
        self.GNS = currencyData['GNS']
        self.GNH = currencyData['GNH']
        self.GBP = currencyData['GBP']

    def get_gold_for_mode(self, season_mode: str) -> int:
        mode_map = {
            "GSS": self.GSS,
            "GSH": self.GSH,
            "GNS": self.GNS,
            "GNH": self.GNH,
            "GBP": self.GBP
        }
        return mode_map.get(season_mode, None)


class GoldMessage(BaseMessage):
    currencyData: CurrencyData

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        if 'currencyData' in msg_dict:
            self.currencyData = CurrencyData(msg_dict['currencyData'])
        elif 'currency_data' in msg_dict:
            self.currencyData = CurrencyData(msg_dict['currency_data'])
