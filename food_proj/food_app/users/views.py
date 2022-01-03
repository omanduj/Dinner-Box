from django.shortcuts import render, redirect
from django.http import JsonResponse
from passlib.hash import pbkdf2_sha256  # used to hash password
from users.db_operations import insert_one_user, find_one_user, get_one_user
import uuid  # used to make _id easier to use?

# request.session["user"] // stores info in it

def start_session(request, user):
    """Purpose: To begin a session for a given user
    Parameters: User object
    Return Value: user information in json format
    """
    del user["password"]
    request.session["logged_in"] = True
    request.session["user"] = user

    return user

def signup_user(request):  # used in routes signup endpoint
    """Purpose: To sign up a new user for service
    Parameters: N/a
    Return Value: Json Response
    """
    user = {  # Create user object
        "_id": uuid.uuid4().hex,
        "name": request.POST.get('username'),
        "email": request.POST.get('email'),
        "password": request.POST.get('password')
    }

    user["password"] = pbkdf2_sha256.encrypt(user["password"])

    if find_one_user(user["email"]):
        return {"error": "Email already in use"}

    if insert_one_user(user):
        start_session(request, user)
        return {'Success': 'User Created!'}

    return {"Error": "Sign Up failed"}

# playgirllibby

def login_user(request):  # used in routes as login endpoint
    """Purpose: To login a user to their account
    Parameters: N/a
    Return Value: if user not found - Error response
                    if user found - session is started with the user
    """
    user = get_one_user(request.POST.get('email'))
    password = request.POST.get('password')
    if user and pbkdf2_sha256.verify(request.POST.get('password'), user["password"]):
        return start_session(request, user)

    return ("Invalid Credentials")




def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        response = signup_user(request)
        return render(request, 'dashboard.html', {'user': response})

def login(request):
    if request.method == 'POST':
        print(request.session["user"])
        response = login_user(request)
        return render(request, 'dashboard.html', {'user': response})

def signout(request):
    request.session.clear()
    return redirect("/home/")
