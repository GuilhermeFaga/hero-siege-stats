import json
import re

from scapy.all import Packet
from scapy.layers.inet import IP
from scapy.layers.inet import TCP

from src.models.events.gold import GoldEvent
from src.models.events.xp import XPEvent
from src.models.events.account import AccountEvent
from src.models.events.mail import MailEvent
from src.models.events.added_item import AddedItemEvent
from src.models.events.drop import ItemDropEvent

from src.models.messages.gold import GoldMessage
from src.models.messages.xp import XPMessage
from src.models.messages.account import AccountMessage
from src.models.messages.mail import MailMessage
from src.models.messages.added_item import AddedItemMessage

from src.consts import events as consts
from src.consts.enums import ItemSources


_continuos_packets: dict[str, list[str]] = {}
_last_src_ack: dict[str, str] = {}


class MessageParser:

    @staticmethod
    def capture(message):
        match = re.search("{.+}", str(message))

        if match is None:
            return None

        msg = match.group(0)

        # Log messages to file
        with open("./messages.txt", "a") as file:
            file.write(msg + "\n")

        try:
            parsed = json.loads(msg)
            # print("MessageParser.capture:", parsed)
            return parsed
        except:
            # print("MessageParser.capture.except:", msg)
            pass

    @staticmethod
    def message_to_event(msg_dict: dict):
        event_name = MessageParser.identify_event(msg_dict)

        if event_name is None or msg_dict is None:
            return None

        if event_name == consts.EvNameUpdateGold:
            return GoldEvent(GoldMessage(msg_dict))
        if event_name == consts.EvNameUpdateXP:
            return XPEvent(XPMessage(msg_dict))
        if event_name == consts.EvNameUpdateAccount:
            return AccountEvent(AccountMessage(msg_dict))
        if event_name == consts.EvNameUpdateMail:
            return MailEvent(MailMessage(msg_dict))
        if event_name == consts.EvNameItemAdded:
            return AddedItemEvent(AddedItemMessage(msg_dict))
        if event_name == consts.EvNameItemDrop:
            return ItemDropEvent(msg_dict)

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
        elif 'name' in msg_dict:
            return consts.EvNameUpdateAccount
        elif msg_dict.get("message") == ItemSources.NEW_ITEM.value:
            return consts.EvNameItemDrop
        else:
            return None

    @staticmethod
    def packet_to_event(packet: Packet):

        if IP not in packet:
            return None

        if TCP not in packet:
            return None

        try:
            packet.load
        except:
            return None

        msg: dict = {}
        packet_src = str(packet[IP].src)
        packet_key = str(packet[TCP].ack)

        if _last_src_ack.get(packet_src, None) is None:
            _last_src_ack[packet_src] = packet_key

        if _continuos_packets.get(packet_key, None) is None:
            _continuos_packets[packet_key] = []

        _continuos_packets[packet_key].append(str(packet.load))

        if packet_key != _last_src_ack[packet_src]:
            load = "".join(_continuos_packets[_last_src_ack[packet_src]])
            # print("MessageParser.packet_to_event:", load)
            load = load.replace("'b'", '')
            for possible_msg in load.split("\\"):
                msg = MessageParser.capture(possible_msg)
                if msg is not None:
                    break
            del _continuos_packets[_last_src_ack[packet_src]]

        _last_src_ack[packet_src] = packet_key

        if msg is None:
            return None

        # Check if player has obtained an item
        if msg.get("addedItemObject") is not None:
            # Do not generate item event if item not picked up from ground
            if msg.get("message") != ItemSources.FROM_GROUND:
                return None

        return MessageParser.message_to_event(msg)
