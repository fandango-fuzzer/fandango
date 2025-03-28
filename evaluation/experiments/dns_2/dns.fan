from struct import unpack, pack
from faker import Faker
from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from copy import deepcopy
from fandango.language.parse import parse
from fandango.language.grammar import Grammar
from random import randint
import socket
import threading

fake = Faker()

def gen_q_name():
    result = b''
    #domain_parts = fake.domain_name().split('.')
    #domain_parts = "fandango.io".split('.')
    domain_parts = "google.com".split('.')
    for part in domain_parts:
        result += len(part).to_bytes(1, 'big')
        result += part.encode('iso8859-1')
    return result

def byte_to_int(byte_val):
    return int(unpack('>H', bytes(byte_val))[0])

def msg_suffix(name):
    suffixes = []
    len_idx = 0
    prefix_len = name[len_idx]
    while prefix_len != 0:
        suffixes.append((len_idx, name[len_idx:]))
        len_idx = len_idx + prefix_len + 1
        prefix_len = name[len_idx]
    return suffixes

def to_byte_tree(byte_val):
    children = []
    for idx in range(8):
        bit_val = (byte_val >> idx) & 1
        children.insert(0, DerivationTree(NonTerminal('<bit>'), [
            DerivationTree(Terminal(bit_val))
        ]))
    return DerivationTree(NonTerminal('byte'), children)

def compress_name(uncompressed, curr_idx, len_reduction, suffix_dict):
    name_len = 0
    while uncompressed[curr_idx + name_len] != 0:
        name_len += uncompressed[curr_idx + name_len] + 1
    name_len += 1
    b_name = uncompressed[curr_idx:(curr_idx+name_len)]

    if name_len == 1:
        return b_name, name_len, len_reduction

    for n_offset, suffix in msg_suffix(b_name):
        if suffix in suffix_dict:
            cpr_ptr = suffix_dict[suffix]
            bin_ptr = pack('>H', (192 << 8) | cpr_ptr)
            new_name = b_name[:n_offset] + bin_ptr
            len_reduction += len(b_name) - len(new_name)
            return new_name, name_len, len_reduction
        else:
            offset_name_start = curr_idx
            suffix_dict[suffix] = offset_name_start + n_offset - len_reduction
            return b_name, name_len, len_reduction

def compress_msg(uncompressed):
    qd_count = byte_to_int(uncompressed[4:6])
    an_count = byte_to_int(uncompressed[6:8])
    ns_count = byte_to_int(uncompressed[8:10])
    ar_count = byte_to_int(uncompressed[10:12])
    compressed = uncompressed[0:12]
    curr_idx = 12

    suffix_dict = dict()
    len_reduction = 0
    for i in range(qd_count):
        name, decompressed_len, len_reduction = compress_name(uncompressed, curr_idx, len_reduction, suffix_dict)
        compressed = compressed + name
        curr_idx += decompressed_len
        compressed += uncompressed[curr_idx:curr_idx+4]
        curr_idx += 4
    for i in range(an_count + ns_count + ar_count):
        name, decompressed_len, len_reduction = compress_name(uncompressed, curr_idx, len_reduction, suffix_dict)
        compressed = compressed + name
        curr_idx += decompressed_len
        compressed += uncompressed[curr_idx:curr_idx+8]
        curr_idx += 8
        r_data_len = byte_to_int(uncompressed[curr_idx:curr_idx+2])
        compressed += uncompressed[curr_idx:curr_idx+2]
        curr_idx += 2
        compressed += uncompressed[curr_idx:curr_idx+r_data_len]
        curr_idx += r_data_len
    return compressed

def decompress_name(compressed, name_idx):
    segment_len = compressed[name_idx]
    compressed_len = 0
    decompressed = b''
    while segment_len != 0:
        # If first two bits are 1
        if (segment_len & 192) == 192:
            name_ptr = (segment_len & 63) << 8
            name_ptr += compressed[name_idx+1]
            decompressed = decompressed + decompress_name(compressed, name_ptr)[0]
            return decompressed, compressed_len + 2
        decompressed = decompressed + bytes([segment_len])
        decompressed = decompressed + compressed[name_idx + 1 : name_idx + 1 + segment_len]
        compressed_len = compressed_len + segment_len + 1
        name_idx = name_idx + segment_len + 1
        segment_len = compressed[name_idx]
    decompressed = decompressed + bytes([0])
    return decompressed, compressed_len + 1


def decompress_msg(compressed):
    count_header = compressed[4:12]
    qd_count = byte_to_int(count_header[:2])
    an_count = byte_to_int(count_header[2:4])
    ns_count = byte_to_int(count_header[4:6])
    ar_count = byte_to_int(count_header[6:8])
    decompressed = compressed[0:12]
    curr_idx = 12
    for i in range(qd_count):
        name, compressed_len = decompress_name(compressed, curr_idx)
        decompressed = decompressed + name
        curr_idx += compressed_len
        decompressed += compressed[curr_idx:curr_idx+4]
        curr_idx += 4
    for i in range(an_count + ns_count + ar_count):
        name, compressed_len = decompress_name(compressed, curr_idx)
        decompressed = decompressed + name
        curr_idx += compressed_len
        decompressed += compressed[curr_idx:curr_idx+8]
        curr_idx += 8
        r_data_len = byte_to_int(compressed[curr_idx:curr_idx+2])
        decompressed += compressed[curr_idx:curr_idx+2]
        curr_idx += 2
        decompressed += compressed[curr_idx:curr_idx+r_data_len]
        curr_idx += r_data_len
    return decompressed


