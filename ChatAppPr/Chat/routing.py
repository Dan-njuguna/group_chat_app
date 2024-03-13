from django.contrib import admin
from django.urls import path, include
from Chat.consumers import ChatConsumer

urlpatterns = [
	path('admin/', admin.site.urls),
	path("", include("chat.urls")),
    path("", ChatConsumer.as_asgi()),
]
