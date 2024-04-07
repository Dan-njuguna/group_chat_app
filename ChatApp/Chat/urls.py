from django.contrib import admin
from django.urls import path, include
from django.core import exceptions
from channels.routing import URLRouter, ProtocolTypeRouter
from . import views

urlpatterns = [
    path("Chat/", include("Chat.urls")),
    # path("login/", views.LoginView, name="login"),
    path("admin/", admin.sites.urls),
]