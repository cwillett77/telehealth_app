from django.urls import re_path
from .consumers import MyConsumer  # Ensure this is your correct consumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/$', MyConsumer.as_asgi()),
]
