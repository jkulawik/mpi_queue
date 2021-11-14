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
LAST_HOP = 3  # ta liczba definiuje też liczbę kolejek w systemie
for i in range(LAST_HOP):
    queues.append(PacketQueue(i, keep_packet_len, event_list))
    print(queues[i])  # debug adresów


# Generacja pierwszego eventu
start_arrival_time = exp(avg_input_rate)
start_packet = Packet(arrival_time=start_arrival_time, destination_address="exit")  # domyślnie pójdzie do q1
event_list.append(Event(EventType.PACKET_ARRIVAL, start_packet, start_arrival_time, event_address=0))

loop_count = 0
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
        if next_hop == LAST_HOP:  # To mógłby być nowy typ eventu ale chyba tu będzie wygodniej
            print(f"Packet left network at time {time}")

            # Generacja nowego pakietu na wejściu
            arrival_time = exp(avg_input_rate) + time
            new_packet = Packet(arrival_time, destination_address="exit")  # domyślnie pójdzie do q1
            event_list.append(Event(EventType.PACKET_ARRIVAL, new_packet, arrival_time, event_address=1))
        else:
            current_q = queues[event.packet.next_hop_address]
            current_q.buffer_packet(event.packet)  # To generuje nowy event typu Packet Serviced

    # W którejś kolejce ma zostać obsłużony pakiet:
    elif event.event_type == EventType.PACKET_SERVICE:
        current_q = None
        # Znajdujemy kolejkę która powinna obsłużyć pakiet z Eventu:
        for q in queues:
            if event.packet in q.queue:
                current_q = q
                print(f"Debug: packet found in queue {current_q.address}")
        current_q.service_next_packet(time)  # to wygeneruje nowy arrival

    event_list.pop(0)  # usuwamy event


