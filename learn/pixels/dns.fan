<start> ::= <dns_req role='client'> <dns_resp role='server'>
<dns_req> ::= <header_req> <question> <answer> <authority> <additional>
<dns_header_req> ::= <h_id> <h_qr_query> <h_opcode_standard> <h_tc> <h_rd> <h_ra> <h_z> <h_rcode> <h_qd_count> <h_an_count> <h_ns_count> <h_ar_count>
<h_qr_query> ::= '0'
<h_qr_resp> ::= '1'
<h_opcode> ::= <h_opcode_standard> | <h_opcode_inverse> | <h_opcode_status_req> | <h_opcode_other>
<h_opcode_standard> ::= '0000'
<h_opcode_inverse> ::= '0001'
<h_opcode_status_req> ::= '0010'
<h_opcode_other> ::= <bit>{4, 4}
<h_tc> ::= <bit>
<h_rd> ::= <bit>
<h_ra> ::= <bit>
<h_z> ::= '0'
<h_rcode> ::= <h_rcode_none> | <h_rcode_format> | <h_rcode_server> | <h_rcode_name> | <h_rcode_ni> | <h_rcode_refused> | <h_rcode_other>
<h_rcode_none> ::= '0000'
<h_rcode_format> ::= '0001'
<h_rcode_server> ::= '0010'
<h_rcode_name> ::= '0011'
<h_rcode_ni> ::= '0100'
<h_rcode_refused> ::= '0101'
<h_rcode_other> ::= <bit>{4, 4}
<h_qd_count> ::= <bit>{16, 16}
<h_an_count> ::= <bit>{16, 16}
<h_ns_count> ::= <bit>{16, 16}
<h_ar_count> ::= <bit>{16, 16}
<h_id> ::= <bit>{16, 16}
<bit> ::= '0' | '1'
<byte> ::= <bit>{8, 8}
<hex_byte> ::= '0x' <hex> <hex>
<hex> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' |

<question> ::= <q_name> <q_type> <q_class>
<q_name> ::= <q_name_entry>+ '0x00'
<q_name_entry> ::= <name_length> <name>
<name> ::= <letter>+
<letter> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
<name_length> ::= <number_start> <number>
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number> ::= '0' | <number_start>
<q_type> ::= '0x0001'
<q_class> ::= '0x0001'

int('0b' + <h_rcode_other>) > 5
int('0b' + <h_opcode_other>) > 2
int(<q_name_entry>.<name_length>) == len(<q_name_entry>.<name>)

role_server = tcp://192.168.0.1:25511
role_client = self