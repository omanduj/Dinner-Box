from django.shortcuts import render, redirect
from django.http import JsonResponse
from passlib.hash import pbkdf2_sha256
from geopy.geocoders import Nominatim
from users.db_operations import insert_one_user, find_one_user, get_one_user
from get_food.views import random_picker
import uuid
import geocoder

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
        "name": request.POST.get("username"),
        "email": request.POST.get("email"),
        "password": request.POST.get("password"),
    }

    user["password"] = pbkdf2_sha256.encrypt(user["password"])

    if find_one_user(user["email"]):
        return {"response": "Email already in use"}

    if insert_one_user(user):
        start_session(request, user)
        return {"response": "User Created!"}

    return {"response": "Sign Up failed"}


def login_user(request):
    """Purpose: To login a user to their account
    Parameters: N/a
    Return Value: if user not found - Error response
                    if user found - session is started with the user
    """
    user = get_one_user(request.POST.get("email"))
    password = request.POST.get("password")
    if user and pbkdf2_sha256.verify(request.POST.get("password"), user["password"]):
        return {"response": start_session(request, user)}

    return {"response": "Invalid Credentials"}


def food_random_picker(request):
    """Purpose: To serve as endpoint to return information of restaurant that fits the users criteria
    Parameters: N/a
    Return Value: JsonResponse with information of a restaurant that satisfies a certain criteria
    """
    if request.method == "GET":
        return render(request, "food_finder.html")

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        cost = request.POST.get("cost")
        my_location = geocoder.ip("me")
        my_restaurant = random_picker(cost, rating, my_location.address)

        response_dict = {
            "Restaurant Name": my_restaurant["name"],
            "Genre": my_restaurant["categories"],
            "Rating": my_restaurant["rating"],
            "Price": my_restaurant["price"],
            "Location": my_restaurant["location"]["address1"],
        }

        return JsonResponse({"You have been Registered": response_dict})


def home(request):
    """Purpose: To render the sign up/login webpage
    Parameters: N/a
    Return Value: Rendering the home.html file
    """
    if request.method == "GET":
        return render(request, "home.html")


def signup(request):
    """Purpose: To sign a user up for the service
    Parameters: N/a
    Return Value: On success it will display dashboard.html with success options
                    On Error it will display dashboard.html with error window
    """
    if request.method == "POST":
        result = signup_user(request)
        if result["response"] == "User Created!":
            return render(request, "dashboard.html", {"user": result})
        return render(request, "dashboard.html", {"response": result})


def login(request):
    """Purpose: To login a user and display dashboard capabilities
    Parameters: N/a
    Return Value: On success it will display dashboard.html with success options
                    On Error it will display dashboard.html with error window
    """
    if request.method == "POST":
        result = login_user(request)
        if result["response"] != "Invalid Credentials":
            del result["response"]["Notes"]
            result["response"]["name"] = result["response"]["name"].capitalize()
            return render(request, "dashboard.html", {"user": result})
        if result["response"] == "Invalid Credentials":
            return render(request, "dashboard.html", {"response": result})

    if request.method == "GET":
        if request.session["user"]:
            user = get_one_user(request.session["user"]["email"])
            del user["password"]
            user["name"] = user["name"].capitalize()
            return render(request, "dashboard.html", {"user": user})
        if response == "Invalid Credentials":
            print(response)
            return render(request, "dashboard.html", {"response": response})


def signout(request):
    """Purpose: To sign a user out
    Parameters: N/a
    Return Value: redirection to the sign up and login page
    """
    request.session.clear()
    return redirect("/home/")
