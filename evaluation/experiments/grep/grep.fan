<start> ::= <Input:grep_file><Output:grep_resp>
<grep_file> ::= 'Hello\n'
<grep_resp> ::= 'Hello\n'

import subprocess
import asyncio
import threading

ProcessManager.instance().command = "grep --line-buffered Hello"

class Output(FandangoParty):
    def __init__(self):
        super().__init__(Ownership.EXTERNAL)
        self.proc = ProcessManager.instance().get_process()
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        while True:
            line = self.proc.stdout.readline()
            self.receive_msg("Output", line)

class Input(FandangoParty):

    def __init__(self):
        super().__init__(Ownership.FUZZER)
        self.proc = ProcessManager.instance().get_process()

    def on_send(self, message: DerivationTree, recipient: str):
        self.proc.stdin.write(message.to_string())
        self.proc.stdin.flush()
