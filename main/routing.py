# routing.py

from django.urls import path
from . import consumers  # Импортируйте ваши консумеры

websocket_urlpatterns = [
    path('ws/user/<int:user_id>/', consumers.UserConsumer.as_asgi()),  # URL для WebSocket
]
