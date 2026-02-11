from django.urls import re_path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    re_path("ws/chat/", ChatConsumer.as_asgi()),
]