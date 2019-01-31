import word2vec
import numpy
import spacy

model = word2vec.load("/Users/tonynguyen/Desktop/ML/chatbot-nlp/text.bin")
nlp = spacy.load('en_core_web_sm')


def sentence2vec(sentence: str) -> numpy.ndarray:
    """
    Return the ndarray representing <sentence>.
    """
    tokenizer = nlp(sentence)
    vecs = []
    for token in tokenizer:
        try:
            vec = model[token.text.lower()]
            vecs.append(vec)
        except KeyError as e:
            vecs.append([0 for _ in range(100)])

    total_vector = vecs[0] if vecs else None

    if vecs[1:]:
        for word_vector in vecs[1:]:
            total_vector = numpy.add(total_vector, word_vector)

    return total_vector
