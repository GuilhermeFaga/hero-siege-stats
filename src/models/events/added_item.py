from src.models.messages.added_item import AddedItemMessage, AddedItemObject
from src.models.events.base import BaseEvent

from src.consts import events as consts


class AddedItemEvent(BaseEvent):
    value: AddedItemObject

    def __init__(self, added_item_message: AddedItemMessage):
        self.name = consts.EvNameItemAdded
        self.value = added_item_message.addedItemObject
