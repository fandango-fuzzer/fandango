import base64
import socket
from datetime import datetime, timezone
import random

def format_unix_time(unix_time):
    dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    return dt.strftime('%a, %d %b %Y %H:%M:%S %z')

def str_to_unix_time(unix_time_formatted):
    dt = datetime.strptime(unix_time_formatted, '%a, %d %b %Y %H:%M:%S %z')
    return int(dt.timestamp())

def encode64(input):
    return base64.b64encode(str(input).encode('utf-8')).decode('utf-8')

def decode64(input):
    return base64.b64decode(str(input).encode('utf-8')).decode('utf-8')

def plain64(user, password):
    raw = '\x00' + str(user) + '\x00' + str(password)
    return base64.b64encode(raw.encode('utf-8')).decode('utf-8')

<start> ::= <state_setup>

# The server greets with 220, the client greets with EHLO or HELO, then the
# grammar leads over to the logged out state.
<state_setup> ::= <Server:response_setup> <greeting> <state_logged_out>

<greeting> ::= <greeting_ehlo> | <greeting_helo>
<greeting_ehlo> ::= <Client:request_ehlo> <Server:response_ehlo>
<greeting_helo> ::= <Client:request_helo> <Server:response_helo>

# Logged out: authenticate, run a command that works without login, or quit. A
# mail without auth gets rejected by the server.
<state_logged_out> ::= \
      <exchange_login_valid> \
    | <exchange_login_invalid> \
    | (<exchange_pre_auth_cmd> <state_logged_out>) \
    | (<exchange_mail_unauth> <state_logged_out>) \
    | <exchange_quit>

<exchange_pre_auth_cmd> ::= \
      <exchange_noop> \
    | <exchange_help> \
    | <exchange_rset> \
    | <exchange_vrfy> \
    | <exchange_expn> \
    | <exchange_bad_command>

# Logged in: send a mail, run a stateless command, or quit.
<state_logged_in> ::= \
      ((<exchange_mail> | <exchange_pre_auth_cmd>) <state_logged_in>) \
    | <exchange_quit>

# A successful login (AUTH PLAIN initial-response, AUTH PLAIN, or AUTH LOGIN)
# leads to the logged in state.
<exchange_login_valid> ::= \
      (<login_plain_initial_valid> <state_logged_in>) \
    | (<login_plain_multiline_valid> <state_logged_in>) \
    | (<login_login_valid> <state_logged_in>)

<login_plain_initial_valid> ::= \
    <Client:request_auth_plain_initial_correct> <Server:response_auth_success>

<login_plain_multiline_valid> ::= \
    <Client:request_auth_plain> <Server:response_auth_continue> \
    <Client:request_auth_plain_correct> <Server:response_auth_success>

<login_login_valid> ::= \
    <Client:request_auth_login> <Server:response_auth_expect_user> \
    <Client:request_auth_user_correct> <Server:response_auth_expect_pass> \
    <Client:request_auth_pass_correct> <Server:response_auth_success>

# A failed login (any mechanism) returns to the logged out state.
<exchange_login_invalid> ::= \
      (<login_plain_initial_invalid> <state_logged_out>) \
    | (<login_plain_multiline_invalid> <state_logged_out>) \
    | (<login_login_invalid> <state_logged_out>)

<login_plain_initial_invalid> ::= \
    <Client:request_auth_plain_initial_incorrect> <Server:response_auth_fail>

<login_plain_multiline_invalid> ::= \
    <Client:request_auth_plain> <Server:response_auth_continue> \
    <Client:request_auth_plain_incorrect> <Server:response_auth_fail>

<login_login_invalid> ::= \
    <Client:request_auth_login> <Server:response_auth_expect_user> \
    ((<Client:request_auth_user_correct> <Server:response_auth_expect_pass> \
        <Client:request_auth_pass_incorrect>) \
     | (<Client:request_auth_user_incorrect> <Server:response_auth_expect_pass> \
        (<Client:request_auth_pass_incorrect> | <Client:request_auth_pass_correct>))) \
    <Server:response_auth_fail>

<request_auth_login> ::= 'AUTH LOGIN\r\n'
<response_auth_expect_user> ::= '334 ' r'[a-zA-Z0-9\+/\\\=]+' '\r\n'
<request_auth_user_correct> ::= <user_correct_64> '\r\n'
<request_auth_user_incorrect> ::= <user_incorrect_64> '\r\n'
<response_auth_expect_pass> ::= '334 ' r'[a-zA-Z0-9\+/\\\=]+' '\r\n'
<request_auth_pass_correct> ::= <pass_correct_64> '\r\n'
<request_auth_pass_incorrect> ::= <pass_incorrect_64> '\r\n'

