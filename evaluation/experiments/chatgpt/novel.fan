from faker import Faker
fake = Faker()

<start> ::= <exchange>
<exchange> ::= <Client:request><Gpt:response>
<request> ::= <gpt_model><gpt_message>


<gpt_model> ::= 'gpt-4.1' | 'o4-mini' #| 'o3'
<gpt_message> ::= 'You are a poet. Write me a poem that includes the words: ' <msg_words> '. You are not allowed to alter these words in any way.'
<msg_words> ::= <msg_word> (', ' <msg_word>)*
<msg_word> ::= r'[a-zA-Z]+' := fake.word()
<response> ::= r'[a-zA-Z0-9 \n]+'

where forall <ex> in <exchange>:
    forall <word> in <ex>.<request>..<msg_word>:
        <word> in <ex>.<response>

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