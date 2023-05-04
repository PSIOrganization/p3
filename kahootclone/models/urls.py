'''
File: urls.py
Contains all the urls relevant to the kahootclone project
'''

from django.urls import path
from . import views

urlpatterns = [
     path('signup', views.SignUp.as_view(), name='signup'),
]
