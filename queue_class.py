from small_classes import Event
from small_classes import EventType
from small_classes import Packet


class PacketQueue:
    queue = []

    def __init__(self, address, keep_packet_len: bool, event_list_ref):
        self.address = address
        self.keep_packet_len = keep_packet_len
        self.event_list_ref = event_list_ref

    def buffer_packet(self, packet: Packet):
        self.queue.append(packet)

        if not self.keep_packet_len:
            packet.randomize_service_time()

        event = Event(EventType.PACKET_SERVICED, packet, packet.service_end_time, event_address=self.address)
        self.event_list_ref.append(event)

    def service_next_packet(self, time):
        if len(self.queue) == 0:  # to chyba teoretycznie nie powinno móc zajść?
            return
        packet: Packet = self.queue[0]

        # "Routing"
        # Można się bawić w tablice rutingu, ale na razie zrobiłem statycznie dla prostoty
        if self.address < 3:
            packet.next_hop_address = self.address + 1
        else:
            packet.next_hop_address = "exit"

        # jeżeli obsługujemy pakiet w tym miejscu, to znaczy że przechodzi on przez sieć;
        # tym samym jego czas przyjścia do następnego rutera chyba _nie_ powinien być losowy z rozkład wykładniczym?
        packet.arrival_time = time + 0.1  # Na razie jest więc stały czas propagacji między ruterami
        # TODO upewnić się czy czas propagacji między ruterami powinien być stały

        # "Wysłanie" pakietu dalej:
        event = Event(EventType.PACKET_ARRIVAL, packet, packet.arrival_time, event_address=packet.next_hop_address)
        self.event_list_ref.append(event)
        # Pakiet obsłużony, wywalamy go z bufora:
        self.queue.pop(0)
