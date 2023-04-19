'''
File: views.py
Contains the views of the application.
'''

from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import View

from .models import User

from rest_framework.renderers import JSONRenderer


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class SignUp(View):

    http_method_names = ['get', 'post', 'head']

    def get(self, request):
        '''
        Renders the signup page
        @return: render
        @author: Elena Balseiro García
        '''
        form = MyUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        '''
        Creates a new user
        @return: redirect to home page if the form is valid
        @return: render if the form is not valid
        @author: José Manuel López-Serrano Tapia
        '''
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
