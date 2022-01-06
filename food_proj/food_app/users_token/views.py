from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.functional import wraps
from passlib.hash import pbkdf2_sha256
from geopy.geocoders import Nominatim
from get_food.views import display, random_picker
import jwt
import datetime
import pymongo
import requests
import geocoder



app = {}
app['SECRET_KEY'] = 'thisisthesecretkey'

client = pymongo.MongoClient("mongodb://localhost:27017/")  # connect to db
db = (
    client.user_tokens
)

# curl http://127.0.0.1:8000/auth/ -H "Authorization:{Bearer:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjpudWxsLCJleHAiOjE2NDE0MzE0ODJ9.Dhbb6W3kqhDLKZaQCsQWEWkUM8g7ZtvAyYUB3g8tTjk}" --data 'cost=$&rating=2'

def check_for_token(func):
    """Purpose: To verify token is sent in request
    Return Value: wrapped = Verification
    """
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        # look up jwt.decode
        token = request.headers['Authorization']
        token = token.split(':')
        token = token[-1][0:-1]
        if not token:
            return JsonResponse({'message': 'Missing Token!'}), 401
        try:
            data = jwt.decode(token, app['SECRET_KEY'], algorithms=["HS256"])
        except Exception as e:
            return JsonResponse({'Message': 'Expired Token'})
        return func(request, token, *args, **kwargs)
    return wrapped

def index(request):
    """Purpose: Issue token to new and existing users
    Parameters: request
    Return Value: rendering of a template
    """
    request.session['logged_in'] = False
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        return "Currently Not Logged In"

def public(request):
    """Purpose: To serve as public endpoint where all users can view information
    Parameters: request
    Return Value: JsonResponse - response showing request was successful
    """
    return JsonResponse({'Success': "Anyone can view this"})

@check_for_token
@csrf_exempt
def auth(request, token):
    """Purpose: To serve as endpoint where users pass in token and data to receive desired response
    Parameters: request
                token - The issued token used for verification
    Return Value: JsonResponse - response showing request was successful with desired information
    """
    user = db.user_tokens.find_one({"token": token})
    cost = request.POST.get('cost')
    rating = int(request.POST.get('rating'))

    my_location = geocoder.ip('me')

    my_restaurant = random_picker(cost, rating, my_location.address)

    response_dict = {'Success': 'Hello %s, Here is your restaurant:' % user['email'],
                        'Restaurant Name': my_restaurant['name'],
                        'Genre': my_restaurant['categories'],
                        'Rating': my_restaurant['rating'],
                        'Price': my_restaurant['price'],
                        'Location': my_restaurant['location']['address1']}

    return JsonResponse(response_dict)

def token_login(request):
    """Purpose: To serve as endpoint where users obtain a token
    Parameters: request
    Return Value: JsonResponse - response showing request was successful with desired information or
                                response showing request has failed
    """
    if request.method == 'POST':
        user = db.user_tokens.find_one({"email": request.POST.get("email")})
        if user == None:
            password = pbkdf2_sha256.encrypt(request.POST.get('password'))
            request.session['logged_in'] = True
            token_en = jwt.encode({'user': request.POST.get('username'),
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5000)},
                                app['SECRET_KEY'])

            token = jwt.decode(token_en, app['SECRET_KEY'], algorithms=["HS256"])
            # db.user_tokens.insert_one({"email": request.POST.get("email"), 'password': password, 'token': {str(datetime.datetime.utcnow()): token}})
            db.user_tokens.insert_one({"email": request.POST.get("email"), 'password': password, 'token': token_en})

            return JsonResponse({'You have been Registered': token_en})

        elif user != None:
            if user['email'] == request.POST.get("email") and pbkdf2_sha256.verify(request.POST.get('password'), user['password']):
                request.session['logged_in'] = True
                token = jwt.encode({'user': request.POST.get('username'),
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5000)},
                                    app['SECRET_KEY'])
                # db.user_tokens.update({"email": request.POST.get("email")}, {'$set': {'token.{}'.format(datetime.datetime.utcnow()): token}})
                db.user_tokens.update({"email": request.POST.get("email")}, {'$set': {'token': token}})
                print(datetime.datetime.utcnow() + datetime.timedelta(seconds=30))
                return JsonResponse({'New Token Created': token})
            else:
                return JsonResponse({'Error': 'Email Does Not Corresponds to Password'})
        else:
            return  JsonResponse({'Error': "Not Found"})
