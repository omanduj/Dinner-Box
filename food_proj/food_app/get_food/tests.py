from django.test import TestCase
from .views import format_info, random_picker, peronal_picker, Restaurant_info
from geopy.geocoders import Nominatim

import geocoder
import json
       


class RandomTest(TestCase):
    def test_response_count(self):
        my_location = geocoder.ip("me")
        response = format_info(my_location)
        assert len(response) <= 50

    def test_random_picker(self):
        my_location = geocoder.ip("me")
        response = random_picker('$', 2, my_location)
        assert len(response) == 10

    def test_random_picker_invalid(self):
        my_location = geocoder.ip("me")
        try:
            response = random_picker('$', 9, my_location)
            assert True == False
        except:
            assert True == True

    def test_object(self):
        my_restaurant = Restaurant_info('Name')
        assert my_restaurant.name == 'Name'
