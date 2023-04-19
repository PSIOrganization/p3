from django.shortcuts import render
from rest_framework import viewsets
from .models import Participant, Game, Guess


class ParticipantView(viewsets.ModelViewSet):
    def post(self, request):
        context = request.POST.get('context')
        