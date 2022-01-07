from django.shortcuts import render
from django.db import models
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
    url = 'https://api.yelp.com/v3/businesses/search?'
    return url

def parameters(location):
    params = {'term': 'food',
                 'limit': 50,
                 'offset': 50,
                 'radius': 10000,
                 'location': location}
    return params

def credentials():
    key = '2E7rOgAXr-suArMqgPvLy0dF6YKqKzH26MhFSi6-23fF3qfsZjkysaeT_E9mWgrU_NVBpp4D7Tz-jmarCmx_wLtxoCNlH-j_2mFCW7yHS_nLr1pJ4B-ArBEXNS12YXYx'
    headers = {'Authorization': 'bearer %s' % key}
    return headers

def send_cred(location):
    headers = credentials()
    url = create_url()
    params = parameters(location)
    response = requests.get(url = url,
                            params = params,
                            headers = headers)
    return response

def restaurant_collection(restaurant_data):
    all_restaurant_info = {}
    for restaurant in restaurant_data:
        restaurant_obj = Restaurant_info(restaurant['name'])
        restaurant_obj.id = restaurant['id']
        restaurant_obj.alias = restaurant['alias']
        restaurant_obj.is_closed = restaurant['is_closed']
        restaurant_obj.categories = restaurant['categories']
        restaurant_obj.rating = restaurant['rating']
        restaurant_obj.coordinates = restaurant['coordinates']
        restaurant_obj.transactions = restaurant['transactions']
        if 'price' in restaurant:
            restaurant_obj.price = restaurant['price']
        restaurant_obj.location = restaurant['location']

        all_restaurant_info[restaurant_obj.name] = json.loads(json.dumps(restaurant_obj.__dict__))

    return all_restaurant_info

def format_info(location):
    response = send_cred(location)
    restaurant_info = json.loads(response.content.decode('UTF-8'))
    business_data = restaurant_info['businesses']
    all_restaurant_info = restaurant_collection(business_data)

    return all_restaurant_info

def random_picker(price, rating, location):
    restaurant_info = format_info(location)
    options = []
    price_ranker = price.count("$")
    for restaurant_name, restaurant_description in restaurant_info.items():
        if restaurant_description['price'] != None:
            if restaurant_description['price'].count("$") <= price_ranker:
                if restaurant_description['is_closed'] != "False":
                    if restaurant_description['rating'] >= rating:
                        options.append(restaurant_description)
    choice = random.choice(options)
    return choice

def display(location, *args, **kwargs):
    restaurant_info = format_info(location)
    test = {
        'restaurant_dict': restaurant_info
    }
    return test
    # return render(request, 'home.html', test)
