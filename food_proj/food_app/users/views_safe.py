from django.shortcuts import render
from django.http import JsonResponse
from passlib.hash import pbkdf2_sha256  # used to hash password
import uuid  # used to make _id easier to use?
import pymongo

app = {}
app['SECRET_KEY'] = 'thisisthesecretkey'

client = pymongo.MongoClient("mongodb://localhost:27017/")  # connect to db
db = (
    client.users
)


def start_session(user):  # used in the login in class method
    """Purpose: To begin a session for a given user
    Parameters: User object
    Return Value: user information in json format
    """
    del user["password"]
    session["logged_in"] = True
    session["user"] = user

    return jsonify(user), 200


#     def signout(self):  # used in html as endpoint on logout page
#         """Purpose: To sign a user out
#         Parameters: N/a
#         Return Value: redirects to html user login/sign up page
#         """
#         session.clear()
#         return redirect("/")
#
#     def login(self):  # used in routes as login endpoint
#         """Purpose: To login a user to their account
#         Parameters: N/a
#         Return Value: if user not found - Error response
#                         if user found - session is started with the user
#         """
#         user = db.users.find_one({"email": request.form.get("email")})
#
#         if user and pbkdf2_sha256.verify(
#             request.form.get("password"), user["password"]
#         ):
#             return self.start_session(user)
#
#         return jsonify({"error": "Invalid Credentials"}), 401
#
#     def add_ballot_name(self, item):
#         """Purpose: To add ballot
#         Parameters: item - ballot name given by user
#         Return Value: Json Response
#         """
#         session["ballot_items"] = item
#         db.users.update(
#             {"email": session["user"]["email"]},
#             {"$set": {"ballot_items.{}".format(item): {}}},
#         )
#         return jsonify({"success": "Ballot added"}), 200
#
#     def add_ballot_item(self, item_name, image, description):
#         """Purpose: To add information for a given item in a ballot
#         Parameters: item_name - Name of given item
#                     image - URL of inputted image
#                     description - Description of an item
#         Return Value: Json Response
#         """
#         db.users.update(
#             {"email": session["user"]["email"]},
#             {
#                 "$set": {
#                     "ballot_items.{}.{}".format(session["ballot_items"], item_name): {
#                         "image": image,
#                         "description": description,
#                         "votes": 0,
#                     }
#                 }
#             },
#         )
#         return jsonify({"success": "Item added"}), 200
#
#
# def get_ballots():
#     """Purpose: To get all ballots of a given user for display on dashboard
#     Parameters: N/a
#     Return Value: If ballots found, a Dictionary containing all information of all ballots
#                     If no ballots found, an error code
#     """
#     new_dict = {}
#     ballots = db.users.find({"email": session["user"]["email"]})
#     ballots = list(ballots)
#
#     for item in ballots:
#         name = item["name"]
#         new_dict[name] = item
#
#     my_keys = list(new_dict[session["user"]["name"]].keys())
#
#     if "ballot_items" in my_keys:
#         ballot_item_dict = new_dict[session["user"]["name"]]["ballot_items"]
#         return ballot_item_dict
#     return {"No Ballots": "Make Some Ballots!"}
#
#
# def get_email():
#     """Purpose: To obtain email of the user
#     Parameters: N/a
#     Return Value: Users email address
#     """
#     return session["user"]["email"]
#
#
# def del_img(item, ballot_name):
#     """Purpose: To remove an item from a ballot
#     Parameters: item - Name of ballot item that will be removed
#                 ballot_name - Name of ballot that item is found in
#     Return Value:
#     """  # find given value and sets it to ''
#     # then finds where given route is set to '' and removes it
#     db.users.update(
#         {"email": session["user"]["email"]},
#         {"$set": {"ballot_items.{}.{}".format(ballot_name, item): ""}},
#     )
#     db.users.update(
#         {"email": session["user"]["email"]},
#         {"$unset": {"ballot_items.{}.{}".format(ballot_name, item): ""}},
#     )
#     x = db.users.find(
#         {"email": session["user"]["email"]}, {"ballot_items.{}".format(ballot_name)}
#     )
#     x = list(x)
#     if len(x[0]["ballot_items"][ballot_name]) == 0:
#         db.users.update(
#             {"email": session["user"]["email"]},
#             {"$unset": {"ballot_items.{}".format(ballot_name): ""}},
#         )
#
#
# def get_items_voter(ballot_name):
#     """Purpose: To obtain items of a given ballot
#     Parameters: ballot_name - Ballot name
#     Return Value: Items found in ballot or Error Response
#     """
#     new_dict = {}
#     ballots = db.users.find({"email": session["user"]["email"]})
#     ballots = list(ballots)
#     for item in ballots:
#         name = item["name"]
#         new_dict[name] = item
#     ballots = ballots[0]  # converts list of dict to a dict
#
#     if not ballots["ballot_items"][ballot_name]:
#         return {"error": "No items found"}
#     if ballots["ballot_items"][ballot_name]:
#         return ballots["ballot_items"][ballot_name]
#     return {"error": "No items found"}
#
#
# def vote(item, ballot_name):
#     """Purpose: To allow voting functionality
#     Parameters: item - Name of item that is being voted for
#                 ballot_name - Name of the ballot the item belongs to
#     Return Value: The amount of votes for a given item
#     """
#     db.users.update(
#         {"email": session["user"]["email"]},
#         {"$inc": {"ballot_items.{}.{}.votes".format(ballot_name, item): 1}},
#     )
#     ballots = db.users.find(
#         {"email": session["user"]["email"]}, {"ballot_items.{}".format(ballot_name)}
#     )
#     ballots = list(ballots)[0]
#     total_votes = ballots["ballot_items"][ballot_name][item]["votes"]
#     return total_votes
#
#



def home(request):
    return render(request, 'signup.html')

def signup(request):
    if request.method == 'POST':
        user = {  # Create user object
            "_id": uuid.uuid4().hex,
            "name": request.POST.get('username'),
            "email": request.POST.get('email'),
            "password": request.POST.get('password')
        }
        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        if db.users.find_one({"email": user["email"]}):
            return JsonResponse({"error": "Email already in use"})

        if db.users.insert_one(
            user
        ):
            return JsonResponse({"Success": "Account Created", current_user: start_session(user)})
        #
        # if db.users.find_one({"email": user["email"]}):
        #     return JsonResponse({"error": "Email already in use"})
        #
        # if db.users.insert_one(
        #     user
        # ):
        #     return start_session(
        #         user
        #     )
        #
        # return JsonResponse({"error": "Sign Up failed"})
