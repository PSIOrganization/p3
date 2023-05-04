'''
File: serializers.py
Contains the serializers for the rest server, it is used to serialize the
models and control the data that is sent to the client.
'''

from rest_framework import serializers
from models.models import Participant, Game, Guess


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        '''
        This class is used to serialize the participant model
        '''
        model = Participant
        fields = ['alias', 'game', 'uuidP']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        '''
        This class is used to serialize the game model
        '''
        model = Game
        fields = ['questionnaire', 'created_at', 'publicId', 'state',
                  'questionNo']


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        '''
        This class is used to serialize the guess model
        '''
        model = Guess
        fields = ['participant', 'game', 'question', 'answer']
