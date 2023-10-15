from scapy.layers.inet import IP, TCP

from scapy.interfaces import get_working_ifaces
from scapy.interfaces import NetworkInterface

from scapy.sendrecv import sr1
from scapy.sendrecv import AsyncSniffer

from scapy.packet import Packet

from src.consts.enums import ConnectionError


game_addr = "104.200.17.141"


class Backend:

    @staticmethod
    def initialize(packet_callback) -> AsyncSniffer | ConnectionError:
        result = Backend.get_connection_interface()

        if isinstance(result, ConnectionError):
            return result

        iface = result

        # TODO - Find the correct game server IP
        sniffer = AsyncSniffer(
            iface=iface,
            filter=f"host {game_addr} and len > 70",
            prn=packet_callback,
            store=False
        )
        sniffer.start()

        return sniffer

    @staticmethod
    def get_interfaces() -> list[NetworkInterface]:
        return get_working_ifaces()

    @staticmethod
    def check_internet_connection():
        packet = IP(dst="google.com") / TCP(dport=80, flags='S')
        response: Packet | None = sr1(packet, timeout=5)

        if response is None:
            return False

        return True

    @staticmethod
    def check_server_connection() -> list[str] | None:
        packet = IP(dst=game_addr) / TCP(dport=80, flags='S')
        response: Packet | None = sr1(packet, timeout=5)

        if response is None:
            return None

        return response.route()

    @staticmethod
    def get_connection_interface() -> str | ConnectionError:
        connection = Backend.check_server_connection()

        if connection is None:
            return ConnectionError.NoInternet

        _, connection_iface_ip, _ = connection

        for interface in Backend.get_interfaces():
            if "OK" not in interface.flags or not interface.ip:
                continue

            if interface.ip == connection_iface_ip:
                return interface.description

        return ConnectionError.InterfaceNotFound
