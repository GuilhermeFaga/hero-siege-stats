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
from src.models.messages.base import get_message_field, has_message_field
from src.models.messages.satanic_zone import SatanicZoneMessage

from src.consts import events as consts
from src.engine.backend import PROTOCOL_SIGNATURES


_continuos_packets: dict[str, list[str]] = {}
_last_src_ack: dict[str, str] = {}

GOLD_FIELDS = ("currencyData", "currency_data")
XP_TOTAL_FIELDS = (
    "totalGuildXp",
    "total_guild_xp",
    "totalGuildExp",
    "total_guild_exp",
)
XP_GAIN_FIELDS = ("xp", "experienceGained", "experience_gained")
MAIL_FIELDS = ("newMail", "new_mail", "mail")
ITEM_WRAPPER_FIELDS = (
    "addedItemObject",
    "added_item_object",
)
ITEM_SIGNATURE_FIELDS = (
    "seed",
    "a",
    "itemId",
    "item_id",
    "gid",
)
ITEM_RARITY_FIELDS = ("rarity", "itemRarity", "item_rarity", "d")
SATANIC_ZONE_FIELDS = (
    "satanicZoneName",
    "satanic_zone_name",
)
ACCOUNT_SIGNATURE_FIELDS = (
    "name",
    "class",
    "class_id",
    "heroLevel",
    "herolevel",
    "season",
    "hardcore",
)


