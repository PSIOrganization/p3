# Populate database
# This file has to be placed within the
# catalog/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate
#
# use module Faker generator to generate data
# (https://zetcode.com/python/faker/)
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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kahootclone.settings')
django.setup()

N_QUESTIONNAIRES = 2
N_QUESTIONS = 6
N_ANSWERS = 20
N_GAMES = 2

# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
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

        self.NUMBERUSERS = 4
        self.NUMBERQESTIONARIES = 30
        self.NUMBERQUESTIONS = 100
        self.NUMBERPARTICIPANTS = 20
        self.NUMBERANSWERPERQUESTION = 4
        self.NUMBERGAMES = 4

    # handle is another compulsory name, do not change it"
    # handle function will be executed by 'manage populate'
    def handle(self, *args, **kwargs):
        "this function will be executed by default"

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
        # delete all models stored (clean table)
        # in database
        # order in which data is deleted is important
        # your code goes here...
        print("clean Database")

        User.objects.all().delete()
        print(Questionnaire.objects.all().count())
        print(Question.objects.all().count())
        print(Answer.objects.all().count())
        print(Game.objects.all().count())

    def user(self):
        " Insert users"
        # create user
        print("Users")

        usernames = self.faker.words(2)
        password1, password2 = self.faker.password(), self.faker.password()

        user1 = User(username=usernames[0], password=password1)
        user2 = User(username=usernames[1], password=password2)
        user1.save()
        user2.save()
        print(" -> " + str(user1))
        print(" -> " + str(user2))

    def questionnaire(self):
        "insert questionnaires"
        print("Questionnaires")
        questionnaires = self.faker.words(N_QUESTIONNAIRES)
        # assign users randomly to the questionnaires
        items = list(User.objects.all())

        for i in range(len(questionnaires)):
            random_user = random.choice(items)
            questionnaire = Questionnaire(title=questionnaires[i],
                                          user=random_user)
            questionnaire.save()
            print(" -> " + str(questionnaire) + ", assigned to: " +
                  str(questionnaire.getUser()))

    def question(self):
        " insert questions, assign randomly to questionnaires"
        print("Questions") 
        items = list(Questionnaire.objects.all())
        for _ in range(N_QUESTIONS):
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
        "insert answers, one of them must be the correct one"
        print("Answers")
        # your code goes here
        items = list(Question.objects.all())
        for _ in range(N_ANSWERS):
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
                print(" -> \"" + str(question) + "\" has as correct answer \""
                      + str(true_answer) + "\"")

    def game(self):
        "insert some games"
        print("Game")
        # assign users randomly to the questionnaires
        items = list(Questionnaire.objects.all())

        for _ in range(N_GAMES):
            random_q = random.choice(items)
            game = Game(questionnaire=random_q)
            game.save()
            print(" -> Questionnaire \"" + str(random_q) + "\" assigned to game \"" +
                  str(game) + "\"")

