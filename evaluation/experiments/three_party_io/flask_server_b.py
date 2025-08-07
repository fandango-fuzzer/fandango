import random
from flask import Flask, request
import html

# start with: flask --app flask_server run


app = Flask(__name__)
nr_low = 0
nr_high = 0


@app.route("/api/hello", methods=["POST"])
def hello():
    assert request.json is not None
    return {
        "nr_low": html.escape(str(request.json["nr_low"])),
        "nr_mid": random.randint(
            int(request.json["nr_low"]) + 2, int(request.json["nr_high"]) - 2
        ),
        "nr_high": html.escape(str(request.json["nr_high"])),
    }


if __name__ == "__main__":
    app.run(debug=False, port=8081)
