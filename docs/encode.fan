import base64

<start> ::= b'Data: ' <item>
<item> ::= rb'.*' := base64.b64encode(bytes(<data>))
<data> ::= b'Fandango' <byte>+