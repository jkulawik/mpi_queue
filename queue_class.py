
class PacketQueue:

    queue = []

    def __init__(self, address: str, keep_packet_len: bool):
        self.address = address
        self.keep_packet_len = keep_packet_len

    def service_next_packet(self):
        if len(self.queue) == 0:
            return
        packet = self.queue[0]

        if not self.keep_packet_len:
            packet.randomize_service_time()
        # TODO wygenerować event i dodać go do kolejki