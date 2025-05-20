from faker import Faker
fake = Faker()

<start> ::= <exchange>
<exchange> ::= <Client:request><Gpt:response>
<request> ::= <gpt_model><gpt_message>
<gpt_model> ::= 'gpt-4.1' #| 'o4-mini' #| 'o3'
<gpt_message> ::= 'You are a researcher. Write me a report about the following subjects: ' <subjects> '. In the following context: ' <context> '. With the following orientation: ' <adjective> '. All these mentioned words need to be part of the text and are not allowed to be changed in any way. Avoid the following words at all cost: ' <avoid> '.'
<subjects> ::= <subject> (', ' <subject>)*
<subject> ::= 'Flying cars' | 'Quantum computing' | 'Artificial intelligence' | 'Space exploration' | 'Climate change' | 'Economic collapse'
<context> ::= 'Environmental impact' | 'Technological advancements' | 'Societal implications' | 'Economic factors' | 'Ethical considerations'
<adjective> ::= 'innovative' | 'sustainable' | 'disruptive' | 'transformative' | 'revolutionary'
<avoid> ::= 'Large language model' | 'Musk' | 'AI' | 'Crash' | 'Universe'

<response> ::= r'(?s).*'

where forall <ex> in <exchange>:
    forall <word> in <ex>.<request>..<subject>:
        str(<word>).lower() in str(<ex>.<response>).lower()
where forall <ex> in <exchange>:
    forall <word> in <ex>.<request>..<context>:
        str(<word>).lower() in str(<ex>.<response>).lower()
where forall <ex> in <exchange>:
    forall <word> in <ex>.<request>..<adjective>:
        str(<word>).lower() in str(<ex>.<response>).lower()
where forall <ex> in <exchange>:
    forall <word> in <ex>.<request>..<avoid>:
        str(<word>).lower() not in str(<ex>.<response>).lower()

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