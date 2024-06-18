# core/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usersignin.urls')),  # Include URLs from usersignin app
    path('chat/', include('chat.urls')),  # Include URLs from chat
]