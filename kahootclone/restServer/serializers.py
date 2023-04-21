# in case we need it, we are not sure yet
from rest_framework import serializers
from models.models import Participant, Game, Guess


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['alias', 'game']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['questionnaire', 'created_at', 'publicId']


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ['participant', 'game', 'question', 'answer']
