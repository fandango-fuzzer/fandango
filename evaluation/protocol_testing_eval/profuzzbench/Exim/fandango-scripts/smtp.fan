import base64
import random
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def plain_token():
    # SASL PLAIN: authzid \0 authcid \0 passwd
    return base64.b64encode(b"\x00the_user\x00the_password").decode("utf-8")

def format_date(unix_time):
    dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

def build_bdat_last(msg):
    # CHUNKING (RFC 3030): the BDAT size MUST equal the chunk's byte length.
    body = str(msg)
    return "BDAT " + str(len(body.encode("utf-8"))) + " LAST\r\n" + body


<start> ::= <Server:reply> <greeted>

# ---- Greeting + HELO/EHLO --------------------------------------------------
<greeted> ::= <hello_exchange> <post_hello>
<hello_exchange> ::= <Client:ehlo_cmd> <Server:ehlo_reply> | <Client:helo_cmd> <Server:reply>
<ehlo_cmd> ::= 'EHLO ' <domain> <crlf>
<helo_cmd> ::= 'HELO ' <domain> <crlf>

# Either authenticate first or not (modelled as a choice, not a packet-level '?').
<post_hello> ::= <auth_exchange> <activity> <quit_exchange> | <activity> <quit_exchange>
<quit_exchange> ::= <Client:quit_cmd> <Server:reply>
<quit_cmd> ::= 'QUIT' <crlf>

# ---- Authentication --------------------------------------------------------
<auth_exchange> ::= <auth_login_ok> | <auth_login_bad> | <auth_plain_ok> | <auth_plain_bad>

<auth_login_ok> ::= <Client:auth_login_cmd> <Server:reply> \
                    <Client:user_ok> <Server:reply> \
                    <Client:pass_ok> <Server:reply>
<auth_login_bad> ::= <Client:auth_login_cmd> <Server:reply> \
                     <Client:user_any> <Server:reply> \
                     <Client:pass_bad> <Server:reply>
<auth_login_cmd> ::= 'AUTH LOGIN' <crlf>
<user_ok> ::= 'dGhlX3VzZXI=' <crlf>
<pass_ok> ::= 'dGhlX3Bhc3N3b3Jk' <crlf>
<user_any> ::= <b64> <crlf>
<pass_bad> ::= <b64> <crlf>

<auth_plain_ok> ::= <Client:auth_plain_ok_cmd> <Server:reply>
<auth_plain_bad> ::= <Client:auth_plain_bad_cmd> <Server:reply>
<auth_plain_ok_cmd> ::= 'AUTH PLAIN ' <plain_ok> <crlf>
<auth_plain_bad_cmd> ::= 'AUTH PLAIN ' <b64> <crlf>
<plain_ok> ::= <b64> := plain_token()

# ---- Activity: a recursive sequence of transactions and stand-alone commands
<activity> ::= <action> <activity> | <action>
<action> ::= <mail_transaction> \
           | <Client:vrfy_cmd> <Server:reply> \
           | <Client:expn_cmd> <Server:reply> \
           | <Client:etrn_cmd> <Server:reply> \
           | <Client:noop_cmd> <Server:reply> \
           | <Client:help_cmd> <Server:help_reply> \
           | <Client:rset_cmd> <Server:reply>

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
<mail_transaction> ::= <Client:mail_cmd> <Server:reply> <rcpt_list> <message_phase>

<mail_cmd> ::= 'MAIL FROM:<' <reverse_path> '>' <mail_params> <crlf>
<reverse_path> ::= <mailbox> | ''            # MAIL FROM:<> is a valid (bounce) sender
# Each ESMTP parameter appears at most once, in a fixed order (all inside this
# one client packet, so '?' here is safe for the navigator).
<mail_params> ::= <p_size> <p_body> <p_ret> <p_envid> <p_auth> <p_prdr>
<p_size> ::= ' SIZE=' <number> | ''
<p_body> ::= ' BODY=' <body_type> | ''
<p_ret> ::= ' RET=' <ret_value> | ''
<p_envid> ::= ' ENVID=' <xtext> | ''
<p_auth> ::= ' AUTH=<>' | ''
<p_prdr> ::= ' PRDR' | ''
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

<message_phase> ::= <data_phase>
<data_phase> ::= <Client:data_cmd> <Server:reply> <Client:data_message> <Server:reply>
<data_cmd> ::= 'DATA' <crlf>
# mail_content already ends with CRLF, so appending '.' CRLF terminates the data.
<data_message> ::= <mail_content> '.' <crlf>

# ---- Message content (headers + body) --------------------------------------
<mail_content> ::= <headers> <crlf> <body>
<headers> ::= <h_from> <h_to> <opt_headers>
<opt_headers> ::= <opt_header> <opt_headers> | <opt_header>
<opt_header> ::= <h_subject> | <h_cc> | <h_replyto> | <h_sender> | <h_date> \
               | <h_messageid> | <h_mime> | <h_ctype> | <h_cte> | <h_xheader>
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
<body> ::= <body_line> <body_more>
<body_more> ::= <body_line> <body_more> | ''
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
<b64> ::= r'[A-Za-z0-9+/]{2,40}={0,2}'
<printable> ::= r'[A-Za-z0-9 _.\-]{1,40}'
<safe_text> ::= r'[A-Za-z0-9 _.\-]{0,60}'
<crlf> ::= '\r\n'
# Body lines never start with '.', so SMTP dot-stuffing is not required.

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
