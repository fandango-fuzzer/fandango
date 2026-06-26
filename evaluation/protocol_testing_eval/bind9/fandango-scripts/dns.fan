from struct import unpack, pack
from faker import Faker
from fandango.language.symbols import NonTerminal
from random import randint, choice

fake = Faker()

fandango_is_client = False
# If used as a client interact with a command like this:
# dig @127.0.0.1 -p 25566 A fandango.io +noedns +time=100 +tries=1


# DNS record type numbers.
TYPE_A = 1
TYPE_NS = 2
TYPE_CNAME = 5
TYPE_SOA = 6
TYPE_PTR = 12
TYPE_MX = 15
TYPE_TXT = 16
TYPE_AAAA = 28
TYPE_SRV = 33
TYPE_OPT = 41

# RR types whose RDATA contains a single domain name at a fixed offset.
# The value is the number of fixed bytes preceding that name.
SINGLE_NAME_PREFIX = {
    TYPE_NS: 0,
    TYPE_CNAME: 0,
    TYPE_PTR: 0,
    TYPE_MX: 2,    # 2-byte preference, then exchange name
    TYPE_SRV: 6,   # priority(2) weight(2) port(2), then target name
}


# This function gets a question and the response section of a DNS response and verifies if the response does answer the question.
# This also handles responses that are transitive. For example if the question is for a type A record for "example.com" and the response contains
# a CNAME record pointing "example.com" to "alias.com" and then an A record for "alias.com", this function will verify that the response correctly
# answers the original question through the CNAME redirection.
def verify_transitive(question, response):
    type_byte = bytes(question.find_direct_trees(NonTerminal("<q_type>"))[0])
    allowed_names = [bytes(question.find_direct_trees(NonTerminal("<q_name>"))[0])]
    for ans in response.find_subtrees("<answer_an>"):
        if bytes(ans.children[1])[0:2] == pack('>H', TYPE_CNAME) and bytes(ans.find_direct_trees(NonTerminal("<q_name_optional>"))[0]) in allowed_names:
            allowed_names.append(bytes(ans.children[1].children[0].children[4])) # <type_cname>.<q_name>
    for ans in response.find_subtrees("<answer_an>"):
        if bytes(ans.children[1])[0:2] == type_byte and bytes(ans.find_direct_trees(NonTerminal("<q_name_optional>"))[0]) in allowed_names:
            return True
    return False


def response_not_answering(response) -> bool:
    return not any(True for _ in response.find_subtrees("<h_rcode_noerror>"))

# Generate a domain name to query. We mix names the local server is authoritative for with public
# domains it must recurse for; some of them CNAME elsewhere, exercising the client's CNAME-chain parsing.
def gen_q_name():
    result = b''
    domain_name = choice([
        'example.com', 'mail.example.com', 'www.example.com', '_sip._tcp.example.com',
        '1.0.0.127.in-addr.arpa', 'doesnotexist.example.com',
        'test.example.com', 'www.github.com', 'www.wikipedia.org',
        'github.com', 'google.com', 'example.com', 'cloudflare.com',
        'wikipedia.org', 'amazon.com',
    ])

    domain_parts = domain_name.split('.')
    for part in domain_parts:
        result += len(part).to_bytes(1, 'big')
        result += part.encode('iso8859-1')

    return result


# Generate a length-prefixed character-string for use inside TXT RDATA.
def gen_txt_string():
    s = fake.sentence(nb_words=randint(1, 4)).encode('iso8859-1')[:255]
    return len(s).to_bytes(1, 'big') + s


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


# Compresses a resource record's RDATA, compressing the embedded name(s) of name-bearing types.
def compress_rdata(uncompressed: bytes, rr_type: int, curr_idx: int,
                   r_data_len: int, len_reduction: int,
                   suffix_dict: dict[bytes, int]) -> tuple[bytes, int, int]:
    if rr_type in SINGLE_NAME_PREFIX:
        prefix = SINGLE_NAME_PREFIX[rr_type]
        out = uncompressed[curr_idx:curr_idx + prefix]
        name, name_len, len_reduction = compress_name(
            uncompressed, curr_idx + prefix, len_reduction, suffix_dict)
        out += name
        return out, prefix + name_len, len_reduction

    if rr_type == TYPE_SOA:
        # MNAME, RNAME, then 20 bytes of serial/refresh/retry/expire/minimum.
        mname, mlen, len_reduction = compress_name(
            uncompressed, curr_idx, len_reduction, suffix_dict)
        rname, rlen, len_reduction = compress_name(
            uncompressed, curr_idx + mlen, len_reduction, suffix_dict)
        tail = uncompressed[curr_idx + mlen + rlen:curr_idx + mlen + rlen + 20]
        return mname + rname + tail, mlen + rlen + 20, len_reduction

    # Default: verbatim RDATA (A, AAAA, TXT, OPT, ...).
    return uncompressed[curr_idx:curr_idx + r_data_len], r_data_len, len_reduction


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

        new_rdata, decompressed_rdata_len, len_reduction = compress_rdata(
            uncompressed, rr_type, curr_idx, r_data_len, len_reduction, suffix_dict)
        compressed += pack('>H', len(new_rdata))
        compressed += new_rdata
        curr_idx += decompressed_rdata_len

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


