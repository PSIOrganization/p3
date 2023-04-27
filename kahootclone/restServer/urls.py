from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

# Here we will add all urls relevant to the models app
router.register('participant', views.ParticipantViewSet, 'participant')
router.register('games', views.GameViewSet, 'game')
router.register('guess', views.GuessViewSet, 'guess')


# En el router vamos agnadiendo los endpoints a los viewsets
urlpatterns = [
    path('', include(router.urls))
]

# Here we will be registering the endpoints
