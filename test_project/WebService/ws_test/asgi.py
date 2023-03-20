import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from engine_side.middleware import JwtAuthMiddlewareStack # Это я попытался реализовать самопизную авторизацию. Для использования подставить вместо Authmiddlewarestack, 
from engine_side import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ws_test.settings')
django.setup()

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),)
})