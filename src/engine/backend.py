import logging
import os
import re
import socket
import psutil

from scapy.interfaces import get_working_ifaces
from scapy.interfaces import NetworkInterface

from src.consts.enums import ConnectionError
from src.consts.logger import LOGGING_NAME
from src.consts.connectivity_test_hosts import (
    CONNECTIVITY_HOSTS,
    CONNECTIVITY_TEST_PORT,
    CONNECTION_TIMEOUT,
)


# Game protocol signatures for packet filtering
PROTOCOL_SIGNATURES = {
    "json_start": "{",  # JSON format packets
    "special_start": "x",  # Special format packets
    "min_length": 30,  # Minimum packet length
    "excluded_keys": ["inventory_charms", "steam"],  # Keys to exclude
}

GAME_PROCESS_NAMES = {
    "herosiege",
    "herosiegeexe",
    "herosiegewin64shippingexe",
}

APP_PROCESS_NAMES = {
    "herosiegestats",
    "herosiegestatsexe",
}

PCAP_IF_UP = 0x00000002


def _normalize_process_name(name: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def _interface_flags_indicate_up(flags) -> bool:
    if isinstance(flags, int):
        # Some capture providers report 0 while still returning usable interfaces.
        return flags == 0 or bool(flags & PCAP_IF_UP)

    flags_text = str(flags).upper()
    return not flags_text or any(flag in flags_text for flag in ("OK", "UP", "RUNNING"))


def _is_usable_interface(iface: NetworkInterface) -> bool:
    return bool(getattr(iface, "ip", "")) and _interface_flags_indicate_up(
        getattr(iface, "flags", "")
    )


def _is_virtual_interface(iface: NetworkInterface) -> bool:
    description = getattr(iface, "description", "") or ""
    return "virtual" in description.lower() or "hyper-v" in description.lower()


class Backend:
    @staticmethod
    def get_open_connections_from_process() -> set:
        current_pid = os.getpid()
        pids: set[int] = set()
        hs_ips = set()
        for proccess in psutil.process_iter(["pid", "name"]):
            if proccess.info["pid"] == current_pid:
                continue

            process_name = _normalize_process_name(proccess.info.get("name"))
            if process_name in APP_PROCESS_NAMES:
                continue

            if process_name in GAME_PROCESS_NAMES:
                pids.add(proccess.info["pid"])

        if pids:
            connections = psutil.net_connections(kind="inet")
            for connection in connections:
                if connection.pid in pids:
                    remote_ip = getattr(connection.raddr, "ip", None)
                    if remote_ip:
                        hs_ips.add(remote_ip)
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
            ip_filter_string = f"(host {' or host '.join(sorted(hs_ips))}) and len > 30"
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
                    (CONNECTIVITY_TEST_HOST, CONNECTIVITY_TEST_PORT),
                    timeout=CONNECTION_TIMEOUT,
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
            return _is_usable_interface(iface) and not _is_virtual_interface(iface)

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
            if _is_usable_interface(interface):
                logger.warning(
                    f"Falling back to available interface: {interface.description}"
                )
                return interface.description

        logger.error("No suitable network interface found")
        return ConnectionError.InterfaceNotFound
