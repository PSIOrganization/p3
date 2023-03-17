import datetime
from django.shortcuts import render

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import get_object_or_404
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
