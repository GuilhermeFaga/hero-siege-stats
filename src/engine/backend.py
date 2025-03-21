import logging
import socket
import re

from scapy.interfaces import get_working_ifaces
from scapy.interfaces import NetworkInterface

from scapy.sendrecv import AsyncSniffer

from src.consts.enums import ConnectionError
from src.consts.logger import LOGGING_NAME

CONNECTIVITY_TEST_HOST = "google.com"
CONNECTIVITY_TEST_PORT = 80
CONNECTION_TIMEOUT = 5

# Game protocol signatures for packet filtering
PROTOCOL_SIGNATURES = {
    'json_start': '{',  # JSON format packets
    'special_start': 'x',  # Special format packets
    'min_length': 30,  # Minimum packet length
    'excluded_keys': ['inventory_charms', 'steam']  # Keys to exclude
}

class Backend:
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
        
        return f"({base_filter}) and ({json_filter} or {special_filter})"

    @staticmethod
    def initialize(packet_callback) -> AsyncSniffer | ConnectionError:
        """
        Initialize packet sniffer with protocol-based filtering
        Args:
            packet_callback: Callback function for packet processing
        Returns:
            AsyncSniffer instance or ConnectionError
        """
        logger = logging.getLogger(LOGGING_NAME)
        logger.debug("Initializing backend...")
        
        iface = Backend.get_connection_interface()
        if isinstance(iface, ConnectionError):
            logger.error(f"Failed to get connection interface: {iface}")
            return iface

        try:
            sniffer = AsyncSniffer(
                iface=iface,
                filter=Backend.get_packet_filter(),
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
                connection_iface_ip, _ = s.getsockname()
                return connection_iface_ip
        except (TimeoutError, socket.gaierror) as e:
            logger.error(f"Internet connection check failed: {e}")
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
