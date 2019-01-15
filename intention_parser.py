from FirebaseSetUp import all_intentions
from training import extract_features, array
from sklearn.svm import SVC
from sklearn.externals import joblib

classifier = SVC(kernel="linear", C=1.0)
features = [extract_features(sentence) for sentence in all_intentions]
print(features)
output = [all_intentions[sentence] for sentence in all_intentions]
classifier.fit(features, output)
joblib.dump(classifier, "intentions.pkl")

# classifier = joblib.load("intentions.pkl", "r")
# features = [extract_features("I want free rooms in Bahen.")]
# prediction = classifier.predict(features)
# legend = {0: "food", 1: "courses", 2: "parking", 3: "rooms"}
# print(prediction)