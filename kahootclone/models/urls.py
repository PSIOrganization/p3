'''
File: urls.py
Contains all the urls relevant to the kahootclone project
'''

from django.urls import path
from . import views

# Here we will add all urls relevant to the models app

urlpatterns = [
     path('signup', views.SignUp.as_view(), name='signup'),
]
