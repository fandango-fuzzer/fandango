import random
from flask import Flask, request
import json
import requests

# start with: flask --app flask_server run


app = Flask(__name__)
nr_low = 0
nr_high = 0
nr_mid = 0
url_party_c = "http://localhost:8081/api/hello"


@app.route("/api/hello", methods=["POST"])
def hello():
    json = request.get_json()
    global nr_low
    global nr_high
    global nr_mid
    global url_party_c
    if "nr" not in json:
        nr_low = random.randint(1, 100)
        nr_high = nr_low + 10
        json = {"nr_low": nr_low, "nr_high": nr_high}
        print(f"Generated challenge: {json}")

        external_response = requests.post(url_party_c, json=json)
        nr_mid = external_response.json()["nr_mid"]
        return external_response.json()
    else:
        result = nr_low < json["nr"] < nr_mid < nr_high
        result |= nr_low < nr_mid < json["nr"] < nr_high
        return {"result": result}


if __name__ == "__main__":
    app.run(debug=False, port=8080)
