'''
File: views.py
Contains the views of the application.
'''

from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import View

from .models import User, Participant, Game, Guess, Question, Answer
from .serializers import ParticipantSerializer
from .serializers import GameSerializer
from .serializers import GuessSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins

from .constants import QUESTION


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


class ParticipantViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be created.
    '''
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def create(self, request):
        '''
        Creates a new participant
        @return: render if the form is not valid
        @return: redirect to home page if the form is valid
        '''
        data = request.data
        game = Game.objects.get(publicId=data['game'])
        if Participant.objects.filter(game=game, alias=data['alias']).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        new_participant = Participant(game=game, alias=data['alias'])
        new_participant.save()
        serializer = ParticipantSerializer(new_participant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        # should not update a participant, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def retrieve(self, request, pk):
        # should not list participants, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def destroy(self, request, pk):
        # should not delete a participant, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)


class GameViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be retrieved.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'publicId'

    def update(self, request, publicId):
        # should not update a participant, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def create(self, request):
        # should not list participants, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def destroy(self, request, publicId):
        # should not delete a participant, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)


class GuessViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be created.
    '''
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer

    def create(self, request):
        '''
        Creates a new guess
        @return: render if the form is not valid
        @return: redirect to home page if the form is valid
        '''
        data = request.data
        game = Game.objects.get(publicId=data['game'])
        participant = Participant.objects.get(uuidP=data['uuidp'])
        question_list = Question.objects.filter(
            questionnaire=game.questionnaire)
        question = question_list[game.questionNo]
        answer_list = Answer.objects.filter(question=question)
        answer = answer_list[data['answer']]
        if game.state != QUESTION:
            info_msg = "wait until the question is shown"
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data=info_msg)

        if Guess.objects.filter(question=question,
                                participant=participant).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        new_guess = Guess(game=game, participant=participant,
                          question=question, answer=answer)
        new_guess.save()
        serializer = GuessSerializer(new_guess)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        # should not update a participant, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def retrieve(self, request, pk):
        # should not list participants, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def destroy(self, request, pk):
        # should not delete a participant, returns error message:
        # "Authentication credentials were not provided."
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)
