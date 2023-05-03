from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from models.models import (Game, Guess, Participant,
                           User, Questionnaire, Question, Answer)
from rest_framework.reverse import reverse
import json
from models.constants import QUESTION, LEADERBOARD
###################
# You may modify the following variables
    # default API names
    # URL Style           HTTP Method	Action	       alias
    # {prefix}/           GET	        list	       {basename}-list
    #                     POST	        create
    # {prefix}/{lookup}/  GET	        retrieve	   {basename}-detail
    #                     PUT	        update
    #                     PATCH	        partial_update
    #                     DELETE	    destroy
# rest API service alias
GAME_DETAIL = "game-detail"
GAME_LIST = "game-list"

PARTICIPANT_DETAIL = "participant-detail"
PARTICIPANT_LIST = "participant-list"

GUESS_DETAIL = "guess-detail"
GUESS_LIST = "guess-list"


# these are the error messages returned by the application in
# different contexts.
GUESS_ERROR = 'wait until the question is shown'
GUESS_DELETE_ERROR = "Authentication credentials were not provided."
GUESS_UPDATE_ERROR = "Authentication credentials were not provided."
GUESS_CREATE_ERROR = "Authentication credentials were not provided."

PARTICIPANT_UPDATE_ERROR = "Authentication credentials were not provided."
PARTICIPANT_DELETE_ERROR = "Authentication credentials were not provided."
PARTICIPANT_LIST_ERROR = "Authentication credentials were not provided."

# PLease do not modify anything below this line
###################


class RestTests(APITestCase):
    """ tests for the rest framework
    """

    def setUp(self):
        # ApiClient acts as a dummy web browser, allowing you to test your views 
        # and interact with your Django application programmatically.
        self.client = APIClient()
        # create user
        self.userDict = {"username": 'a',
                         "password": 'a',
                         "first_name": 'a',
                         "last_name": 'a',
                         "email": 'a@aa.es'
                         }
        user, created = User.objects.get_or_create(**self.userDict)
        # save password encripted
        if created:
            user.set_password(self.userDict['password'])
            user.save()
        self.user = user

        # create questionnaire
        self.questionnaireDict = {"title": 'questionnaire_title',
                                  "user": self.user
                                  }
        self.questionnaire = Questionnaire.objects.get_or_create(
            **self.questionnaireDict)[0]

        # create a few questions
        # question 1
        self.questionDict = {"question": 'this is a question',
                             "questionnaire": self.questionnaire,
                             }
        self.question = Question.objects.get_or_create(**self.questionDict)[0]

        # question2
        self.questionDict2 = {"question": 'this is a question2',
                              "questionnaire": self.questionnaire,
                              }
        self.question2 = Question.objects.get_or_create(
            **self.questionDict2)[0]

        # create a few answers
        # answer1
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

        # answer3
        self.answerDict3 = {"answer": 'this is an answer3',
                            "question": self.question2,
                            "correct": True
                            }
        self.answer3 = Answer.objects.get_or_create(**self.answerDict3)[0]

        # create a game
        self.gameDict = {
            'questionnaire': self.questionnaire,
            'publicId': 123456,
        }
        self.game = Game.objects.get_or_create(**self.gameDict)[0]

        # create a participant
        self.participantDict = {
            'game': self.game,
            'alias': "pepe"}
        self.participant = Participant.objects.get_or_create(
            **self.participantDict)[0]

        # create a guess
        self.guessDict = {
            'participant': self.participant,
            'game': self.game,
            'question': self.question,
            'answer': self.answer,
            }
        self.guess = Guess.objects.get_or_create(**self.guessDict)[0]

    @classmethod
    def decode(cls, txt):
        """convert the html return by the client in something that may 
           by printed on the screen"""
        return txt.decode("utf-8")

    # ==== participant ====
    def test_participant_additional(self):
        "add participant"
        url = reverse(PARTICIPANT_LIST)
        data = {'game': 666,  # does not exist
                'alias': "luis"}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ==== GUESS ===
    def test_guess_additional(self):
        " add a guess additional functionality"
        # print("this")
        url = reverse(GUESS_LIST)
        self.game.questionNo = self.game.questionNo + 1
        self.game.state = QUESTION
        self.game.save()
        data = {'uuidp': self.participant.uuidP,
                'game': self.gameDict['publicId'],
                'answer': 3,
                }
        response = self.client.post(path=url, data=data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.game.state = LEADERBOARD
        self.game.save()
        response = self.client.post(path=url, data=data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data2 = {'uuidp': '',
                 'game': self.gameDict['publicId'],
                 'answer': 1,
                 }
        response = self.client.post(path=url, data=data2, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