class MessageParser:
    @staticmethod
    def _iter_message_dicts(value):
        if isinstance(value, dict):
            yield value
            return

        if isinstance(value, list):
            for item in value:
                yield from MessageParser._iter_message_dicts(item)

    @staticmethod
    def _is_item_payload(msg_dict: dict) -> bool:
        operations = get_message_field(msg_dict, "operations", default={})
        return (
            has_message_field(msg_dict, *ITEM_WRAPPER_FIELDS)
            or (
                has_message_field(msg_dict, *ITEM_RARITY_FIELDS)
                and has_message_field(msg_dict, *ITEM_SIGNATURE_FIELDS)
            )
            or has_message_field(operations, "add")
        )

    @staticmethod
    def capture(message, src, dst) -> list | None:
        """
        Capture and parse game protocol messages
        Args:
            message: Raw message content
            src: Source IP
            dst: Destination IP
        Returns:
            Parsed message or None if invalid
        """
        logger = logging.getLogger(LOGGING_NAME)
        try:
            # Check for JSON format packets
            match = re.search(r"(\{.+\}|\[.+\])", str(message))
            if match is None:
                # Handle special format packets
                if len(message) <= 100:
                    return None

                # Validate special format packet header
                if message[0] != PROTOCOL_SIGNATURES["special_start"]:
                    return None

                # Skip first 3 characters as they are fixed prefix
                truncated_message = message[3:]
                result = None
                try:
                    import base64

                    # Reserved for future use
                    if "[INV]" in truncated_message:
                        jwt_token = truncated_message.split("[INV]")[1]
                        # Decode JWT Token
                        decoded = base64.b64decode(jwt_token)
                        result = json.loads(decoded)
                    elif "&" not in truncated_message:
                        # Decode JWT Token
                        decoded = base64.b64decode(truncated_message)
                        result = json.loads(decoded)
                    else:
                        # Parse URL query string format
                        from urllib.parse import parse_qs

                        parsed = parse_qs(truncated_message)
                        # Convert list values to single values
                        result = {k: v[0] for k, v in parsed.items()}
                    # logger.debug(f"MessageParser.capture: {result} from {src} to {dst}")
                    return result
                except Exception as e:
                    logger.debug(f"Message parsing failed: {e}")
                    return None

            # Process JSON format packets
            msg = match.group(0)
            try:
                parsed = json.loads(msg)
                # Filter out excluded packet types
                if any(key in parsed for key in PROTOCOL_SIGNATURES["excluded_keys"]):
                    return None
                return parsed
            except json.JSONDecodeError:
                return None
        except Exception as e:
            logger.error(f"Error in Capture function: {e}")
            return None

    @staticmethod
    def message_to_event(msg_list: list):
        logger = logging.getLogger(LOGGING_NAME)
        try:
            if msg_list is None:
                return None
            events: list[BaseEvent] = []
            for msg_dict in MessageParser._iter_message_dicts(msg_list):
                try:
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
                        events.extend(
                            AddedItemEvent(added_item_message)
                            for added_item_message in AddedItemMessage.from_msg_dict(
                                msg_dict
                            )
                        )
                    if event_name == consts.EvNameUpdateSatanicZone:
                        events.append(SatanicZoneEvent(SatanicZoneMessage(msg_dict)))
                except Exception as e:
                    logger.warning(f"Error processing single message: {e}")
                    continue
            return events
        except Exception as e:
            logger.error(f"Error converting message to event: {e}")
            return None

    @staticmethod
    def identify_event(msg_dict: dict):
        logger = logging.getLogger(LOGGING_NAME)
        try:
            # Skip non-dictionary messages (commonly from item list packets) to prevent type errors
            # Check if msg_dict is a dictionary type
            if not isinstance(msg_dict, dict):
                # logger.warning(f"msg_dict is not a dictionary, got {type(msg_dict)}, {msg_dict}")
                return None
            if "steam" in msg_dict:
                return None

            message = str(get_message_field(msg_dict, "message", default="")).lower()

            if has_message_field(msg_dict, *GOLD_FIELDS):
                return consts.EvNameUpdateGold
            elif has_message_field(msg_dict, *XP_TOTAL_FIELDS):
                return consts.EvNameUpdateXP
            elif "mail" in message or has_message_field(msg_dict, *MAIL_FIELDS):
                return consts.EvNameUpdateMail
            elif MessageParser._is_item_payload(msg_dict):
                return consts.EvNameItemAdded
            elif has_message_field(msg_dict, *SATANIC_ZONE_FIELDS):
                return consts.EvNameUpdateSatanicZone
            elif has_message_field(msg_dict, "experience") and has_message_field(
                msg_dict, *ACCOUNT_SIGNATURE_FIELDS
            ):
                return consts.EvNameUpdateAccount
            elif has_message_field(msg_dict, *XP_GAIN_FIELDS):
                return consts.EvNameUpdateXP
            else:
                return None
        except Exception as e:
            logger.error(f"Error identifying event type: {e}")
            return None

    @staticmethod
    def packet_to_event(packet: Packet):
        logger = logging.getLogger(LOGGING_NAME)
        try:
            if IP not in packet or TCP not in packet:
                return None

            try:
                packet.load
            except:
                return None

            msg_list = None
            result_messages: list = []
            packet_src = str(packet[IP].src)
            packet_key = str(packet[TCP].ack)

            try:
                if _last_src_ack.get(packet_src, None) is None:
                    _last_src_ack[packet_src] = packet_key

                if _continuos_packets.get(packet_key, None) is None:
                    _continuos_packets[packet_key] = []

                _continuos_packets[packet_key].append(str(packet.load))
                if packet_key != _last_src_ack[packet_src]:
                    old_key = _last_src_ack[packet_src]
                    if old_key in _continuos_packets:
                        load = "".join(_continuos_packets[_last_src_ack[packet_src]])

                        load = load.replace("'b'", "")
                        for possible_msg in load.split("\\"):
                            msg_list = MessageParser.capture(
                                possible_msg, packet_src, packet[IP].dst
                            )
                            if msg_list is not None:
                                result_messages.append(msg_list)
                        del _continuos_packets[_last_src_ack[packet_src]]
                    else:
                        logger.debug(f"Skipping missing packet buffer key: {old_key}")

                _last_src_ack[packet_src] = packet_key

            except Exception as e:
                logger.error(f"Error processing packet: {e}")
                return None

            if result_messages is None or not result_messages:
                return None
            return MessageParser.message_to_event(result_messages)
        except Exception as e:
            logger.error(f"Error converting packet to event: {e}")
            return None

    @staticmethod
    def reset_packet_buffers():
        global _continuos_packets, _last_src_ack
        _continuos_packets.clear()
        _last_src_ack.clear()
