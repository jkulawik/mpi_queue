class PacketQueue:
    def __init__(self, id_string: str, next_q_id: str, keep_packet_len: bool):
        # Variables used for routing
        self.id_string = id_string
        self.next_q_id = next_q_id
        # Other vars
        self.keep_packet_len = keep_packet_len
