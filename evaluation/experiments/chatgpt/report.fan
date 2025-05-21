from faker import Faker
fake = Faker()

<start> ::= <exchange>
<exchange> ::= <Client:request><Gpt:response>
<request> ::= <gpt_model><gpt_message>
<gpt_model> ::= 'gpt-4.1' #| 'o4-mini' #| 'o3'
<gpt_message> ::= 'You are a researcher. Write a report about the following subject: ' <subject>
                  '. Every word in the subject must appear exactly as written in the text. No changes allowed. '
                  'Avoid using the following words under any circumstances: ' <avoid> '.'
<subject> ::= <verb> ' ' <adjective> ' ' <noun>
<verb> ::= 'testing' | 'evaluating' | 'debugging' | 'inventing' | 'fixing' | 'discussing'
<noun> ::= 'rocket' | 'networks' | 'cars' | 'cyborgs' | 'space' | 'climate' | 'economy'
<adjective> ::= 'innovative' | 'sustainable' | 'disruptive' | 'transformative' | 'revolutionary'
<avoid> ::= 'AI' | 'crash' | 'Elon' | 'universe'

<response> ::= r'(?s).*'

where str(<exchange>.<request>..<verb>).lower() in str(<exchange>.<response>).lower()
where str(<exchange>.<request>..<adjective>).lower() in str(<exchange>.<response>).lower()
where str(<exchange>.<request>..<noun>).lower() in str(<exchange>.<response>).lower()
where str(<exchange>.<request>..<avoid>).lower() not in str(<exchange>.<response>).lower().split(' ')

import openai
class Client(FandangoAgent):
    def __init__(self):
        super().__init__(True)
        if not self.is_fandango():
            return
        openai.api_key = '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'

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        response = openai.responses.create(
           model=message.children[0].to_string(),
           input=message.children[1].to_string()
        )
        self.receive_msg("Gpt", response.output_text)

class Gpt(FandangoAgent):
    def __init__(self):
        super().__init__(False)