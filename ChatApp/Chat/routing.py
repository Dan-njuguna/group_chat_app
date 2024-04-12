from channels.routing import ProtocolTypeRouter, URLRouter
from Chat.consumers import ChatConsumer
from django.urls import path
from .views import LoginView as  chat

websocket_urlpatterns = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("/", ChatConsumer.as_asgi()),
    ]),
})