from channels.routing import ProtocolTypeRouter, URLRouter
from Chat.consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("Chat/", ChatConsumer.as_asgi()),
    ]),
})