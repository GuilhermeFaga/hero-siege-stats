import json

import pytest
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw

from src.consts.season import CURRENT_SEASON
from src.engine.message_parser import MessageParser


@pytest.fixture(autouse=True)
def reset_message_parser_buffers():
    MessageParser.reset_packet_buffers()
    yield
    MessageParser.reset_packet_buffers()


@pytest.fixture
def currency_data_factory():
    def factory(**overrides):
        data = {
            "account_id": 123,
            "GSS": 1000,
            "GSH": 2000,
            "GNS": 3000,
            "GNH": 4000,
            "GBP": 5000,
        }
        data.update(overrides)
        return data

    return factory


@pytest.fixture
def gold_message_factory(currency_data_factory):
    def factory(key="currencyData", **currency_overrides):
        return {key: currency_data_factory(**currency_overrides)}

    return factory


@pytest.fixture
def xp_message_factory():
    def factory(message="Guild gained 150 xp", total_guild_xp=10_000):
        return {"message": message, "totalGuildXp": total_guild_xp}

    return factory


@pytest.fixture
def mail_message_factory():
    def factory(message="You have new mail"):
        return {"message": message}

    return factory


@pytest.fixture
def added_item_object_factory():
    def factory(rarity=6, mf_drop=0, sockets=None, **overrides):
        data = {
            "seed": 1,
            "id": 100,
            "token_level": 0,
            "identified": 1,
            "type": 1,
            "timestamp": "2026-01-01 00:00:00",
            "drop_quality": 1,
            "rarity": rarity,
            "token": 0,
            "tier": 1,
            "amount": 1,
            "weapon_type": 0,
            "market_id": 0,
            "mf_drop": mf_drop,
            "account": "test-account",
        }
        for index in range(1, 7):
            data[f"socket_{index}"] = None
        if sockets is not None:
            for index, socket in enumerate(sockets, start=1):
                data[f"socket_{index}"] = socket
        data.update(overrides)
        return data

    return factory


@pytest.fixture
def added_item_message_factory(added_item_object_factory):
    def factory(**overrides):
        return {
            "addedItemFingerprint": "fingerprint",
            "addedItemObject": added_item_object_factory(**overrides),
        }

    return factory


@pytest.fixture
def account_message_factory():
    def factory(
        season=CURRENT_SEASON,
        hardcore=0,
        blood_pact=0,
        experience=10_000,
        **overrides,
    ):
        data = {
            "version": 1,
            "name": "TestHero",
            "class": 1,
            "level": 10,
            "experience": experience,
            "herolevel": 1,
            "talentMap_0": {},
            "talentMap_1": {},
            "talentMap_2": {},
            "talentMap_3": {},
            "subTalentMap_0": {},
            "subTalentMap_1": {},
            "subTalentMap_2": {},
            "subTalentMap_3": {},
            "aura": [],
            "loadout": 0,
            "talent_loadout": 0,
            "difficulty": 1,
            "level_max_damage": 0,
            "level_max_dps": 0,
            "damage_source": "",
            "bind_skill": [],
            "bind_skill2": [],
            "weapon_skin": [],
            "fortune_enemies": [],
            "potion_autofill": 0,
            "potion_useall": 0,
            "talent_reset": 0,
            "season_reward_wings": 0,
            "soloselffound": 0,
            "acts": [],
            "act_previous": [],
            "act_zones_1": [],
            "act_zones_2": [],
            "act_zones_3": [],
            "act_zones_4": [],
            "act_zones_5": [],
            "act_zones_6": [],
            "act_zones_7": [],
            "act_zones_8": [],
            "merc_alive": 0,
            "merc_type": 0,
            "merc_aura": 0,
            "merc_talents": [],
            "merc_hat": [],
            "merc_skin": [],
            "merc_name": [],
            "chaos_towers_cleared": 0,
            "wormhole_zone": [],
            "wormhole_levels": [],
            "fortune_item": [],
            "inventory_tab_name": [],
            "shield_skin": 0,
            "playstation_id": "",
            "attribute_points": [],
            "back_accessory": 0,
            "inventory_reset": 0,
            "hat": 0,
            "skin": 0,
            "hardcore": hardcore,
            "season": season,
            "season_reward_effect": 0,
            "season_reward_portal": 0,
            "incarnation_exp": 0,
            "title": 0,
            "companion": 0,
            "player_explosion": 0,
            "player_trail": 0,
            "heroboard": "",
            "grindfest_door_open": 0,
            "waypoints": {},
            "codex_data": "",
            "playtime": 0,
            "chaos_tower_boss_kills": 0,
            "chaos_tower_boss_kills_hash": "",
            "hell_subdifficulty": 0,
            "spell_chain_skin": 0,
            "spell_explo_skin": 0,
            "quest_chains": {},
            "blood_pact": blood_pact,
        }
        data.update(overrides)
        return data

    return factory


@pytest.fixture
def satanic_zone_message_factory():
    def factory(zone="sz_1_1", buffs="1|2|3"):
        return {"satanicZoneName": zone, "buffs": buffs}

    return factory


@pytest.fixture
def json_payload_factory():
    def factory(message):
        return json.dumps(message, separators=(",", ":"))

    return factory


@pytest.fixture
def scapy_tcp_packet_factory():
    def factory(payload, src="10.0.0.1", dst="10.0.0.2", ack=1):
        return IP(src=src, dst=dst) / TCP(ack=ack) / Raw(load=payload)

    return factory
