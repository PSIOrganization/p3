# created by R. Marabini
# on lun ago 22 11:14:51 CEST 2022
from django.test import TestCase
from django.test.client import Client
import random
import string

from models.models import User as User
from models.models import Questionnaire as Questionnaire
from models.models import Question as Question
from models.models import Answer as Answer
from models.models import Game as Game
from models.models import Participant as Participant
from models.models import Guess as Guess
# we assume the different states are defined in constants.py
from models.constants import WAITING

from django.urls import reverse

from .views import GameCreate


class AdditionalTests(TestCase):
    """Test additional functionalities of the models"""

    def checkLogin(self, SERVICE, KEY, args=None):
        """ log in and check key is in response when user is logged"""
        client = Client()
        # log-in
        response = client.post(reverse('login'),
                               self.userDict, follow=True)
        # after login session user should exist
        self.assertTrue(response.context['user'].is_active)
        if args is None:
            response = client.get(
                reverse(SERVICE), follow=True)
        else:
            response = client.get(
                reverse(SERVICE, args=args), follow=True)

        # latest_questionnaire_list should exist
        if KEY != "DO_NOT_CHECK_KEY":
            self.assertTrue(KEY in response.context)
        return response

    def setUp(self):
        # user
        self.userDict = {"username": 'a',
                         "password": 'a',
                         "first_name": 'a',
                         "last_name": 'a',
                         "email": 'a@aa.es'
                         }
        user, created = User.objects.get_or_create(**self.userDict)
        if created:
            user.set_password(self.userDict['password'])
            user.save()
        self.user = user

        # first questionnaire
        self.questionnaireDict1 = {"title": 'questionnaire_title1',
                                   "user": self.user
                                   }
        self.questionnaire1 = Questionnaire.objects.get_or_create(
            **self.questionnaireDict1)[0]

        # question
        self.questionDict = {"question": 'this is a question',
                             "questionnaire": self.questionnaire1,
                             }
        self.question = Question.objects.get_or_create(**self.questionDict)[0]

        # question2
        self.questionDict2 = {"question": 'this is a question2',
                              "questionnaire": self.questionnaire1,
                              }
        self.question2 = Question.objects.get_or_create(
            **self.questionDict2)[0]

        # answer
        self.answerDict = {"answer": 'this is an answer',
                           "question": self.question,
                           "correct": True
                           }
        self.answer = Answer.objects.get_or_create(**self.answerDict)[0]

        # answer2
        self.answerDict2 = {"answer": 'this is an answer2',
                            "question": self.question,
                            "correct": False
                            }
        self.answer2 = Answer.objects.get_or_create(**self.answerDict2)[0]

        # second questionnaire
        self.questionnaireDict2 = {"title": 'questionnaire_title2',
                                   "user": self.user
                                   }
        self.questionnaire2 = Questionnaire.objects.get_or_create(
            **self.questionnaireDict2)[0]

        # question3
        self.questionDict3 = {"question": 'this is a question3',
                              "questionnaire": self.questionnaire2,
                              }
        self.question3 = Question.objects.get_or_create(
            **self.questionDict3)[0]

        # answer3
        self.answerDict3 = {"answer": 'this is an answer3',
                            "question": self.question3,
                            "correct": False
                            }
        self.answer3 = Answer.objects.get_or_create(**self.answerDict3)[0]

    def test_gameCreate(self):
        id = self.questionnaire1.id
        args = [str(id)]

        # validate first defective questionnaire
        ret = GameCreate.validate(self, self.questionnaire1)
        self.assertFalse(ret)

        # validate second defective questionnaire
        ret = GameCreate.validate(self, self.questionnaire2)
        self.assertFalse(ret)

        # show error message for first defective questionnaire
        response = self.checkLogin(
            'game-create', 'DO_NOT_CHECK_KEY', args=args)
        self.assertNotEqual(response.content.decode('utf-8').find(
            "invalid questionnaire"), -1)
