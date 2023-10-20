
class Account:
    account_id: str = ""

    def __init__(self):
        pass

    def update(self, account_id=None):
        if account_id is not None:
            self.account_id = account_id
