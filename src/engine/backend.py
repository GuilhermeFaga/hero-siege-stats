from enum import Enum
import socket

from scapy.interfaces import get_working_ifaces
from scapy.interfaces import NetworkInterface

from scapy.sendrecv import AsyncSniffer

from src.consts.enums import ConnectionError


class Regions(str, Enum):
    AMERICAS = "America-Mevius"
    EUROPE_1 = "Europe-Inoya"
    EUROPE_2 = "Europe-Damien"
    ASIA = "Asia-Karponia"


login_servers: dict[Regions, str] = {
    Regions.AMERICAS: "104.200.17.141",
    Regions.EUROPE_1: "195.197.146.222",
    Regions.EUROPE_2: "139.144.181.45",
    Regions.ASIA: "139.162.85.20"
}


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
            filter=f"(host {' or host '.join(login_servers.values())}) and len > 30",
            prn=packet_callback,
            store=False
        )
        sniffer.start()

        return sniffer

    @staticmethod
    def get_interfaces() -> list[NetworkInterface]:
        return get_working_ifaces()

    @staticmethod
    def check_internet_connection() -> bool:
        try:
            s = socket.create_connection(("google.com", 80), timeout=5)
            s.close()

            return True

        except TimeoutError:
            print("TimeoutError",  TimeoutError)
        except socket.gaierror:
            print("socket.gaierror",  socket.gaierror)

        return False

    @staticmethod
    def check_server_connection() -> str | None:
        if not Backend.check_internet_connection():
            return None

        try:
            s = socket.create_connection(
                (login_servers[Regions.ASIA], 80), timeout=5)
            connection_iface_ip, _ = s.getsockname()
            s.close()

            return connection_iface_ip

        except TimeoutError:
            print("TimeoutError",  TimeoutError)
        except socket.gaierror:
            print("socket.gaierror",  socket.gaierror)

        return None

    @staticmethod
    def get_connection_interface() -> str | ConnectionError:
        connection_iface_ip = Backend.check_server_connection()

        if connection_iface_ip is None:
            return ConnectionError.NoInternet

        for interface in Backend.get_interfaces():
            if "OK" not in interface.flags or not interface.ip:
                continue

            if interface.ip == connection_iface_ip:
                return interface.description

        return ConnectionError.InterfaceNotFound
