'''
File: populate.py
Populates the database with random data
'''

import os

import django

import random

from django.core.management.base import BaseCommand
from models.models import User as User
from models.models import Questionnaire as Questionnaire
from models.models import Question as Question
from models.models import Answer as Answer
from models.models import Game as Game

from faker import Faker
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kahootclone.settings')
django.setup()

# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly


class Command(BaseCommand):
    """
    This class is compulsory, do not change its name
    """
    help = """populate kahootclone database"""

    # if you want to pass an argument to the function
    # uncomment this line
    # def add_arguments(self, parser):
    #    parser.add_argument('publicId',
    #        type=int,
    #        help='game the participants will join to')
    #    parser.add_argument('sleep',
    #        type=float,
    #        default=2.,
    #        help='wait this seconds until inserting next participant')

    def __init__(self, sneaky=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # "if 'RENDER'" allows you to deal with different
        # behaviour in render.com and locally
        # That is, we check a variable ('RENDER')
        # that is only defined in render.com
        if 'RENDER' in os.environ:
            pass
        else:
            pass

        self.N_QUESTIONNARIES = 2
        self.N_QUESTIONS = 6
        self.N_ANSWERS = 20
        self.N_GAMES = 5

    # handle is another compulsory name, do not change it"
    # handle function will be executed by 'manage populate'
    def handle(self, *args, **kwargs):
        """
        This function will be executed by 
        """

        self.cleanDataBase()   # clean database
        # The faker.Faker() creates and initializes a faker generator,
        self.faker = Faker()
        self.user()  # create users
        self.questionnaire()  # create questionaries
        self.question()  # create questions
        self.answer()  # create answers
        self.assign_correct_answer()  # set one correct answer per question
        self.game()  # create games

    def cleanDataBase(self):
        """
        Clean the database before inputting new data
        """
        User.objects.all().delete()

    def user(self):
        """
        Create two random users and insert them
        """
        print("Users")

        usernames = self.faker.words(2)
        password1, password2 = self.faker.password(), self.faker.password()

        user1 = User(username=usernames[0], password=make_password(password1))
        user2 = User(username=usernames[1], password=make_password(password2))
        user1.save()
        user2.save()
        print(" -> " + usernames[0] + ", with password " + password1)
        print(" -> " + usernames[1] + ", with password " + password2)

    def questionnaire(self):
        """
        Create N_QUESTIONNARIES and insert them
        """
        print("Questionnaires")
        questionnaires = self.faker.words(self.N_QUESTIONNARIES)
        # assign users randomly to the questionnaires
        items = list(User.objects.all())

        for i in range(len(questionnaires)):
            random_user = random.choice(items)
            questionnaire = Questionnaire(title=questionnaires[i],
                                          user=random_user)
            questionnaire.save()
            print(" -> " + str(questionnaire) + ", assigned to: " +
                  str(questionnaire.getUser().get_username()))

    def question(self):
        """
        Insert questions, assign randomly to questionnaires
        """
        print("Questions")
        items = list(Questionnaire.objects.all())
        for _ in range(self.N_QUESTIONS):
            q = self.faker.text(20)
            q = q.replace(".", "?")
            # print(questions)
            random_questionnaire = random.choice(items)
            question = Question(question=q, questionnaire=random_questionnaire,
                                answerTime=random.randint(5, 10))
            question.save()
            print(" -> \"" + str(q) + "\", assigned to questionnaire: " +
                  str(random_questionnaire) + ", answerTime: " +
                  str(question.answerTime))

    def answer(self):
        """
        Insert answers, one of them must be the correct one
        """
        print("Answers")
        # your code goes here
        items = list(Question.objects.all())
        for _ in range(self.N_ANSWERS):
            a = self.faker.word()
            # print(questions)
            random_question = random.choice(items)
            answer = Answer(answer=a, question=random_question, correct=False)
            answer.save()

            n_answers = Answer.objects.filter(question=random_question).count()
            print(" -> \"" + str(a) + "\" assigned to question: \"" +
                  str(random_question) + "\"")
            if n_answers == 4:
                print("[question removed]")
                items.remove(random_question)

    def assign_correct_answer(self):
        """
        Sets correct answer
        """
        print("Correct answer for each question")
        items = list(Question.objects.all())
        for question in items:
            answers = Answer.objects.filter(question=question)
            n_answers = answers.count()
            if n_answers == 0:
                print(" -> \"" + str(question) + "\" has no answers")
            else:
                true_answer = random.choice(answers)
                true_answer.set_correct(True)
                true_answer.save()
                print(" -> \"" + str(question) + "\" has as correct answer \""
                      + str(true_answer) + "\"")

    def game(self):
        """
        Creates a game by assigning random questionnaires
        """
        print("Game")
        # assign users randomly to the questionnaires
        items = list(Questionnaire.objects.all())

        for _ in range(self.N_GAMES):
            random_q = random.choice(items)
            game = Game(questionnaire=random_q)
            game.save()
            print(" -> Questionnaire \"" + str(random_q) +
                  "\" assigned to game \"" + str(game) + "\"")
