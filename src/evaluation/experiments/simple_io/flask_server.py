import random
from flask import Flask, request

# start with: flask --app flask_server run


app = Flask(__name__)
nr_low = 0
nr_high = 0

@app.route('/api/hello', methods=['POST'])
def hello():
    json = request.get_json()
    global nr_low
    global nr_high
    if 'nr' not in json:
        nr_low = random.randint(1, 100)
        nr_high = nr_low + random.randint(1, 10)
        json = {
            'nr_low': nr_low,
            'nr_high': nr_high
        }
    else:
        print(json)
        json = {
            "result": nr_low < int(json['nr']) < nr_high
        }
    return json


