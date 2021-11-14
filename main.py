from queue_class import PacketQueue
from small_classes import EventType
from small_classes import Event
from small_classes import Packet
from misc import exp

keep_packet_len: bool = False
event_list = []
total_sim_time = 10.0
time = 0.0
avg_input_rate = 0.125

# Routing: pakiety mają adresy docelowe a kolejki "wiedzą" o wszystkich innych kolejkach
# Zakładamy routing typu wejście->1->2->...->N->wyjście
queues = []
NUMBER_OF_QUEUES = 3
for i in range(NUMBER_OF_QUEUES):
    queues.append(PacketQueue(i, keep_packet_len, event_list))


# Generacja pierwszego eventu
start_arrival_time = exp(avg_input_rate)
start_packet = Packet(arrival_time=start_arrival_time, destination_address="exit")  # domyślnie pójdzie do q1
event_list.append(Event(EventType.PACKET_ARRIVAL, start_packet, start_arrival_time, event_address=1))

loop_count = 1
while time < total_sim_time:
    event_list.sort(key=lambda x: x.time)
    event = event_list[0]
    assert(event.time > time)
    time = event.time

    loop_count += 1
    print("Loop:", loop_count)
    #print("Number of events in list:", len(event_list))
    print(event)

    # Do którejś kolejki przyszedł pakiet:
    if event.event_type == EventType.PACKET_ARRIVAL:
        next_hop = event.packet.next_hop_address

        # "Routing"
        if next_hop == "exit":
            pass
            # TODO trzeba jakoś obsłużyć pakiety wychodzące z sieci
            # wygenerować nowy pakiet na wejściu sieci z czasem przyjścia = rozkład wykładniczy?
        else:
            current_q = queues[next_hop-1]
            current_q.buffer_packet(event.packet)  # To generuje nowy event typu Packet Serviced

    # W którejś kolejce został obsłużony pakiet:
    elif event.event_type == EventType.PACKET_SERVICED:
        current_q = None
        # Znajdujemy kolejkę która powinna obsłużyć pakiet z Eventu:
        for q in queues:
            if event.packet in q.queue:
                current_q = q
        current_q.service_next_packet(time)  # to wygeneruje nowy arrival

    event_list.pop(0)  # usuwamy event


