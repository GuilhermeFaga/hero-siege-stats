import pytest

from src.consts.season import CURRENT_SEASON
from src.models.messages.account import AccountMessage
from src.models.messages.added_item import AddedItemObject
from src.models.messages.gold import CurrencyData
from src.models.messages.mail import MailMessage
from src.models.messages.satanic_zone import SatanicZoneMessage
from src.models.messages.xp import XPMessage


@pytest.mark.parametrize(
    ("message", "expected_xp"),
    [("Guild gained 150 xp", 150), ("No number here", 0)],
)
def test_xp_message_extracts_first_integer(message, expected_xp):
    xp_message = XPMessage({"message": message, "totalGuildXp": 10})

    assert xp_message.xp == expected_xp


def test_currency_data_returns_gold_for_requested_mode(currency_data_factory):
    currency_data = CurrencyData(currency_data_factory(GSS=11, GSH=22))

    assert currency_data.get_gold_for_mode("GSS") == 11
    assert currency_data.get_gold_for_mode("GSH") == 22
    assert currency_data.get_gold_for_mode("unknown") is None


@pytest.mark.parametrize(
    ("season", "hardcore", "blood_pact", "expected_mode"),
    [
        (CURRENT_SEASON, 0, 0, "GSS"),
        (CURRENT_SEASON, 1, 0, "GSH"),
        (0, 0, 0, "GNS"),
        (0, 1, 0, "GNH"),
        (0, 0, 1, "GBP"),
    ],
)
def test_account_message_returns_current_season_mode(
    account_message_factory,
    season,
    hardcore,
    blood_pact,
    expected_mode,
):
    account_message = AccountMessage(
        account_message_factory(
            season=season,
            hardcore=hardcore,
            blood_pact=blood_pact,
        )
    )

    assert account_message.get_current_season_mode() == expected_mode


def test_added_item_object_counts_present_sockets(added_item_object_factory):
    item = AddedItemObject(added_item_object_factory(sockets=[10, 20, 30]))

    assert item.sockets == 3


@pytest.mark.parametrize(
    ("message", "expected_new_mail"),
    [("No new mail", 0), ("You have new mail", 1)],
)
def test_mail_message_identifies_new_mail(message, expected_new_mail):
    mail_message = MailMessage({"message": message})

    assert mail_message.new_mail == expected_new_mail


def test_satanic_zone_message_parses_zone_and_buffs(satanic_zone_message_factory):
    message = SatanicZoneMessage(
        satanic_zone_message_factory(zone="sz_1_1", buffs="1|2")
    )

    assert message.satanic_info.satanic_zone == "Act 1 : Outskirts of Inoya"
    assert [buff.buff_name for buff in message.satanic_info.buffs] == [
        "Loot Goblin I",
        "Loot Goblin II",
    ]
