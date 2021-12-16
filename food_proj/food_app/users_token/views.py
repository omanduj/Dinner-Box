from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.utils.functional import wraps
from .models import AuthForm
import jwt
import datetime

app = {}
app['SECRET_KEY'] = 'thisisthesecretkey'

# Create your views here.
def check_for_token(func):
    @wraps(func, requests)
    def wrapped(*args, **kwargs):
        token = request.session.get("token")
        if not token:
            return JsonResponse({'message': 'Missing Token!'}), 401
        try:
            data = jwt.decode(token, app['SECRET_KEY'], algorithms=["HS256"])
        except:
            return JsonResponse({'Message': 'Invalid Token'})
        return func(*args, **kwargs)
    return wrapped



     
def index(request):
    request.session['logged_in'] = False
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        print(request.session)
        return "Currently Not Logged In"

def public(request):
    return JsonResponse({'Success': "Anyone can view this"})

@check_for_token
def auth(request):
    return JsonResponse({'Success': "Only Viewable with a token"})


def login(request):
    if request.method == 'POST':
        if request.POST.get('username') == 'omanduj' and request.POST.get('password') == 'password':
                request.session['logged_in'] = True
                token = jwt.encode({'user': request.POST.get('username'),
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)},
                                    app['SECRET_KEY'])
                return JsonResponse({'token': token})
        else:
            return JsonResponse({'Error': "Not Found"})
    else:
        return JsonResponse({'Error': "Not Found"})
