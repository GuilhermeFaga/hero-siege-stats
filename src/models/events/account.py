from src.models.messages.account import AccountMessage
from src.models.events.base import BaseEvent

from src.consts import events as consts


class AccountEvent(BaseEvent):
    value: AccountMessage

    def __init__(self, account_message: AccountMessage):
        self.name = consts.EvNameUpdateAccount
        self.value = account_message

    @staticmethod
    def cast(model):
        if isinstance(model, AccountEvent):
            return model
        else:
            raise Exception("Invalid model")
