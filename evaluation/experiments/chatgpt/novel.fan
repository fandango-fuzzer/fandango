from faker import Faker
fake = Faker()

<start> ::= <exchange>
<exchange> ::= <Client:request><Gpt:response>
<request> ::= '{"model": "' <gpt_model> '", "messages": [{"role": "user", "content": "' <gpt_message> '"}]}'
#<request> ::= <gpt_model><gpt_message>
<gpt_model> ::= 'gpt-4.1' #| 'o4-mini' #| 'o3'
<gpt_message> ::= 'You are a poet. Write me a poem that includes the words: ' <msg_words> '. You are not allowed to alter these words in any way.'
<msg_words> ::= <msg_word> (', ' <msg_word>)*
<msg_word> ::= r'[a-zA-Z]+' := fake.word()
<response> ::= r'(?s).*'
#<response> ::= '{\'id\': \'' <gpt_id> '\', \'object\': \'chat.completion\', \'created\': ' <gpt_created> ', \'model\': \''
#        <gpt_model_reply> '\', \'choices\': [{\'index\': 0, \'message\': {\'role\': \'assistant\', \'content\': \'' <gpt_reply> '\', \'refusal\': None, \'annotations\': []}, \'logprobs\': None, \'finish_reason\': \'stop\'}], \'usage\': {\'prompt_tokens\': <number>, \'completion_tokens\': <number>, \'total_tokens\': <number>, \'prompt_tokens_details\': {\'cached_tokens\': <number>, \'audio_tokens\': 0}, \'completion_tokens_details\': {\'reasoning_tokens\': 0, \'audio_tokens\': 0, \'accepted_prediction_tokens\': 0, \'rejected_prediction_tokens\': 0}}, \'service_tier\': \'default\', \'system_fingerprint\': \''<gpt_fingerprint> '\'}'
#<gpt_id> ::= 'chatcmpl-' r'[a-zA-Z0-9]+'
#<gpt_model_reply> ::= r'[a-z0-9\-\.,\s\n]+'
#<gpt_created> ::= r'[0-9]+'
#<gpt_reply> ::= r'[a-zA-Z0-9\-\.]+'
#<gpt_fingerprint> ::= 'fp_' r'[a-z0-9]+'


where forall <ex> in <exchange>:
    forall <word> in <ex>.<request>..<msg_word>:
        str(<word>) in str(<ex>.<response>)

import requests
import json
class Client(FandangoAgent):
    def __init__(self):
        super().__init__(True)
        if not self.is_fandango():
            return
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        data = json.loads(message.to_string())
        response = requests.post(self.url, headers=self.headers, json=data)
        response = response.json()
        response = response["choices"][0]["message"]["content"]
        self.receive_msg("Gpt", str(response))

class Gpt(FandangoAgent):
    def __init__(self):
        super().__init__(False)