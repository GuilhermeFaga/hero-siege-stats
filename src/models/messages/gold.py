from datetime import datetime


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


class GoldMessage:
    status: str
    message: str
    currency_data: CurrencyData

    def __init__(self, msg_dict: dict):
        self.status = msg_dict['status']
        self.message = msg_dict['message']
        self.currency_data = CurrencyData(msg_dict['currencyData'])
