import enum
from misc import exp


class EventType(enum.Enum):
    PACKET_ARRIVAL = 0
    PACKET_SERVICED = 1


class Packet:
    # TODO Można tu dodać referencję do kolejki żeby łatwiej było przetwarzać zdarzenia
    # wtedy byłaby taka hierarchia że zdarzenie -> pakiet -> kolejka -> wytwórz zdarzenie

    service_time = None  # This basically represents packet size
    service_end_time = None
    avg_service_time = 0.125

    def __init__(self, arrival_time: float, destination_address: str):
        self.arrival_time = arrival_time
        self.randomize_service_time()
        self.destination_address = destination_address

    # Oddzielone jako funkcja żeby wykorzystać w ruterach
    def randomize_service_time(self):
        self.service_time = exp(self.avg_service_time)
        self.service_end_time = self.arrival_time + self.service_time


class Event:
    def __init__(self, time, event_type: EventType, packet: Packet):
        self.time = time
        self.event_type = event_type
        self.packet = packet  # the packet that arrived or was serviced

    def __str__(self):
        return f'Time: {self.time} Type: {self.event_type}'
