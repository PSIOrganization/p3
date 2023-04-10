import datetime
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import View, ListView, DetailView

from django.template import loader

from models.models import User, Questionnaire, Question, Answer, Game, Participant
import random
import faker


# Create your views here.
# The views (views.py) must be implemented using classes.


class HomePage(View):
    """Home page of the application"""

    def get(self, request):
        template = loader.get_template('home.html')

        if request.user.is_authenticated:
            last_questionnaires = Questionnaire.objects.filter(
                user=request.user)[:5]
            context = {
                'last_questionnaires': last_questionnaires,
            }
            return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(None, request))
        # first variable
        # is the variable dictionary to pass to the template


class QuestionnaireListView(LoginRequiredMixin, ListView):
    model = Questionnaire
    context_object_name = 'questionnaire_list'
    template_name = 'models/questionnaire_list.html'

    def get_queryset(self):
        return Questionnaire.objects.filter(user=self.request.user)


class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    model = Questionnaire
    fields = ['title']
    success_url = reverse_lazy('questionnaire-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionnaireCreate, self).form_valid(form)


class QuestionnaireUpdate(LoginRequiredMixin, UpdateView):
    model = Questionnaire
    fields = ['title']


class QuestionnaireDelete(LoginRequiredMixin, DeleteView):
    model = Questionnaire
    success_url = reverse_lazy('questionnaire-list')


class QuestionnaireDetailView(LoginRequiredMixin, DetailView):
    model = Questionnaire

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireDetailView,
                        self).get_context_data(**kwargs)
        context['question_list'] = Question.objects.filter(
            questionnaire=self.object)
        return context


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question', 'answerTime']

    def form_valid(self, form):
        # asociar questionnaire_id al cuestionario
        questionnaire_id = self.kwargs['pk']
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        form.instance.questionnaire = questionnaire
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        questionnaire_id = self.object.questionnaire.id
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': questionnaire_id})


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['question', 'answerTime']

    def get_success_url(self):
        questionnaire_id = self.object.questionnaire.id
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': questionnaire_id})


class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question

    def get_success_url(self):
        questionnaire_id = self.object.questionnaire.id
        return reverse_lazy('questionnaire-detail',
                            kwargs={'pk': questionnaire_id})


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView,
                        self).get_context_data(**kwargs)
        context['answer_list'] = Answer.objects.filter(
            question=self.object)
        context['number_answers'] = context['answer_list'].count()
        return context


class AnswerCreate(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer', 'correct']  # just one correct answer

    def form_valid(self, form):
        question_id = self.kwargs['pk']
        question = get_object_or_404(Question, pk=question_id)
        form.instance.question = question
        return super(AnswerCreate, self).form_valid(form)

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy('question-detail',
                            kwargs={'pk': question_id})


class AnswerUpdate(LoginRequiredMixin, UpdateView):
    model = Answer
    fields = ['answer', 'correct']

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy('question-detail',
                            kwargs={'pk': question_id})


class AnswerDelete(LoginRequiredMixin, DeleteView):
    model = Answer

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy('question-detail',
                            kwargs={'pk': question_id})


class GameCreate(LoginRequiredMixin, View):
    model = Game

    def validate(self, questionnaire):
        # Validate if the questionnaire is valid
        question_list = Question.objects.filter(questionnaire=questionnaire)
        # if question_list.count() <= 0:
        #     return False

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
        questionnaire = Questionnaire.objects.get(id=self.kwargs['pk'])
        if not self.validate(questionnaire):
            return redirect('questionnaire-detail', pk=self.kwargs['pk'])
        context = dict()
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

    def get(self, request, **kwargs):
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
