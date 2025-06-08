<start> ::= <exchange>{20}
<exchange> ::= <Client:request><Gpt:response>
<request> ::= <gpt_model><gpt_message>
<gpt_model> ::= 'gpt-4.1' #| 'o4-mini' #| 'o3'
<gpt_message> ::= 'Write a report about ' <subject> '. '
                  'Include every word from the subject. '
                  'Under no circumstances should the '
                  'following non-case sensitive character '
                  'sequence be used: ' <avoid>
<subject> ::= <verb> ' ' <adjective> ' ' <noun> ' ' <place>
<verb> ::= 'testing' | 'evaluating' | 'fixing'
<adjective> ::= 'sustainable' | 'intestinal' | 'innovative'
<noun> ::= 'rocket' | 'cars' | 'rockets' | 'satellites'
<place> ::= 'at Google' | 'on Mars' | 'at ASE 2025'
<avoid> ::= 'AI' | 'crash' | 'Elon' | 'universe'
<response> ::= r'(?s).*'

where forall <ex> in <exchange>:
    str(<ex>.<request>..<verb>).lower() in str(<ex>.<response>).lower()
    and str(<ex>.<request>..<adjective>).lower() in str(<ex>.<response>).lower()
    and str(<ex>.<request>..<noun>).lower() in str(<ex>.<response>).lower()
    and str(<ex>.<request>..<avoid>).lower() not in str(<ex>.<response>).lower()

import openai
class Client(FandangoParty):
    def __init__(self):
        super().__init__(True)
        if not self.is_fuzzer_controlled():
            return
        openai.api_key = 'YOUR_OPENAI_API_KEY'

    def on_send(self, message: DerivationTree, recipient: str):
        response = openai.responses.create(
           model=message.children[0].to_string(),
           input=message.children[1].to_string()
        )
        self.receive_msg("Gpt", response.output_text)

class Gpt(FandangoParty):
    def __init__(self):
        super().__init__(False)