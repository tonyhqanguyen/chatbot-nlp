import spacy
from app import *
from flask import jsonify

nlp = spacy.load("en_core_web_sm")
nlp2 = spacy.load("/Users/tonynguyen/Desktop/ML/chatbot-nlp/entity_recognizer")


@app.route('/ner', methods=["POST"])
def get_entity():
    inputs = get_inputs()
    sentence = inputs["sentence"]
    doc = nlp(sentence)
    if not len(doc.ents):
        doc = nlp2(sentence)

    response = {
        "entities": list(doc.ents)
    }

    return jsonify(response), 200
