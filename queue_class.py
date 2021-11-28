from small_classes import Event, EventType, Packet
from misc import exp


class PacketQueue:
    link_transfer_delay = 0.0

    def __str__(self):
        return f"Queue with address {self.address}"

    def __init__(self, address, keep_packet_len: bool, event_list_ref):
        self.queue = []
        self.address = address
        self.keep_packet_len = keep_packet_len
        self.event_list_ref = event_list_ref

    def generate_packet_service_event(self, packet: Packet, time):
        if not self.keep_packet_len:
            packet.service_time = exp(packet.avg_service_time)
        packet.service_end_time = time + packet.service_time

        event = Event(EventType.PACKET_SERVICE, packet, packet.service_end_time, event_address=self.address)
        self.event_list_ref.append(event)

    def buffer_packet(self, packet: Packet):
        #print(f"Debug: router {self.address} buffering")
        self.queue.append(packet)

        # Jeżeli kolejka była wcześniej pusta, nie zostanie wygenerowany event obsługi więc trzeba to zrobić tutaj:
        if len(self.queue) == 1:
            self.generate_packet_service_event(packet, packet.arrival_time)

    def service_next_packet(self, time):
        #print(f"Debug: router {self.address} service start")

        if len(self.queue) == 0:  # to chyba teoretycznie nie powinno móc zajść?
            print("WARNING: Trying to service empty queue")
            return
        packet: Packet = self.queue[0]

        # "Routing"
        packet.next_hop_address = self.address + 1
        #print(f"Debug: packet's next hop is {packet.next_hop_address}")

        # jeżeli obsługujemy pakiet w tym miejscu, to znaczy że przechodzi on przez sieć;
        # tym samym jego czas przyjścia do następnego rutera chyba _nie_ powinien być losowy z rozkład wykładniczym?
        packet.arrival_time = time + self.link_transfer_delay  # Na razie jest więc stały czas propagacji między ruterami
        # TODO upewnić się czy czas propagacji między ruterami powinien być stały

        # "Wysłanie" pakietu dalej:
        event = Event(EventType.PACKET_ARRIVAL, packet, packet.arrival_time, event_address=packet.next_hop_address)
        self.event_list_ref.append(event)
        # Pakiet obsłużony, wywalamy go z bufora:
        self.queue.pop(0)

        # Generujemy czas obsługi dla następnego pakietu
        if len(self.queue) > 0:
            self.generate_packet_service_event(self.queue[0], time)
