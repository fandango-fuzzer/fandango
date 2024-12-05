
def gen_dns_for_name_field():
    from faker import Faker
    fake = Faker()
    names = fake.domain_name().split('.')
    result = ""
    for name in reversed(names):
        result += str(len(name)) + name
    return result


<start> ::= <dns_req>;
<dns_req> ::= <header_req> <question>;
<header_req> ::= <h_id> <h_qr_query> <h_opcode_standard> <h_tc> <h_rd> <h_ra> <h_z> <h_rcode> <h_qd_count> <h_an_count> <h_ns_count> <h_ar_count>;
<h_qr_query> ::= '0';
<h_qr_resp> ::= '1';
<h_opcode> ::= <h_opcode_standard> | <h_opcode_inverse> | <h_opcode_status_req> | <h_opcode_other>;
<h_opcode_standard> ::= '0000';
<h_opcode_inverse> ::= '0001';
<h_opcode_status_req> ::= '0010';
<h_opcode_other> ::= <bit>{4, 4};
<h_tc> ::= <bit>;
<h_rd> ::= <bit>;
<h_ra> ::= <bit>;
<h_z> ::= '0';
<h_rcode> ::= <h_rcode_none> | <h_rcode_format> | <h_rcode_server> | <h_rcode_name> | <h_rcode_ni> | <h_rcode_refused> | <h_rcode_other>;
<h_rcode_none> ::= '0x0';
<h_rcode_format> ::= '0x1';
<h_rcode_server> ::= '0x2';
<h_rcode_name> ::= '0x3';
<h_rcode_ni> ::= '0x4';
<h_rcode_refused> ::= '0x5';
<h_rcode_other> ::= '0x' <hex>;
<h_qd_count> ::= '0x0001';
<h_an_count> ::= '0x0000';
<h_ns_count> ::= '0x0000';
<h_ar_count> ::= '0x0000';
<h_id> ::= '0x' <hex_byte> <hex_byte>;
<bit> ::= '0' | '1';
<byte> ::= <bit>{8, 8};
<hex_byte> ::= <hex> <hex>;
<hex> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f';
<question> ::= <q_name> <q_type> <q_class>;
<q_name> ::= <q_name_content> '0x00';
<q_name_content> ::= <q_name_entry>+ :: gen_dns_for_name_field();
<q_name_entry> ::= <name_length> <name>;
<name> ::= <letter>+ ('-' <letter>+)*;
<letter> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z';
<name_length> ::= <number_start> <number>*;
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';
<number> ::= '0' | <number_start>;
<q_type> ::= '0x0001';
<q_class> ::= '0x0001';
<answer> ::= <q_name> <a_type> <a_class> <a_ttl> <a_rd_length> <a_rdata>;
<a_type> ::= '0x0001';
<a_class> ::= '0x0001';
<a_ttl> ::= <byte>{2, 2};
<a_rd_length> ::= <byte>{2, 2};
<a_rdata> ::= <ip_address>;
<ip_address> ::= <ip_address_sequence> '.' <ip_address_sequence> '.' <ip_address_sequence>;
<ip_address_sequence> ::= <number> | <number_start> <number>{0, 2};

int(str(<h_rcode_other>), 16) > 5;
int(str(<h_opcode_other>), 2) > 2;
int(str(<a_rd_length>), 2) == len(<a_rdata>);
int(str(<answer>.<a_rd_length>), 2) == len(<answer>.<a_rdata>);
int(<ip_address_sequence>) <= 255;
int(<q_name_entry>.<name_length>) == len(<q_name_entry>.<name>);