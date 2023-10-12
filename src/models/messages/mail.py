
class MailMessage:
    status: str
    message: str
    new_mail: int

    def __init__(self, msg_dict: dict):
        self.status = msg_dict['status']
        self.message = msg_dict['message']
        self.new_mail = 0 if self.message == 'No new mail' else 1
