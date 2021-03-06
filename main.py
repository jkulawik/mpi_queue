from queue_class import PacketQueue
from small_classes import EventType, Event, Packet
from misc import exp
# Statystyki
import matplotlib.pyplot as plot


# GLOBALNE Parametry symulacji - nie musimy zerować przy pętli
keep_packet_len: bool = False
total_sim_time = 500.0
avg_input_rate = 0.1  # λ
avg_service_time = 0.2  # μ (w tego typu symulacji długość obsługi i wielkość pakietu są równoważne)
REPETITIONS = 1
DIFFERENCE_LIST = []
THEO_LIST = []
PRACT_LIST = []

# Inicjalizacja

# Routing: pakiety mają adresy docelowe a kolejki "wiedzą" o wszystkich innych kolejkach
# Zakładamy routing typu wejście->1->2->...->N->wyjście

for sim_repetition in range(REPETITIONS):
    #To trzeba było przenieść aby było na każdą iteracje nowe
    event_list = []
    time = 0.0
    Packet.avg_service_time = avg_service_time
    PACKET_PER_QUEUE = {}  # Liczba pakietów przesłana przez daną kolejkę. Liczba pakietów / total_sim_time -> przepustowość

    queues = []
    LAST_HOP = 30  # ta liczba definiuje też liczbę kolejek w systemie/
    for i in range(LAST_HOP):
        queues.append(PacketQueue(i, keep_packet_len, event_list))
        #print(queues[i])  # debug adresów

    # Statystyki
    input_intervals = []
    output_intervals = []
    avg_thru_time_sum = 0.0
    avg_thru_packet_count = 0
    previous_exit_time = 0.0

    # Generacja pierwszego eventu
    start_arrival_time = exp(avg_input_rate)
    input_intervals.append(start_arrival_time)
    start_packet = Packet(arrival_time=start_arrival_time, destination_address="exit", creation_time=0.0)  # domyślnie pójdzie do q1
    event_list.append(Event(EventType.PACKET_ARRIVAL, start_packet, start_arrival_time, event_address=0))

    loop_count = 0
    while time < total_sim_time:
        event_list.sort(key=lambda x: x.time)
        event = event_list[0]
        assert(event.time >= time)
        time = event.time

        loop_count += 1
        #print("Loop:", loop_count)
        #print("Number of events in list:", len(event_list))
        #print(event)

        # Do którejś kolejki przyszedł pakiet:
        if event.event_type == EventType.PACKET_ARRIVAL:
            next_hop = event.packet.next_hop_address
            #print(next_hop)
            if next_hop == 0:
                # Generacja nowego pakietu na wejściu
                interval = exp(avg_input_rate)
                arrival_time = interval + time
                new_packet = Packet(arrival_time, destination_address="exit",
                                    creation_time=time)  # domyślnie pójdzie do q1
                event_list.append(Event(EventType.PACKET_ARRIVAL, new_packet, arrival_time, event_address=0))
                #print(f'NEW PACKET WILL ARRIVE {arrival_time}')
            # "Routing"
            if next_hop == LAST_HOP:  # To mógłby być nowy typ eventu ale chyba tu będzie wygodniej
                #print(f"Packet left network at time {time}")
                avg_thru_time_sum += time-event.packet.creation_time
                avg_thru_packet_count += 1

                # Statystyki
                input_intervals.append(interval)
                output_intervals.append(time-previous_exit_time)
                previous_exit_time = time
            else:
                current_q = queues[event.packet.next_hop_address]
                current_q.buffer_packet(event.packet)  # To generuje nowy event typu Packet Serviced

        # W którejś kolejce ma zostać obsłużony pakiet:
        elif event.event_type == EventType.PACKET_SERVICE:
            #print(event)
            current_q = None
            # Znajdujemy kolejkę która powinna obsłużyć pakiet z Eventu:
            for q in queues:
                if event.packet in q.queue:
                    current_q = q
                    #print(f"Debug: packet found in queue {current_q.address}")
                    try:#W celu zliczenia ile obsłużono pakietów dla danych kolejek, zwiększamy counter po każdej iteracji
                        PACKET_PER_QUEUE[q.address] += 1
                    except:
                        PACKET_PER_QUEUE[q.address] = 1
                    current_q.service_next_packet(time)  # to wygeneruje nowy arrival

        event_list.pop(0)  # usuwamy event

    # Wyniki
    serviced_packets = PACKET_PER_QUEUE[LAST_HOP-1]
    print("Obsłużona liczba pakietów:", PACKET_PER_QUEUE)
    #link_delay = PacketQueue.link_transfer_delay  # TODO nieuwzględnione w obliczeniach

    l = 1/avg_input_rate
    u = avg_service_time
    r = l/u  # rho

    for q in range(len(PACKET_PER_QUEUE)):
        thru = PACKET_PER_QUEUE[q] / total_sim_time
        PRACT_LIST.append(thru)

        if q != 0:
            l = 1/THEO_LIST[q-1]
        print(l)
        theo = r/u + 1/(u-l) + pow(r, 2)/(l-u)  # to już jest wartość oczekiwana
        # więc dla kolejnych kolejek lambda wynosi odwrotność tej wartości (tylko nw czy to poprawne wg. teorii)

        THEO_LIST.append(theo)

        DIFFERENCE_LIST.append((theo - thru) * 100 / theo)

#

print(THEO_LIST)
#plot.style.use('seaborn-deep')

# plot.plot(DIFFERENCE_LIST, 'ro')
# plot.title("Różnica w %")
# plot.xlabel("Numer kolejki w łańcuchu")
# plot.show()

plot.plot(THEO_LIST, 'b+')
plot.title("Przepustowość teoretyczna [pakiet/s]")
plot.xlabel("Numer kolejki w łańcuchu")
plot.show()

plot.plot(PRACT_LIST, 'g+')
plot.title("Przepustowość zmierzona [pakiet/s]")
plot.xlabel("Numer kolejki w łańcuchu")
plot.show()


# x_axis = numpy.linspace(0.0, 0.5)
# #plot.style.use('seaborn-deep')
# plot.hist([input_intervals, output_intervals], label=["input", "output"])
# plot.legend(loc='upper right')
# plot.title("Rozkład opóźnień między pakietami na wejściu i wyjściu sieci")
# plot.show()
