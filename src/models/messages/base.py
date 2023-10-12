
class BaseMessage:
    status: str
    message: str

    def __init__(self, msg_dict: dict):
        self.status = msg_dict['status']
        self.message = msg_dict['message']
