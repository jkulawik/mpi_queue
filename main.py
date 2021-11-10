from queue_class import PacketQueue

keep_packet_len: bool = False

# Routing: q1 -> q2 -> q3
q1 = PacketQueue("1", keep_packet_len)  # entry node
q2 = PacketQueue("2", keep_packet_len)
q3 = PacketQueue("3", keep_packet_len)  # exit node

print("Hello world")
