import logging
import socket

from scapy.interfaces import get_working_ifaces
from scapy.interfaces import NetworkInterface

from scapy.sendrecv import AsyncSniffer

from src.consts.enums import ConnectionError
from src.consts.logger import LOGGING_NAME

LOGIN_SERVERS = {
    "America-Mevius": "104.200.17.141",
    "Europe-Inoya": "195.197.146.222",
    "Europe-Damien": "139.144.181.45",
    "Japan-Karponia": "139.162.85.20"
}

CONNECTIVITY_TEST_HOST = "google.com"
CONNECTIVITY_TEST_PORT = 80
CONNECTION_TIMEOUT = 5

class Backend:
    @staticmethod
    def initialize(packet_callback) -> AsyncSniffer | ConnectionError:
        logger = logging.getLogger(LOGGING_NAME)
        logger.debug("Initializing backend...")
        
        iface = Backend.get_connection_interface()
        if isinstance(iface, ConnectionError):
            logger.error(f"Failed to get connection interface: {iface}")
            return iface

        try:
            # TODO - Find the correct game server IP
            sniffer = AsyncSniffer(
                iface=iface,
                filter=f"(host {' or host '.join(LOGIN_SERVERS.values())}) and len > 30",
                prn=packet_callback,
                store=False
            )
            sniffer.start()
            logger.info(f"Sniffer started on interface: {iface}")
            return sniffer
            
        except Exception as e:
            logger.error(f"Failed to initialize sniffer: {e}")
            return ConnectionError.InterfaceNotFound

    @staticmethod
    def get_interfaces() -> list[NetworkInterface]:
        return get_working_ifaces()

    @staticmethod
    def check_internet_connection() -> bool:
        logger = logging.getLogger(LOGGING_NAME)
        try:
            with socket.create_connection(
                (CONNECTIVITY_TEST_HOST, CONNECTIVITY_TEST_PORT), 
                timeout=CONNECTION_TIMEOUT
            ) as s:
                return True
        except (TimeoutError, socket.gaierror) as e:
            logger.error(f"Internet connection check failed: {e}")
            return False

    @staticmethod
    def check_server_connection() -> str | None:
        logger = logging.getLogger(LOGGING_NAME)
        if not Backend.check_internet_connection():
            logger.warning("No internet connection available")
            return None

        try:
            with socket.create_connection(
                (LOGIN_SERVERS["America-Mevius"], CONNECTIVITY_TEST_PORT), 
                timeout=CONNECTION_TIMEOUT
            ) as s:
                connection_iface_ip, _ = s.getsockname()
                return connection_iface_ip
        except (TimeoutError, socket.gaierror) as e:
            logger.error(f"Server connection check failed: {e}")
            return None

    @staticmethod
    def get_connection_interface() -> str | ConnectionError:
        logger = logging.getLogger(LOGGING_NAME)
        connection_iface_ip = Backend.check_server_connection()

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
            if is_valid_physical_interface(interface) and interface.ip == connection_iface_ip:
                logger.info(f"Found matching physical interface: {interface.description}")
                return interface.description

        # Try to find any available physical interface
        for interface in interfaces:
            if is_valid_physical_interface(interface):
                logger.info(f"Using available physical interface: {interface.description}")
                return interface.description

        # Fallback to any working interface
        for interface in interfaces:
            if "OK" in interface.flags and interface.ip:
                logger.warning(f"Falling back to available interface: {interface.description}")
                return interface.description

        logger.error("No suitable network interface found")
        return ConnectionError.InterfaceNotFound
