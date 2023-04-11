from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import View

from .models import User


# Create your views here.
# The views (views.py) must be implemented using classes.


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class SignUp(View):

    http_method_names = ['get', 'post', 'head']

    def get(self, request):
        form = MyUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
