from django.urls import path
from . import views

# Here we will add all urls relevant to the models app

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
]
