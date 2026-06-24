include('dns.fan')

# If used as a client interact with a command like this:
# dig @127.0.0.1 -p 25565 A fandango.io +noedns +time=100 +tries=1

# Fandango plays the server
fandango_is_client = False

# Server-only response constraints. The client wrapper omits them so it can parse real error/CNAME
# replies; here they copy the request's values into the response so Fandango propagates them.

# QDCOUNT + opcode + full question echo.
where forall <ex> in <start>.<exchange>:
    bytes(<ex>.<dns_resp>.<header_resp>.<resp_qd_count>) == bytes(<ex>.<dns_req>.<header_req>.<req_qd_count>) and <ex>.<dns_resp>.<header_resp>.<h_opcode_req> == <ex>.<dns_req>.<header_req>.<h_opcode_req> and <ex>.<dns_resp>.<question_section>.<question> == <ex>.<dns_req>.<question>

# Each answer RR answers a question: either it resolves it transitively (verify_transitive, following
# CNAME chains) or it directly matches the question's RR type and owner name. The chosen RR body
# carries its own type-correct RDATA, so the answer is a well-formed record of the queried type.
# Counted as 2 constraints
where forall <ex> in <start>.<exchange>:
    forall <a> in <ex>.<dns_resp>.<answer_an_section>.<answer_an>:
        exists <q> in <ex>.<dns_req>.<question>:
            verify_transitive(<q>, <ex>.<dns_resp>) or bytes(<a>.<answer_an_type>)[0:2] == bytes(<q>.<q_type>) and bytes(<a>.<q_name_optional>) == bytes(<q>.<q_name>)
