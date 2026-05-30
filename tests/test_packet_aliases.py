import sys
import types
import unittest


def _stub_optional_dependencies():
    psutil = types.ModuleType("psutil")
    psutil.process_iter = lambda attrs=None: []
    psutil.net_connections = lambda kind=None: []
    sys.modules.setdefault("psutil", psutil)

    scapy = types.ModuleType("scapy")
    scapy_all = types.ModuleType("scapy.all")
    scapy_interfaces = types.ModuleType("scapy.interfaces")
    scapy_layers = types.ModuleType("scapy.layers")
    scapy_inet = types.ModuleType("scapy.layers.inet")

    class Packet:
        pass

    class NetworkInterface:
        pass

    scapy_all.Packet = Packet
    scapy_interfaces.get_working_ifaces = lambda: []
    scapy_interfaces.NetworkInterface = NetworkInterface
    scapy_inet.IP = object()
    scapy_inet.TCP = object()

    sys.modules.setdefault("scapy", scapy)
    sys.modules.setdefault("scapy.all", scapy_all)
    sys.modules.setdefault("scapy.interfaces", scapy_interfaces)
    sys.modules.setdefault("scapy.layers", scapy_layers)
    sys.modules.setdefault("scapy.layers.inet", scapy_inet)


_stub_optional_dependencies()

from src.consts import events as consts
from src.engine.backend import _interface_flags_indicate_up, _normalize_process_name
from src.engine.message_parser import MessageParser
from src.models.stats.added_items import AddedItemsStats


class PacketAliasTests(unittest.TestCase):
    def test_identifies_renamed_packet_fields(self):
        cases = [
            ({"currency_data": {}}, consts.EvNameUpdateGold),
            ({"total_guild_xp": 10}, consts.EvNameUpdateXP),
            ({"added_item_object": {"rarity": "Satanic", "item_id": 1}}, consts.EvNameItemAdded),
            ({"satanic_zone_name": "SZ_1_1", "zone_buffs": [1]}, consts.EvNameUpdateSatanicZone),
            ({"experience": 123, "season": 10}, consts.EvNameUpdateAccount),
        ]

        for payload, event_name in cases:
            with self.subTest(payload=payload):
                self.assertEqual(MessageParser.identify_event(payload), event_name)

    def test_nested_payloads_are_flattened_into_events(self):
        payloads = [
            [
                {"currency_data": {"gss": 100, "gsh": 0, "gns": 0, "gnh": 0, "gbp": 0}},
                {"total_guild_xp": 500, "message": "Gained 15 XP"},
            ],
            {"satanic_zone_name": "SZ_1_1", "zone_buffs": [1, 26]},
        ]

        events = MessageParser.message_to_event(payloads)

        self.assertEqual([event.name for event in events], [
            consts.EvNameUpdateGold,
            consts.EvNameUpdateXP,
            consts.EvNameUpdateSatanicZone,
        ])
        self.assertEqual(events[0].value.GSS, 100)
        self.assertEqual(events[1].value, 15)
        self.assertIn("Act 1", events[2].value.satanic_zone)

    def test_query_string_nested_json_values_are_deserialized(self):
        payloads = [
            {
                "currency_data": '{"gss": 321, "gsh": 0, "gns": 0, "gnh": 0, "gbp": 0}'
            }
        ]

        events = MessageParser.message_to_event(payloads)

        self.assertEqual(events[0].name, consts.EvNameUpdateGold)
        self.assertEqual(events[0].value.GSS, 321)

    def test_capture_accepts_json_arrays(self):
        payload = 'prefix [{"total_guild_xp": 500, "message": "Gained 15 XP"}] suffix'

        messages = MessageParser.capture(payload, "127.0.0.1", "127.0.0.2")
        events = MessageParser.message_to_event(messages)

        self.assertEqual(events[0].name, consts.EvNameUpdateXP)
        self.assertEqual(events[0].value, 15)

    def test_item_stats_accept_named_rarity_and_magic_find_alias(self):
        events = MessageParser.message_to_event([
            {"added_item_object": {"rarity": "Satanic", "mfDrop": 1, "item_id": 123}}
        ])
        stats = AddedItemsStats()

        stats.update(events[0].value)

        self.assertEqual(stats.added_items["Satanic"]["total"], 1)
        self.assertEqual(stats.added_items["Satanic"]["mf"], 1)

    def test_inventory_update_ext_adds_items_from_short_fields(self):
        payload = {
            "status": 1,
            "message": "Success on inventory update ext",
            "operations": {
                "add": {
                    "8-4653008-6501d20d1309c0002-1": {
                        "e": 10,
                        "m": 1,
                        "a": 676909917,
                        "sh": "1f489321a528",
                        "j": 0,
                        "b": 71,
                        "d": 6,
                        "c": 1,
                    },
                    "8-4653008-6501d20d1308a0001-6": {
                        "e": 10,
                        "a": 624778371,
                        "sh": "91011929141f",
                        "j": 0,
                        "b": 8,
                        "d": 9,
                        "c": 0,
                    },
                }
            },
        }

        events = MessageParser.message_to_event([payload])
        stats = AddedItemsStats()

        for event in events:
            stats.update(event.value)

        self.assertEqual([event.name for event in events], [
            consts.EvNameItemAdded,
            consts.EvNameItemAdded,
        ])
        self.assertEqual(stats.added_items["Satanic"]["total"], 1)
        self.assertEqual(stats.added_items["Satanic"]["mf"], 1)
        self.assertEqual(stats.added_items["Heroic"]["total"], 1)
        self.assertEqual(stats.added_items["Heroic"]["mf"], 0)

    def test_hero_siege_process_names_are_normalized(self):
        self.assertEqual(_normalize_process_name("Hero_Siege.exe"), "herosiegeexe")
        self.assertEqual(_normalize_process_name("Hero Siege.exe"), "herosiegeexe")
        self.assertEqual(_normalize_process_name("HeroSiege-Win64-Shipping.exe"), "herosiegewin64shippingexe")

    def test_interface_flags_support_scapy_2_7_ints(self):
        self.assertTrue(_interface_flags_indicate_up(0))
        self.assertTrue(_interface_flags_indicate_up(2))
        self.assertFalse(_interface_flags_indicate_up(32))
        self.assertTrue(_interface_flags_indicate_up("OK"))


if __name__ == "__main__":
    unittest.main()
