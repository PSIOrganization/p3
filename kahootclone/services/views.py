'''
File: views.py
Defines the views of the application
'''

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, ListView, DetailView
from django.template import loader
from models.models import Questionnaire, Question, Answer, Game, Participant
from models.constants import WAITING, QUESTION, ANSWER, LEADERBOARD
import faker


class HomePage(View):
    """
    Home page of the application
    """

    def get(self, request):
        """
        Get the home page
        @param request: request
        @return: home page
        @author: Elena Balseiro García
        """
        template = loader.get_template('home.html')

        if request.user.is_authenticated:
            last_questionnaires = Questionnaire.objects.filter(
                user=request.user)[:5]
            context = {
                'last_questionnaires': last_questionnaires,
            }
            return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(None, request))


class QuestionnaireListView(LoginRequiredMixin, ListView):
    '''
    List of questionnaires
    '''
    model = Questionnaire
    context_object_name = 'questionnaire_list'
    template_name = 'models/questionnaire_list.html'

    def get_queryset(self):
        '''
        Get the questionnaires of the user
        @return: questionnaires of the user
        @author: José Manuel López-Serrano Tapia
        '''
        return Questionnaire.objects.filter(user=self.request.user)


class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    '''
    Create a questionnaire
    '''
    model = Questionnaire
    fields = ['title']
    success_url = reverse_lazy('questionnaire-list')

    def form_valid(self, form):
        '''
        Associate the user to the questionnaire
        @param form: form
        @return: form valid or not valid
        @author: Elena Balseiro García
        '''
        form.instance.user = self.request.user
        return super(QuestionnaireCreate, self).form_valid(form)


class QuestionnaireUpdate(LoginRequiredMixin, UpdateView):
    '''
    Update a questionnaire
    '''
    model = Questionnaire
    fields = ['title']


class QuestionnaireDelete(LoginRequiredMixin, DeleteView):
    '''
    Delete a questionnaire
    '''
    model = Questionnaire
    success_url = reverse_lazy('questionnaire-list')


class QuestionnaireDetailView(LoginRequiredMixin, DetailView):
    '''
    Detail of a questionnaire
    '''

    model = Questionnaire

    def get_context_data(self, **kwargs):
        '''
        Get the context data
        @param kwargs: keyword arguments
        @return: context data with the questions of the questionnaire
        @author: José Manuel López-Serrano Tapia
        '''
        context = super(QuestionnaireDetailView,
                        self).get_context_data(**kwargs)
        context['question_list'] = Question.objects.filter(
            questionnaire=self.object)
        return context


class QuestionCreate(LoginRequiredMixin, CreateView):
    '''
    Create a question
    '''
    model = Question
    fields = ['question', 'answerTime']

    def form_valid(self, form):
        '''
        Associate the questionnaire to the question
        @param form: form
        @return: form valid or not valid
        @author: Elena Balseiro García
        '''
        # asociar questionnaire_id al cuestionario
        questionnaire_id = self.kwargs['pk']
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        form.instance.questionnaire = questionnaire
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        '''
        Get the success url
        @return: success url to the questionnaire detail view
        @author: José Manuel López-Serrano Tapia
        '''
        questionnaire_id = self.object.questionnaire.id
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': questionnaire_id})


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    '''
    Update a question
    '''
    model = Question
    fields = ['question', 'answerTime']

    def get_success_url(self):
        '''
        Get the success url
        @return: success url to the questionnaire detail view
        @author: José Manuel López-Serrano Tapia
        '''
        questionnaire_id = self.object.questionnaire.id
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': questionnaire_id})


class QuestionDelete(LoginRequiredMixin, DeleteView):
    '''
    Delete a question
    '''
    model = Question

    def get_success_url(self):
        '''
        Get the success url
        @return: success url to the questionnaire detail view
        @author: Elena Balseiro García
        '''
        questionnaire_id = self.object.questionnaire.id
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': questionnaire_id})


class QuestionDetailView(LoginRequiredMixin, DetailView):
    '''
    Detail of a question
    '''
    model = Question

    def get_context_data(self, **kwargs):
        '''
        Get the context data
        @param kwargs: keyword arguments
        @return: context data with the answers of the question and the number
        of answers of the question
        @author: José Manuel López-Serrano Tapia
        '''
        context = super(QuestionDetailView,
                        self).get_context_data(**kwargs)
        context['answer_list'] = Answer.objects.filter(
            question=self.object)
        context['number_answers'] = context['answer_list'].count()
        return context


class AnswerCreate(LoginRequiredMixin, CreateView):
    '''
    Create an answer
    '''
    model = Answer
    fields = ['answer', 'correct']  # just one correct answer

    def form_valid(self, form):
        '''
        Associate the question to the answer
        @param form: form
        @return: form valid or not valid
        @author: Elena Balseiro García
        '''
        question_id = self.kwargs['pk']
        question = get_object_or_404(Question, pk=question_id)
        form.instance.question = question
        return super(AnswerCreate, self).form_valid(form)

    def get_success_url(self):
        '''
        Get the success url
        @return: success url to the question detail view
        @author: José Manuel López-Serrano Tapia
        '''
        question_id = self.object.question.id
        return reverse_lazy('question-detail',
                            kwargs={'pk': question_id})


