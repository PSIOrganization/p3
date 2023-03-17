from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    '''Default user class, just in case we want
    to add something extra in the future'''
    #  remove pass command if you add something here
    pass

