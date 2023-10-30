import os

from src.models.messages.added_item import AddedItemMessage, AddedItemObject
from src.models.events.base import BaseEvent

from src.consts import events as consts


class AddedItemEvent(BaseEvent):
    value: AddedItemObject
    addedItemFingerprint: str = ""

    def __init__(self, added_item_message: AddedItemMessage):
        self.name = consts.EvNameItemAdded
        self.value = added_item_message.addedItemObject
        self.addedItemFingerprint = added_item_message.addedItemFingerprint

        self.update_log()

    def update_log(self) -> None:
        lines: list[str] = []
        # Append log containing zone name, difficulty, item name, stats, rarity
        if os.path.exists("./session.txt"):

            with open("./session.txt", "r") as file:
                lines = file.readlines()

            with open("./session.txt", "w") as file:
                for line in lines:
                    if self.addedItemFingerprint not in line:
                        file.write(line)
                        continue

                    with open("./item-drops", "a") as drops:
                        drops.write("Picked up: %s %s" % (self.addedItemFingerprint, "\n"))
