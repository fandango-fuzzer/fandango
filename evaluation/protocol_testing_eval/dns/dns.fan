from struct import unpack, pack
from faker import Faker
from fandango.language.symbols import NonTerminal
from random import randint

fake = Faker()

fandango_is_client = True
# If uses as a client interact with a command like this:
# dig @127.0.0.1 -p 25565 A fandango.io +noedns +time=100 +tries=1


# This function gets a question and the response section of a DNS response and verifies if the response does answer the question.
# This also handles responses that are transitive. For example if the question is for a type A record for "example.com" and the response contains
# a CNAME record pointing "example.com" to "alias.com" and then an A record for "alias.com", this function will verify that the response correctly
# answers the original question through the CNAME redirection.
def verify_transitive(question, response):
    type_byte = bytes(question.find_direct_trees(NonTerminal("<q_type>"))[0])
    allowed_names = [bytes(question.find_direct_trees(NonTerminal("<q_name>"))[0])]
    for ans in response.find_all_trees(NonTerminal("<answer_an>")):
        if bytes(ans.children[1])[0:2] == pack('>H', 5) and bytes(ans.find_direct_trees(NonTerminal("<q_name_optional>"))[0]) in allowed_names:
            allowed_names.append(bytes(ans.children[1].children[0].children[4])) # <type_cname>.<q_name>
    for ans in response.find_all_trees(NonTerminal("<answer_an>")):
        if bytes(ans.children[1])[0:2] == type_byte and bytes(ans.find_direct_trees(NonTerminal("<q_name_optional>"))[0]) in allowed_names:
            return True
    return False


# Generate a random domain name. We either generate a domain name using the Faker library, which likely is not known to the DNS server,
# or we use 'github.com' or 'cispa.de' which should be known to the DNS server.
def gen_q_name():
    result = b''
    rand = randint(0, 2)

    if rand == 0:
        domain_name = 'github.com'
    elif rand == 1:
        domain_name = 'cispa.de'
    else:
        domain_name = fake.domain_name()

    domain_parts = domain_name.split('.')
    for part in domain_parts:
        result += len(part).to_bytes(1, 'big')
        result += part.encode('iso8859-1')

    return result

# Convert a 2-byte byte array to an integer
def byte_to_int(byte_val):
    return int(unpack('>H', bytes(byte_val))[0])

# Generates a list of tuples, for a DNS name containing an entry for each zone present in it including the offset to that zone within the DNS name.
# Example msg_suffix(b'\x08fandango\x02io\x00') would result in [(0, b'\x08fandango\x02io\x00'), (9, b'\x02io\x00')]
def msg_suffix(name):
    suffixes = []
    len_idx = 0
    prefix_len = name[len_idx]
    while prefix_len != 0:
        suffixes.append((len_idx, name[len_idx:]))
        len_idx = len_idx + prefix_len + 1
        prefix_len = name[len_idx]
    return suffixes

# Applies the DNS name compression algorithm to a DNS name starting at curr_idx within the uncompressed message.
# suffix dict is a dictionary mapping known DNS suffix names to their offsets within the already analyzed compressed part of the message.
def compress_name(uncompressed: bytes, curr_idx: int,
                  len_reduction: int, suffix_dict: dict[bytes, int]) -> tuple[bytes, int, int]:
    """
    Compress a single name in a DNS message.
    :param: uncompressed - the message before compression
    :param: curr_idx - the current index in `compress_msg()` (see below)
    :param: len_reduction - how many bytes we already have compressed
    :param: suffix_dict - the suffixes encoded so far
    :return: a tuple (new_name, length, len_reduction) - the compressed name, its length, the new length reduction
    """
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

# Compresses a full DNS message applying the DNS name compression algorithm to all names present in the message.
def compress_msg(uncompressed: bytes) -> bytes:
    """
    Compress a single DNS message.
    """
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

