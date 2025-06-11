<start> ::= <ProgIn:grep_file><ProgOut:grep_resp>
<grep_file> ::= 'Hello\n'
<grep_resp> ::= 'Hello\n'

#set_program_command("grep --line-buffered Hello")
ProcessManager.instance().command = "grep --line-buffered Hello"
