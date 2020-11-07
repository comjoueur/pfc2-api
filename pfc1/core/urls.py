
from django.urls import path
from pfc1.core import views


urlpatterns = [
    path('', views.pacman_view),
]
