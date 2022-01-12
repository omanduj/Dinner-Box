import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = (
    client.users
)

#--------------------------- Users ---------------------#

def find_one_user(email):
    if db.users.find_one({"email": email}):
        return True
    return False

def insert_one_user(email):
    if db.users.insert_one(email):
        return True
    return False

def get_one_user(email):
    if db.users.find_one({"email": email}):
        user = db.users.find_one({"email": email})
        return user
    return False

#--------------------------- Notes ---------------------#

def add_note(email, name, note, rating):
    #check if note with restaurant already exists, if it does  notify the user
    if db.users.update({'email': email}, {'$set': {'Notes.{}'.format(name): {'note': note, 'rating': rating, 'date': datetime.datetime.utcnow()}}}):
        return 'Note Added'
    return 'Note Was Not Added'

def check_note_exists(email, name):
    note = db.users.find_one({'email': email}, {'Notes.{}'.format(name)})
    return note

def get_user_notes(email):
    notes = db.users.find({'email': email}, {'Notes'})
    return notes

# def get_user_notes_sorted_rating(email):
#     notes = db.users.find({'email': email}).sort('Notes', 1)
#     return notes

def delete_note(email, restaurant_name):
    db.users.update(
        {"email": email},
        {"$set": {"Notes.{}".format(restaurant_name): ""}},
    )
    db.users.update(
        {"email": email},
        {"$unset": {"Notes.{}".format(restaurant_name): ""}},
    )
    note_found = db.users.find(
        {"email": email}
    )

    notes_found = list(note_found)[0]['Notes']
    return notes_found
