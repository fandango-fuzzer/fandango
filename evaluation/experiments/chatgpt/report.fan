<start> ::= <Client:request><Gpt:response>
<request> ::= <gpt_model><gpt_message>
<gpt_model> ::= 'gpt-4.1' #| 'o4-mini' #| 'o3'
<gpt_message> ::= 'Write a report about ' <subject> '. ' \
                  'Include every word from the subject. ' \
                  'Under no circumstances should the ' \
                  'following non-case sensitive character ' \
                  'sequence be used: ' <avoid>
<subject> ::= <verb> ' ' <adjective> ' ' <noun> ' ' <place>
<verb> ::= 'testing' | 'evaluating' | 'fixing'
<adjective> ::= 'sustainable' | 'intestinal' | 'innovative'
<noun> ::= 'rocket' | 'cars' | 'rockets' | 'satellites'
<place> ::= 'at Google' | 'on Mars' | 'at FSE 2026'
<avoid> ::= 'woke' | 'crash' | 'Elon' | 'universe'
<response> ::= r'(?s).*'

where str(<request>..<verb>).lower() in str(<response>).lower()

where str(<request>..<adjective>).lower() in str(<response>).lower()

where str(<request>..<noun>).lower() in str(<response>).lower()

where str(<request>..<avoid>).lower() not in str(<response>).lower()

import openai
class Client(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.CONNECT)
        if not self.is_fuzzer_controlled():
            return
        openai.api_key = 'YOUR_OPENAI_API_KEY'

    def send(self, message: DerivationTree, recipient: str):
        response = openai.responses.create(
           model=message.children[0].to_string(),
           input=message.children[1].to_string()
        )
        self.receive(response.output_text, sender="Gpt")

    def start(self):
        pass

    def stop(self):
        pass

class Gpt(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self):
        pass

    def stop(self):
        pass