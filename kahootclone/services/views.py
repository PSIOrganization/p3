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

from models.models import User, Questionnaire, Question, Answer


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
    context_object_name = 'questionnaire_list'   # your own name for the list as a template variable
    template_name = 'models/questionnaire_list.html'  # Specify your own template name/location

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
    fields = ['title']  # Not recommended
    # (potential security issue if more fields added)


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
