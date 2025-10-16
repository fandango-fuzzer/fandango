from faker import Faker
fake = Faker()

<start> ::= <banner_exchange> <CONNECTION_state>

<banner_exchange> ::= <Server:banner>
<banner> ::= <text> <crlf>

# ---- STATE DEFINITIONS ----
<CONNECTION_state> ::= <CONNECTION_exchanges> <TRANSACTION_state>
<TRANSACTION_state> ::= <TRANSACTION_exchanges> <end_state>
<end_state> ::= <Client:QUIT> <Server:quit_response>

# ---- EXCHANGES ----
<CONNECTION_exchanges> ::= <EHLO_exchange> | <HELO_exchange>
<EHLO_exchange> ::= <Client:EHLO> <Server:ehlo_response>
<HELO_exchange> ::= <Client:HELO> <Server:helo_response>
<TRANSACTION_exchanges> ::= <NOOP_exchange>
<NOOP_exchange> ::= <Client:NOOP> <Server:noop_response>

# ---- CLIENT COMMANDS ----
<EHLO> ::= "EHLO" <space> <domain> <crlf>
<HELO> ::= "HELO" <space> <domain> <crlf>
<NOOP> ::= "NOOP" <crlf>
<QUIT> ::= "QUIT" <crlf>
<domain> ::= r"[a-zA-Z0-9\-\.]+" := str(fake.domain_name())

# ---- SERVER RESPONSES ----
<ehlo_response> ::= <multi_line_positive_response>
<multi_line_positive_response> ::= ("250" ("-" | <space>) <text> <crlf>)+
<helo_response> ::= <positive_response>
<noop_response> ::= <positive_response>
<quit_response> ::= <positive_response>

<positive_response> ::= ("250" | "221") <space> <text> <crlf>

# ---- TERMINALS ----
<space> ::= " "
<crlf> ::= "\r\n"
<text> ::= r"[^\r\n]*"
