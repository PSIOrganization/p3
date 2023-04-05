from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('questionnairelist/', views.QuestionnaireListView.as_view(),
         name='questionnaire-list'),
    path('questionnaire/<int:pk>/', views.QuestionnaireDetailView.as_view(),
         name='questionnaire-detail'),
    path('questionnairecreate/', views.QuestionnaireCreate.as_view(),
         name='questionnaire-create'),
    path('questionnaireupdate/<int:pk>/', views.QuestionnaireUpdate.as_view(),
         name='questionnaire-update'),
    path('questionnaireremove/<int:pk>/', views.QuestionnaireDelete.as_view(),
         name='questionnaire-remove'),
]

urlpatterns += [
    path('question/<int:pk>/', views.QuestionDetailView.as_view(),
         name='question-detail'),
    path('questioncreate/<int:pk>/', views.QuestionCreate.as_view(),
         name='question-create'),
    path('questionupdate/<int:pk>/', views.QuestionUpdate.as_view(),
         name='question-update'),
    path('questionremove/<int:pk>/', views.QuestionDelete.as_view(),
         name='question-remove'),
]

urlpatterns += [
    path('answercreate/<int:pk>/', views.AnswerCreate.as_view(),
         name='answer-create'),
    path('answerupdate/<int:pk>/', views.AnswerUpdate.as_view(),
         name='answer-update'),
    path('answerremove/<int:pk>/', views.AnswerDelete.as_view(),
         name='answer-remove'),
]

urlpatterns += [
    path('gamecreate/<int:pk>/', views.GameCreate.as_view(),
         name='game-create'),
    path('gameUpdateParticipant/<int:publicid>/',
         views.GameUpdateParticipant.as_view(),
         name='game-updateparticipant')

]
