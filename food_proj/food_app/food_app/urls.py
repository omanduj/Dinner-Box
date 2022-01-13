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

from get_food.views import display, peronal_picker
from users_token.views import index, token_login, public, auth, token_instructions
from users.views import home, signup, login, signout, food_random_picker
from notes.views import create_note, view_notes, delete_user_note, view_notes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_food/', display),             #used to display all restaurants (to be removed) - GET
    path('public/', public),                ###To be used to display information
    path('auth/', auth),                    #used to provide authentication to users with tokens - POST
    path('home/', home),                    ###To be used to sign up and login users to their dashboard

    path('token/', index),                  #used to give new tokens to users - GET -> login/
    path('token/login/', token_login),                  #used to save user token info and display token - POST
    path('user/token/instructions/', token_instructions),

    path('user/signup/', signup),
    path('user/signout/', signout),
    path('user/dashboard/', login),
    path('user/personal_picks/', peronal_picker),
    
    # path('user/notes/', login),             #?

    path('user/create-notes/', create_note),
    path('user/view-notes', view_notes),
    path('user/delete-note/', delete_user_note),
    path('user/order/', view_notes),

    path('user/foodpicker/', food_random_picker)
]
