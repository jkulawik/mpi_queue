import enum
from misc import exp


class EventType(enum.Enum):
    PACKET_ARRIVAL = 0  # Oznacza przyjście pakietu do bufora jakiejś kolejki
    PACKET_SERVICE = 1  # Oznacza zakończenie przetwarzania i rozpoczęcie wysyłania pakietu


class Packet:
    avg_service_time = 0.125  # to można przechować gdziekolwiek ale tu jest wygodnie

    def __init__(self, arrival_time: float, destination_address: str):
        self.service_time = None
        self.service_end_time = None
        self.arrival_time = arrival_time
        self.randomize_service_time()
        self.destination_address = destination_address
        self.next_hop_address = 1  # dla ułatwienia od razu przypiszmy poprawny dla nowych pakietów

    # Oddzielone jako funkcja żeby wykorzystać w ruterach
    def randomize_service_time(self):
        self.service_time = exp(self.avg_service_time) # Możemy uznać że długość obsługi oznacza wielkość pakietu
        self.service_end_time = self.arrival_time + self.service_time


class Event:
    def __init__(self, event_type: EventType, packet: Packet, time: float, event_address):
        self.event_type = event_type
        self.packet = packet  # the packet that arrived or was serviced
        self.time = time
        self.event_address = event_address

    def __str__(self):
        ret = f"Event:\n"
        ret += f"\tTime: {self.time}\n"
        if self.event_type == EventType.PACKET_ARRIVAL:
            ret += f"\tPacket arrived in router {self.event_address}"
        elif self.event_type == EventType.PACKET_SERVICE:
            ret += f"\tPacket service in router {self.event_address}"
        return ret
