import enum
from misc import exp


class EventType(enum.Enum):
    PACKET_ARRIVAL = 0  # Oznacza przyjście pakietu do bufora jakiejś kolejki
    PACKET_SERVICED = 1  # Oznacza zakończenie przetwarzania pakietu i przesłanie go dalej


class Packet:
    service_time = None  # Możemy uznać że długość obsługi oznacza wielkość pakietu
    service_end_time = None
    next_hop_address = 1  # dla ułatwienia od razu przypiszmy ruter brzegowy
    avg_service_time = 0.125  # to można przechować gdziekolwiek ale tu jest wygodnie

    def __init__(self, arrival_time: float, destination_address: str):
        self.arrival_time = arrival_time
        self.randomize_service_time()
        self.destination_address = destination_address

    # Oddzielone jako funkcja żeby wykorzystać w ruterach
    def randomize_service_time(self):
        self.service_time = exp(self.avg_service_time)
        self.service_end_time = self.arrival_time + self.service_time


class Event:
    def __init__(self, event_type: EventType, packet: Packet, time: float):
        self.event_type = event_type
        self.packet = packet  # the packet that arrived or was serviced
        self.time = time

    def __str__(self):
        return f'Time: {self.time} Type: {self.event_type}'
