from django.shortcuts import render
from django.db import models

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

def create_url(request):
    url = 'https://api.yelp.com/v3/businesses/search?'
    return url

def parameters(request, location):
    params = {'term': 'food',
                 'limit': 50,
                 'offset': 50,
                 'radius': 10000,
                 'location': location}
    return params

def credentials(request):
    API_KEY = '2E7rOgAXr-suArMqgPvLy0dF6YKqKzH26MhFSi6-23fF3qfsZjkysaeT_E9mWgrU_NVBpp4D7Tz-jmarCmx_wLtxoCNlH-j_2mFCW7yHS_nLr1pJ4B-ArBEXNS12YXYx'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}
    return HEADERS

def store_info(request, business_data):
    wanted_info = {}
    for line in business_data:
        restaurant_obj = Restaurant_info(line['name'])
        restaurant_obj.id = line['id']
        restaurant_obj.alias = line['alias']
        restaurant_obj.is_closed = line['is_closed']
        restaurant_obj.categories = line['categories']
        restaurant_obj.rating = line['rating']
        restaurant_obj.coordinates = line['coordinates']
        restaurant_obj.transactions = line['transactions']
        if 'price' in line:
            restaurant_obj.price = line['price']
        restaurant_obj.location = line['location']

        wanted_info[restaurant_obj.name] = json.loads(json.dumps(restaurant_obj.__dict__))

    return wanted_info

def send_cred(request):
    headers = credentials(request)
    url = create_url(request)
    params = parameters(request, 'Waukegan')
    response = requests.get(url = url,
                            params = params,
                            headers = headers)
    return response

def fix_info(request):
    response = send_cred(request)
    fixed_data = json.loads(response.content.decode('UTF-8'))

    business_data = fixed_data['businesses']
    wanted_store_info = store_info(request, business_data)

    return wanted_store_info

def random_picker(price, rating):
    wanted_store_info = fix_info()
    options = []
    price_ranker = price.count("$")
    for key, value in wanted_store_info.items():
        if value['price'] != None:
            if value['price'].count("$") <= price_ranker:
                if value['is_closed'] != "False":
                    if value['rating'] >= rating:
                        options.append(value['name'])
    choice = random.choice(options)
    return choice

def display(request, *args, **kwargs):
    wanted_store_info = fix_info(request)
    print(request.GET)
    test = {
        'restaurant_dict': wanted_store_info
    }
    return render(request, 'home.html', test)
