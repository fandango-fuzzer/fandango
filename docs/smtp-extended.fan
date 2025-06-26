<start> ::= <connect>
<connect> ::= <Server:id> <helo>

<id> ::= '220 ' <hostname> ' ESMTP Postfix\r\n'
<hostname> ::= r"[-a-zA-Z0-9.:]+" := "host.example.com"

<helo> ::= <Client:HELO> \
    (<Server:hello> <mail_from> | <Server:error>)
<HELO> ::= 'HELO ' <hostname> '\r\n'

<hello> ::= '250 Hello ' <hostname> ', glad to meet you\r\n' \
    <mail_from>

<error> ::= '5' <digit> <digit> ' ' <error_message> '\r\n'
<error_message> ::= r'[^\r]*' := "Error"

<mail_from> ::= <Client:MAIL_FROM> \
    (<Server:ok> <mail_to> | <Server:error>)

<MAIL_FROM> ::= 'MAIL FROM:<' <email> '>\r\n'
# Actual email addresses are much more varied
<email> ::= r"[-a-zA-Z0-9.]+" '@' <hostname> := "alice@example.com"

<ok> ::= '250 Ok\r\n'

<mail_to> ::= <Client:RCPT_TO> \
    (<Server:ok> <data> | <Server:ok> <mail_to> | <Server:error>)

<RCPT_TO> ::= 'RCPT TO:<' <email> '>\r\n'

<data> ::= <Client:DATA> <Server:end_data> <Client:message> \
    (<Server:ok> <quit> | <Server:error>)

<DATA> ::= 'DATA\r\n'

<end_data> ::= '354 End data with <CR><LF>.<CR><LF>\r\n'

<message> ::= r'[^.\r\n]*\r\n[.]\r\n'

<quit> ::= <Client:QUIT> <Server:bye>

<QUIT> ::= 'QUIT\r\n'

<bye> ::= '221 Bye\r\n'
