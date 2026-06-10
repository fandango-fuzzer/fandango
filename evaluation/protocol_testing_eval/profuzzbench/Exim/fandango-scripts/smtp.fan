import base64
import random
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def format_date(unix_time):
    dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

def encode64(s):
    return base64.b64encode(str(s).encode("utf-8")).decode("utf-8")

def bdat_len(chunk):
    # Byte length of a BDAT chunk as a decimal string. The message content is
    # ASCII (the lexical regexes never emit non-ASCII), so character count equals
    # byte count; CRLF counts as the 2 bytes it is.
    return str(len(str(chunk)))


<start> ::= <Server:reply> <greeted>

# ---- Greeting + HELO/EHLO --------------------------------------------------
<greeted> ::= <hello_exchange> <post_hello>
<hello_exchange> ::= <Client:ehlo_cmd> <Server:ehlo_reply> | <Client:helo_cmd> <Server:reply>
<ehlo_cmd> ::= 'EHLO ' <domain> <crlf>
<helo_cmd> ::= 'HELO ' <domain> <crlf>

<post_hello> ::= <unauth_state>

<unauth_state> ::= <unauth_info> <unauth_info> <unauth_outcome>
<unauth_info> ::= <Client:noop_cmd> <Server:reply> \
                | <Client:help_cmd> <Server:help_reply> \
                | <Client:rset_cmd> <Server:reply> \
                | <Client:vrfy_cmd> <Server:reply> \
                | <Client:expn_cmd> <Server:reply> \
                | ''
<unauth_outcome> ::= <opt_login_fail> <login_ok> <authed_state> \
                   | <login_fail> <quit_exchange> \
                   | <quit_exchange>
<opt_login_fail> ::= <login_fail> | ''

<authed_state> ::= <authed_info> <authed_info> <mail_loop>
<authed_info> ::= <Client:noop_cmd> <Server:reply> \
                | <Client:help_cmd> <Server:help_reply> \
                | <Client:rset_cmd> <Server:reply> \
                | <Client:vrfy_cmd> <Server:reply> \
                | <Client:expn_cmd> <Server:reply> \
                | <Client:etrn_cmd> <Server:reply> \
                | ''
<mail_loop> ::= <mail_transaction> <mail_loop> | <quit_exchange>

<quit_exchange> ::= <Client:quit_cmd> <Server:reply>
<quit_cmd> ::= 'QUIT' <crlf>

# ---- Authentication --------------------------------------------------------
# A successful login moves to the authenticated state; a failed one stays
# unauthenticated. Only AUTH LOGIN is used: it is the only mechanism Exim
# advertises here (AUTH PLAIN returns 504, so it would not be within protocol).
<login_ok> ::= <auth_login_ok>
<login_fail> ::= <auth_login_bad>

<auth_login_ok> ::= <Client:auth_login_cmd> <Server:reply> \
                    <Client:user_ok> <Server:reply> \
                    <Client:pass_ok> <Server:reply>
<auth_login_bad> ::= <Client:auth_login_cmd> <Server:reply> \
                     <Client:user_any> <Server:reply> \
                     <Client:pass_bad> <Server:reply>
<auth_login_cmd> ::= 'AUTH LOGIN' <crlf>
<user_ok> ::= 'dGhlX3VzZXI=' <crlf>
<pass_ok> ::= 'dGhlX3Bhc3N3b3Jk' <crlf>
# Wrong credentials must be VALID base64, otherwise Exim aborts the AUTH exchange
# with "501 Invalid base64 data" before the password step and the session desyncs.
# Encoding a random word guarantees decodable base64 (and is almost never the real
# user/password), so the server proceeds to the 535 auth-failure path.
<user_any> ::= <wrong_b64> <crlf>
<pass_bad> ::= <wrong_b64> <crlf>
<wrong_b64> ::= r'[A-Za-z0-9+/]+={0,2}' := encode64(<wrong_word>)
<wrong_word> ::= r'[a-zA-Z0-9_]{1,16}'

