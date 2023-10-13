
class BaseMessage:
    status: str
    message: str

    def __init__(self, msg_dict: dict):
        self.status = msg_dict.get('status', '')
        self.message = msg_dict.get('message', '')
