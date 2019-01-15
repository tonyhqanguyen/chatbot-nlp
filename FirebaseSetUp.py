import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/tonynguyen/Desktop/ML/chatbot-nlp/chatbot0603-firebase-adminsdk-fvju5-d1aa135919.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatbot0603.firebaseio.com/'
})

root = db.reference("Intentions")
all_intentions = root.get()


# food = 0
# courses =
for sentence in all_intentions:
    if all_intentions[sentence] == "food":
        all_intentions[sentence] = 0
    elif all_intentions[sentence] == "courses":
        all_intentions[sentence] = 1
    elif all_intentions[sentence] == "parking":
        all_intentions[sentence] = 2
    else:
        all_intentions[sentence] = 3

all_intentions: dict
# data = {
#     "courses": {
#         "examples": [],
#         "centroid": None
#     },
#     "food": {
#         "examples": [],
#         "centroid": None
#     },
#     "parking": {
#         "examples": [],
#         "centroid": None
#     },
#     "rooms": {
#         "examples": [],
#         "centroid": None
#     }
# }
#
# for key in all_intentions:
#     data[all_intentions[key]]["examples"].append(key)
#
# all_intentions: dict

