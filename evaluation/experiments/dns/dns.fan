from faker import Faker
fake = Faker()

def gen_q_name():
    result = b''
    domain_parts = fake.domain_name().split('.')
    for part in domain_parts:
        result += len(part).to_bytes(1, 'big')
        result += part.encode('iso8859-1')
    return result


<start> ::= <dns_req>
<dns_req> ::= <header_req> <question>*
#                       qr      opcode       aa tc rd    ra z     rcode   qdcount  ancount nscount arcount
<header_req> ::= <h_id> 0 <h_opcode_standard> 0 0 <h_rd> 0 0{4} <h_rcode> 0{15} 1 0{16} 0{16} 0{16}
<h_id> ::= <byte><byte>
<h_opcode_standard> ::= 0 0 0 0
<h_rd> ::= <bit>

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
<q_name> ::= <q_name_entry> :: gen_q_name()
<q_name_entry> ::= <bit>+
<name_length> ::= <bit>{8}
<name> ::= <bit>+
<q_type> ::= 0{15} 1
<q_class> ::= 0{15} 1
#<answer> ::= <q_name> <a_type> <a_class> <a_ttl> <a_rd_length> <a_rdata>
#<a_type> ::= 0 0 0 1
#<a_class> ::= 0 0 0 1
#<a_ttl> ::= <byte>{2, 2}
#<a_rd_length> ::= <byte>{2, 2}
#<a_rdata> ::= <ip_address>
#<ip_address> ::= <ip_address_sequence> '.' <ip_address_sequence> '.' <ip_address_sequence>
#<ip_address_sequence> ::= <number> | <number_start> <number>{0, 2}
