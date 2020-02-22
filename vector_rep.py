import word2vec
import numpy as np
import spacy


model = word2vec.load("word2vec.bin")
nlp = spacy.load('en_core_web_sm')


def sentence2vec(sentence):
    """
    Return the ndarray representing <sentence>.
    """
    total_vector = np.zeros(100)
    tokenizer = nlp(sentence)
    for word in tokenizer:
        if word.text.lower() in model:
            total_vector.__iadd__(model[word.text.lower()])

    return total_vector
