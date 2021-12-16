from django.db import models
from django import forms

# Create your models here.
class AuthForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_password = forms.CharField(label='Your password', max_length=100)
