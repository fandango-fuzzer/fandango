<start> ::= <ProgIn:grep_file><ProgOut:grep_resp>
<grep_file> ::= 'Hello\n'
<grep_resp> ::= 'Hello\n'

#set_program_command("grep Hello")
ProcessManager.instance().command = "grep Hello"


class ProgIn(ProgIn):
    @property
    def close_post_transmit(self) -> bool:
        return True
