from struct import unpack
from faker import Faker
fake = Faker()

def gen_q_name():
    result = b''
    #domain_parts = fake.domain_name().split('.')
    domain_parts = "fandango.io".split('.')
    for part in domain_parts:
        result += len(part).to_bytes(1, 'big')
        result += part.encode('iso8859-1')
    return result


<start> ::= <Client:dns_req> <Server:dns_resp>
<dns_req> ::= <header_req> <question>
<dns_resp> ::= <header_resp> <question> <answer>+

#                       qr      opcode       aa tc rd  ra  z      rcode   qdcount  ancount nscount arcount
<header_req> ::= <h_id> 0 <h_opcode_standard> 1 0 <h_rd> 0 0 0 0 <h_rcode_none> 0{15} 1 0{16} 0{16} 0{16}
<header_resp> ::= <h_id> 1 <h_opcode_standard> <bit> 0 <h_rd> <bit> 0 0 0 <h_rcode_none> <resp_qd_count> <resp_an_count> <resp_ns_count> <resp_ar_count>
# aa=1 if server has authority over domain

where <dns_req>.<header_req>.<h_rd> == <dns_resp>.<header_resp>.<h_rd>
where <dns_req>.<header_req>.<h_id> == <dns_resp>.<header_resp>.<h_id>
where <dns_req>.<question>.<q_name>.<q_name_written_complete> == <dns_resp>.<answer>.<q_name>.<q_name_written_complete>
where <dns_req>.<question> == <dns_resp>.<question>
where unpack('>H', bytes(<dns_resp>.<header_resp>.<resp_qd_count>))[0] == len((<dns_resp>).find_direct_trees(NonTerminal("<question>"))) # count nr of questions
where (unpack('>H', bytes(<dns_resp>.<header_resp>.<resp_an_count>))[0] + unpack('>H', bytes(<dns_resp>.<header_resp>.<resp_ns_count>))[0] + unpack('>H', bytes(<dns_resp>.<header_resp>.<resp_ar_count>))[0]) == len((<dns_resp>).find_direct_trees(NonTerminal("<answer>"))) # count nr of answers
<resp_qd_count> ::= 0{15} 1
<resp_an_count> ::= 0{15} 1
<resp_ns_count> ::= 0{15} <bit>
<resp_ar_count> ::= 0{15} <bit>

where forall <req> in <dns_req>:
    forall <n1> in <req>..<q_name_written_complete>:
        get_index_within(<n1>, <req>, ['<q_name_written_complete>', '<q_name_written_partly>', '<q_name_written_pointer>']) == 0

where forall <req> in <dns_req>:
    forall <n2> in <req>..<q_name_written_pointer>:
        get_index_within(<n2>, <req>, ['<q_name_written_complete>', '<q_name_written_partly>', '<q_name_written_pointer>']) != 0

where forall <req> in <dns_req>:
    forall <n3> in <req>..<q_name_written_partly>:
        get_index_within(<n3>, <req>, ['<q_name_written_complete>', '<q_name_written_partly>', '<q_name_written_pointer>']) != 0



<h_id> ::= <byte><byte>
<h_opcode_standard> ::= 0 0 0 0
<h_rd> ::= <bit>
<h_qr> ::= <bit>

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
<q_name> ::= <q_name_written_complete> | <q_name_written_partly> | <q_name_written_pointer>
<offset_qname> ::= 1 1 <bit>{14}
<q_name_written_complete> ::= <q_name_written> 0{8}
<q_name_written_partly> ::= <q_name_written> <offset_qname>
<q_name_written_pointer> ::= <offset_qname>
<q_name_written> ::= <label_len_octet> <non_zero_byte>+ := gen_q_name()
<q_type> ::= 0{15} 1 # Equals type A (Host address)
<rr_class> ::= 0{15} 1 # Equals class IN (Internet)


<answer> ::= <q_name> <a_type> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<a_type> ::= <type_a> | <type_ns>
<a_ttl> ::= <byte>{4}
<a_rd_length> ::= <byte>{2}
<a_rdata> ::= <byte>


<type_a> ::= 0{15} 1
<type_ns> ::= 0{14} 1 0


import socket
class Client(FandangoAgent):
        def __init__(self):
            super().__init__(True)

        def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message, ("liggesmeyer.net", 53))
            response, nothing = sock.recvfrom(1024)

            response_setter("Server", response)

class Server(FandangoAgent):

        def __init__(self):
            super().__init__(False)