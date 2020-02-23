import spacy
from app_utils import get_inputs
from flask import jsonify
import json
import en_core_web_sm


nlp = en_core_web_sm.load()
nlp2 = spacy.load('entity_recognizer')


def get_entity():
    inputs = get_inputs()
    sentence = inputs["sentence"]
    doc = nlp(sentence)
    if not doc.ents:
        doc = nlp2(sentence)

    response = '{\"entities\": ' + str(list(doc.ents)) + '}'

    return jsonify(response), 200
