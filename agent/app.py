from flask import Flask, make_response, request

import agent

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def alert():
    print("AHHHH PROD IS DOWN :(", flush=True)
    if request.content_type != "application/json":
        return "Content-Type must be application/json", 400

    data = request.get_json()
    agent.forward_alert(data)

    return "TEST", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