<request_auth_plain> ::= 'AUTH PLAIN\r\n'
<response_auth_continue> ::= r'334 [A-Za-z0-9+/=\\]*\r\n'
<request_auth_plain_correct> ::= <plain_correct_64> '\r\n'
<request_auth_plain_incorrect> ::= <plain_incorrect_64> '\r\n'

<request_auth_plain_initial_correct> ::= 'AUTH PLAIN ' <plain_correct_64> '\r\n'
<request_auth_plain_initial_incorrect> ::= 'AUTH PLAIN ' <plain_incorrect_64> '\r\n'

<response_auth_success> ::= '235 ' r'[a-zA-Z0-9\-\. ]+' '\r\n'
<response_auth_fail> ::= r'5\d\d' ' ' r'[a-zA-Z0-9\-\.:\(\)/ ]+' '\r\n'

# The credential base64 is computed, not hard-coded.
<user_correct_64> ::= r'[a-zA-Z0-9\+/\\\=]+' := encode64('the_user')
<pass_correct_64> ::= r'[a-zA-Z0-9\+/\\\=]+' := encode64('the_password')
<user_incorrect_64> ::= r'[a-zA-Z0-9\+/\\\=]+' := encode64(<user_incorrect>)
<pass_incorrect_64> ::= r'[a-zA-Z0-9\+/\\\=]+' := encode64(<pass_incorrect>)
<plain_correct_64> ::= r'[a-zA-Z0-9\+/\\\=]+' := plain64('the_user', 'the_password')
<plain_incorrect_64> ::= r'[a-zA-Z0-9\+/\\\=]+' := plain64('wrong_user', 'wrong_pass')

<user_incorrect> ::= r'^(?!the_user$)([a-zA-Z0-9_]+)' := decode64(<user_incorrect_64>)
<pass_incorrect> ::= r'^(?!the_password$)([a-zA-Z0-9_]+)' := decode64(<pass_incorrect_64>)

<response_setup> ::= '220 ' r'[a-zA-Z0-9\-\. ]+' '\r\n'
# Verbs are matched case-insensitively, but generated upper-case.
<request_ehlo> ::= r'(?i:EHLO)' ' ' <client_identifier> '\r\n'
<request_helo> ::= r'(?i:HELO)' ' ' <client_identifier> '\r\n'
<client_identifier> ::= r'([a-zA-Z0-9\-\.]+[ ]?)+' := 'io.fandango.local'
<response_ehlo> ::= <response_ehlo_param>+ <response_ehlo_end> := '250-fandango-server\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
<response_ehlo_param> ::= '250-' r'[a-zA-Z0-9\-\.=\[\]\, ]+' '\r\n'
<response_ehlo_end> ::= '250 ' r'[a-zA-Z0-9\-\.=\[\]\, ]+' '\r\n'
<response_helo> ::= '250 ' r'[a-zA-Z0-9\-\.=\[\]\, ]+' '\r\n'

<exchange_quit> ::= <Client:request_quit> <Server:response_quit>
<exchange_noop> ::= <Client:request_noop> <Server:positive_response>
<exchange_help> ::= <Client:request_help> <Server:response_help>
<exchange_rset> ::= <Client:request_rset> <Server:positive_response>
<exchange_vrfy> ::= <Client:request_vrfy> <Server:response_vrfy_expn>
<exchange_expn> ::= <Client:request_expn> <Server:response_vrfy_expn>
<exchange_bad_command> ::= <Client:request_bad_command> <Server:response_command_error>

<request_quit> ::= r'(?i:QUIT)' '\r\n'
<response_quit> ::= '221 ' r'[a-zA-Z0-9\-\. ]+' '\r\n'
<request_noop> ::= 'NOOP' (' ' r'[^ \r\n]*')? '\r\n'
<request_help> ::= 'HELP\r\n'
<request_rset> ::= 'RSET\r\n'
<request_vrfy> ::= 'VRFY ' <email_address> '\r\n'
<request_expn> ::= 'EXPN ' r'[a-zA-Z0-9_\-]+' '\r\n'
# VRFY/EXPN are commonly refused; accept any reply code.
<response_vrfy_expn> ::= r'[2-5]\d\d' ' ' r'[a-zA-Z0-9\-\.:@<>\(\) ]+' '\r\n'
<response_help> ::= (r'2\d\d' '-' r'[^\r\n\x80-\xFF]+' '\r\n')+ r'2\d\d' ' ' r'[^\r\n\x80-\xFF]+' '\r\n'

<request_bad_command> ::= ('XYZZY' | 'FOOBAR' | 'WTF') (' ' r'[^\r\n]*')? '\r\n'
<response_command_error> ::= r'5\d\d' ' ' r'[a-zA-Z0-9\-\.:\(\) ]+' '\r\n'

# A mail transaction is stepped so RSET can abort it before DATA. Once DATA is
# accepted the body runs opaque until <CRLF>.<CRLF>.
<exchange_mail> ::= \
    <Client:request_mail_from> <Server:response_mail_from> <transaction_after_from>

