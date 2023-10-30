from src.models.events.base import BaseEvent
from src.consts import events as consts


class ItemDropEvent(BaseEvent):
    def __init__(self, msg_dict: dict):
        self.name = consts.EvNameItemDrop
        self.value = msg_dict.get("addedFingerprint", "")
        self.log_item()

    def log_item(self) -> None:
        # Log item drop
        with open("./dropped-items.txt", "a") as file:
            file.write(self.value + "\n")