# Decompresses a DNS name starting at name_idx within the compressed message.
def decompress_name(compressed: bytes, name_idx: int) -> tuple[bytes, int]:
    """
    Decompress the package `compressed` at the current index `name_idx` of a name.
    :param: compressed - the package to be decompressed
    :param: name_idx - the index of a name in `compressed`
    :returns: a pair (decompressed, length) - the decompressed package and its length increase
    """
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

# Decompresses a full DNS message applying the DNS name decompression algorithm to all names present in the message.
def decompress_msg(compressed: bytes) -> bytes:
    """
    Decompress the DNS message `compressed`.
    :param: compressed - the compressed DNS message
    :returns: the decompressed DNS message.
    """
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
        else:
            decompressed += compressed[curr_idx-2:curr_idx]
            decompressed += compressed[curr_idx:curr_idx+r_data_len]
            curr_idx += r_data_len

    return decompressed




<start> ::= <exchange>

# Each exchange consists of a request made by the client and a response from the server.
<exchange> ::= <Client:dns_req> <Server:dns_resp>

# A request consists of a header and a number of questions and answers as specified in the header
<dns_req> ::= <header_req> <question>{byte_to_int(<req_qd_count>)}
<dns_resp> ::= <header_resp> <question_section> <answer_an_section> <answer_au_section> <answer_opt_section>

<question_section> ::= <question>{byte_to_int(<header_req>.<req_qd_count>)}
<answer_an_section> ::= <answer_an>{byte_to_int(<resp_an_count>)}
<answer_au_section> ::= <answer_au>{byte_to_int(<resp_ns_count>)}
<answer_opt_section> ::= <answer_opt>{byte_to_int(<resp_ar_count>)}

#                       qr      opcode       aa tc rd  ra  z      rcode   qdcount  ancount nscount arcount
<header_req> ::= <h_id> 0 <h_opcode_standard> 0 0 <h_rd> 0 0 <bit> 0 <h_rcode_noerror> <req_qd_count> 0{16} 0{16} 0{16}
<header_resp> ::= <h_id> 1 <h_opcode_standard> <bit> 0 <h_rd> <h_ra> 0 <h_aa> 0 (<h_rcode_noerror> | <h_rcode_nxdomain>) <resp_qd_count> <resp_an_count> <resp_ns_count> <resp_ar_count>
# aa=1 if server has authority over domain

# Ensures that for each request/response pair the following parts match:
# The recursion desired flag (RD) (<h_rd>)
# The DNS message identifier (ID) (<h_id>)
# The question that the response aims to answer is the same as the question in the request (<question>)
# The question count in the response matches the question count in the request (<req_qd_count>)
# Counted as 4 constraints
where forall <ex> in <start>.<exchange>:
    <ex>.<dns_resp>.<header_resp>.<h_rd> == <ex>.<dns_req>.<header_req>.<h_rd> and <ex>.<dns_resp>.<header_resp>.<h_id> == <ex>.<dns_req>.<header_req>.<h_id> and <ex>.<dns_resp>.<question_section>.<question> == <ex>.<dns_req>.<question> and bytes(<ex>.<dns_resp>.<header_resp>.<resp_qd_count>) == bytes(<ex>.<dns_req>.<header_req>.<req_qd_count>)


<req_qd_count> ::= <byte>{2} := pack(">H", 1)
<resp_qd_count> ::= <bit>{16} := pack(">H", 1)
<resp_an_count> ::= <bit>{16} := pack(">H", randint(1, 2))
<resp_ns_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<resp_ar_count> ::= <bit>{16} := pack(">H", randint(0, 2))

# Unused
# <req_ar_count> ::= <bit>{16} := pack(">H", randint(0, 0))

<h_id> ::= <byte><byte>
<h_opcode_standard> ::= 0 0 0 0
<h_rd> ::= 1 # 0 causes server failure with cname
<h_aa> ::= <bit>
<h_ra> ::= <bit>