class AnswerUpdate(LoginRequiredMixin, UpdateView):
    '''
    Update an answer
    '''
    model = Answer
    fields = ['answer', 'correct']

    def get_success_url(self):
        '''
        Get the success url
        @return: success url to the question detail view
        @author: Elena Balseiro García
        '''
        question_id = self.object.question.id
        return reverse_lazy('question-detail',
                            kwargs={'pk': question_id})


class AnswerDelete(LoginRequiredMixin, DeleteView):
    '''
    Delete an answer
    '''
    model = Answer

    def get_success_url(self):
        '''
        Get the success url
        @return: success url to the question detail view
        @author: José Manuel López-Serrano Tapia
        '''
        question_id = self.object.question.id
        return reverse_lazy('question-detail',
                            kwargs={'pk': question_id})


class GameCreate(LoginRequiredMixin, View):
    '''
    Create a game and redirect to the game page
    '''

    model = Game

    def validate(self, questionnaire):
        '''
        Validate that the questionnaire is valid
        @param questionnaire: questionnaire to validate
        @return: True if the questionnaire is valid, False otherwise
        @author: Elena Balseiro García
        '''
        question_list = Question.objects.filter(questionnaire=questionnaire)
        if question_list.count() <= 0:
            return False

        for question in question_list:
            answer_list = Answer.objects.filter(question=question)
            if answer_list.count() < 1 or answer_list.count() > 4:
                return False
            correct_answer = Answer.objects.filter(question=question,
                                                   correct=True)
            if correct_answer.count() != 1:
                return False

        return True

    def get(self, request, **kwargs):
        '''
        Create a game and redirect to the game page
        @param request: request
        @param kwargs: keyword arguments
        @return: redirect to the game page or error page if the questionnaire
        is not valid or the user is not the owner of the questionnaire
        @author: José Manuel López-Serrano Tapia
        '''
        questionnaire = Questionnaire.objects.get(id=self.kwargs['pk'])
        context = dict()
        if not self.validate(questionnaire):
            context['questionnaire_id'] = self.kwargs['pk']
            context['error'] = "invalid questionnaire, please check that"
            context['error2'] = "  - there is at least a question"
            context['error3'] = "  - there is at least an answer per question"
            error4 = "  - there is exactly one correct answer per question"
            context['error4'] = error4
            return render(request, 'errors/invalid_questionnaire.html',
                          context)
        if request.user != questionnaire.user:
            context['error_message'] = "does not belong to logged user"
            context['questionnaire'] = questionnaire
            return render(request, 'errors/not_your_game.html', context)
        context['game'] = Game(questionnaire=questionnaire)
        context['game'].save()
        request.session['publicid'] = context['game'].publicId
        request.session['game_state'] = context['game'].state
        return render(request, 'game_create.html', context)


class GameUpdateParticipant(View):
    '''
    This view is used to update the participant
    '''

    def get(self, request, **kwargs):
        '''
        This view is used to update the participant
        @param request: the request
        @param kwargs: the keyword arguments
        @author: Elena Balseiro García
        '''
        if 'publicid' not in request.session:
            context = dict()
            context['error_message'] = "does not belong to logged user"
            return render(request, 'errors/not_your_game.html', context)

        game = Game.objects.get(publicId=request.session['publicid'])
        faker_name = faker.Faker()

        random_participant = Participant(game=game, alias=faker_name.word())
        random_participant.save()
        participant_list = Participant.objects.filter(game=game)
        string = ""
        for participant in participant_list:
            string += str(participant) + "\n"
        return HttpResponse(str(string))


class GameCountdown(View):
    '''
    This view is used to monitor the game
    '''

    def get(self, request, **kwargs):
        '''
        This view is used to monitor the game
        @param request: the request
        @param kwargs: the keyword arguments
        @return: the rendered template appropriate in each case
        @author: José Manuel López-Serrano Tapia
        '''
        current_game = Game.objects.get(publicId=request.session['publicid'])
        current_state = current_game.get_state()
        if current_state == WAITING:
            request.session['game_state'] = QUESTION
            current_game.set_state(QUESTION)
            current_game.save()
            return render(request, 'game/countdown.html')
        elif current_state == QUESTION:
            question_list = Question.objects.filter(
                questionnaire=current_game.questionnaire)
            current_question = question_list[current_game.questionNo]
            answer_list = Answer.objects.filter(question=current_question)

            context = dict()
            context['question'] = current_question
            context['answer_list'] = answer_list

            request.session['game_state'] = ANSWER
            current_game.set_state(ANSWER)
            current_game.save()
            return render(request, 'game/question.html', context)
        elif current_state == ANSWER:
            question_list = Question.objects.filter(
                questionnaire=current_game.questionnaire)
            current_question = question_list[current_game.questionNo]
            correct_answer = Answer.objects.get(question=current_question,
                                                correct=True)
            context = dict()
            context['question'] = current_question
            context['correct_answer'] = correct_answer

            if question_list.count() == current_game.questionNo + 1:
                request.session['game_state'] = LEADERBOARD
                current_game.set_state(LEADERBOARD)
                current_game.save()
                context['final'] = True
                return render(request, 'game/answer.html', context)
            request.session['game_state'] = QUESTION
            current_game.set_state(QUESTION)
            current_game.bump_question()
            current_game.save()
            return render(request, 'game/answer.html', context)
        elif current_state == LEADERBOARD:
            return render(request, 'game/leaderboard.html')
