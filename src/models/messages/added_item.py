from src.models.messages.base import BaseMessage


class addedItemObject:
    seed: int
    id: int
    token_level: int
    identified: int | None
    type: int
    timestamp: str
    drop_quality: int
    rarity: int
    token: int
    tier: int
    amount: int
    weapon_type: int
    market_id: int
    mf_drop: int
    socket_1: int | None
    socket_2: int | None
    socket_3: int | None
    socket_4: int | None
    socket_5: int | None
    socket_6: int | None
    sockets: int
    account: str

    def __init__(self, addedItemObject: dict):
        self.seed = addedItemObject['seed']
        self.id = addedItemObject['id']
        self.token_level = addedItemObject['token_level']
        self.identified = addedItemObject.get('identified', None)
        self.type = addedItemObject['type']
        self.timestamp = addedItemObject['timestamp']
        self.drop_quality = addedItemObject['drop_quality']
        self.rarity = addedItemObject['rarity']
        self.token = addedItemObject['token']
        self.tier = addedItemObject['tier']
        self.amount = addedItemObject['amount']
        self.weapon_type = addedItemObject['weapon_type']
        self.market_id = addedItemObject['market_id']
        self.mf_drop = addedItemObject['mf_drop']
        self.socket_1 = addedItemObject.get('socket_1', None)
        self.socket_2 = addedItemObject.get('socket_2', None)
        self.socket_3 = addedItemObject.get('socket_3', None)
        self.socket_4 = addedItemObject.get('socket_4', None)
        self.socket_5 = addedItemObject.get('socket_5', None)
        self.socket_6 = addedItemObject.get('socket_6', None)
        self.sockets = len([socket for socket in [self.socket_1, self.socket_2,
                           self.socket_3, self.socket_4, self.socket_5, self.socket_6] if socket is not None])
        self.account = addedItemObject['account']


class AddedItemMessage(BaseMessage):
    addedItemFingerprint: str

    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        self.addedItemFingerprint = msg_dict['addedItemFingerprint']
        self.addedItemObject = addedItemObject(msg_dict['addedItemObject'])
