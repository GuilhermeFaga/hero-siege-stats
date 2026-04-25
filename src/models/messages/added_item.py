from src.models.messages.base import (
    BaseMessage,
    get_message_field,
    int_message_field,
)


def _extract_inventory_add_items(msg_dict: dict) -> list[tuple[str | None, dict]]:
    operations = get_message_field(msg_dict, 'operations', default={})
    added_items = get_message_field(operations, 'add', default=None)
    if not isinstance(added_items, dict):
        return []

    return [
        (fingerprint, item_data)
        for fingerprint, item_data in added_items.items()
        if isinstance(item_data, dict)
    ]


class AddedItemObject:
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
        self.seed = int_message_field(addedItemObject, 'seed', 'a')
        self.id = int_message_field(
            addedItemObject, 'id', 'itemId', 'item_id', 'gid'
        )
        self.token_level = int_message_field(
            addedItemObject, 'token_level', 'tokenLevel', 'e'
        )
        self.identified = get_message_field(addedItemObject, 'identified', default=None)
        self.type = int_message_field(
            addedItemObject, 'type', 'itemType', 'item_type', 'b'
        )
        self.timestamp = get_message_field(addedItemObject, 'timestamp', default='')
        self.drop_quality = int_message_field(
            addedItemObject, 'drop_quality', 'dropQuality', 'j'
        )
        self.rarity = get_message_field(
            addedItemObject, 'rarity', 'itemRarity', 'item_rarity', 'd', default=0
        )
        self.token = int_message_field(addedItemObject, 'token')
        self.tier = int_message_field(addedItemObject, 'tier', 'n')
        self.amount = int_message_field(addedItemObject, 'amount', default=1)
        self.weapon_type = int_message_field(
            addedItemObject, 'weapon_type', 'weaponType'
        )
        self.market_id = int_message_field(addedItemObject, 'market_id', 'marketId')
        self.mf_drop = int_message_field(
            addedItemObject,
            'mf_drop',
            'mfDrop',
            'm',
        )
        self.socket_1 = get_message_field(addedItemObject, 'socket_1', default=None)
        self.socket_2 = get_message_field(addedItemObject, 'socket_2', default=None)
        self.socket_3 = get_message_field(addedItemObject, 'socket_3', default=None)
        self.socket_4 = get_message_field(addedItemObject, 'socket_4', default=None)
        self.socket_5 = get_message_field(addedItemObject, 'socket_5', default=None)
        self.socket_6 = get_message_field(addedItemObject, 'socket_6', default=None)
        self.sockets = len(
            [
                socket
                for socket in [
                    self.socket_1,
                    self.socket_2,
                    self.socket_3,
                    self.socket_4,
                    self.socket_5,
                    self.socket_6,
                ]
                if socket is not None
            ]
        )
        self.account = get_message_field(
            addedItemObject, 'account', 'accountId', 'account_id', default=''
        )


class AddedItemMessage(BaseMessage):
    addedItemFingerprint: str | None

    @staticmethod
    def from_msg_dict(msg_dict: dict) -> list["AddedItemMessage"]:
        inventory_add_items = _extract_inventory_add_items(msg_dict)
        if inventory_add_items:
            return [
                AddedItemMessage(
                    msg_dict, item_object=item_object, fingerprint=fingerprint
                )
                for fingerprint, item_object in inventory_add_items
            ]

        return [AddedItemMessage(msg_dict)]

    def __init__(
        self,
        msg_dict: dict,
        item_object: dict | None = None,
        fingerprint: str | None = None,
    ):
        super().__init__(msg_dict)
        self.addedItemFingerprint = fingerprint or get_message_field(
            msg_dict,
            'addedItemFingerprint',
            'added_item_fingerprint',
            'fingerprint',
            default=None,
        )
        added_item_object = item_object or get_message_field(
            msg_dict,
            'addedItemObject',
            'added_item_object',
            default=msg_dict,
        )
        self.addedItemObject = AddedItemObject(added_item_object)
