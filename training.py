import FirebaseSetUp
from numpy import ndarray, array
from typing import Set, Any
import spacy
import re
from collections import Counter
from vector_rep import sentence2vec


nlp = spacy.load('en_core_web_sm')
alphabet = "abcdefghijklmnopqrstuvwxyz"
words_list = open("./words.txt", "r")
vocab_non_alpha = [word[:-1].lower() for word in words_list.readlines()]
vocab = [word for word in vocab_non_alpha if word.isalpha()]
vocab.sort()
vocab_points = {}
for word in vocab:
    points = sum([alphabet.index(letter) + word.index(letter) for letter in word])
    vocab_points[word] = points
words_list.close()

slang_words = open("./slangs.txt", "r")
slangs = [slang[:-1].lower() for slang in slang_words.readlines()]
slang_words.close()


def words(text):
    return re.findall(r'\w+', text.lower())


appearance_count = Counter(words(open("big.txt").read()))


def binary_search(arr: list, item: Any) -> bool:
    """
    Search <arr> for <item> and return true if found, false otherwise.
    """
    arr_copy = arr[:]
    while len(arr_copy) > 0:
        mid_index = len(arr_copy)//2
        mid_item = arr_copy[mid_index]
        if mid_item == item:
            return True
        elif item < mid_item:
            arr_copy = arr_copy[:mid_index]
        else:
            arr_copy = arr_copy[mid_index + 1:]
    return False


def extract_known_words(potential_words: Set[str]) -> Set[str]:
    """
    From the set of <potential_words>, return the set of words that exist in the dictionary.
    """
    # initializes empty known words set
    known_words = set()

    # get all the lengths of the potential words
    lengths = list(set([len(word) for word in potential_words]))

    # the dictionary of vocab to look at for certain lengths
    lengths_dict = {}

    # loop over every length
    for length in lengths:
        words_dict = {}
        sorted_dict = {}
        for word in vocab_points:
            if len(vocab) == length:
                if vocab_points[word] not in words_dict:
                    words_dict[vocab_points[word]] = [word]
                else:
                    words_dict[vocab_points[word]].append(word)

        keys = list(words_dict.keys())
        keys.sort()
        for key in keys:
            sorted_dict[key] = words_dict[key]
        lengths_dict[length] = sorted_dict

    # loop over all the potential words
    for word in potential_words:
        # get the correct score : word dictionary
        scores_dict = lengths_dict[len(word)]
        keys = list(scores_dict.keys())
        word_score = sum([alphabet.index(letter.lower()) + word.index(letter) for letter in word])

        # binary search
        found_score = binary_search(keys, word_score)
        found_word = False
        if found_score:
            found_word = binary_search(scores_dict[word_score], word)

        if found_word:
            known_words.add(word)

    return known_words


def one_edit(word) -> Set[str]:
    """
    Return all the words that are one edit away from <word>.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    # split the word into part left and part right with increasing separating indices
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    # words formed if deleted last letter of the right split
    deletions = [left + right[1:] for left, right in splits if len(right) >= 1]

    # words formed if any 2 subsequent letters in the word are swapped
    transpositions = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]

    # words formed by replacing each letter of the word by another letter in the alphabet
    replacements = [left + new_letter + right[1:] for left, right in splits if len(right) >= 1
                    for new_letter in alphabet]

    # words formed by adding any letter from the alphabet into any position of the word
    insertions = [left + new_letter + right for left, right in splits for new_letter in alphabet]
    return set(deletions + replacements + transpositions + insertions)


def two_edits(word: str) -> Set[str]:
    """
    Return all the words that are 2 edits away from <word>.
    """
    one_edit_away = one_edit(word)
    two_edits_away = []
    for one_edit_word in one_edit_away:
        another_edit = one_edit(one_edit_word)
        two_edits_away += another_edit
    return set(two_edits_away)


def possible_corrections(word: str) -> Set[str]:
    """
    Get the possible spelling corrections for <word>.
    """
    known_original = extract_known_words({word})
    if len(known_original) > 0:
        return extract_known_words({word})
    known_one_edit = extract_known_words(one_edit(word))
    if len(known_one_edit) > 0:
        return known_one_edit
    two_editions = two_edits(word)
    known_two_edits = extract_known_words(two_editions)
    if len(known_two_edits):
        return known_two_edits
    return {word}


def probability(word, total_words=sum(appearance_count.values())):
    """
    The probability of the word appearing in big.txt.
    """
    return appearance_count[word]/total_words if word in appearance_count else 0


def predict_autocorrect(word):
    """
    The autocorrect prediction for <word>.
    """
    return max(possible_corrections(word), key=probability)


def extract_features(sentence: str) -> ndarray:
    """
    Return a numpy array of the features.
    """
    sentence_parsed = nlp(sentence)

    num_pronouns = 0
    num_corconj = 0
    num_pastverb = 0
    num_futureverb = 0
    num_commas = 0
    num_multipunc = 0
    num_common_nouns = 0
    num_proper_nouns = 0
    num_adv = 0
    num_wh = 0
    num_slangs = 0
    num_uppercase = 0

    token_lengths = []

    for index in range(len(sentence_parsed)):
        token = sentence_parsed[index]
        token_text = token.text.lower()

        # SPELL CHECK OR IDENTIFY IF IT IS A SLANG WORD
        # if word is not in dictionary
        if token_text not in vocab:
            if token_text in slangs:
                num_slangs += 1
            elif token_text.isalpha() and token.pos_ != "PUNC" and token.pos_ != "PROPN":
                token_text = predict_autocorrect(token_text)

        # append length
        token_lengths.append(len(token_text))

        # CHECK POS

        # pronoun token
        if token.pos_ == "PRON":
            num_pronouns += 1

        # proper noun token
        elif token.pos_ == "PROPN":
            num_proper_nouns += 1

        # adverb token
        elif token.pos_ == "ADV":
            num_adv += 1

        # check if is common noun
        elif token.pos_ == "NOUN":
            num_common_nouns += 1

        # ===================

        # CHECK TAGS

        # coordinate conjunction token
        if token.tag_ == "CC":
            num_corconj += 1

        # past tense verb
        elif token.tag_ == "VBD":
            num_pastverb += 1

        # multi-character punctuation
        elif token.tag_ == "NFP":
            num_multipunc += 1

        # ===================

        # CHECK OTHER INFO

        # future verb token
        if token_text == "will" or (index < len(sentence_parsed) - 2
                                and token_text == "going"
                                and sentence_parsed[index + 1].text == "to"
                                and sentence_parsed[index + 2].tag_ == "VB"):
            num_futureverb += 1

        # comma token
        if token_text == ",":
            num_commas += 1

        # wh- token
        if len(token_text) >= 2 and token_text[:2] == "wh":
            num_wh += 1

        # uppercase words with length >= 3
        if len(token_text) >= 3 and token_text.isupper():
            num_uppercase += 1

    avg_token_length = sum(token_lengths)/len(sentence_parsed)
    sentence_size = len(sentence_parsed)

    sentence_vector = sentence2vec(sentence)

    # features = [num_pronouns, num_corconj, num_pastverb, num_futureverb, num_commas, num_multipunc, num_common_nouns,
    #             num_proper_nouns, num_adv, num_wh, num_slangs, num_uppercase, avg_token_length, sentence_size,
    #             sentence_vector]

    return array(sentence_vector)


if __name__ == "__main__":
    print("korrectud", predict_autocorrect("korrectud"))