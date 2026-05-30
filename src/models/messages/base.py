import json
import re


_MISSING = object()


def _normalize_message_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(key).lower())


def _coerce_message_value(value):
    if not isinstance(value, str):
        return value

    stripped_value = value.strip()
    if not stripped_value or stripped_value[0] not in "[{":
        return value

    try:
        return json.loads(stripped_value)
    except json.JSONDecodeError:
        return value


def get_message_field(msg_dict: dict | None, *names: str, default=None):
    if not isinstance(msg_dict, dict):
        return default

    for name in names:
        if name in msg_dict:
            return _coerce_message_value(msg_dict[name])

    normalized_names = {_normalize_message_key(name) for name in names}
    for key, value in msg_dict.items():
        if _normalize_message_key(key) in normalized_names:
            return _coerce_message_value(value)

    return default


def has_message_field(msg_dict: dict | None, *names: str) -> bool:
    return get_message_field(msg_dict, *names, default=_MISSING) is not _MISSING


def int_message_field(msg_dict: dict | None, *names: str, default: int = 0) -> int:
    value = get_message_field(msg_dict, *names, default=default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class BaseMessage:
    status: str
    message: str

    def __init__(self, msg_dict: dict):
        self.status = get_message_field(msg_dict, 'status', default='')
        self.message = get_message_field(msg_dict, 'message', default='')
