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
        "name": request.POST.get('username'),
        "email": request.POST.get('email'),
        "password": request.POST.get('password'),
    }

    user["password"] = pbkdf2_sha256.encrypt(user["password"])

    if find_one_user(user["email"]):
        return {"error": "Email already in use"}

    if insert_one_user(user):
        start_session(request, user)
        return {'Success': 'User Created!'}

    return {"Error": "Sign Up failed"}

def login_user(request):
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



def food_random_picker(request):
    if request.method == 'GET':
        return render(request, 'food_finder.html')

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        cost = request.POST.get('cost')
        my_location = geocoder.ip('me')
        my_restaurant = random_picker(cost, rating, my_location.address)

        response_dict = {
                        'Restaurant Name': my_restaurant['name'],
                        'Genre': my_restaurant['categories'],
                        'Rating': my_restaurant['rating'],
                        'Price': my_restaurant['price'],
                        'Location': my_restaurant['location']['address1']}

        return JsonResponse({'You have been Registered': response_dict})


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        response = signup_user(request)
        return render(request, 'dashboard.html', {'user': response})

def login(request):
    if request.method == 'POST':
        response = login_user(request)
        if response != 'Invalid Credentials':
            del response['Notes']
            response['name'] = response['name'].capitalize()
            return render(request, 'dashboard.html', {'user': response})
        if response == 'Invalid Credentials':
            return render(request, 'dashboard.html', {'response': response})

    if request.method == 'GET':
        if request.session['user']:
            user = get_one_user(request.session['user']['email'])
            del user['password']
            user['name'] = user['name'].capitalize()
            return render(request, 'dashboard.html', {'user': user})
        if response == 'Invalid Credentials':
            return render(request, 'dashboard.html', {'response': response})

def signout(request):
    request.session.clear()
    return redirect("/home/")
