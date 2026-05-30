import pytest

from src.consts import events as consts
from src.engine.message_parser import MessageParser
from src.models.events.account import AccountEvent
from src.models.events.added_item import AddedItemEvent
from src.models.events.gold import GoldEvent
from src.models.events.mail import MailEvent
from src.models.events.satanic_zone import SatanicZoneEvent
from src.models.events.xp import XPEvent


@pytest.mark.parametrize(
    ("message_fixture", "expected_event_type", "expected_event_name"),
    [
        ("gold_message_factory", GoldEvent, consts.EvNameUpdateGold),
        ("xp_message_factory", XPEvent, consts.EvNameUpdateXP),
        ("mail_message_factory", MailEvent, consts.EvNameUpdateMail),
        ("added_item_message_factory", AddedItemEvent, consts.EvNameItemAdded),
        (
            "satanic_zone_message_factory",
            SatanicZoneEvent,
            consts.EvNameUpdateSatanicZone,
        ),
        ("account_message_factory", AccountEvent, consts.EvNameUpdateAccount),
    ],
)
def test_message_to_event_creates_expected_events(
    request,
    message_fixture,
    expected_event_type,
    expected_event_name,
):
    message = request.getfixturevalue(message_fixture)()

    events = MessageParser.message_to_event([message])

    assert len(events) == 1
    assert isinstance(events[0], expected_event_type)
    assert events[0].name == expected_event_name


def test_message_to_event_supports_currency_data_snake_case(gold_message_factory):
    events = MessageParser.message_to_event([gold_message_factory(key="currency_data")])

    assert len(events) == 1
    assert isinstance(events[0], GoldEvent)


def test_message_to_event_skips_unknown_and_non_dict_messages(xp_message_factory):
    events = MessageParser.message_to_event(
        [
            "not a dict",
            {"unrecognized": True},
            xp_message_factory(message="Gained 42 xp"),
        ]
    )

    assert len(events) == 1
    assert isinstance(events[0], XPEvent)
    assert events[0].value == 42


@pytest.mark.parametrize(
    ("message", "expected_name"),
    [
        ({"currencyData": {}}, consts.EvNameUpdateGold),
        ({"currency_data": {}}, consts.EvNameUpdateGold),
        ({"totalGuildXp": 1}, consts.EvNameUpdateXP),
        ({"message": "new mail"}, consts.EvNameUpdateMail),
        ({"addedItemObject": {}}, consts.EvNameItemAdded),
        ({"satanicZoneName": "sz_1_1"}, consts.EvNameUpdateSatanicZone),
        ({"experience": 1}, consts.EvNameUpdateAccount),
    ],
)
def test_identify_event_returns_expected_event_name(message, expected_name):
    assert MessageParser.identify_event(message) == expected_name


@pytest.mark.parametrize("message", [None, "not a dict", {"steam": "id"}, {}])
def test_identify_event_returns_none_for_ignored_messages(message):
    assert MessageParser.identify_event(message) is None