# ---- Session / informational commands (valid in either state) --------------
<vrfy_cmd> ::= 'VRFY ' <vrfy_arg> <crlf>
<vrfy_arg> ::= <mailbox> | <local_part>
<expn_cmd> ::= 'EXPN ' <local_part> <crlf>
<etrn_cmd> ::= 'ETRN ' <etrn_arg> <crlf>
<etrn_arg> ::= <domain> | '#' <local_part>
<noop_cmd> ::= 'NOOP' <noop_tail> <crlf>
<noop_tail> ::= ' ' <printable> | ''
<help_cmd> ::= 'HELP' <help_tail> <crlf>
<help_tail> ::= ' ' <help_topic> | ''
<help_topic> ::= 'HELO' | 'EHLO' | 'MAIL' | 'RCPT' | 'DATA' | 'BDAT' | 'AUTH' | 'VRFY' | 'EXPN' | 'NOOP' | 'QUIT' | 'RSET' | 'HELP'
<rset_cmd> ::= 'RSET' <crlf>

# ---- Mail transaction ------------------------------------------------------
<mail_transaction> ::= <Client:mail_cmd> <Server:reply> <rcpt_list> <message_phase> \
                     | <prdr_transaction>

<prdr_transaction> ::= <Client:prdr_mail_cmd> <Server:reply> \
                       <Client:rcpt_cmd> <Server:reply> \
                       <Client:rcpt_cmd> <Server:reply> \
                       <Client:data_cmd> <Server:reply> \
                       <Client:data_message> <Server:prdr_reply>
<prdr_mail_cmd> ::= 'MAIL FROM:<' <reverse_path> '>' <mail_params> ' PRDR' <crlf>
<prdr_reply> ::= <reply> <reply> <reply> <reply>

<mail_cmd> ::= 'MAIL FROM:<' <reverse_path> '>' <mail_params> <crlf>
<reverse_path> ::= <mailbox> | ''            # MAIL FROM:<> is a valid (bounce) sender
# Each ESMTP parameter appears at most once, in a fixed order (all inside this
# one client packet, so '?' here is safe for the navigator).
# (PRDR is omitted: it makes Exim emit an extra per-recipient response sequence
# after DATA that this single-reply data phase does not model.)
<mail_params> ::= <p_size> <p_body> <p_ret> <p_envid> <p_auth>
<p_size> ::= ' SIZE=' <number> | ''
<p_body> ::= ' BODY=' <body_type> | ''
<p_ret> ::= ' RET=' <ret_value> | ''
<p_envid> ::= ' ENVID=' <xtext> | ''
<p_auth> ::= ' AUTH=<>' | ''
<body_type> ::= '7BIT' | '8BITMIME'
<ret_value> ::= 'FULL' | 'HDRS'

<rcpt_list> ::= <Client:rcpt_cmd> <Server:reply> <rcpt_list> | <Client:rcpt_cmd> <Server:reply>
<rcpt_cmd> ::= 'RCPT TO:<' <forward_path> '>' <rcpt_params> <crlf>
<forward_path> ::= <mailbox>
<rcpt_params> ::= <p_notify> <p_orcpt>
<p_notify> ::= ' NOTIFY=' <notify_value> | ''
<p_orcpt> ::= ' ORCPT=rfc822;' <xtext> | ''
<notify_value> ::= 'NEVER' | <notify_opt> | <notify_opt> ',' <notify_opt>
<notify_opt> ::= 'SUCCESS' | 'FAILURE' | 'DELAY'

# A message is submitted either with the classic DATA/dot path or, since Exim
# advertises CHUNKING, with the BDAT path (RFC 3030). BDAT carries a length-prefixed
# chunk instead of a dot-terminated stream.
<message_phase> ::= <data_phase> | <bdat_phase>
<data_phase> ::= <Client:data_cmd> <Server:reply> <Client:data_message> <Server:reply>
<data_cmd> ::= 'DATA' <crlf>
# mail_content already ends with CRLF, so appending '.' CRLF terminates the data.
<data_message> ::= <mail_content> '.' <crlf>

<bdat_phase> ::= <Client:bdat_last_cmd> <Server:bdat_reply>
<bdat_reply> ::= <resp_code> '-' <resp_text> <crlf> <resp_code> <resp_final_text> <crlf>
<bdat_last_cmd> ::= 'BDAT ' <bdat_size> ' LAST' <crlf> <bdat_chunk>
<bdat_size> ::= r'[0-9]{1,7}'
<bdat_chunk> ::= <mail_content>
where <bdat_size> == bdat_len(<bdat_chunk>)

# ---- Message content (headers + body) --------------------------------------
<mail_content> ::= <headers> <crlf> <body>
<headers> ::= <h_from> <h_to> <oh_subject> <oh_cc> <oh_replyto> <oh_sender> \
              <oh_date> <oh_messageid> <oh_mime> <oh_ctype> <oh_cte> <oh_xheader>