<start> ::= <Client:dns_req> <Server:dns_resp>
<dns_req_compressed> ::= <byte>+ #:= compress_msg(<dns_req>)
<dns_resp_compressed> ::= <byte>+ #:= compress_msg(<dns_resp>)
<dns_req> ::= <header_req> <question> <answer>{byte_to_int(<req_ar_count>)} #:= decompress_msg(<dns_req_compressed>)
<dns_resp> ::= <header_resp> <question>{byte_to_int(<resp_qd_count>)} <answer>{byte_to_int(<resp_an_count>)} <answer>{byte_to_int(<resp_ns_count>)} <answer>{byte_to_int(<resp_ar_count>)} #:= decompress_msg(<dns_resp_compressed>)

#                       qr      opcode       aa tc rd  ra  z      rcode   qdcount  ancount nscount arcount
<header_req> ::= <h_id> 0 <h_opcode_standard> 0 0 <h_rd> 0 0 <bit> 0 <h_rcode_none> 0{15} 1 0{16} 0{16} <req_ar_count>
<header_resp> ::= <h_id> 1 <h_opcode_standard> <bit> 0 <h_rd> <bit> 0 <h_aa> 0 <h_rcode_none> <resp_qd_count> <resp_an_count> <resp_ns_count> <resp_ar_count>
# aa=1 if server has authority over domain

where <dns_req>.<header_req>.<h_rd> == <dns_resp>.<header_resp>.<h_rd>
where <dns_req>.<header_req>.<h_id> == <dns_resp>.<header_resp>.<h_id>
where <dns_req>.<question>.<q_name>.<q_name_written_complete> == <dns_resp>.<answer>.<q_name>.<q_name_written_complete>
where <dns_req>.<question> == <dns_resp>.<question>
<resp_qd_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<resp_an_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<resp_ns_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<resp_ar_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<req_ar_count> ::= <bit>{16} := pack(">H", randint(0, 0))

<h_id> ::= <byte><byte>
<h_opcode_standard> ::= 0 0 0 0
<h_rd> ::= <bit>
<h_aa> ::= <bit>

<h_rcode> ::= <h_rcode_none> | <h_rcode_format> | <h_rcode_server> | <h_rcode_name> | <h_rcode_ni> | <h_rcode_refused> | <h_rcode_other>
<h_rcode_none> ::= 0 0 0 0
<h_rcode_format> ::= 0 0 0 1
<h_rcode_server> ::= 0 0 1 0
<h_rcode_name> ::= 0 0 1 1
<h_rcode_ni> ::= 0 1 0 0
<h_rcode_refused> ::= 0 1 0 1
<h_rcode_other> ::= (1 <bit>{3, 3}) | (0 1 1 <bit>)
<bit> ::= 0 | 1
<byte> ::= <bit>{8}
<non_zero_byte> ::= (<bit>{7} 1) | (<bit>{6} 1 <bit>) | (<bit>{5} 1 <bit>{2}) | (<bit>{4} 1 <bit>{3}) | (<bit>{3} 1 <bit>{4}) | (<bit>{2} 1 <bit>{5}) | (<bit> 1 <bit>{6}) | (1 <bit>{7})
<label_len_octet> ::= (<bit>{7} 1) | (<bit>{6} 1 <bit>) | (<bit>{5} 1 <bit>{2}) | (<bit>{4} 1 <bit>{3}) | (<bit>{3} 1 <bit>{4}) | (<bit>{2} 1 <bit>{5}) # Max label length = 63


<question> ::= <q_name> <q_type> <rr_class>
<q_name> ::= <q_name_written_complete>
<q_name_written_complete> ::= <q_name_written>? 0{8}
<q_name_written> ::= <label_len_octet> <non_zero_byte>+ := gen_q_name()
<q_type> ::= 0{15} 1 # Equals type A (Host address)
<rr_class> ::= 0{15} 1 # Equals class IN (Internet)


<answer> ::= <q_name> ((<a_type> <rr_class>) | <type_opt> <udp_payload_size>) <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<a_type> ::= <type_a> | <type_ns> | <type_soa>
<a_ttl> ::= <byte>{4}
<a_rd_length> ::= <byte>{2} := pack(">H", randint(0, 0))
<a_rdata> ::= <byte>


<type_a> ::= 0{15} 1
<type_ns> ::= 0{14} 1 0
<type_soa> ::= 0{13} 1 1 0
<type_opt> ::= 0{10} 1 0 1 0 0 1
<udp_payload_size> ::= <bit>{16}


import socket
class Client(FandangoAgent):
        def __init__(self):
            super().__init__(True)

        def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(compress_msg(message), ("1.1.1.1", 53))
            response, nothing = sock.recvfrom(1024)
            self.receive_msg("Server", decompress_msg(response))

class Server(FandangoAgent):

        def __init__(self):
            is_fandango = False
            super().__init__(is_fandango)
            if is_fandango:
                self.id_addr = dict()
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                server_thread = threading.Thread(target=self.server_loop)
                server_thread.daemon = True
                server_thread.start()

        def server_loop(self):
            bufferSize = 1024
            localIP = "127.0.0.1"
            localPort = 25565
            self.server_socket.bind((localIP, localPort))
            while(True):
                message, addr = self.server_socket.recvfrom(bufferSize)
                m_id = message[:2]
                self.id_addr[m_id] = addr
                self.receive_msg("Client", decompress_msg(message))


        def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
            m_id = message[:2]
            self.server_socket.sendto(compress_msg(message), self.id_addr[m_id])
