from scapy.all import sniff, AsyncSniffer


class Backend:

    @staticmethod
    def initialize(packet_callback):
        # TODO - Find the correct interface
        # TODO - Find the correct game server IP
        sniffer = AsyncSniffer(
            iface="Wi-Fi",
            filter="host 104.200.17.141 and len > 70",
            prn=packet_callback,
            store=False
        )
        sniffer.start()

        return sniffer
