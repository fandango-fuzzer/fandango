from faker import Faker
fake = Faker()

def gen_q_name():
    result = b''
    domain_parts = fake.domain_name().split('.')
    for part in domain_parts:
        result += len(part).to_bytes(1, 'big')
        result += part.encode('iso8859-1')
    result += b'a' #Todo Workaround of byte parsing bug. Remove when resolved.
    return result


<start> ::= <dns_req> <dns_resp>
<dns_req> ::= <header_req> <question>
<dns_resp> ::= <header_resp> <answer>
#                       qr      opcode       aa tc rd  ra z ad cd rcode   qdcount  ancount nscount arcount
<header_req> ::= <h_id> 0 <h_opcode_standard> 1 0 <h_rd> 0 0 0 0 <h_rcode_none> 0{15} 1 0{16} 0{16} 0{16}
<header_resp> ::= <h_id> 1 <h_opcode_standard> 1 0 <h_rd> 0 0 0 0 <h_rcode_none> 0{16} 0{15} 1 0{16} 0{16}

where <dns_req>.<header_req>.<h_rd> == <dns_resp>.<header_resp>.<h_rd>
where <dns_req>.<header_req>.<h_id> == <dns_resp>.<header_resp>.<h_id>
where <dns_req>.<question>.<q_name> == <dns_resp>.<answer>.<q_name>


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



<question> ::= <q_name> 0{8} <q_type> <q_class>
<q_name> ::= <byte>+ := gen_q_name()
<q_name_entry> ::= <byte>+
<q_type> ::= 0{15} 1
<q_class> ::= 0{15} 1

<answer> ::= <q_name> <a_type> <a_class> <a_ttl> <a_rd_length> <a_rdata>
<a_type> ::= 0 0 0 1 # Equals type A (Host address)
<a_class> ::= 0 0 0 1 # Equals class IN (Internet)
<a_ttl> ::= <byte>{2}
<a_rd_length> ::= 0 1 0 0  # Equals 4
<a_rdata> ::= <ip_address>
<ip_address> ::= <byte>{4}
