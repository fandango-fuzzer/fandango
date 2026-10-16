# A server that leaves the grammar for four reasons, one per way the violation profile learns a cause:
# - <help> after <ehlo> (an earlier packet); <helo> is the costlier greeting, after which <help> is answered
# - <cmd> with the argument '!' inside one regular expression (a value)
# - <set> with the argument <bad> (a k-path)
# - <get> after a <set> with <bad> (an earlier message's content)
<start> ::= <Fuzzer:Extern:hello> <state>
<state> ::= (<exchange_ehlo> <greeted>) | (<exchange_helo> <greeted>) | <Fuzzer:Extern:quit>
<greeted> ::= (<exchange_help> <greeted>) | (<exchange_cmd> <greeted>) | (<exchange_set> <greeted>) | (<exchange_get> <greeted>) | <Fuzzer:Extern:quit>
<exchange_ehlo> ::= <Fuzzer:Extern:ehlo> <Extern:Fuzzer:ok>
<exchange_helo> ::= <Fuzzer:Extern:helo> <Extern:Fuzzer:ok> <Extern:Fuzzer:ok>
<exchange_help> ::= <Fuzzer:Extern:help> <Extern:Fuzzer:helptext>
<exchange_cmd> ::= <Fuzzer:Extern:cmd> <Extern:Fuzzer:ok>
<exchange_set> ::= <Fuzzer:Extern:set> <Extern:Fuzzer:ok>
<exchange_get> ::= <Fuzzer:Extern:get> <Extern:Fuzzer:value>
<cmd> ::= 'cmd ' <word> '\n'
<word> ::= r'[abc!]'
<set> ::= 'set ' <argument> '\n'
<argument> ::= <good> | <bad>
<good> ::= 'a' | 'b' | 'c'
<bad> ::= '!'
<hello> ::= 'hello\n'
<quit> ::= 'quit\n'
<ehlo> ::= 'ehlo\n'
<helo> ::= 'helo\n'
<help> ::= 'help\n'
<get> ::= 'get\n'
<ok> ::= 'ok\n'
<helptext> ::= 'helptext\n'
<value> ::= 'value\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)
        self.greeted_by_ehlo = False
        self.bad_set = False

    def send(self, message: DerivationTree, recipient: str):
        text = str(message)
        if text == "ehlo\n":
            self.greeted_by_ehlo = True
            self.receive("ok\n", "Extern")
        elif text == "helo\n":
            self.receive("ok\n", "Extern")
            self.receive("ok\n", "Extern")
        elif text == "help\n":
            self.receive("garbage\n" if self.greeted_by_ehlo else "helptext\n", "Extern")
        elif text.startswith("cmd "):
            self.receive("garbage\n" if "!" in text else "ok\n", "Extern")
        elif text.startswith("set "):
            self.bad_set = self.bad_set or "!" in text
            self.receive("ok\n", "Extern")
        elif text == "get\n":
            self.receive("garbage\n" if self.bad_set else "value\n", "Extern")

    def start(self):
        self.greeted_by_ehlo = False
        self.bad_set = False

    def stop(self):
        pass


class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self):
        pass

    def stop(self):
        pass
