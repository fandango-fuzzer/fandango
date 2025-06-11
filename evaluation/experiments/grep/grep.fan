<start> ::= <ProgIn:grep_file><ProgOut:grep_resp>
<grep_file> ::= 'Hello\n'
<grep_resp> ::= 'Hello\n'

ProcessManager.instance().command = "grep --line-buffered Hello"
