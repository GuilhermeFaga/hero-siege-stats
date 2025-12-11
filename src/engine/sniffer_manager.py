import logging
import threading

from src.engine import Engine
from src.engine.backend import Backend
from src.consts.logger import LOGGING_NAME
from src.engine import sniffer_filter_thread

from scapy.sendrecv import AsyncSniffer
from src.consts.enums import ConnectionError

class SnifferManager():
    def __init__(self,packet_callback):
        self.logger = logging.getLogger(LOGGING_NAME)
        self.iface = Backend.get_connection_interface()
        self.filter = Backend.get_packet_filter()
        self.callback = packet_callback
        self._create_sniffer()
        
        self._start_filter_thread()

    def _create_sniffer(self):
        try:
            if self.iface == ConnectionError.InterfaceNotFound:
                raise Exception("No Interface found")
            self.sniffer = AsyncSniffer(
                iface=self.iface,
                filter=self.filter,
                prn=self.callback,
                store=False
            )
            self.sniffer.start()
            self.logger.info(f"Sniffer started on interface: {self.iface}")
        except Exception as e:
            self.logger.error(f"Failed to initialize sniffer: {e}")
            #Workaround for app.py handling of sniffer creation/usage
            self.sniffer = ConnectionError.InterfaceNotFound

    def change_sniffer_filter(self,new_filter):
        if hasattr(self.sniffer,'stop_cb'):
            self.sniffer.stop()
            self.filter = new_filter


            from src.engine.message_parser import MessageParser
            MessageParser.reset_packet_buffers()
            
            self._create_sniffer()
            self.logger.info(f"Sniffer-Filter changed to : {new_filter}")
            
        else:
            self.logger.warning("Tried to stop sniffer too early after starting it.")
    
    def _start_filter_thread(self):
        check_for_filter_changes_thread = threading.Thread(target=sniffer_filter_thread.observe_changing_ips,args=(self,))
        check_for_filter_changes_thread.daemon = True
        if not check_for_filter_changes_thread.is_alive():
            check_for_filter_changes_thread.start()

sniffer_manager = SnifferManager(Engine.queue_an_event)