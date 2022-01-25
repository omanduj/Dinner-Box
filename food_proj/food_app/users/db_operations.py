from config import USERNAME, PASSWORD
import pymongo
import datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")
# client = pymongo.MongoClient("mongodb://{}:{}@mongodb_container:127.0.0.1".format(USERNAME, PASSWORD))
db = client.users

# --------------------------- Users ---------------------#


def find_one_user(email):
    """Purpose: To find if a user exists in database
    Parameters: email - The email used to register a user
    Return Value: True - If user is found
                    False - If user is not fount
    """
    if db.users.find_one({"email": email}):
        return True
    return False


def insert_one_user(email):
    """Purpose: To create a new user
    Parameters: email - The email used to register a user
    Return Value: True - If the user was created successfuly
                    False - If the user was not created
    """
    if db.users.insert_one(email):
        return True
    return False


def get_one_user(email):
    """Purpose: To obtain information pertaining to a user
    Parameters: email - The email used to register a user
    Return Value: user - The information pertaining to a user
                    False - If no user if found
    """
    if db.users.find_one({"email": email}):
        user = db.users.find_one({"email": email})
        return user
    return False




def add_note(email, name, note, rating):
    """Purpose: To add a note to a users account
    Parameters: email - The email used to register a user
                name - The name of the restaurant
                note - The note pertaining to the restaurant
                rating - The rating pertaining to the restaurant
    Return Value: Notification whethet a note was added successfully or not
    """
    # check if note with restaurant already exists, if it does  notify the user
    if db.users.update(
        {"email": email},
        {
            "$set": {
                "Notes.{}".format(name): {
                    "note": note,
                    "rating": rating,
                    "date": datetime.datetime.utcnow(),
                }
            }
        },
    ):
        return "Note Added"
    return "Note Was Not Added"


def check_note_exists(email, name):
    """Purpose: To check if a note for a given restaurant already exists or not
    Parameters: email - The email used to register a user
                name - The name of the restaurant
    Return Value: note - The note already stored with the given name
    """
    note = db.users.find_one({"email": email}, {"Notes.{}".format(name)})
    return note


def get_user_notes(email):
    """Purpose: To retrieve notes that are under a given users account
    Parameters: email - The email used to register a user
    Return Value: notes - The notes stored pertaining to a given user
    """
    notes = db.users.find({"email": email}, {"Notes"})
    return notes


# def get_user_notes_sorted_rating(email):
#     notes = db.users.find({'email': email}).sort('Notes', 1)
#     return notes


def delete_note(email, restaurant_name):
    """Purpose: To remove a restaurants note from a users account
    Parameters: email - The email used to register a user
                restaurant_name - The name of the restaurant to be deleted
    Return Value: notes_found - The notes registed to the user minus the previously deleted note
    """
    db.users.update(
        {"email": email},
        {"$set": {"Notes.{}".format(restaurant_name): ""}},
    )
    db.users.update(
        {"email": email},
        {"$unset": {"Notes.{}".format(restaurant_name): ""}},
    )
    note_found = db.users.find({"email": email})

    notes_found = list(note_found)[0]["Notes"]
    return notes_found
