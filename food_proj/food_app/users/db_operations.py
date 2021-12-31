import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = (
    client.users
)

def find_one_user(username):
    if db.users.find_one({"email": username}):
        return True
    return False

def insert_one_user(username):
    if db.users.insert_one(username):
        return True
    return False

def get_one_user(username):
    if db.users.find_one({"email": username}):
        user = db.users.find_one({"email": username})
        return user
    return False
