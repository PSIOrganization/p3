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

from .models import User


# Create your views here.
# The views (views.py) must be implemented using classes.


class HomePage(View):
    """Home page of the application"""

    def get(self, request):
        template = loader.get_template('home.html')
        return HttpResponse(template.render(None, request)) 
        # first variable 
        # is the variable dictionary to pass to the template


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class SignUp(View):

    http_method_names = ['get', 'post', 'head']

    # def get(self, request):
    #     template = loader.get_template('signup.html')
    #     return HttpResponse(template.render(None, request)) 

    def get(self, request):
        form = MyUserCreationForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #no hace falta hacer authenticate ya que ya obtenemos el user al guardar el form
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')
        
        