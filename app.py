from flask import Flask
from intention_parser import get_intention
from entity_extraction import get_entity
import os

app = Flask("Chatbot")

@app.route("/")
def hello_world():
    return "HELLO WORLD!"


@app.route("/intention", methods=["POST"])
def intention():
    print("Detecting intention...")
    return get_intention()


@app.route('/ner', methods=["POST"])
def entity():
    print("Getting entity...")
    return get_entity()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
