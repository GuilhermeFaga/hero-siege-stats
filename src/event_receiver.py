import abc

from consts import events as consts


class EventReceiver(abc.ABC):
    def receive(self, event):
        event_name: str = event[consts.EvKeyName]
        value: dict = event[consts.EvKeyValue]

        self.on_event(event_name, value)

    @abc.abstractmethod
    def on_event(self, name: str, value: dict):
        pass


# class FameEventReceiver(EventReceiver):

#     def on_event(self, event_name: str, value: dict):
#         if event_name == consts.EvNameUpdateFame:
#             self.on_fame_update(value[consts.EvKeyValue])

#     @abc.abstractmethod
#     def on_fame_update(self, value: float):
#         pass
