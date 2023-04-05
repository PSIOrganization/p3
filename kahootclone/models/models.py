from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random

from django.urls import reverse
# Create your models here.


class User(AbstractUser):
    '''Default user class, just in case we want
    to add something extra in the future'''
    #  remove pass command if you add something here

    def get_username(self):
        return self.username

    def __str__(self):
        return str(self.username) + ", " + str(self.password)


class Questionnaire(models.Model):
    '''Questionnaire class'''
    # questionnaire_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField('creation', auto_now_add=True)
    updated_at = models.DateTimeField('last-update', auto_now=True)  # default?
    # on_delete?????
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated_at']

    def getUser(self):
        return self.user

    def get_absolute_url(self):
        return reverse('questionnaire-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    '''Question class'''
    # question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=5000)
    # on_delete?????
    questionnaire = models.ForeignKey('Questionnaire',
                                      on_delete=models.CASCADE)
    created_at = models.DateTimeField('creation', auto_now_add=True)
    updated_at = models.DateTimeField('last-update', auto_now=True)
    answerTime = models.IntegerField()

    def __str__(self):
        return str(self.question)


class Answer(models.Model):
    '''Answer class'''
    # answer_id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=5000)
    # on_delete?????
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    correct = models.BooleanField()

    def __str__(self):
        return str(self.answer)

    def set_correct(self, bool):
        self.correct = bool


class Game(models.Model):
    # game_id = models.AutoField(primary_key=True)
    questionnaire = models.ForeignKey('Questionnaire',
                                      on_delete=models.CASCADE)
    created_at = models.DateTimeField('creation', auto_now_add=True)

    class State(models.IntegerChoices):
        WAITING = 1
        QUESTION = 2
        ANSWER = 3
        LEADERBOARD = 4

    state = models.IntegerField(choices=State.choices, default=State.WAITING)
    publicId = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):  # an override
        self.publicId = random.randint(1, 1e6)
        super(Game, self).save(*args, **kwargs)
    countdownTime = models.IntegerField(null=True, blank=True)
    questionNo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        ret = str(self.questionnaire) + ', ' + str(self.publicId)
        return ret


class Participant(models.Model):
    # participant_id = models.AutoField(primary_key=True)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    alias = models.CharField(max_length=20)
    points = models.IntegerField(default=1)
    uuidP = models.UUIDField(default=uuid.uuid4)

    # def save(self, *args, **kwargs):  # turbio
    #     self.points += self.points  # change this
    #     super(Participant, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.alias) + ' ' + str(self.points)


class Guess(models.Model):
    # guess_id = models.AutoField(primary_key=True)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    def __str__(self):
        ret = str(self.answer) + ' ' + str(self.participant)
        ret += ' ' + str(self.question) + ' ' + str(self.game)
        return ret
