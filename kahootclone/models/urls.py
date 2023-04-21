'''
File: urls.py
Contains all the urls relevant to the kahootclone project
'''

from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

# Here we will add all urls relevant to the models app
router.register('participant', views.ParticipantViewSet, 'participant')
router.register('games', views.GameViewSet, 'game')
router.register('guess', views.GuessViewSet, 'guess')

urlpatterns = [
     path('signup', views.SignUp.as_view(), name='signup'),
     path('api/', include(router.urls)),
]