<h_rcode> ::= <h_rcode_noerror> | <h_rcode_formerr> | <h_rcode_servfail> | <h_rcode_nxdomain> | <h_rcode_notimp> | <h_rcode_refused> | <h_rcode_other>
<h_rcode_noerror>  ::= 0 0 0 0  # NOERROR - no error
<h_rcode_formerr>  ::= 0 0 0 1  # FORMERR - format error
<h_rcode_servfail> ::= 0 0 1 0  # SERVFAIL - server failure
<h_rcode_nxdomain> ::= 0 0 1 1  # NXDOMAIN - non existent domain
<h_rcode_notimp>   ::= 0 1 0 0  # NOTIMP - not implemented
<h_rcode_refused>  ::= 0 1 0 1  # REFUSED - query refused
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

# Checks if a dns response answers the corresponding dns question using the verify_transitive-function.
# The second part of the `or` clause `bytes(<a>.<answer_an_type>)[0:2]...` also checks this, but only for direct answers without allowing transitive response chains.
# This allows Fandango optimizations to be used to generate a valid answer more efficiently.
# Counted as 2 constraints
where forall <ex> in <start>.<exchange>:
    forall <a> in <ex>.<dns_resp>.<answer_an_section>.<answer_an>:
        exists <q> in <ex>.<dns_req>.<question>:
            verify_transitive(<q>, <ex>.<dns_resp>) or bytes(<a>.<answer_an_type>)[0:2] == bytes(<q>.<q_type>) and bytes(<a>.<q_name_optional>) == bytes(<q>.<q_name>)

<answer_au> ::= <q_name_optional> <type_soa>
<answer_opt> ::= <q_name_optional> (<type_opt>|<type_a>|<type_aaaa>)
<answer_an> ::= <q_name_optional> <answer_an_type>
<a_ttl> ::= 0 <bit>{7} <byte>{3}
<a_rd_length> ::= <byte>{2} := pack(">H", randint(0, 0))
<a_rdata> ::= <byte>
<answer_an_type> ::= (<type_a> |<type_cname> | <type_ns>)

<type_id_a> ::= 0{15} 1
<type_id_ns> ::= 0{14} 1 0
<type_id_soa> ::= 0{13} 1 1 0
<type_id_cname> ::= 0{13} 1 0 1
<type_id_opt> ::= 0{10} 1 0 1 0 0 1
<type_id_aaaa> ::= 0{11} 1 1 1 0 0
<type_a> ::= <type_id_a> <rr_class> <a_ttl> 0{13} 1 0 0 <ip_address>
<type_aaaa> ::= <type_id_aaaa> <rr_class> <a_ttl> 0{11} 1 0 0 0 0 <ip_address_v6>
<ip_address> ::= <byte>{4}
<ip_address_v6> ::= <byte>{16}
<type_ns> ::= <type_id_ns> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_soa> ::= <type_id_soa> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_opt> ::= <type_id_opt> <udp_payload_size> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_cname> ::= <type_id_cname> <rr_class> <a_ttl> <a_rd_length> <q_name>
<udp_payload_size> ::= <bit>{16}

# <type_cname> responses must have the correct length in the <a_rd_length> field (r data length), which corresponds to the following <q_name> field.
# Counted as one constraint
where forall <t> in <type_cname>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<q_name>)))



class NetworkParty(NetworkParty):
    # We want all sent messages to be compressed and all received messages to be decompressed for all parties.
    # Therefore we override the send and the receive functions in the base NetworkParty class.
    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(decompress_msg(message), sender)

    def send(self, message: str | bytes, recipient: Optional[str]) -> None:
        if isinstance(message, DerivationTree):
            message = message.to_bytes(encoding="utf-8")
        super().send(compress_msg(message), recipient)


# If we do not specify --client or --server, these are the default settings:
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT if fandango_is_client else ConnectionMode.EXTERNAL,
            uri="udp://127.0.0.1:25566"
        )
        self.start()


class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.OPEN if not fandango_is_client else ConnectionMode.EXTERNAL,
            uri="udp://localhost:25565"
        )
        self.start()
