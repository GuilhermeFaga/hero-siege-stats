from datetime import datetime, timedelta

from src.models.messages.added_item import AddedItemObject
from src.models.messages.gold import CurrencyData
from src.models.stats.added_items import AddedItemsStats
from src.models.stats.gold import GoldStats
from src.models.stats.session import Session
from src.models.stats.xp import XPStats


def test_gold_stats_initial_total_does_not_count_as_earned(currency_data_factory):
    stats = GoldStats()

    stats.update(CurrencyData(currency_data_factory(GSS=100)), season_mode="GSS")

    assert stats.total_gold == 100
    assert stats.total_gold_earned == 0


def test_gold_stats_counts_positive_diffs_only(currency_data_factory):
    stats = GoldStats(total_gold=100)

    stats.update(CurrencyData(currency_data_factory(GSS=125)), season_mode="GSS")
    stats.update(CurrencyData(currency_data_factory(GSS=75)), season_mode="GSS")

    assert stats.total_gold == 75
    assert stats.total_gold_earned == 25


def test_xp_stats_counts_positive_diffs_only():
    stats = XPStats(total_xp=100)

    stats.update(total_xp=150)
    stats.update(total_xp=90)

    assert stats.total_xp == 90
    assert stats.total_xp_earned == 50


def test_xp_stats_add_scales_packet_xp():
    stats = XPStats()

    stats.add(15)

    assert stats.total_xp == 100
    assert stats.total_xp_earned == 100


def test_session_calculates_value_per_hour():
    session = Session()
    session.start_time = datetime.now() - timedelta(minutes=30)

    assert session.calculate_value_per_hour(50) == 100


def test_added_items_stats_updates_total_and_magic_find(added_item_object_factory):
    stats = AddedItemsStats()

    stats.update(AddedItemObject(added_item_object_factory(rarity=6, mf_drop=1)))

    assert stats.added_items["Satanic"] == {"total": 1, "mf": 1}


def test_added_items_stats_instances_do_not_share_counts(added_item_object_factory):
    first = AddedItemsStats()
    second = AddedItemsStats()

    first.update(AddedItemObject(added_item_object_factory(rarity=7)))

    assert first.added_items["Angelic"]["total"] == 1
    assert second.added_items["Angelic"]["total"] == 0
