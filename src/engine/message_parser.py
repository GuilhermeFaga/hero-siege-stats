import json
import re

from src.consts import events as consts
from src.models.event import Event


class MessageParser:

    @staticmethod
    def capture(message):
        match = re.search("{.+}", str(message))

        if match is None:
            return None

        msg = match.group(0)
        try:
            parsed = json.loads(msg)
            # print("MessageParser.capture:", parsed)
            return parsed
        except:
            pass

    @staticmethod
    def message_to_event(msg_dict: dict):
        event_name = MessageParser.identify_event(msg_dict)

        if event_name is None or msg_dict is None:
            return None

        return Event(event_name, consts.EvValues[event_name](msg_dict))

    @staticmethod
    def identify_event(msg_dict: dict):
        if 'currencyData' in msg_dict:
            return consts.EvNameUpdateGold
        elif 'totalGuildXp' in msg_dict:
            return consts.EvNameUpdateXP
        elif 'mail' in msg_dict.get('message', ''):
            return consts.EvNameUpdateMail
        elif 'addedItemObject' in msg_dict:
            return consts.EvNameItemAdded
        elif 'satanicZoneName' in msg_dict:
            return consts.EvNameUpdateSatanicZone
        else:
            return None

    @staticmethod
    def packet_to_event(packet):
        # print("MessageParser.packet_to_event:", packet.load)
        msg = MessageParser.capture(packet.load)

        if msg is None:
            return None

        return MessageParser.message_to_event(msg)
