from FirebaseSetUp import all_intentions
from training import extract_features, array
import sklearn
from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy
import sys


# classifier = SVC(kernel="linear", C=1.0)
# features = [extract_features(sentence) for sentence in all_intentions]
# # print(features)
# output = [all_intentions[sentence] for sentence in all_intentions]
# classifier.fit(features, output)
# joblib.dump(classifier, "intentions.pkl")

classifier = joblib.load("intentions.pkl", "r")
# sentences = ["I want places for dim sum", "What are some courses about Egyptian myths?",
#              "Find me some parking places near Bahen", "Are there free rooms in Galbraith?"]
sentence = sys.argv[1]
legend = {0: "food", 1: "courses", 2: "parking", 3: "rooms"}


def predict(message: str) -> str:
    """
    Predict and return the intention of the message.
    """
    features = [extract_features(message)]
    prediction = int(classifier.predict(features))
    return legend[prediction]


result = predict(sentence)
print(result)
