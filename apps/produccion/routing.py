#apps/produccion/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('api/notificaciones/', consumers.NotificacionConsumer.as_asgi()),
]