<oh_subject> ::= <h_subject> | ''
<oh_cc> ::= <h_cc> | ''
<oh_replyto> ::= <h_replyto> | ''
<oh_sender> ::= <h_sender> | ''
<oh_date> ::= <h_date> | ''
<oh_messageid> ::= <h_messageid> | ''
<oh_mime> ::= <h_mime> | ''
<oh_ctype> ::= <h_ctype> | ''
<oh_cte> ::= <h_cte> | ''
<oh_xheader> ::= <h_xheader> | ''
<h_from> ::= 'From: ' <mailbox> <crlf>
<h_to> ::= 'To: ' <mailbox> <crlf>
<h_cc> ::= 'Cc: ' <mailbox> <crlf>
<h_replyto> ::= 'Reply-To: ' <mailbox> <crlf>
<h_sender> ::= 'Sender: ' <mailbox> <crlf>
<h_subject> ::= 'Subject: ' <printable> <crlf>
<h_date> ::= 'Date: ' <date_value> <crlf>
<h_messageid> ::= 'Message-ID: <' <local_part> '@' <domain> '>' <crlf>
<h_mime> ::= 'MIME-Version: 1.0' <crlf>
<h_ctype> ::= 'Content-Type: ' <content_type> <crlf>
<h_cte> ::= 'Content-Transfer-Encoding: ' <cte_value> <crlf>
<h_xheader> ::= 'X-' <token> ': ' <printable> <crlf>
<content_type> ::= 'text/plain; charset=utf-8' | 'text/html' | 'multipart/mixed; boundary=abc'
<cte_value> ::= '7bit' | '8bit' | 'base64' | 'quoted-printable'
<date_value> ::= <formatted_date> := format_date(random.randint(1, 2147483647))
<formatted_date> ::= r'[A-Za-z0-9:+, ]+'
# Body bounded to 1-3 lines (finite k-paths, still exercises body reception).
<body> ::= <body_line> <body_line2> <body_line3>
<body_line2> ::= <body_line> | ''
<body_line3> ::= <body_line> | ''
<body_line> ::= <safe_text> <crlf>

# ---- Lexical primitives ----------------------------------------------------
<mailbox> ::= <local_part> '@' <domain>
# Exim-acceptable: no restricted chars (% ! /), no leading/trailing dot or hyphen.
<local_part> ::= r'[a-zA-Z0-9]' | r'[a-zA-Z0-9][a-zA-Z0-9._+\-]{0,20}[a-zA-Z0-9]'
<domain> ::= <label> '.' <label> | <label> '.' <label> '.' <label>
<label> ::= r'[a-zA-Z0-9]' | r'[a-zA-Z0-9][a-zA-Z0-9\-]{0,10}[a-zA-Z0-9]'
<number> ::= r'[1-9][0-9]{0,6}'
<token> ::= r'[A-Za-z0-9\-]{1,16}'
<xtext> ::= r'[A-Za-z0-9]{1,24}'
<printable> ::= r'[A-Za-z0-9 _.\-]{1,40}'
<safe_text> ::= r'[A-Za-z0-9 _.\-]{0,60}'
<crlf> ::= '\r\n'

# ---- Server replies --------------------------------------------------------
<reply> ::= <resp_code> <resp_final_text> <crlf>
<resp_final_text> ::= ' ' <resp_text> | ''

<ehlo_reply> ::= <ehlo_line> <ehlo_more> <ehlo_final>
<ehlo_more> ::= <ehlo_line> <ehlo_more> | ''
<ehlo_line> ::= <resp_code> '-' <resp_text> <crlf>
<ehlo_final> ::= <resp_code> ' ' <resp_text> <crlf>

<help_reply> ::= <help_more> <help_final>
<help_more> ::= <help_line> <help_more> | ''
<help_line> ::= <resp_code> '-' <resp_text> <crlf>
<help_final> ::= <resp_code> <help_final_text> <crlf>
<help_final_text> ::= ' ' <resp_text> | ''

<resp_code> ::= r'[2-5][0-9][0-9]'
<resp_text> ::= r'[^\r\n]*'

# ---- Parties ---------------------------------------------------------------
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://127.0.0.1:8025"
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://127.0.0.1:8025"
        )
        self.start()
