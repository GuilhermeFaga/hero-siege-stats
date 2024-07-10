import json
import logging
import re

from scapy.all import Packet
from scapy.layers.inet import IP
from scapy.layers.inet import TCP

from src.consts.logger import LOGGING_NAME
from src.models.events.base import BaseEvent
from src.models.events.gold import GoldEvent
from src.models.events.xp import XPEvent
from src.models.events.account import AccountEvent
from src.models.events.mail import MailEvent
from src.models.events.added_item import AddedItemEvent
from src.models.events.satanic_zone import SatanicZoneEvent

from src.models.messages.gold import GoldMessage
from src.models.messages.xp import XPMessage
from src.models.messages.account import AccountMessage
from src.models.messages.mail import MailMessage
from src.models.messages.added_item import AddedItemMessage
from src.models.messages.satanic_zone import SatanicZoneMessage

from src.consts import events as consts


_continuos_packets: dict[str, list[str]] = {}
_last_src_ack: dict[str, str] = {}


class MessageParser:
    @staticmethod
    def capture(message)-> list | None:
        logger = logging.getLogger(LOGGING_NAME)
        match = re.search("{.+}", str(message))
        if match is None:
            return None
        msg = match.group(0)
        try:
            parsed = json.loads(msg)
            #logger.log(logging.DEBUG,f"MessageParser.capture: {parsed}")
            return parsed
        except json.JSONDecodeError:
            #logger.log(logging.DEBUG,f"MessageParser.capture.except: {msg}")
            return None


    @staticmethod
    def message_to_event(msg_list: list):
        if msg_list is None:
            return None
        events : list[BaseEvent] = []        
        for msg_dict in msg_list:
            event_name = MessageParser.identify_event(msg_dict)
            if event_name is None:
                continue
            if event_name == consts.EvNameUpdateGold:
                events.append(GoldEvent(GoldMessage(msg_dict)))
            if event_name == consts.EvNameUpdateXP:
                events.append(XPEvent(XPMessage(msg_dict)))
            if event_name == consts.EvNameUpdateAccount:
                events.append(AccountEvent(AccountMessage(msg_dict)))
            if event_name == consts.EvNameUpdateMail:
                events.append(MailEvent(MailMessage(msg_dict)))
            if event_name == consts.EvNameItemAdded:
                events.append(AddedItemEvent(AddedItemMessage(msg_dict)))
            if event_name == consts.EvNameUpdateSatanicZone:
                events.append(SatanicZoneEvent(SatanicZoneMessage(msg_dict)))
        return events
    @staticmethod
    def identify_event(msg_dict: dict):
        if 'steam' in msg_dict:
            return None

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
        else:
            return None

    @staticmethod
    def packet_to_event(packet: Packet):
        logger = logging.getLogger(LOGGING_NAME)
        if IP not in packet:
            return None

        if TCP not in packet:
            return None

        try:
            packet.load
        except:
            return None

        msg_list = None
        result_messages: list = []
        packet_src = str(packet[IP].src)
        packet_key = str(packet[TCP].ack)

        if _last_src_ack.get(packet_src, None) is None:
            _last_src_ack[packet_src] = packet_key

        if _continuos_packets.get(packet_key, None) is None:
            _continuos_packets[packet_key] = []

        _continuos_packets[packet_key].append(str(packet.load))

        if packet_key != _last_src_ack[packet_src]:
            load = "".join(_continuos_packets[_last_src_ack[packet_src]])
            #logger.log(logging.DEBUG,f"MessageParser.packet_to_event: {load}")
            load = load.replace("'b'", '')
            for possible_msg in load.split("\\"):
                msg_list = MessageParser.capture(possible_msg)
                if msg_list is not None:
                    result_messages.append(msg_list) 
            del _continuos_packets[_last_src_ack[packet_src]]

        _last_src_ack[packet_src] = packet_key

        if result_messages is None or not result_messages :
            return None
        return MessageParser.message_to_event(result_messages)
