'''
File: models.py
Defines the models for the application
'''

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random

from django.urls import reverse


class User(AbstractUser):
    '''Default user class, just in case we want
    to add something extra in the future'''
    #  remove pass command if you add something here

    def get_username(self):
        '''
        Returns username of the user
        @return: username of the user
        @author: Elena Balseiro García
        '''
        return self.username

    def __str__(self):
        '''
        Convert User info to string
        @return string containing username of user
        @author: José Manuel López-Serrano Tapia
        '''
        return str(self.username)


class Questionnaire(models.Model):
    '''Questionnaire class'''
    # questionnaire_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField('creation', auto_now_add=True)
    updated_at = models.DateTimeField('last-update', auto_now=True)  # default?
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated_at']

    def getUser(self):
        '''
        Returns user of the questionnaire
        @return: user of the questionnaire
        @author: José Manuel López-Serrano Tapia
        '''
        return self.user

    def get_absolute_url(self):
        '''
        Returns the url to access a particular instance of the model
        @return: url to access a particular instance of the model
        @author: Elena Balseiro García
        '''
        return reverse('questionnaire-detail', args=[str(self.id)])

    def __str__(self):
        '''
        Convert Questionnaire info to string
        @return string containing the title of the questionnaire
        @author: José Manuel López-Serrano Tapia
        '''
        return str(self.title)


class Question(models.Model):
    '''Question class'''
    # question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=5000)
    questionnaire = models.ForeignKey('Questionnaire',
                                      on_delete=models.CASCADE)
    created_at = models.DateTimeField('creation', auto_now_add=True)
    updated_at = models.DateTimeField('last-update', auto_now=True)
    answerTime = models.IntegerField(null=True, blank=True)

    def __str__(self):
        '''
        Convert Question info to string
        @return string containing the question
        @author: Elena Balseiro García
        '''
        return str(self.question)


class Answer(models.Model):
    '''Answer class'''
    # answer_id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=5000)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    correct = models.BooleanField()

    def __str__(self):
        '''
        Convert Answer info to string
        @return string containing the answer
        @author: Elena Balseiro García
        '''
        return str(self.answer)

    def set_correct(self, bool):
        '''
        Sets correct attribute
        @param bool: boolean value to set correct attribute to
        @author: José Manuél López-Serrano Tapia
        '''
        self.correct = bool

    def get_correct(self):
        '''
        Returns correct attribute
        @return correct attribute
        @author: Elena Balseiro García
        '''
        return self.correct


class Game(models.Model):
    '''Game class'''
    questionnaire = models.ForeignKey('Questionnaire',
                                      on_delete=models.CASCADE)
    created_at = models.DateTimeField('creation', auto_now_add=True)

    class State(models.IntegerChoices):
        WAITING = 1
        COUNTDOWN = 2
        QUESTION = 3
        ANSWER = 4
        LEADERBOARD = 5

    state = models.IntegerField(choices=State.choices, default=State.WAITING)
    publicId = models.IntegerField(unique=True)
    countdownTime = models.IntegerField(null=True, blank=True)
    questionNo = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        '''
        Override save method to generate a random publicId
        @param args: arguments
        @param kwargs: keyword arguments
        @author: José Manuél López-Serrano Tapia
        '''
        if self.publicId is None:
            self.publicId = random.randint(1, 1e6)
        super(Game, self).save(*args, **kwargs)

    def get_state(self):
        '''
        Returns state of the game
        @return: state of the game
        @author: Elena Balseiro García
        '''
        return self.state

    def set_state(self, state):
        '''
        Sets state of the game
        @param state: state of the game
        @author: José Manuél López-Serrano Tapia
        '''
        self.state = state

    def bump_question(self):
        '''
        Bumps the question number
        @author: Elena Balseiro García
        '''
        self.questionNo += 1

    def __str__(self):
        '''
        Convert Game info to string
        @return string containing alias and points of participant
        @author: José Manuél López-Serrano Tapia
        '''
        ret = str(self.questionnaire) + ', ' + str(self.publicId)
        return ret


class Participant(models.Model):
    '''Participant class'''
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    alias = models.CharField(max_length=20)
    points = models.IntegerField(default=0)
    uuidP = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = ['-points']

    def __str__(self):
        '''
        Convert Participant info to string
        @return string containing alias and points of participant
        @author: Elena Balseiro García
        '''
        return str(self.alias) + ' ' + str(self.points)

    def bump_up(self):
        '''
        Bumps up the points of the participant
        @author: José Manuél López-Serrano Tapia
        '''
        self.points += 1


class Guess(models.Model):
    '''Guess class'''
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        '''
        Override save method to bump up points if answer is correct
        @param args: arguments
        @param kwargs: keyword arguments
        @author: José Manuel López-Serrano Tapia
        '''
        if self.answer.get_correct():
            self.participant.bump_up()
            self.participant.save()
        super(Guess, self).save(*args, **kwargs)

    def __str__(self):
        '''
        Convert Guess info to string
        @return string containing answer, participant, question and game of
        Guess
        @author: Elena Balseiro García
        '''
        ret = str(self.answer) + ' ' + str(self.participant)
        ret += ' ' + str(self.question) + ' ' + str(self.game)
        return ret
