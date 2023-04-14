from django.urls import path, include
from services import views
from rest_framework import routers

router = routers.DefaultRouter()

# En el router vamos agnadiendo los endpoints a los viewsets
urlpatterns = [
    path('', include(router.urls)),
]

# Here we will be registering the endpoints
