'''
File: views.py
Defines the API endpoints for the rest server
'''

from rest_framework import viewsets

from models.models import Participant, Game, Guess, Question, Answer
from .serializers import ParticipantSerializer
from .serializers import GameSerializer
from .serializers import GuessSerializer

from rest_framework import status
from rest_framework.response import Response

from models.constants import QUESTION, LEADERBOARD


class ParticipantViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows participants to be created.
    Any other functionality is not allowed.
    '''
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def create(self, request):
        '''
        Creates a new participant
        @return: response error if the form is not valid
        @return: ok response with participant created if the form is valid
        @author: Elena Balseiro García
        '''
        data = request.data
        game_exists = Game.objects.filter(publicId=data['game']).exists()
        if not game_exists:
            error_message = "Game does not exist"
            return Response(error_message,
                            status=status.HTTP_403_FORBIDDEN)

        game = Game.objects.get(publicId=data['game'])
        if Participant.objects.filter(game=game, alias=data['alias']).exists():
            error_message = "There is a participant with this alias already"
            return Response(error_message,
                            status=status.HTTP_403_FORBIDDEN)
        new_participant = Participant(game=game, alias=data['alias'])
        new_participant.save()
        serializer = ParticipantSerializer(new_participant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        '''
        Returns 403 error message
        @return: error response
        @author: José Manuel López-Serrano Tapia
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def retrieve(self, request, pk):
        '''
        Returns 403 error message
        @return: error response
        @author: Elena Balseiro García
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def destroy(self, request, pk):
        '''
        Returns 403 error message
        @return: error response
        @author: José Manuel López-Serrano Tapia
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)


class GameViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows a game to be retrieved.
    Any other functionality is not allowed.
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'publicId'

    def update(self, request, publicId):
        '''
        Returns 403 error message
        @return: error response
        @author: Elena Balseiro García
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def create(self, request):
        '''
        Returns 403 error message
        @return: error response
        @author: José Manuel López-Serrano Tapia
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def destroy(self, request, publicId):
        '''
        Returns 403 error message
        @return: error response
        @author: Elena Balseiro García
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)


class GuessViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows guesses to be created.
    Any other functionality is not allowed.
    '''
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer

    def create(self, request):
        '''
        Creates a new guess
        @return: response error if the form is not valid
        @return: ok response with guess created
        @author: José Manuel López-Serrano Tapia
        '''
        data = request.data
        print(data)

        # check if participant uuidp exists
        if data['uuidp'] == "":
            error_msg = "Something went wrong, " \
                        "you are not registered in this game!"
            return Response(error_msg,
                            status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.get(publicId=data['game'])

        if game.state != QUESTION:
            if game.state == LEADERBOARD:
                error_msg = "You can't answer anymore, " \
                            "the game is over!"
            else:
                error_msg = "You can't answer yet, " \
                            "wait until the question is shown!"
            return Response(error_msg,
                            status=status.HTTP_403_FORBIDDEN)

        participant = Participant.objects.get(uuidP=data['uuidp'])
        question_list = Question.objects.filter(
            questionnaire=game.questionnaire)
        question = question_list[game.questionNo]

        if Guess.objects.filter(question=question,
                                participant=participant).exists():
            error_msg = "You already answered this question!"
            return Response(error_msg,
                            status=status.HTTP_403_FORBIDDEN)

        answer_list = Answer.objects.filter(question=question)

        if data['answer'] >= len(answer_list):
            error_msg = "Answer does not exist"
            return Response(error_msg,
                            status=status.HTTP_403_FORBIDDEN)
            # change maybe
        answer = answer_list[data['answer']]

        new_guess = Guess(game=game, participant=participant,
                          question=question, answer=answer)
        new_guess.save()
        serializer = GuessSerializer(new_guess)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        '''
        Returns 403 error message
        @return: error response
        @author: Elena Balseiro García
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def retrieve(self, request, pk):
        '''
        Returns 403 error message
        @return: error response
        @author: José Manuel López-Serrano Tapia
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)

    def destroy(self, request, pk):
        '''
        Returns 403 error message
        @return: error response
        @author: Elena Balseiro García
        '''
        error_message = "Authentication credentials were not provided."
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data=error_message)
