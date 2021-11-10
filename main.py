from queue_class import PacketQueue
from small_classes import EventType

keep_packet_len: bool = False
event_list = []  # TODO dodać silne typowanie na Event?
total_sim_time = 10.0
time = 0.0


# Routing: pakiety mają adresy docelowe a kolejki "wiedzą" o wszystkich innych kolejkach
q1 = PacketQueue(1, keep_packet_len, event_list)  # entry node
q2 = PacketQueue(2, keep_packet_len, event_list)
q3 = PacketQueue(3, keep_packet_len, event_list)  # exit node

# TODO generacja pierwszego eventu

while time < total_sim_time:
    # TODO eventy korzystają z czasu dotarcia pakietu, a trzeba go jeszcze odpowiednio ustawić

    # TODO posortować eventy
    event = event_list[0]
    time = event.time

    if event.event_type == EventType.PACKET_ARRIVAL:
        next_hop = event.packet.next_hop_address

        # "Routing"
        if next_hop == "exit":
            # TODO trzeba jakoś obsłużyć pakiety wychodzące z sieci
            pass
        else:
            current_q = None
            # Trochę to głupio zrobione bo na szybko i na sztywno, pewnie da się lepiej
            if next_hop == 1:
                current_q = q1
            elif next_hop == 2:
                current_q = q2
            elif next_hop == 3:
                current_q = q3
            current_q.buffer_packet(event.packet)  # to wygeneruje nowy event serviced
    if event.event_type == EventType.PACKET_SERVICED:
        pass
        # TODO get kolejkę która powinna obsłużyć pakiet z Eventu
        # q.service_next_packet() # to wygeneruje nowy arrival

    # inne typy eventów...?
