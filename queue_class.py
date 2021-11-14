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
        # TODO ustawić czas zdarzenia na czas zakończenia obsługi pakietu
        packet.randomize_service_time()

        event = Event(EventType.PACKET_SERVICED, packet)
        self.event_list_ref.append(event)

    def service_next_packet(self):
        if len(self.queue) == 0:
            return
        packet: Packet = self.queue.pop(0)
        #Musimy ustawić tu dotarcie na koniec obsługi, bo inaczej zostanie 0.0
        packet.arrival_time = packet.service_end_time
        if not self.keep_packet_len:
            packet.randomize_service_time()

        # "Routing"
        # Można się bawić w tablice rutingu, ale na razie zrobiłem statycznie dla prostoty
        if self.address < 3:
            packet.next_hop_address = self.address + 1
        else:
            packet.next_hop_address = -1

        # "Wysłanie" pakietu dalej:
        event = Event(EventType.PACKET_ARRIVAL, packet)
        self.event_list_ref.append(event)
        # Pakiet obsłużony, wywalamy go z bufora:
        #Refactor: pop zwraca popowany obiekt, także można użyć od razu na górze pop