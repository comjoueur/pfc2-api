
from django.urls import path
from pfc1.core import views
from pfc1.core import consumers


urlpatterns = [
    path('', views.pacman_view),
]

websocket_urlpatterns = [
    path('socket_action/', consumers.ActionConsumer.as_asgi()),
]
