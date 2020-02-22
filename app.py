from flask import Flask
from intention_parser import get_intention
from entity_extraction import get_entity

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
