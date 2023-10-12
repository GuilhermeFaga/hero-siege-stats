import abc

from src.consts import events as consts


class EventReceiver(abc.ABC):
    def receive(self, event):
        event_name: str = event[consts.EvKeyName]
        value: dict = event[consts.EvKeyValue]

        self.on_event(event_name, value)

    @abc.abstractmethod
    def on_event(self, name: str, value: dict):
        pass
