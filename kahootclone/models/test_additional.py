'''
File: test_additional.py
Defines some additional tests for the models
'''

from django.test import TestCase
from django.test.client import Client
import random
import string

from .models import User as User
from .models import Questionnaire as Questionnaire
from .models import Question as Question
from .models import Answer as Answer
from .models import Game as Game
from .models import Participant as Participant
from .models import Guess as Guess
# we assume the different states are defined in constants.py
from .constants import WAITING, ANSWER

from django.urls import reverse


class AdditionalTests(TestCase):
    """Test additional functionalities of the models"""

    def create_check(self, dictionary, ObjectClass, check=True):
        """ create an object of the class 'ObjectClass'
        using the dictionary. Then,
        check that all key-values in the
        dictionary are attributes in the object.
        return created object of class Object
        """
        # create object
        item = ObjectClass.objects.create(**dictionary)
        if check:
            # check that str function exists
            self.assertTrue(ObjectClass.__str__ is not object.__str__)
            for key, value in dictionary.items():
                self.assertEqual(getattr(item, key), value)
            # execute __str__() so all the code in models.py is checked
            item.__str__()
        return item

    def test_questionnaire(self):
        """
        additional functionality of Questionnaire
        @author: José Manuel López-Serrano Tapia
        """
        questionnaire = self.createQuestionnaire(
            check=False)

        self.assertEqual(questionnaire.get_absolute_url(),
                         '/kahoot-clone/questionnaire/' +
                         str(questionnaire.id) + '/')
        self.assertEqual(questionnaire.getUser(), questionnaire.user)

    def test_answer(self):
        """
        additional functionality of Answer
        @author: Elena Balseiro García
        """
        answer = self.createAnswer(check=False)
        answer.set_correct(False)
        self.assertFalse(answer.get_correct())

    def test_game(self):
        """
        additional functionality of Game
        @author: José Manuel López-Serrano Tapia
        """
        game = self.createGame(check=False)
        game.set_state(ANSWER)
        self.assertEqual(game.state, game.get_state())
        game.bump_question()
        self.assertEqual(game.questionNo, 1)

    def test_signup(self):
        """
        additional functionality of signUp view
        @author: Elena Balseiro García
        """
        client = Client()
        response = client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        user = {'username': 'testuser',
                'password1': 'testpassword',
                'password2': 'doesnotmatch',
                }
        response = client.post(reverse('signup'), user, follow=True)

        # check that it redirects to the same page
        self.assertEqual(response.status_code, 200)
        # check that error message is present
        self.assertNotEqual(response.content.decode('utf-8').find(
            'The two password fields didn’t match.'), -1)

    def createQuestionnaire(self, check):
        def randStr(chars=string.ascii_uppercase + string.digits, N=10):
            return ''.join(random.choice(chars) for _ in range(N))

        self.userDict = {"username": randStr(),
                         "password": 'a',
                         "first_name": 'a',
                         "last_name": 'a',
                         "email": 'a@aa.es'}
        user = User.objects.create_user(**self.userDict)
        questionnaireDict = {
            'title': 'questionnaire_title',
            'user': user
            }

        return self.create_check(questionnaireDict, Questionnaire, check)

    def createQuestion(self, check):
        questionnaire = self.createQuestionnaire(False)
        questionDict = {
            'question': 'question_text',
            'questionnaire': questionnaire,
            'answerTime': 20,
            }
        return self.create_check(questionDict, Question, check)

    def createAnswer(self, check):
        question = self.createQuestion(check=True)
        answerDict = {
            'answer': 'answer_text',
            'question': question,
            'correct': True,
            }
        return self.create_check(answerDict, Answer, check)

    def createGame(self, check):
        questionnaire = self.createQuestionnaire(check=False)
        gameDict = {
            'questionnaire': questionnaire,
            'state': WAITING,
            'countdownTime': 10,
            'questionNo': 0,
            }
        return self.create_check(gameDict, Game, check)

    def createParticipant(self, check):
        game = self.createGame(check=False)
        participantDict = {
            'game': game,
            'alias': 'mialias',
            'points': 0,
            }
        return self.create_check(participantDict, Participant, check)

    def createGuess(self, check):
        game = self.createGame(check=False)
        participant = self.createParticipant(check=False)
        answer = self.createAnswer(check=False)
        question = self.createQuestion(check=False)
        guessDict = {
            'game': game,
            'participant': participant,
            'question': question,
            'answer': answer,
            }
        return self.create_check(guessDict, Guess, check)