# Decompresses a resource record's RDATA, expanding compression pointers in name-bearing types.
def decompress_rdata(compressed: bytes, rr_type: int, curr_idx: int,
                     r_data_len: int) -> tuple[bytes, int]:
    if rr_type in SINGLE_NAME_PREFIX:
        prefix = SINGLE_NAME_PREFIX[rr_type]
        out = compressed[curr_idx:curr_idx + prefix]
        name, clen = decompress_name(compressed, curr_idx + prefix)
        return out + name, prefix + clen

    if rr_type == TYPE_SOA:
        mname, mlen = decompress_name(compressed, curr_idx)
        rname, rlen = decompress_name(compressed, curr_idx + mlen)
        tail = compressed[curr_idx + mlen + rlen:curr_idx + mlen + rlen + 20]
        return mname + rname + tail, mlen + rlen + 20

    return compressed[curr_idx:curr_idx + r_data_len], r_data_len


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

        new_rdata, compressed_rdata_len = decompress_rdata(
            compressed, rr_type, curr_idx, r_data_len)
        decompressed += pack('>H', len(new_rdata))
        decompressed += new_rdata
        curr_idx += compressed_rdata_len

    return decompressed




<start> ::= <exchange>

# Each exchange consists of a request made by the client and a response from the server.
<exchange> ::= <Client:dns_req> <Server:dns_resp>

# A request consists of a header, QDCOUNT questions and an optional EDNS0 OPT record in the additional section.
# A response consists of a header, the echoed question section, an answer, an authority and an additional section.
<dns_req> ::= <header_req> <question>{byte_to_int(<req_qd_count>)} <req_additional_section>
<dns_resp> ::= <header_resp> <question_section> <answer_an_section> <answer_au_section> <answer_opt_section>

<req_additional_section> ::= <answer_opt>{byte_to_int(<header_req>.<req_ar_count>)}
# Sized by the response's own QDCOUNT, so replies that echo no question still parse.
<question_section> ::= <question>{byte_to_int(<header_resp>.<resp_qd_count>)}
<answer_an_section> ::= <answer_an>{byte_to_int(<resp_an_count>)}
<answer_au_section> ::= <answer_au>{byte_to_int(<resp_ns_count>)}
<answer_opt_section> ::= <answer_opt>{byte_to_int(<resp_ar_count>)}

#                       qr      opcode       aa tc rd  ra  z      rcode   qdcount  ancount nscount arcount
<header_req> ::= <h_id> 0 <h_opcode_req> 0 0 <h_rd> 0 0 <bit> 0 <h_rcode_noerror> <req_qd_count> 0{16} 0{16} <req_ar_count>
<header_resp> ::= <h_id> 1 <h_opcode_req> <h_tc> 0 <h_resp_rd> <resp_flags_lo> <resp_qd_count> <resp_an_count> <resp_ns_count> <resp_ar_count>
# Low byte of the response flags: RA, Z, AA, a reserved 0, then the 4-bit RCODE. The generator forces
# RCODE to NOERROR while randomising RA/Z/AA; parsing still accepts any RCODE.
<resp_flags_lo> ::= <h_ra> <bit> <h_aa> 0 <h_rcode_resp> := pack("B", (choice([0,1])<<7)|(choice([0,1])<<6)|(choice([0,1])<<5))
# aa=1 if server has authority over domain

# For each request/response pair the DNS message identifier (ID) matches.
# Counted as 1 constraint
where forall <ex> in <start>.<exchange>:
    <ex>.<dns_resp>.<header_resp>.<h_id> == <ex>.<dns_req>.<header_req>.<h_id>

# Response/request coupling constraints. They live in the shared grammar and apply UNCONDITIONALLY
# in both modes: in server mode they shape the response Fandango generates; in client mode they act
# as an oracle on the real server's reply (a reply that violates them is recorded as a violation).

# QDCOUNT + opcode + full question echo (the response copies the request's values).
where forall <ex> in <start>.<exchange>:
    bytes(<ex>.<dns_resp>.<header_resp>.<resp_qd_count>) == bytes(<ex>.<dns_req>.<header_req>.<req_qd_count>) and <ex>.<dns_resp>.<header_resp>.<h_opcode_req> == <ex>.<dns_req>.<header_req>.<h_opcode_req> and <ex>.<dns_resp>.<question_section>.<question> == <ex>.<dns_req>.<question>

