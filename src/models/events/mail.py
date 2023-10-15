from src.models.messages.mail import MailMessage
from src.models.events.base import BaseEvent

from src.consts import events as consts


class MailEvent(BaseEvent):
    value: int

    def __init__(self, mail_message: MailMessage):
        self.name = consts.EvNameUpdateXP
        self.value = mail_message.new_mail

    @staticmethod
    def cast(model):
        if isinstance(model, MailEvent):
            return model
        else:
            raise Exception("Invalid model")
