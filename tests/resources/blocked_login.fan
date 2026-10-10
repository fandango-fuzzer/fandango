# A login can succeed from <start>, but the server refuses a second successful login from <logged_in>.
# Blocking the success in <logged_in> must keep the login from <start>. A failed login repeats the exchange, so no
# recursive call lies above the first login and its step starts at <start>; the second login's step starts at
# <logged_in>, the caller of the recursive call <logged_in> -> <exchange_login>.
<start> ::= <exchange_login>
<exchange_login> ::= <Fuzzer:Extern:login> <Extern:Fuzzer:failed> <exchange_login> | <Fuzzer:Extern:login> <Extern:Fuzzer:success> <logged_in>
<logged_in> ::= <Fuzzer:Extern:other> <Extern:Fuzzer:ok> | <exchange_login>
<login> ::= 'login\n'
<failed> ::= 'failed\n'
<success> ::= 'success\n'
<other> ::= 'other\n'
<ok> ::= 'ok\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def start(self):
        pass

    def stop(self):
        pass


class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self):
        pass

    def stop(self):
        pass
