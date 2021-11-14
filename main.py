from queue_class import PacketQueue
from small_classes import EventType, Event, Packet
import logging #propozycja, używajmy typowych loggerów z poziomami

logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

keep_packet_len: bool = False
event_list = []  # TODO dodać silne typowanie na Event?
total_sim_time = 10.0
time = 0.0



# Routing: pakiety mają adresy docelowe a kolejki "wiedzą" o wszystkich innych kolejkach

#Zmieniam na słownik - będzie imo łatwiej ustawiać kolejki i pozbędziemy się ścian ifów, będzie można łatwo zmienić
#układ kolejki etc
# q1 = PacketQueue(1, keep_packet_len, event_list)  # entry node
# q2 = PacketQueue(2, keep_packet_len, event_list)
# q3 = PacketQueue(3, keep_packet_len, event_list)  # exit node

queues = {1:PacketQueue(1, keep_packet_len, event_list), 2: PacketQueue(2, keep_packet_len, event_list),
 3:PacketQueue(3, keep_packet_len, event_list)}

LAST_HOP = len(queues) #NA PRZYSZŁOSC





# Załóżmy że zaczynamy symulacje od przyjścia pakietu
event_list.append(Event(event_type=EventType.PACKET_ARRIVAL, packet=Packet(arrival_time=0.0, destination_address=LAST_HOP)))


while time < total_sim_time:
    # TODO eventy korzystają z czasu dotarcia pakietu, a trzeba go jeszcze odpowiednio ustawić

    event_list.sort(key=lambda x: x.time, reverse=False) #Sortujemy na bazie parametru time eventu
    logging.debug(f"{time}: Posortowano Liste Eventów, liczba w kolejce: {len(event_list)}")
    #event = event_list[0]
    #Zamiast brać pierwsze z wierzchu może lepiej robić pop aby od razu zdjąć z kolejki
    try:
        event = event_list.pop()
    except:
        logging.error(f"{time}: Brak pakietu do obsłużenia, lista zdarzeń pusta")
        break
    time = event.time
    logging.debug(f"{time}: Zdarzenie: {event}")

    #Możemy zamiast ściany IFów zrobić case (python 3.9), albo po prostu potworzyć funkcje dla każdego typu i zrobić refactor na
    #słownik - może być prostsze w utrzymaniu
    next_hop = event.packet.next_hop_address
    logging.debug(f"{time} Aktualny next hop: {next_hop}")
    if event.event_type == EventType.PACKET_ARRIVAL:


        # "Routing"
        if next_hop == -1:
            # TODO trzeba jakoś obsłużyć pakiety wychodzące z sieci
            pass
        else:
            #current_q = None
            # Next hop ma mieszane typy, propozycja: zawsze inty, exit na -1
            # if next_hop == 1:
            #     current_q = q1
            # elif next_hop == 2:
            #     current_q = q2
            # elif next_hop == 3:
            #     current_q = q3
            #Słownik zamiast ściany ifów, elastyczniej i DRY
            current_q = queues.get(next_hop, None)
            current_q.buffer_packet(event.packet)  # to wygeneruje nowy event serviced

    if event.event_type == EventType.PACKET_SERVICED:
        current_q = queues.get(next_hop, None)
        current_q.service_next_packet() # to wygeneruje nowy arrival
    # inne typy eventów...?