<transaction_after_from> ::= \
      (<rcpt_ok> <transaction_after_rcpt>) \
    | <exchange_rset>

<transaction_after_rcpt> ::= \
      (<rcpt_ok> <transaction_after_rcpt>) \
    | <transaction_data> \
    | <exchange_rset>

<transaction_data> ::= \
    <Client:request_mail_data> <Server:response_mail_data> \
    <Client:Server:mail_data> <Server:positive_response>

<rcpt_ok> ::= <Client:request_mail_to> <Server:response_mail_to>

# MAIL FROM before auth is rejected (the server requires auth).
<exchange_mail_unauth> ::= <Client:request_mail_from> <Server:response_mail_denied>
<response_mail_denied> ::= r'5(30|03|07|54)' ' ' r'[a-zA-Z0-9\-\.:\(\) ]+' '\r\n'

<mail_data> ::= <mail_header> <mail_body>
# Subject/from/to/date come first; any further header is optional and may be
# reordered, with <mail_header_other> catching unknown header lines.
<mail_header> ::= <mail_header_subject> \
    <mail_header_from> \
    <mail_header_to> \
    <mail_header_date> \
    <mail_header_optional>* \
    <mail_header_end>
<mail_header_optional> ::= <mail_header_message_id> \
    | <mail_header_mailer> \
    | <mail_header_reply_to> \
    | <mail_header_mime> \
    | <mail_header_content_type> \
    | <mail_header_encoding> \
    | <mail_header_other>
<mail_header_other> ::= r'[A-Za-z][A-Za-z0-9\-]*' ': ' r'[^\r\n]*' '\r\n'
<mail_body> ::= <mail_contents_64> <mail_body_end>

<request_mail_from> ::= r'(?i:MAIL FROM:)' '<' <email_address> '>' <mail_params>? '\r\n'
<response_mail_from> ::= '250 ' r'[a-zA-Z0-9\-\. ]+' '\r\n'
<request_mail_to> ::= r'(?i:RCPT TO:)' '<' <email_address> '>' <rcpt_params>? '\r\n'
<response_mail_to> ::= '250 ' r'[a-zA-Z0-9\-\.\: ]+' '\r\n'
<request_mail_data> ::= r'(?i:DATA)' '\r\n'
<response_mail_data> ::= '354 ' r'[a-zA-Z0-9\-\.\,\"\:\<\> ]+' '\r\n'

<mail_params> ::= (' SIZE=' r'[1-9][0-9]{0,6}')? (' BODY=' ('7BIT' | '8BITMIME'))?
<rcpt_params> ::= (' ORCPT=rfc822;' <email_address>)?

<mail_body_end> ::= '\r\n\r\n.\r\n'
<mail_contents_64> ::= r'[a-zA-Z0-9\+/\\\=]+' := encode64(<mail_contents>)
<mail_contents> ::= r'([a-zA-Z0-9\r\n]+)' := decode64(<mail_contents_64>)

<mail_header_subject> ::= 'subject: ' r'[^\r\n]*' '\r\n'
<mail_header_from> ::= 'from: ' <email_address> '\r\n'
<mail_header_to> ::= 'to: ' <email_address> '\r\n'
<mail_header_date> ::= 'date: ' <unix_time_formatted> '\r\n'
<mail_header_message_id> ::= 'message-id: <' r'[a-zA-Z0-9]+' '@' r'[a-z]+\.[a-z]+' '>\r\n'
<mail_header_mailer> ::= 'x-mailer: ' r'[^\r\n]*' '\r\n'
<mail_header_reply_to> ::= 'reply-to: ' <email_address> '\r\n'
<mail_header_mime> ::= 'mime-version: 1.0\r\n'
<mail_header_content_type> ::= 'content-type: text/plain; charset=utf-8\r\n'
<mail_header_encoding> ::= 'content-transfer-encoding: base64\r\n'
<mail_header_end> ::= '\r\n'

<positive_response> ::= '250 ' r'[a-zA-Z0-9\-\.: ]+' '\r\n'
<email_address> ::= r'[a-z]+@[a-z]+\.de'
<unix_time_formatted> ::= r'[a-zA-Z0-9\:\+\, ]+' := format_unix_time(int(<unix_time>))
<unix_time> ::= <unix_time_number> := str(str_to_unix_time(str(<unix_time_formatted>)))
<unix_time_number> ::= r'[1-9][0-9]+' := str(random.randint(0, 2147483647))

# The envelope sender/recipient must match the from/to headers.
where forall <mail> in <mail_data>:
    (str(<mail>..<request_mail_from>.<email_address>) == str(<mail>..<mail_header_from>.<email_address>)
    and str(<mail>..<request_mail_to>.<email_address>) == str(<mail>..<mail_header_to>.<email_address>))
