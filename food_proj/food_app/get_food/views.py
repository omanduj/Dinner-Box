from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from users.db_operations import get_user_notes
import random
import requests
import json

# Create your views here.
class Restaurant_info(models.Model):
    def __init__(self, name):
        self.name = name
        self.id = None
        self.alias = None
        self.is_closed = None
        self.categories = None
        self.rating = None
        self.coordinates = None
        self.transactions = None
        self.price = None
        self.location = None


def create_url():
    """Purpose: To create Yelp url endpoint that will be hit
    Parameters: N/a
    Return Value: url - URL endpoing that will yield desired information
    """
    url = "https://api.yelp.com/v3/businesses/search?"
    return url


def parameters(location):
    """Purpose: To set up parameters that will be sent to the yelp api
    Parameters: location - Location of user obtained
    Return Value: params - Formatted information that will be sent to yelp api
    """
    params = {
        "term": "food",
        "limit": 50,
        "offset": 50,
        "radius": 10000,
        "location": location,
    }
    return params


def credentials():
    """Purpose: To obtain the key required by the yelp api
    Parameters: N/a
    Return Value: headers - information formatted in required format
    """
    key = "2E7rOgAXr-suArMqgPvLy0dF6YKqKzH26MhFSi6-23fF3qfsZjkysaeT_E9mWgrU_NVBpp4D7Tz-jmarCmx_wLtxoCNlH-j_2mFCW7yHS_nLr1pJ4B-ArBEXNS12YXYx"
    headers = {"Authorization": "bearer %s" % key}
    return headers


def send_cred(location):
    """Purpose: To send a request to the previously defined endpoint with the informationf formatted in the parameter and
                credentials functions
    Parameters: location - Current location of the user
    Return Value: response - Information of restaurants in the area
    """
    headers = credentials()
    url = create_url()
    params = parameters(location)
    response = requests.get(url=url, params=params, headers=headers)
    return response


def restaurant_collection(restaurant_data):
    """Purpose: To clean information returned from api request into desired format
    Parameters: restaurant_data - The information provided by yelp about restaurants in the area
    Return Value: all_restaurant_info - A dictionary with all desired information cleaned and formatted
    """
    all_restaurant_info = {}
    for restaurant in restaurant_data:
        restaurant_obj = Restaurant_info(restaurant["name"])
        restaurant_obj.id = restaurant["id"]
        restaurant_obj.alias = restaurant["alias"]
        restaurant_obj.is_closed = restaurant["is_closed"]
        restaurant_obj.categories = restaurant["categories"]
        restaurant_obj.rating = restaurant["rating"]
        restaurant_obj.coordinates = restaurant["coordinates"]
        restaurant_obj.transactions = restaurant["transactions"]
        if "price" in restaurant:
            restaurant_obj.price = restaurant["price"]
        restaurant_obj.location = restaurant["location"]

        all_restaurant_info[restaurant_obj.name] = json.loads(
            json.dumps(restaurant_obj.__dict__)
        )

    return all_restaurant_info


def format_info(location):
    """Purpose: To format yelp api response into usable information
    Parameters: location - Current location of the use
    Return Value: all_restaurant_info - Unstructured information will yelp api response
    """
    response = send_cred(location)
    restaurant_info = json.loads(response.content.decode("UTF-8"))
    # Possible error where no info is returned, causing a 'input valid input' alert
    business_data = restaurant_info["businesses"]
    all_restaurant_info = restaurant_collection(business_data)

    return all_restaurant_info


def random_picker(price, rating, location):
    """Purpose: To select a restaurant based on user inputted criteria
    Parameters: price - The desired expensivness of a restaurant in the format of $, $$, or $$$
                rating - The minimum desired rating for a restaurant
                location - Current location of the use
    Return Value: choice - A randomly selected restaurant with all relevant information such as location, rating, and type of food
    """
    restaurant_info = format_info(location)
    options = []
    price_ranker = price.count("$")
    for restaurant_name, restaurant_description in restaurant_info.items():
        if restaurant_description["price"] != None:
            if restaurant_description["price"].count("$") <= price_ranker:
                if restaurant_description["is_closed"] != "False":
                    if restaurant_description["rating"] >= rating:
                        options.append(restaurant_description)
    choice = random.choice(options)
    return choice


def display(location, *args, **kwargs):
    """Purpose: To obtain all information returned by yelp api
    Parameters: location - Currrent location of user
    Return Value: test - A dictionary containing all the formatted info from the yelp api response
    """
    restaurant_info = format_info(location)
    test = {"restaurant_dict": restaurant_info}
    return test
    # return render(request, 'home.html', test)


def peronal_picker(request):
    """Purpose: To randomly select restaurant from personal list that fits user criteria
    Parameters: N/a
    Return Value: A JsonResponse which is used in the scripts.js file to alter html page
    """
    if request.method == "GET":
        return render(request, "personal_food_picker.html")

    if request.method == "POST":
        rating = int(request.POST.get("rating"))

        notes = get_user_notes(request.session["user"]["email"])
        notes = list(notes)[0]["Notes"]

        options = []
        for name, info in notes.items():
            if info["rating"] >= rating:
                options.append(name)
        if len(options) != 0:
            random_option = random.choice(options)
            my_restaurant = notes[random_option]
            return JsonResponse({random_option: my_restaurant})
        return JsonResponse({"Error": "Nothing Found"})
