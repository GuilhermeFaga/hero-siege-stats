import time

from typing import TYPE_CHECKING

from src.engine.backend import Backend

if TYPE_CHECKING:
    from src.engine.sniffer_manager import SnifferManager

def observe_changing_ips(sniffer_manager: "SnifferManager"):
    while True:
        new_filter : str = Backend.get_packet_filter()
        if new_filter:
            if new_filter != sniffer_manager.filter:
                sniffer_manager.change_sniffer_filter(new_filter)
        time.sleep(1)