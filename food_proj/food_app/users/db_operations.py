import pymongo

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
    if db.users.update({'email': email}, {'$set': {'Notes.{}'.format(name): {'note': note, 'rating': rating}}}):
        return 'Note Added'
    return 'Note Was Not Added'