# Each answer RR answers a question. But only when the server actually answers (RCODE == NOERROR).
# Counted as 2 constraints
where forall <ex> in <start>.<exchange>:
    forall <a> in <ex>.<dns_resp>.<answer_an_section>.<answer_an>:
        exists <q> in <ex>.<dns_req>.<question>:
            response_not_answering(<ex>.<dns_resp>) or verify_transitive(<q>, <ex>.<dns_resp>) or bytes(<a>.<answer_an_type>)[0:2] == bytes(<q>.<q_type>) and bytes(<a>.<q_name_optional>) == bytes(<q>.<q_name>)


# Mostly single-question requests; two-question packets still occur to exercise multi-question handling.
<req_qd_count> ::= <byte>{2} := pack(">H", choice([1, 1, 1, 2]))
# 0 or 1 EDNS0 OPT record in the request's additional section.
<req_ar_count> ::= <bit>{16} := pack(">H", choice([0, 0, 1]))

# Server generation emits one question, one answer, no authority/additional records. When parsing a
# real reply the counts are read from the wire, so this does not restrict validation.
<resp_qd_count> ::= <bit>{16} := pack(">H", 1)
<resp_an_count> ::= <bit>{16} := pack(">H", 1)
<resp_ns_count> ::= <bit>{16} := pack(">H", 0)
<resp_ar_count> ::= <bit>{16} := pack(">H", 0)

<h_id> ::= <byte><byte>

# QUERY is listed multiple times so generation favours it; STATUS/NOTIFY still occur to drive their handlers.
<h_opcode_req> ::= <h_opcode_query> | <h_opcode_query> | <h_opcode_query> | <h_opcode_query> | <h_opcode_status> | <h_opcode_notify>
<h_opcode_query>  ::= 0 0 0 0   # QUERY (0)
<h_opcode_status> ::= 0 0 1 0   # STATUS (2)
<h_opcode_notify> ::= 0 1 0 0   # NOTIFY (4)

<h_rd> ::= 1 # 0 causes server failure with cname
<h_resp_rd> ::= <bit>   # response RD: echoes request RD for QUERY, may be 0 otherwise
<h_aa> ::= <bit>
<h_ra> ::= <bit>
<h_tc> ::= <bit>   # truncation flag

# Full RCODE space, needed to parse real error replies; generation is forced to NOERROR by <resp_flags_lo>.
<h_rcode_resp> ::= <h_rcode_noerror> | <h_rcode_formerr> | <h_rcode_servfail> | <h_rcode_nxdomain> | <h_rcode_notimp> | <h_rcode_refused>
<h_rcode_noerror>  ::= 0 0 0 0  # NOERROR - no error
<h_rcode_formerr>  ::= 0 0 0 1  # FORMERR - format error
<h_rcode_servfail> ::= 0 0 1 0  # SERVFAIL - server failure
<h_rcode_nxdomain> ::= 0 0 1 1  # NXDOMAIN - non existent domain
<h_rcode_notimp>   ::= 0 1 0 0  # NOTIMP - not implemented
<h_rcode_refused>  ::= 0 1 0 1  # REFUSED - query refused
<bit> ::= 0 | 1
<byte> ::= <bit>{8}
<label_len_octet> ::= <byte>


# Questions may ask for any of the common RR types.
<question> ::= <q_name> <q_type> <rr_class>
<q_name_optional> ::= <q_name_written>? 0{8}
<q_name> ::= <q_name_written> 0{8}
<q_name_written> ::= (<label_len_octet> <byte>{byte_to_int(b'\x00' + bytes(<label_len_octet>))})+ := gen_q_name()
# A/CNAME/NS are weighted up to keep the resolver/answer paths busy; the rest still drive their decoders.
<q_type> ::= <type_id_a> | <type_id_a> | <type_id_a> | <type_id_cname> | <type_id_cname> | <type_id_ns> | <type_id_ns> | <type_id_soa> | <type_id_ptr> | <type_id_mx> | <type_id_txt> | <type_id_aaaa> | <type_id_srv>
<rr_class> ::= 0{15} 1 # Equals class IN (Internet)

# Each answer RR is one of the RR-type bodies below, each carrying its own type-correct RDATA.
<answer_an> ::= <q_name_optional> <answer_an_type>
<answer_an_type> ::= <type_a> | <type_aaaa> | <type_ns> | <type_cname> | <type_soa> | <type_mx> | <type_txt> | <type_ptr> | <type_srv>
# Authority section: NS records or the zone SOA.
<answer_au> ::= <q_name_optional> (<type_soa> | <type_ns>)
# Additional section: glue (A/AAAA) or an EDNS0 OPT pseudo-record.
<answer_opt> ::= <q_name_optional> (<type_opt> | <type_a> | <type_aaaa>)

