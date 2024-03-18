"""
ASGI config for ChatApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.urls import path
import Chat.routing
from Chat.consumers import ChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatApp.settings")

asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_app,

    #Websocket for Chat being handled
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("Chat/", ChatConsumer.as_asgi())
                ]),
        ),
    ),
})