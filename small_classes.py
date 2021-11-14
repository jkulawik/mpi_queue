import enum
from misc import exp


class EventType(enum.Enum):
    PACKET_ARRIVAL = 0  # Oznacza przyjście pakietu do bufora jakiejś kolejki
    PACKET_SERVICED = 1  # Oznacza zakończenie przetwarzania pakietu i przesłanie go dalej


class Packet:

    service_time = None  # Możemy uznać że długość obsługi oznacza wielkość pakietu
    service_end_time = None
    next_hop_address = 1  # dla ułatwienia od razu przypiszmy ruter brzegowy (zmiana na int)
    avg_service_time = 0.125  # to można przechować gdziekolwiek ale tu jest wygodnie

    def __init__(self, arrival_time: float, destination_address: int):
        self.arrival_time = arrival_time
        self.randomize_service_time()
        self.destination_address = destination_address

    # Oddzielone jako funkcja żeby wykorzystać w ruterach
    def randomize_service_time(self):
        self.service_time = exp(self.avg_service_time)
        self.service_end_time = self.arrival_time + self.service_time


class Event:

    def __init__(self, event_type: EventType, packet: Packet):
        self.event_type = event_type
        self.packet = packet  # the packet that arrived or was serviced
        # self.time = packet.arrival_time
        # ^ Wydaje mi się że 1. tu jest błąd, bo przecież event zakończenia obsługi nie ustawimy na arrival_time
        # 2. W efekcie lepiej to wynieść do metody time(), skoro i tak pozyskujemy to na bazie pakietu

    def __str__(self):
        return f'Time: {self.time} Type: {self.event_type}'

    @property
    def time(self):
        if self.event_type == EventType.PACKET_ARRIVAL:
            return self.packet.arrival_time
        elif self.event_type == EventType.PACKET_SERVICED:
            return self.packet.service_end_time
