from vector_rep import sentence2vec
from sklearn.externals import joblib
from app import *
from flask import jsonify

classifier = joblib.load("intentions.pkl", "r")
legend = {0: "food", 1: "courses", 2: "parking", 3: "rooms"}


def predict(message: str) -> str:
    """
    Predict and return the intention of the message.
    """
    features = [sentence2vec(message)]
    prediction = int(classifier.predict(features))
    return legend[prediction]


@app.route("/intention", methods=["POST"])
def get_intention():
    inputs = get_inputs()
    response = {
        "intention": predict(inputs["message"])
    }

    return jsonify(response), 200
