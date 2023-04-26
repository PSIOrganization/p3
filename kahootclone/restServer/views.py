from django.shortcuts import render
from rest_framework import viewsets

from models.models import Participant, Game, Guess, Question, Answer
from .serializers import ParticipantSerializer
from .serializers import GameSerializer
from .serializers import GuessSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins

from models.constants import QUESTION

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
        game_exists = Game.objects.filter(publicId=data['game']).exists()
        if not game_exists:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
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

        