<a_ttl> ::= 0 <bit>{7} <byte>{3}
<a_rd_length> ::= <byte>{2} := pack(">H", randint(0, 0))

# RR type identifiers (16-bit, big endian)
<type_id_a>     ::= 0{15} 1                # 1
<type_id_ns>    ::= 0{14} 1 0              # 2
<type_id_cname> ::= 0{13} 1 0 1            # 5
<type_id_soa>   ::= 0{13} 1 1 0            # 6
<type_id_ptr>   ::= 0{12} 1 1 0 0         # 12
<type_id_mx>    ::= 0{12} 1 1 1 1         # 15
<type_id_txt>   ::= 0{11} 1 0 0 0 0       # 16
<type_id_aaaa>  ::= 0{11} 1 1 1 0 0       # 28
<type_id_srv>   ::= 0{10} 1 0 0 0 0 1     # 33
<type_id_opt>   ::= 0{10} 1 0 1 0 0 1     # 41

# A: 4-byte IPv4 address. RDLENGTH is fixed at 4.
<type_a> ::= <type_id_a> <rr_class> <a_ttl> 0{13} 1 0 0 <ip_address>
# AAAA: 16-byte IPv6 address. RDLENGTH is fixed at 16.
<type_aaaa> ::= <type_id_aaaa> <rr_class> <a_ttl> 0{11} 1 0 0 0 0 <ip_address_v6>
<ip_address> ::= <byte>{4}
<ip_address_v6> ::= <byte>{16}

# NS / PTR / CNAME: RDATA is a single domain name.
<type_ns>    ::= <type_id_ns>    <rr_class> <a_ttl> <a_rd_length> <q_name>
<type_ptr>   ::= <type_id_ptr>   <rr_class> <a_ttl> <a_rd_length> <q_name>
<type_cname> ::= <type_id_cname> <rr_class> <a_ttl> <a_rd_length> <q_name>

# SOA: MNAME RNAME serial refresh retry expire minimum.
<type_soa> ::= <type_id_soa> <rr_class> <a_ttl> <a_rd_length> <soa_rdata>
<soa_rdata> ::= <q_name> <q_name> <byte>{4} <byte>{4} <byte>{4} <byte>{4} <byte>{4}

# MX: 2-byte preference + exchange name.
<type_mx> ::= <type_id_mx> <rr_class> <a_ttl> <a_rd_length> <mx_rdata>
<mx_rdata> ::= <byte>{2} <q_name>

# SRV: priority + weight + port + target name.
<type_srv> ::= <type_id_srv> <rr_class> <a_ttl> <a_rd_length> <srv_rdata>
<srv_rdata> ::= <byte>{2} <byte>{2} <byte>{2} <q_name>

# TXT: a length-prefixed character string.
<type_txt> ::= <type_id_txt> <rr_class> <a_ttl> <a_rd_length> <txt_rdata>
<txt_rdata> ::= <label_len_octet> <byte>{byte_to_int(b'\x00' + bytes(<label_len_octet>))} := gen_txt_string()

# OPT (EDNS0): CLASS carries the UDP payload size, TTL the extended rcode/version/flags. An empty
# option list (RDLENGTH 0) is the common, valid case.
<type_opt> ::= <type_id_opt> <udp_payload_size> <a_ttl> <a_rd_length> <opt_rdata>
<udp_payload_size> ::= <bit>{16} := pack(">H", choice([512, 1232, 4096]))
<opt_rdata> ::= <opt_option>?
<opt_option> ::= <byte>{2} <opt_opt_len> <byte>{byte_to_int(<opt_opt_len>)}
<opt_opt_len> ::= <byte>{2} := pack(">H", randint(0, 4))

# Every name-bearing or variable-length RDATA declares its uncompressed byte length in the
# RDLENGTH (<a_rd_length>) field, which corresponds to the RDATA that follows.
# Counted as one constraint
where forall <t> in <type_cname>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<q_name>)))
# Counted as one constraint
where forall <t> in <type_ns>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<q_name>)))
# Counted as one constraint
where forall <t> in <type_ptr>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<q_name>)))
# Counted as one constraint
where forall <t> in <type_soa>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<soa_rdata>)))
# Counted as one constraint
where forall <t> in <type_mx>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<mx_rdata>)))
# Counted as one constraint
where forall <t> in <type_srv>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<srv_rdata>)))
# Counted as one constraint
where forall <t> in <type_txt>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<txt_rdata>)))
# Counted as one constraint
where forall <t> in <type_opt>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<opt_rdata>)))


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
