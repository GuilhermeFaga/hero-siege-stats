import logging
import socket
import psutil

from scapy.interfaces import get_working_ifaces
from scapy.interfaces import NetworkInterface

from src.consts.enums import ConnectionError
from src.consts.logger import LOGGING_NAME
from src.consts.connectivity_test_hosts import CONNECTIVITY_HOSTS,CONNECTIVITY_TEST_PORT,CONNECTION_TIMEOUT



# Game protocol signatures for packet filtering
PROTOCOL_SIGNATURES = {
    "json_start": "{",  # JSON format packets
    "special_start": "x",  # Special format packets
    "min_length": 30,  # Minimum packet length
    "excluded_keys": ["inventory_charms", "steam"],  # Keys to exclude
}


class Backend:

    @staticmethod
    def get_open_connections_from_process() -> set:
        pid: int = 0
        hs_ips = set()
        for proccess in psutil.process_iter(["pid", "name"]):
            if proccess.info["name"] == "Hero_Siege.exe":
                pid = proccess.info["pid"]

        if pid != 0:
            connections = psutil.net_connections(kind="inet")
            for connection in connections:
                if connection.pid == pid:
                    hs_ips.add(connection.raddr.ip)
        return hs_ips

    @staticmethod
    def get_packet_filter() -> str:
        """
        Generate BPF filter based on protocol signatures
        Returns: BPF filter string
        """
        # Filter for TCP packets with minimum length
        base_filter = f"tcp and len > {PROTOCOL_SIGNATURES['min_length']}"

        # Filter for JSON format packets (starting with '{')
        json_filter = f"tcp[((tcp[12:1] & 0xf0) >> 2):1] = 0x{ord(PROTOCOL_SIGNATURES['json_start']):02x}"

        # Filter for special format packets (starting with 'x')
        special_filter = f"tcp[((tcp[12:1] & 0xf0) >> 2):1] = 0x{ord(PROTOCOL_SIGNATURES['special_start']):02x}"

        hs_ips = Backend.get_open_connections_from_process()
        if not hs_ips:
            ip_filter_string = "len < 0"
        else:
            ip_filter_string = f"(host {' or host '.join(hs_ips)}) and len > 30"
        # following filter line commented out because there seems to be a flaw because no package is actually getting through
        # return f"({base_filter}) and ({json_filter} or {special_filter})"
        return ip_filter_string

    @staticmethod
    def get_interfaces() -> list[NetworkInterface]:
        return get_working_ifaces()

    @staticmethod
    def check_internet_connection() -> bool:
        logger = logging.getLogger(LOGGING_NAME)
        for CONNECTIVITY_TEST_HOST in CONNECTIVITY_HOSTS:
            try:
                with socket.create_connection(
                    (CONNECTIVITY_TEST_HOST, CONNECTIVITY_TEST_PORT),timeout=CONNECTION_TIMEOUT
                ) as s:
                    connection_iface_ip = s.getsockname()[0]
                    return connection_iface_ip
            except (TimeoutError, socket.gaierror) as e:
                logger.info(f"Could not check connection to: {CONNECTIVITY_TEST_HOST}")
                pass
            except Exception as e:
                logger.error(f"Unknown error: {e}")
        logger.error(f"Internet connection check failed")
        return None

    @staticmethod
    def get_connection_interface() -> str | ConnectionError:
        logger = logging.getLogger(LOGGING_NAME)
        connection_iface_ip = Backend.check_internet_connection()

        if connection_iface_ip is None:
            return ConnectionError.NoInternet

        interfaces = Backend.get_interfaces()

        def is_valid_physical_interface(iface: NetworkInterface) -> bool:
            return (
                "OK" in iface.flags
                and iface.ip
                and "Virtual" not in iface.description
                and "Hyper-V" not in iface.description
            )

        # Try to find matching physical interface
        for interface in interfaces:
            if (
                is_valid_physical_interface(interface)
                and interface.ip == connection_iface_ip
            ):
                logger.info(
                    f"Found matching physical interface: {interface.description}"
                )
                return interface.description

        # Try to find any available physical interface
        for interface in interfaces:
            if is_valid_physical_interface(interface):
                logger.info(
                    f"Using available physical interface: {interface.description}"
                )
                return interface.description

        # Fallback to any working interface
        for interface in interfaces:
            if "OK" in interface.flags and interface.ip:
                logger.warning(
                    f"Falling back to available interface: {interface.description}"
                )
                return interface.description

        logger.error("No suitable network interface found")
        return ConnectionError.InterfaceNotFound
