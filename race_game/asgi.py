"""
ASGI config for race_game project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import multiplayer.routing
# from multiplayer.middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'race_game.settings')

application = ProtocolTypeRouter({
    "http"  :get_asgi_application(),
    "websocket" : AuthMiddlewareStack(
        URLRouter(
            multiplayer.routing.websocket_urlpatterns
        )
    ),
})
