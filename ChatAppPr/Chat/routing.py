'''
from django.contrib import admin
from django.urls import path, include
from chat.consumers import ChatConsumer

urlpatterns = [
	path('admin/', admin.site.urls),
	path("", include("chat.urls")),
    path("", ChatConsumer.as_asgi()),
]
'''
from django.contrib import admin
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.consumers import ChatConsumer

# Django's traditional URL routing
d_urlpatterns = [
    path('admin/', admin.site.urls),
]

# Channels' routing
channels_urlpatterns = [
    path("", ChatConsumer.as_asgi()),
]

# Combine Django and Channels URL patterns
urlpatterns = URLRouter([
    path("", URLRouter(d_urlpatterns)),
    path("", URLRouter(channels_urlpatterns)),
])
