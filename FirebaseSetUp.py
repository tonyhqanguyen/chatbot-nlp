import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("apikey.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatbot0603.firebaseio.com/'
})

root = db.reference("Intentions")
entities = db.reference("Entities")
all_intentions = root.get()
all_entities = entities.get()


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

legend = {0: "food", 1: "courses", 2: "parking", 3: "rooms"}


def define_entities(data: str, position: str):
    """
    Write the entity indices to Firebase.
    """
    entities.child(data).push({
        "label": legend[all_intentions[data]],
        position: "keyword"
    })


if __name__ == "__main__":
    BOLD = '\033[1m'
    END = '\033[0m'
    lst = list(all_intentions.keys())[524:]
    i = 525

    for sentence in lst:
        print(f"{BOLD} {i}/535 {END}")
        i += 1
        if len(sentence.split(" ")) == 1:
            define_entities(sentence, f"{0} {len(sentence)}")
        else:
            print("Sentence: ", f"{BOLD} {sentence} {END}")
            print("Sentence length: ", f"{BOLD} {len(sentence)} {END}")
            split = sentence.split(" ")
            for token in split:
                print("Token: ", f"{BOLD} {token} {END}")
                print("Starting index: ", f"{BOLD} {sentence.find(token)} {END}")
                print("Ending index: ", f"{BOLD} {sentence.find(token) + len(token)} {END}")
                print("-----------------")

            indices = input("Input the desired token indices (start and end): ")
            print("You inputted: ", indices)
            while "/" not in indices:
                print("You need a slash")
                indices = input("Input the desired token indices (start and end): ")
                print("You inputted: ", input)

            slash = indices.index("/")
            beginning = indices[:slash]
            end = indices[slash + 1:]

            while not beginning.isdigit() or not end.isdigit():
                print("You put in non numeric values")
                indices = input("Input the desired token indices (start and end): ")
                print("You inputted: ", indices)
                slash = indices.index("/")
                beginning = indices[:slash]
                end = indices[slash + 1:]

            beginning = int(beginning)
            end = int(end)

            while beginning < 0:
                print("Your starting index is before the beginning of the string")
                indices = input("Input the desired token indices (start and end): ")
                print("You inputted: ", indices)
                slash = indices.index("/")
                beginning = indices[:slash]
                end = indices[slash + 1:]

            while end > len(sentence):
                print("Your ending index is after the end of the string")
                indices = input("Input the desired token indices (start and end): ")
                print("You inputted: ", indices)
                slash = indices.index("/")
                beginning = indices[:slash]
                end = indices[slash + 1:]

            print("Your chosen starting index: ", beginning)
            print("Your chosen ending index: ", end)
            define_entities(sentence, f"{beginning} {end}")
            print("Processed sentence into database")
            print("===========================")
