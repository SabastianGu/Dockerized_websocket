from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/', consumers.TheConsumer.as_asgi()),
    path(r'ws/endpoint/', consumers.UserConsumer.as_asgi())
]