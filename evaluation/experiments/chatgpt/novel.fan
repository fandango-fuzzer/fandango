
<start> ::= <>
<request> ::= <gpt_model><gpt_messages>

<gpt_model> ::= 'gpt-4.1' | 'o4-mini' | 'o3'
<gpt_messages> ::=

import openai
class Client(FandangoAgent):
    def __init__(self):
        super().__init__(True)
        if not self.is_fandango():
            return
        openai.api_key = None

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        response = openai.ChatCompletion.create(
           model="gpt-4",
           messages=[{"role": "user", "content": "Hello, ChatGPT!"}]
        )
        self.receive_msg("GPT", response["choices"][0]["message"]["content"]))