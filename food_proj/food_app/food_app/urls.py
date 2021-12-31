"""food_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from get_food.views import display
from users_token.views import index, login, public, auth
from users.views import home, signup, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_food/', display),             #used to display all restaurants (to be removed) - GET
    path('token/', index),                  #used to give new tokens to users - GET -> login/
    path('login/', login),                  #used to save user token info and display token - POST
    path('public/', public),                ###To be used to display information
    path('auth/', auth),                    #used to provide authentication to users with tokens - POST
    path('home/', home),                    ###To be used to sign up and login users to their dashboard
    path('signup/', signup),
    path('login/', login)
]
