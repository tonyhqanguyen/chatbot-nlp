import json
import numpy as np
import spacy
import en_core_web_sm


indices = json.load(open("indices.json"))
vecs = np.load("word2vec.npy")
nlp = en_core_web_sm.load()


def sentence2vec(sentence):
    """
    Return the ndarray representing <sentence>.
    """
    total_vector = np.zeros(100)
    tokenizer = nlp(sentence)
    for word in tokenizer:
        if word.text.lower() in indices:
            index = indices[word.text.lower()]
            total_vector.__iadd__(vecs[index])

    return total_vector
