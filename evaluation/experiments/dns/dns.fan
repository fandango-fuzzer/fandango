from struct import unpack, pack
from faker import Faker
import time
from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from copy import deepcopy
from fandango.language.parse import parse
from fandango.language.grammar import Grammar
from random import randint
import socket
import threading

fake = Faker()

fandango_is_client = False

def gen_q_name():
    result = b''
    domain_parts = fake.domain_name().split('.')
    #domain_parts = "fandango.io".split('.')
    #domain_parts = "google.com".split('.')
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
        rr_type = uncompressed[curr_idx:curr_idx+2]
        compressed += rr_type
        rr_type = byte_to_int(rr_type)
        curr_idx += 2
        compressed += uncompressed[curr_idx:curr_idx+6]
        curr_idx += 6
        r_data_len = byte_to_int(uncompressed[curr_idx:curr_idx+2])
        curr_idx += 2

        if rr_type == 5: # If CNAME entry
            name, decompressed_len, len_reduction = compress_name(uncompressed, curr_idx, len_reduction, suffix_dict)
            compressed += pack('>H', len(name))
            compressed = compressed + name
            curr_idx += decompressed_len
        else:
            compressed += uncompressed[curr_idx-2:curr_idx]
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
        rr_type = compressed[curr_idx:curr_idx+2]
        decompressed += rr_type
        rr_type = byte_to_int(rr_type)
        curr_idx += 2
        decompressed += compressed[curr_idx:curr_idx+6]
        curr_idx += 6
        r_data_len = byte_to_int(compressed[curr_idx:curr_idx+2])
        curr_idx += 2
        if rr_type == 5: #If CNAME entry
            c_name, compressed_len = decompress_name(compressed, curr_idx)
            decompressed += pack('>H', len(c_name))
            decompressed += c_name
            curr_idx += compressed_len
            pass
        else:
            decompressed += compressed[curr_idx-2:curr_idx]
            decompressed += compressed[curr_idx:curr_idx+r_data_len]
            curr_idx += r_data_len
    return decompressed


<start> ::= <exchange>

# Each exchange consists of a request made by the client and a response from the server.
<exchange> ::= <Client:dns_req> <Server:dns_resp>

# A request consists of a header and a number of questions and answers as specified in the header
<dns_req> ::= <header_req> <question>{byte_to_int(<req_qd_count>)} <answer>{byte_to_int(<req_ar_count>)}
<dns_resp> ::= <header_resp> <question>{byte_to_int(<header_req>.<req_qd_count>)} <answer_an>{byte_to_int(<resp_an_count>)} <answer_au>{byte_to_int(<resp_ns_count>)} <answer_opt>{byte_to_int(<resp_ar_count>)}

#                       qr      opcode       aa tc rd  ra  z      rcode   qdcount  ancount nscount arcount
<header_req> ::= <h_id> 0 <h_opcode_standard> 0 0 <h_rd> 0 0 <bit> 0 <h_rcode_none> <req_qd_count> 0{16} 0{16} <req_ar_count>
<header_resp> ::= <h_id> 1 <h_opcode_standard> <bit> 0 <h_rd> <h_ra> 0 <h_aa> 0 (<h_rcode_none> | <h_rcode_name>) <resp_qd_count> <resp_an_count> <resp_ns_count> <resp_ar_count>
# aa=1 if server has authority over domain

where forall <ex> in <start>.<exchange>:
    <ex>.<dns_resp>.<header_resp>.<h_rd> == <ex>.<dns_req>.<header_req>.<h_rd>
    and <ex>.<dns_resp>.<header_resp>.<h_id> == <ex>.<dns_req>.<header_req>.<h_id>
    and <ex>.<dns_resp>.<question> == <ex>.<dns_req>.<question>
    and bytes(<ex>.<dns_resp>.<header_resp>.<resp_qd_count>) == bytes(<ex>.<dns_req>.<header_req>.<req_qd_count>)


<req_qd_count> ::= <byte>{2} := pack(">H", 1)
<resp_qd_count> ::= <bit>{16} := pack(">H", 1)
<resp_an_count> ::= <bit>{16} := pack(">H", randint(1, 2))
<resp_ns_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<resp_ar_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<req_ar_count> ::= <bit>{16} := pack(">H", randint(0, 0))

<h_id> ::= <byte><byte>
<h_opcode_standard> ::= 0 0 0 0
<h_rd> ::= 1 # 0 causes server failure with cname
<h_aa> ::= <bit>
<h_ra> ::= <bit>

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
<label_len_octet> ::= <byte>

<question> ::= <q_name> <q_type> <rr_class>
<q_name_optional> ::= <q_name_written>? 0{8}
<q_name> ::= <q_name_written> 0{8}
<q_name_written> ::= (<label_len_octet> <byte>{byte_to_int(b'\x00' + bytes(<label_len_octet>))})+ := gen_q_name()
<q_type> ::= <type_id_cname> | <type_id_a> | <type_id_ns>
<rr_class> ::= 0{15} 1 # Equals class IN (Internet)

# Type of first answer is the same as of the question
where forall <ex> in <start>.<exchange>:
    forall <q> in <ex>.<dns_req>.<question>:
        forall <a> in <ex>.<dns_resp>.<answer_an>:
            (bytes(<a>.children[1])[0:2] == bytes(<q>.<q_type>) and bytes(<a>.<q_name_optional>) == bytes(<q>.<q_name>))
            or get_index_within(<a>, <ex>.<dns_resp>, ['<answer_an>']) != get_index_within(<q>, <ex>.<dns_req>, ['<question>'])



<answer_au> ::= <q_name_optional> <type_soa>
<answer_opt> ::= <q_name_optional> <type_opt>
<answer_an> ::= <q_name_optional> (<type_a> |<type_cname> | <type_ns>)
<answer> ::= <q_name_optional> (<type_a> |<type_cname> | <type_ns> | <type_soa> | <type_opt>)
<a_ttl> ::= 0 <bit>{7} <byte>{3}
<a_rd_length> ::= <byte>{2} := pack(">H", randint(0, 0))
<a_rdata> ::= <byte>

<type_id_a> ::= 0{15} 1
<type_id_ns> ::= 0{14} 1 0
<type_id_soa> ::= 0{13} 1 1 0
<type_id_cname> ::= 0{13} 1 0 1
<type_id_opt> ::= 0{10} 1 0 1 0 0 1
<type_a> ::= <type_id_a> <rr_class> <a_ttl> 0{13} 1 0 0 <byte>{4}
<type_ns> ::= <type_id_ns> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_soa> ::= <type_id_soa> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_opt> ::= <type_id_opt> <udp_payload_size> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_cname> ::= <type_id_cname> <rr_class> <a_ttl> <a_rd_length> <q_name>
<udp_payload_size> ::= <bit>{16}

where forall <t> in <type_cname>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<q_name>)))


class UdpTcpProtocolDecorator(UdpTcpProtocolDecorator):
    def on_send(self, message: DerivationTree, recipient: Optional[str]):
        compress_msg(message.to_bytes())
        super().on_send(message, recipient)

class ConnectParty(ConnectParty):
    def receive_msg(self, sender: Optional[str], message: str | bytes) -> None:
        super().receive_msg(sender, decompress_msg(message))


class Client(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY if fandango_is_client else Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT,
            uri="udp://localhost:53"
        )
        self.start()

class Server(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY if not fandango_is_client else Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.OPEN,
            uri="udp://localhost:25565"
        )
        self.start()
