import datetime
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import View, ListView, DetailView

from django.template import loader



# Create your views here.
# The views (views.py) must be implemented using classes.

class HomePage(View):
    """Home page of the application"""

    def get(self, request):
        template = loader.get_template('home.html')
        return HttpResponse(template.render(None, request)) 
        # first variable is the variable dictionary to pass to the template

class SignUp(View):

    def signup(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
            else:
                pass # validation form???????
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    
