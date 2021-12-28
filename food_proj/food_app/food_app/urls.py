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
from users.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_food/', display),
    path('users_token/', index),
    path('login/', login),
    path('public/', public),
    path('auth/', auth),
    path('home/', home)
]
