from src.models.messages.base import BaseMessage


class MailMessage(BaseMessage):
    new_mail: int

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.new_mail = 0 if self.message == 'No new mail' else 1
