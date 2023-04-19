# in case we need it, we are not sure yet
from rest_framework import serializers
from models.models import Participant, Game, Guess


# class ParticipantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Participant
#         # fields = ['id', 'nombre', 'apellido', 'email']
#         fields = '__all__'
