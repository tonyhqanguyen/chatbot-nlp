import spacy
from app_utils import get_inputs
from flask import jsonify

nlp = spacy.load("en_core_web_sm")

def get_entity():
    inputs = get_inputs()
    sentence = inputs["sentence"]
    doc = nlp(sentence)

    response = {
        "entities": list(doc.ents)
    }

    return jsonify(response), 200
