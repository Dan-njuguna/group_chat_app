from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('Chat.urls')),  # Include your chat app's URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Include the authentication URLs
]